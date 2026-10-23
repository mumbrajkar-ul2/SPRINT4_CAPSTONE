"""Phase 10 Half B tests. Replay only. No Azure. No packaged write."""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.app_a.agent.budget import MAX_GATHER_VISITS, MAX_TOOL_INVOCATIONS, RECURSION_LIMIT, STEP_BUDGET
from apps.app_a.agent.checkpointer import new_saver, reset_checkpointer
from apps.app_a.agent.graph import GRAPH_NAME, build_graph, is_waiting, reset_graph, run_agent, snapshot_for
from apps.app_a.agent.opa_client import build_opa_input, evaluate, local_evaluate, opa_binary_path
from apps.app_a.agent.tools import READ_TOOLS, WRITE_NAME_HINTS, WRITE_TOOLS, tools_reaching_model
from apps.app_a.audit.reader import read_trace
from apps.app_a.audit.store import COLUMNS, reset_audit_store
from apps.app_a.server import app as app_a
from apps.app_a.store import PACKAGED_OPEN_URIS, get_case, reset_runtime
from apps.shared.oidc_session import bearer_headers

_SIGN = {"meaning": "I confirm this record.", "reason": "Reviewed the cited case."}

ROOT = Path(__file__).resolve().parents[2]
CHILD = Path(__file__).resolve().parent / "agent_restart_child.py"


def _headers(role: str, corr: str) -> dict[str, str]:
    return bearer_headers(role, correlation_id=corr)


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


def test_no_write_tool_reaches_the_model() -> None:
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
    joined = " ".join(names)
    for hint in WRITE_NAME_HINTS:
        assert hint not in joined


def test_fd15_budget_constants() -> None:
    assert RECURSION_LIMIT == 12
    assert STEP_BUDGET == 8
    assert MAX_TOOL_INVOCATIONS == 8
    assert MAX_GATHER_VISITS == 3
    assert GRAPH_NAME == "app_a_investigate"


def test_opa_injection_ic01_blocks(isolated_runtime) -> None:
    payload = {
        "proposed_action": "approve",
        "record_change": True,
        "injection": True,
        "corpus_id": "IC-01",
        "block_flag": True,
        "archive_match": "one",
        "region_disagreement": False,
        "silent_threshold": False,
        "finance_audit_mismatch": False,
        "actor_id": "",
        "proposed_by": "model_draft",
        "actor_role": "",
        "action_type": "",
        "owner_invented": False,
        "budget_exhausted": False,
        "citations_empty": False,
        "untrusted_quote_present": True,
    }
    result = evaluate(payload)
    assert result["verdict"] == "BLOCK"
    assert result["engine"] == "opa_binary"
    assert result["opa_binary_present"] is True
    assert local_evaluate(payload) == "BLOCK"


def test_opa_all_corpus_rows_block(isolated_runtime) -> None:
    actions = {
        "IC-01": "approve",
        "IC-02": "approve",
        "IC-02-tiny": "approve",
        "IC-03": "approve",
        "IC-04": "release",
        "IC-05": "approve",
        "IC-06": "release",
    }
    for corpus_id, action in actions.items():
        payload = {
            "proposed_action": action,
            "record_change": True,
            "injection": True,
            "corpus_id": corpus_id,
            "block_flag": True,
            "archive_match": "one",
            "region_disagreement": False,
            "silent_threshold": False,
            "finance_audit_mismatch": False,
            "actor_id": "",
            "proposed_by": "model_draft",
            "actor_role": "",
            "action_type": "",
            "owner_invented": False,
            "budget_exhausted": False,
            "citations_empty": False,
            "untrusted_quote_present": True,
        }
        assert evaluate(payload)["verdict"] == "BLOCK"
        assert local_evaluate(payload) == "BLOCK"


def test_inject_ic01_blocks_and_does_not_write(isolated_runtime) -> None:
    corr = "corr-p10b-ic01-001"
    client = TestClient(app_a)
    before = get_case("REPLAY-000000000")
    response = client.post(
        "/api/agent/run",
        headers=_headers("RT-01", corr),
        json={"case_id": "REPLAY-000000000", "scenario": "IC-01", "proposed_action": "approve"},
    )
    assert response.status_code == 409
    body = response.json()
    assert body["opa_verdict"] == "BLOCK"
    assert body["waiting"] is False
    after = get_case("REPLAY-000000000")
    assert after is not None
    assert after.get("status") == before.get("status")
    assert after.get("approvals") == []
    assert after.get("blocked") is True
    rows = client.get(f"/api/audit/{corr}", headers=_headers("RT-01", corr)).json()["rows"]
    assert any(row["event_type"] == "EV-12" for row in rows)
    assert any(row["opa_verdict"] == "BLOCK" for row in rows)
    assert not any(row["row_kind"] == "human_approval" for row in rows)


def test_restart_reopened_saver_keeps_pending(isolated_runtime) -> None:
    corr = "corr-p10b-reopen-001"
    ckpt = isolated_runtime / "reopen.sqlite3"
    conn1, saver1 = new_saver(ckpt)
    result = run_agent(
        {
            "correlation_id": corr,
            "thread_id": corr,
            "case_id": "PS000000016",
            "actor_id": "demo-rt01-1",
            "actor_role": "RT-01",
            "scenario": "SP-08",
            "proposed_action": "",
            "step_count": 0,
            "tool_call_count": 0,
            "gather_visits": 0,
            "budget_exhausted": False,
            "citations": [],
            "untrusted_quotes": [],
            "lake_item_ids": [],
            "draft_plan": "",
            "sentence": "",
            "verdict": "",
            "opa_verdict": "",
            "block": False,
            "record_change": False,
            "waiting_role": "",
            "proposed_by": "model_draft",
            "human_decision": "",
            "human_action_type": "",
            "human_actor_id": "",
            "human_actor_role": "",
            "error_class": "",
        },
        checkpointer=saver1,
    )
    graph1 = build_graph(saver1)
    assert is_waiting(graph1, corr)
    assert (result.get("state") or {}).get("opa_verdict") == "HOLD_FOR_REVIEW"
    conn1.close()
    conn2, saver2 = new_saver(ckpt)
    graph2 = build_graph(saver2)
    assert is_waiting(graph2, corr)
    snap = graph2.get_state({"recursion_limit": 12, "configurable": {"thread_id": corr}})
    values = dict(snap.values or {})
    assert values.get("waiting_role") == "RT-03"
    conn2.close()


def test_restart_second_process_keeps_pending(isolated_runtime) -> None:
    corr = "corr-p10b-child-001"
    ckpt = isolated_runtime / "child.sqlite3"
    audit = isolated_runtime / "child-audit.sqlite3"
    env = os.environ.copy()
    env["MODEL_MODE"] = "replay"
    env["APP_A_CHECKPOINT_PATH"] = str(ckpt)
    env["APP_A_AUDIT_PATH"] = str(audit)
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [sys.executable, str(CHILD), str(ckpt), str(audit), corr, "PS000000016"],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout.strip().splitlines()[-1])
    assert payload["waiting"] is True
    conn, saver = new_saver(ckpt)
    graph = build_graph(saver)
    assert is_waiting(graph, corr)
    conn.close()


def test_recipe_explain_names_both_revisions(isolated_runtime) -> None:
    client = TestClient(app_a)
    response = client.post(
        "/api/agent/run",
        headers=_headers("RT-01", "corr-recipe-explain-001"),
        json={"case_id": "PS000000016", "proposed_action": "review recipe mismatch"},
    )
    assert response.status_code == 200
    body = response.json()
    sentence = body.get("sentence") or ""
    assert "R02" in sentence
    assert "R01" in sentence
    assert "ECN0000001" in sentence
    assert "2023-01-01T07:00" in sentence
    assert "2023-01-05T16:00" in sentence
    assert "has no effective date" in sentence
    assert "rule.recipe.mismatch_show_both" in (body.get("citations") or [])
    assert not body.get("draft_plan")
    assert (body.get("case") or {}).get("engineering_hold") in {0, None}


def test_trace_scenario_8_full_audit(isolated_runtime) -> None:
    corr = "corr-p10b-doc-20261018-001"
    client = TestClient(app_a)
    start = client.post(
        "/api/agent/run",
        headers=_headers("RT-01", corr),
        json={"case_id": "PS000000016"},
    )
    assert start.status_code == 200
    body = start.json()
    assert body["opa_verdict"] == "HOLD_FOR_REVIEW"
    assert body["waiting"] is True
    assert body["waiting_role"] == "RT-03"
    hold_before = (body.get("case") or {}).get("engineering_hold")
    same = client.post(
        "/api/approvals",
        headers=_headers("RT-03", corr),
        json={
            "case_id": "PS000000016",
            "action_type": "recipe_hold_or_release",
            "decision": "hold",
            "proposed_by": "demo-rt03-1",
        },
    )
    assert same.status_code == 403
    snap = snapshot_for(corr)
    assert snap is not None
    assert "interrupt_wait" in tuple(snap.next or ()) or bool(snap.interrupts)
    ok = client.post(
        "/api/approvals",
        headers=_headers("RT-03", corr),
        json={
            "case_id": "PS000000016",
            "action_type": "recipe_hold_or_release",
            "decision": "hold",
            "proposed_by": "model_draft",
            "signature": _SIGN,
        },
    )
    assert ok.status_code == 200
    assert ok.json()["case"]["engineering_hold"] == 1
    assert hold_before in {0, 1, None}
    audit = client.get(f"/api/audit/{corr}", headers=_headers("RT-01", corr))
    assert audit.status_code == 200
    rows = audit.json()["rows"]
    assert rows
    assert [row["seq"] for row in rows] == list(range(1, len(rows) + 1))
    assert all(row["correlation_id"] == corr for row in rows)
    step_names = [row.get("step_name") for row in rows]
    assert "load_case" in step_names
    assert "plan_draft" in step_names
    assert "gather_tools" in step_names
    assert "assemble_evidence" in step_names
    assert "ground_and_cite" in step_names
    assert "opa_gate" in step_names
    assert "interrupt_wait" in step_names
    assert "apply_human_decision" in step_names
    assert any(row["tool_name"] == "get_case" for row in rows)
    assert any(row["tool_name"] == "get_item" for row in rows)
    assert any(row["row_kind"] == "human_approval" and row["event_type"] == "EV-09" for row in rows)
    assert any(row["opa_verdict"] == "HOLD_FOR_REVIEW" for row in rows)
    for row in rows:
        for column in COLUMNS:
            assert column in row
    assert all("mode=ro" in uri for uri in PACKAGED_OPEN_URIS)
    missing = client.get("/api/audit/corr-does-not-exist", headers=_headers("RT-01", corr))
    assert missing.status_code == 404


def test_budget_exhausted_holds(isolated_runtime, monkeypatch) -> None:
    from apps.app_a.agent import budget as budget_mod

    monkeypatch.setattr(budget_mod, "STEP_BUDGET", 1)
    corr = "corr-p10b-budget-001"
    result = run_agent(
        {
            "correlation_id": corr,
            "thread_id": corr,
            "case_id": "E-00000000",
            "actor_id": "demo-rt01-1",
            "actor_role": "RT-01",
            "scenario": "SP-09",
            "proposed_action": "",
            "step_count": 0,
            "tool_call_count": 0,
            "gather_visits": 0,
            "budget_exhausted": False,
            "citations": [],
            "untrusted_quotes": [],
            "lake_item_ids": [],
            "draft_plan": "",
            "sentence": "",
            "verdict": "",
            "opa_verdict": "",
            "block": False,
            "record_change": False,
            "waiting_role": "",
            "proposed_by": "model_draft",
            "human_decision": "",
            "human_action_type": "",
            "human_actor_id": "",
            "human_actor_role": "",
            "error_class": "",
        }
    )
    state = result.get("state") or {}
    assert state.get("budget_exhausted") is True
    assert state.get("opa_verdict") == "HOLD_FOR_REVIEW"
    assert get_case("E-00000000")["event_time"] != get_case("E-00000000")["arrival_time"]


def test_recursion_limit_caught(isolated_runtime, monkeypatch) -> None:
    from apps.app_a.agent import graph as graph_mod
    from langgraph.errors import GraphRecursionError

    monkeypatch.setattr(graph_mod, "after_gather", lambda _state: "gather_tools")
    reset_graph()
    corr = "corr-p10b-recursion-001"
    result = run_agent(
        {
            "correlation_id": corr,
            "thread_id": corr,
            "case_id": "E-00000000",
            "actor_id": "demo-rt01-1",
            "actor_role": "RT-01",
            "scenario": "SP-09",
            "proposed_action": "",
            "step_count": 0,
            "tool_call_count": 0,
            "gather_visits": 0,
            "budget_exhausted": False,
            "citations": [],
            "untrusted_quotes": [],
            "lake_item_ids": [],
            "draft_plan": "",
            "sentence": "",
            "verdict": "",
            "opa_verdict": "",
            "block": False,
            "record_change": False,
            "waiting_role": "",
            "proposed_by": "model_draft",
            "human_decision": "",
            "human_action_type": "",
            "human_actor_id": "",
            "human_actor_role": "",
            "error_class": "",
        }
    )
    assert result.get("error_class") == "wait_for_person"
    assert (result.get("state") or {}).get("opa_verdict") == "HOLD_FOR_REVIEW"
    rows = read_trace(corr)
    assert any(row.get("notes") == "GraphRecursionError" for row in rows)
    assert get_case("E-00000000").get("approvals") == []
    _ = GraphRecursionError


def test_replay_plan_draft_does_not_open_azure(isolated_runtime, monkeypatch) -> None:
    def forbid(*_args, **_kwargs):
        raise AssertionError("replay must not open a network socket")

    monkeypatch.setattr(socket, "create_connection", forbid)
    monkeypatch.setattr(socket, "socket", forbid)
    from apps.app_a.intelligence.generate import generate

    result = generate("zz-phase10-no-replay-hash-unique-question", prompt_id="P-DRAFT-PLAN")
    assert result["verdict"] == "ABSTAIN"
    assert result.get("model_mode") == "replay"
    assert opa_binary_path()


def test_audit_columns_are_twenty_seven() -> None:
    assert len(COLUMNS) == 27
    assert COLUMNS[0] == "audit_id"
    assert COLUMNS[2] == "seq"
    assert "occurred_at" in COLUMNS
    assert "recorded_at" in COLUMNS


def test_opa_input_has_no_amount_field() -> None:
    payload = build_opa_input(
        {
            "proposed_action": "explain",
            "record_change": False,
            "scenario": "SP-09",
            "block": False,
            "citations": ["rule.clock.event_vs_arrival"],
            "proposed_by": "model_draft",
        }
    )
    assert "amount" not in payload
    assert 50000 not in payload.values()
    assert 999999 not in payload.values()
    assert evaluate(payload)["verdict"] == "EXECUTE"
