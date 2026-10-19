"""Write one Application B audit_chain row. The model does not write this table."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from apps.app_b.audit.store import COLUMNS, get_connection

ROW_KINDS = {"agent_step", "human_approval", "control"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def next_seq(correlation_id: str) -> int:
    conn = get_connection()
    row = conn.execute(
        "SELECT MAX(seq) AS m FROM audit_chain WHERE correlation_id = ?",
        (correlation_id,),
    ).fetchone()
    current = row["m"] if row and row["m"] is not None else 0
    return int(current) + 1


def append_row(
    *,
    correlation_id: str,
    row_kind: str,
    event_type: str,
    actor_id: str | None = None,
    actor_role: str | None = None,
    case_id: str | None = None,
    step_name: str | None = None,
    tool_name: str | None = None,
    draft_present: bool = False,
    proposed_action: str | None = None,
    opa_verdict: str | None = None,
    action_type: str | None = None,
    decision: str | None = None,
    proposed_by: str | None = None,
    lake_item_ids: list[str] | None = None,
    thread_id: str | None = None,
    graph_name: str | None = None,
    interrupt_id: str | None = None,
    checkpoint_id: str | None = None,
    error_class: str | None = None,
    untrusted_quote_present: bool = False,
    notes: str | None = None,
    occurred_at: str | None = None,
) -> dict[str, Any]:
    if row_kind not in ROW_KINDS:
        raise ValueError(f"row_kind must be one of {sorted(ROW_KINDS)}")
    now = _now()
    row = {
        "audit_id": uuid4().hex,
        "correlation_id": correlation_id,
        "seq": next_seq(correlation_id),
        "row_kind": row_kind,
        "event_type": event_type,
        "occurred_at": occurred_at or now,
        "recorded_at": now,
        "actor_id": actor_id,
        "actor_role": actor_role,
        "case_id": case_id,
        "app": "app_b",
        "step_name": step_name,
        "tool_name": tool_name,
        "draft_present": 1 if draft_present else 0,
        "proposed_action": proposed_action,
        "opa_verdict": opa_verdict,
        "action_type": action_type,
        "decision": decision,
        "proposed_by": proposed_by,
        "lake_item_ids": json.dumps(list(lake_item_ids or [])),
        "thread_id": thread_id or correlation_id,
        "graph_name": graph_name,
        "interrupt_id": interrupt_id,
        "checkpoint_id": checkpoint_id,
        "error_class": error_class,
        "untrusted_quote_present": 1 if untrusted_quote_present else 0,
        "notes": notes,
    }
    conn = get_connection()
    placeholders = ", ".join("?" for _ in COLUMNS)
    conn.execute(
        f"INSERT INTO audit_chain ({', '.join(COLUMNS)}) VALUES ({placeholders})",
        [row[name] for name in COLUMNS],
    )
    conn.commit()
    return dict(row)
