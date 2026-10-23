"""POST /api/agent/run starts graph app_a_investigate."""
from __future__ import annotations

import os

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_a.agent.graph import run_agent
from apps.app_a.events import mint_correlation_id
from apps.app_a.store import get_case
from apps.shared.source_badge import source_badge
from apps.shared.identity import (
    HEADER_ACTOR_ID,
    HEADER_ACTOR_ROLE,
    HEADER_CORRELATION,
    error_body,
    header_get,
)

router = APIRouter()

os.environ.setdefault("MODEL_MODE", "replay")


@router.post("/api/agent/run")
def post_agent_run(request: Request, payload: dict) -> JSONResponse:
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or mint_correlation_id()
    actor_id = header_get(request.headers, HEADER_ACTOR_ID)
    actor_role = header_get(request.headers, HEADER_ACTOR_ROLE)
    case_id = str(payload.get("case_id") or "")
    scenario = str(payload.get("scenario") or payload.get("corpus_id") or "")
    if not case_id and not scenario:
        return JSONResponse(
            error_body("not_found", "POST /api/agent/run needs a case_id.", correlation_id=correlation_id),
            status_code=404,
        )
    if case_id and get_case(case_id) is None and not scenario.startswith("IC-"):
        return JSONResponse(
            error_body("not_found", "No Application A case has that id.", correlation_id=correlation_id),
            status_code=404,
        )
    result = run_agent(
        {
            "correlation_id": correlation_id,
            "thread_id": correlation_id,
            "case_id": case_id,
            "actor_id": actor_id,
            "actor_role": actor_role,
            "scenario": scenario,
            "proposed_action": str(payload.get("proposed_action") or ""),
            "step_count": 0,
            "tool_call_count": 0,
            "gather_visits": 0,
            "budget_exhausted": False,
            "citations": [],
            "untrusted_quotes": [],
            "lake_item_ids": [],
            "draft_plan": "",
            "sentence": "",
            "verdict": "",
            "opa_verdict": "",
            "block": False,
            "record_change": False,
            "waiting_role": "",
            "proposed_by": "model_draft",
            "human_decision": "",
            "human_action_type": "",
            "human_actor_id": "",
            "human_actor_role": "",
            "error_class": "",
        }
    )
    state = result.get("state") or {}
    if state.get("error_class") == "not_found":
        return JSONResponse(
            error_body("not_found", "No Application A case has that id.", correlation_id=correlation_id),
            status_code=404,
        )
    if result.get("error_class") == "wait_for_person":
        return JSONResponse(
            {
                "ok": False,
                "error_class": "wait_for_person",
                "correlation_id": correlation_id,
                "opa_verdict": "HOLD_FOR_REVIEW",
                "waiting": False,
                "sentence": state.get("sentence") or "",
                "draft_plan": state.get("draft_plan") or "",
                "citations": state.get("citations") or [],
                "retrieved_item_ids": state.get("retrieved_item_ids") or [],
                "model_mode": state.get("model_mode") or "",
                "answer_source": state.get("answer_source") or "",
                "model": state.get("model") or "",
                "source_badge": state.get("source_badge")
                or source_badge(app_code="a", answer_source=state.get("answer_source") or "", model_name=state.get("model") or ""),
                "replay_save": state.get("replay_save") or None,
                "message": state.get("message") or None,
                "proposed_by": state.get("proposed_by") or "model_draft",
            },
            status_code=409,
        )
    case = get_case(case_id) if case_id else None
    status = 409 if state.get("opa_verdict") == "BLOCK" else 200
    body = {
        "ok": state.get("opa_verdict") != "BLOCK",
        "correlation_id": correlation_id,
        "thread_id": correlation_id,
        "graph_name": "app_a_investigate",
        "opa_verdict": state.get("opa_verdict"),
        "waiting": bool(result.get("waiting")),
        "waiting_role": state.get("waiting_role"),
        "draft_plan": state.get("draft_plan"),
        "citations": state.get("citations") or [],
        "verdict": state.get("verdict"),
        "sentence": state.get("sentence") or "",
        "block": bool(state.get("block")),
        "error_class": state.get("error_class") or None,
        "model_mode": state.get("model_mode") or "",
        "answer_source": state.get("answer_source") or "",
        "model": state.get("model") or "",
        "source_badge": state.get("source_badge")
        or source_badge(
            app_code="a",
            answer_source=state.get("answer_source") or "",
            model_name=state.get("model") or "",
            block=bool(state.get("block")),
            error_class=state.get("error_class"),
        ),
        "retrieved_item_ids": state.get("retrieved_item_ids") or [],
        "replay_save": state.get("replay_save") or None,
        "message": state.get("message") or None,
        "proposed_by": state.get("proposed_by") or "model_draft",
        "case": case,
    }
    if state.get("opa_verdict") == "BLOCK":
        body["error_class"] = "blocked"
        body["ok"] = False
    return JSONResponse(body, status_code=status)
