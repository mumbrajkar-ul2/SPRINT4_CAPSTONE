"""Read-time helpers for the lake. Runtime opens SQLite read-only."""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

LAKE_ROOT = Path(__file__).resolve().parent
SQLITE_PATH = LAKE_ROOT / "generated" / "context-lake.sqlite3"
ENUM_PATH = LAKE_ROOT / "schemas" / "enums.generated.json"
ENVELOPE_SCHEMA_PATH = LAKE_ROOT / "schemas" / "read-envelope.schema.json"
DEFAULT_SEARCH_LIMIT = 20
MAX_DEPTH = 6
BLOCK_ACTIONS = {"approve", "release", "ignore-validation", "close-from-text"}
INJECTION_ITEM_PREFIX = "data.injection."
SITE_MAP = {
    "IN-BLR": {"country": "IN", "sales_region": "APAC"},
    "JP-KN": {"country": "JP", "sales_region": "APAC"},
    "US-TX": {"country": "US", "sales_region": "AMER"},
    "BR-SP": {"country": "BR", "sales_region": "AMER"},
    "DE-BY": {"country": "DE", "sales_region": "EMEA"},
    "GB-ENG": {"country": "GB", "sales_region": "EMEA"},
}
OPEN_WORDS = {
    "OPEN",
    "UNDER_REVIEW",
    "REVIEW",
    "HOLD",
    "ESCALATED",
    "REOPENED",
    "QUEUED",
    "PROCESSING",
    "ENGINEERING_REVIEW",
    "not reviewed",
    "provisionally cleared",
    "BLOCKED",
}
ARCHIVE_LIMITS = {
    ("APAC", "2022"): 15000,
    ("EMEA", "2022"): 16100,
    ("AMER", "2022"): 17200,
    ("APAC", "2023"): 17500,
    ("EMEA", "2023"): 18600,
    ("AMER", "2023"): 19700,
    ("APAC", "2024"): 20000,
    ("EMEA", "2024"): 21100,
    ("AMER", "2024"): 22200,
    ("APAC", "2025"): 22500,
    ("EMEA", "2025"): 23600,
    ("AMER", "2025"): 24700,
    ("APAC", "2026"): 25000,
    ("EMEA", "2026"): 26100,
    ("AMER", "2026"): 27200,
}


def open_readonly(path: Path | None = None) -> sqlite3.Connection:
    db = path or SQLITE_PATH
    uri = f"file:{db.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def load_enums() -> dict[str, Any]:
    return json.loads(ENUM_PATH.read_text(encoding="utf-8"))


def envelope_validator() -> Draft202012Validator:
    schema = json.loads(ENVELOPE_SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def check_claim(claims: list[dict[str, Any]], enums: dict[str, Any] | None = None) -> dict[str, Any]:
    enums = enums or load_enums()
    unknown: list[str] = []
    tables = set(enums.get("tables", []))
    columns = set(enums.get("columns", []))
    item_ids = set(enums.get("item_ids", []))
    status_words = set(enums.get("status_words", []))
    sites = set(enums.get("site_codes", []))
    countries = set(enums.get("country_codes", []))
    regions = set(enums.get("sales_regions", []))
    for claim in claims:
        table = claim.get("table")
        column = claim.get("column")
        if table and table not in tables:
            unknown.append(f"table:{table}")
        if table and column:
            key = f"{table}.{column}"
            if key not in columns:
                unknown.append(f"column:{key}")
        item_id = claim.get("item_id")
        if item_id and item_id not in item_ids:
            unknown.append(f"item_id:{item_id}")
        rule_id = claim.get("rule_id")
        if rule_id and rule_id not in item_ids:
            unknown.append(f"rule_id:{rule_id}")
        status = claim.get("status_word")
        if status and status not in status_words:
            unknown.append(f"status_word:{status}")
        site = claim.get("site")
        if site and site not in sites:
            unknown.append(f"site:{site}")
        country = claim.get("country")
        if country and country not in countries:
            unknown.append(f"country:{country}")
        region = claim.get("sales_region")
        if region and region not in regions:
            unknown.append(f"sales_region:{region}")
    if unknown:
        return {"ok": False, "result": "reject", "unknown": unknown}
    return {"ok": True, "result": "ok", "unknown": []}


def _item_from_row(row: sqlite3.Row) -> dict[str, Any]:
    return {k: row[k] for k in row.keys()}


def make_envelope(
    *,
    lake_version: str,
    items: list[dict[str, Any]],
    edges: list[dict[str, Any]] | None = None,
    verdict: str,
    block: bool = False,
) -> dict[str, Any]:
    quotes = []
    for item in items:
        if item.get("trust") == "untrusted_text":
            quotes.append(item.get("statement", ""))
    env = {
        "ok": True,
        "lake_version": lake_version,
        "items": items,
        "edges": edges or [],
        "citations": [item["id"] for item in items],
        "trust_summary": "contains_untrusted_text" if quotes else "trusted",
        "untrusted_quotes": quotes,
        "verdict": verdict,
        "block": block,
    }
    envelope_validator().validate(env)
    return env


def lake_version(conn: sqlite3.Connection) -> str:
    row = conn.execute("SELECT lake_version FROM items LIMIT 1").fetchone()
    return row["lake_version"] if row else "0.0.0"


def get_item(item_id: str, *, include_draft: bool = False, conn: sqlite3.Connection | None = None) -> dict[str, Any]:
    own = conn is None
    conn = conn or open_readonly()
    try:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        version = lake_version(conn)
        if row is None:
            return make_envelope(lake_version=version, items=[], verdict="ABSTAIN")
        item = _item_from_row(row)
        if item["item_status"] == "draft" and not include_draft:
            return make_envelope(lake_version=version, items=[], verdict="ABSTAIN")
        if item["item_status"] == "superseded":
            return make_envelope(lake_version=version, items=[item], verdict="ANSWER")
        return make_envelope(lake_version=version, items=[item], verdict="ANSWER")
    finally:
        if own:
            conn.close()


def search_items(
    query: str,
    *,
    kind: str | None = None,
    limit: int = DEFAULT_SEARCH_LIMIT,
    conn: sqlite3.Connection | None = None,
) -> dict[str, Any]:
    own = conn is None
    conn = conn or open_readonly()
    try:
        tokens = [t for t in re.findall(r"[A-Za-z0-9._-]+", query) if len(t) > 1]
        stop = {"the", "and", "for", "from", "with", "that", "this", "which", "does", "what", "when", "how", "is", "of", "to", "on", "in", "or", "a"}
        tokens = [t for t in tokens if t.lower() not in stop]
        hits: dict[str, dict[str, Any]] = {}
        if tokens:
            match = " OR ".join(f'"{t}"' for t in tokens)
            sql = "SELECT items.* FROM items_fts JOIN items ON items.id = items_fts.id WHERE items_fts MATCH ?"
            args: list[Any] = [match]
            if kind:
                sql += " AND items.kind = ?"
                args.append(kind)
            sql += " AND items.item_status = 'accepted' LIMIT ?"
            args.append(limit)
            for row in conn.execute(sql, args):
                hits[row["id"]] = _item_from_row(row)
        # Also retrieve by exact id token.
        for token in tokens:
            row = conn.execute(
                "SELECT * FROM items WHERE id = ? AND item_status = 'accepted'",
                (token,),
            ).fetchone()
            if row:
                hits[row["id"]] = _item_from_row(row)
        items = list(hits.values())[:limit]
        verdict = "ANSWER" if items else "ABSTAIN"
        return make_envelope(lake_version=lake_version(conn), items=items, verdict=verdict)
    finally:
        if own:
            conn.close()


def get_links(
    item_id: str,
    *,
    types: list[str] | None = None,
    depth: int = MAX_DEPTH,
    direction: str = "both",
    conn: sqlite3.Connection | None = None,
) -> dict[str, Any]:
    own = conn is None
    conn = conn or open_readonly()
    try:
        type_filter = types or [
            "implements",
            "conflicts_with",
            "supersedes",
            "governs",
            "evidenced_by",
            "depends_on",
            "maps_to",
            "tested_by",
        ]
        placeholders = ",".join("?" for _ in type_filter)
        visited: set[tuple[str, str, str]] = set()
        found_edges: list[dict[str, str]] = []
        found_ids = {item_id}
        frontier = {item_id}
        for _ in range(depth):
            if not frontier:
                break
            nxt: set[str] = set()
            for start in frontier:
                if direction in {"outgoing", "both"}:
                    rows = conn.execute(
                        f"SELECT from_id, type, to_id FROM edges WHERE from_id = ? AND type IN ({placeholders})",
                        [start, *type_filter],
                    ).fetchall()
                    for row in rows:
                        key = (row["from_id"], row["type"], row["to_id"])
                        if key in visited:
                            continue
                        visited.add(key)
                        found_edges.append({"from_id": row["from_id"], "type": row["type"], "to_id": row["to_id"]})
                        found_ids.add(row["to_id"])
                        nxt.add(row["to_id"])
                if direction in {"incoming", "both"}:
                    rows = conn.execute(
                        f"SELECT from_id, type, to_id FROM edges WHERE to_id = ? AND type IN ({placeholders})",
                        [start, *type_filter],
                    ).fetchall()
                    for row in rows:
                        key = (row["from_id"], row["type"], row["to_id"])
                        if key in visited:
                            continue
                        visited.add(key)
                        found_edges.append({"from_id": row["from_id"], "type": row["type"], "to_id": row["to_id"]})
                        found_ids.add(row["from_id"])
                        nxt.add(row["from_id"])
            frontier = nxt
        items = []
        for iid in sorted(found_ids):
            row = conn.execute(
                "SELECT * FROM items WHERE id = ? AND item_status != 'draft'",
                (iid,),
            ).fetchone()
            if row:
                items.append(_item_from_row(row))
        verdict = "ANSWER" if items else "ABSTAIN"
        return make_envelope(
            lake_version=lake_version(conn),
            items=items,
            edges=found_edges,
            verdict=verdict,
        )
    finally:
        if own:
            conn.close()


def derive_location(site_code: str | None, country_code: str | None, sales_region: str | None) -> dict[str, Any]:
    if site_code:
        if site_code not in SITE_MAP:
            return {"hold": True, "reason": "unknown_site"}
        derived = SITE_MAP[site_code]
        if country_code and country_code != derived["country"]:
            return {"hold": True, "reason": "country_disagree"}
        if sales_region and sales_region != derived["sales_region"]:
            return {"hold": True, "reason": "region_disagree"}
        return {"hold": False, "country": derived["country"], "sales_region": derived["sales_region"], "site": site_code}
    if country_code in {"AU", "ZA"}:
        return {"hold": True, "reason": "no_site"}
    if country_code:
        country_to_region = {v["country"]: v["sales_region"] for v in SITE_MAP.values()}
        derived_region = country_to_region.get(country_code)
        if sales_region and derived_region and sales_region != derived_region:
            return {"hold": True, "reason": "region_disagree"}
        return {"hold": False, "country": country_code, "sales_region": sales_region or derived_region, "site": None}
    if sales_region:
        return {"hold": False, "country": None, "sales_region": sales_region, "site": None}
    return {"hold": True, "reason": "empty_lookup"}


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def rule_at(
    rule_id: str,
    on_date: str,
    *,
    site_code: str | None = None,
    country_code: str | None = None,
    sales_region: str | None = None,
    conn: sqlite3.Connection | None = None,
) -> dict[str, Any]:
    own = conn is None
    conn = conn or open_readonly()
    try:
        version = lake_version(conn)
        loc = derive_location(site_code, country_code, sales_region)
        if loc.get("hold"):
            item = conn.execute(
                "SELECT * FROM items WHERE id = 'rule.region.disagreement'"
            ).fetchone()
            items = [_item_from_row(item)] if item else []
            extra = conn.execute(
                "SELECT * FROM items WHERE id = 'rule.recipe_release.no_match'"
            ).fetchone()
            if extra and loc.get("reason") in {"empty_lookup", "no_site"}:
                items.append(_item_from_row(extra))
            return make_envelope(lake_version=version, items=items, verdict="HOLD_FOR_REVIEW")

        if rule_id in {"rule.recipe_release.limit", "recipe_release"}:
            region = loc.get("sales_region")
            rows = conn.execute(
                """
                SELECT * FROM items
                WHERE id LIKE 'rule.recipe_release.limit.v%'
                  AND item_status = 'accepted'
                """
            ).fetchall()
            matched = []
            day = _parse_date(on_date)
            for row in rows:
                if row["valid_from"] and row["valid_to"]:
                    if not (_parse_date(row["valid_from"]) <= day <= _parse_date(row["valid_to"])):
                        continue
                statement = row["statement"]
                if region and region not in statement:
                    continue
                matched.append(row)
            if len(matched) != 1:
                item = conn.execute(
                    "SELECT * FROM items WHERE id = 'rule.recipe_release.no_match'"
                ).fetchone()
                items = [_item_from_row(item)] if item else []
                return make_envelope(lake_version=version, items=items, verdict="HOLD_FOR_REVIEW")
            return make_envelope(lake_version=version, items=[_item_from_row(matched[0])], verdict="ANSWER")

        row = conn.execute(
            "SELECT * FROM items WHERE id = ? AND item_status = 'accepted'",
            (rule_id,),
        ).fetchone()
        if row is None:
            return make_envelope(lake_version=version, items=[], verdict="ABSTAIN")
        if row["authority"] == "unresolved" or row["policy_status"] == "proposed":
            return make_envelope(lake_version=version, items=[_item_from_row(row)], verdict="HOLD_FOR_REVIEW")
        return make_envelope(lake_version=version, items=[_item_from_row(row)], verdict="ANSWER")
    finally:
        if own:
            conn.close()


def injection_block(locator_item_id: str, proposed_action: str, conn: sqlite3.Connection | None = None) -> dict[str, Any]:
    own = conn is None
    conn = conn or open_readonly()
    try:
        env = get_item(locator_item_id, conn=conn)
        items = list(env["items"])
        rule = conn.execute(
            "SELECT * FROM items WHERE id = 'rule.untrusted_text.block'"
        ).fetchone()
        if rule:
            items.append(_item_from_row(rule))
        action = proposed_action.lower()
        block = locator_item_id.startswith(INJECTION_ITEM_PREFIX) and any(
            action.startswith(a) or a in action for a in BLOCK_ACTIONS
        )
        if block:
            return make_envelope(
                lake_version=lake_version(conn),
                items=items,
                verdict="HOLD_FOR_REVIEW",
                block=True,
            )
        return make_envelope(lake_version=lake_version(conn), items=items, verdict="ANSWER", block=False)
    finally:
        if own:
            conn.close()


def operational_route(status: str, *, engineering_action: str | None = None, final_disposition: bool = False) -> str:
    if status in OPEN_WORDS:
        return "OPEN"
    if status == "CLOSED":
        if engineering_action == "pending":
            return "OPEN"
        if final_disposition and engineering_action == "none":
            return "CLOSED_OPERATIONAL"
        return "HOLD_FOR_REVIEW"
    return "HOLD_FOR_REVIEW"


def js_allows(amount: float, region: str, year: int) -> bool:
    limit = ARCHIVE_LIMITS.get((region, str(year)), 999999)
    return amount <= limit * 1.05


def canonical_within_limit(amount: float, region: str, on_date: str) -> dict[str, Any]:
    year = on_date[:4]
    limit = ARCHIVE_LIMITS.get((region, year))
    if limit is None:
        return {"route": "HOLD_FOR_REVIEW", "limit": None}
    return {"within_limit": amount <= limit, "limit": limit}


def python_priority(status: str, severity: str, amount: float) -> str:
    if status == "CLOSED":
        return "ARCHIVE"
    if severity == "CRITICAL" or amount > 50000:
        return "URGENT"
    if severity == "HIGH" or status == "ESCALATED":
        return "review"
    return "QUEUE"


def validate_read_request(params: dict[str, Any], method: str = "GET") -> dict[str, Any]:
    allowed = {
        "query",
        "kind",
        "id",
        "type",
        "depth",
        "rule_id",
        "on_date",
        "site_code",
        "country_code",
        "sales_region",
        "include_draft",
        "proposed_action",
    }
    extra = sorted(set(params) - allowed)
    if extra:
        return {"ok": False, "reject": extra}
    if method.upper() in {"PUT", "POST", "PATCH", "DELETE"}:
        return {"ok": False, "reject": ["write_method"]}
    if "parent_lot_id" in params:
        return {"ok": False, "reject": ["parent_lot_id"]}
    return {"ok": True, "reject": []}
