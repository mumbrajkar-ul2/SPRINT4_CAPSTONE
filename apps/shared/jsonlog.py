"""One JSON object per line on stdout. The API key is never written."""
from __future__ import annotations

import contextvars
import json
import sys
from datetime import datetime, timezone
from typing import Any

_TRACEPARENT: contextvars.ContextVar[str] = contextvars.ContextVar("traceparent", default="")


def set_traceparent(value: str) -> None:
    _TRACEPARENT.set(value)

FORBIDDEN_KEYS = {
    "api_key",
    "x-api-key",
    "x_api_key",
    "fabpulse_api_key",
    "authorization",
    "password",
    "secret",
    "token",
}


def emit(
    *,
    service: str,
    event: str,
    level: str = "info",
    correlation_id: str | None = None,
    actor_id: str | None = None,
    path: str | None = None,
    status: int | None = None,
    duration_ms: float | None = None,
    **extra: Any,
) -> None:
    line: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": service,
        "level": level,
        "event": event,
        "correlation_id": correlation_id,
        "actor_id": actor_id,
        "path": path,
        "status": status,
        "duration_ms": duration_ms,
        "traceparent": _TRACEPARENT.get() or None,
    }
    for key, value in extra.items():
        if key.lower() in FORBIDDEN_KEYS:
            continue
        line[key] = value
    sys.stdout.write(json.dumps(line, separators=(",", ":")) + "\n")
    sys.stdout.flush()
