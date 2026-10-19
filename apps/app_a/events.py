"""Audit write helper. Phase 10 rows go to table audit_chain."""
from __future__ import annotations

from typing import Any
from uuid import uuid4

from apps.app_a.audit.reader import read_trace
from apps.app_a.audit.store import reset_audit_store
from apps.app_a.audit.writer import append_row


def mint_correlation_id() -> str:
    return f"corr-app-a-{uuid4().hex[:12]}"


def record_event(
    event_type: str,
    *,
    correlation_id: str | None,
    actor_id: str | None,
    actor_role: str | None,
    case_id: str | None,
    lake_item_ids: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    extra = extra or {}
    row_kind = "human_approval" if event_type in {"EV-09", "EV-10"} else "control"
    if event_type == "EV-08":
        row_kind = "agent_step"
    return append_row(
        correlation_id=correlation_id or mint_correlation_id(),
        row_kind=row_kind,
        event_type=event_type,
        actor_id=actor_id,
        actor_role=actor_role,
        case_id=case_id,
        step_name=extra.get("step_name"),
        tool_name=extra.get("tool_name"),
        draft_present=bool(extra.get("draft_present")),
        proposed_action=extra.get("proposed_action"),
        opa_verdict=extra.get("opa_verdict"),
        action_type=extra.get("action_type"),
        decision=extra.get("decision"),
        proposed_by=extra.get("proposed_by"),
        lake_item_ids=list(lake_item_ids or extra.get("lake_item_ids") or []),
        thread_id=extra.get("thread_id") or correlation_id,
        graph_name=extra.get("graph_name"),
        interrupt_id=extra.get("interrupt_id"),
        checkpoint_id=extra.get("checkpoint_id"),
        error_class=extra.get("error_class"),
        untrusted_quote_present=bool(extra.get("untrusted_quote_present")),
        notes=extra.get("notes"),
    )


def events_for(correlation_id: str) -> list[dict[str, Any]]:
    return read_trace(correlation_id)


def reset_events() -> None:
    reset_audit_store()
