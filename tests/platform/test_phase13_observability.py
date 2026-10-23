"""Phase 13 Half B observability tests. HB-31-01. SC-31-01."""
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
RESULTS = ROOT / "docs" / "31-observability" / "telemetry-results.md"
MISS_QUESTION = "What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file"
CITE_QUESTION = "Which port does the Context Lake REST listener use?"
MISS_CORR = "corr-p13-31b-doc-20261018-001"
CITE_CORR = "corr-p13-31b-cite-001"
from apps.shared.oidc_session import bearer_headers

PROBE_HEADERS = bearer_headers("RT-01", correlation_id=MISS_CORR)


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
        raise AssertionError("Azure must not be called during HB-31-01")

    def forbid(*_args, **_kwargs):
        raise AssertionError("HB-31-01 must not open a network socket")

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


@pytest.mark.skip(reason="SC-31-01 is now present. Before snapshot is in docs/31-observability/telemetry-results.md")
def test_hb31_01_before_replay_miss_line_absent() -> None:
    client = TestClient(app_a)
    response = client.post(
        "/api/query",
        headers=PROBE_HEADERS,
        json={"question": MISS_QUESTION},
    )
    assert response.status_code == 200
    assert response.json()["error_class"] == "replay_miss"


def test_hb31_01_before_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "HB-31-01 before" in text
    assert "Measured before" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "no line has `event=replay_miss`" in text or "omit `replay_miss`" in text
    assert "request_ok" in text
    assert MISS_QUESTION in text


def test_hb31_01_after_replay_miss_emits_one_line(replay_only, capsys) -> None:
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
        json={"question": MISS_QUESTION},
    )
    captured = capsys.readouterr().out
    body = response.json()
    rows = _json_lines(captured)
    misses = _events(rows, "replay_miss")
    requests = _events(rows, "request_ok")

    assert response.status_code == 200
    assert body["verdict"] == "ABSTAIN"
    assert body["error_class"] == "replay_miss"
    assert body["sentence"] == ""
    assert "arch.listener.lake_rest_8091" in (body.get("retrieved_item_ids") or [])
    assert body["correlation_id"] == MISS_CORR
    assert body.get("model_mode") == "replay"
    assert body.get("answer_source") == "replay_file"

    assert len(misses) == 1
    line = misses[0]
    assert line["service"] == "app-a"
    assert line["event"] == "replay_miss"
    assert line["level"] == "info"
    assert line["path"] == "/api/query"
    assert line["status"] == 200
    assert line["correlation_id"] == MISS_CORR
    assert line["model_mode"] == "replay"
    assert line["error_class"] == "replay_miss"
    assert line.get("prompt_hash")
    assert "api_key" not in line
    assert "token" not in line
    assert "local-demo-only" not in json.dumps(line)
    assert requests
    assert all(row.get("event") != "replay_miss" or row is line for row in rows)


def test_hb31_01_cited_answer_is_not_replay_miss(replay_only, capsys) -> None:
    client = TestClient(app_a)
    capsys.readouterr()
    response = client.post(
        "/api/query",
        headers={**PROBE_HEADERS, "X-Correlation-Id": CITE_CORR},
        json={"question": CITE_QUESTION},
    )
    captured = capsys.readouterr().out
    body = response.json()
    rows = _json_lines(captured)
    misses = _events(rows, "replay_miss")

    assert response.status_code == 200
    assert body["verdict"] == "ANSWER"
    assert body["error_class"] is None
    assert "arch.listener.lake_rest_8091" in (body.get("citations") or [])
    assert body["sentence"]
    assert misses == []
    assert any(row.get("event") == "request_ok" for row in rows)
