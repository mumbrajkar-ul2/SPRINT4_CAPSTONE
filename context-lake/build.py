"""Build context-lake.sqlite3 from YAML. Enforces write-time and build-time gates."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from harvest.common import (
    CORRELATION_ID,
    INHERITED,
    INHERITED_REL,
    KIND_FOLDER,
    LAKE_ROOT,
    REGISTER_PATH,
    WORKSPACE,
    load_register,
    open_ro,
    sha256_file,
)

ITEMS_DIR = LAKE_ROOT / "items"
SEMANTIC_DIR = LAKE_ROOT / "semantic-layer"
SCHEMA_DIR = LAKE_ROOT / "schemas"
GENERATED_DIR = LAKE_ROOT / "generated"
SQLITE_PATH = GENERATED_DIR / "context-lake.sqlite3"
MANIFEST_PATH = GENERATED_DIR / "manifest.json"
PIN_PATH = GENERATED_DIR / "app-b-pin.json"
ENUM_PATH = SCHEMA_DIR / "enums.generated.json"

REQUIRED_KINDS = set(KIND_FOLDER)
REQUIRED_BP = [f"decision.bp{i}" for i in range(1, 9)]
REQUIRED_RULE_CARDS = [
    "rule.recipe_release.limit",
    "rule.recipe_release.no_match",
    "rule.policy.overlap_or_invalid",
    "rule.recipe_release.limit.impl.js",
    "rule.recipe_release.limit.impl.js_default",
    "rule.urgent.amount.impl.python",
    "rule.priority.closed.impl.python",
    "rule.urgent.severity.impl.python",
    "rule.open_closed.operational",
    "rule.open_closed.finance_audit",
    "rule.region.site_canonical",
    "rule.region.specificity",
    "rule.region.disagreement",
    "rule.threshold.silent",
    "rule.month_end.blank.impl.java",
    "rule.month_end.float.impl.java",
    "rule.open_flag.impl.night_batch",
    "rule.night_batch.join_multiply",
    "rule.feed.replay_duplicate",
    "rule.recipe.mismatch_show_both",
    "rule.clock.event_vs_arrival",
    "rule.untrusted_text.block",
    "rule.threshold.never_999999",
    "rule.threshold.demo_50000",
    "rule.hold.person_only",
]
REQUIRED_MAPS = [
    "map.site.IN-BLR",
    "map.site.JP-KN",
    "map.site.US-TX",
    "map.site.BR-SP",
    "map.site.DE-BY",
    "map.site.GB-ENG",
]
INSTRUCTION_RE = re.compile(r"\b(approve|ignore validation|release all holds)\b", re.I)
ROW_DUMP_RE = re.compile(r"\bL000000\d{2}\b")


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def item_validator() -> Draft202012Validator:
    return Draft202012Validator(load_schema("item.schema.json"))


def card_validator() -> Draft202012Validator:
    return Draft202012Validator(load_schema("rule-card.schema.json"))


def term_validator() -> Draft202012Validator:
    return Draft202012Validator(load_schema("term.schema.json"))


def iter_item_files() -> list[Path]:
    files = []
    for path in ITEMS_DIR.rglob("*.yaml"):
        if path.name.endswith(".card.yaml"):
            continue
        files.append(path)
    return files


def iter_card_files() -> list[Path]:
    return list(ITEMS_DIR.rglob("*.card.yaml"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def flatten_terms(payload: Any) -> list[dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "term_id" in payload:
        return [payload]
    if isinstance(payload, dict) and "terms" in payload:
        return payload["terms"]
    raise ValueError("unrecognized term document")


def pragma_catalog() -> tuple[set[str], set[str]]:
    tables: set[str] = set()
    columns: set[str] = set()
    for dbp in (
        INHERITED / "data" / "legacy.sqlite3",
        INHERITED / "data" / "enterprise_legacy.sqlite3",
    ):
        conn = open_ro(dbp)
        for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            tables.add(name)
            for col in conn.execute(f"PRAGMA table_info({name})"):
                columns.add(f"{name}.{col[1]}")
        conn.close()
    return tables, columns


def write_time_check(item: dict[str, Any], path: Path, validator: Draft202012Validator) -> list[str]:
    errors = [e.message for e in validator.iter_errors(item)]
    if path.stem != item.get("id"):
        errors.append(f"file stem {path.stem} does not match id {item.get('id')}")
    if item.get("kind") == "business_rule" and not item.get("authority"):
        errors.append("business_rule missing authority")
    if item.get("trust") == "trusted_code" and "data.injection" in str(item.get("id")):
        errors.append("injection item marked trusted_code")
    if item.get("policy_status") == "decided" and (
        "999999" in item.get("statement", "") and "not" not in item.get("statement", "").lower()
    ):
        if item.get("id") not in {
            "rule.recipe_release.limit.impl.js_default",
            "rule.threshold.never_999999",
        }:
            errors.append("decided item mentions 999999 as a live number")
    if item.get("id") in {"rule.urgent.amount.impl.python", "rule.threshold.demo_50000"}:
        if item.get("policy_status") == "decided":
            errors.append("50000 marked decided")
    if item.get("item_status") == "accepted" and "_drafts" in path.parts:
        errors.append("accepted item still in _drafts")
    if item.get("item_status") == "accepted" and item.get("claim") == "inference":
        if item.get("reviewer") is None and "model draft" in item.get("statement", "").lower():
            errors.append("model-drafted accepted without reviewer")
    if ROW_DUMP_RE.search(item.get("statement", "")):
        errors.append("statement looks like a raw lot row")
    if item.get("trust") != "untrusted_text" and INSTRUCTION_RE.search(item.get("statement", "")):
        lowered = item.get("statement", "").lower()
        if not any(token in lowered for token in ("block", "never", "does not", "data", "person")):
            errors.append("instruction language in trusted statement")
    return errors


def build() -> dict[str, Any]:
    errors: list[str] = []
    validator = item_validator()
    cvalidator = card_validator()
    tvalidator = term_validator()
    register = load_register()
    tables, columns = pragma_catalog()

    items: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for path in iter_item_files():
        item = load_yaml(path)
        errs = write_time_check(item, path, validator)
        errors.extend(f"{path.name}: {e}" for e in errs)
        item_id = item["id"]
        if item_id in seen_ids:
            errors.append(f"duplicate id {item_id}")
        seen_ids.add(item_id)
        source_path = item["source"]["path"]
        resolved = WORKSPACE / source_path
        if not resolved.exists():
            errors.append(f"{item_id}: source.path missing on disk: {source_path}")
        inherited_key = None
        prefix = str(INHERITED_REL).replace("\\", "/") + "/"
        if source_path.replace("\\", "/").startswith(prefix):
            inherited_key = source_path.replace("\\", "/")[len(prefix) :]
        if inherited_key:
            expected = register.get(inherited_key)
            if expected and expected != item["source"]["sha256"]:
                errors.append(f"{item_id}: sha256 disagrees with register")
        locator = item["source"].get("locator")
        if locator and locator not in columns:
            errors.append(f"{item_id}: locator {locator} absent from PRAGMA table_info")
        item["_path"] = str(path)
        items.append(item)

    cards = []
    card_ids = set()
    for path in iter_card_files():
        card = load_yaml(path)
        errs = [e.message for e in cvalidator.iter_errors(card)]
        errors.extend(f"{path.name}: {e}" for e in errs)
        table = json.dumps(card.get("decision_table", []))
        if "999999" in table and card["id"] != "rule.recipe_release.limit.impl.js_default":
            errors.append(f"{card['id']}: 999999 in canonical decision_table")
        if card.get("authority") == "unresolved":
            blob = json.dumps(card.get("decision_table", [])) + json.dumps(card.get("tests", []))
            if "HOLD_FOR_REVIEW" not in blob:
                errors.append(f"{card['id']}: unresolved card missing HOLD_FOR_REVIEW")
        cards.append(card)
        card_ids.add(card["id"])

    terms: list[dict[str, Any]] = []
    term_ids: set[str] = set()
    for path in SEMANTIC_DIR.glob("*.yaml"):
        payload = flatten_terms(load_yaml(path))
        for term in payload:
            errs = [e.message for e in tvalidator.iter_errors(term)]
            errors.extend(f"{path.name}: {e}" for e in errs)
            terms.append(term)
            term_ids.add(term["term_id"])

    accepted = [i for i in items if i["item_status"] == "accepted"]
    kinds_present = {i["kind"] for i in accepted}
    missing_kinds = REQUIRED_KINDS - kinds_present
    if missing_kinds:
        errors.append(f"missing accepted kinds: {sorted(missing_kinds)}")
    for bp in REQUIRED_BP:
        if not any(i["id"].startswith(bp) for i in accepted):
            errors.append(f"missing decision item {bp}")
    for card_id in REQUIRED_RULE_CARDS:
        if card_id not in card_ids:
            errors.append(f"missing rule card {card_id}")
    for map_id in REQUIRED_MAPS:
        if map_id not in seen_ids or map_id not in term_ids:
            errors.append(f"missing mapping term {map_id}")

    all_ids = {i["id"] for i in items}
    edges = []
    for item in items:
        for link in item.get("links", []):
            if link["to"] not in all_ids:
                errors.append(f"{item['id']}: link to missing {link['to']}")
            edges.append((item["id"], link["type"], link["to"]))

    if errors:
        for err in errors:
            print(f"BUILD FAIL: {err}", file=sys.stderr)
        raise SystemExit(1)

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    if SQLITE_PATH.exists():
        SQLITE_PATH.unlink()

    conn = sqlite3.connect(str(SQLITE_PATH))
    conn.execute(
        """
        CREATE TABLE items (
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            statement TEXT NOT NULL,
            source_path TEXT NOT NULL,
            source_lines TEXT,
            source_sha256 TEXT NOT NULL,
            source_locator TEXT,
            valid_from TEXT,
            valid_to TEXT,
            recorded_at TEXT NOT NULL,
            claim TEXT NOT NULL,
            trust TEXT NOT NULL,
            authority TEXT,
            owner TEXT NOT NULL,
            lake_version TEXT NOT NULL,
            item_status TEXT NOT NULL,
            policy_status TEXT NOT NULL,
            honesty TEXT NOT NULL,
            supersedes TEXT,
            reviewer TEXT,
            reviewed_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE edges (
            from_id TEXT NOT NULL,
            type TEXT NOT NULL,
            to_id TEXT NOT NULL,
            UNIQUE (from_id, type, to_id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE terms (
            term_id TEXT NOT NULL,
            canonical_name TEXT NOT NULL,
            definition TEXT NOT NULL,
            local_system TEXT,
            local_name TEXT,
            maps_to_term TEXT,
            claim TEXT NOT NULL,
            authority TEXT,
            source_path TEXT,
            policy_status TEXT
        )
        """
    )
    for item in items:
        vt = item.get("valid_time") or {}
        conn.execute(
            """
            INSERT INTO items VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                item["id"],
                item["kind"],
                item["statement"],
                item["source"]["path"],
                item["source"].get("lines"),
                item["source"]["sha256"],
                item["source"].get("locator"),
                vt.get("from"),
                vt.get("to"),
                item["recorded_at"],
                item["claim"],
                item["trust"],
                item.get("authority"),
                item["owner"],
                item["lake_version"],
                item["item_status"],
                item["policy_status"],
                item["honesty"],
                item.get("supersedes"),
                item.get("reviewer"),
                item.get("reviewed_at"),
            ),
        )
    for edge in edges:
        conn.execute("INSERT OR IGNORE INTO edges VALUES (?,?,?)", edge)
    term_rows = 0
    for term in terms:
        locals_ = term.get("local_names") or [{"system": "", "field_or_word": "", "meaning": ""}]
        for local in locals_:
            conn.execute(
                """
                INSERT INTO terms VALUES (?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    term["term_id"],
                    term["canonical_name"],
                    term["definition"],
                    local.get("system"),
                    local.get("field_or_word"),
                    term.get("maps_to_term"),
                    term["claim"],
                    term.get("authority"),
                    term.get("source_path"),
                    term.get("policy_status"),
                ),
            )
            term_rows += 1
    conn.execute("CREATE VIRTUAL TABLE items_fts USING fts5(id, statement)")
    conn.execute("INSERT INTO items_fts(id, statement) SELECT id, statement FROM items")
    fts_count = conn.execute("SELECT COUNT(*) FROM items_fts").fetchone()[0]
    item_count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    if item_count and not fts_count:
        raise SystemExit("BUILD FAIL: empty FTS5 index")
    conn.commit()
    conn.close()

    status_words = [
        "OPEN",
        "UNDER_REVIEW",
        "CLOSED",
        "ESCALATED",
        "REOPENED",
        "REVIEW",
        "HOLD",
        "WAIVED",
        "BLOCKED",
        "QUEUED",
        "PROCESSING",
        "ENGINEERING_REVIEW",
        "RELEASED",
    ]
    enums = {
        "kind": sorted(REQUIRED_KINDS),
        "claim": ["verified_fact", "inference", "assumption", "unknown"],
        "trust": ["trusted_code", "trusted_record", "untrusted_text"],
        "authority": ["policy_archive", "sme", "unresolved"],
        "item_status": ["accepted", "draft", "superseded"],
        "policy_status": ["decided", "proposed", "n/a"],
        "honesty": ["REAL", "PRECOMPUTED", "SIMULATED", "EDUCATIONAL", "n/a"],
        "link_type": [
            "implements",
            "conflicts_with",
            "supersedes",
            "governs",
            "evidenced_by",
            "depends_on",
            "maps_to",
            "tested_by",
        ],
        "tables": sorted(tables),
        "columns": sorted(columns),
        "site_codes": ["BR-SP", "DE-BY", "GB-ENG", "IN-BLR", "JP-KN", "US-TX"],
        "country_codes": ["AU", "BR", "DE", "GB", "IN", "JP", "US", "ZA"],
        "sales_regions": ["APAC", "EMEA", "AMER"],
        "archive_rule_name": ["recipe_release"],
        "register_codes": ["FAB-RULE-0", "FAB-RULE-1", "FAB-RULE-2", "FAB-RULE-3", "FAB-RULE-4"],
        "status_words": status_words,
        "item_ids": sorted(all_ids),
        "additionalProperties": False,
    }
    ENUM_PATH.write_text(json.dumps(enums, indent=2) + "\n", encoding="utf-8")

    extra_sources = {}
    for item in items:
        path = item["source"]["path"]
        if not path.replace("\\", "/").startswith(str(INHERITED_REL).replace("\\", "/")):
            extra_sources[path] = item["source"]["sha256"]
    sqlite_sha = sha256_file(SQLITE_PATH)
    enum_sha = sha256_file(ENUM_PATH)
    manifest = {
        "lake_version": "1.0.0",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "item_count": item_count,
        "edge_count": len(edges),
        "term_count": term_rows,
        "sqlite_sha256": sqlite_sha,
        "source_register_sha256": sha256_file(REGISTER_PATH),
        "correlation_id": CORRELATION_ID,
        "extra_sources": extra_sources,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    pin = {
        "lake_version": "1.0.0",
        "sqlite_sha256": sqlite_sha,
        "enum_sha256": enum_sha,
        "canonical_rule_card_ids": REQUIRED_RULE_CARDS,
    }
    PIN_PATH.write_text(json.dumps(pin, indent=2) + "\n", encoding="utf-8")
    if SQLITE_PATH.resolve() != (LAKE_ROOT / "generated" / "context-lake.sqlite3").resolve():
        raise SystemExit("BUILD FAIL: sqlite path drift")
    print(
        f"build ok items={item_count} edges={len(edges)} terms={term_rows} "
        f"sqlite={SQLITE_PATH}"
    )
    return manifest


if __name__ == "__main__":
    build()
