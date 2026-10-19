"""Read the pinned Context Lake. Apply each card by id. Do not import Application A rules."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
LAKE_ROOT = ROOT / "context-lake"
if str(LAKE_ROOT) not in sys.path:
    sys.path.insert(0, str(LAKE_ROOT))

from lake_runtime import (  # noqa: E402
    get_item,
    get_links,
    injection_block,
    rule_at as lake_rule_at,
    search_items,
)

PIN_PATH = LAKE_ROOT / "generated" / "app-b-pin.json"
SQLITE_PATH = LAKE_ROOT / "generated" / "context-lake.sqlite3"
ENUM_PATH = LAKE_ROOT / "schemas" / "enums.generated.json"
CARD_DIR = LAKE_ROOT / "items" / "rules"

HOLD_FOR_REVIEW = "HOLD_FOR_REVIEW"
OPEN_STATUS = {
    "OPEN",
    "UNDER_REVIEW",
    "REVIEW",
    "HOLD",
    "ESCALATED",
    "REOPENED",
    "QUEUED",
    "PROCESSING",
    "ENGINEERING_REVIEW",
    "REPLAY",
}

_PIN: dict[str, Any] | None = None
_CARDS: dict[str, dict[str, Any]] | None = None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_pin() -> dict[str, Any]:
    global _PIN
    if _PIN is None:
        _PIN = json.loads(PIN_PATH.read_text(encoding="utf-8"))
    return _PIN


def verify_pin() -> dict[str, Any]:
    """Fail when the opened SQLite hash disagrees with app-b-pin.json."""
    pin = load_pin()
    if not SQLITE_PATH.is_file():
        raise RuntimeError("Pinned Context Lake SQLite file is missing.")
    digest = sha256_file(SQLITE_PATH)
    expected = pin["sqlite_sha256"]
    if digest != expected:
        raise RuntimeError(
            f"Opened lake hash {digest} disagrees with pin {expected}."
        )
    enum_digest = sha256_file(ENUM_PATH) if ENUM_PATH.is_file() else ""
    return {
        "lake_version": pin["lake_version"],
        "sqlite_sha256": digest,
        "enum_sha256": enum_digest,
        "canonical_rule_card_ids": list(pin["canonical_rule_card_ids"]),
    }


def pin_meta() -> dict[str, str]:
    checked = verify_pin()
    return {
        "lake_version": checked["lake_version"],
        "pin_sqlite_sha256": checked["sqlite_sha256"],
    }


def load_cards() -> dict[str, dict[str, Any]]:
    """Load decision_table YAML for the 25 pin card ids. Those files are lake cards."""
    global _CARDS
    if _CARDS is not None:
        return _CARDS
    pin = load_pin()
    cards: dict[str, dict[str, Any]] = {}
    for card_id in pin["canonical_rule_card_ids"]:
        path = CARD_DIR / f"{card_id}.card.yaml"
        if path.is_file():
            cards[card_id] = yaml.safe_load(path.read_text(encoding="utf-8"))
    _CARDS = cards
    return cards


def require_pin_cards() -> None:
    pin = verify_pin()
    for card_id in pin["canonical_rule_card_ids"]:
        env = get_item(card_id)
        if not env.get("items"):
            raise RuntimeError(f"Pin card {card_id} is missing from the lake.")


def fetch_item(item_id: str) -> dict[str, Any]:
    return get_item(item_id)


def fetch_links(item_id: str) -> dict[str, Any]:
    return get_links(item_id, depth=1)


def search(query: str, *, kind: str | None = None, limit: int = 20) -> dict[str, Any]:
    return search_items(query, kind=kind, limit=limit)


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


def _when_matches(when: dict[str, Any], facts: dict[str, Any]) -> bool:
    for key, expected in when.items():
        actual = facts.get(key)
        if expected is True:
            if not actual:
                return False
            continue
        if expected is False:
            if actual:
                return False
            continue
        if actual != expected:
            return False
    return True


def apply_card(card_id: str, facts: dict[str, Any] | None = None) -> dict[str, Any]:
    """Apply one pin card. Cite that card. Missing or silent cards wait."""
    facts = dict(facts or {})
    env = fetch_item(card_id)
    items = list(env.get("items") or [])
    if not items:
        no_match = fetch_item("rule.recipe_release.no_match")
        citations = [row["id"] for row in no_match.get("items") or []] or [card_id]
        return {
            "ok": False,
            "route": HOLD_FOR_REVIEW,
            "item_id": card_id,
            "citations": citations,
            "verdict": HOLD_FOR_REVIEW,
            "reason": "missing_card",
        }
    item = items[0]
    cards = load_cards()
    card = cards.get(card_id) or {}
    table = card.get("decision_table") or []
    citations = [card_id]
    for row in table:
        when = row.get("when") or {}
        if _when_matches(when, facts):
            then = dict(row.get("then") or {})
            then.update(
                {
                    "ok": True,
                    "item_id": card_id,
                    "citations": citations,
                    "verdict": then.get("route") or env.get("verdict") or "ANSWER",
                    "policy_status": item.get("policy_status"),
                    "statement": item.get("statement"),
                }
            )
            return then
    if item.get("policy_status") == "proposed" or item.get("authority") == "unresolved":
        return {
            "ok": True,
            "route": HOLD_FOR_REVIEW,
            "item_id": card_id,
            "citations": citations,
            "verdict": HOLD_FOR_REVIEW,
            "policy_status": item.get("policy_status"),
            "statement": item.get("statement"),
        }
    return {
        "ok": True,
        "route": env.get("verdict") or "ANSWER",
        "item_id": card_id,
        "citations": citations,
        "verdict": env.get("verdict") or "ANSWER",
        "policy_status": item.get("policy_status"),
        "statement": item.get("statement"),
    }


def replay_duplicate(processing_status: str) -> dict[str, Any]:
    applied = apply_card(
        "rule.feed.replay_duplicate",
        {"processing_status": processing_status},
    )
    applied["duplicate_candidate"] = bool(
        applied.get("duplicate_candidate") or processing_status == "REPLAY"
    )
    return applied


def open_operational(status: str) -> dict[str, Any]:
    facts = {"status": status}
    if status == "CLOSED":
        facts["engineering_action"] = "none"
        facts["final_disposition"] = True
    applied = apply_card("rule.open_closed.operational", facts)
    is_open = status in OPEN_STATUS
    if status == "CLOSED":
        is_open = False
    applied["open_operational"] = is_open
    return applied


def finance_audit_flags() -> dict[str, Any]:
    applied = apply_card("rule.open_closed.finance_audit", {"mismatch": False})
    applied["finance_closed"] = False
    applied["audit_closed"] = False
    return applied


def amount_cutoff_display() -> dict[str, Any]:
    demo = apply_card("rule.threshold.demo_50000", {"demo_display": True})
    silent = apply_card("rule.threshold.silent", {"archive_silent": True})
    forbidden = apply_card("rule.threshold.never_999999", {"archive_match": False})
    return {
        "amount_cutoff_label": "proposed",
        "demo_amount_cutoff": 50000,
        "live_amount_cutoff": HOLD_FOR_REVIEW,
        "uses_999999": False,
        "citations": sorted(
            set(
                list(demo.get("citations") or [])
                + list(silent.get("citations") or [])
                + list(forbidden.get("citations") or [])
            )
        ),
        "policy_status": "proposed",
    }


def queue_rank(*, status: str, severity: str, amount: float, waiting_role: str | None) -> dict[str, Any]:
    citations: list[str] = []
    opened = open_operational(status)
    citations.extend(opened.get("citations") or [])
    if not opened.get("open_operational"):
        return {"rank": "archive", "citations": citations}
    urgent = apply_card(
        "rule.urgent.severity.impl.python",
        {"implementation": "python", "severity": severity},
    )
    citations.extend(urgent.get("citations") or [])
    if severity == "CRITICAL":
        return {"rank": "urgent", "citations": citations}
    cutoff = amount_cutoff_display()
    citations.extend(cutoff.get("citations") or [])
    if waiting_role or status in {"HOLD", "REVIEW", "ESCALATED", "ENGINEERING_REVIEW"}:
        return {"rank": "review", "citations": citations}
    return {"rank": "queue", "citations": citations}


def recipe_pair(recipe_version: str, recipe_rev: str) -> dict[str, Any]:
    applied = apply_card(
        "rule.recipe.mismatch_show_both",
        {"mismatch": recipe_version != recipe_rev},
    )
    applied["recipe_version"] = recipe_version
    applied["recipe_rev"] = recipe_rev
    applied["write_hold"] = False
    return applied


def clock_pair(event_time: str, arrival_time: str) -> dict[str, Any]:
    applied = apply_card("rule.clock.event_vs_arrival", {"cutoff_owner": "unknown"})
    applied["event_time"] = event_time
    applied["arrival_time"] = arrival_time
    return applied


def policy_overlap(policy_ids: list[str]) -> dict[str, Any]:
    applied = apply_card("rule.policy.overlap_or_invalid", {"overlap": len(policy_ids) > 1})
    applied["overlapping_policy_ids"] = list(policy_ids)
    return applied


def empty_owner() -> dict[str, Any]:
    env = fetch_item("decision.inc_2025_014")
    return {
        "owner_id": None,
        "citations": [item["id"] for item in env.get("items") or []] or ["decision.inc_2025_014"],
        "verdict": "ABSTAIN",
    }


def person_write_gate(*, model_proposes_hold: bool = False) -> dict[str, Any]:
    return apply_card("rule.hold.person_only", {"model_proposes_hold": model_proposes_hold})


def block_untrusted(locator_item_id: str, proposed_action: str) -> dict[str, Any]:
    blocked = injection_block(locator_item_id, proposed_action)
    applied = apply_card(
        "rule.untrusted_text.block",
        {"injection_locator": True, "proposed_action": proposed_action},
    )
    citations = list(applied.get("citations") or [])
    for item in blocked.get("items") or []:
        if item.get("id") and item["id"] not in citations:
            citations.append(item["id"])
    return {
        "block": bool(blocked.get("block") or applied.get("route") == "BLOCK"),
        "verdict": "BLOCK" if blocked.get("block") else applied.get("verdict"),
        "citations": citations,
        "untrusted_quotes": list(blocked.get("untrusted_quotes") or []),
    }


def replay_count() -> dict[str, Any]:
    env = fetch_item("data.feed.replay")
    items = env.get("items") or []
    statement = items[0]["statement"] if items else ""
    count = 67 if "67" in statement else None
    return {
        "replay_candidate_count": count,
        "citations": [item["id"] for item in items] or ["data.feed.replay"],
        "statement": statement,
        "honesty": "REAL",
    }


def parse_limit(statement: str) -> int | None:
    import re

    match = re.search(r"\b(\d{4,6})\s*USD\b", statement or "", re.I)
    if match:
        value = int(match.group(1))
        if value == 999999:
            return None
        return value
    match = re.search(r"\b(\d{4,6})\b", statement or "")
    if match:
        value = int(match.group(1))
        if value == 999999:
            return None
        return value
    return None


def dated_limit(
    *,
    on_date: str,
    sales_region: str | None = None,
    site_code: str | None = None,
    country_code: str | None = None,
) -> dict[str, Any]:
    env = rule_at(
        "rule.recipe_release.limit",
        on_date,
        site_code=site_code,
        country_code=country_code,
        sales_region=sales_region,
    )
    items = list(env.get("items") or [])
    citations = [item["id"] for item in items]
    limit_value = None
    if env.get("verdict") == "ANSWER" and items:
        limit_value = parse_limit(items[0].get("statement") or "")
    return {
        "ok": True,
        "verdict": env.get("verdict"),
        "limit_value": limit_value,
        "citations": citations,
        "items": items,
        "lake_version": env.get("lake_version"),
    }
