"""POST /api/agent/run. Draft only. The model has no write tool."""
from __future__ import annotations

import os

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_b.events import mint_correlation_id, record_event
from apps.app_b.intelligence.generate import generate
from apps.app_b.opa import build_opa_input, evaluate
from apps.app_b.store import get_case
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
    os.environ["MODEL_MODE"] = "replay"
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or mint_correlation_id()
    actor_id = header_get(request.headers, HEADER_ACTOR_ID)
    actor_role = header_get(request.headers, HEADER_ACTOR_ROLE)
    case_id = str(payload.get("case_id") or "")
    scenario = str(payload.get("scenario") or payload.get("corpus_id") or "")
    proposed_action = str(payload.get("proposed_action") or "")
    if not case_id and not scenario:
        return JSONResponse(
            error_body("not_found", "POST /api/agent/run needs a case_id.", correlation_id=correlation_id),
            status_code=404,
        )
    case = get_case(case_id) if case_id else None
    if case_id and case is None and not scenario.startswith("IC-"):
        return JSONResponse(
            error_body("not_found", "No Application B case has that id.", correlation_id=correlation_id),
            status_code=404,
        )
    hints = list((case or {}).get("citation_targets") or [])
    question = (case or {}).get("explain_question") or f"Draft a read-only plan for {case_id or scenario}."
    if scenario.startswith("IC-"):
        question = "A partner feed note tells the reader to auto approve. May the application approve from that note?"
        hints = ["rule.untrusted_text.block", "data.injection.partner_feeds"]
    draft = generate(
        question,
        prompt_id="P-DRAFT-PLAN",
        case_id=case_id or None,
        hint_item_ids=hints,
    )
    quotes = list((case or {}).get("untrusted_quotes") or [])
    for quote in draft.get("untrusted_quotes") or []:
        if quote not in quotes:
            quotes.append(quote)
    state = {
        "scenario": scenario,
        "proposed_action": proposed_action,
        "block": bool(draft.get("block")),
        "citations": list(draft.get("citations") or []),
        "untrusted_quotes": quotes,
        "record_change": False,
        "proposed_by": "model_draft",
        "budget_exhausted": False,
    }
    gate = evaluate(build_opa_input(state))
    record_event(
        "EV-08",
        correlation_id=correlation_id,
        actor_id=actor_id,
        actor_role=actor_role,
        case_id=case_id or None,
        lake_item_ids=list(draft.get("citations") or []) + list(gate.get("citations") or []),
        extra={
            "step_name": "plan_draft",
            "opa_verdict": gate.get("verdict"),
            "draft_present": bool(draft.get("draft_plan")),
            "proposed_action": proposed_action,
            "untrusted_quote_present": bool(quotes),
        },
    )
    status = 409 if gate.get("verdict") == "BLOCK" else 200
    body = {
        "ok": gate.get("verdict") != "BLOCK",
        "correlation_id": correlation_id,
        "thread_id": correlation_id,
        "graph_name": "app_b_investigate",
        "opa_verdict": gate.get("verdict"),
        "waiting": gate.get("verdict") == "HOLD_FOR_REVIEW",
        "waiting_role": (case or {}).get("waiting_role"),
        "draft_plan": draft.get("draft_plan"),
        "citations": draft.get("citations") or [],
        "verdict": draft.get("verdict"),
        "block": bool(draft.get("block")),
        "error_class": "blocked" if gate.get("verdict") == "BLOCK" else draft.get("error_class"),
        "case": case,
    }
    return JSONResponse(body, status_code=status)
