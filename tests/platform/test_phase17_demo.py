"""Phase 17 demo session and React source checks."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("FABPULSE_API_KEY", "local-demo-only")
os.environ.setdefault("MODEL_MODE", "replay")

from apps.app_a.server import DEMO_SESSION as SESSION_A  # noqa: E402
from apps.app_a.server import app as app_a  # noqa: E402
from apps.app_b.server import DEMO_SESSION as SESSION_B  # noqa: E402
from apps.app_b.server import app as app_b  # noqa: E402

HEADERS = {
    "X-Api-Key": "local-demo-only",
    "X-Actor-Id": "rt05-demo",
    "X-Actor-Role": "RT-05",
}


def _client(app, session):
    session.reset()
    return TestClient(app)


def test_react_source_exists() -> None:
    for folder in (ROOT / "apps" / "app_a" / "ui", ROOT / "apps" / "app_b" / "ui"):
        package = (folder / "package.json").read_text(encoding="utf-8")
        assert '"react"' in package
        jsx = list(folder.rglob("*.jsx"))
        assert jsx
    dockerfile = (ROOT / "Dockerfile.platform").read_text(encoding="utf-8")
    assert "nodejs" in dockerfile
    assert "npm run build" in dockerfile


def test_replay_queue_then_drop() -> None:
    client = _client(app_a, SESSION_A)
    start = client.get("/api/demo/state", headers=HEADERS).json()
    received = client.post("/api/demo/replay/receive", headers=HEADERS).json()
    assert received["queue_count"] == start["queue_count"] + 1
    assert received["replay"]["feed_ingested"] == "2022-04-25T19:09"
    assert received["replay"]["replay_ingested"] == "2022-04-25T20:09"
    assert received["packaged_replay_rows"] == 67
    assert received["delivery_status"] == "on the work queue"
    assert "Work-queue count is" in received["message"]
    reviewer = {
        "X-Api-Key": "local-demo-only",
        "X-Actor-Id": "rt01-demo",
        "X-Actor-Role": "RT-01",
    }
    refused = client.post("/api/demo/replay/drop", headers=reviewer)
    assert refused.status_code == 403
    assert "RT-05" in refused.json()["message"]
    assert refused.json()["delivery_status"] == "on the work queue"
    assert refused.json()["queue_count"] == received["queue_count"]
    dropped = client.post("/api/demo/replay/drop", headers=HEADERS).json()
    assert dropped["queue_count"] == start["queue_count"]
    assert dropped["delivery_status"] == "dropped"
    assert "RT-05 dropped the duplicate" in dropped["message"]


def test_recipe_clock_policy_and_outage() -> None:
    client = _client(app_a, SESSION_A)
    state = client.get("/api/demo/state", headers=HEADERS).json()
    recipe = state["recipe"]
    assert recipe["dispatch_recipe"] == "R02"
    assert recipe["started"] == "2023-01-05T16:00"
    assert recipe["tool_recipe"] == "R01"
    assert recipe["tool_effective_date"] is None
    assert recipe["change_effective"] == "2023-01-01T07:00"
    clocks = client.post("/api/demo/clocks/apply", headers=HEADERS).json()
    assert clocks["clock"]["event_time"] == "2020-12-30"
    assert clocks["clock"]["arrival_time"] == "2021-01-01"
    assert "no clock" in clocks["clock"]["metrology_clock"]
    policy = client.post("/api/demo/policy/check", headers=HEADERS).json()
    assert policy["policy"]["in_force_count"] == 4
    assert policy["policy"]["verdict"] == "ABSTAIN"
    owner = {
        "X-Api-Key": "local-demo-only",
        "X-Actor-Id": "rt04-demo",
        "X-Actor-Role": "RT-04",
    }
    decided = client.post("/api/demo/policy/decide", headers=owner, json={"choice": "keep-wait"}).json()
    assert decided["policy_choice"] == "keep-wait"
    timeout = client.post("/api/demo/outage/probe?mode=timeout", headers=HEADERS).json()
    assert timeout["last_probe"]["attempt_count"] == 2
    assert "Attempt count is 2" in timeout["last_probe"]["sentence"]
    schema = client.post("/api/demo/outage/probe?mode=schema", headers=HEADERS).json()
    assert schema["last_probe"]["attempt_count"] == 1
    assert "Attempt count is 1" in schema["last_probe"]["sentence"]
    parked = client.post("/api/demo/outage/park", headers=HEADERS).json()
    assert parked["parked_intakes"][0]["status"] == "PARKED"
    replayed = client.post("/api/demo/outage/replay", headers=HEADERS).json()
    assert replayed["parked_intakes"][0]["status"] == "REPLAYED"


def test_rule_trace_is_application_b_only() -> None:
    client_a = _client(app_a, SESSION_A)
    missing = client_a.get("/api/demo/rule-trace", headers=HEADERS)
    assert missing.status_code == 404
    client_b = _client(app_b, SESSION_B)
    traced = client_b.get("/api/demo/rule-trace", headers=HEADERS).json()
    roles = [step["role"] for step in traced["rule_trace"]]
    assert roles == [
        "historical decision",
        "earlier code",
        "specification",
        "test",
        "transformed implementation",
    ]
    assert traced["phase10_correlation_id"] == "corr-p10b-doc-20261018-001"


def test_app_b_timeout_attempt_count() -> None:
    client = _client(app_b, SESSION_B)
    timeout = client.post("/api/demo/outage/probe?mode=timeout", headers=HEADERS).json()
    assert timeout["last_probe"]["attempt_count"] == 2
