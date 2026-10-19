"""Queue ranking uses transformed priority(). The queue module does not import the model."""
from __future__ import annotations

import inspect

from fastapi.testclient import TestClient

from apps.app_a.rules.adapter import live_policy, rank
from apps.app_a.routes import queue as queue_mod
from apps.app_a.server import app as app_a


def test_priority_urgent_and_no_50000_live_policy() -> None:
    assert rank("OPEN", "CRITICAL", 1) == "urgent"
    assert live_policy("APAC", 1999) == "HOLD_FOR_REVIEW"
    assert live_policy(question="urgent_amount_cutoff") == "HOLD_FOR_REVIEW"
    apac_2026 = live_policy("APAC", 2026)
    assert apac_2026["limit"] == 25000


def test_queue_module_does_not_import_generate() -> None:
    source = inspect.getsource(queue_mod)
    assert "intelligence.generate" not in source
    assert "generate(" not in source


def test_queue_order_matches_priority(api_headers) -> None:
    response = TestClient(app_a).get("/api/queue", headers=api_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["model_used"] is False
    items = body["items"]
    ids = [row["case_id"] for row in items]
    assert "C00000066" in ids
    assert "C00000103" in ids
    assert ids.index("C00000066") < ids.index("C00000003")
    replay = next(row for row in items if row["case_id"] == "REPLAY-000000000")
    assert replay["duplicate_candidate"] is True
    assert replay["waiting_role"] == "RT-05"
    assert replay["status"] == "REPLAY"
