"""Phase 13 Half B resilience tests. HB-28-01. SC-28-01."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.app_a.agent.tools import WRITE_TOOLS
from apps.app_a.routes.recovery import UPSTREAM_RETRY_COUNT
from apps.app_a.rules.adapter import intake_dedupe
from apps.app_a.runtime.dlq import close_dlq, list_parked_intakes, reset_dlq
from apps.app_a.server import app as app_a

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs" / "28-resilience" / "failure-injection-results.md"
PACKAGED_LEGACY = (
    ROOT
    / "fabpulse-legacy-workshop-v8-Semiconductor"
    / "fabpulse-legacy"
    / "data"
    / "legacy.sqlite3"
)
PACKAGED_SHA256 = "2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879"
from apps.shared.oidc_session import bearer_headers

PROBE_HEADERS = bearer_headers("RT-01", correlation_id="corr-p13-28b-doc-20261018-001")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_lines(captured: str) -> list[dict]:
    rows = []
    for line in captured.splitlines():
        if line.startswith("{"):
            rows.append(json.loads(line))
    return rows


def _inbox_count(db_path: Path, message_id: str) -> int:
    uri = f"file:{Path(db_path).as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        row = conn.execute(
            "SELECT COUNT(*) FROM gateway_inbox WHERE message_id = ?",
            (message_id,),
        ).fetchone()
        return int(row[0]) if row else 0
    finally:
        conn.close()


def _first_lot_id(db_path: Path) -> str:
    uri = f"file:{Path(db_path).as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        row = conn.execute("SELECT lot_id FROM wafer_lots ORDER BY lot_id LIMIT 1").fetchone()
        assert row is not None
        return str(row[0])
    finally:
        conn.close()


def _row_by_message(rows: list[dict], message_id: str) -> dict:
    for row in rows:
        if row.get("message_id") == message_id:
            return row
    raise AssertionError(f"No parked row with message_id {message_id}")


@pytest.fixture
def isolated_dlq(tmp_path, monkeypatch):
    legacy_copy = tmp_path / "legacy.sqlite3"
    shutil.copy2(PACKAGED_LEGACY, legacy_copy)
    dlq_path = tmp_path / "dlq.sqlite3"
    monkeypatch.setenv("MODEL_MODE", "replay")
    monkeypatch.setenv("FABPULSE_API_KEY", "local-demo-only")
    monkeypatch.setenv("APP_A_DLQ_PATH", str(dlq_path))
    monkeypatch.setenv("LEGACY_DB", str(legacy_copy))
    monkeypatch.delenv("SOURCE_GATEWAY_URL", raising=False)

    from app import store as legacy_store

    previous_db = legacy_store.DB
    legacy_store.DB = legacy_copy
    reset_dlq()

    def boom(*_args, **_kwargs):
        raise AssertionError("Azure must not be called during HB-28-01")

    monkeypatch.setattr("apps.app_a.intelligence.azure_client.complete_azure", boom)
    monkeypatch.setattr("apps.app_a.intelligence.generate.complete_azure", boom)

    yield {
        "legacy_copy": legacy_copy,
        "dlq_path": dlq_path,
        "lot_id": _first_lot_id(legacy_copy),
    }
    reset_dlq()
    close_dlq()
    legacy_store.DB = previous_db


@pytest.mark.skip(reason="SC-28-01 is now present. Before snapshot is in docs/28-resilience/failure-injection-results.md")
def test_hb28_01_before_recovery_has_no_parked_intakes() -> None:
    client = TestClient(app_a)
    response = client.get("/api/recovery", headers=PROBE_HEADERS)
    assert response.status_code == 200
    assert "parked_intakes" not in response.json()


def test_hb28_01_before_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "HB-28-01 before" in text
    assert "parked_intakes" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "Measured before" in text
    assert "invalid` | 1 | 1 | REAL" in text or "| 1 | 1 | REAL |" in text


def test_hb28_01_after_park_and_replay(isolated_dlq, capsys) -> None:
    packaged_before = _sha256(PACKAGED_LEGACY)
    assert packaged_before == PACKAGED_SHA256
    assert os.environ.get("MODEL_MODE") == "replay"
    assert WRITE_TOOLS == []
    assert UPSTREAM_RETRY_COUNT == 1

    client = TestClient(app_a)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"ok": True}

    missing = client.get("/api/recovery")
    assert missing.status_code == 401
    assert missing.json()["error_class"] == "unauthenticated"

    park_bad = intake_dedupe(
        [{"message_id": "DLQ-28-BAD"}],
        correlation_id="corr-p13-28b-doc-20261018-001",
    )
    assert park_bad["invalid"] == 1
    assert park_bad["accepted"] == 0
    assert park_bad["received"] == 1

    recovery = client.get("/api/recovery", headers=PROBE_HEADERS)
    assert recovery.status_code == 200
    parked = recovery.json()["parked_intakes"]
    assert len(parked) >= 1
    bad = _row_by_message(parked, "DLQ-28-BAD")
    assert bad["status"] == "PARKED"
    assert bad["reason"] == "missing_required_fields"

    same = client.post(
        "/api/recovery/dlq/replay",
        headers=PROBE_HEADERS,
        json={"parked_id": bad["parked_id"]},
    )
    assert same.status_code == 200
    same_body = same.json()
    assert same_body["status"] == "PARKED"
    assert same_body["invalid"] == 1
    assert same_body["accepted"] == 0
    assert _inbox_count(isolated_dlq["legacy_copy"], "DLQ-28-BAD") == 0
    assert _row_by_message(same_body["parked_intakes"], "DLQ-28-BAD")["status"] == "PARKED"

    lot_id = isolated_dlq["lot_id"]
    park_ok = intake_dedupe(
        [
            {
                "message_id": "DLQ-28-OK",
                "business_key": lot_id,
                "system": "mes",
                "event_type": "lot_started",
            }
        ],
        correlation_id="corr-p13-28b-doc-20261018-001",
    )
    assert park_ok["invalid"] == 1
    assert park_ok["accepted"] == 0
    listed = list_parked_intakes()
    ok = _row_by_message(listed, "DLQ-28-OK")
    completed = {
        "message_id": "DLQ-28-OK",
        "business_key": lot_id,
        "system": "mes",
        "event_type": "lot_started",
        "occurred_at": "2025-02-02T03:00:00Z",
    }
    replay_ok = client.post(
        "/api/recovery/dlq/replay",
        headers=PROBE_HEADERS,
        json={"parked_id": ok["parked_id"], "payload": completed},
    )
    assert replay_ok.status_code == 200
    replay_body = replay_ok.json()
    assert replay_body["accepted"] == 1
    assert replay_body["invalid"] == 0
    assert replay_body["status"] == "REPLAYED"
    still = _row_by_message(replay_body["parked_intakes"], "DLQ-28-OK")
    assert still["status"] == "REPLAYED"
    assert _inbox_count(isolated_dlq["legacy_copy"], "DLQ-28-OK") == 1
    assert _inbox_count(PACKAGED_LEGACY, "DLQ-28-OK") == 0
    assert _inbox_count(PACKAGED_LEGACY, "DLQ-28-BAD") == 0

    listed_after = client.get("/api/recovery", headers=PROBE_HEADERS)
    assert listed_after.status_code == 200
    after_rows = listed_after.json()["parked_intakes"]
    assert _row_by_message(after_rows, "DLQ-28-OK")["status"] == "REPLAYED"
    assert _row_by_message(after_rows, "DLQ-28-BAD")["status"] == "PARKED"

    again = client.post(
        "/api/recovery/dlq/replay",
        headers=PROBE_HEADERS,
        json={"parked_id": ok["parked_id"], "payload": completed},
    )
    assert again.status_code == 200
    assert again.json()["duplicates"] == 1
    assert again.json()["status"] == "REPLAYED"
    assert _inbox_count(isolated_dlq["legacy_copy"], "DLQ-28-OK") == 1

    health_after = client.get("/health")
    assert health_after.status_code == 200
    assert health_after.json() == {"ok": True}

    captured = capsys.readouterr().out
    events = {row.get("event") for row in _json_lines(captured)}
    assert "intake_parked" in events
    assert "intake_replayed" in events

    assert _sha256(PACKAGED_LEGACY) == packaged_before
    assert WRITE_TOOLS == []
    assert os.environ.get("MODEL_MODE") == "replay"


def test_hb28_01_retry_count_is_engineering_default() -> None:
    assert UPSTREAM_RETRY_COUNT == 1


def test_hb28_01_after_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "HB-28-01 after" in text
    assert "DLQ-28-BAD" in text
    assert "REPLAYED" in text
    assert "intake_parked" in text
    assert "intake_replayed" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "Unknown" in text
