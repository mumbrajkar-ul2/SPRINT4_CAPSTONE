"""Freeze-set run in replay. Every AI answer cites a lake item or abstains."""
from __future__ import annotations

from apps.app_a.eval.run_freeze import run_freeze
from apps.app_a.intelligence.prompts import prompt_path


def test_prompt_files_exist() -> None:
    for prompt_id in ("P-EXPLAIN-CONFLICT", "P-NL-QUERY", "P-DRAFT-PLAN"):
        path = prompt_path(prompt_id, "1.0.0")
        assert path.is_file(), path


def test_freeze_set_every_answer_cites_or_abstains() -> None:
    report = run_freeze()
    rows = report["rows"]
    assert len(rows) >= 26 + 5 + 3
    ungrounded = [row for row in rows if row["id"] in {"UQ-01", "UQ-02", "UQ-03"}]
    assert len(ungrounded) == 3
    for row in ungrounded:
        assert row["verdict"] == "ABSTAIN", row
        assert row["invented"] is False, row
    failed = [row for row in rows if not row["pass"]]
    served = []
    for row in rows:
        verdict = row.get("verdict")
        citations = row.get("citations") or []
        if verdict in {"ANSWER", "HOLD_FOR_REVIEW"} or row.get("block"):
            if not citations:
                served.append(row["id"])
    assert served == [], served
    assert failed == [], failed
