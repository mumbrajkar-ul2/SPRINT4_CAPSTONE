"""Demo session routes. Each app passes its own queue count and recovery probe."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.shared.demo_session import DemoSession
from apps.shared.identity import HEADER_ACTOR_ID, HEADER_ACTOR_ROLE, HEADER_CORRELATION, header_get
from apps.shared.jsonlog import emit

Probe = Callable[[str], dict[str, Any]]


def build_demo_router(
    *,
    app_name: str,
    service: str,
    lineage: bool,
    session: DemoSession,
    base_queue: Callable[[], int],
    probe: Probe,
) -> APIRouter:
    router = APIRouter()

    def _actor(request: Request) -> tuple[str, str, str | None]:
        return (
            header_get(request.headers, HEADER_ACTOR_ID),
            header_get(request.headers, HEADER_ACTOR_ROLE),
            header_get(request.headers, HEADER_CORRELATION) or None,
        )

    def _body(request: Request) -> dict[str, Any]:
        actor_id, actor_role, correlation_id = _actor(request)
        session.correlation_id = correlation_id
        payload = session.snapshot(base_queue=base_queue(), app_name=app_name, lineage=lineage)
        payload["actor_id"] = actor_id
        payload["actor_role"] = actor_role
        emit(
            service=service,
            event="demo_session",
            correlation_id=correlation_id,
            actor_id=actor_id,
            path=str(request.url.path),
            status=200,
        )
        return payload

    @router.get("/api/demo/state")
    def demo_state(request: Request) -> dict[str, Any]:
        return _body(request)

    @router.post("/api/demo/reset")
    def demo_reset(request: Request) -> dict[str, Any]:
        session.reset()
        return _body(request)

    @router.post("/api/demo/replay/receive")
    def demo_receive(request: Request) -> dict[str, Any]:
        session.receive_replay()
        return _body(request)

    @router.post("/api/demo/replay/drop")
    def demo_drop(request: Request) -> JSONResponse:
        _actor_id, actor_role, _correlation = _actor(request)
        error = session.confirm_drop(actor_role=actor_role)
        payload = _body(request)
        if error:
            payload["ok"] = False
            payload["message"] = error
            return JSONResponse(payload, status_code=403)
        return JSONResponse(payload)

    @router.post("/api/demo/clocks/apply")
    def demo_clocks(request: Request) -> dict[str, Any]:
        session.apply_backfill()
        return _body(request)

    @router.post("/api/demo/policy/check")
    def demo_policy(request: Request) -> dict[str, Any]:
        session.check_policy()
        return _body(request)

    @router.post("/api/demo/policy/decide")
    def demo_policy_decide(request: Request, payload: dict) -> JSONResponse:
        _actor_id, actor_role, _correlation = _actor(request)
        choice = str(payload.get("choice") or "keep-wait")
        error = session.decide_policy(choice, actor_role=actor_role)
        body = _body(request)
        if error:
            body["ok"] = False
            body["message"] = error
            return JSONResponse(body, status_code=403)
        return JSONResponse(body)

    @router.post("/api/demo/outage/probe")
    def demo_probe(request: Request, mode: str = "timeout") -> dict[str, Any]:
        state = probe(mode)
        attempt = int(state.get("attempt_count") or 1)
        if mode == "schema":
            sentence = f"Upstream schema did not match. Attempt count is {attempt}. This probe is not retried."
        elif mode == "timeout":
            sentence = f"Upstream timed out. Attempt count is {attempt}. The probe target is port 8090."
        else:
            sentence = str(state.get("status_visible") or "")
        session.last_probe = {
            "mode": mode,
            "attempt_count": attempt,
            "sentence": sentence,
            "status_visible": sentence,
            "error_class": state.get("error_class"),
        }
        body = _body(request)
        body["last_probe"] = session.last_probe
        return body

    @router.post("/api/demo/outage/park")
    def demo_park(request: Request) -> dict[str, Any]:
        session.park()
        return _body(request)

    @router.post("/api/demo/outage/replay")
    def demo_replay_parked(request: Request) -> dict[str, Any]:
        session.replay_parked()
        return _body(request)

    @router.post("/api/demo/owner")
    def demo_owner(request: Request, payload: dict) -> JSONResponse:
        _actor_id, actor_role, _correlation = _actor(request)
        if actor_role != "RT-06":
            body = _body(request)
            body["ok"] = False
            body["message"] = "The owner of INC-2025-014 stays empty unless RT-06 types one."
            return JSONResponse(body, status_code=403)
        typed = str(payload.get("owner_id") or "").strip()
        session.owner_typed = typed or None
        return JSONResponse(_body(request))

    @router.get("/api/demo/rule-trace")
    def demo_rule_trace(request: Request) -> JSONResponse:
        body = _body(request)
        if not lineage:
            body["ok"] = False
            body["message"] = "Application A has no lineage route."
            return JSONResponse(body, status_code=404)
        return JSONResponse(body)

    @router.post("/api/demo/gateway/receive")
    def demo_gateway(request: Request, payload: dict) -> dict[str, Any]:
        message_id = str(payload.get("message_id") or "")
        session.receive_gateway(message_id, payload)
        return _body(request)

    @router.post("/api/demo/gateway/pull")
    def demo_gateway_pull(request: Request) -> JSONResponse:
        import json
        import os
        from urllib.error import URLError
        from urllib.request import urlopen

        base = (os.environ.get("SOURCE_GATEWAY_URL") or "http://127.0.0.1:8090").rstrip("/")
        url = f"{base}/api/events?limit=1"
        try:
            with urlopen(url, timeout=3) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            body = _body(request)
            body["ok"] = False
            body["message"] = f"Port 8090 did not return a message. {exc}"
            return JSONResponse(body, status_code=503)
        items = list(payload.get("items") or [])
        if not items:
            body = _body(request)
            body["ok"] = False
            body["message"] = "The gateway returned no message."
            return JSONResponse(body, status_code=404)
        item = items[0]
        session.receive_gateway(str(item.get("message_id") or ""), item)
        return JSONResponse(_body(request))

    return router
