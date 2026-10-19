"""Canonical rule cards versus the four recorded deviations. Output is REAL."""
from __future__ import annotations

from pathlib import Path

import yaml

from lake_runtime import (
    ARCHIVE_LIMITS,
    canonical_within_limit,
    js_allows,
    operational_route,
    python_priority,
)

LAKE = Path(__file__).resolve().parents[1]


def _card(item_id: str) -> dict:
    path = LAKE / "items" / "rules" / f"{item_id}.card.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_rc01_canonical_limits() -> None:
    assert canonical_within_limit(18000, "EMEA", "2023-07-01") == {"within_limit": True, "limit": 18600}
    assert canonical_within_limit(19000, "EMEA", "2023-07-01") == {"within_limit": False, "limit": 18600}
    assert canonical_within_limit(25000, "APAC", "2026-06-01") == {"within_limit": True, "limit": 25000}
    assert canonical_within_limit(25001, "APAC", "2026-06-01") == {"within_limit": False, "limit": 25000}
    assert canonical_within_limit(27200, "AMER", "2026-06-01") == {"within_limit": True, "limit": 27200}


def test_rc01_card_has_fifteen_rows() -> None:
    card = _card("rule.recipe_release.limit")
    assert len(card["decision_table"]) == 15
    assert "999999" not in str(card["decision_table"])


def test_rc02_no_match_is_hold() -> None:
    assert canonical_within_limit(100, "APAC", "2021-06-01")["route"] == "HOLD_FOR_REVIEW"


def test_js_105_versus_archive() -> None:
    assert js_allows(15700, "APAC", 2022) is True
    assert canonical_within_limit(15700, "APAC", "2022-06-01")["within_limit"] is False
    assert js_allows(27000, "APAC", 2026) is False
    assert canonical_within_limit(27000, "APAC", "2026-06-01")["within_limit"] is False


def test_js_default_is_not_canonical() -> None:
    assert js_allows(100, "IN", 2026) is True
    assert canonical_within_limit(100, "IN", "2026-01-01")["route"] == "HOLD_FOR_REVIEW"
    card = _card("rule.recipe_release.no_match")
    assert all(row["expect"]["route"] == "HOLD_FOR_REVIEW" for row in card["tests"])


def test_python_50000_is_proposed() -> None:
    assert python_priority("OPEN", "LOW", 50001) == "URGENT"
    assert python_priority("OPEN", "LOW", 49999) == "QUEUE"
    card = _card("rule.urgent.amount.impl.python")
    assert card["policy_status"] == "proposed"
    assert card["authority"] == "unresolved"
    demo = _card("rule.threshold.demo_50000")
    assert demo["policy_status"] == "proposed"


def test_never_999999_as_live_policy() -> None:
    card = _card("rule.threshold.never_999999")
    assert card["tests"][0]["expect"]["limit_is_999999"] is False
    assert card["tests"][0]["expect"]["route"] == "HOLD_FOR_REVIEW"
    for year_region, limit in ARCHIVE_LIMITS.items():
        assert limit != 999999, year_region


def test_python_closed_is_not_sme_closed() -> None:
    assert python_priority("CLOSED", "LOW", 1) == "ARCHIVE"
    assert operational_route("CLOSED") == "HOLD_FOR_REVIEW"


def test_review_and_hold_are_open() -> None:
    assert operational_route("REVIEW") == "OPEN"
    assert operational_route("HOLD") == "OPEN"
    assert operational_route("UNDER_REVIEW") == "OPEN"
    assert operational_route("CLOSED", engineering_action="pending") == "OPEN"
    assert operational_route("CLOSED", engineering_action="none", final_disposition=True) == "CLOSED_OPERATIONAL"


def test_finance_audit_card_holds() -> None:
    card = _card("rule.open_closed.finance_audit")
    assert card["authority"] == "unresolved"
    assert card["policy_status"] == "proposed"
    assert all(row["expect"]["route"] == "HOLD_FOR_REVIEW" for row in card["tests"])


def test_site_map_card() -> None:
    card = _card("rule.region.site_canonical")
    expect = {row["given"]["site"]: row["expect"] for row in card["tests"]}
    assert expect["IN-BLR"] == {"country": "IN", "sales_region": "APAC"}
    assert expect["US-TX"] == {"country": "US", "sales_region": "AMER"}


def test_disagreement_and_au_za_wait() -> None:
    card = _card("rule.region.disagreement")
    routes = [row["expect"]["route"] for row in card["tests"]]
    assert routes == ["HOLD_FOR_REVIEW", "HOLD_FOR_REVIEW", "HOLD_FOR_REVIEW"]


def test_java_blank_and_night_batch() -> None:
    blank = _card("rule.month_end.blank.impl.java")
    assert blank["tests"][0]["expect"]["canonical_route"] == "HOLD_FOR_REVIEW"
    night = _card("rule.open_flag.impl.night_batch")
    assert night["tests"][0]["expect"] == {"flagged": True, "route": "OPEN"}
    join = _card("rule.night_batch.join_multiply")
    assert join["tests"][0]["expect"]["canonical_route"] == "HOLD_FOR_REVIEW"
