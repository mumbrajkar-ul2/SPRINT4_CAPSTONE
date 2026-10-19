"""HTTP pause and resume for the Application B checkpoint."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_b.agent.pause import resume_pause, start_pause
from apps.shared.identity import HEADER_ACTOR_ID, HEADER_CORRELATION, header_get

router = APIRouter()


@router.post("/api/agent/pause")
def post_pause(request: Request, payload: dict) -> JSONResponse:
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or str(payload.get("correlation_id") or "")
    case_id = str(payload.get("case_id") or "PS000000016")
    if not correlation_id:
        return JSONResponse({"ok": False, "message": "A correlation id is required."}, status_code=400)
    body = start_pause(correlation_id, case_id)
    return JSONResponse(body)


@router.post("/api/agent/resume")
def post_resume(request: Request, payload: dict) -> JSONResponse:
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or str(payload.get("correlation_id") or "")
    actor_id = header_get(request.headers, HEADER_ACTOR_ID) or str(payload.get("actor_id") or "")
    body = resume_pause(correlation_id, actor_id)
    status = 403 if body.get("ok") is False else 200
    return JSONResponse(body, status_code=status)
