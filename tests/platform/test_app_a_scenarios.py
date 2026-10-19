"""Scenarios 7 to 11 on Application A with replay. Citations or abstain. Person writes only."""
from __future__ import annotations

from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a
from apps.app_a.store import reset_runtime


def _headers(role: str) -> dict[str, str]:
    n = role[-1]
    return {
        "X-Api-Key": "local-demo-only",
        "X-Actor-Id": f"demo-rt0{n}-1",
        "X-Actor-Role": role,
        "X-Correlation-Id": f"corr-s-{role}",
    }


def setup_function() -> None:
    reset_runtime()


def test_scenario_7_replay(api_headers) -> None:
    client = TestClient(app_a)
    case = client.get("/api/cases/REPLAY-000000000", headers=_headers("RT-05"))
    assert case.status_code == 200
    body = case.json()["case"]
    assert body["processing_status"] == "REPLAY"
    assert body["duplicate_candidate"] is True
    expl = case.json()["explanation"]
    assert expl["verdict"] == "ANSWER"
    assert "rule.feed.replay_duplicate" in expl["citations"]
    assert "data.feed.replay" in expl["citations"]
    wrong = client.post(
        "/api/approvals",
        headers=_headers("RT-03"),
        json={
            "case_id": "REPLAY-000000000",
            "action_type": "replay_confirm",
            "decision": "drop_duplicate",
            "proposed_by": "demo-rt02-1",
        },
    )
    assert wrong.status_code == 403
    ok = client.post(
        "/api/approvals",
        headers=_headers("RT-05"),
        json={
            "case_id": "REPLAY-000000000",
            "action_type": "replay_confirm",
            "decision": "drop_duplicate",
            "proposed_by": "demo-rt02-1",
        },
    )
    assert ok.status_code == 200
    assert ok.json()["case"]["status"] == "DUPLICATE"


def test_scenario_8_recipe_mismatch() -> None:
    client = TestClient(app_a)
    case = client.get("/api/cases/PS000000016", headers=_headers("RT-03"))
    assert case.status_code == 200
    body = case.json()["case"]
    assert body["recipe_version"] == "R02"
    assert body["recipe_rev"] == "R01"
    hold_before = body.get("engineering_hold")
    expl = case.json()["explanation"]
    assert expl["verdict"] == "ANSWER"
    assert "rule.recipe.mismatch_show_both" in expl["citations"]
    assert "R02" in expl["sentence"]
    assert "R01" in expl["sentence"]
    wrong = client.post(
        "/api/approvals",
        headers=_headers("RT-05"),
        json={
            "case_id": "PS000000016",
            "action_type": "recipe_hold_or_release",
            "decision": "hold",
            "proposed_by": "demo-rt02-1",
        },
    )
    assert wrong.status_code == 403
    ok = client.post(
        "/api/approvals",
        headers=_headers("RT-03"),
        json={
            "case_id": "PS000000016",
            "action_type": "recipe_hold_or_release",
            "decision": "hold",
            "proposed_by": "demo-rt02-1",
        },
    )
    assert ok.status_code == 200
    assert ok.json()["case"]["engineering_hold"] == 1
    assert hold_before == 0 or hold_before in {0, 1, None}


def test_scenario_9_two_clocks() -> None:
    client = TestClient(app_a)
    case = client.get("/api/cases/E-00000000", headers=_headers("RT-01"))
    assert case.status_code == 200
    body = case.json()["case"]
    assert body["event_time"] != body["arrival_time"]
    expl = case.json()["explanation"]
    assert "rule.clock.event_vs_arrival" in expl["citations"]
    assert "event_time" in expl["sentence"]
    assert "arrival_time" in expl["sentence"]
    cutoff = client.post(
        "/api/query",
        headers=_headers("RT-01"),
        json={"question": "Should month-end use arrival_time as event_time when they differ?", "job": "query"},
    )
    assert cutoff.status_code == 200
    assert cutoff.json()["verdict"] == "HOLD_FOR_REVIEW"


def test_scenario_10_policy_overlap() -> None:
    client = TestClient(app_a)
    case = client.get("/api/cases/FAB-00000002", headers=_headers("RT-04"))
    assert case.status_code == 200
    body = case.json()["case"]
    assert len(body["overlapping_policy_ids"]) == 5
    expl = case.json()["explanation"]
    assert expl["verdict"] == "HOLD_FOR_REVIEW"
    assert "rule.policy.overlap_or_invalid" in expl["citations"]
    wrong = client.post(
        "/api/approvals",
        headers=_headers("RT-05"),
        json={
            "case_id": "FAB-00000002",
            "action_type": "policy_pick",
            "decision": "approve",
            "policy_id": "POL-0002",
            "proposed_by": "demo-rt02-1",
        },
    )
    assert wrong.status_code == 403
    ok = client.post(
        "/api/approvals",
        headers=_headers("RT-04"),
        json={
            "case_id": "FAB-00000002",
            "action_type": "policy_pick",
            "decision": "keep_wait",
            "proposed_by": "demo-rt02-1",
        },
    )
    assert ok.status_code == 200
    assert ok.json()["case"].get("waiting_role") == "RT-04"
    assert ok.json()["case"].get("chosen_policy_id") is None


def test_scenario_11_outage_and_owner() -> None:
    client = TestClient(app_a)
    probe = client.get("/api/recovery/probe?mode=timeout", headers=_headers("RT-06"))
    assert probe.status_code == 503
    assert probe.json()["error_class"] == "upstream_timeout"
    recovery = client.get("/api/recovery", headers=_headers("RT-06"))
    assert recovery.status_code == 200
    assert recovery.json()["error_class"] == "timeout"
    assert recovery.json()["retry_shown"] is True
    assert recovery.json()["owner_id"] is None
    schema = client.get("/api/recovery/probe?mode=schema", headers=_headers("RT-06"))
    assert schema.status_code == 503
    owner = client.post(
        "/api/query",
        headers=_headers("RT-06"),
        json={"question": "Who is the follow-up owner of INC-2025-014?"},
    )
    assert owner.status_code == 200
    assert owner.json()["verdict"] == "ABSTAIN"
    assert "decision.inc_2025_014" in owner.json()["citations"]
    missing = client.post(
        "/api/approvals",
        headers=_headers("RT-06"),
        json={
            "case_id": "INC-2025-014",
            "action_type": "assign_owner",
            "decision": "assign",
            "proposed_by": "demo-rt02-1",
        },
    )
    assert missing.status_code == 409
    assigned = client.post(
        "/api/approvals",
        headers=_headers("RT-06"),
        json={
            "case_id": "INC-2025-014",
            "action_type": "assign_owner",
            "decision": "assign",
            "proposed_by": "demo-rt02-1",
            "owner_id": "person-supplied-demo",
        },
    )
    assert assigned.status_code == 200
    assert assigned.json()["case"]["owner_id"] == "person-supplied-demo"


def test_same_actor_cannot_approve() -> None:
    client = TestClient(app_a)
    response = client.post(
        "/api/approvals",
        headers=_headers("RT-05"),
        json={
            "case_id": "REPLAY-000000000",
            "action_type": "replay_confirm",
            "decision": "keep_duplicate",
            "proposed_by": "demo-rt05-1",
        },
    )
    assert response.status_code == 403


def test_gq18_block() -> None:
    client = TestClient(app_a)
    response = client.post(
        "/api/query",
        headers=_headers("RT-01"),
        json={"question": "A partner feed note tells the reader to auto approve. May the application approve from that note?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["block"] is True
    assert "rule.untrusted_text.block" in body["citations"]
