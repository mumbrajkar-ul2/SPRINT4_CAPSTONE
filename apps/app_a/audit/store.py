"""SQLite file for table audit_chain. 27 columns from audit-chain.md."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_AUDIT_PATH = ROOT / "apps" / "app_a" / "audit" / "audit_chain.sqlite3"

COLUMNS = (
    "audit_id",
    "correlation_id",
    "seq",
    "row_kind",
    "event_type",
    "occurred_at",
    "recorded_at",
    "actor_id",
    "actor_role",
    "case_id",
    "app",
    "step_name",
    "tool_name",
    "draft_present",
    "proposed_action",
    "opa_verdict",
    "action_type",
    "decision",
    "proposed_by",
    "lake_item_ids",
    "thread_id",
    "graph_name",
    "interrupt_id",
    "checkpoint_id",
    "error_class",
    "untrusted_quote_present",
    "notes",
)

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS audit_chain (
    audit_id TEXT PRIMARY KEY,
    correlation_id TEXT NOT NULL,
    seq INTEGER NOT NULL,
    row_kind TEXT NOT NULL CHECK (row_kind IN ('agent_step', 'human_approval', 'control')),
    event_type TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    actor_id TEXT,
    actor_role TEXT,
    case_id TEXT,
    app TEXT NOT NULL,
    step_name TEXT,
    tool_name TEXT,
    draft_present INTEGER NOT NULL,
    proposed_action TEXT,
    opa_verdict TEXT,
    action_type TEXT,
    decision TEXT,
    proposed_by TEXT,
    lake_item_ids TEXT NOT NULL,
    thread_id TEXT,
    graph_name TEXT,
    interrupt_id TEXT,
    checkpoint_id TEXT,
    error_class TEXT,
    untrusted_quote_present INTEGER NOT NULL,
    notes TEXT,
    UNIQUE (correlation_id, seq)
);
CREATE INDEX IF NOT EXISTS idx_audit_correlation ON audit_chain (correlation_id);
"""

_CONN: sqlite3.Connection | None = None
_PATH: Path | None = None


def audit_path() -> Path:
    env = (os.environ.get("APP_A_AUDIT_PATH") or "").strip()
    return Path(env) if env else DEFAULT_AUDIT_PATH


def get_connection(path: Path | None = None) -> sqlite3.Connection:
    global _CONN, _PATH
    target = path or audit_path()
    if _CONN is not None and _PATH == target:
        return _CONN
    if _CONN is not None:
        try:
            _CONN.close()
        except sqlite3.Error:
            pass
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(CREATE_SQL)
    _CONN = conn
    _PATH = target
    return conn


def reset_audit_store() -> None:
    global _CONN, _PATH
    if _CONN is not None:
        try:
            _CONN.execute("DELETE FROM audit_chain")
            _CONN.commit()
        except sqlite3.Error:
            pass
        try:
            _CONN.close()
        except sqlite3.Error:
            pass
    _CONN = None
    _PATH = None
