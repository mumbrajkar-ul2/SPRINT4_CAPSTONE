"""AT-LAKE-RO, AT-LAKE-KEY, and version read."""
from __future__ import annotations

from fastapi.testclient import TestClient

from rest_server import app as lake_rest


def test_at_lake_ro_post_rejected(lake_headers) -> None:
    response = TestClient(lake_rest).post("/v1/items", headers=lake_headers, json={})
    assert response.status_code == 405
    assert response.json()["error_class"] == "lake_write_rejected"


def test_at_lake_key_version_without_key() -> None:
    response = TestClient(lake_rest).get("/v1/version")
    assert response.status_code == 401
    assert response.json()["error_class"] == "missing_identity"


def test_lake_version_with_key(lake_headers) -> None:
    response = TestClient(lake_rest).get("/v1/version", headers=lake_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["lake_version"] == "1.0.0"
    assert body["sqlite_sha256"]
