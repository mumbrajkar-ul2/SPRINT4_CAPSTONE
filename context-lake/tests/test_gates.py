"""Contract-gate fixtures for model-output and read-time. Output is REAL."""
from __future__ import annotations

from pathlib import Path

import yaml

from lake_runtime import check_claim, get_item, validate_read_request

LAKE = Path(__file__).resolve().parents[1]


def test_check_claim_rejects_parent_lot_id() -> None:
    result = check_claim([{"table": "wafer_lots", "column": "parent_lot_id"}])
    assert result["result"] == "reject"
    assert any("parent_lot_id" in name for name in result["unknown"])


def test_check_claim_rejects_unknown_table_and_status() -> None:
    result = check_claim(
        [
            {"table": "lot_family"},
            {"status_word": "DONE"},
            {"item_id": "rule.recipe_release.limit.v2099.moon"},
            {"site": "IN-DEL"},
        ]
    )
    assert result["result"] == "reject"
    blob = " ".join(result["unknown"])
    assert "lot_family" in blob
    assert "DONE" in blob
    assert "v2099.moon" in blob
    assert "IN-DEL" in blob


def test_check_claim_accepts_known_column() -> None:
    result = check_claim([{"table": "wafer_lots", "column": "engineering_hold"}])
    assert result["result"] == "ok"


def test_draft_not_served_as_current() -> None:
    env = get_item("data.draft.business_context")
    assert env["items"] == []
    assert env["verdict"] == "ABSTAIN"
    flagged = get_item("data.draft.business_context", include_draft=True)
    assert flagged["items"]
    assert flagged["items"][0]["item_status"] == "draft"


def test_read_time_rejects_unknown_param_and_write() -> None:
    assert validate_read_request({"parent_lot_id": "L3"})["ok"] is False
    assert validate_read_request({"rewrite": True})["ok"] is False
    assert validate_read_request({"id": "rule.recipe_release.limit"}, method="POST")["ok"] is False
    assert validate_read_request({"id": "rule.recipe_release.limit"}, method="GET")["ok"] is True


def test_no_accepted_item_in_drafts() -> None:
    drafts = LAKE / "items" / "_drafts"
    for path in drafts.glob("*.yaml"):
        item = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert item["item_status"] != "accepted"
