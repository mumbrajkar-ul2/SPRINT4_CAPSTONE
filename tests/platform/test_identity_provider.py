"""Acceptance tests for the local Force Fab identity provider."""
from __future__ import annotations

import base64
import os
import re
import secrets
from urllib.parse import parse_qs, urlsplit

import jwt
import pyotp
import pytest
from fastapi.testclient import TestClient
from jwt import PyJWK

from apps.identity.app import create_app
from apps.identity.crypto_util import pkce_challenge, totp_at
from apps.identity.seed_data import DEMO_PASSWORD

SECRET = "JBSWY3DPEHPK3PXP"
REDIRECT = "http://127.0.0.1:8100/auth/callback"


@pytest.fixture()
def idp(tmp_path, monkeypatch):
    monkeypatch.delenv("FF_ENV", raising=False)
    monkeypatch.delenv("FF_DEMO_HINTS", raising=False)
    monkeypatch.delenv("FF_IDP_PUBLIC_URL", raising=False)
    return create_app(state_dir=tmp_path)


@pytest.fixture()
def client(idp):
    return TestClient(idp, follow_redirects=False)


def _request_id(html: str) -> str:
    match = re.search(r"name='request_id' value='([^']+)'", html)
    assert match, html
    return match.group(1)


def _begin(client: TestClient, **extra):
    verifier = secrets.token_urlsafe(48)
    params = {
        "response_type": "code",
        "client_id": "force-fab-app-a",
        "redirect_uri": REDIRECT,
        "state": extra.pop("state", "state-1"),
        "nonce": extra.pop("nonce", "nonce-1"),
        "code_challenge": pkce_challenge(verifier),
        "code_challenge_method": "S256",
        "scope": "openid",
    }
    params.update(extra)
    response = client.get("/authorize", params=params)
    return verifier, response


def _password(client: TestClient, page, username: str, password: str = DEMO_PASSWORD):
    return client.post(
        "/authorize/continue",
        data={
            "request_id": _request_id(page.text),
            "stage": "login",
            "username": username,
            "password": password,
        },
    )


def _otp(client: TestClient, page, code: str | None = None):
    return client.post(
        "/authorize/continue",
        data={
            "request_id": _request_id(page.text),
            "stage": "otp",
            "otp": code if code is not None else pyotp.TOTP(SECRET).now(),
        },
    )


def _exchange(client: TestClient, location: str, verifier: str, redirect: str = REDIRECT):
    parsed = parse_qs(urlsplit(location).query)
    return client.post(
        "/token",
        data={
            "grant_type": "authorization_code",
            "code": parsed["code"][0],
            "redirect_uri": redirect,
            "code_verifier": verifier,
            "client_id": "force-fab-app-a",
            "client_secret": "dev-secret-a",
        },
    )


def _login(client: TestClient, username: str, **extra) -> dict:
    verifier, page = _begin(client, **extra)
    assert page.status_code == 200, page.text
    stepped = _password(client, page, username)
    if stepped.status_code == 200 and "One-time code" in stepped.text:
        if "Enrol" in stepped.text:
            stepped = client.post(
                "/authorize/continue",
                data={
                    "request_id": _request_id(stepped.text),
                    "stage": "enroll",
                    "otp": pyotp.TOTP(SECRET).now(),
                },
            )
        else:
            stepped = _otp(client, stepped)
    assert stepped.status_code == 302, stepped.text
    token = _exchange(client, stepped.headers["location"], verifier)
    assert token.status_code == 200, token.text
    return token.json()


def _bearer(token: dict) -> dict[str, str]:
    return {"Authorization": f"Bearer {token['access_token']}"}


def test_discovery(client: TestClient) -> None:
    body = client.get("/.well-known/openid-configuration").json()
    assert body["code_challenge_methods_supported"] == ["S256"]
    assert body["authorization_endpoint"].endswith("/authorize")
    assert body["jwks_uri"].endswith("/jwks.json")
    assert "authorization_code" in body["grant_types_supported"]


def test_jwks_and_signing_key_file(client: TestClient, idp) -> None:
    body = client.get("/jwks.json").json()
    assert body["keys"][0]["kty"] == "RSA"
    assert body["keys"][0]["alg"] == "RS256"
    key_path = idp.state.directory / "signing_key.pem"
    assert key_path.is_file()
    if os.name != "nt":
        assert key_path.stat().st_mode & 0o777 == 0o600


def test_pkce_flow_verifies_against_jwks(client: TestClient) -> None:
    bundle = _login(client, "reviewer.tw", nonce="nonce-pkce")
    jwks = client.get("/jwks.json").json()
    key = PyJWK.from_dict(jwks["keys"][0]).key
    issuer = client.get("/.well-known/openid-configuration").json()["issuer"]
    access = jwt.decode(bundle["access_token"], key, algorithms=["RS256"], audience="force-fab-app-a", issuer=issuer)
    ident = jwt.decode(bundle["id_token"], key, algorithms=["RS256"], audience="force-fab-app-a", issuer=issuer)
    assert access["sub"] == "reviewer.tw"
    assert "RT-01" in access["roles"]
    assert access["acr"] == "mfa"
    assert ident["nonce"] == "nonce-pkce"
    assert access["exp"] - access["iat"] == 15 * 60


def test_wrong_verifier_rejected(client: TestClient) -> None:
    verifier, page = _begin(client)
    stepped = _password(client, page, "reviewer.tw")
    stepped = _otp(client, stepped)
    token = _exchange(client, stepped.headers["location"], "x" * 50)
    assert token.status_code == 400
    assert token.json()["error"] == "invalid_grant"


def test_reused_code_rejected(client: TestClient) -> None:
    verifier, page = _begin(client)
    stepped = _otp(client, _password(client, page, "reviewer.tw"))
    first = _exchange(client, stepped.headers["location"], verifier)
    second = _exchange(client, stepped.headers["location"], verifier)
    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["error"] == "invalid_grant"


def test_wrong_redirect_rejected(client: TestClient) -> None:
    verifier, page = _begin(client)
    stepped = _otp(client, _password(client, page, "reviewer.tw"))
    token = _exchange(client, stepped.headers["location"], verifier, redirect="http://127.0.0.1:8100/other")
    assert token.status_code == 400
    assert token.json()["error"] == "invalid_grant"


def test_otp_required(client: TestClient) -> None:
    _verifier, page = _begin(client)
    stepped = _password(client, page, "engineer.az")
    assert stepped.status_code == 200
    assert "One-time code" in stepped.text
    assert stepped.status_code != 302


def test_wrong_otp_fails(client: TestClient) -> None:
    _verifier, page = _begin(client)
    stepped = _password(client, page, "engineer.az")
    rejected = _otp(client, stepped, code="000000")
    assert rejected.status_code == 401
    assert "rejected" in rejected.text


def test_step_up_forces_otp_when_mfa_is_old(client: TestClient, idp) -> None:
    _login(client, "opslead")
    idp.state.conn.execute("UPDATE sessions SET auth_time=?", (int(idp.state.clock()) - 600,))
    idp.state.conn.commit()
    _verifier, page = _begin(client, acr_values="mfa")
    assert page.status_code == 200
    assert "One-time code" in page.text


def test_refresh_rotation(client: TestClient) -> None:
    bundle = _login(client, "reviewer.tw")
    refreshed = client.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": bundle["refresh_token"],
            "client_id": "force-fab-app-a",
            "client_secret": "dev-secret-a",
        },
    )
    assert refreshed.status_code == 200
    body = refreshed.json()
    assert body["refresh_token"] != bundle["refresh_token"]
    assert body["access_token"]


def test_refresh_reuse_revokes_family(client: TestClient) -> None:
    bundle = _login(client, "reviewer.tw")
    first = client.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": bundle["refresh_token"],
            "client_id": "force-fab-app-a",
            "client_secret": "dev-secret-a",
        },
    ).json()
    reuse = client.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": bundle["refresh_token"],
            "client_id": "force-fab-app-a",
            "client_secret": "dev-secret-a",
        },
    )
    assert reuse.status_code == 400
    child = client.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": first["refresh_token"],
            "client_id": "force-fab-app-a",
            "client_secret": "dev-secret-a",
        },
    )
    assert child.status_code == 400


def test_client_credentials(client: TestClient) -> None:
    raw = base64.b64encode(b"force-fab-svc-a:dev-svc-a").decode("ascii")
    response = client.post(
        "/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {raw}"},
    )
    assert response.status_code == 200
    key = PyJWK.from_dict(client.get("/jwks.json").json()["keys"][0]).key
    issuer = client.get("/.well-known/openid-configuration").json()["issuer"]
    payload = jwt.decode(
        response.json()["access_token"],
        key,
        algorithms=["RS256"],
        audience="force-fab-lake",
        issuer=issuer,
    )
    assert payload["sub"] == "force-fab-svc-a"
    assert payload["roles"] == ["SVC"]


def test_lockout(client: TestClient) -> None:
    verifier, page = _begin(client)
    request_id = _request_id(page.text)
    for _ in range(5):
        page = client.post(
            "/authorize/continue",
            data={"request_id": request_id, "stage": "login", "username": "reviewer.tw", "password": "wrong-password-value"},
        )
        verifier, page = _begin(client)
        request_id = _request_id(page.text)
    locked = _password(client, page, "reviewer.tw")
    assert locked.status_code == 401
    assert "locked" in locked.text
    assert verifier


def test_rate_limit_429(client: TestClient) -> None:
    last = None
    for index in range(21):
        _verifier, page = _begin(client, state=f"s{index}")
        last = client.post(
            "/authorize/continue",
            data={
                "request_id": _request_id(page.text),
                "stage": "login",
                "username": f"nobody{index}",
                "password": "wrong-password-value",
            },
        )
    assert last is not None
    assert last.status_code == 429
    assert last.headers["retry-after"] == "60"


def test_password_too_short_without_mfa(client: TestClient) -> None:
    admin = _bearer(_login(client, "admin"))
    short = client.post(
        "/api/admin/users",
        headers=admin,
        json={"username": "short.user", "name": "Short", "password": "short-password", "mfa_enrolled": False},
    )
    long = client.post(
        "/api/admin/users",
        headers=admin,
        json={"username": "long.user", "name": "Long", "password": "long-enough-pass", "mfa_enrolled": False},
    )
    huge = client.post(
        "/api/admin/users",
        headers=admin,
        json={"username": "huge.user", "name": "Huge", "password": "a" * 65, "mfa_enrolled": False},
    )
    assert short.status_code == 400
    assert long.status_code == 200
    assert huge.status_code == 400


def test_password_short_allowed_with_mfa(client: TestClient) -> None:
    admin = _bearer(_login(client, "admin"))
    tiny = client.post(
        "/api/admin/users",
        headers=admin,
        json={"username": "tiny.user", "name": "Tiny", "password": "sevench", "mfa_enrolled": True},
    )
    ok = client.post(
        "/api/admin/users",
        headers=admin,
        json={"username": "ok.user", "name": "Ok", "password": "eightchr", "mfa_enrolled": True},
    )
    assert tiny.status_code == 400
    assert ok.status_code == 200


def test_password_blocklist(client: TestClient) -> None:
    admin = _bearer(_login(client, "admin"))
    blocked = client.post(
        "/api/admin/users",
        headers=admin,
        json={"username": "blocked.user", "name": "Blocked", "password": "password1234567", "mfa_enrolled": False},
    )
    assert blocked.status_code == 400
    assert "blocklist" in blocked.json()["message"]


def test_rfc6238_vector() -> None:
    assert totp_at(b"12345678901234567890", 59, ascii_secret=True) == "287082"
    assert totp_at(b"12345678901234567890", 1111111109, ascii_secret=True) == "081804"


def test_scim_crud(client: TestClient) -> None:
    raw = base64.b64encode(b"force-fab-scim:dev-scim").decode("ascii")
    token = client.post(
        "/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {raw}"},
    )
    assert token.status_code == 200
    headers = {"Authorization": f"Bearer {token.json()['access_token']}"}
    created = client.post(
        "/scim/v2/Users",
        headers=headers,
        json={"userName": "scim.user", "name": {"formatted": "SCIM User"}, "password": DEMO_PASSWORD, "active": True},
    )
    assert created.status_code == 201
    listed = client.get('/scim/v2/Users', headers=headers, params={"filter": 'userName eq "scim.user"'})
    assert listed.json()["totalResults"] == 1
    patched = client.patch(
        "/scim/v2/Users/scim.user",
        headers=headers,
        json={"Operations": [{"op": "replace", "path": "active", "value": False}]},
    )
    assert patched.json()["active"] is False
    deleted = client.delete("/scim/v2/Users/scim.user", headers=headers)
    assert deleted.status_code == 204
    groups = client.get("/scim/v2/Groups", headers=headers)
    names = {item["displayName"] for item in groups.json()["Resources"]}
    assert "RT-01" in names
    assert "FF-ADMIN" in names


def test_jit_request_approve_and_self_approve(client: TestClient, idp) -> None:
    admin_token = _login(client, "admin")
    other = TestClient(idp, follow_redirects=False)
    glass = _login(other, "breakglass")
    requested = client.post(
        "/api/admin/jit",
        headers=_bearer(admin_token),
        json={"role": "RT-06", "minutes": 30, "reason": "cover a shift"},
    )
    assert requested.status_code == 200
    request_id = requested.json()["id"]
    self_approve = client.post(f"/api/admin/jit/{request_id}/approve", headers=_bearer(admin_token))
    assert self_approve.status_code == 403
    assert self_approve.json()["error_class"] == "self_approve"
    approved = other.post(f"/api/admin/jit/{request_id}/approve", headers=_bearer(glass))
    assert approved.status_code == 200
    verifier, page = _begin(client)
    assert page.status_code == 302
    bundle = _exchange(client, page.headers["location"], verifier).json()
    payload = jwt.decode(bundle["access_token"], options={"verify_signature": False})
    assert "RT-06" in payload["roles"]
    assert "elevated_until" in payload


def test_jit_expiry(client: TestClient, idp) -> None:
    admin_token = _login(client, "admin")
    other = TestClient(idp, follow_redirects=False)
    glass = _login(other, "breakglass")
    request_id = client.post(
        "/api/admin/jit",
        headers=_bearer(admin_token),
        json={"role": "RT-06", "minutes": 30, "reason": "cover a shift"},
    ).json()["id"]
    assert other.post(f"/api/admin/jit/{request_id}/approve", headers=_bearer(glass)).status_code == 200
    idp.state.conn.execute("UPDATE jit_grants SET elevated_until=0")
    idp.state.conn.commit()
    verifier, page = _begin(client)
    bundle = _exchange(client, page.headers["location"], verifier).json()
    payload = jwt.decode(bundle["access_token"], options={"verify_signature": False})
    assert "RT-06" not in payload["roles"]
    assert "FF-ADMIN" in payload["roles"]


def test_break_glass_event(client: TestClient, idp) -> None:
    bundle = _login(client, "breakglass")
    denied = TestClient(idp, follow_redirects=False)
    admin = _login(denied, "admin")
    blocked = denied.post(
        "/api/admin/break-glass",
        headers=_bearer(admin),
        json={"minutes": 30, "reason": "not allowed"},
    )
    assert blocked.status_code == 403
    opened = client.post(
        "/api/admin/break-glass",
        headers=_bearer(bundle),
        json={"minutes": 30, "reason": "plant down"},
    )
    assert opened.status_code == 200
    rows = idp.state.conn.execute("SELECT body FROM auth_events").fetchall()
    assert any('"type":"break_glass"' in row["body"] and '"severity":"critical"' in row["body"] for row in rows)
    too_long = client.post(
        "/api/admin/break-glass",
        headers=_bearer(bundle),
        json={"minutes": 90, "reason": "too long"},
    )
    assert too_long.status_code == 400


def test_access_review_and_csv(client: TestClient) -> None:
    admin = _bearer(_login(client, "admin"))
    created = client.post("/api/admin/reviews", headers=admin, json={"name": "cycle-1"})
    assert created.status_code == 200
    review_id = created.json()["id"]
    items = client.get(f"/api/admin/reviews/{review_id}", headers=admin).json()["items"]
    assert items
    decision = client.post(
        f"/api/admin/reviews/{review_id}/items/{items[0]['id']}",
        headers=admin,
        json={"decision": "certify", "comment": "=1+1"},
    )
    assert decision.status_code == 200
    csv_text = client.get(f"/api/admin/reviews/{review_id}/export.csv", headers=admin).text
    assert "'=1+1" in csv_text
    assert items[0]["username"] in csv_text


def test_hash_chain_detects_tampering(client: TestClient, idp) -> None:
    _verifier, page = _begin(client)
    _password(client, page, "reviewer.tw", password="wrong-password-value")
    admin = _bearer(_login(client, "admin"))
    intact = client.get("/api/admin/audit/verify", headers=admin).json()
    assert intact["ok"] is True
    assert intact["length"] >= 1
    idp.state.conn.execute("UPDATE auth_events SET body='tampered' WHERE seq=1")
    idp.state.conn.commit()
    broken = client.get("/api/admin/audit/verify", headers=admin).json()
    assert broken["ok"] is False
    assert broken["broken_at"] == 1


def test_admin_endpoints_reject_non_admin(client: TestClient) -> None:
    reviewer = _bearer(_login(client, "reviewer.tw"))
    response = client.get("/api/admin/users", headers=reviewer)
    assert response.status_code == 403
    assert response.json()["error_class"] == "forbidden"


def test_logout_clears_session(client: TestClient) -> None:
    _login(client, "reviewer.tw")
    denied = client.get("/logout", params={"post_logout_redirect_uri": "https://evil.example/back"})
    assert denied.status_code == 400
    left = client.get("/logout", params={"post_logout_redirect_uri": "http://127.0.0.1:8100"})
    assert left.status_code == 302
    assert left.headers["location"] == "http://127.0.0.1:8100"
    _verifier, page = _begin(client)
    assert page.status_code == 200
    assert "Password" in page.text


def test_prompt_login_ignores_session(client: TestClient) -> None:
    _login(client, "reviewer.tw")
    _verifier, page = _begin(client, prompt="login")
    assert page.status_code == 200
    assert "Password" in page.text


def test_enrolment_for_analyst(client: TestClient) -> None:
    verifier, page = _begin(client, acr_values="mfa")
    stepped = _password(client, page, "analyst.az")
    assert "Enrol" in stepped.text
    enrolled = client.post(
        "/authorize/continue",
        data={"request_id": _request_id(stepped.text), "stage": "enroll", "otp": pyotp.TOTP(SECRET).now()},
    )
    assert enrolled.status_code == 302
    bundle = _exchange(client, enrolled.headers["location"], verifier).json()
    payload = jwt.decode(bundle["access_token"], options={"verify_signature": False})
    assert payload["acr"] == "mfa"
    assert payload["sub"] == "analyst.az"


def test_sod_blocks_admin_and_auditor_except_breakglass(client: TestClient) -> None:
    admin = _bearer(_login(client, "admin"))
    blocked = client.post("/api/admin/users/admin/roles", headers=admin, json={"role": "FF-AUDITOR"})
    assert blocked.status_code == 409
    assert blocked.json()["error_class"] == "sod_violation"
    users = client.get("/api/admin/users", headers=admin).json()["users"]
    breakglass = next(item for item in users if item["username"] == "breakglass")
    assert "FF-ADMIN" in breakglass["roles"]
    assert "RT-02" in breakglass["roles"]


def test_auditor_is_read_only(client: TestClient) -> None:
    auditor = _bearer(_login(client, "auditor"))
    listed = client.get("/api/admin/users", headers=auditor)
    assert listed.status_code == 200
    created = client.post(
        "/api/admin/users",
        headers=auditor,
        json={"username": "nope.user", "name": "Nope", "password": "long-enough-pass", "mfa_enrolled": False},
    )
    assert created.status_code == 403


def test_otp_cannot_be_reused_in_the_same_step(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("FF_ENV", raising=False)
    monkeypatch.delenv("FF_DEMO_HINTS", raising=False)
    frozen = {"now": 1_700_000_030.0}
    app = create_app(state_dir=tmp_path, clock=lambda: frozen["now"])
    local = TestClient(app, follow_redirects=False)
    code = pyotp.TOTP(SECRET).at(int(frozen["now"]))
    verifier, page = _begin(local)
    first = _otp(local, _password(local, page, "engineer.az"), code=code)
    assert first.status_code == 302
    _exchange(local, first.headers["location"], verifier)
    verifier, page = _begin(local, state="state-2", nonce="nonce-2", prompt="login")
    second = _otp(local, _password(local, page, "engineer.az"), code=code)
    assert second.status_code == 401


def test_demo_hint_shows_current_code(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("FF_ENV", raising=False)
    monkeypatch.setenv("FF_DEMO_HINTS", "1")
    app = create_app(state_dir=tmp_path)
    local = TestClient(app, follow_redirects=False)
    _verifier, page = _begin(local)
    stepped = _password(local, page, "reviewer.tw")
    assert re.search(r"Demo: current code \d{6}", stepped.text)


def test_demo_hints_refused_in_production(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("FF_ENV", "production")
    monkeypatch.setenv("FF_DEMO_HINTS", "1")
    with pytest.raises(RuntimeError, match="FF_DEMO_HINTS"):
        create_app(state_dir=tmp_path)


def test_sso_cookie_signs_in_without_a_second_password(client: TestClient) -> None:
    _login(client, "policy.owner")
    verifier, page = _begin(client, state="state-sso", nonce="nonce-sso")
    assert page.status_code == 302
    bundle = _exchange(client, page.headers["location"], verifier).json()
    payload = jwt.decode(bundle["access_token"], options={"verify_signature": False})
    assert payload["sub"] == "policy.owner"
