"""Phase 13 Half B hardening tests. HB-27-01. SC-27-01."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a
from apps.app_b.server import app as app_b
from apps.shared.identity import missing_server_key
from mcp_server import app as lake_mcp
from rest_server import app as lake_rest

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs" / "27-hardening" / "hardening-test-results.md"
COMPOSE = ROOT / "compose.yaml"
from apps.shared.oidc_session import bearer_headers

PROBE_HEADERS = bearer_headers("RT-01", correlation_id="corr-p13-27b-doc-20261018-001")


def _json_lines(captured: str) -> list[dict]:
    rows = []
    for line in captured.splitlines():
        if line.startswith("{"):
            rows.append(json.loads(line))
    return rows


def _unset_key(monkeypatch) -> None:
    monkeypatch.delenv("FABPULSE_API_KEY", raising=False)


def _assert_no_key_literals(blob: str, payload: dict) -> None:
    assert "local-demo-only" not in blob
    assert "X-Api-Key" not in blob
    assert "api_key" not in payload


@pytest.mark.skip(reason="SC-27-01 is now present. Before snapshot is in docs/27-hardening/hardening-test-results.md")
def test_hb27_01_before_missing_process_key_is_401() -> None:
    client = TestClient(app_a)
    response = client.get("/api/identity-check", headers=PROBE_HEADERS)
    assert response.status_code == 401
    assert response.json()["error_class"] == "unauthenticated"


def test_hb27_01_before_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "HB-27-01 before" in text
    assert "missing_identity" in text
    assert "Measured before" in text or "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "401" in text


def test_hb27_01_after_app_a_missing_process_key_is_503(monkeypatch, capsys) -> None:
    _unset_key(monkeypatch)
    client = TestClient(app_a)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"ok": True}
    response = client.get("/api/identity-check", headers=PROBE_HEADERS)
    assert response.status_code == 503
    body = response.json()
    assert body["error_class"] == "missing_server_key"
    assert body["ok"] is False
    assert "items" not in body
    assert "recipe" not in body
    assert "queue" not in body
    assert "FABPULSE_API_KEY" in body["message"]
    assert ".env.example" in body["message"]
    assert "local-demo-only" not in body["message"]
    captured = capsys.readouterr().out
    lines = _json_lines(captured)
    miss = [row for row in lines if row.get("event") == "server_key_missing"]
    assert miss
    payload = miss[-1]
    assert payload["service"] == "app-a"
    assert payload["status"] == 503
    assert payload["path"] == "/api/identity-check"
    blob = json.dumps(payload)
    _assert_no_key_literals(blob, payload)


def test_hb27_01_after_app_b_missing_process_key_is_503(monkeypatch) -> None:
    _unset_key(monkeypatch)
    client = TestClient(app_b)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"ok": True}
    response = client.get("/api/identity-check", headers=PROBE_HEADERS)
    assert response.status_code == 503
    assert response.json()["error_class"] == "missing_server_key"


def test_hb27_01_after_lake_rest_missing_process_key_is_503(monkeypatch) -> None:
    _unset_key(monkeypatch)
    client = TestClient(lake_rest)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"ok": True}
    response = client.get("/v1/version", headers=PROBE_HEADERS)
    assert response.status_code == 503
    assert response.json()["error_class"] == "missing_server_key"


def test_hb27_01_after_lake_mcp_missing_process_key_is_503(monkeypatch) -> None:
    _unset_key(monkeypatch)
    client = TestClient(lake_mcp)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["ok"] is True
    response = client.get("/v1/tools", headers=PROBE_HEADERS)
    assert response.status_code == 503
    assert response.json()["error_class"] == "missing_server_key"


def test_hb27_01_restored_key_without_headers_is_401(monkeypatch) -> None:
    monkeypatch.setenv("FABPULSE_API_KEY", "local-demo-only")
    response = TestClient(app_a).get("/api/identity-check")
    assert response.status_code == 401
    assert response.json()["error_class"] == "unauthenticated"


def test_hb27_01_restored_key_with_three_headers_is_200(monkeypatch) -> None:
    monkeypatch.setenv("FABPULSE_API_KEY", "local-demo-only")
    response = TestClient(app_a).get("/api/identity-check", headers=PROBE_HEADERS)
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["actor_id"] == "demo-rt01-1"
    assert body["actor_role"] == "RT-01"


def test_hb27_01_admin_role_on_queue_is_403(monkeypatch) -> None:
    monkeypatch.setenv("FABPULSE_API_KEY", "local-demo-only")
    headers = bearer_headers("GUEST", actor="guest-1")
    response = TestClient(app_a).get("/api/queue", headers=headers)
    assert response.status_code == 403
    assert response.json()["error_class"] == "forbidden_role"


def test_hb27_01_ports_8080_and_8090_stay_ungated() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    payload = yaml.safe_load(text)
    services = payload["services"]
    assert "FABPULSE_API_KEY" not in str(services["legacy"].get("environment") or {})
    assert "FABPULSE_API_KEY" not in str(services["source-gateway"].get("environment") or {})
    assert "stay without an identity check" in text
    assert '"${HOST_PORT:-8080}:8080"' in text
    assert '"${SOURCE_HOST_PORT:-8090}:8090"' in text


def test_hb27_01_missing_server_key_message_omits_key_literal() -> None:
    body = missing_server_key("corr-p13-27b-doc-20261018-001")
    assert body["error_class"] == "missing_server_key"
    assert "local-demo-only" not in body["message"]
    blob = json.dumps(body)
    assert "local-demo-only" not in blob


def test_hb27_01_after_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "HB-27-01 after" in text
    assert "missing_server_key" in text
    assert "server_key_missing" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
