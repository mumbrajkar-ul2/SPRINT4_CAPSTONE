"""Header checks for Application A, Application B, and lake listeners."""
from __future__ import annotations

import os
from typing import Any, Mapping

HEADER_API_KEY = "X-Api-Key"
HEADER_ACTOR_ID = "X-Actor-Id"
HEADER_ACTOR_ROLE = "X-Actor-Role"
HEADER_CORRELATION = "X-Correlation-Id"

LAKE_ITEM_IDENTITY = "decision.bp8.auth_and_owner"

CLOSED_ROLES = ("RT-01", "RT-02", "RT-03", "RT-04", "RT-05", "RT-06")
ACCEPTED_ROLES = CLOSED_ROLES + ("FF-ADMIN", "FF-AUDITOR", "SVC")
ACTION_ROLE_MAP = {
    "dispose": "RT-01",
    "approve_agent": "RT-02",
    "recipe_hold_or_release": "RT-03",
    "policy_pick": "RT-04",
    "keep_wait": "RT-04",
    "replay_confirm": "RT-05",
    "assign_owner": "RT-06",
}
DEMO_ACTORS = {
    "demo-rt01-1": "RT-01",
    "demo-rt02-1": "RT-02",
    "demo-rt03-1": "RT-03",
    "demo-rt04-1": "RT-04",
    "demo-rt05-1": "RT-05",
    "demo-rt06-1": "RT-06",
}


def configured_api_key() -> str | None:
    value = os.environ.get("FABPULSE_API_KEY")
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def header_get(headers: Mapping[str, str], name: str) -> str:
    for key, value in headers.items():
        if key.lower() == name.lower():
            return (value or "").strip()
    return ""


def error_body(
    error_class: str,
    message: str,
    *,
    correlation_id: str | None = None,
    lake_item_ids: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "error_class": error_class,
        "message": message,
        "correlation_id": correlation_id,
        "waiting_role": None,
        "lake_item_ids": lake_item_ids or [],
    }


def missing_identity(correlation_id: str | None = None) -> dict[str, Any]:
    return error_body(
        "missing_identity",
        "This request needs X-Api-Key, X-Actor-Id, and X-Actor-Role.",
        correlation_id=correlation_id,
        lake_item_ids=[LAKE_ITEM_IDENTITY],
    )


def missing_server_key(correlation_id: str | None = None) -> dict[str, Any]:
    return error_body(
        "missing_server_key",
        "The process has no FABPULSE_API_KEY. Set that variable. The documented local default lives in .env.example.",
        correlation_id=correlation_id,
        lake_item_ids=[LAKE_ITEM_IDENTITY],
    )


def identity_reject(error: Mapping[str, Any]) -> tuple[dict[str, Any], int, str]:
    """Return the error body, HTTP status, and log event for an identity or key miss."""
    if error.get("error_class") == "missing_server_key":
        return dict(error), 503, "server_key_missing"
    return dict(error), 401, "identity_missing"


def forbidden_role(correlation_id: str | None = None) -> dict[str, Any]:
    return error_body(
        "forbidden_role",
        "X-Actor-Role must be one of RT-01 to RT-06 and must match the action.",
        correlation_id=correlation_id,
        lake_item_ids=[LAKE_ITEM_IDENTITY, "term.approval"],
    )


def missing_lake_key(correlation_id: str | None = None) -> dict[str, Any]:
    return error_body(
        "missing_identity",
        "This lake read needs X-Api-Key.",
        correlation_id=correlation_id,
        lake_item_ids=[LAKE_ITEM_IDENTITY],
    )


def lake_write_rejected(correlation_id: str | None = None) -> dict[str, Any]:
    return error_body(
        "lake_write_rejected",
        "Lake items change only when build.py writes the SQLite file.",
        correlation_id=correlation_id,
        lake_item_ids=["arch.lake.yaml_sqlite"],
    )


def check_app_identity(headers: Mapping[str, str]) -> dict[str, Any] | None:
    """Return an error body when a case-path call is missing a valid identity."""
    correlation_id = header_get(headers, HEADER_CORRELATION) or None
    expected = configured_api_key()
    if expected is None:
        return missing_server_key(correlation_id)
    key = header_get(headers, HEADER_API_KEY)
    actor = header_get(headers, HEADER_ACTOR_ID)
    role = header_get(headers, HEADER_ACTOR_ROLE)
    if not key or not actor or not role or key != expected:
        return missing_identity(correlation_id)
    return None


def check_closed_role(headers: Mapping[str, str]) -> dict[str, Any] | None:
    """Return an error when X-Actor-Role is present but not an accepted role."""
    correlation_id = header_get(headers, HEADER_CORRELATION) or None
    role = header_get(headers, HEADER_ACTOR_ROLE)
    if role and role not in ACCEPTED_ROLES:
        return forbidden_role(correlation_id)
    return None


def check_write_action(
    *,
    role: str,
    action_type: str,
    actor_id: str,
    proposed_by: str,
    correlation_id: str | None = None,
) -> dict[str, Any] | None:
    """Return an error when the person role does not match the write."""
    allowed = ACTION_ROLE_MAP.get(action_type)
    if allowed is None or role not in CLOSED_ROLES:
        return forbidden_role(correlation_id)
    if actor_id == proposed_by or not actor_id or not proposed_by:
        return forbidden_role(correlation_id)
    if role != allowed:
        if action_type == "recipe_hold_or_release":
            return error_body(
                "forbidden_role",
                "Hold waits for RT-03.",
                correlation_id=correlation_id,
                lake_item_ids=[LAKE_ITEM_IDENTITY, "term.approval"],
            )
        return forbidden_role(correlation_id)
    return None


def check_lake_key(headers: Mapping[str, str]) -> dict[str, Any] | None:
    """Return an error body when a lake route has no service token."""
    correlation_id = header_get(headers, HEADER_CORRELATION) or None
    expected = configured_api_key()
    if expected is None:
        return missing_server_key(correlation_id)
    from apps.shared.oidc_session import legacy_headers, verify_access_token

    if legacy_headers():
        key = header_get(headers, HEADER_API_KEY)
        if key and key == expected:
            return None
    header = header_get(headers, "Authorization")
    token = header.split(" ", 1)[1].strip() if header.lower().startswith("bearer ") else ""
    if token:
        payload = verify_access_token(token, audience="force-fab-lake")
        if payload and "SVC" in (payload.get("roles") or []):
            return None
    return missing_lake_key(correlation_id)
