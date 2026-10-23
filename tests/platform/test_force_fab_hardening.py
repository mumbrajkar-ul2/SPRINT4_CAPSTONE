"""Security headers, exact CORS, rate limit, probes, and trace ids."""
from __future__ import annotations

from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a
from apps.app_b.server import app as app_b


def test_healthz_metrics_and_traceparent() -> None:
    client = TestClient(app_a)
    live = client.get("/healthz")
    assert live.status_code == 200
    assert live.json() == {"ok": True}
    assert live.headers["x-content-type-options"] == "nosniff"
    assert "connect-src" in live.headers["content-security-policy"]
    assert "http://127.0.0.1:8110" in live.headers["content-security-policy"]
    sent = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
    traced = client.get("/health", headers={"traceparent": sent})
    echoed = traced.headers["traceparent"]
    assert echoed.startswith("00-4bf92f3577b34da6a3ce929d0e0e4736-")
    assert echoed != sent
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "ff_requests_total" in metrics.text
    assert "ff_ai_calls_total" in metrics.text


def test_application_b_connects_to_the_other_app_without_naming_it_in_source() -> None:
    response = TestClient(app_b).get("/healthz")
    policy = response.headers["content-security-policy"]
    assert "connect-src" in policy
    assert "http://127.0.0.1:8095" in policy or "8095" in policy


def test_cors_allows_the_demo_origins_only() -> None:
    client = TestClient(app_b)
    blocked = client.get("/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in blocked.headers
    allowed = client.get("/health", headers={"Origin": "http://127.0.0.1:8110"})
    assert allowed.headers["access-control-allow-origin"] == "http://127.0.0.1:8110"
    assert allowed.headers["access-control-allow-credentials"] == "true"


def test_rate_limit_is_read_on_each_request(monkeypatch) -> None:
    monkeypatch.setenv("FF_RATE_LIMIT_PER_MIN", "1")
    client = TestClient(app_a)
    headers = {"Authorization": "Bearer rate-limit-probe", "X-Forwarded-For": "203.0.113.44"}
    first = client.get("/api/identity-check", headers=headers)
    assert first.status_code == 401
    second = client.get("/api/identity-check", headers=headers)
    assert second.status_code == 429
    assert second.json()["error_class"] == "rate_limited"
    assert second.headers["retry-after"] == "60"
