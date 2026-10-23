"""Application A closed roles, static UI, and Phase 8 identity behaviour."""
from __future__ import annotations

from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a


def test_health_and_ui_open() -> None:
    client = TestClient(app_a)
    assert client.get("/health").json() == {"ok": True}
    page = client.get("/")
    assert page.status_code == 200
    assert "Role picker" in page.text
    css = client.get("/assets/styles.css")
    assert css.status_code == 200


def test_unknown_role_is_403(api_headers) -> None:
    forged = dict(api_headers)
    forged["X-Actor-Role"] = "ADMIN"
    ignored = TestClient(app_a).get("/api/queue", headers=forged)
    assert ignored.status_code == 200
    from apps.shared.oidc_session import bearer_headers

    guest = bearer_headers("GUEST", actor="guest-1")
    response = TestClient(app_a).get("/api/queue", headers=guest)
    assert response.status_code == 403
    assert response.json()["error_class"] == "forbidden_role"


def test_queue_without_headers_is_401() -> None:
    response = TestClient(app_a).get("/api/queue")
    assert response.status_code == 401
    assert response.json()["error_class"] == "unauthenticated"
