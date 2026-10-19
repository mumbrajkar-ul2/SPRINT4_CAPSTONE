"""Rebuild a waiting approval from SqliteSaver and audit_chain rows."""
from __future__ import annotations

from typing import Any

from apps.app_a.agent.checkpointer import list_thread_ids
from apps.app_a.agent.graph import snapshot_for
from apps.app_a.audit.store import get_connection


def _snapshot_waiting(correlation_id: str) -> dict[str, Any] | None:
    try:
        snap = snapshot_for(correlation_id)
    except Exception:
        return None
    if snap is None:
        return None
    nxt = tuple(getattr(snap, "next", ()) or ())
    pending = bool(getattr(snap, "interrupts", None)) or "interrupt_wait" in nxt
    if not pending:
        return None
    values = dict(getattr(snap, "values", {}) or {})
    return {
        "correlation_id": correlation_id,
        "thread_id": correlation_id,
        "case_id": values.get("case_id"),
        "waiting_role": values.get("waiting_role"),
        "draft_plan": values.get("draft_plan"),
        "proposed_action": values.get("proposed_action"),
        "proposed_by": values.get("proposed_by") or "model_draft",
        "opa_verdict": values.get("opa_verdict"),
    }


def waiting_ids_from_audit(case_id: str | None = None) -> list[str]:
    conn = get_connection()
    sql = """
        SELECT DISTINCT correlation_id
        FROM audit_chain
        WHERE step_name = 'interrupt_wait' AND notes = 'paused'
    """
    args: list[Any] = []
    if case_id:
        sql += " AND case_id = ?"
        args.append(case_id)
    paused = [row["correlation_id"] for row in conn.execute(sql, args)]
    finished = {
        row["correlation_id"]
        for row in conn.execute(
            """
            SELECT DISTINCT correlation_id FROM audit_chain
            WHERE row_kind = 'human_approval'
               OR (step_name = 'interrupt_wait' AND notes = 'resumed')
            """
        )
    }
    return [cid for cid in paused if cid not in finished]


def overlay_for_case(case_id: str) -> dict[str, Any] | None:
    for cid in waiting_ids_from_audit(case_id):
        found = _snapshot_waiting(cid)
        if found:
            return found
    for thread_id in list_thread_ids():
        found = _snapshot_waiting(thread_id)
        if found and found.get("case_id") == case_id:
            return found
    return None


def find_waiting_thread(case_id: str, correlation_id: str | None = None) -> dict[str, Any] | None:
    if correlation_id:
        found = _snapshot_waiting(correlation_id)
        if found:
            found["case_id"] = found.get("case_id") or case_id
            return found
    return overlay_for_case(case_id)
