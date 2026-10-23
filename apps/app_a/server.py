"""Application A listener on host port 8100."""
from __future__ import annotations

import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from apps.app_a.audit.store import audit_path
from apps.app_a.intelligence.generate import generate as generate_answer
from apps.app_a.routes.agent import router as agent_router
from apps.app_a.routes.approvals import router as approvals_router
from apps.app_a.routes.audit import router as audit_router
from apps.app_a.routes.cases import router as cases_router
from apps.app_a.routes.query import router as query_router
from apps.app_a.routes.queue import router as queue_router
from apps.app_a.routes.recovery import apply_probe
from apps.app_a.routes.recovery import router as recovery_router
from apps.app_a.store import queue_items
from apps.shared.ask_route import build_ask_router
from apps.shared.demo_routes import build_demo_router
from apps.shared.feature_api import build_feature_router
from apps.shared.demo_session import DemoSession
from apps.shared.identity import (
    HEADER_ACTOR_ID,
    HEADER_CORRELATION,
    check_app_identity,
    check_closed_role,
    header_get,
    identity_reject,
)
from apps.shared.jsonlog import emit
from apps.shared.http_guard import app_origins, install_platform
from apps.shared.oidc_session import install_auth, prepare_request, refuse_unsafe_flags

SERVICE = "app-a"
UI_DIR = Path(__file__).resolve().parent / "ui"
DEMO_SESSION = DemoSession()
refuse_unsafe_flags()

app = FastAPI(title=SERVICE, docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _is_open_path(method: str, path: str) -> bool:
    if path in {"/health", "/healthz", "/readyz", "/metrics"} or path.startswith("/auth/"):
        return True
    if method.upper() != "GET":
        return False
    if path == "/" or path == "/index.html":
        return True
    if path.startswith("/assets/") or path.startswith("/ui/"):
        return True
    return False


@app.middleware("http")
async def identity_and_logs(request: Request, call_next):
    started = time.perf_counter()
    path = request.url.path
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or None
    actor_id = header_get(request.headers, HEADER_ACTOR_ID) or None
    if not _is_open_path(request.method, path):
        failure = prepare_request(request, audience="force-fab-app-a", app_code="a")
        if failure is not None:
            if failure.status_code == 401:
                duration_ms = round((time.perf_counter() - started) * 1000, 3)
                emit(
                    service=SERVICE,
                    event="identity_missing",
                    level="warn",
                    correlation_id=correlation_id,
                    path=path,
                    status=401,
                    duration_ms=duration_ms,
                )
            return failure
        actor_id = header_get(request.headers, HEADER_ACTOR_ID) or None
        error = check_app_identity(request.headers)
        if error:
            body, status, event = identity_reject(error)
            duration_ms = round((time.perf_counter() - started) * 1000, 3)
            emit(
                service=SERVICE,
                event=event,
                level="warn",
                correlation_id=correlation_id,
                path=path,
                status=status,
                duration_ms=duration_ms,
            )
            return JSONResponse(body, status_code=status)
        role_error = check_closed_role(request.headers)
        if role_error:
            duration_ms = round((time.perf_counter() - started) * 1000, 3)
            emit(
                service=SERVICE,
                event="forbidden_role",
                level="warn",
                correlation_id=correlation_id,
                actor_id=actor_id,
                path=path,
                status=403,
                duration_ms=duration_ms,
            )
            return JSONResponse(role_error, status_code=403)
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started) * 1000, 3)
    event = "health_ok" if path == "/health" else "request_ok"
    emit(
        service=SERVICE,
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


def _ui_index() -> Path:
    built = UI_DIR / "dist" / "index.html"
    if built.is_file():
        return built
    return UI_DIR / "index.html"


@app.get("/")
def index() -> FileResponse:
    return FileResponse(_ui_index())


install_auth(app, app_code="a", audience="force-fab-app-a", port=8100)
app.include_router(
    build_feature_router(
        app_code="a",
        queue_items=queue_items,
        audit_path=audit_path,
        lake_detail=False,
    )
)
app.include_router(build_ask_router(app_code="a", generate=generate_answer))
app.include_router(queue_router)
app.include_router(cases_router)
app.include_router(query_router)
app.include_router(recovery_router)
app.include_router(approvals_router)
app.include_router(audit_router)
app.include_router(agent_router)
app.include_router(
    build_demo_router(
        app_name="Application A",
        service=SERVICE,
        lineage=False,
        session=DEMO_SESSION,
        base_queue=lambda: len(queue_items()),
        probe=apply_probe,
    )
)

if UI_DIR.is_dir():
    built_assets = UI_DIR / "dist" / "assets"
    legacy_assets = UI_DIR / "assets"
    assets = built_assets if built_assets.is_dir() else legacy_assets
    if assets.is_dir():
        app.mount("/assets", StaticFiles(directory=assets), name="assets")

install_platform(app, service=SERVICE, app_code="a", db_path=audit_path())
