"""Injection corpus must yield BLOCK. A leak fails the job. Output is REAL."""
from __future__ import annotations

from pathlib import Path

import yaml

from lake_runtime import get_item, injection_block

LAKE = Path(__file__).resolve().parents[1]
CORPUS = yaml.safe_load((LAKE / "eval" / "injection-corpus.yaml").read_text(encoding="utf-8"))


def test_every_injection_row_blocks() -> None:
    leaks = []
    for row in CORPUS["records"]:
        env = injection_block(row["locator_item"], row["proposed_action"])
        if env["block"] is not True:
            leaks.append(row["id"])
        if env.get("verdict") in {"EXECUTE", "ANSWER-as-approve"}:
            leaks.append(row["id"])
    assert leaks == []


def test_accepted_items_do_not_order_approve() -> None:
    env_ids = []
    for path in (LAKE / "items").rglob("*.yaml"):
        if path.name.endswith(".card.yaml") or "_drafts" in path.parts:
            continue
        item = yaml.safe_load(path.read_text(encoding="utf-8"))
        if item.get("item_status") != "accepted":
            continue
        text = item["statement"]
        if item.get("trust") != "untrusted_text" and "auto approve" in text.lower() and "never" not in text.lower():
            env_ids.append(item["id"])
    assert env_ids == []


def test_injection_items_are_untrusted() -> None:
    for row in CORPUS["records"]:
        env = get_item(row["locator_item"])
        assert env["items"]
        assert env["items"][0]["trust"] == "untrusted_text"
        assert env["trust_summary"] == "contains_untrusted_text"
        assert env["untrusted_quotes"]


def test_no_write_of_operational_status() -> None:
    # The fixture only returns an envelope. It does not update cases or lots.
    env = injection_block("data.injection.partner_feeds", "approve")
    assert "write" not in env
    assert env["block"] is True
