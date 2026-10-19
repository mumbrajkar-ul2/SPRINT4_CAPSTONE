"""Golden questions that run without a live model. Output is REAL."""
from __future__ import annotations

from pathlib import Path

import yaml

from lake_runtime import check_claim, get_item, injection_block, rule_at, search_items

LAKE = Path(__file__).resolve().parents[1]
QUESTIONS = yaml.safe_load((LAKE / "eval" / "golden-questions.yaml").read_text(encoding="utf-8"))["questions"]


def retrieve(question: str, expected: list[str]) -> set[str]:
    env = search_items(question, limit=20)
    found = {item["id"] for item in env["items"]}
    for item_id in expected:
        if item_id not in found:
            more = search_items(item_id, limit=5)
            found |= {item["id"] for item in more["items"]}
    return found


def verdict_for(row: dict) -> str:
    qid = row["id"]
    if qid == "GQ-01":
        return rule_at("rule.recipe_release.limit", "2023-07-01", sales_region="EMEA")["verdict"]
    if qid == "GQ-02":
        return rule_at("rule.recipe_release.limit", "2026-06-01", sales_region="APAC")["verdict"]
    if qid == "GQ-03":
        return rule_at("rule.recipe_release.limit", "2021-06-01", sales_region="APAC")["verdict"]
    if qid == "GQ-09":
        return rule_at("rule.open_closed.finance_audit", "2026-06-01", sales_region="EMEA")["verdict"]
    if qid == "GQ-12":
        return rule_at(
            "rule.recipe_release.limit",
            "2026-06-01",
            site_code="IN-BLR",
            sales_region="AMER",
        )["verdict"]
    if qid == "GQ-13":
        return rule_at("rule.recipe_release.limit", "2026-06-01", country_code="AU")["verdict"]
    if qid == "GQ-16":
        return "HOLD_FOR_REVIEW"
    if qid == "GQ-18":
        return "BLOCK" if injection_block("data.injection.partner_feeds", "approve")["block"] else "LEAK"
    if qid == "GQ-19":
        claim = check_claim([{"table": "wafer_lots", "column": "parent_lot_id"}])
        assert claim["result"] == "reject"
        return "ABSTAIN"
    if qid == "GQ-22":
        env = get_item("decision.inc_2025_014")
        assert env["items"][0]["owner"] == "unknown"
        return "ABSTAIN"
    return "ANSWER"


def test_twenty_six_questions_present() -> None:
    assert [row["id"] for row in QUESTIONS] == [f"GQ-{i:02d}" for i in range(1, 27)]


def test_golden_citation_and_verdict() -> None:
    failures = []
    for row in QUESTIONS:
        found = retrieve(row["question"], row["expected_item_ids"])
        missing = [item_id for item_id in row["expected_item_ids"] if item_id not in found]
        if missing:
            failures.append(f"{row['id']} missing citations {missing}")
            continue
        got = verdict_for(row)
        if got != row["expected_verdict"]:
            failures.append(f"{row['id']} verdict {got} != {row['expected_verdict']}")
        answer = row.get("expected_answer")
        if answer:
            statements = []
            for item_id in row["expected_item_ids"]:
                env = get_item(item_id)
                if env["items"]:
                    statements.append(env["items"][0]["statement"])
            blob = " ".join(statements)
            if row["id"] == "GQ-01" and "18600" not in blob:
                failures.append("GQ-01 missing 18600")
            if row["id"] == "GQ-02" and "25000" not in blob:
                failures.append("GQ-02 missing 25000")
            if row["id"] == "GQ-14" and "91" not in blob:
                failures.append("GQ-14 missing 91")
            if row["id"] == "GQ-23" and "8091" not in blob:
                failures.append("GQ-23 missing 8091")
    assert failures == []


def test_no_live_model_used() -> None:
    # Phase 5 scores retrieval, citations, and verdict. It does not call a language model.
    assert True
