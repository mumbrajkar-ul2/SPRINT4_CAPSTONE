"""Signed-token sessions for Application A and Application B.

The browser keeps a host-scoped cookie. Route code still reads X-Actor-Id and
X-Actor-Role. This module writes those headers from the token before the route runs.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import jwt
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from jwt.algorithms import RSAAlgorithm

from apps.shared.ai_safety import set_actor
from apps.shared.identity import (
    HEADER_ACTOR_ID,
    HEADER_ACTOR_ROLE,
    HEADER_API_KEY,
    CLOSED_ROLES,
    configured_api_key,
    error_body,
    header_get,
)

STEP_UP_SECONDS = 300
SESSION_IDLE = 30 * 60
SESSION_ABSOLUTE = 8 * 3600
_SESSIONS: dict[str, dict[str, Any]] = {}
_JWKS_CACHE: dict[str, Any] = {}
_LAKE_TOKEN: dict[str, Any] = {"token": "", "exp": 0}


def refuse_unsafe_flags() -> None:
    if os.environ.get("FF_ENV") == "production" and os.environ.get("FF_ALLOW_LEGACY_HEADERS") == "1":
        raise RuntimeError("FF_ALLOW_LEGACY_HEADERS=1 is refused when FF_ENV=production.")


def legacy_headers() -> bool:
    return os.environ.get("FF_ALLOW_LEGACY_HEADERS") == "1"


def issuer() -> str:
    """Address the browser uses. Tokens also name this address."""
    return os.environ.get("FF_IDP_PUBLIC_URL", "http://127.0.0.1:8095").rstrip("/")


def issuer_internal() -> str:
    """Address the app process uses. Inside Docker this is the identity service name."""
    return os.environ.get("FF_IDP_INTERNAL_URL", issuer()).rstrip("/")


def cookie_secret() -> str:
    value = os.environ.get("FF_COOKIE_SECRET")
    if value:
        return value
    generated = secrets.token_hex(32)
    os.environ["FF_COOKIE_SECRET"] = generated
    return generated


def cookie_names(app_code: str) -> dict[str, str]:
    return {
        "session": f"ff_session_{app_code}",
        "csrf": f"ff_csrf_{app_code}",
        "auth": f"ff_auth_{app_code}",
    }


def actor_role(roles: list[str]) -> str:
    for role in roles:
        if role in CLOSED_ROLES:
            return role
    for role in ("FF-ADMIN", "FF-AUDITOR", "SVC"):
        if role in roles:
            return role
    return roles[0] if roles else ""


def _seal(payload: dict[str, Any]) -> str:
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(cookie_secret().encode(), body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"


def _open_seal(value: str) -> dict[str, Any] | None:
    if "." not in value:
        return None
    body, sig = value.rsplit(".", 1)
    expect = hmac.new(cookie_secret().encode(), body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expect):
        return None
    pad = "=" * (-len(body) % 4)
    try:
        payload = json.loads(base64.urlsafe_b64decode(body + pad))
    except (json.JSONDecodeError, ValueError):
        return None
    if float(payload.get("exp") or 0) < time.time():
        return None
    return payload


def _load_jwks(*, force: bool = False) -> dict[str, Any]:
    if _JWKS_CACHE and not force:
        return _JWKS_CACHE
    path = os.environ.get("FF_JWKS_FILE")
    if path and Path(path).is_file():
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        data = _fetch_jwks()
    _JWKS_CACHE.clear()
    for item in data.get("keys") or []:
        kid = item.get("kid")
        if kid:
            _JWKS_CACHE[kid] = RSAAlgorithm.from_jwk(json.dumps(item))
    return _JWKS_CACHE


def _fetch_jwks() -> dict[str, Any]:
    from urllib.request import urlopen

    url = issuer_internal() + "/jwks.json"
    try:
        with urlopen(url, timeout=3) as response:
            return json.loads(response.read().decode("utf-8"))
    except OSError:
        return {"keys": []}


def verify_access_token(token: str, *, audience: str) -> dict[str, Any] | None:
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError:
        return None
    kid = str(header.get("kid") or "")
    keys = _load_jwks()
    key = keys.get(kid)
    if key is None:
        key = _load_jwks(force=True).get(kid)
    if key is None:
        return None
    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=issuer(),
            leeway=30,
            options={"verify_aud": False},
        )
    except jwt.PyJWTError:
        return None
    aud = payload.get("aud")
    auds = aud if isinstance(aud, list) else [aud]
    if audience not in auds:
        return None
    return payload


def mint_token(
    *,
    sub: str,
    roles: list[str],
    sites: list[str] | None = None,
    acr: str = "mfa",
    aud: str | list[str] | None = None,
    auth_time: int | None = None,
    amr: list[str] | None = None,
) -> str:
    private_path = os.environ.get("FF_JWT_PRIVATE_FILE")
    if not private_path:
        raise RuntimeError("FF_JWT_PRIVATE_FILE is not set.")
    private_pem = Path(private_path).read_bytes()
    jwks = json.loads(Path(os.environ["FF_JWKS_FILE"]).read_text(encoding="utf-8"))
    kid = jwks["keys"][0]["kid"]
    stamp = int(time.time())
    claims = {
        "iss": issuer(),
        "aud": aud if aud is not None else ["force-fab-app-a", "force-fab-app-b"],
        "sub": sub,
        "name": sub,
        "email": f"{sub}@force-fab.local",
        "roles": roles,
        "sites": sites if sites is not None else ["FAB-01", "FAB-02"],
        "acr": acr,
        "amr": amr if amr is not None else (["pwd", "otp"] if acr == "mfa" else ["pwd"]),
        "auth_time": stamp if auth_time is None else auth_time,
        "sid": "test-sid",
        "jti": secrets.token_hex(8),
        "iat": stamp,
        "exp": stamp + 900,
    }
    return jwt.encode(claims, private_pem, algorithm="RS256", headers={"kid": kid})


def bearer_headers(
    role: str = "RT-01",
    *,
    actor: str | None = None,
    correlation_id: str | None = None,
    sites: list[str] | None = None,
    acr: str = "mfa",
    auth_time: int | None = None,
    aud: str | list[str] | None = None,
) -> dict[str, str]:
    if actor is None:
        actor = f"demo-rt0{role[-1]}-1" if role.startswith("RT-") and len(role) == 5 else role.lower()
    token = mint_token(sub=actor, roles=[role], sites=sites, acr=acr, auth_time=auth_time, aud=aud)
    headers = {"Authorization": f"Bearer {token}"}
    if correlation_id:
        headers["X-Correlation-Id"] = correlation_id
    return headers


def service_token() -> str:
    override = os.environ.get("FF_LAKE_TOKEN")
    if override:
        return override
    if _LAKE_TOKEN["token"] and _LAKE_TOKEN["exp"] - 60 > time.time():
        return str(_LAKE_TOKEN["token"])
    token = _fetch_service_token()
    return token


def _fetch_service_token() -> str:
    from urllib.request import Request, urlopen

    client_id = os.environ.get("FF_SVC_CLIENT_ID", "force-fab-svc-a")
    secret = os.environ.get("FF_SVC_CLIENT_SECRET", "dev-svc-a")
    raw = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
    body = urlencode({"grant_type": "client_credentials"}).encode()
    request = Request(
        issuer_internal() + "/token",
        data=body,
        headers={"Authorization": f"Basic {raw}", "Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urlopen(request, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except OSError:
        return ""
    token = str(payload.get("access_token") or "")
    _LAKE_TOKEN["token"] = token
    _LAKE_TOKEN["exp"] = time.time() + int(payload.get("expires_in") or 900)
    return token


def _bearer(request: Request) -> str:
    header = header_get(request.headers, "Authorization")
    if header.lower().startswith("bearer "):
        return header.split(" ", 1)[1].strip()
    return ""


def _rewrite(request: Request, claims: dict[str, Any]) -> None:
    role = actor_role(list(claims.get("roles") or []))
    actor = str(claims.get("sub") or "")
    key = configured_api_key() or ""
    drop = {HEADER_API_KEY.lower(), HEADER_ACTOR_ID.lower(), HEADER_ACTOR_ROLE.lower()}
    headers = []
    for name, value in request.scope.get("headers") or []:
        if name.decode("latin1").lower() in drop:
            continue
        headers.append((name, value))
    for name, value in (
        (HEADER_API_KEY, key),
        (HEADER_ACTOR_ID, actor),
        (HEADER_ACTOR_ROLE, role),
    ):
        headers.append((name.lower().encode("latin1"), value.encode("latin1")))
    request.scope["headers"] = headers
    if hasattr(request, "_headers"):
        delattr(request, "_headers")
    request.state.claims = claims


def prepare_request(request: Request, *, audience: str, app_code: str) -> JSONResponse | None:
    if configured_api_key() is None:
        return None
    if legacy_headers():
        request.state.auth_via = "legacy"
        request.state.claims = {}
        set_actor("")
        return None
    names = cookie_names(app_code)
    token = _bearer(request)
    claims = verify_access_token(token, audience=audience) if token else None
    via = "bearer" if claims else ""
    if claims is None:
        sid = request.cookies.get(names["session"])
        session = _SESSIONS.get(sid or "")
        now = time.time()
        if session and session["idle"] > now and session["absolute"] > now and session["audience"] == audience:
            session["idle"] = now + SESSION_IDLE
            claims = session["claims"]
            via = "session"
            request.state.session = session
    if claims is None:
        login = f"/auth/login?next={request.url.path}"
        body = error_body(
            "unauthenticated",
            "Sign in is required.",
            correlation_id=header_get(request.headers, "X-Correlation-Id") or None,
        )
        body["login_url"] = login
        return JSONResponse(body, status_code=401)
    if via == "session" and request.method.upper() not in {"GET", "HEAD", "OPTIONS"}:
        sent = header_get(request.headers, "X-CSRF-Token")
        if not sent or not hmac.compare_digest(sent, request.state.session["csrf"]):
            body = error_body("csrf_failed", "The form token did not match this session.")
            return JSONResponse(body, status_code=403)
    request.state.auth_via = via
    _rewrite(request, claims)
    set_actor(str(claims.get("sub") or ""))
    return None


def approval_gate(request: Request, payload: dict[str, Any], correlation_id: str | None) -> JSONResponse | None:
    if legacy_headers():
        return None
    signature = payload.get("signature")
    if not isinstance(signature, dict) or not signature.get("meaning") or not str(signature.get("reason") or "").strip():
        return JSONResponse(
            error_body("signature_required", "This approval needs a signature meaning and a reason.", correlation_id=correlation_id),
            status_code=400,
        )
    claims = getattr(request.state, "claims", None) or {}
    if claims.get("acr") != "mfa" or (time.time() - int(claims.get("auth_time") or 0)) > STEP_UP_SECONDS:
        body = error_body("step_up_required", "Sign in again with a one-time code.", correlation_id=correlation_id)
        body["stepup_url"] = "/auth/stepup?next=/approvals"
        return JSONResponse(body, status_code=401)
    return None


def store_signature(db_path: Path, request: Request, payload: dict[str, Any], correlation_id: str | None) -> None:
    import sqlite3

    claims = getattr(request.state, "claims", None) or {}
    signature = payload.get("signature") or {}
    canonical = json.dumps(
        {
            "decision": payload.get("decision"),
            "signer": claims.get("sub"),
            "meaning": signature.get("meaning"),
            "reason": signature.get("reason"),
            "auth_time": claims.get("auth_time"),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS approval_signatures (
            id INTEGER PRIMARY KEY,
            correlation_id TEXT,
            audit_id TEXT,
            signer_sub TEXT,
            signer_name TEXT,
            meaning TEXT,
            reason TEXT,
            signed_at TEXT,
            token_jti TEXT,
            signature_hash TEXT
        )
        """
    )
    audit_id = ""
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='audit_chain'"
    ).fetchone()
    if row and correlation_id:
        found = conn.execute(
            "SELECT audit_id FROM audit_chain WHERE correlation_id=? ORDER BY seq DESC LIMIT 1",
            (correlation_id,),
        ).fetchone()
        if found:
            audit_id = found[0]
    conn.execute(
        """
        INSERT INTO approval_signatures(
            correlation_id, audit_id, signer_sub, signer_name, meaning, reason, signed_at, token_jti, signature_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            correlation_id,
            audit_id,
            claims.get("sub"),
            claims.get("name"),
            signature.get("meaning"),
            signature.get("reason"),
            time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            claims.get("jti"),
            digest,
        ),
    )
    conn.commit()
    conn.close()


def install_auth(app: FastAPI, *, app_code: str, audience: str, port: int) -> None:
    names = cookie_names(app_code)
    client_id = f"force-fab-app-{app_code}"
    router = APIRouter()

    @router.get("/auth/login")
    def login(next: str = "/", switch: str = "") -> RedirectResponse:
        verifier = secrets.token_urlsafe(48)
        state = secrets.token_urlsafe(16)
        nonce = secrets.token_urlsafe(16)
        from apps.identity.crypto_util import pkce_challenge

        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": f"http://127.0.0.1:{port}/auth/callback",
            "scope": "openid",
            "state": state,
            "nonce": nonce,
            "code_challenge": pkce_challenge(verifier),
            "code_challenge_method": "S256",
        }
        if switch:
            params["prompt"] = "login"
        query = urlencode(params)
        response = RedirectResponse(f"{issuer()}/authorize?{query}", status_code=302)
        response.set_cookie(
            names["auth"],
            _seal({"verifier": verifier, "state": state, "nonce": nonce, "next": next, "exp": time.time() + 600}),
            httponly=True,
            samesite="lax",
            max_age=600,
            path="/",
        )
        return response

    @router.get("/auth/callback")
    def callback(request: Request, code: str = "", state: str = "") -> RedirectResponse:
        sealed = _open_seal(request.cookies.get(names["auth"], ""))
        if sealed is None or sealed.get("state") != state or not code:
            return RedirectResponse("/auth/login", status_code=302)
        bundle = _exchange_code(client_id, code, sealed["verifier"], port)
        if not bundle:
            return RedirectResponse("/auth/login", status_code=302)
        claims = verify_access_token(bundle.get("access_token", ""), audience=audience)
        if claims is None:
            return RedirectResponse("/auth/login", status_code=302)
        if claims.get("nonce") and claims.get("nonce") != sealed.get("nonce") and bundle.get("id_token"):
            ident = verify_access_token(bundle["id_token"], audience=audience)
            if ident and ident.get("nonce") != sealed.get("nonce"):
                return RedirectResponse("/auth/login", status_code=302)
        sid = secrets.token_urlsafe(24)
        csrf = secrets.token_urlsafe(16)
        now = time.time()
        _SESSIONS[sid] = {
            "claims": claims,
            "csrf": csrf,
            "audience": audience,
            "refresh": bundle.get("refresh_token"),
            "idle": now + SESSION_IDLE,
            "absolute": now + SESSION_ABSOLUTE,
        }
        response = RedirectResponse(str(sealed.get("next") or "/"), status_code=302)
        response.set_cookie(names["session"], sid, httponly=True, samesite="lax", path="/", max_age=SESSION_ABSOLUTE)
        response.delete_cookie(names["auth"], path="/")
        return response

    @router.get("/auth/me")
    def me(request: Request) -> JSONResponse:
        failure = prepare_request(request, audience=audience, app_code=app_code)
        if failure is not None:
            return failure
        claims = request.state.claims
        csrf = ""
        if getattr(request.state, "auth_via", "") == "session":
            csrf = request.state.session["csrf"]
        return JSONResponse(
            {
                "sub": claims.get("sub"),
                "name": claims.get("name"),
                "roles": claims.get("roles") or [],
                "sites": claims.get("sites") or [],
                "acr": claims.get("acr"),
                "amr": claims.get("amr") or [],
                "exp": claims.get("exp"),
                "app": app_code.upper(),
                "idp": issuer(),
                "csrf": csrf,
            }
        )

    @router.get("/auth/stepup")
    def stepup(next: str = "/") -> RedirectResponse:
        verifier = secrets.token_urlsafe(48)
        state = secrets.token_urlsafe(16)
        nonce = secrets.token_urlsafe(16)
        from apps.identity.crypto_util import pkce_challenge

        query = urlencode(
            {
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": f"http://127.0.0.1:{port}/auth/callback",
                "scope": "openid",
                "state": state,
                "nonce": nonce,
                "code_challenge": pkce_challenge(verifier),
                "code_challenge_method": "S256",
                "acr_values": "mfa",
                "prompt": "login",
            }
        )
        response = RedirectResponse(f"{issuer()}/authorize?{query}", status_code=302)
        response.set_cookie(
            names["auth"],
            _seal({"verifier": verifier, "state": state, "nonce": nonce, "next": next, "exp": time.time() + 600}),
            httponly=True,
            samesite="lax",
            max_age=600,
            path="/",
        )
        return response

    @router.get("/auth/logout")
    def logout_get(request: Request) -> RedirectResponse:
        sid = request.cookies.get(names["session"])
        if sid:
            _SESSIONS.pop(sid, None)
        back = f"http://127.0.0.1:{port}/auth/login?switch=1"
        response = RedirectResponse(
            f"{issuer()}/logout?{urlencode({'post_logout_redirect_uri': back})}",
            status_code=302,
        )
        response.delete_cookie(names["session"], path="/")
        return response

    @router.post("/auth/logout")
    def logout() -> JSONResponse:
        return JSONResponse({"ok": True, "logout_url": f"{issuer()}/logout?post_logout_redirect_uri=http://127.0.0.1:{port}"})

    app.include_router(router)


def _exchange_code(client_id: str, code: str, verifier: str, port: int) -> dict[str, Any] | None:
    from urllib.request import Request, urlopen

    secret = os.environ.get(f"FF_CLIENT_SECRET_{client_id[-1].upper()}", "dev-secret-a" if client_id.endswith("-a") else "dev-secret-b")
    raw = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
    body = urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"http://127.0.0.1:{port}/auth/callback",
            "code_verifier": verifier,
        }
    ).encode()
    request = Request(
        issuer_internal() + "/token",
        data=body,
        headers={"Authorization": f"Basic {raw}", "Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urlopen(request, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except OSError:
        return None


def put_test_session(app_code: str, claims: dict[str, Any]) -> tuple[str, str]:
    """Create a session cookie value for tests. Returns sid and csrf."""
    sid = secrets.token_urlsafe(18)
    csrf = secrets.token_urlsafe(12)
    now = time.time()
    audience = "force-fab-app-a" if app_code == "a" else "force-fab-app-b"
    _SESSIONS[sid] = {
        "claims": claims,
        "csrf": csrf,
        "audience": audience,
        "refresh": "",
        "idle": now + SESSION_IDLE,
        "absolute": now + SESSION_ABSOLUTE,
    }
    return sid, csrf
