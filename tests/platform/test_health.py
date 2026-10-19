"""AT-HEALTH in-process checks for the four new listeners."""
from __future__ import annotations

from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a
from apps.app_b.server import app as app_b
from mcp_server import app as lake_mcp
from rest_server import app as lake_rest


def test_at_health_8091_lake_rest() -> None:
    response = TestClient(lake_rest).get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_at_health_8092_lake_mcp_lists_tools() -> None:
    response = TestClient(lake_mcp).get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["tools"] == ["search_items", "get_item", "get_links", "rule_at"]


def test_at_health_8100_app_a() -> None:
    response = TestClient(app_a).get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_at_health_8110_app_b() -> None:
    response = TestClient(app_b).get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
