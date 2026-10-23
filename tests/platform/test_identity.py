"""AT-ID-A, AT-ID-B, AT-ID-HIT, AT-ID-KEY, and case-read 401."""
from __future__ import annotations

from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a
from apps.app_b.server import app as app_b


def test_at_id_a_missing_identity() -> None:
    client = TestClient(app_a)
    response = client.get("/api/identity-check")
    assert response.status_code == 401
    body = response.json()
    assert body["error_class"] == "unauthenticated"
    assert "items" not in body
    assert "recipe" not in body
    assert "queue" not in body


def test_at_id_b_missing_identity() -> None:
    client = TestClient(app_b)
    response = client.get("/api/identity-check")
    assert response.status_code == 401
    assert response.json()["error_class"] == "unauthenticated"


def test_at_id_hit_echoes_actor(api_headers) -> None:
    for app in (app_a, app_b):
        client = TestClient(app)
        response = client.get("/api/identity-check", headers=api_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["ok"] is True
        assert body["actor_id"] == "demo-rt01-1"
        assert body["actor_role"] == "RT-01"
        assert "recipe_version" not in body
        assert "queue" not in body
        assert "items" not in body


def test_at_id_key_wrong_key(api_headers) -> None:
    headers = dict(api_headers)
    headers["X-Api-Key"] = "wrong"
    headers["X-Actor-Id"] = "forged-actor"
    headers["X-Actor-Role"] = "ADMIN"
    for app in (app_a, app_b):
        response = TestClient(app).get("/api/identity-check", headers=headers)
        assert response.status_code == 200
        body = response.json()
        assert body["actor_id"] == "demo-rt01-1"
        assert body["actor_role"] == "RT-01"


def test_case_read_without_headers_is_401() -> None:
    for app in (app_a, app_b):
        response = TestClient(app).get("/api/cases/CASE-1")
        assert response.status_code == 401
        assert response.json()["error_class"] == "unauthenticated"


def test_health_stays_open() -> None:
    for app in (app_a, app_b):
        response = TestClient(app).get("/health")
        assert response.status_code == 200
        assert response.json() == {"ok": True}
