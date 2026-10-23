"""POST /api/approvals. Person only. The model has no write tool."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_a.agent.graph import resume_agent
from apps.app_a.agent.waiting import find_waiting_thread
from apps.app_a.audit.store import audit_path
from apps.app_a.events import record_event
from apps.app_a.store import get_case, is_blocked, record_approval
from apps.shared.oidc_session import approval_gate, store_signature
from apps.shared.identity import (
    HEADER_ACTOR_ID,
    HEADER_ACTOR_ROLE,
    HEADER_CORRELATION,
    check_write_action,
    error_body,
    header_get,
)

router = APIRouter()


@router.post("/api/approvals")
def post_approval(request: Request, payload: dict) -> JSONResponse:
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or None
    actor_id = header_get(request.headers, HEADER_ACTOR_ID)
    actor_role = header_get(request.headers, HEADER_ACTOR_ROLE)
    action_type = str(payload.get("action_type") or "")
    proposed_by = str(payload.get("proposed_by") or "")
    case_id = str(payload.get("case_id") or "")
    if actor_role.lower().startswith("model") or actor_id.lower().startswith("model"):
        return JSONResponse(check_write_action(
            role="model",
            action_type=action_type,
            actor_id=actor_id,
            proposed_by=proposed_by,
            correlation_id=correlation_id,
        ), status_code=403)

    denied = check_write_action(
        role=actor_role,
        action_type=action_type,
        actor_id=actor_id,
        proposed_by=proposed_by,
        correlation_id=correlation_id,
    )
    if denied:
        return JSONResponse(denied, status_code=403)
    gated = approval_gate(request, payload, correlation_id)
    if gated is not None:
        return gated

    case = get_case(case_id)
    if case is None:
        return JSONResponse(
            error_body("not_found", "No Application A case has that id.", correlation_id=correlation_id),
            status_code=404,
        )
    if is_blocked(case_id) or case.get("blocked"):
        record_event(
            "EV-12",
            correlation_id=correlation_id,
            actor_id=actor_id,
            actor_role=actor_role,
            case_id=case_id,
            lake_item_ids=["rule.untrusted_text.block"],
        )
        body = error_body("blocked", "This write is blocked. Untrusted text is not an approval.", correlation_id=correlation_id, lake_item_ids=["rule.untrusted_text.block"])
        body["untrusted_quotes"] = case.get("untrusted_quotes") or []
        return JSONResponse(body, status_code=409)

    if action_type == "assign_owner" and not payload.get("owner_id"):
        return JSONResponse(
            error_body(
                "wait_for_person",
                "assign_owner needs a person-supplied owner_id. Application A does not invent a name.",
                correlation_id=correlation_id,
                lake_item_ids=["decision.inc_2025_014"],
            ),
            status_code=409,
        )

    recorded = {
        "case_id": case_id,
        "action_type": action_type,
        "decision": payload.get("decision"),
        "actor_id": actor_id,
        "actor_role": actor_role,
        "proposed_by": proposed_by,
        "correlation_id": correlation_id,
        "owner_id": payload.get("owner_id"),
        "policy_id": payload.get("policy_id"),
        "hold_value": payload.get("hold_value") or payload.get("decision"),
    }
    waiting = find_waiting_thread(case_id, correlation_id)
    if waiting:
        thread_id = waiting["thread_id"]
        resume_agent(
            thread_id,
            {
                "decision": payload.get("decision"),
                "action_type": action_type,
                "actor_id": actor_id,
                "actor_role": actor_role,
                "proposed_by": proposed_by,
                "owner_id": payload.get("owner_id"),
                "policy_id": payload.get("policy_id"),
                "hold_value": payload.get("hold_value") or payload.get("decision"),
            },
        )
        updated = get_case(case_id) or {}
        store_signature(audit_path(), request, payload, correlation_id)
        return JSONResponse({"ok": True, "approval": recorded, "case": updated, "resumed": True, "correlation_id": thread_id})
    updated = record_approval(case_id, recorded)
    event_type = "EV-10" if action_type == "assign_owner" else "EV-09"
    record_event(
        event_type,
        correlation_id=correlation_id,
        actor_id=actor_id,
        actor_role=actor_role,
        case_id=case_id,
        lake_item_ids=list(case.get("citation_targets") or []),
        extra={"action_type": action_type, "decision": payload.get("decision")},
    )
    store_signature(audit_path(), request, payload, correlation_id)
    return JSONResponse({"ok": True, "approval": recorded, "case": updated})
