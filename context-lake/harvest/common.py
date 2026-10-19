"""Shared harvest helpers. Reads the source register. Does not write the lake."""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from typing import Any

import yaml

WORKSPACE = Path(__file__).resolve().parents[2]
LAKE_ROOT = WORKSPACE / "context-lake"
INHERITED_REL = Path("fabpulse-legacy-workshop-v8-Semiconductor") / "fabpulse-legacy"
INHERITED = WORKSPACE / INHERITED_REL
REGISTER_PATH = WORKSPACE / "sources" / "register.yaml"
RECORDED_AT = "2026-10-18"
LAKE_VERSION = "1.0.0"
CORRELATION_ID = "corr-p5b-doc-20261018-001"

KIND_FOLDER = {
    "business_rule": "rules",
    "domain_knowledge": "domain",
    "architecture": "architecture",
    "code_intelligence": "code",
    "data_relationship": "data",
    "dependency": "dependencies",
    "decision": "decisions",
}

SITE_MAP = {
    "IN-BLR": {"country": "IN", "sales_region": "APAC"},
    "JP-KN": {"country": "JP", "sales_region": "APAC"},
    "US-TX": {"country": "US", "sales_region": "AMER"},
    "BR-SP": {"country": "BR", "sales_region": "AMER"},
    "DE-BY": {"country": "DE", "sales_region": "EMEA"},
    "GB-ENG": {"country": "GB", "sales_region": "EMEA"},
}

ARCHIVE_LIMITS = [
    ("2022", "APAC", "2022-01-01", "2022-12-31", 15000),
    ("2022", "EMEA", "2022-01-01", "2022-12-31", 16100),
    ("2022", "AMER", "2022-01-01", "2022-12-31", 17200),
    ("2023", "APAC", "2023-01-01", "2023-12-31", 17500),
    ("2023", "EMEA", "2023-01-01", "2023-12-31", 18600),
    ("2023", "AMER", "2023-01-01", "2023-12-31", 19700),
    ("2024", "APAC", "2024-01-01", "2024-12-31", 20000),
    ("2024", "EMEA", "2024-01-01", "2024-12-31", 21100),
    ("2024", "AMER", "2024-01-01", "2024-12-31", 22200),
    ("2025", "APAC", "2025-01-01", "2025-12-31", 22500),
    ("2025", "EMEA", "2025-01-01", "2025-12-31", 23600),
    ("2025", "AMER", "2025-01-01", "2025-12-31", 24700),
    ("2026", "APAC", "2026-01-01", "2026-12-31", 25000),
    ("2026", "EMEA", "2026-01-01", "2026-12-31", 26100),
    ("2026", "AMER", "2026-01-01", "2026-12-31", 27200),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_register() -> dict[str, str]:
    payload = yaml.safe_load(REGISTER_PATH.read_text(encoding="utf-8"))
    files = payload["register"]["files"]
    return {row["path"].replace("\\", "/"): row["sha256"] for row in files}


def inherited_path(rel: str) -> Path:
    return INHERITED / rel


def source_for_inherited(rel: str, register: dict[str, str], *, lines: str | None = None, locator: str | None = None) -> dict[str, str]:
    key = rel.replace("\\", "/")
    if key not in register:
        raise KeyError(f"inherited path not in register: {key}")
    path = inherited_path(rel)
    if not path.exists():
        raise FileNotFoundError(path)
    on_disk = sha256_file(path)
    if on_disk != register[key]:
        raise ValueError(f"hash mismatch for {key}: register={register[key]} disk={on_disk}")
    source = {
        "path": str(INHERITED_REL / rel).replace("\\", "/"),
        "sha256": register[key],
    }
    if lines:
        source["lines"] = lines
    if locator:
        source["locator"] = locator
    return source


def source_for_workspace(rel: str, *, lines: str | None = None, locator: str | None = None) -> dict[str, str]:
    path = WORKSPACE / rel
    if not path.exists():
        raise FileNotFoundError(path)
    source = {
        "path": rel.replace("\\", "/"),
        "sha256": sha256_file(path),
    }
    if lines:
        source["lines"] = lines
    if locator:
        source["locator"] = locator
    return source


def open_ro(path: Path) -> sqlite3.Connection:
    uri = f"file:{path.as_posix()}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def dump_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)
    path.write_text(text, encoding="utf-8")


def item_path(item: dict[str, Any], *, draft: bool = False) -> Path:
    if draft:
        folder = LAKE_ROOT / "items" / "_drafts"
    else:
        folder = LAKE_ROOT / "items" / KIND_FOLDER[item["kind"]]
    return folder / f"{item['id']}.yaml"


def write_item(item: dict[str, Any], *, draft: bool = False) -> Path:
    path = item_path(item, draft=draft)
    dump_yaml(path, item)
    return path


def base_item(
    *,
    id: str,
    kind: str,
    statement: str,
    source: dict[str, str],
    claim: str,
    trust: str,
    owner: str,
    policy_status: str,
    honesty: str,
    links: list[dict[str, str]] | None = None,
    authority: str | None = None,
    valid_time: dict[str, str | None] | None = None,
    supersedes: str | None = None,
    item_status: str = "accepted",
    reviewer: str | None = None,
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": id,
        "kind": kind,
        "statement": statement,
        "source": source,
        "recorded_at": RECORDED_AT,
        "claim": claim,
        "trust": trust,
        "owner": owner,
        "lake_version": LAKE_VERSION,
        "item_status": item_status,
        "policy_status": policy_status,
        "honesty": honesty,
        "links": links or [],
    }
    if authority is not None:
        item["authority"] = authority
    if valid_time is not None:
        item["valid_time"] = valid_time
    if supersedes is not None:
        item["supersedes"] = supersedes
    if reviewer is not None:
        item["reviewer"] = reviewer
    if reviewed_at is not None:
        item["reviewed_at"] = reviewed_at
    return item
