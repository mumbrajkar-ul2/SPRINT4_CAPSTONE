"""AD-CHECKPOINT. SqliteSaver on apps/app_a/runtime/checkpoints.sqlite3."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CHECKPOINT_PATH = ROOT / "apps" / "app_a" / "runtime" / "checkpoints.sqlite3"
CHECKPOINT_PATH = DEFAULT_CHECKPOINT_PATH

_SAVER: SqliteSaver | None = None
_CONN: sqlite3.Connection | None = None
_PATH: Path | None = None


def checkpoint_path() -> Path:
    env = (os.environ.get("APP_A_CHECKPOINT_PATH") or "").strip()
    return Path(env) if env else DEFAULT_CHECKPOINT_PATH


def open_connection(path: Path | None = None) -> sqlite3.Connection:
    target = path or checkpoint_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target), check_same_thread=False)
    return conn


def get_saver(path: Path | None = None) -> SqliteSaver:
    """Return a SqliteSaver bound to the checkpoint file. Reuses one connection per path."""
    global _SAVER, _CONN, _PATH
    target = path or checkpoint_path()
    if _SAVER is not None and _PATH == target and _CONN is not None:
        return _SAVER
    if _CONN is not None:
        try:
            _CONN.close()
        except sqlite3.Error:
            pass
    _CONN = open_connection(target)
    _SAVER = SqliteSaver(_CONN)
    _PATH = target
    return _SAVER


def new_saver(path: Path | None = None) -> tuple[sqlite3.Connection, SqliteSaver]:
    """Open a new connection and saver. Used to prove a reopen sees the wait."""
    conn = open_connection(path)
    return conn, SqliteSaver(conn)


def reset_checkpointer() -> None:
    global _SAVER, _CONN, _PATH
    if _CONN is not None:
        try:
            _CONN.close()
        except sqlite3.Error:
            pass
    _SAVER = None
    _CONN = None
    _PATH = None


def list_thread_ids(path: Path | None = None) -> list[str]:
    target = path or checkpoint_path()
    if not target.exists():
        return []
    conn = sqlite3.connect(f"file:{target.as_posix()}?mode=ro", uri=True)
    try:
        names = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "checkpoints" not in names:
            return []
        rows = conn.execute("SELECT DISTINCT thread_id FROM checkpoints").fetchall()
        return [str(row[0]) for row in rows]
    finally:
        conn.close()
