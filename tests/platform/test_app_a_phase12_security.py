"""Phase 12 Half B security tests. HB-24-01 and HB-24-02. Replay only."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.app_a.agent.nodes import WRITE_FROM_TEXT, load_case
from apps.app_a.agent.opa_client import build_opa_input, evaluate
from apps.app_a.agent.tools import READ_TOOLS, WRITE_TOOLS, tools_reaching_model
from apps.app_a.server import app as app_a
from apps.app_a.store import LEGACY_DB, PACKAGED_OPEN_URIS, get_case, reset_runtime
from apps.app_a.agent.checkpointer import reset_checkpointer
from apps.app_a.agent.graph import reset_graph
from apps.app_a.audit.store import reset_audit_store

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs" / "24-security-privacy" / "security-test-results.md"

CORPUS_ACTIONS = (
    ("IC-01", "approve", "REPLAY-000000000"),
    ("IC-02", "approve", ""),
    ("IC-02-tiny", "approve", ""),
    ("IC-03", "approve", ""),
    ("IC-04", "release", ""),
    ("IC-05", "approve", ""),
    ("IC-06", "release", ""),
)


def _headers(corr: str) -> dict[str, str]:
    return {
        "X-Api-Key": "local-demo-only",
        "X-Actor-Id": "demo-rt01-1",
        "X-Actor-Role": "RT-01",
        "X-Correlation-Id": corr,
    }


@pytest.fixture
def isolated_runtime(tmp_path, monkeypatch):
    monkeypatch.setenv("MODEL_MODE", "replay")
    monkeypatch.setenv("APP_A_CHECKPOINT_PATH", str(tmp_path / "checkpoints.sqlite3"))
    monkeypatch.setenv("APP_A_AUDIT_PATH", str(tmp_path / "audit.sqlite3"))
    reset_audit_store()
    reset_checkpointer()
    reset_graph()
    reset_runtime()
    yield tmp_path
    reset_audit_store()
    reset_checkpointer()
    reset_graph()
    reset_runtime()


def _select_replay_injection_feed() -> str:
    uri = f"file:{LEGACY_DB.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    rows = list(
        conn.execute(
            "SELECT feed_id, raw_json FROM partner_feeds "
            "WHERE processing_status = 'REPLAY' ORDER BY feed_id"
        )
    )
    conn.close()
    for row in rows:
        notes = str((json.loads(row["raw_json"]) or {}).get("notes") or "")
        low = notes.lower()
        if "auto approve" in low or "auto-approve" in low or "disregard" in low:
            return str(row["feed_id"])
    raise AssertionError("No REPLAY partner feed has auto-approve or disregard-validation notes")


def _packaged_snapshot() -> dict[str, object]:
    uri = f"file:{LEGACY_DB.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    cases = tuple((row["id"], row["status"]) for row in conn.execute("SELECT id, status FROM cases ORDER BY id"))
    holds = tuple(
        (row["lot_id"], row["engineering_hold"])
        for row in conn.execute("SELECT lot_id, engineering_hold FROM wafer_lots ORDER BY lot_id")
    )
    conn.close()
    return {"cases": cases, "holds": holds}


def _assert_no_write(client: TestClient, corr: str, case_id: str, before_case: dict | None, packaged_before: dict) -> dict:
    rows = client.get(f"/api/audit/{corr}", headers=_headers(corr)).json()["rows"]
    assert not any(row.get("row_kind") == "human_approval" for row in rows)
    if case_id and before_case is not None:
        after_case = get_case(case_id)
        assert after_case is not None
        assert after_case.get("status") == before_case.get("status")
        assert after_case.get("approvals") == []
        assert after_case.get("engineering_hold") == before_case.get("engineering_hold")
    assert _packaged_snapshot() == packaged_before
    assert all("mode=ro" in uri for uri in PACKAGED_OPEN_URIS)
    return {"rows": rows}


@pytest.mark.skip(reason="SC-24-01 is now present. Before snapshot is in docs/24-security-privacy/security-test-results.md")
def test_hb24_01_before_untrusted_approve_without_corpus_id() -> None:
    return


def test_hb24_01_after_untrusted_approve_without_corpus_id(isolated_runtime) -> None:
    feed_id = _select_replay_injection_feed()
    assert feed_id == "REPLAY-000000000"
    case = get_case(feed_id)
    assert case is not None
    assert case.get("untrusted_quotes"), "Fixture untrusted_quotes must be non-empty"
    packaged_before = _packaged_snapshot()
    before_status = case.get("status")
    before_hold = case.get("engineering_hold")
    corr = "corr-p12-24b-hb2401-after"
    client = TestClient(app_a)
    response = client.post(
        "/api/agent/run",
        headers=_headers(corr),
        json={"case_id": feed_id, "proposed_action": "approve"},
    )
    assert response.status_code == 409
    body = response.json()
    assert body["opa_verdict"] == "BLOCK"
    assert body["waiting"] is False
    assert body["error_class"] == "blocked"
    assert body.get("verdict") != "ANSWER" or body.get("citations")
    after = get_case(feed_id)
    assert after is not None
    assert after.get("status") == before_status
    assert after.get("approvals") == []
    assert after.get("engineering_hold") == before_hold
    audit = _assert_no_write(client, corr, feed_id, case, packaged_before)
    rows = audit["rows"]
    assert any(row.get("event_type") == "EV-12" for row in rows)
    block_rows = [row for row in rows if row.get("opa_verdict") == "BLOCK"]
    assert block_rows
    assert any(int(row.get("untrusted_quote_present") or 0) == 1 for row in block_rows)
    assert WRITE_TOOLS == []


def test_hb24_01_quoted_feed_explain_still_cites(isolated_runtime) -> None:
    feed_id = _select_replay_injection_feed()
    case = get_case(feed_id)
    assert case is not None
    assert case.get("untrusted_quotes")
    packaged_before = _packaged_snapshot()
    corr = "corr-p12-24b-hb2401-explain"
    client = TestClient(app_a)
    response = client.post(
        "/api/agent/run",
        headers=_headers(corr),
        json={"case_id": feed_id, "proposed_action": "explain"},
    )
    body = response.json()
    assert body.get("opa_verdict") != "BLOCK"
    assert body.get("error_class") != "blocked"
    assert response.status_code != 409 or body.get("error_class") != "blocked"
    citations = body.get("citations") or []
    sentence = body.get("sentence") or (body.get("case") or {}).get("sentence") or ""
    if body.get("verdict") == "ANSWER":
        assert citations
    else:
        assert citations or sentence
    if body.get("verdict") == "ANSWER":
        assert citations
    _assert_no_write(client, corr, feed_id, case, packaged_before)


@pytest.mark.parametrize("corpus_id,action,case_id", CORPUS_ACTIONS)
def test_hb24_02_corpus_http_blocks_and_does_not_write(isolated_runtime, corpus_id: str, action: str, case_id: str) -> None:
    packaged_before = _packaged_snapshot()
    before_case = get_case(case_id) if case_id else None
    corr = f"corr-p12-24b-hb2402-{corpus_id}"
    client = TestClient(app_a)
    payload: dict[str, str] = {"scenario": corpus_id, "proposed_action": action}
    if case_id:
        payload["case_id"] = case_id
    response = client.post("/api/agent/run", headers=_headers(corr), json=payload)
    assert response.status_code == 409
    body = response.json()
    assert body["opa_verdict"] == "BLOCK"
    assert body["waiting"] is False
    assert body["error_class"] == "blocked"
    _assert_no_write(client, corr, case_id, before_case, packaged_before)


def test_sc24_05_write_tools_stay_empty() -> None:
    names = tools_reaching_model()
    assert names == [
        "search_items",
        "get_item",
        "get_links",
        "rule_at",
        "get_case",
        "get_recovery_status",
    ]
    assert READ_TOOLS == names
    assert WRITE_TOOLS == []


def test_sc24_01_load_case_and_opa_input_pair_quotes_with_write(isolated_runtime) -> None:
    feed_id = _select_replay_injection_feed()
    loaded = load_case(
        {
            "case_id": feed_id,
            "proposed_action": "approve",
            "correlation_id": "corr-p12-24b-unit-load",
        }
    )
    assert loaded["untrusted_quotes"]
    assert loaded["block"] is True
    assert loaded["scenario"] == "SP-07"
    payload = build_opa_input({**loaded, "citations": ["rule.feed.replay_duplicate"]})
    assert payload["corpus_id"] == ""
    assert payload["injection"] is True
    assert payload["block_flag"] is True
    assert payload["untrusted_quote_present"] is True
    assert "amount" not in payload
    assert 50000 not in payload.values()
    assert 999999 not in payload.values()
    result = evaluate(payload)
    assert result["verdict"] == "BLOCK"
    assert result["verdict"] in ("EXECUTE", "HOLD_FOR_REVIEW", "BLOCK")
    assert result["engine"] in ("opa_binary", "local_evaluator")


@pytest.mark.parametrize("action", sorted(WRITE_FROM_TEXT))
def test_sc24_01_all_write_from_text_actions_block_with_quotes(isolated_runtime, action: str) -> None:
    feed_id = _select_replay_injection_feed()
    loaded = load_case(
        {
            "case_id": feed_id,
            "proposed_action": action,
            "correlation_id": f"corr-p12-24b-unit-{action}",
        }
    )
    assert loaded["block"] is True
    payload = build_opa_input(loaded)
    assert payload["injection"] is True
    assert evaluate(payload)["verdict"] == "BLOCK"


def test_sc24_01_explain_does_not_set_injection(isolated_runtime) -> None:
    feed_id = _select_replay_injection_feed()
    loaded = load_case(
        {
            "case_id": feed_id,
            "proposed_action": "explain",
            "correlation_id": "corr-p12-24b-unit-explain",
        }
    )
    assert loaded["untrusted_quotes"]
    assert loaded["block"] is False
    payload = build_opa_input({**loaded, "record_change": False, "citations": ["rule.feed.replay_duplicate"]})
    assert payload["injection"] is False
    assert payload["block_flag"] is False
    assert payload["untrusted_quote_present"] is True
    assert evaluate(payload)["verdict"] == "EXECUTE"


def test_hb24_01_before_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "REPLAY-000000000" in text
    assert "HOLD_FOR_REVIEW" in text
    assert "Measured before" in text
    assert "Honesty: REAL" in text or "Honesty | REAL" in text
