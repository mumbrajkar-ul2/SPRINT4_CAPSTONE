"""Signed-token checks for both apps and the lake listener."""
from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a
from apps.app_b.server import app as app_b
from apps.shared.oidc_session import bearer_headers, cookie_names, mint_token, put_test_session, refuse_unsafe_flags
from apps.shared.site_scope import path_skips_site, site_visible
from rest_server import app as lake_rest

_SIGN = {"meaning": "I confirm this record.", "reason": "Reviewed the cited case."}


def test_bad_bearer_is_unauthenticated() -> None:
    response = TestClient(app_a).get("/api/identity-check", headers={"Authorization": "Bearer not-a-token"})
    assert response.status_code == 401
    assert response.json()["error_class"] == "unauthenticated"


def test_login_redirects_to_the_identity_provider() -> None:
    response = TestClient(app_a).get("/auth/login", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"].startswith(os.environ["FF_IDP_PUBLIC_URL"])


def test_cookie_post_without_csrf_is_rejected() -> None:
    token = mint_token(sub="demo-rt05-1", roles=["RT-05"])
    import jwt

    claims = jwt.decode(token, options={"verify_signature": False})
    sid, csrf = put_test_session("a", claims)
    name = cookie_names("a")["session"]
    client = TestClient(app_a)
    opened = client.get("/api/queue", cookies={name: sid})
    assert opened.status_code == 200
    posted = client.post("/api/demo/replay/receive", cookies={name: sid})
    assert posted.status_code == 403
    assert posted.json()["error_class"] == "csrf_failed"
    sent = client.post("/api/demo/replay/receive", cookies={name: sid}, headers={"X-CSRF-Token": csrf})
    assert sent.status_code == 200


def test_step_up_runs_after_the_role_check() -> None:
    wrong = bearer_headers("RT-05", acr="pwd", auth_time=1)
    refused = TestClient(app_a).post(
        "/api/approvals",
        headers=wrong,
        json={
            "case_id": "PS000000016",
            "action_type": "recipe_hold_or_release",
            "decision": "hold",
            "proposed_by": "model_draft",
        },
    )
    assert refused.status_code == 403
    assert refused.json()["message"] == "Hold waits for RT-03."
    stale = bearer_headers("RT-03", acr="pwd", auth_time=1)
    stepped = TestClient(app_a).post(
        "/api/approvals",
        headers=stale,
        json={
            "case_id": "PS000000016",
            "action_type": "recipe_hold_or_release",
            "decision": "hold",
            "proposed_by": "model_draft",
            "signature": _SIGN,
        },
    )
    assert stepped.status_code == 401
    assert stepped.json()["error_class"] == "step_up_required"


def test_admin_alone_cannot_approve() -> None:
    headers = bearer_headers("FF-ADMIN", actor="admin")
    response = TestClient(app_a).post(
        "/api/approvals",
        headers=headers,
        json={
            "case_id": "PS000000016",
            "action_type": "recipe_hold_or_release",
            "decision": "hold",
            "proposed_by": "model_draft",
        },
    )
    assert response.status_code == 403
    assert response.json()["error_class"] == "forbidden_role"


def test_same_person_stays_forbidden_role() -> None:
    headers = bearer_headers("RT-03")
    response = TestClient(app_a).post(
        "/api/approvals",
        headers=headers,
        json={
            "case_id": "PS000000016",
            "action_type": "recipe_hold_or_release",
            "decision": "hold",
            "proposed_by": "demo-rt03-1",
            "signature": _SIGN,
        },
    )
    assert response.status_code == 403
    assert response.json()["error_class"] == "forbidden_role"


def test_lake_rejects_a_token_without_the_service_role() -> None:
    headers = bearer_headers("RT-01", aud="force-fab-lake")
    response = TestClient(lake_rest).get("/v1/version", headers=headers)
    assert response.status_code == 401
    assert response.json()["error_class"] == "missing_identity"


def test_legacy_headers_are_refused_in_production(monkeypatch) -> None:
    monkeypatch.setenv("FF_ENV", "production")
    monkeypatch.setenv("FF_ALLOW_LEGACY_HEADERS", "1")
    with pytest.raises(RuntimeError):
        refuse_unsafe_flags()


def test_site_rules_keep_the_scenario_ids_open() -> None:
    assert path_skips_site("/api/queue")
    assert path_skips_site("/api/demo/state")
    assert site_visible(["FAB-02"], "DE-BY", "PS000000016")
    assert site_visible(["FAB-02"], None, "OTHER")
    assert site_visible(["FAB-01"], "DE-BY", "LOT-1")
    assert not site_visible(["FAB-02"], "DE-BY", "LOT-1")
