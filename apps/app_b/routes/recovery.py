"""GET /api/recovery. Gateway failure mapping. Recovery GET stays 200."""
from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_b.events import record_event
from apps.app_b.intelligence.generate import generate
from apps.app_b.store import get_case
from apps.shared.identity import HEADER_ACTOR_ID, HEADER_ACTOR_ROLE, HEADER_CORRELATION, header_get

router = APIRouter()

_LAST: dict[str, Any] = {
    "status_visible": "No upstream probe has run in this process yet.",
    "error_class": "none",
    "retry_shown": False,
    "owner_id": None,
}

MODE_MAP = {
    "timeout": ("upstream_timeout", "timeout", 503),
    "schema": ("upstream_schema", "schema", 503),
    "rate_limit": ("upstream_rate_limit", "rate_limit", 503),
    "normal": ("none", "none", 200),
}


def source_url() -> str | None:
    value = (os.environ.get("SOURCE_GATEWAY_URL") or "").strip()
    return value or None


def _simulate(mode: str) -> dict[str, Any]:
    if mode == "timeout":
        return {"http_status": 503, "body": {"error": "upstream unavailable", "retryable": True}}
    if mode == "schema":
        return {"http_status": 200, "body": {"unexpected_schema": "v3", "records": None}}
    if mode == "rate_limit":
        return {"http_status": 429, "body": {"error": "source throttle", "retryable": True}}
    return {"http_status": 200, "body": {"mode": "normal"}}


def probe_gateway(mode: str) -> dict[str, Any]:
    base = source_url()
    if not base:
        return _simulate(mode)
    url = f"{base.rstrip('/')}/api/failure?mode={mode}"
    try:
        req = Request(url)
        with urlopen(req, timeout=3) as response:
            body = json.loads(response.read().decode("utf-8"))
            return {"http_status": response.status, "body": body}
    except HTTPError as exc:
        raw = exc.read().decode("utf-8") if exc.fp else "{}"
        try:
            body = json.loads(raw) if raw else {"error": str(exc)}
        except json.JSONDecodeError:
            body = {"error": raw}
        return {"http_status": exc.code, "body": body}
    except (URLError, TimeoutError, json.JSONDecodeError):
        return {"http_status": 503, "body": {"error": "upstream unavailable", "retryable": True}}


def apply_probe(mode: str) -> dict[str, Any]:
    mapped = MODE_MAP.get(mode, MODE_MAP["timeout"])
    error_class_full, error_class, fail_status = mapped
    raw = probe_gateway(mode)
    if mode == "schema":
        visible = "Upstream schema did not match. Retry is visible. No 8-hour target is claimed."
        status_for_user = fail_status
    elif mode == "timeout":
        visible = "Upstream timed out. Retry is visible. Numeric RTO stays Unknown."
        status_for_user = fail_status
    elif mode == "rate_limit":
        visible = "Upstream returned a throttle. Retry is visible."
        status_for_user = fail_status
    else:
        visible = "Upstream probe returned normal."
        status_for_user = 200
        error_class_full = "none"
        error_class = "none"
    _LAST.update(
        {
            "status_visible": visible,
            "error_class": error_class,
            "error_class_full": error_class_full,
            "retry_shown": error_class != "none",
            "owner_id": None,
            "upstream_http_status": raw.get("http_status"),
            "upstream_body": raw.get("body"),
            "probe_http_status": status_for_user,
        }
    )
    return dict(_LAST)


@router.get("/api/recovery")
def get_recovery(request: Request, mode: str | None = None) -> dict[str, object]:
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or None
    actor_id = header_get(request.headers, HEADER_ACTOR_ID)
    actor_role = header_get(request.headers, HEADER_ACTOR_ROLE)
    state = dict(_LAST)
    if mode in MODE_MAP:
        state = apply_probe(mode)
        record_event(
            "EV-11",
            correlation_id=correlation_id,
            actor_id=actor_id,
            actor_role=actor_role,
            case_id="INC-2025-014",
            lake_item_ids=["term.outage", "decision.inc_2025_014"],
            extra={"error_class": state.get("error_class")},
        )
    case = get_case("INC-2025-014") or {}
    cited = generate(
        "What user-visible recovery status should Application B show for an outage?",
        prompt_id="P-NL-QUERY",
        case_id="INC-2025-014",
        hint_item_ids=["term.outage", "decision.inc_2025_014"],
    )
    return {
        "ok": True,
        "status_visible": state.get("status_visible"),
        "error_class": state.get("error_class"),
        "retry_shown": state.get("retry_shown"),
        "owner_id": case.get("owner_id"),
        "sentence": cited.get("sentence"),
        "citations": cited.get("citations"),
        "verdict": cited.get("verdict"),
        "correlation_id": correlation_id,
    }


@router.get("/api/recovery/probe")
def probe(request: Request, mode: str = "timeout") -> JSONResponse:
    state = apply_probe(mode)
    record_event(
        "EV-11",
        correlation_id=header_get(request.headers, HEADER_CORRELATION) or None,
        actor_id=header_get(request.headers, HEADER_ACTOR_ID),
        actor_role=header_get(request.headers, HEADER_ACTOR_ROLE),
        case_id="INC-2025-014",
        lake_item_ids=["term.outage"],
        extra={"error_class": state.get("error_class")},
    )
    status = int(state.get("probe_http_status") or 503)
    body = {
        "ok": status == 200,
        "error_class": state.get("error_class_full") if status != 200 else None,
        "status_visible": state.get("status_visible"),
        "retry_shown": state.get("retry_shown"),
        "owner_id": None,
    }
    return JSONResponse(body, status_code=status)
