"""Park one invalid intake. List it. Replay it. Never delete the row."""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from apps.shared.jsonlog import emit

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DLQ_PATH = ROOT / "apps" / "app_a" / "runtime" / "dlq.sqlite3"

_CONN: sqlite3.Connection | None = None
_PATH: Path | None = None

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS parked_intake (
    parked_id TEXT PRIMARY KEY,
    message_id TEXT NOT NULL UNIQUE,
    payload_json TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    correlation_id TEXT,
    parked_at TEXT NOT NULL,
    replayed_at TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_parked_intake_message ON parked_intake(message_id);
"""


def dlq_path() -> Path:
    env = (os.environ.get("APP_A_DLQ_PATH") or "").strip()
    return Path(env) if env else DEFAULT_DLQ_PATH


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    payload = json.loads(row["payload_json"])
    return {
        "parked_id": row["parked_id"],
        "message_id": row["message_id"],
        "payload": payload,
        "payload_json": row["payload_json"],
        "reason": row["reason"],
        "status": row["status"],
        "correlation_id": row["correlation_id"],
        "parked_at": row["parked_at"],
        "replayed_at": row["replayed_at"],
    }


def _connect(path: Path | None = None) -> sqlite3.Connection:
    global _CONN, _PATH
    target = path or dlq_path()
    if _CONN is not None and _PATH == target:
        return _CONN
    close_dlq()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(CREATE_SQL)
    conn.commit()
    _CONN = conn
    _PATH = target
    return conn


def close_dlq() -> None:
    global _CONN, _PATH
    if _CONN is not None:
        try:
            _CONN.close()
        except sqlite3.Error:
            pass
    _CONN = None
    _PATH = None


def reset_dlq() -> None:
    close_dlq()


def get_parked(parked_id: str) -> dict[str, Any] | None:
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM parked_intake WHERE parked_id = ?",
        (parked_id,),
    ).fetchone()
    return _row_to_dict(row) if row else None


def get_parked_by_message_id(message_id: str) -> dict[str, Any] | None:
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM parked_intake WHERE message_id = ?",
        (message_id,),
    ).fetchone()
    return _row_to_dict(row) if row else None


def list_parked_intakes() -> list[dict[str, Any]]:
    target = dlq_path()
    if not target.exists():
        return []
    conn = _connect(target)
    rows = conn.execute(
        "SELECT * FROM parked_intake ORDER BY parked_at, parked_id"
    ).fetchall()
    return [_row_to_dict(row) for row in rows]


def park_invalid_intake(
    event: dict[str, Any] | object,
    *,
    reason: str,
    correlation_id: str | None = None,
) -> dict[str, Any]:
    """Write or refresh one PARKED row. This function does not delete."""
    payload = event if isinstance(event, dict) else {"value": event}
    message_id = str(payload.get("message_id") or "")
    existing = get_parked_by_message_id(message_id) if message_id else None
    parked_id = existing["parked_id"] if existing else uuid4().hex
    parked_at = existing["parked_at"] if existing else _now()
    payload_json = json.dumps(payload, sort_keys=True)
    conn = _connect()
    conn.execute(
        """
        INSERT INTO parked_intake (
            parked_id, message_id, payload_json, reason, status,
            correlation_id, parked_at, replayed_at
        ) VALUES (?, ?, ?, ?, 'PARKED', ?, ?, NULL)
        ON CONFLICT(message_id) DO UPDATE SET
            payload_json = excluded.payload_json,
            reason = excluded.reason,
            correlation_id = excluded.correlation_id
        """,
        (parked_id, message_id, payload_json, reason, correlation_id, parked_at),
    )
    conn.commit()
    row = get_parked_by_message_id(message_id) if message_id else get_parked(parked_id)
    assert row is not None
    emit(
        service="app-a",
        event="intake_parked",
        level="info",
        correlation_id=correlation_id,
        path="/api/recovery",
        parked_id=row["parked_id"],
        message_id=row["message_id"],
        status=row["status"],
        reason=reason,
    )
    return row


def replace_payload(parked_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    conn = _connect()
    conn.execute(
        "UPDATE parked_intake SET payload_json = ? WHERE parked_id = ?",
        (json.dumps(payload, sort_keys=True), parked_id),
    )
    conn.commit()
    return get_parked(parked_id)


def mark_replayed(parked_id: str) -> dict[str, Any] | None:
    """Set REPLAYED. The row stays in the table."""
    conn = _connect()
    now = _now()
    conn.execute(
        """
        UPDATE parked_intake
        SET status = 'REPLAYED', replayed_at = COALESCE(replayed_at, ?)
        WHERE parked_id = ?
        """,
        (now, parked_id),
    )
    conn.commit()
    return get_parked(parked_id)


def emit_replayed(
    row: dict[str, Any],
    *,
    correlation_id: str | None,
    accepted: int,
    invalid: int,
    duplicates: int,
) -> None:
    emit(
        service="app-a",
        event="intake_replayed",
        level="info",
        correlation_id=correlation_id,
        path="/api/recovery/dlq/replay",
        parked_id=row["parked_id"],
        message_id=row["message_id"],
        status=row["status"],
        accepted=accepted,
        invalid=invalid,
        duplicates=duplicates,
    )
