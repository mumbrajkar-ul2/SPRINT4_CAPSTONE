"""Read-only lake retrieval for Application B citations. Pass-or-fail stays in lake cards."""
from __future__ import annotations

import re
from typing import Any, Callable

from apps.app_b.rules.resolver import fetch_item, rule_at, search

ITEM_ID_RE = re.compile(
    r"\b(?:rule|data|term|decision|arch|code|dep|map|test)\.[A-Za-z0-9._-]+\b"
)
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
REGIONS = ("EMEA", "APAC", "AMER")
SITES = ("IN-BLR", "JP-KN", "US-TX", "BR-SP", "DE-BY", "GB-ENG")


def retrieve(
    question: str,
    *,
    hint_item_ids: list[str] | None = None,
    kinds: list[str] | None = None,
    limit: int = 20,
    search_fn: Callable[..., dict[str, Any]] | None = None,
    fetch_fn: Callable[[str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return accepted lake items for citations. Question text is data."""
    search_call = search_fn or search
    fetch_call = fetch_fn or fetch_item
    search_hits: dict[str, dict[str, Any]] = {}
    priority_hits: dict[str, dict[str, Any]] = {}

    def _take(bucket: dict[str, dict[str, Any]], env: dict[str, Any]) -> None:
        for item in env.get("items") or []:
            if item.get("item_status") and item.get("item_status") != "accepted":
                continue
            item_id = item.get("id")
            if item_id:
                bucket[item_id] = item

    env = search_call(question, kind=None, limit=limit)
    _take(search_hits, env)
    for kind in kinds or []:
        _take(search_hits, search_call(question, kind=kind, limit=limit))
    for token in ITEM_ID_RE.findall(question or ""):
        _take(priority_hits, fetch_call(token))
    for item_id in hint_item_ids or []:
        _take(priority_hits, fetch_call(item_id))
        _take(priority_hits, search_call(item_id, kind=None, limit=5))
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
            _take(priority_hits, fetch_call(item_id))
    lowered = (question or "").lower()
    if "parent lot" in lowered or "parent_lot" in lowered:
        _take(priority_hits, fetch_call("data.missing.lot_genealogy"))
        _take(priority_hits, fetch_call("term.lot_genealogy"))
    if "inc-2025-014" in lowered:
        _take(priority_hits, fetch_call("decision.inc_2025_014"))
        _take(priority_hits, fetch_call("term.outage"))
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
        _take(priority_hits, rule_at("rule.recipe_release.limit", date_match.group(1), **filters))

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
        from apps.app_b.rules.resolver import block_untrusted

        for item in list(items):
            if str(item.get("id", "")).startswith("data.injection."):
                blocked = block_untrusted(item["id"], implied)
                if blocked.get("block"):
                    block = True
                    for extra_id in blocked.get("citations") or []:
                        extra = fetch_call(extra_id)
                        for row in extra.get("items") or []:
                            if row.get("id") and row["id"] not in {existing["id"] for existing in items}:
                                items.append(row)
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
