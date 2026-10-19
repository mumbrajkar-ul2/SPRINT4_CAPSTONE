"""GET /api/cases/{id}. SCH-06 body. Optional cited explanation from the lake."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_b.events import record_event
from apps.app_b.intelligence.generate import generate
from apps.app_b.store import get_case
from apps.shared.identity import HEADER_ACTOR_ID, HEADER_ACTOR_ROLE, HEADER_CORRELATION, header_get
from apps.shared.identity import error_body

router = APIRouter()

SCENARIO_EVENTS = {
    "SP-07": "EV-02",
    "SP-08": "EV-04",
    "SP-09": "EV-05",
    "SP-10": "EV-06",
    "SP-11": "EV-11",
}


@router.get("/api/cases/{case_id}")
def get_case_route(case_id: str, request: Request, explain: bool = True) -> JSONResponse:
    body = get_case(case_id)
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or None
    if body is None:
        return JSONResponse(
            error_body(
                "not_found",
                "No Application B case has that id.",
                correlation_id=correlation_id,
            ),
            status_code=404,
        )
    actor_id = header_get(request.headers, HEADER_ACTOR_ID)
    actor_role = header_get(request.headers, HEADER_ACTOR_ROLE)
    event_type = SCENARIO_EVENTS.get(body.get("scenario") or "")
    if event_type:
        record_event(
            event_type,
            correlation_id=correlation_id,
            actor_id=actor_id,
            actor_role=actor_role,
            case_id=case_id,
            lake_item_ids=list(body.get("citation_targets") or []),
        )
    explanation = None
    if explain:
        question = body.get("explain_question") or f"Explain case {case_id}."
        explanation = generate(
            question,
            prompt_id="P-EXPLAIN-CONFLICT",
            case_id=case_id,
            hint_item_ids=list(body.get("citation_targets") or []),
        )
        body = dict(body)
        body["sentence"] = explanation.get("sentence")
        body["citations"] = explanation.get("citations")
        body["verdict"] = explanation.get("verdict")
        body["block"] = explanation.get("block")
        if explanation.get("untrusted_quotes"):
            body["untrusted_quotes"] = explanation.get("untrusted_quotes")
        if explanation.get("draft_plan"):
            body["draft_plan"] = explanation.get("draft_plan")
        if explanation.get("error_class"):
            body["error_class"] = explanation.get("error_class")
    return JSONResponse({"ok": True, "case": body, "explanation": explanation})
