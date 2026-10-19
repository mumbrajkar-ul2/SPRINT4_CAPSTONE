"""Six read-only tools. WRITE_TOOLS is empty. Untrusted text stays data."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
LAKE_ROOT = ROOT / "context-lake"
if str(LAKE_ROOT) not in sys.path:
    sys.path.insert(0, str(LAKE_ROOT))

from lake_runtime import get_item as lake_get_item  # noqa: E402
from lake_runtime import get_links as lake_get_links
from lake_runtime import rule_at as lake_rule_at
from lake_runtime import search_items as lake_search_items

from apps.app_a.routes.recovery import apply_probe, _LAST
from apps.app_a.store import get_case as store_get_case

READ_TOOLS: list[str] = [
    "search_items",
    "get_item",
    "get_links",
    "rule_at",
    "get_case",
    "get_recovery_status",
]
WRITE_TOOLS: list[str] = []

WRITE_NAME_HINTS = ("update", "write", "approve", "hold", "drop", "assign", "delete")


def tools_reaching_model() -> list[str]:
    """Names the gather node may call. No write name is in this list."""
    return list(READ_TOOLS)


def search_items(
    q: str,
    *,
    kind: str | None = None,
    on_date: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    _ = on_date
    return lake_search_items(q or "", kind=kind, limit=limit)


def get_item(id: str) -> dict[str, Any]:
    env = lake_get_item(id)
    if not env.get("items"):
        env = dict(env)
        env["ok"] = False
        env["verdict"] = env.get("verdict") or "ABSTAIN"
    return env


def get_links(id: str, *, type: str | None = None, depth: int | None = None) -> dict[str, Any]:
    types = [type] if type else None
    return lake_get_links(id, types=types, depth=1 if depth is None else depth)


def rule_at(
    rule_id: str,
    on_date: str,
    *,
    site_code: str | None = None,
    country_code: str | None = None,
    sales_region: str | None = None,
) -> dict[str, Any]:
    return lake_rule_at(
        rule_id,
        on_date,
        site_code=site_code,
        country_code=country_code,
        sales_region=sales_region,
    )


def get_case(case_id: str) -> dict[str, Any]:
    body = store_get_case(case_id)
    if body is None:
        return {"ok": False, "error_class": "not_found", "untrusted_quotes": [], "block": False}
    quotes = list(body.get("untrusted_quotes") or [])
    return {
        "ok": True,
        "case": body,
        "untrusted_quotes": quotes,
        "block": False,
    }


def get_recovery_status(mode: str | None = None) -> dict[str, Any]:
    if mode in {"timeout", "schema", "rate_limit", "normal"}:
        state = apply_probe(mode)
    else:
        state = dict(_LAST)
    return {
        "ok": True,
        "recovery": {
            "status_visible": state.get("status_visible"),
            "error_class": state.get("error_class"),
            "owner_id": None,
            "retry_shown": state.get("retry_shown"),
        },
        "untrusted_quotes": [],
        "block": False,
    }


TOOL_IMPLS = {
    "search_items": search_items,
    "get_item": get_item,
    "get_links": get_links,
    "rule_at": rule_at,
    "get_case": get_case,
    "get_recovery_status": get_recovery_status,
}


def call_tool(name: str, **kwargs: Any) -> dict[str, Any]:
    if name not in TOOL_IMPLS or name in WRITE_TOOLS:
        return {"ok": False, "error_class": "forbidden_role", "message": "That tool is not on the allow-list."}
    return TOOL_IMPLS[name](**kwargs)
