"""GET /api/recovery. Gateway failure mapping. Recovery GET stays 200. Probe may return 503."""
from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request as UrlRequest, urlopen

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from apps.app_a.events import record_event
from apps.app_a.intelligence.generate import generate
from apps.app_a.rules.adapter import intake_apply
from apps.app_a.runtime.dlq import (
    emit_replayed,
    get_parked,
    list_parked_intakes,
    mark_replayed,
    replace_payload,
)
from apps.shared.identity import HEADER_ACTOR_ID, HEADER_ACTOR_ROLE, HEADER_CORRELATION, header_get

router = APIRouter()

# One extra source-gateway probe after timeout or throttle. Not a quality floor.
UPSTREAM_RETRY_COUNT = 1
_RETRYABLE_MODES = frozenset({"timeout", "rate_limit"})

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
    """Call 8090 when SOURCE_GATEWAY_URL is set. Otherwise replay the same fixture shapes locally."""
    base = source_url()
    if not base:
        return _simulate(mode)
    url = f"{base.rstrip('/')}/api/failure?mode={mode}"
    try:
        req = UrlRequest(url)
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


class DlqReplayBody(BaseModel):
    parked_id: str
    payload: dict[str, Any] | None = Field(default=None)


def apply_probe(mode: str) -> dict[str, Any]:
    mapped = MODE_MAP.get(mode, MODE_MAP["timeout"])
    error_class_full, error_class, fail_status = mapped
    raw = probe_gateway(mode)
    attempt_count = 1
    first_error_class = error_class_full if mode != "normal" else "none"
    if mode in _RETRYABLE_MODES:
        extra = max(0, int(UPSTREAM_RETRY_COUNT))
        for _ in range(extra):
            raw = probe_gateway(mode)
            attempt_count += 1
    if mode == "schema":
        # Gateway may return HTTP 200 with an unexpected body. Schema is not retried.
        visible = f"Upstream schema did not match. Attempt count is {attempt_count}. This probe is not retried."
        status_for_user = fail_status
    elif mode == "timeout":
        visible = f"Upstream timed out. Attempt count is {attempt_count}. The probe target is port 8090."
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
            "attempt_count": attempt_count,
            "first_error_class": first_error_class,
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
            lake_item_ids=["term.outage", "arch.listener.gateway_8090"],
            extra={"error_class": state.get("error_class")},
        )
    cited = generate(
        "What user-visible recovery status should Application A show for an outage?",
        prompt_id="P-NL-QUERY",
        case_id="INC-2025-014",
        hint_item_ids=["term.outage", "decision.inc_2025_014"],
    )
    return {
        "ok": True,
        "status_visible": state.get("status_visible"),
        "error_class": state.get("error_class"),
        "retry_shown": state.get("retry_shown"),
        "owner_id": None,
        "sentence": cited.get("sentence"),
        "citations": cited.get("citations"),
        "verdict": cited.get("verdict"),
        "correlation_id": correlation_id,
        "parked_intakes": list_parked_intakes(),
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
        "attempt_count": state.get("attempt_count"),
        "first_error_class": state.get("first_error_class") if status != 200 else None,
    }
    return JSONResponse(body, status_code=status)


@router.post("/api/recovery/dlq/replay")
def replay_parked_intake(request: Request, body: DlqReplayBody) -> JSONResponse:
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or None
    row = get_parked(body.parked_id)
    if row is None:
        return JSONResponse(
            {
                "ok": False,
                "error_class": "not_found",
                "message": "That parked intake is not in the dead-letter file.",
                "parked_id": body.parked_id,
                "parked_intakes": list_parked_intakes(),
            },
            status_code=404,
        )
    payload = body.payload if body.payload is not None else row["payload"]
    if body.payload is not None:
        replaced = replace_payload(body.parked_id, payload)
        if replaced is not None:
            row = replaced
    result = intake_apply([payload])
    if result["accepted"] >= 1 or result["duplicates"] >= 1:
        updated = mark_replayed(body.parked_id)
        if updated is not None:
            row = updated
    else:
        row = get_parked(body.parked_id) or row
    emit_replayed(
        row,
        correlation_id=correlation_id,
        accepted=int(result["accepted"]),
        invalid=int(result["invalid"]),
        duplicates=int(result["duplicates"]),
    )
    record_event(
        "EV-11",
        correlation_id=correlation_id,
        actor_id=header_get(request.headers, HEADER_ACTOR_ID),
        actor_role=header_get(request.headers, HEADER_ACTOR_ROLE),
        case_id="INC-2025-014",
        lake_item_ids=["term.outage"],
        extra={"error_class": "invalid" if result["invalid"] else "none", "step_name": "dlq_replay"},
    )
    return JSONResponse(
        {
            "ok": True,
            "parked_id": row["parked_id"],
            "message_id": row["message_id"],
            "status": row["status"],
            "accepted": result["accepted"],
            "invalid": result["invalid"],
            "duplicates": result["duplicates"],
            "received": result["received"],
            "parked_intakes": list_parked_intakes(),
            "correlation_id": correlation_id,
        }
    )
