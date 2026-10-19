"""GET /api/audit/{correlation_id} returns the full trace in seq order."""
from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from apps.app_a.audit.reader import read_trace
from apps.shared.identity import error_body

router = APIRouter()


@router.get("/api/audit/{correlation_id}")
def get_audit(correlation_id: str) -> JSONResponse:
    if not correlation_id:
        return JSONResponse(
            error_body("not_found", "No audit rows have that correlation id."),
            status_code=404,
        )
    rows = read_trace(correlation_id)
    if not rows:
        return JSONResponse(
            error_body("not_found", "No audit rows have that correlation id.", correlation_id=correlation_id),
            status_code=404,
        )
    return JSONResponse({"ok": True, "correlation_id": correlation_id, "rows": rows})
