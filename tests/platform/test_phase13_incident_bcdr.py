"""Phase 13 Half B incident and BCDR tests. HB-29-01. SC-29-01. TT-29-01."""
from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.app_a.agent.tools import WRITE_TOOLS
from apps.app_a.rules.adapter import intake_dedupe
from apps.app_a.runtime.dlq import close_dlq, reset_dlq
from apps.app_a.server import app as app_a

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs" / "29-incident-bcdr" / "tabletop-results.md"
RTO_RPO = ROOT / "docs" / "29-incident-bcdr" / "rto-rpo.md"
OPERATIONS = ROOT / "operations"
RUNBOOKS = (
    OPERATIONS / "ai-incident-playbook.md",
    OPERATIONS / "containment-procedures.md",
    OPERATIONS / "bc-plan.md",
    OPERATIONS / "dr-plan.md",
)
PACKAGED_LEGACY = (
    ROOT
    / "fabpulse-legacy-workshop-v8-Semiconductor"
    / "fabpulse-legacy"
    / "data"
    / "legacy.sqlite3"
)
PACKAGED_SHA256 = "2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879"
PROBE_HEADERS = {
    "X-Api-Key": "local-demo-only",
    "X-Actor-Id": "demo-rt01-1",
    "X-Actor-Role": "RT-01",
    "X-Correlation-Id": "corr-p13-29b-doc-20261018-001",
}
FORBIDDEN_FLOOR_PHRASES = ("8 hour", "8-hour", "24 hour", "24-hour")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _row_by_message(rows: list[dict], message_id: str) -> dict:
    for row in rows:
        if row.get("message_id") == message_id:
            return row
    raise AssertionError(f"No parked row with message_id {message_id}")


def _route_paths() -> set[str]:
    paths: set[str] = set()
    for route in app_a.routes:
        path = getattr(route, "path", None)
        if path:
            paths.add(path)
    return paths


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
        raise AssertionError("Azure must not be called during HB-29-01")

    monkeypatch.setattr("apps.app_a.intelligence.azure_client.complete_azure", boom)
    monkeypatch.setattr("apps.app_a.intelligence.generate.complete_azure", boom)

    yield {
        "legacy_copy": legacy_copy,
        "dlq_path": dlq_path,
    }
    reset_dlq()
    close_dlq()
    legacy_store.DB = previous_db


def test_hb29_01_before_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "HB-29-01 before" in text
    assert "Measured before" in text
    assert "operations/ai-incident-playbook.md" in text
    assert "absent" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text


def test_hb29_01_runbooks_present_without_numeric_floors() -> None:
    assert RTO_RPO.is_file()
    assert not (OPERATIONS / "rto-rpo.md").exists()
    assert not (OPERATIONS / "tabletop-results.md").exists()
    for path in RUNBOOKS:
        assert path.is_file(), f"missing operations runbook {path.name}"
        text = path.read_text(encoding="utf-8")
        assert "Recovery time stays Unknown" in text
        assert "Recovery point stays Unknown" in text
        lower = text.lower()
        for phrase in FORBIDDEN_FLOOR_PHRASES:
            assert phrase not in lower
        assert "corr-p13-29b-doc-20261018-001" in text


def test_hb29_01_no_new_incident_route() -> None:
    paths = _route_paths()
    assert "/api/recovery" in paths
    assert "/api/recovery/dlq/replay" in paths
    assert "/health" in paths
    assert "/api/incident" not in paths


def test_hb29_01_tabletop_parked_intake_stays_listed(isolated_dlq) -> None:
    packaged_before = _sha256(PACKAGED_LEGACY)
    assert packaged_before == PACKAGED_SHA256
    assert os.environ.get("MODEL_MODE") == "replay"
    assert WRITE_TOOLS == []

    client = TestClient(app_a)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"ok": True}

    park_bad = intake_dedupe(
        [{"message_id": "DLQ-28-BAD"}],
        correlation_id="corr-p13-29b-doc-20261018-001",
    )
    assert park_bad["invalid"] == 1
    assert park_bad["accepted"] == 0
    assert park_bad["received"] == 1

    recovery = client.get("/api/recovery", headers=PROBE_HEADERS)
    assert recovery.status_code == 200
    body = recovery.json()
    assert body["owner_id"] is None
    parked = body["parked_intakes"]
    assert len(parked) >= 1
    bad = _row_by_message(parked, "DLQ-28-BAD")
    assert bad["status"] == "PARKED"

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
    still = _row_by_message(same_body["parked_intakes"], "DLQ-28-BAD")
    assert still["status"] == "PARKED"

    listed_again = client.get("/api/recovery", headers=PROBE_HEADERS)
    assert listed_again.status_code == 200
    listed_body = listed_again.json()
    assert listed_body["owner_id"] is None
    assert _row_by_message(listed_body["parked_intakes"], "DLQ-28-BAD")["status"] == "PARKED"

    health_after = client.get("/health")
    assert health_after.status_code == 200
    assert health_after.json() == {"ok": True}

    assert _sha256(PACKAGED_LEGACY) == packaged_before
    assert WRITE_TOOLS == []
    assert os.environ.get("MODEL_MODE") == "replay"


def test_hb29_01_after_snapshot_is_recorded() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert "HB-29-01 after" in text
    assert "DLQ-28-BAD" in text
    assert "PARKED" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "Recovery-time floor claimed" in text
    assert "Recovery-point floor claimed" in text
    assert "none. Cell stays Unknown" in text
    assert "Unknown" in text
