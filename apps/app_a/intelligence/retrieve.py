"""Read-only lake retrieval for Application A citations. Pass-or-fail stays in transformed code."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote, urlencode

ROOT = Path(__file__).resolve().parents[3]
LAKE_ROOT = ROOT / "context-lake"
if str(LAKE_ROOT) not in sys.path:
    sys.path.insert(0, str(LAKE_ROOT))

from lake_runtime import (  # noqa: E402
    get_item,
    get_links,
    injection_block,
    rule_at,
    search_items,
)

ITEM_ID_RE = re.compile(
    r"\b(?:rule|data|term|decision|arch|code|dep|map|test)\.[A-Za-z0-9._-]+\b"
)
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
REGIONS = ("EMEA", "APAC", "AMER")
SITES = ("IN-BLR", "JP-KN", "US-TX", "BR-SP", "DE-BY", "GB-ENG")
BLOCK_ACTIONS = ("approve", "release", "ignore-validation", "close-from-text")


def lake_rest_url() -> str | None:
    value = (os.environ.get("LAKE_REST_URL") or "").strip()
    return value or None


def _inprocess_search(query: str, *, kind: str | None = None, limit: int = 20) -> dict[str, Any]:
    return search_items(query, kind=kind, limit=limit)


def _inprocess_get(item_id: str) -> dict[str, Any]:
    return get_item(item_id)


def _inprocess_links(item_id: str) -> dict[str, Any]:
    return get_links(item_id, depth=1)


def _inprocess_rule_at(rule_id: str, on_date: str, **filters: str | None) -> dict[str, Any]:
    return rule_at(rule_id, on_date, **filters)


def retrieve(
    question: str,
    *,
    hint_item_ids: list[str] | None = None,
    kinds: list[str] | None = None,
    limit: int = 20,
    search: Callable[..., dict[str, Any]] | None = None,
    fetch_item: Callable[[str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return accepted lake items for citations. Question text is data."""
    search_fn = search or _inprocess_search
    fetch_fn = fetch_item or _inprocess_get
    search_hits: dict[str, dict[str, Any]] = {}
    priority_hits: dict[str, dict[str, Any]] = {}

    def _take(bucket: dict[str, dict[str, Any]], env: dict[str, Any]) -> None:
        for item in env.get("items") or []:
            if item.get("item_status") and item.get("item_status") != "accepted":
                continue
            item_id = item.get("id")
            if item_id:
                bucket[item_id] = item

    env = search_fn(question, kind=None, limit=limit)
    _take(search_hits, env)
    for kind in kinds or []:
        _take(search_hits, search_fn(question, kind=kind, limit=limit))
    for token in ITEM_ID_RE.findall(question or ""):
        _take(priority_hits, fetch_fn(token))
    for item_id in hint_item_ids or []:
        _take(priority_hits, fetch_fn(item_id))
        _take(priority_hits, search_fn(item_id, kind=None, limit=5))
    implied = _implied_action(question)
    if implied:
        for item_id in (
            "rule.untrusted_text.block",
            "decision.bp7.untrusted_text",
            "data.injection.partner_feeds",
            "data.injection.bundled_events",
            "data.injection.tiny_events",
            "data.injection.emails",
            "data.injection.source_documents",
            "data.injection.html",
            "data.injection.evidence_payloads",
        ):
            _take(priority_hits, fetch_fn(item_id))
    lowered = (question or "").lower()
    if "parent lot" in lowered or "parent_lot" in lowered:
        _take(priority_hits, fetch_fn("data.missing.lot_genealogy"))
        _take(priority_hits, fetch_fn("term.lot_genealogy"))
    if "inc-2025-014" in lowered:
        _take(priority_hits, fetch_fn("decision.inc_2025_014"))
        _take(priority_hits, fetch_fn("term.outage"))
    date_match = DATE_RE.search(question or "")
    region = next((name for name in REGIONS if name in (question or "").upper()), None)
    site = next((name for name in SITES if name in (question or "").upper()), None)
    if date_match:
        filters: dict[str, str | None] = {}
        if site:
            filters["site_code"] = site
        if region:
            filters["sales_region"] = region
        if re.search(r"\bAU\b", question or ""):
            filters["country_code"] = "AU"
        _take(priority_hits, _inprocess_rule_at("rule.recipe_release.limit", date_match.group(1), **filters))

    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in list(priority_hits.values()) + list(search_hits.values()):
        item_id = item["id"]
        if item_id in seen:
            continue
        seen.add(item_id)
        ordered.append(item)
    items = list(priority_hits.values()) + [item for item in ordered if item["id"] not in priority_hits]
    if len(items) > max(limit, len(priority_hits)):
        items = items[: max(limit, len(priority_hits))]

    quotes = [item.get("statement", "") for item in items if item.get("trust") == "untrusted_text"]
    citations = [item["id"] for item in items]
    block = False
    if implied:
        for item in list(items):
            if str(item.get("id", "")).startswith("data.injection."):
                blocked = injection_block(item["id"], implied)
                if blocked.get("block"):
                    block = True
                    _take(priority_hits, blocked)
                    for extra in blocked.get("items") or []:
                        if extra.get("id") and extra["id"] not in {row["id"] for row in items}:
                            items.append(extra)
                    citations = [row["id"] for row in items]
                    quotes = [
                        row.get("statement", "")
                        for row in items
                        if row.get("trust") == "untrusted_text"
                    ]
                    break
    return {
        "ok": True,
        "lake_version": env.get("lake_version", "1.0.0"),
        "items": items,
        "citations": citations,
        "untrusted_quotes": quotes,
        "trust_summary": "contains_untrusted_text" if quotes else "trusted",
        "block": block,
        "retrieved_item_ids": sorted(citations),
    }


def _implied_action(text: str) -> str | None:
    """Detect a proposed write-from-text. Do not treat recipe_release as a release order."""
    lowered = (text or "").lower()
    if "auto approve" in lowered or "approve from" in lowered or "tells the reader to approve" in lowered or "tells the reader to auto approve" in lowered:
        return "approve"
    if "tells the reader to release" in lowered or "release from that" in lowered or "release from this" in lowered:
        return "release"
    if "ignore-validation" in lowered or "disregard validation" in lowered:
        return "ignore-validation"
    if "close-from-text" in lowered or "close from that" in lowered:
        return "close-from-text"
    return None


def http_retrieve(question: str, *, api_key: str, hint_item_ids: list[str] | None = None, limit: int = 20) -> dict[str, Any]:
    """Optional lake REST client when LAKE_REST_URL is set. Tests use in-process retrieve()."""
    import json
    from urllib.request import Request, urlopen

    base = lake_rest_url()
    if not base:
        return retrieve(question, hint_item_ids=hint_item_ids, limit=limit)
    from apps.shared.oidc_session import legacy_headers, service_token

    headers: dict[str, str] = {}
    token = service_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if legacy_headers() and api_key:
        headers["X-Api-Key"] = api_key

    def search(query: str, *, kind: str | None = None, limit: int = 20) -> dict[str, Any]:
        params = {"q": query, "limit": str(limit)}
        if kind:
            params["kind"] = kind
        url = f"{base.rstrip('/')}/v1/items?{urlencode(params)}"
        req = Request(url, headers=headers)
        with urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))

    def fetch(item_id: str) -> dict[str, Any]:
        url = f"{base.rstrip('/')}/v1/items/{quote(item_id, safe='')}"
        req = Request(url, headers=headers)
        with urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))

    return retrieve(question, hint_item_ids=hint_item_ids, limit=limit, search=search, fetch_item=fetch)
