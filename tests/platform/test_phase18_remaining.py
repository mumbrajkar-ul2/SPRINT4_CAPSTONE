"""Phase 18 closes DEV-010 through DEV-020 on the laptop."""
from __future__ import annotations

import json
import os
import sys
import threading
from pathlib import Path
from urllib.request import urlopen

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
LEGACY = ROOT / "fabpulse-legacy-workshop-v8-Semiconductor" / "fabpulse-legacy"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(LEGACY) not in sys.path:
    sys.path.insert(0, str(LEGACY))

os.environ.setdefault("FABPULSE_API_KEY", "local-demo-only")
os.environ.setdefault("MODEL_MODE", "replay")

from apps.app_a.server import DEMO_SESSION as SESSION_A  # noqa: E402
from apps.app_a.server import app as app_a  # noqa: E402
from apps.app_b.agent.pause import close_pause, pause_status, start_pause  # noqa: E402
from apps.app_b.server import DEMO_SESSION as SESSION_B  # noqa: E402
from apps.app_b.server import app as app_b  # noqa: E402
from services.source_gateway.server import Handler  # noqa: E402
from http.server import ThreadingHTTPServer

from apps.shared.oidc_session import bearer_headers

HEADERS = bearer_headers("RT-03", actor="rt03-demo", correlation_id="corr-p18-click-20261019-001")
KILL_ID = "corr-p18-kill-20261019-001"


def test_pause_restart_and_different_person(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("APP_B_CHECKPOINT_PATH", str(tmp_path / "checkpoints.sqlite3"))
    close_pause()
    started = start_pause(KILL_ID)
    assert started["waiting"] is True
    assert started["correlation_id"] == KILL_ID
    close_pause()
    again = pause_status(KILL_ID)
    assert again["waiting"] is True
    assert again["correlation_id"] == KILL_ID
    assert again["case_id"] == "PS000000016"
    from apps.app_b.agent.pause import resume_pause

    refused = resume_pause(KILL_ID, "model_draft")
    assert refused["ok"] is False
    accepted = resume_pause(KILL_ID, "rt03-demo")
    assert accepted["waiting"] is False
    close_pause()


def test_three_jobs_and_anonymous_case() -> None:
    client = TestClient(app_b)
    for name, role in (
        ("change-impact", "RT-03"),
        ("evidence-pack", "RT-01"),
        ("operational-handoff", "RT-06"),
    ):
        body = client.post(f"/api/agent/jobs/{name}", headers=HEADERS).json()
        assert body["tools"]
        assert body["waiting_role"] == role
        assert body["write_tools"] == []
        assert body["audit_id"]
    missing = client.get("/api/cases/PS000000016")
    assert missing.status_code >= 400
    present = client.get("/api/cases/PS000000016", headers=HEADERS)
    assert present.status_code == 200


def test_injection_blocks_both_ports() -> None:
    payload = {
        "case_id": "REPLAY-000000000",
        "scenario": "IC-01",
        "proposed_action": "approve",
    }
    for app in (app_a, app_b):
        client = TestClient(app)
        before = client.get("/api/cases/REPLAY-000000000", headers=HEADERS).json()
        response = client.post("/api/agent/run", headers=HEADERS, json=payload)
        assert response.status_code == 409
        assert response.json()["opa_verdict"] == "BLOCK"
        after = client.get("/api/cases/REPLAY-000000000", headers=HEADERS).json()
        assert after.get("status") == before.get("status")


def test_gateway_message_raises_session_queue() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        os.environ["SOURCE_GATEWAY_URL"] = f"http://127.0.0.1:{port}"
        SESSION_A.reset()
        client = TestClient(app_a)
        start = client.get("/api/demo/state", headers=HEADERS).json()
        pulled = client.post("/api/demo/gateway/pull", headers=HEADERS)
        assert pulled.status_code == 200
        body = pulled.json()
        assert body["queue_count"] == start["queue_count"] + 1
        gateway = json.loads(urlopen(f"http://127.0.0.1:{port}/api/events?limit=1", timeout=3).read())
        assert body["gateway_message"]["message_id"] == gateway["items"][0]["message_id"]
        assert body["replay_open"] is False
    finally:
        server.shutdown()
        os.environ.pop("SOURCE_GATEWAY_URL", None)


def test_demo_click_logs_correlation_id(capsys) -> None:
    SESSION_B.reset()
    client = TestClient(app_b)
    client.get("/api/demo/state", headers=HEADERS)
    captured = capsys.readouterr().out
    assert "corr-p18-click-20261019-001" in captured
    assert "demo_session" in captured


def test_demo_key_file_and_image_note() -> None:
    key_path = ROOT / "secrets" / "demo-api-key.txt"
    assert key_path.is_file()
    assert key_path.read_text(encoding="utf-8").strip() == "local-demo-only"
    note = (ROOT / "docs" / "44-remaining-deviations" / "image-digest.md").read_text(encoding="utf-8")
    assert "303065d4735d4d2fd6da888e05069200ffcee92bb0a1b4265ebfea213a2ce0d3" in note
    assert "unnamed" in note.lower() or "not named" in note.lower()


def test_react_has_injection_and_anonymous_buttons() -> None:
    text = (ROOT / "apps" / "ui_shared" / "src" / "DemoApp.jsx").read_text(encoding="utf-8")
    assert "Try to approve from the feed note" in text
    assert "Open the case with no identity" in text
    assert "Take the next gateway message" in text
    for folder in ("app_a", "app_b"):
        page = (ROOT / "apps" / folder / "ui" / "src" / "App.jsx").read_text(encoding="utf-8")
        assert "@ff/DemoApp.jsx" in page
