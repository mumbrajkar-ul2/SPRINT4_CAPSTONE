"""AT-LOG-JSON. Identity miss writes a JSON line. The key is absent."""
from __future__ import annotations

import json

from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a


def test_at_log_json_identity_missing(capsys) -> None:
    TestClient(app_a).get("/api/identity-check")
    captured = capsys.readouterr().out
    lines = [line for line in captured.splitlines() if line.startswith("{")]
    assert lines
    payload = json.loads(lines[-1])
    assert payload["service"] == "app-a"
    assert payload["event"] == "identity_missing"
    assert payload["level"] == "warn"
    blob = json.dumps(payload)
    assert "local-demo-only" not in blob
    assert "X-Api-Key" not in blob
    assert "api_key" not in payload
