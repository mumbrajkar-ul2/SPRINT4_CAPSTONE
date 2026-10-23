"""Force Fab Identity HTTP application."""
from __future__ import annotations

import base64
import json
import os
import secrets
import threading
from contextlib import contextmanager
from html import escape
from pathlib import Path
from typing import Any, Callable, Iterator
from urllib.parse import urlencode, urlsplit

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from apps.identity.crypto_util import (
    DEMO_TOTP_SECRET,
    check_password,
    current_step,
    dummy_hash,
    hash_password,
    hashes_equal,
    json_jwk,
    load_or_create_key,
    password_problem,
    pkce_challenge,
    sha256_text,
    sign_jwt,
    totp_at,
    totp_ok,
)
from apps.identity.db import connect
from apps.identity.seed_data import seed

ACCESS_TTL = 15 * 60
REFRESH_TTL = 8 * 3600
CODE_TTL = 60
REQUEST_TTL = 600
SESSION_TTL = 8 * 3600
STEP_UP_SECONDS = 300

# Same colors and type as the shift screen in apps/ui_shared/src/theme.css.
_PAGE_STYLE = """
:root {
  color-scheme: dark;
  --bg: #14181d;
  --panel: #1d242c;
  --ink: #f4f1ea;
  --muted: #b7c0c8;
  --line: #33404a;
  --accent: #d85a45;
  --accent-ink: #1a100e;
  font-family: "Segoe UI", sans-serif;
}
body { margin: 0; min-height: 100vh; background: var(--bg); color: var(--ink); }
.page-bar { height: 4px; background: var(--accent); }
.console-header {
  display: flex; align-items: center; gap: 16px;
  padding: 16px 20px; background: var(--panel); border-bottom: 1px solid var(--line);
}
.logo-word { font-size: 22px; font-weight: 700; }
.logo-word small { font-weight: 500; color: var(--muted); }
.sheet { display: grid; justify-items: center; padding: 48px 16px 64px; }
.card {
  width: min(440px, 100%); box-sizing: border-box;
  background: var(--panel); border: 1px solid var(--line); border-radius: 10px;
  padding: 28px 24px 24px;
}
h1 { margin: 0 0 8px; font-size: 28px; font-weight: 700; color: var(--ink); }
p { margin: 0 0 16px; font-size: 16px; line-height: 1.45; color: var(--ink); }
.lead { color: var(--muted); }
.hint {
  color: var(--ink); background: #2a343e; border: 1px solid var(--line);
  border-radius: 8px; padding: 10px 12px;
}
.notice, .card form + p {
  background: #3a2422; border: 1px solid var(--accent); border-radius: 8px; padding: 10px 12px;
}
label { display: block; margin: 0 0 14px; color: var(--muted); font-size: 14px; font-weight: 600; }
input, button { font-family: inherit; font-size: 16px; }
input {
  display: block; width: 100%; box-sizing: border-box; margin-top: 6px;
  background: var(--bg); color: var(--ink); border: 1px solid var(--line);
  border-radius: 8px; padding: 10px 12px;
}
input:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
button {
  width: 100%; margin-top: 6px; background: var(--accent); color: var(--accent-ink);
  border: 0; border-radius: 8px; font-weight: 700; padding: 10px 16px; cursor: pointer;
}
ul { margin: 0 0 16px; padding-left: 20px; }
li { margin: 6px 0; }
a { color: #f0c36a; }
"""


def create_app(
    *,
    state_dir: str | Path | None = None,
    clock: Callable[[], float] | None = None,
) -> FastAPI:
    if os.environ.get("FF_ENV") == "production" and os.environ.get("FF_DEMO_HINTS") == "1":
        raise RuntimeError("FF_DEMO_HINTS=1 is refused when FF_ENV=production.")
    directory = Path(state_dir or os.environ.get("FF_STATE_DIR") or Path(".run") / "identity")
    directory.mkdir(parents=True, exist_ok=True)
    conn = connect(directory / "identity.sqlite3")
    seed(conn)
    private_pem, public_key, kid = load_or_create_key(directory)
    issuer = os.environ.get("FF_IDP_PUBLIC_URL", "http://127.0.0.1:8095").rstrip("/")
    demo_hints = os.environ.get("FF_DEMO_HINTS") == "1"
    filler = dummy_hash()
    lock = threading.Lock()
    now = clock or (lambda: __import__("time").time())

    app = FastAPI(title="Force Fab Identity", docs_url=None, redoc_url=None)
    app.state.conn = conn
    app.state.lock = lock
    app.state.directory = directory
    app.state.public_key = public_key
    app.state.kid = kid
    app.state.issuer = issuer
    app.state.clock = now

    @contextmanager
    def db() -> Iterator[Any]:
        with lock:
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    def append_event(event: dict[str, Any]) -> None:
        row = conn.execute("SELECT hash FROM auth_events ORDER BY seq DESC LIMIT 1").fetchone()
        prev = row["hash"] if row else ""
        body = json.dumps(event, sort_keys=True, separators=(",", ":"))
        digest = sha256_text(prev + body)
        conn.execute(
            "INSERT INTO auth_events(prev_hash, hash, body, created) VALUES (?, ?, ?, ?)",
            (prev, digest, body, now()),
        )

    def page(title: str, body: str, status: int = 200) -> HTMLResponse:
        doc = (
            "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<meta name='color-scheme' content='dark'>"
            f"<title>{escape(title)}</title><style>{_PAGE_STYLE}</style></head><body>"
            "<div class='page-bar' aria-hidden='true'></div>"
            "<header class='console-header'><span class='logo-word'>Force Fab <small>by TSM Corp.</small></span></header>"
            f"<main class='sheet'><section class='card'>{body}</section></main></body></html>"
        )
        return HTMLResponse(doc, status_code=status)

    def user_by_name(username: str):
        return conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

    def roles_for(user_id: int) -> list[str]:
        names = [row["role"] for row in conn.execute("SELECT role FROM user_roles WHERE user_id=?", (user_id,))]
        grants = conn.execute(
            "SELECT role, elevated_until FROM jit_grants WHERE user_id=? AND elevated_until>?",
            (user_id, now()),
        ).fetchall()
        for grant in grants:
            if grant["role"] not in names:
                names.append(grant["role"])
        return names

    def sites_for(user_id: int) -> list[str]:
        return [row["site"] for row in conn.execute("SELECT site FROM user_sites WHERE user_id=?", (user_id,))]

    def elevated_until(user_id: int) -> int | None:
        row = conn.execute(
            "SELECT MAX(elevated_until) AS until_ts FROM jit_grants WHERE user_id=? AND elevated_until>?",
            (user_id, now()),
        ).fetchone()
        if row and row["until_ts"]:
            return int(row["until_ts"])
        return None

    def client_row(client_id: str):
        return conn.execute("SELECT * FROM clients WHERE client_id=?", (client_id,)).fetchone()

    def redirects_of(row) -> list[str]:
        return list(json.loads(row["redirect_uris"]))

    def registered_origins() -> set[str]:
        origins: set[str] = set()
        for row in conn.execute("SELECT redirect_uris FROM clients"):
            for uri in json.loads(row["redirect_uris"]):
                parts = urlsplit(uri)
                origins.add(f"{parts.scheme}://{parts.netloc}")
        return origins

    def session_row(sid: str | None):
        if not sid:
            return None
        row = conn.execute("SELECT * FROM sessions WHERE sid=?", (sid,)).fetchone()
        if row is None or row["exp"] <= now():
            return None
        return row

    def decode_bearer(request: Request) -> dict[str, Any] | None:
        header = request.headers.get("authorization", "")
        if not header.lower().startswith("bearer "):
            return None
        token = header.split(" ", 1)[1].strip()
        try:
            payload = jwt_decode(token)
        except Exception:
            return None
        jti = str(payload.get("jti") or "")
        if jti and conn.execute("SELECT 1 FROM revoked_jti WHERE jti=?", (jti,)).fetchone():
            return None
        return payload

    def jwt_decode(token: str) -> dict[str, Any]:
        import jwt

        return jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=issuer,
            leeway=30,
            options={"verify_aud": False},
        )

    def authenticate_client(request: Request, form: dict[str, str]):
        client_id = ""
        secret = ""
        header = request.headers.get("authorization", "")
        if header.lower().startswith("basic "):
            try:
                raw = base64.b64decode(header.split(" ", 1)[1].strip()).decode("utf-8")
                client_id, secret = raw.split(":", 1)
            except (ValueError, UnicodeError):
                return None
        else:
            client_id = form.get("client_id", "")
            secret = form.get("client_secret", "")
        row = client_row(client_id)
        if row is None:
            check_password(secret or "x", filler)
            return None
        if not check_password(secret, row["secret_hash"]):
            return None
        return row

    def rate_limited(ip: str) -> bool:
        cutoff = now() - 60
        count = conn.execute(
            "SELECT COUNT(*) AS n FROM login_attempts WHERE ip=? AND at_ts>?",
            (ip, cutoff),
        ).fetchone()["n"]
        if count >= 20:
            return True
        conn.execute("INSERT INTO login_attempts(ip, at_ts) VALUES (?, ?)", (ip, now()))
        return False

    def client_ip(request: Request) -> str:
        if request.client is None:
            return "unknown"
        return request.client.host or "unknown"

    def mint_access(
        user,
        *,
        aud: str,
        acr: str,
        amr: list[str],
        auth_time: int,
        sid: str,
        break_glass: bool,
    ) -> str:
        stamp = int(now())
        roles = roles_for(user["id"])
        claims: dict[str, Any] = {
            "iss": issuer,
            "aud": aud,
            "sub": user["username"],
            "name": user["name"],
            "email": user["email"],
            "roles": roles,
            "sites": sites_for(user["id"]),
            "acr": acr,
            "amr": amr,
            "auth_time": auth_time,
            "sid": sid,
            "jti": secrets.token_hex(16),
            "iat": stamp,
            "exp": stamp + ACCESS_TTL,
        }
        until = elevated_until(user["id"])
        if until is not None:
            claims["elevated_until"] = until
        if break_glass or user["break_glass_until"] > now():
            claims["break_glass"] = True
        return sign_jwt(claims, private_pem, kid)

    def mint_id(user, *, aud: str, nonce: str, acr: str, auth_time: int, sid: str) -> str:
        stamp = int(now())
        claims = {
            "iss": issuer,
            "aud": aud,
            "sub": user["username"],
            "name": user["name"],
            "email": user["email"],
            "nonce": nonce,
            "acr": acr,
            "auth_time": auth_time,
            "sid": sid,
            "iat": stamp,
            "exp": stamp + ACCESS_TTL,
        }
        return sign_jwt(claims, private_pem, kid)

    def store_refresh(user_id: int, client_id: str, family_id: str, acr: str, amr: str, auth_time: int, sid: str, break_glass: bool) -> str:
        raw = secrets.token_urlsafe(32)
        conn.execute(
            """
            INSERT INTO refresh_tokens(
                token_hash, family_id, user_id, client_id, exp, used, revoked, acr, amr, auth_time, sid, break_glass
            ) VALUES (?, ?, ?, ?, ?, 0, 0, ?, ?, ?, ?, ?)
            """,
            (sha256_text(raw), family_id, user_id, client_id, now() + REFRESH_TTL, acr, amr, auth_time, sid, 1 if break_glass else 0),
        )
        return raw

    def revoke_family(family_id: str) -> None:
        conn.execute("UPDATE refresh_tokens SET revoked=1 WHERE family_id=?", (family_id,))

    def ensure_session(user, acr: str, amr: str, auth_time: int, break_glass: bool, sid: str | None = None) -> str:
        if sid:
            conn.execute(
                "UPDATE sessions SET acr=?, amr=?, auth_time=?, exp=?, break_glass=? WHERE sid=?",
                (acr, amr, auth_time, now() + SESSION_TTL, 1 if break_glass else 0, sid),
            )
            return sid
        sid = secrets.token_urlsafe(24)
        csrf = secrets.token_urlsafe(16)
        conn.execute(
            """
            INSERT INTO sessions(sid, user_id, csrf, acr, amr, auth_time, exp, break_glass)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (sid, user["id"], csrf, acr, amr, auth_time, now() + SESSION_TTL, 1 if break_glass else 0),
        )
        return sid

    def issue_code(request_row, user, acr: str, amr: str, auth_time: int, sid: str) -> RedirectResponse:
        raw = secrets.token_urlsafe(32)
        break_glass = 1 if user["break_glass_until"] > now() else 0
        conn.execute(
            """
            INSERT INTO auth_codes(
                code_hash, client_id, redirect_uri, user_id, nonce, code_challenge, exp, used, acr, amr, auth_time, sid, break_glass
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?)
            """,
            (
                sha256_text(raw),
                request_row["client_id"],
                request_row["redirect_uri"],
                user["id"],
                request_row["nonce"],
                request_row["code_challenge"],
                now() + CODE_TTL,
                acr,
                amr,
                auth_time,
                sid,
                break_glass,
            ),
        )
        query = urlencode({"code": raw, "state": request_row["state"]})
        target = request_row["redirect_uri"]
        sep = "&" if "?" in target else "?"
        response = RedirectResponse(f"{target}{sep}{query}", status_code=302)
        response.set_cookie("ffidp_session", sid, httponly=True, samesite="lax", path="/", max_age=SESSION_TTL)
        return response

    def token_bundle(user, client, *, nonce: str, acr: str, amr: str, auth_time: int, sid: str, family_id: str | None, break_glass: bool) -> dict[str, Any]:
        aud = client["token_aud"]
        access = mint_access(user, aud=aud, acr=acr, amr=amr.split(","), auth_time=auth_time, sid=sid, break_glass=break_glass)
        ident = mint_id(user, aud=aud, nonce=nonce, acr=acr, auth_time=auth_time, sid=sid)
        family = family_id or secrets.token_hex(16)
        refresh = store_refresh(user["id"], client["client_id"], family, acr, amr, auth_time, sid, break_glass or user["break_glass_until"] > now())
        return {
            "access_token": access,
            "id_token": ident,
            "refresh_token": refresh,
            "token_type": "Bearer",
            "expires_in": ACCESS_TTL,
        }

    def sod_blocked(user, role: str) -> bool:
        if user["username"] == "breakglass":
            return False
        current = {row["role"] for row in conn.execute("SELECT role FROM user_roles WHERE user_id=?", (user["id"],))}
        proposed = current | {role}
        return "FF-ADMIN" in proposed and "FF-AUDITOR" in proposed

    @app.get("/health")
    def health() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/.well-known/openid-configuration")
    def discovery() -> dict[str, Any]:
        return {
            "issuer": issuer,
            "authorization_endpoint": f"{issuer}/authorize",
            "token_endpoint": f"{issuer}/token",
            "userinfo_endpoint": f"{issuer}/userinfo",
            "jwks_uri": f"{issuer}/jwks.json",
            "revocation_endpoint": f"{issuer}/revoke",
            "end_session_endpoint": f"{issuer}/logout",
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code", "refresh_token", "client_credentials"],
            "code_challenge_methods_supported": ["S256"],
            "token_endpoint_auth_methods_supported": ["client_secret_basic", "client_secret_post"],
            "id_token_signing_alg_values_supported": ["RS256"],
        }

    @app.get("/jwks.json")
    def jwks() -> dict[str, Any]:
        return {"keys": [json_jwk(public_key, kid)]}

    @app.get("/authorize")
    def authorize_get(request: Request):
        params = request.query_params
        problem = _authorize_problem(params)
        if problem is not None:
            return problem
        client = client_row(params.get("client_id", ""))
        request_id = secrets.token_urlsafe(18)
        with db():
            conn.execute(
                """
                INSERT INTO auth_requests(
                    request_id, client_id, redirect_uri, state, nonce, code_challenge, acr_values, prompt, stage, exp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'login', ?)
                """,
                (
                    request_id,
                    client["client_id"],
                    params.get("redirect_uri"),
                    params.get("state"),
                    params.get("nonce"),
                    params.get("code_challenge"),
                    params.get("acr_values", ""),
                    params.get("prompt", ""),
                    now() + REQUEST_TTL,
                ),
            )
            session = session_row(request.cookies.get("ffidp_session"))
            prompt = params.get("prompt", "")
            if session is not None and prompt != "login":
                user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
                needs_mfa = "mfa" in params.get("acr_values", "")
                fresh = session["acr"] == "mfa" and (int(now()) - int(session["auth_time"])) <= STEP_UP_SECONDS
                if needs_mfa and not fresh:
                    if user["mfa_enrolled"]:
                        conn.execute(
                            "UPDATE auth_requests SET stage='otp', user_id=? WHERE request_id=?",
                            (user["id"], request_id),
                        )
                        return page("Force Fab Identity", _otp_form(request_id, user))
                    conn.execute(
                        "UPDATE auth_requests SET stage='enroll', user_id=? WHERE request_id=?",
                        (user["id"], request_id),
                    )
                    return page("Force Fab Identity", _enroll_form(request_id))
                row = conn.execute("SELECT * FROM auth_requests WHERE request_id=?", (request_id,)).fetchone()
                return issue_code(row, user, session["acr"], session["amr"], int(session["auth_time"]), session["sid"])
        return page("Force Fab Identity", _login_form(request_id, ""))

    def _authorize_problem(params) -> JSONResponse | None:
        if params.get("response_type") != "code":
            return JSONResponse({"error": "unsupported_response_type"}, status_code=400)
        if params.get("code_challenge_method") != "S256" or not params.get("code_challenge"):
            return JSONResponse({"error": "invalid_request", "error_description": "PKCE S256 is required."}, status_code=400)
        if not params.get("state") or not params.get("nonce"):
            return JSONResponse({"error": "invalid_request", "error_description": "state and nonce are required."}, status_code=400)
        client = client_row(params.get("client_id", ""))
        if client is None or params.get("redirect_uri") not in redirects_of(client):
            return JSONResponse({"error": "invalid_request", "error_description": "redirect_uri is not registered."}, status_code=400)
        return None

    def _login_form(request_id: str, message: str) -> str:
        note = f"<p class='notice' role='alert'>{escape(message)}</p>" if message else ""
        return (
            "<h1>Sign in</h1>"
            "<p class='lead'>Enter the login and password for this shift.</p>"
            f"{note}<form method='post' action='/authorize/continue'>"
            f"<input type='hidden' name='request_id' value='{escape(request_id)}'>"
            "<input type='hidden' name='stage' value='login'>"
            "<label>Login<input name='username' autocomplete='username' autocapitalize='none' spellcheck='false' autofocus></label>"
            "<label>Password<input type='password' name='password' autocomplete='current-password'></label>"
            "<button type='submit'>Sign in</button></form>"
        )

    def _otp_form(request_id: str, user) -> str:
        hint = ""
        if demo_hints and user is not None and user["mfa_secret"]:
            code = totp_at(user["mfa_secret"], int(now()))
            hint = f"<p class='hint'>Demo: current code {escape(code)}</p>"
        return (
            "<h1>One-time code</h1>"
            "<p class='lead'>Enter the six-digit code. A new code replaces it every 30 seconds.</p>"
            f"{hint}<form method='post' action='/authorize/continue'>"
            f"<input type='hidden' name='request_id' value='{escape(request_id)}'>"
            "<input type='hidden' name='stage' value='otp'>"
            "<label>One-time code<input name='otp' inputmode='numeric' autocomplete='one-time-code' autofocus></label>"
            "<button type='submit'>Continue</button></form>"
        )

    def _enroll_form(request_id: str) -> str:
        hint = ""
        if demo_hints:
            code = totp_at(DEMO_TOTP_SECRET, int(now()))
            hint = f"<p class='hint'>Demo: current code {escape(code)}</p>"
        return (
            "<h1>Set up the one-time code</h1>"
            "<p class='lead'>This login has no one-time code yet. Enrol one to continue.</p>"
            f"{hint}<form method='post' action='/authorize/continue'>"
            f"<input type='hidden' name='request_id' value='{escape(request_id)}'>"
            "<input type='hidden' name='stage' value='enroll'>"
            "<label>One-time code<input name='otp' inputmode='numeric' autocomplete='one-time-code' autofocus></label>"
            "<button type='submit'>Enrol</button></form>"
        )

    @app.post("/authorize/continue")
    async def authorize_continue(request: Request):
        form = dict(await request.form())
        request_id = str(form.get("request_id") or "")
        stage = str(form.get("stage") or "")
        ip = client_ip(request)
        with db():
            if rate_limited(ip):
                return JSONResponse(
                    {"error": "rate_limited", "message": "Too many sign-in attempts from this address."},
                    status_code=429,
                    headers={"Retry-After": "60"},
                )
            row = conn.execute("SELECT * FROM auth_requests WHERE request_id=?", (request_id,)).fetchone()
            if row is None or row["exp"] <= now():
                return page("Force Fab Identity", "<p>This sign-in request expired.</p>", status=400)
            if stage == "login":
                return _password_stage(row, str(form.get("username") or "").strip(), str(form.get("password") or ""))
            if stage == "otp":
                return _otp_stage(row, str(form.get("otp") or ""))
            if stage == "enroll":
                return _enroll_stage(row, str(form.get("otp") or ""))
        return page("Force Fab Identity", "<p>This sign-in step is unknown.</p>", status=400)

    def _password_stage(row, username: str, password: str):
        user = user_by_name(username)
        if user is None or not user["active"]:
            check_password(password or "x", filler)
            append_event({"type": "login_fail", "username": username})
            return page("Force Fab Identity", _login_form(row["request_id"], "Sign-in failed."), status=401)
        if user["locked_until"] > now():
            check_password(password, user["password_hash"])
            append_event({"type": "login_fail", "username": username, "locked": True})
            return page("Force Fab Identity", _login_form(row["request_id"], "This account is locked."), status=401)
        if not check_password(password, user["password_hash"]):
            failed = int(user["failed_count"]) + 1
            if failed >= 5:
                strikes = int(user["lock_strikes"]) + 1
                minutes = 15 * (2 ** (strikes - 1))
                conn.execute(
                    "UPDATE users SET failed_count=0, lock_strikes=?, locked_until=? WHERE id=?",
                    (strikes, now() + minutes * 60, user["id"]),
                )
            else:
                conn.execute("UPDATE users SET failed_count=? WHERE id=?", (failed, user["id"]))
            append_event({"type": "login_fail", "username": username})
            return page("Force Fab Identity", _login_form(row["request_id"], "Sign-in failed."), status=401)
        conn.execute("UPDATE users SET failed_count=0 WHERE id=?", (user["id"],))
        append_event({"type": "login_ok", "username": username})
        needs_mfa = "mfa" in (row["acr_values"] or "") or bool(user["mfa_enrolled"])
        if user["mfa_enrolled"] and needs_mfa:
            conn.execute(
                "UPDATE auth_requests SET stage='otp', user_id=? WHERE request_id=?",
                (user["id"], row["request_id"]),
            )
            return page("Force Fab Identity", _otp_form(row["request_id"], user))
        if "mfa" in (row["acr_values"] or "") and not user["mfa_enrolled"]:
            conn.execute(
                "UPDATE auth_requests SET stage='enroll', user_id=? WHERE request_id=?",
                (user["id"], row["request_id"]),
            )
            return page("Force Fab Identity", _enroll_form(row["request_id"]))
        auth_time = int(now())
        sid = ensure_session(user, "pwd", "pwd", auth_time, user["break_glass_until"] > now())
        fresh = conn.execute("SELECT * FROM auth_requests WHERE request_id=?", (row["request_id"],)).fetchone()
        return issue_code(fresh, user, "pwd", "pwd", auth_time, sid)

    def _consume_code(user, code: str, secret: str) -> bool:
        if not totp_ok(secret, code, now()):
            return False
        step = current_step(now())
        seen = conn.execute(
            "SELECT 1 FROM totp_steps WHERE user_id=? AND step=?",
            (user["id"], step),
        ).fetchone()
        if seen:
            return False
        conn.execute("INSERT INTO totp_steps(user_id, step) VALUES (?, ?)", (user["id"], step))
        return True

    def _otp_stage(row, code: str):
        user = conn.execute("SELECT * FROM users WHERE id=?", (row["user_id"],)).fetchone()
        if user is None or not _consume_code(user, code, user["mfa_secret"] or ""):
            append_event({"type": "mfa_fail", "username": user["username"] if user else ""})
            return page("Force Fab Identity", _otp_form(row["request_id"], user) + "<p>That code was rejected.</p>", status=401)
        append_event({"type": "mfa_ok", "username": user["username"]})
        auth_time = int(now())
        existing = session_row(None)
        sid = ensure_session(user, "mfa", "pwd,otp", auth_time, user["break_glass_until"] > now())
        fresh = conn.execute("SELECT * FROM auth_requests WHERE request_id=?", (row["request_id"],)).fetchone()
        return issue_code(fresh, user, "mfa", "pwd,otp", auth_time, sid)

    def _enroll_stage(row, code: str):
        user = conn.execute("SELECT * FROM users WHERE id=?", (row["user_id"],)).fetchone()
        if user is None or not totp_ok(DEMO_TOTP_SECRET, code, now()):
            append_event({"type": "mfa_fail", "username": user["username"] if user else ""})
            return page("Force Fab Identity", _enroll_form(row["request_id"]) + "<p>That code was rejected.</p>", status=401)
        conn.execute(
            "UPDATE users SET mfa_secret=?, mfa_enrolled=1 WHERE id=?",
            (DEMO_TOTP_SECRET, user["id"]),
        )
        user = conn.execute("SELECT * FROM users WHERE id=?", (user["id"],)).fetchone()
        if not _consume_code(user, code, DEMO_TOTP_SECRET):
            return page("Force Fab Identity", _enroll_form(row["request_id"]) + "<p>That code was rejected.</p>", status=401)
        append_event({"type": "mfa_ok", "username": user["username"], "enrolled": True})
        auth_time = int(now())
        sid = ensure_session(user, "mfa", "pwd,otp", auth_time, False)
        fresh = conn.execute("SELECT * FROM auth_requests WHERE request_id=?", (row["request_id"],)).fetchone()
        return issue_code(fresh, user, "mfa", "pwd,otp", auth_time, sid)

    @app.post("/token")
    async def token(request: Request):
        form = {key: str(value) for key, value in (await request.form()).items()}
        with db():
            client = authenticate_client(request, form)
            if client is None:
                return JSONResponse({"error": "invalid_client"}, status_code=401)
            grant = form.get("grant_type", "")
            if grant == "authorization_code":
                return _code_grant(client, form)
            if grant == "refresh_token":
                return _refresh_grant(client, form)
            if grant == "client_credentials":
                return _client_grant(client)
        return JSONResponse({"error": "unsupported_grant_type"}, status_code=400)

    def _code_grant(client, form: dict[str, str]):
        raw = form.get("code", "")
        row = conn.execute("SELECT * FROM auth_codes WHERE code_hash=?", (sha256_text(raw),)).fetchone()
        if row is None or row["used"] or row["exp"] <= now() or row["client_id"] != client["client_id"]:
            return JSONResponse({"error": "invalid_grant"}, status_code=400)
        if form.get("redirect_uri") != row["redirect_uri"]:
            return JSONResponse({"error": "invalid_grant", "error_description": "redirect_uri does not match."}, status_code=400)
        verifier = form.get("code_verifier", "")
        if len(verifier) < 43 or len(verifier) > 128 or not hashes_equal(pkce_challenge(verifier), row["code_challenge"]):
            conn.execute("UPDATE auth_codes SET used=1 WHERE code_hash=?", (row["code_hash"],))
            return JSONResponse({"error": "invalid_grant", "error_description": "PKCE verifier was rejected."}, status_code=400)
        conn.execute("UPDATE auth_codes SET used=1 WHERE code_hash=?", (row["code_hash"],))
        user = conn.execute("SELECT * FROM users WHERE id=?", (row["user_id"],)).fetchone()
        bundle = token_bundle(
            user,
            client,
            nonce=row["nonce"],
            acr=row["acr"],
            amr=row["amr"],
            auth_time=int(row["auth_time"]),
            sid=row["sid"],
            family_id=None,
            break_glass=bool(row["break_glass"]),
        )
        return JSONResponse(bundle)

    def _refresh_grant(client, form: dict[str, str]):
        raw = form.get("refresh_token", "")
        row = conn.execute("SELECT * FROM refresh_tokens WHERE token_hash=?", (sha256_text(raw),)).fetchone()
        if row is None or row["client_id"] != client["client_id"]:
            return JSONResponse({"error": "invalid_grant"}, status_code=400)
        if row["used"] or row["revoked"] or row["exp"] <= now():
            revoke_family(row["family_id"])
            append_event({"type": "refresh_reuse", "family_id": row["family_id"], "client_id": client["client_id"]})
            return JSONResponse({"error": "invalid_grant", "error_description": "Refresh token reuse revoked the family."}, status_code=400)
        conn.execute("UPDATE refresh_tokens SET used=1 WHERE token_hash=?", (row["token_hash"],))
        user = conn.execute("SELECT * FROM users WHERE id=?", (row["user_id"],)).fetchone()
        bundle = token_bundle(
            user,
            client,
            nonce="",
            acr=row["acr"],
            amr=row["amr"],
            auth_time=int(row["auth_time"]),
            sid=row["sid"],
            family_id=row["family_id"],
            break_glass=bool(row["break_glass"]),
        )
        return JSONResponse(bundle)

    def _client_grant(client):
        if client["client_type"] != "client_credentials":
            return JSONResponse({"error": "unauthorized_client"}, status_code=400)
        stamp = int(now())
        role = "SCIM" if client["client_id"] == "force-fab-scim" else "SVC"
        claims = {
            "iss": issuer,
            "aud": client["token_aud"],
            "sub": client["client_id"],
            "roles": [role],
            "acr": "pwd",
            "amr": ["client"],
            "auth_time": stamp,
            "jti": secrets.token_hex(16),
            "iat": stamp,
            "exp": stamp + ACCESS_TTL,
        }
        return JSONResponse(
            {
                "access_token": sign_jwt(claims, private_pem, kid),
                "token_type": "Bearer",
                "expires_in": ACCESS_TTL,
            }
        )

    @app.get("/userinfo")
    def userinfo(request: Request):
        with db():
            payload = decode_bearer(request)
        if payload is None:
            return JSONResponse({"error": "invalid_token"}, status_code=401)
        return {
            "sub": payload.get("sub"),
            "name": payload.get("name"),
            "email": payload.get("email"),
            "roles": payload.get("roles") or [],
            "sites": payload.get("sites") or [],
        }

    @app.post("/revoke")
    async def revoke(request: Request):
        form = {key: str(value) for key, value in (await request.form()).items()}
        with db():
            client = authenticate_client(request, form)
            if client is None:
                return JSONResponse({"error": "invalid_client"}, status_code=401)
            raw = form.get("token", "")
            row = conn.execute("SELECT * FROM refresh_tokens WHERE token_hash=?", (sha256_text(raw),)).fetchone()
            if row is not None:
                revoke_family(row["family_id"])
            else:
                try:
                    payload = jwt_decode(raw)
                except Exception:
                    payload = None
                if payload and payload.get("jti"):
                    conn.execute("INSERT OR IGNORE INTO revoked_jti(jti) VALUES (?)", (payload["jti"],))
        return Response(status_code=200)

    @app.get("/logout")
    def logout(request: Request, post_logout_redirect_uri: str = ""):
        parts = urlsplit(post_logout_redirect_uri)
        origin = f"{parts.scheme}://{parts.netloc}"
        with db():
            if origin not in registered_origins():
                return JSONResponse({"error": "invalid_request", "error_description": "Logout redirect is not a registered app origin."}, status_code=400)
            sid = request.cookies.get("ffidp_session")
            if sid:
                conn.execute("DELETE FROM sessions WHERE sid=?", (sid,))
                append_event({"type": "logout", "sid": sid})
        response = RedirectResponse(post_logout_redirect_uri, status_code=302)
        response.delete_cookie("ffidp_session", path="/")
        return response

    def bearer_user(request: Request, *, write: bool):
        payload = decode_bearer(request)
        if payload is None:
            return None, JSONResponse({"ok": False, "error_class": "unauthenticated", "message": "Sign in is required."}, status_code=401)
        roles = set(payload.get("roles") or [])
        if write and "FF-ADMIN" not in roles:
            return None, JSONResponse({"ok": False, "error_class": "forbidden", "message": "FF-ADMIN is required."}, status_code=403)
        if not write and not ({"FF-ADMIN", "FF-AUDITOR"} & roles):
            return None, JSONResponse({"ok": False, "error_class": "forbidden", "message": "FF-ADMIN or FF-AUDITOR is required."}, status_code=403)
        user = user_by_name(str(payload.get("sub") or ""))
        if user is None:
            return None, JSONResponse({"ok": False, "error_class": "forbidden", "message": "This token has no user."}, status_code=403)
        return user, None

    @app.get("/api/admin/users")
    def admin_users(request: Request):
        with db():
            user, error = bearer_user(request, write=False)
            if error is not None:
                return error
            rows = []
            for item in conn.execute("SELECT * FROM users ORDER BY username"):
                rows.append(
                    {
                        "username": item["username"],
                        "name": item["name"],
                        "active": bool(item["active"]),
                        "roles": roles_for(item["id"]),
                        "sites": sites_for(item["id"]),
                        "mfa_enrolled": bool(item["mfa_enrolled"]),
                    }
                )
        return {"ok": True, "users": rows}

    @app.post("/api/admin/users")
    async def admin_create_user(request: Request):
        body = await request.json()
        with db():
            actor, error = bearer_user(request, write=True)
            if error is not None:
                return error
            username = str(body.get("username") or "").strip()
            password = str(body.get("password") or "")
            enrolled = bool(body.get("mfa_enrolled"))
            problem = password_problem(password, mfa_enrolled=enrolled)
            if not username or user_by_name(username) is not None:
                return JSONResponse({"ok": False, "message": "Choose a new login."}, status_code=400)
            if problem:
                return JSONResponse({"ok": False, "message": problem}, status_code=400)
            secret = DEMO_TOTP_SECRET if enrolled else None
            conn.execute(
                """
                INSERT INTO users(username, name, email, password_hash, active, mfa_secret, mfa_enrolled)
                VALUES (?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    username,
                    str(body.get("name") or username),
                    f"{username}@force-fab.local",
                    hash_password(password),
                    secret,
                    1 if enrolled else 0,
                ),
            )
            append_event({"type": "admin_create_user", "username": username, "actor": actor["username"]})
        return {"ok": True, "username": username}

    @app.post("/api/admin/users/{username}/roles")
    async def admin_assign_role(username: str, request: Request):
        body = await request.json()
        role = str(body.get("role") or "")
        with db():
            actor, error = bearer_user(request, write=True)
            if error is not None:
                return error
            user = user_by_name(username)
            known = conn.execute("SELECT 1 FROM roles WHERE name=?", (role,)).fetchone()
            if user is None or known is None:
                return JSONResponse({"ok": False, "message": "User or role was not found."}, status_code=404)
            if sod_blocked(user, role):
                return JSONResponse(
                    {"ok": False, "error_class": "sod_violation", "message": "One user cannot hold both FF-ADMIN and FF-AUDITOR."},
                    status_code=409,
                )
            conn.execute("INSERT OR IGNORE INTO user_roles(user_id, role) VALUES (?, ?)", (user["id"], role))
            append_event({"type": "role_assign", "username": username, "role": role, "actor": actor["username"]})
        return {"ok": True}

    @app.post("/api/admin/users/{username}/disable")
    def admin_disable(username: str, request: Request):
        with db():
            actor, error = bearer_user(request, write=True)
            if error is not None:
                return error
            user = user_by_name(username)
            if user is None:
                return JSONResponse({"ok": False, "message": "User was not found."}, status_code=404)
            conn.execute("UPDATE users SET active=0 WHERE id=?", (user["id"],))
            append_event({"type": "user_disabled", "username": username, "actor": actor["username"]})
        return {"ok": True}

    @app.post("/api/admin/users/{username}/enable")
    def admin_enable(username: str, request: Request):
        with db():
            _actor, error = bearer_user(request, write=True)
            if error is not None:
                return error
            conn.execute("UPDATE users SET active=1 WHERE username=?", (username,))
        return {"ok": True}

    @app.get("/api/admin/sessions")
    def admin_sessions(request: Request):
        with db():
            _user, error = bearer_user(request, write=False)
            if error is not None:
                return error
            rows = []
            for item in conn.execute(
                """
                SELECT sessions.sid, users.username, sessions.exp, sessions.acr
                FROM sessions JOIN users ON users.id = sessions.user_id
                """
            ):
                rows.append({"sid": item["sid"], "username": item["username"], "exp": item["exp"], "acr": item["acr"]})
        return {"ok": True, "sessions": rows}

    @app.post("/api/admin/sessions/{sid}/revoke")
    def admin_revoke_session(sid: str, request: Request):
        with db():
            _actor, error = bearer_user(request, write=True)
            if error is not None:
                return error
            conn.execute("DELETE FROM sessions WHERE sid=?", (sid,))
        return {"ok": True}

    @app.post("/api/admin/jit")
    async def jit_request(request: Request):
        body = await request.json()
        with db():
            payload = decode_bearer(request)
            if payload is None:
                return JSONResponse({"ok": False, "error_class": "unauthenticated", "message": "Sign in is required."}, status_code=401)
            actor = user_by_name(str(payload.get("sub") or ""))
            if actor is None or not actor["active"]:
                return JSONResponse({"ok": False, "error_class": "forbidden", "message": "This token has no user."}, status_code=403)
            minutes = int(body.get("minutes") or 0)
            role = str(body.get("role") or "")
            reason = str(body.get("reason") or "").strip()
            if minutes < 1 or minutes > 240 or not reason:
                return JSONResponse({"ok": False, "message": "Minutes must be 1 to 240, with a reason."}, status_code=400)
            if conn.execute("SELECT 1 FROM roles WHERE name=?", (role,)).fetchone() is None:
                return JSONResponse({"ok": False, "message": "Role was not found."}, status_code=404)
            cur = conn.execute(
                """
                INSERT INTO jit_requests(user_id, role, minutes, reason, status, created)
                VALUES (?, ?, ?, ?, 'pending', ?)
                """,
                (actor["id"], role, minutes, reason, now()),
            )
            request_pk = int(cur.lastrowid)
            append_event({"type": "jit_request", "username": actor["username"], "role": role})
        return {"ok": True, "id": request_pk, "status": "pending"}

    @app.post("/api/admin/jit/{request_id}/approve")
    def jit_approve(request_id: int, request: Request):
        with db():
            actor, error = bearer_user(request, write=True)
            if error is not None:
                return error
            item = conn.execute("SELECT * FROM jit_requests WHERE id=?", (request_id,)).fetchone()
            if item is None or item["status"] != "pending":
                return JSONResponse({"ok": False, "message": "This request is not pending."}, status_code=404)
            if item["user_id"] == actor["id"]:
                return JSONResponse(
                    {"ok": False, "error_class": "self_approve", "message": "A different admin must approve this request."},
                    status_code=403,
                )
            until = now() + int(item["minutes"]) * 60
            conn.execute(
                "UPDATE jit_requests SET status='approved', approver_id=? WHERE id=?",
                (actor["id"], item["id"]),
            )
            conn.execute(
                "INSERT INTO jit_grants(user_id, role, elevated_until) VALUES (?, ?, ?)",
                (item["user_id"], item["role"], until),
            )
            append_event({"type": "elevation", "request_id": item["id"], "role": item["role"], "actor": actor["username"]})
        return {"ok": True, "elevated_until": until}

    @app.post("/api/admin/break-glass")
    async def break_glass(request: Request):
        body = await request.json()
        with db():
            actor, error = bearer_user(request, write=False)
            if error is not None:
                return error
            if actor["username"] != "breakglass":
                return JSONResponse({"ok": False, "message": "Only the breakglass login can activate this."}, status_code=403)
            minutes = int(body.get("minutes") or 0)
            reason = str(body.get("reason") or "").strip()
            if minutes < 1 or minutes > 60 or not reason:
                return JSONResponse({"ok": False, "message": "Break-glass is 60 minutes or fewer, with a reason."}, status_code=400)
            until = now() + minutes * 60
            conn.execute("UPDATE users SET break_glass_until=? WHERE id=?", (until, actor["id"]))
            append_event({"type": "break_glass", "severity": "critical", "username": actor["username"], "reason": reason, "until": until})
        return {"ok": True, "break_glass_until": until}

    @app.post("/api/admin/reviews")
    async def create_review(request: Request):
        body = await request.json()
        with db():
            actor, error = bearer_user(request, write=True)
            if error is not None:
                return error
            name = str(body.get("name") or "").strip()
            if not name:
                return JSONResponse({"ok": False, "message": "Name the review."}, status_code=400)
            cur = conn.execute("INSERT INTO access_reviews(name, created) VALUES (?, ?)", (name, now()))
            review_id = cur.lastrowid
            pairs = conn.execute("SELECT user_id, role FROM user_roles").fetchall()
            for pair in pairs:
                conn.execute(
                    "INSERT INTO review_items(review_id, user_id, role) VALUES (?, ?, ?)",
                    (review_id, pair["user_id"], pair["role"]),
                )
            append_event({"type": "access_review", "review_id": review_id, "actor": actor["username"]})
        return {"ok": True, "id": review_id, "items": len(pairs)}

    @app.get("/api/admin/reviews/{review_id}")
    def get_review(review_id: int, request: Request):
        with db():
            _actor, error = bearer_user(request, write=False)
            if error is not None:
                return error
            items = []
            for item in conn.execute(
                """
                SELECT review_items.id, users.username, review_items.role, review_items.decision, review_items.comment
                FROM review_items JOIN users ON users.id = review_items.user_id
                WHERE review_items.review_id=?
                """,
                (review_id,),
            ):
                items.append(dict(item))
        return {"ok": True, "items": items}

    @app.post("/api/admin/reviews/{review_id}/items/{item_id}")
    async def decide_review_item(review_id: int, item_id: int, request: Request):
        body = await request.json()
        decision = str(body.get("decision") or "")
        comment = str(body.get("comment") or "")
        if decision not in {"certify", "revoke"} or not comment.strip():
            return JSONResponse({"ok": False, "message": "Decision is certify or revoke, with a comment."}, status_code=400)
        with db():
            actor, error = bearer_user(request, write=True)
            if error is not None:
                return error
            item = conn.execute(
                "SELECT * FROM review_items WHERE id=? AND review_id=?",
                (item_id, review_id),
            ).fetchone()
            if item is None:
                return JSONResponse({"ok": False, "message": "Item was not found."}, status_code=404)
            conn.execute(
                "UPDATE review_items SET decision=?, comment=? WHERE id=?",
                (decision, comment, item_id),
            )
            if decision == "revoke":
                conn.execute(
                    "DELETE FROM user_roles WHERE user_id=? AND role=?",
                    (item["user_id"], item["role"]),
                )
            append_event({"type": "review_decision", "item_id": item_id, "decision": decision, "actor": actor["username"]})
        return {"ok": True}

    @app.get("/api/admin/reviews/{review_id}/export.csv")
    def export_review(review_id: int, request: Request):
        with db():
            _actor, error = bearer_user(request, write=False)
            if error is not None:
                return error
            lines = ["username,role,decision,comment"]
            for item in conn.execute(
                """
                SELECT users.username, review_items.role, review_items.decision, review_items.comment
                FROM review_items JOIN users ON users.id = review_items.user_id
                WHERE review_items.review_id=?
                """,
                (review_id,),
            ):
                lines.append(",".join(_csv_cell(item[name]) for name in ("username", "role", "decision", "comment")))
        return Response("\n".join(lines) + "\n", media_type="text/csv")

    @app.get("/api/admin/audit/verify")
    def verify_audit(request: Request):
        with db():
            _actor, error = bearer_user(request, write=False)
            if error is not None:
                return error
            prev = ""
            for row in conn.execute("SELECT seq, prev_hash, hash, body FROM auth_events ORDER BY seq"):
                expect = sha256_text(prev + row["body"])
                if row["prev_hash"] != prev or row["hash"] != expect:
                    return {"ok": False, "broken_at": row["seq"]}
                prev = row["hash"]
            count = conn.execute("SELECT COUNT(*) AS n FROM auth_events").fetchone()["n"]
        return {"ok": True, "length": count}

    def scim_actor(request: Request):
        payload = decode_bearer(request)
        if payload is None:
            return None
        roles = set(payload.get("roles") or [])
        if "SCIM" in roles or "FF-ADMIN" in roles or payload.get("sub") == "force-fab-scim":
            return payload
        return None

    def scim_user(row) -> dict[str, Any]:
        return {
            "id": row["username"],
            "userName": row["username"],
            "active": bool(row["active"]),
            "name": {"formatted": row["name"]},
            "roles": [{"value": role} for role in roles_for(row["id"])],
        }

    @app.get("/scim/v2/Users")
    def scim_list(request: Request, filter: str = ""):
        with db():
            if scim_actor(request) is None:
                return JSONResponse({"detail": "forbidden"}, status_code=403)
            username = ""
            if filter:
                import re

                match = re.search(r'userName eq "([^"]+)"', filter)
                if match is None:
                    return JSONResponse({"detail": "filter is unsupported"}, status_code=400)
                username = match.group(1)
            if username:
                rows = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM users ORDER BY username").fetchall()
            resources = [scim_user(row) for row in rows]
        return {"Resources": resources, "totalResults": len(resources)}

    @app.get("/scim/v2/Users/{username}")
    def scim_get(username: str, request: Request):
        with db():
            if scim_actor(request) is None:
                return JSONResponse({"detail": "forbidden"}, status_code=403)
            row = user_by_name(username)
            if row is None:
                return JSONResponse({"detail": "not found"}, status_code=404)
            return scim_user(row)

    @app.post("/scim/v2/Users")
    async def scim_create(request: Request):
        body = await request.json()
        with db():
            if scim_actor(request) is None:
                return JSONResponse({"detail": "forbidden"}, status_code=403)
            username = str(body.get("userName") or "").strip()
            name = str((body.get("name") or {}).get("formatted") or username)
            password = str(body.get("password") or "")
            problem = password_problem(password, mfa_enrolled=False)
            if not username or user_by_name(username) is not None or problem:
                return JSONResponse({"detail": problem or "invalid user"}, status_code=400)
            conn.execute(
                """
                INSERT INTO users(username, name, email, password_hash, active, mfa_enrolled)
                VALUES (?, ?, ?, ?, 1, 0)
                """,
                (username, name, f"{username}@force-fab.local", hash_password(password)),
            )
            append_event({"type": "scim_change", "action": "create", "username": username})
            row = user_by_name(username)
        return JSONResponse(scim_user(row), status_code=201)

    @app.patch("/scim/v2/Users/{username}")
    async def scim_patch(username: str, request: Request):
        body = await request.json()
        with db():
            if scim_actor(request) is None:
                return JSONResponse({"detail": "forbidden"}, status_code=403)
            user = user_by_name(username)
            if user is None:
                return JSONResponse({"detail": "not found"}, status_code=404)
            for op in body.get("Operations") or []:
                path = str(op.get("path") or "")
                value = op.get("value")
                if path == "active":
                    conn.execute("UPDATE users SET active=? WHERE id=?", (1 if value else 0, user["id"]))
                elif path == "roles":
                    names = []
                    for item in value or []:
                        names.append(item.get("value") if isinstance(item, dict) else str(item))
                    if "FF-ADMIN" in names and "FF-AUDITOR" in names and user["username"] != "breakglass":
                        return JSONResponse({"detail": "sod_violation"}, status_code=409)
                    conn.execute("DELETE FROM user_roles WHERE user_id=?", (user["id"],))
                    for role in names:
                        conn.execute("INSERT INTO user_roles(user_id, role) VALUES (?, ?)", (user["id"], role))
            append_event({"type": "scim_change", "action": "patch", "username": username})
            user = user_by_name(username)
        return scim_user(user)

    @app.delete("/scim/v2/Users/{username}")
    def scim_delete(username: str, request: Request):
        with db():
            if scim_actor(request) is None:
                return JSONResponse({"detail": "forbidden"}, status_code=403)
            user = user_by_name(username)
            if user is None:
                return JSONResponse({"detail": "not found"}, status_code=404)
            conn.execute("UPDATE users SET active=0 WHERE id=?", (user["id"],))
            append_event({"type": "scim_change", "action": "deactivate", "username": username})
        return Response(status_code=204)

    @app.get("/scim/v2/Groups")
    def scim_groups(request: Request):
        with db():
            if scim_actor(request) is None:
                return JSONResponse({"detail": "forbidden"}, status_code=403)
            resources = [{"id": row["name"], "displayName": row["name"]} for row in conn.execute("SELECT name FROM roles ORDER BY name")]
        return {"Resources": resources, "totalResults": len(resources)}

    @app.get("/admin")
    def admin_home(request: Request):
        with db():
            session = session_row(request.cookies.get("ffidp_session"))
            if session is None:
                return page("Force Fab Identity", "<p>Sign in before opening the admin console.</p>", status=401)
            user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
            if "FF-ADMIN" not in roles_for(user["id"]) and "FF-AUDITOR" not in roles_for(user["id"]):
                return page("Force Fab Identity", "<p>This console is for FF-ADMIN and FF-AUDITOR.</p>", status=403)
            read_only = "FF-ADMIN" not in roles_for(user["id"])
            users = conn.execute("SELECT username, active FROM users ORDER BY username").fetchall()
            items = "".join(f"<li>{escape(item['username'])} {'active' if item['active'] else 'disabled'}</li>" for item in users)
            form = ""
            if not read_only:
                form = (
                    "<form method='post' action='/admin/users/disable'>"
                    f"<input type='hidden' name='csrf' value='{escape(session['csrf'])}'>"
                    "<label>Login <input name='username'></label> "
                    "<button type='submit'>Disable</button></form>"
                )
        return page("Force Fab Identity", f"<p>Users</p><ul>{items}</ul>{form}<p><a href='/admin/events'>Events</a></p>")

    @app.post("/admin/users/disable")
    async def admin_form_disable(request: Request):
        form = dict(await request.form())
        with db():
            session = session_row(request.cookies.get("ffidp_session"))
            if session is None or not hashes_equal(str(form.get("csrf") or ""), session["csrf"]):
                return page("Force Fab Identity", "<p>The form token did not match.</p>", status=403)
            user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
            if "FF-ADMIN" not in roles_for(user["id"]):
                return page("Force Fab Identity", "<p>FF-ADMIN is required.</p>", status=403)
            target = str(form.get("username") or "")
            conn.execute("UPDATE users SET active=0 WHERE username=?", (target,))
        return RedirectResponse("/admin", status_code=303)

    @app.get("/admin/events")
    def admin_events(request: Request):
        with db():
            session = session_row(request.cookies.get("ffidp_session"))
            if session is None:
                return page("Force Fab Identity", "<p>Sign in before opening events.</p>", status=401)
            rows = conn.execute("SELECT seq, body FROM auth_events ORDER BY seq").fetchall()
            items = "".join(f"<li>{item['seq']}: {escape(item['body'])}</li>" for item in rows)
        return page("Force Fab Identity", f"<ul>{items}</ul>")

    return app


def _csv_cell(value: Any) -> str:
    text = "" if value is None else str(value)
    if text[:1] in "=+-@":
        text = "'" + text
    if any(ch in text for ch in '",\n'):
        return '"' + text.replace('"', '""') + '"'
    return text
