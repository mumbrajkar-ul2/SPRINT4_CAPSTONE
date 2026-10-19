"""Lake REST listener on host port 8091. Read only."""
from __future__ import annotations

import json
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

SERVICE = "lake-rest"
KINDS = {
    "business_rule",
    "domain_knowledge",
    "architecture",
    "code_intelligence",
    "data_relationship",
    "dependency",
    "decision",
}
LINK_TYPES = {
    "conflicts_with",
    "depends_on",
    "evidenced_by",
    "governs",
    "implements",
    "maps_to",
    "supersedes",
    "tested_by",
}
MANIFEST_PATH = Path(__file__).resolve().parent / "generated" / "manifest.json"

app = FastAPI(title=SERVICE, docs_url=None, redoc_url=None)


def _correlation(request: Request) -> str | None:
    return header_get(request.headers, HEADER_CORRELATION) or None


def _invalid(message: str, correlation_id: str | None) -> JSONResponse:
    return JSONResponse(
        {
            "ok": False,
            "error_class": "invalid_request",
            "message": message,
            "correlation_id": correlation_id,
            "waiting_role": None,
            "lake_item_ids": [],
        },
        status_code=400,
    )


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
        if request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
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
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/v1/version")
def version() -> dict[str, object]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {
        "ok": True,
        "lake_version": manifest["lake_version"],
        "sqlite_sha256": manifest["sqlite_sha256"],
        "item_count": manifest["item_count"],
    }


@app.get("/v1/items")
def items(request: Request, q: str = "", kind: str | None = None, limit: int = 20):
    correlation_id = _correlation(request)
    if kind and kind not in KINDS:
        return _invalid("kind must be one of the seven lake item kinds.", correlation_id)
    return search_items(q, kind=kind, limit=limit)


@app.get("/v1/items/{item_id}")
def one_item(item_id: str):
    env = get_item(item_id)
    if not env["items"] and env["verdict"] == "ABSTAIN":
        body = dict(env)
        body["ok"] = False
        body["error_class"] = "not_found"
        body["message"] = "No lake item has that id."
        body["correlation_id"] = None
        body["waiting_role"] = None
        body["lake_item_ids"] = []
        return JSONResponse(body, status_code=404)
    return env


@app.get("/v1/items/{item_id}/links")
def links(item_id: str, request: Request, type: str | None = None, depth: int = 6):
    correlation_id = _correlation(request)
    types = None
    if type:
        if type not in LINK_TYPES:
            return _invalid("type must be one of the eight lake link types.", correlation_id)
        types = [type]
    return get_links(item_id, types=types, depth=depth)


@app.get("/v1/rules/at")
def rules_at(
    request: Request,
    rule_id: str,
    on_date: str,
    site_code: str | None = None,
    country_code: str | None = None,
    sales_region: str | None = None,
):
    return rule_at(
        rule_id,
        on_date,
        site_code=site_code,
        country_code=country_code,
        sales_region=sales_region,
    )
