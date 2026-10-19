"""Health and identity probe used by Application A and Application B."""
from __future__ import annotations

import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from apps.shared.identity import (
    HEADER_ACTOR_ID,
    HEADER_CORRELATION,
    check_app_identity,
    header_get,
)
from apps.shared.jsonlog import emit


def create_app(service: str) -> FastAPI:
    app = FastAPI(title=service, docs_url=None, redoc_url=None)

    @app.middleware("http")
    async def identity_and_logs(request: Request, call_next):
        started = time.perf_counter()
        path = request.url.path
        correlation_id = header_get(request.headers, HEADER_CORRELATION) or None
        actor_id = header_get(request.headers, HEADER_ACTOR_ID) or None
        if path != "/health":
            error = check_app_identity(request.headers)
            if error:
                duration_ms = round((time.perf_counter() - started) * 1000, 3)
                emit(
                    service=service,
                    event="identity_missing",
                    level="warn",
                    correlation_id=correlation_id,
                    path=path,
                    status=401,
                    duration_ms=duration_ms,
                )
                return JSONResponse(error, status_code=401)
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started) * 1000, 3)
        event = "health_ok" if path == "/health" else "request_ok"
        emit(
            service=service,
            event=event,
            level="info",
            correlation_id=correlation_id,
            actor_id=actor_id if path != "/health" else None,
            path=path,
            status=response.status_code,
            duration_ms=duration_ms,
        )
        return response

    @app.get("/health")
    def health() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/api/identity-check")
    def identity_check(request: Request) -> dict[str, object]:
        return {
            "ok": True,
            "actor_id": header_get(request.headers, HEADER_ACTOR_ID),
            "actor_role": header_get(request.headers, "X-Actor-Role"),
        }

    return app
