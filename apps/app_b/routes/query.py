"""POST /api/query. Retrieve from the lake. FD-14 cite or abstain."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_b.intelligence.generate import generate
from apps.app_b.store import get_case, mark_blocked, set_draft
from apps.shared.identity import HEADER_CORRELATION, header_get

router = APIRouter()

JOB_PROMPTS = {
    "query": "P-NL-QUERY",
    "explain": "P-EXPLAIN-CONFLICT",
    "draft": "P-DRAFT-PLAN",
}


@router.post("/api/query")
def post_query(request: Request, payload: dict) -> JSONResponse:
    question = str(payload.get("question") or "")
    case_id = payload.get("case_id") or ""
    job = str(payload.get("job") or "query")
    prompt_id = JOB_PROMPTS.get(job, "P-NL-QUERY")
    hints: list[str] = []
    if case_id:
        case = get_case(str(case_id))
        if case:
            hints = list(case.get("citation_targets") or [])
    result = generate(question, prompt_id=prompt_id, case_id=str(case_id) if case_id else None, hint_item_ids=hints)
    if result.get("block") and case_id:
        mark_blocked(str(case_id))
    if prompt_id == "P-DRAFT-PLAN" and result.get("draft_plan") and case_id:
        set_draft(str(case_id), str(result["draft_plan"]))
    body = {
        "sentence": result.get("sentence") or "",
        "citations": result.get("citations") or [],
        "verdict": result.get("verdict") or "ABSTAIN",
        "block": bool(result.get("block")),
        "untrusted_quotes": result.get("untrusted_quotes") or [],
        "prompt_id": result.get("prompt_id"),
        "semver": result.get("semver"),
        "prompt_hash": result.get("prompt_hash"),
        "retrieved_item_ids": result.get("retrieved_item_ids") or [],
        "error_class": result.get("error_class"),
        "lake_version": result.get("lake_version"),
        "grounded": result.get("grounded"),
        "reject_reason": result.get("reject_reason"),
        "correlation_id": header_get(request.headers, HEADER_CORRELATION) or None,
    }
    if prompt_id == "P-DRAFT-PLAN":
        body["draft_plan"] = result.get("draft_plan")
    return JSONResponse(body)
