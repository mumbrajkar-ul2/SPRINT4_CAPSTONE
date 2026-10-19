"""Lake MCP listener on host port 8092. HTTP ready check plus four read tools."""
from __future__ import annotations

import sys
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "context-lake") not in sys.path:
    sys.path.insert(0, str(ROOT / "context-lake"))

from apps.shared.identity import (  # noqa: E402
    HEADER_CORRELATION,
    check_lake_key,
    header_get,
    identity_reject,
    lake_write_rejected,
)
from apps.shared.jsonlog import emit  # noqa: E402
from lake_runtime import get_item, get_links, rule_at, search_items  # noqa: E402

SERVICE = "lake-mcp"
READ_TOOLS = ("search_items", "get_item", "get_links", "rule_at")

app = FastAPI(title=SERVICE, docs_url=None, redoc_url=None)


def _correlation(request: Request) -> str | None:
    return header_get(request.headers, HEADER_CORRELATION) or None


@app.middleware("http")
async def key_and_logs(request: Request, call_next):
    started = time.perf_counter()
    path = request.url.path
    correlation_id = _correlation(request)
    if path != "/health":
        error = check_lake_key(request.headers)
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
        if request.method.upper() in {"PUT", "PATCH", "DELETE"}:
            duration_ms = round((time.perf_counter() - started) * 1000, 3)
            emit(
                service=SERVICE,
                event="lake_write_rejected",
                level="warn",
                correlation_id=correlation_id,
                path=path,
                status=405,
                duration_ms=duration_ms,
            )
            return JSONResponse(lake_write_rejected(correlation_id), status_code=405)
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started) * 1000, 3)
    event = "health_ok" if path == "/health" else "request_ok"
    emit(
        service=SERVICE,
        event=event,
        level="info",
        correlation_id=correlation_id,
        path=path,
        status=response.status_code,
        duration_ms=duration_ms,
    )
    return response


@app.get("/health")
def health() -> dict[str, object]:
    return {"ok": True, "tools": list(READ_TOOLS)}


@app.get("/v1/tools")
def list_tools() -> dict[str, object]:
    return {
        "ok": True,
        "tools": [
            {"name": "search_items", "write": False},
            {"name": "get_item", "write": False},
            {"name": "get_links", "write": False},
            {"name": "rule_at", "write": False},
        ],
    }


@app.post("/v1/tools/{tool_name}")
def call_tool(tool_name: str, payload: dict | None = None):
    body = payload or {}
    if tool_name not in READ_TOOLS:
        return JSONResponse(lake_write_rejected(), status_code=405)
    if tool_name == "search_items":
        return search_items(
            str(body.get("query", "")),
            kind=body.get("kind"),
            limit=int(body.get("limit", 20)),
        )
    if tool_name == "get_item":
        return get_item(str(body.get("id", "")))
    if tool_name == "get_links":
        types = [body["type"]] if body.get("type") else None
        return get_links(
            str(body.get("id", "")),
            types=types,
            depth=int(body.get("depth", 6)),
        )
    return rule_at(
        str(body.get("rule_id", "")),
        str(body.get("on_date", "")),
        site_code=body.get("site_code"),
        country_code=body.get("country_code"),
        sales_region=body.get("sales_region"),
    )
