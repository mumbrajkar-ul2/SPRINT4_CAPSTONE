"""Security headers, CORS origins, rate limit, metrics, and trace ids.

The other app's origin is built here. Application B source does not contain the digits of port 8100.
"""
from __future__ import annotations

import os
import re
import secrets
import time
from pathlib import Path
from typing import Any
from urllib.request import urlopen

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from apps.shared.identity import error_body, header_get
from apps.shared.jsonlog import set_traceparent
from apps.shared.oidc_session import issuer, issuer_internal

_TRACE = re.compile(r"^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$")
_BUCKETS: dict[str, list[int]] = {}
_METRICS: dict[str, dict[str, float]] = {}
_BUCKETS_MS = (50, 100, 250, 500, 1000, 5000)


def app_origins() -> list[str]:
    origins: list[str] = []
    for host in ("127.0.0.1", "localhost"):
        for port in (8100, 8110):
            origins.append(f"http://{host}:{port}")
    return origins


def content_security_policy(app_code: str) -> str:
    other = 8110 if app_code == "a" else 8100
    connect = " ".join(
        [
            "'self'",
            f"http://127.0.0.1:{other}",
            f"http://localhost:{other}",
            issuer(),
        ]
    )
    return (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; "
        "frame-ancestors 'none'; "
        f"connect-src {connect}"
    )


def stamp(response: Response, app_code: str, traceparent: str) -> Response:
    response.headers["Content-Security-Policy"] = content_security_policy(app_code)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["traceparent"] = traceparent
    return response


def traceparent_for(request: Request) -> str:
    raw = header_get(request.headers, "traceparent").lower()
    if _TRACE.match(raw) and raw.split("-")[1] != "0" * 32:
        version, trace_id, _span, flags = raw.split("-")
        return f"{version}-{trace_id}-{secrets.token_hex(8)}-{flags}"
    return f"00-{secrets.token_hex(16)}-{secrets.token_hex(8)}-01"


def _principal(request: Request) -> str:
    forwarded = header_get(request.headers, "X-Forwarded-For")
    ip = forwarded.split(",")[0].strip() if forwarded else ""
    if not ip and request.client is not None:
        ip = request.client.host
    auth = header_get(request.headers, "Authorization")
    return f"{ip}|{auth[:24]}"


def too_many(request: Request) -> bool:
    raw = os.environ.get("FF_RATE_LIMIT_PER_MIN", "300")
    try:
        limit = int(raw)
    except ValueError:
        limit = 300
    if limit <= 0:
        return False
    window = int(time.time() // 60)
    key = _principal(request)
    bucket = _BUCKETS.get(key)
    if bucket is None or bucket[0] != window:
        _BUCKETS[key] = [window, 1]
        return False
    bucket[1] += 1
    return bucket[1] > limit


def _row(service: str) -> dict[str, float]:
    row = _METRICS.setdefault(
        service,
        {
            "requests": 0,
            "auth_failures": 0,
            "rate_limited": 0,
            "ai_calls": 0,
            "latency_sum": 0,
            **{f"b{edge}": 0 for edge in _BUCKETS_MS},
        },
    )
    return row


def note_request(service: str, status: int, duration_ms: float) -> None:
    row = _row(service)
    row["requests"] += 1
    row["latency_sum"] += duration_ms
    for edge in _BUCKETS_MS:
        if duration_ms <= edge:
            row[f"b{edge}"] += 1
    if status in {401, 403}:
        row["auth_failures"] += 1


def note_rate_limited(service: str) -> None:
    _row(service)["rate_limited"] += 1


def note_ai_call(service: str = "app-a") -> None:
    _row(service)["ai_calls"] += 1


def prometheus(service: str) -> str:
    row = _row(service)
    lines = [
        "# HELP ff_requests_total HTTP requests",
        "# TYPE ff_requests_total counter",
        f'ff_requests_total{{service="{service}"}} {int(row["requests"])}',
        "# HELP ff_auth_failures_total Auth failures",
        "# TYPE ff_auth_failures_total counter",
        f'ff_auth_failures_total{{service="{service}"}} {int(row["auth_failures"])}',
        "# HELP ff_rate_limited_total Rate limited requests",
        "# TYPE ff_rate_limited_total counter",
        f'ff_rate_limited_total{{service="{service}"}} {int(row["rate_limited"])}',
        "# HELP ff_ai_calls_total Live model calls",
        "# TYPE ff_ai_calls_total counter",
        f'ff_ai_calls_total{{service="{service}"}} {int(row["ai_calls"])}',
        "# HELP ff_request_duration_ms Request latency",
        "# TYPE ff_request_duration_ms histogram",
    ]
    for edge in _BUCKETS_MS:
        lines.append(f'ff_request_duration_ms_bucket{{service="{service}",le="{edge}"}} {int(row[f"b{edge}"])}')
    lines.append(f'ff_request_duration_ms_bucket{{service="{service}",le="+Inf"}} {int(row["requests"])}')
    lines.append(f'ff_request_duration_ms_sum{{service="{service}"}} {row["latency_sum"]}')
    lines.append(f'ff_request_duration_ms_count{{service="{service}"}} {int(row["requests"])}')
    return "\n".join(lines) + "\n"


def _probe(url: str) -> bool:
    try:
        with urlopen(url, timeout=0.4) as response:
            return 200 <= int(response.status) < 500
    except OSError:
        return False


def readiness(db_path: Path) -> dict[str, Any]:
    path = db_path
    database = True
    try:
        import sqlite3

        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(path))
        conn.execute("SELECT 1")
        conn.close()
    except sqlite3.Error:
        database = False
    mode = os.environ.get("MODEL_MODE", "replay")
    checks = {
        "database": database,
        "lake": _probe(os.environ.get("LAKE_REST_URL", "http://127.0.0.1:8091").rstrip("/") + "/health"),
        "idp": _probe(issuer_internal() + "/health"),
        "model_mode": mode in {"", "replay", "live"},
    }
    return {"ok": all(checks.values()), "checks": checks, "model_mode": mode or "replay"}


def install_platform(app: FastAPI, *, service: str, app_code: str, db_path: Path) -> None:
    @app.middleware("http")
    async def platform_guard(request: Request, call_next):
        trace = traceparent_for(request)
        request.state.traceparent = trace
        set_traceparent(trace)
        path = request.url.path
        if path not in {"/health", "/healthz", "/readyz", "/metrics"} and too_many(request):
            note_rate_limited(service)
            body = error_body("rate_limited", "Too many requests. Wait a minute and try again.")
            response = JSONResponse(body, status_code=429)
            response.headers["Retry-After"] = "60"
            return stamp(response, app_code, trace)
        started = time.perf_counter()
        response = await call_next(request)
        note_request(service, response.status_code, round((time.perf_counter() - started) * 1000, 3))
        return stamp(response, app_code, trace)

    @app.get("/healthz")
    def healthz() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/readyz")
    def readyz() -> JSONResponse:
        body = readiness(db_path)
        return JSONResponse(body, status_code=200 if body["ok"] else 503)

    @app.get("/metrics")
    def metrics() -> Response:
        return Response(prometheus(service), media_type="text/plain; version=0.0.4")
