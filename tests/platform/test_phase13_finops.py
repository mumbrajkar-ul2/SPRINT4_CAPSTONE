"""Phase 13 Half B FinOps tests. HB-32-01. SC-32-01."""
from __future__ import annotations

import json
import os
import socket
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.app_a.agent.tools import WRITE_TOOLS
from apps.app_a.intelligence import generate as generate_mod
from apps.app_a.server import app as app_a

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs" / "32-finops" / "baseline-vs-actual-token-analysis.md"
HIT_QUESTION = "Which port does the Context Lake REST listener use?"
MISS_QUESTION = "What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file"
HIT_CORR = "corr-p13-32b-doc-20261018-001"
MISS_CORR = "corr-p13-32b-miss-001"
PROBE_HEADERS = {
    "X-Api-Key": "local-demo-only",
    "X-Actor-Id": "demo-rt01-1",
    "X-Actor-Role": "RT-01",
    "X-Correlation-Id": HIT_CORR,
}


def _json_lines(captured: str) -> list[dict]:
    rows = []
    for line in captured.splitlines():
        if line.startswith("{"):
            rows.append(json.loads(line))
    return rows


def _events(rows: list[dict], name: str) -> list[dict]:
    return [row for row in rows if row.get("event") == name]


@pytest.fixture
def replay_only(monkeypatch):
    monkeypatch.setenv("MODEL_MODE", "replay")
    monkeypatch.setenv("FABPULSE_API_KEY", "local-demo-only")
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)

    def boom(*_args, **_kwargs):
        raise AssertionError("Azure must not be called during HB-32-01")

    def forbid(*_args, **_kwargs):
        raise AssertionError("HB-32-01 must not open a network socket")

    monkeypatch.setattr("apps.app_a.intelligence.azure_client.complete_azure", boom)
    monkeypatch.setattr("apps.app_a.intelligence.generate.complete_azure", boom)
    monkeypatch.setattr(socket, "create_connection", forbid)

    real_generate = generate_mod.generate

    def guarded_generate(*args, **kwargs):
        previous_socket = socket.socket
        socket.socket = forbid  # type: ignore[method-assign]
        try:
            return real_generate(*args, **kwargs)
        finally:
            socket.socket = previous_socket

    monkeypatch.setattr(generate_mod, "generate", guarded_generate)
    monkeypatch.setattr("apps.app_a.routes.query.generate", guarded_generate)
    yield


@pytest.mark.skip(reason="SC-32-01 is now present. Before snapshot is in docs/32-finops/baseline-vs-actual-token-analysis.md")
def test_hb32_01_before_replay_hit_has_no_prompt_tokens() -> None:
    client = TestClient(app_a)
    response = client.post(
        "/api/query",
        headers=PROBE_HEADERS,
        json={"question": HIT_QUESTION},
    )
    assert response.status_code == 200
    assert response.json()["verdict"] == "ANSWER"


def test_hb32_01_before_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "HB-32-01 before" in text
    assert "Measured before" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "no line has `prompt_tokens`" in text or "omit `prompt_tokens`" in text
    assert "request_ok" in text
    assert HIT_QUESTION in text
    assert HIT_CORR in text
    assert "4982.61" in text
    assert "0.603" in text
    assert "SIMULATED" in text
    assert "BO-11" in text
    assert "PROPOSED" in text


def test_hb32_01_after_replay_hit_emits_replay_tokens(replay_only, capsys) -> None:
    assert os.environ.get("MODEL_MODE") == "replay"
    assert WRITE_TOOLS == []

    client = TestClient(app_a)
    capsys.readouterr()

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"ok": True}

    response = client.post(
        "/api/query",
        headers=PROBE_HEADERS,
        json={"question": HIT_QUESTION},
    )
    captured = capsys.readouterr().out
    body = response.json()
    rows = _json_lines(captured)
    tokens = _events(rows, "replay_tokens")
    misses = _events(rows, "replay_miss")
    requests = _events(rows, "request_ok")

    assert response.status_code == 200
    assert body["verdict"] == "ANSWER"
    assert body["error_class"] is None
    assert "arch.listener.lake_rest_8091" in (body.get("citations") or [])
    assert body["sentence"]
    assert body["correlation_id"] == HIT_CORR
    assert body.get("model_mode") == "replay"
    assert body.get("answer_source") == "replay_file"
    assert "prompt_tokens" not in body
    assert "completion_tokens" not in body
    assert "token" not in body

    assert len(tokens) == 1
    line = tokens[0]
    assert line["service"] == "app-a"
    assert line["event"] == "replay_tokens"
    assert line["level"] == "info"
    assert line["path"] == "/api/query"
    assert line["status"] == 200
    assert line["correlation_id"] == HIT_CORR
    assert line["model_mode"] == "replay"
    assert line["prompt_tokens"] == 0
    assert line["completion_tokens"] == 0
    assert "token" not in line
    assert "api_key" not in line
    assert "local-demo-only" not in json.dumps(line)
    assert misses == []
    assert requests
    assert all(row.get("event") != "replay_tokens" or row is line for row in rows)


def test_hb32_01_after_replay_miss_adds_token_fields(replay_only, capsys) -> None:
    client = TestClient(app_a)
    capsys.readouterr()
    response = client.post(
        "/api/query",
        headers={**PROBE_HEADERS, "X-Correlation-Id": MISS_CORR},
        json={"question": MISS_QUESTION},
    )
    captured = capsys.readouterr().out
    body = response.json()
    rows = _json_lines(captured)
    misses = _events(rows, "replay_miss")
    tokens = _events(rows, "replay_tokens")

    assert response.status_code == 200
    assert body["verdict"] == "ABSTAIN"
    assert body["error_class"] == "replay_miss"
    assert body["sentence"] == ""
    assert "arch.listener.lake_rest_8091" in (body.get("retrieved_item_ids") or [])
    assert body["correlation_id"] == MISS_CORR
    assert "prompt_tokens" not in body
    assert "completion_tokens" not in body

    assert len(misses) == 1
    line = misses[0]
    assert line["service"] == "app-a"
    assert line["event"] == "replay_miss"
    assert line["model_mode"] == "replay"
    assert line["error_class"] == "replay_miss"
    assert line["correlation_id"] == MISS_CORR
    assert line["path"] == "/api/query"
    assert line["status"] == 200
    assert line["prompt_tokens"] == 0
    assert line["completion_tokens"] == 0
    assert line.get("prompt_hash")
    assert "token" not in line
    assert tokens == []


def test_hb32_01_cited_answer_is_not_replay_miss(replay_only, capsys) -> None:
    client = TestClient(app_a)
    capsys.readouterr()
    response = client.post(
        "/api/query",
        headers=PROBE_HEADERS,
        json={"question": HIT_QUESTION},
    )
    captured = capsys.readouterr().out
    body = response.json()
    rows = _json_lines(captured)
    misses = _events(rows, "replay_miss")
    tokens = _events(rows, "replay_tokens")

    assert response.status_code == 200
    assert body["verdict"] == "ANSWER"
    assert body["error_class"] is None
    assert "arch.listener.lake_rest_8091" in (body.get("citations") or [])
    assert misses == []
    assert len(tokens) == 1
    assert tokens[0]["event"] == "replay_tokens"
    assert tokens[0]["prompt_tokens"] == 0
    assert tokens[0]["completion_tokens"] == 0
