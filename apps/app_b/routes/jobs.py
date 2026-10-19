"""Three read-only jobs. Each one writes one audit row and waits for a person."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_b.audit.writer import append_row
from apps.shared.identity import HEADER_ACTOR_ID, HEADER_ACTOR_ROLE, HEADER_CORRELATION, header_get

router = APIRouter()

JOBS = {
    "change-impact": {
        "tools": ["search_items", "get_links"],
        "waiting_role": "RT-03",
    },
    "evidence-pack": {
        "tools": ["get_item", "get_case"],
        "waiting_role": "RT-01",
    },
    "operational-handoff": {
        "tools": ["get_case", "get_recovery_status"],
        "waiting_role": "RT-06",
    },
}


@router.post("/api/agent/jobs/{job_name}")
def post_job(job_name: str, request: Request) -> JSONResponse:
    spec = JOBS.get(job_name)
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or f"corr-p18-job-{job_name}"
    if spec is None:
        return JSONResponse({"ok": False, "message": "Unknown job."}, status_code=404)
    row = append_row(
        correlation_id=correlation_id,
        row_kind="agent_step",
        event_type="EV-08",
        actor_id=header_get(request.headers, HEADER_ACTOR_ID),
        actor_role=header_get(request.headers, HEADER_ACTOR_ROLE),
        step_name=job_name,
        tool_name=spec["tools"][0],
        opa_verdict="HOLD_FOR_REVIEW",
        proposed_by="model_draft",
        graph_name="app_b_readonly_job",
        notes="Read-only job. The model has no write tool.",
    )
    return JSONResponse(
        {
            "ok": True,
            "job_name": job_name,
            "tools": spec["tools"],
            "waiting_role": spec["waiting_role"],
            "write_tools": [],
            "audit_id": row["audit_id"],
            "correlation_id": correlation_id,
            "opa_verdict": "HOLD_FOR_REVIEW",
        }
    )
