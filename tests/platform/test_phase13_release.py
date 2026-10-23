"""Phase 13 Half B release tests. HB-30-01. SC-30-01."""
from __future__ import annotations

import hashlib
import os
import shutil
import sqlite3
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from apps.app_a.agent.tools import WRITE_TOOLS
from apps.app_a.rules.adapter import intake_dedupe
from apps.app_a.runtime.dlq import close_dlq, reset_dlq
from apps.app_a.server import app as app_a

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "compose.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "verify.yml"
BACKUP = ROOT / "docs" / "30-release" / "backup-validation.md"
RELEASE = ROOT / "docs" / "30-release" / "release-plan.md"
HOST_DLQ = ROOT / "apps" / "app_a" / "runtime" / "dlq.sqlite3"
HOST_CHECKPOINT = ROOT / "apps" / "app_a" / "runtime" / "checkpoints.sqlite3"
HOST_AUDIT = ROOT / "apps" / "app_a" / "audit" / "audit_chain.sqlite3"
PACKAGED_LEGACY = (
    ROOT
    / "fabpulse-legacy-workshop-v8-Semiconductor"
    / "fabpulse-legacy"
    / "data"
    / "legacy.sqlite3"
)
PACKAGED_SHA256 = "2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879"
from apps.shared.oidc_session import bearer_headers

PROBE_HEADERS = bearer_headers("RT-01", correlation_id="corr-p13-30b-doc-20261018-001")
DLQ_BIND = "./apps/app_a/runtime/dlq.sqlite3:/opt/platform/apps/app_a/runtime/dlq.sqlite3"
CHECKPOINT_BIND = (
    "./apps/app_a/runtime/checkpoints.sqlite3:/opt/platform/apps/app_a/runtime/checkpoints.sqlite3"
)
AUDIT_BIND = "./apps/app_a/audit/audit_chain.sqlite3:/opt/platform/apps/app_a/audit/audit_chain.sqlite3"
REPLAY_BIND = "./operations/model-replay:/opt/platform/operations/model-replay:ro"
RECREATE_CMD = "docker compose up -d --force-recreate app-a"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _compose() -> dict:
    return yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))


def _row_by_message(rows: list[dict], message_id: str) -> dict:
    for row in rows:
        if row.get("message_id") == message_id:
            return row
    raise AssertionError(f"No parked row with message_id {message_id}")


def _status_from_file(path: Path, message_id: str) -> str:
    uri = f"file:{path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        row = conn.execute(
            "SELECT status FROM parked_intake WHERE message_id = ?",
            (message_id,),
        ).fetchone()
        assert row is not None, f"{path} has no row for {message_id}"
        return str(row[0])
    finally:
        conn.close()


def _route_paths() -> set[str]:
    paths: set[str] = set()
    for route in app_a.routes:
        path = getattr(route, "path", None)
        if path:
            paths.add(path)
    return paths


@pytest.fixture
def host_dlq(tmp_path, monkeypatch):
    legacy_copy = tmp_path / "legacy.sqlite3"
    shutil.copy2(PACKAGED_LEGACY, legacy_copy)
    monkeypatch.setenv("MODEL_MODE", "replay")
    monkeypatch.setenv("FABPULSE_API_KEY", "local-demo-only")
    monkeypatch.setenv("APP_A_DLQ_PATH", str(HOST_DLQ))
    monkeypatch.setenv("LEGACY_DB", str(legacy_copy))
    monkeypatch.delenv("SOURCE_GATEWAY_URL", raising=False)

    from app import store as legacy_store

    previous_db = legacy_store.DB
    legacy_store.DB = legacy_copy
    reset_dlq()

    def boom(*_args, **_kwargs):
        raise AssertionError("Azure must not be called during HB-30-01")

    monkeypatch.setattr("apps.app_a.intelligence.azure_client.complete_azure", boom)
    monkeypatch.setattr("apps.app_a.intelligence.generate.complete_azure", boom)

    yield {"legacy_copy": legacy_copy, "backup_dir": tmp_path / "backups"}
    reset_dlq()
    close_dlq()
    legacy_store.DB = previous_db


def test_hb30_01_before_snapshot_is_recorded() -> None:
    text = BACKUP.read_text(encoding="utf-8")
    assert "HB-30-01 before" in text
    assert "Measured before" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "app-a volumes omit the three sqlite files" in text
    assert "model-replay" in text


def test_hb30_01_host_sqlite_paths_are_files() -> None:
    for path in (HOST_DLQ, HOST_CHECKPOINT, HOST_AUDIT):
        assert path.is_file(), f"{path} must be a file so Docker does not create a directory"
        assert not path.is_dir()


def test_hb30_01_compose_has_three_sqlite_binds() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    payload = _compose()
    volumes = [str(row) for row in payload["services"]["app-a"]["volumes"]]
    assert REPLAY_BIND in volumes
    assert DLQ_BIND in volumes
    assert CHECKPOINT_BIND in volumes
    assert AUDIT_BIND in volumes
    assert DLQ_BIND in text
    assert CHECKPOINT_BIND in text
    assert AUDIT_BIND in text
    app_b_volumes = str(payload["services"]["app-b"]["volumes"])
    assert "dlq.sqlite3" not in app_b_volumes
    assert "checkpoints.sqlite3" not in app_b_volumes
    assert "audit_chain.sqlite3" not in app_b_volumes


def test_hb30_01_ports_8080_and_8090_stay_ungated() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    services = _compose()["services"]
    assert "FABPULSE_API_KEY" not in str(services["legacy"].get("environment") or {})
    assert "FABPULSE_API_KEY" not in str(services["source-gateway"].get("environment") or {})
    assert "stay without an identity check" in text
    assert '"${HOST_PORT:-8080}:8080"' in text
    assert '"${SOURCE_HOST_PORT:-8090}:8090"' in text


def test_hb30_01_model_mode_replay_no_new_flag() -> None:
    payload = _compose()
    env = payload["services"]["app-a"]["environment"]
    assert "replay" in str(env["MODEL_MODE"])
    compose_text = COMPOSE.read_text(encoding="utf-8")
    assert "FEATURE_" not in compose_text
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "MODEL_MODE: replay" in workflow
    assert "generate --reset" not in workflow


def test_hb30_01_no_login_server_or_new_route() -> None:
    payload = _compose()
    assert "login" not in payload["services"]
    paths = _route_paths()
    assert "/health" in paths
    assert "/api/recovery" in paths
    assert "/api/recovery/dlq/replay" in paths
    assert "/login" not in paths
    assert "/api/login" not in paths
    assert "/api/incident" not in paths


def test_hb30_01_park_reopen_same_host_file(host_dlq) -> None:
    packaged_before = _sha256(PACKAGED_LEGACY)
    assert packaged_before == PACKAGED_SHA256
    assert os.environ.get("MODEL_MODE") == "replay"
    assert WRITE_TOOLS == []
    assert HOST_DLQ.is_file()

    client = TestClient(app_a)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"ok": True}

    park_bad = intake_dedupe(
        [{"message_id": "DLQ-30-ROLL"}],
        correlation_id="corr-p13-30b-doc-20261018-001",
    )
    assert park_bad["invalid"] == 1
    assert park_bad["accepted"] == 0
    assert park_bad["received"] == 1

    close_dlq()
    assert _status_from_file(HOST_DLQ, "DLQ-30-ROLL") == "PARKED"

    host_dlq["backup_dir"].mkdir(parents=True, exist_ok=True)
    copy_path = host_dlq["backup_dir"] / "dlq.sqlite3"
    shutil.copy2(HOST_DLQ, copy_path)
    assert _status_from_file(copy_path, "DLQ-30-ROLL") == "PARKED"
    shutil.copy2(HOST_CHECKPOINT, host_dlq["backup_dir"] / "checkpoints.sqlite3")
    shutil.copy2(HOST_AUDIT, host_dlq["backup_dir"] / "audit_chain.sqlite3")
    assert (host_dlq["backup_dir"] / "checkpoints.sqlite3").is_file()
    assert (host_dlq["backup_dir"] / "audit_chain.sqlite3").is_file()

    recovery = client.get("/api/recovery", headers=PROBE_HEADERS)
    assert recovery.status_code == 200
    body = recovery.json()
    assert body["owner_id"] is None
    parked = _row_by_message(body["parked_intakes"], "DLQ-30-ROLL")
    assert parked["status"] == "PARKED"

    same = client.post(
        "/api/recovery/dlq/replay",
        headers=PROBE_HEADERS,
        json={"parked_id": parked["parked_id"]},
    )
    assert same.status_code == 200
    same_body = same.json()
    assert same_body["status"] == "PARKED"
    assert same_body["invalid"] == 1
    assert same_body["accepted"] == 0
    still = _row_by_message(same_body["parked_intakes"], "DLQ-30-ROLL")
    assert still["status"] == "PARKED"

    close_dlq()
    assert _status_from_file(HOST_DLQ, "DLQ-30-ROLL") == "PARKED"

    health_after = client.get("/health")
    assert health_after.status_code == 200
    assert health_after.json() == {"ok": True}
    assert _sha256(PACKAGED_LEGACY) == packaged_before
    assert WRITE_TOOLS == []
    assert os.environ.get("MODEL_MODE") == "replay"


def test_hb30_01_after_snapshot_is_recorded() -> None:
    text = BACKUP.read_text(encoding="utf-8")
    release = RELEASE.read_text(encoding="utf-8")
    assert "HB-30-01 after" in text
    assert "DLQ-30-ROLL" in text
    assert "PARKED" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "NEEDS_HUMAN" in text
    assert RECREATE_CMD in text
    assert "Recovery-time floor claimed" in text
    assert "none. Cell stays Unknown" in text
    assert DLQ_BIND in release or "dlq.sqlite3" in release
    assert "Honesty | REAL" in release or "Honesty: REAL" in release


def test_hb30_01_needs_human_recreate_row() -> None:
    text = BACKUP.read_text(encoding="utf-8")
    assert "NEEDS_HUMAN" in text
    assert RECREATE_CMD in text
    assert "did not invent a recreate pass" in text
