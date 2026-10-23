# Force Fab — Enhancements Replication Guide

**Audience:** the owner of the base capstone repo (FabPulse Sprint 4, App A + App B).
**Purpose:** describe every enhancement made on our side so they can be rebuilt in your repo, with your own tooling and model provider.
**What this is not:** a code drop. This guide gives specifications — behaviour, endpoints, data rules, UI and acceptance tests. Wherever a step needs an AI model, it says *your model client*; use whichever provider your repo already uses.

**Base we started from:** your repo as cloned on 2026-10-20, most likely commit `09b1e93` ("After applying B_soft motif and creating presentation"). We did not confirm the exact commit.
Your commit `62ecefd` ("Bug fix in Scenario-2 for Recipe Mismatch" — `demo_session.py`, `identity.py`, `docs/42-executive/scenario-demo-scripts.md` and tests) appears to be missing from our copy; that doc is not in our tree. Keep your fix, and where §3 rewrites identity, carry it forward.

---

## 0. Summary of enhancements

| # | Enhancement | Why it matters (guideline) |
|---|---|---|
| 1 | Product rename to **Force Fab** (user-visible only), "by B_soft" co-brand kept | Branding (G15) |
| 2 | **Force Fab Identity** — local OIDC identity provider (new service, port 8095) | Production-grade access (G5, G11) |
| 3 | Apps authenticate through the IdP (server-side session, signed tokens, e-signatures, site access) | Role-based experience, controls (G5, G11) |
| 4 | Platform hardening: security headers, CORS lockdown, rate limit, health/readiness/metrics, tracing | Operations (G13) |
| 5 | New business feature API (dashboard, cases, inbox, genealogy, SPC, partners, audit, glossary, knowledge graph, KPIs, faults) | No half-built prototype (G5), explainability (G7), semantic layer (G8), A vs B (G14) |
| 6 | AI safety controls: per-user token budget, recipe-value masking, write-once replay evidence | OWASP LLM Top 10 |
| 7 | "Ask Force Fab AI" panel + source badge on every answer | Visible AI difference between A and B (G4) |
| 8 | New UI shell with left navigation and 12 pages, shared by both apps | Enterprise UI (G5) |
| 9 | One dark theme (NVIDIA / Foxconn / AMD-inspired tokens), distinct accent per app, WCAG 2.2 AA | Branding, accessibility |
| 10 | Native one-click launcher (no Docker) | Demo reliability |
| 11 | Tests: +130 (identity, auth, features, ask, theme contrast) | Evidence (G12) |

Result on our side: **347 passed, 7 skipped, 7 failed**. The 7 are environment-only failures that already existed (OPA binary not installed, container bind-mount files, a demo-key file, container-only `/api/recovery` mount).

---

## 1. Rename to Force Fab (user-visible only)

- **Change only text people see.** Do not rename folders, env variables, compose service names, database files or `FABPULSE_API_KEY`; existing tests assert on those.
- **Titles:**
  - App A: `Force Fab · Application A — AI-transformed`
  - App B: `Force Fab · Application B — Context Lake`
  - IdP: `Force Fab Identity`
- **Where to change them:** both `ui/index.html` `<title>`, the header wordmark, launcher window titles, README and deck title.
- **Header:** wordmark **Force Fab**, followed by small text **by B_soft** (keep `className="logo-word"`, text only, no `<img>`, because guideline 15 requires B_soft branding and your presenter test checks it).

**Acceptance:** no "FabPulse" in any built UI file, page title or IdP page.

---

## 2. Force Fab Identity — local OIDC identity provider

A new service, port **8095**, started **before** the apps. It is a production-shaped mock IdP with dummy users. In production you would swap it for the corporate IdP using the same OIDC contract.

### 2.1 Storage
SQLite in a state folder (`FF_STATE_DIR`, default `.run/identity/`). Tables:
- users, roles, user_roles, user_sites
- clients
- auth_codes, sessions, refresh_tokens (with `family_id`, `used`, `revoked`)
- jit_requests
- access_reviews and review items
- auth_events (hash-chained, §2.6)

### 2.2 Keys and tokens
- **Signing key:** RSA 2048, generated on first start, saved as `signing_key.pem` (permissions 0600), with a `kid`. JWKS served at `/jwks.json` and also written to the state folder.
- **Lifetimes:** access token RS256, 15 min; ID token 15 min; refresh token 8 h absolute, **one-time use, rotated on every refresh**. If a used refresh token is presented again, **revoke the whole token family** and log an event (reuse detection).
- **Claims:** `iss`, `aud` (the client id), `sub`, `name`, `email`, `roles`, `sites`, `acr` (`pwd` | `mfa`), `amr`, `auth_time`, `sid`, `jti`, `exp`, `iat`. Add `elevated_until` while JIT elevation is active, and `break_glass: true` for break-glass sessions.
- **Service tokens** (`client_credentials`): `sub` = client id, `roles: ["SVC"]`, `aud: "force-fab-lake"`.

### 2.3 Endpoints
| Endpoint | Behaviour |
|---|---|
| `GET /.well-known/openid-configuration` | Standard discovery document |
| `GET /jwks.json` | Public keys |
| `GET/POST /authorize` | Authorization code flow. **PKCE S256 mandatory**, exact `redirect_uri` match, `state` + `nonce`. Renders the branded login page, then an OTP page if the user has MFA. `acr_values=mfa` forces OTP if the last MFA is older than 5 min; users not enrolled get an enrolment page. `prompt=login` forces re-login. The code is single-use and lives 60 s. |
| `POST /token` | Grant types `authorization_code` (+ `code_verifier`, client secret via Basic auth or form), `refresh_token` (rotation), `client_credentials` (service clients only) |
| `GET /userinfo`, `POST /revoke`, `GET /logout` | Logout only redirects to registered app origins |
| `GET /health` | Liveness |

IdP session cookie `ffidp_session` (HttpOnly, SameSite=Lax). This gives **single sign-on**: signing in to App A means App B signs in without asking for the password again.

### 2.4 Password and login policy (NIST SP 800-63B-4)
- **Passwords:** 15–64 characters, or 8 minimum if MFA is enrolled. No composition rules. Check against a small blocklist of common or breached passwords. Hash with bcrypt.
- **Lockout:** after 5 failures, locked for 15 min (progressive).
- **Rate limit:** 20 attempts per IP per minute, then HTTP 429 with `Retry-After`.
- **Comparisons:** constant time.
- **MFA:** TOTP per RFC 6238 (SHA1, 6 digits, 30 s step, ±1 step tolerance). A code can't be reused within its step.

### 2.5 Governance features (`/api/admin/*`, FF-ADMIN only; FF-AUDITOR read-only)
- **Users:** list, create, disable, enable, assign role. **SoD:** one user may not hold both FF-ADMIN and FF-AUDITOR (break-glass seed excepted).
- **Sessions:** list and revoke.
- **JIT elevation:** a user requests a role for N minutes (max 240) with a reason. A **different** admin approves; self-approval is rejected. The role appears in tokens until `elevated_until`, then expires automatically.
- **Break-glass:** only the `breakglass` user can activate it, for 60 min max. Activation logs a **critical** event.
- **Access reviews:** create a campaign, which generates one item per user-role. Each item is certified or revoked with a comment. Evidence is exported as CSV.
- **SCIM 2.0 subset:**
  - `/scim/v2/Users`: list with `userName eq` filter, get, create, PATCH (active, roles), DELETE (deactivates).
  - `/scim/v2/Groups`: list roles.
  - Authorised by a SCIM client token or FF-ADMIN.
- **Admin console** at `/admin`: server-rendered pages (users, sessions, JIT, reviews, events) that work without JavaScript. Forms are CSRF-protected.

### 2.6 Auth event log
Every login, failure, MFA, elevation, break-glass, token reuse and SCIM change is appended with `prev_hash` and `hash = sha256(prev_hash + event)`. `GET /api/admin/audit/verify` recomputes the chain and reports any tampering.

### 2.7 Seed data (dummy, local only)
Password for all: `ForceFab-Demo-2026!`. Every enrolled user shares the demo TOTP secret `JBSWY3DPEHPK3PXP`. The login page shows "Demo: current code ######" only when `FF_DEMO_HINTS=1`.

| Login | Name | Roles | Sites | MFA |
|---|---|---|---|---|
| reviewer.tw | Mei Chen | RT-01 | FAB-01 | yes |
| shiftlead.tw | Wei Lin | RT-02 | FAB-01 | yes |
| engineer.az | Jordan Patel | RT-03 | FAB-02 | yes |
| policy.owner | Sofia Alvarez | RT-04 | FAB-01, FAB-02 | yes |
| analyst.az | Liam Brooks | RT-05 | FAB-02 | **no** (shows enrolment) |
| opslead | Ava Huang | RT-06 | FAB-01, FAB-02 | yes |
| admin | Force Fab Admin | FF-ADMIN | both | yes |
| auditor | Grace Kim | FF-AUDITOR | both | yes |
| breakglass | Break Glass | FF-ADMIN, RT-02 | both | yes |

FAB-01 = Taiwan, FAB-02 = Arizona.

| Client | Type | Secret (dummy) | Notes |
|---|---|---|---|
| force-fab-app-a | confidential web | dev-secret-a | redirect `http://127.0.0.1:8100/auth/callback` and the `localhost` equivalent |
| force-fab-app-b | confidential web | dev-secret-b | 8110 equivalents |
| force-fab-svc-a / force-fab-svc-b | client_credentials | dev-svc-a / dev-svc-b | audience `force-fab-lake` |
| force-fab-scim | client_credentials | dev-scim | SCIM only |

**Acceptance tests (33 on our side):**
- Discovery and JWKS.
- Full PKCE flow, with the token verified against JWKS.
- Rejections: wrong verifier, reused code, wrong redirect.
- OTP: required, wrong code fails, step-up.
- Refresh rotation, and reuse revokes the family.
- `client_credentials`.
- Lockout and 429.
- Password policy cases, and the RFC 6238 test vectors.
- SCIM CRUD.
- JIT: request, approve, self-approve rejected, expiry.
- Break-glass event.
- Access review and CSV.
- Hash chain detects tampering.
- Admin endpoints return 403 for non-admins.
- Logout.

---

## 3. Apps authenticate through the IdP (both apps)

**Principle:** identity comes **only** from a signed token. The browser never holds a token, an API key or a role picker. Client-sent `X-Actor-Id`, `X-Actor-Role` and `X-Api-Key` headers are **ignored**: the middleware strips them and rewrites them from the token, so existing route code keeps working.

### 3.1 Backend-for-frontend (BFF) routes on each app
| Route | Behaviour |
|---|---|
| `GET /auth/login?next=` | Creates the PKCE verifier, state and nonce (kept in a short signed cookie) and redirects to the IdP |
| `GET /auth/callback` | Exchanges the code server-side, validates the ID token nonce, creates a server-side session |
| `GET /auth/me` | Returns `{sub, name, roles, sites, acr, amr, exp, app, idp, csrf}` |
| `GET /auth/stepup?next=` | Re-authorises with `acr_values=mfa` |
| `POST /auth/logout` | Clears the session and returns `logout_url` (IdP logout → app origin) |

- **Sessions:** stored server-side; idle timeout 30 min, absolute 8 h; refreshed with the refresh token.
- **Cookies are host-scoped, not port-scoped.** On `127.0.0.1`, App A, App B and the IdP share cookies, so use **per-app names**: `ff_session_a` / `ff_session_b`, `ff_csrf_a` / `ff_csrf_b`, `ff_auth_a` / `ff_auth_b`. We lost time to this: with one shared name, the apps logged each other out.
- **CSRF:** every cookie-authenticated non-GET request needs an `X-CSRF-Token` header matching the session's token. The UI gets the token from `/auth/me` (`csrf` field) rather than by reading cookies.
- **Bearer tokens:** `Authorization: Bearer` is also accepted, for API clients and tests.
- **Token checks:** RS256 signature via JWKS (cached, refetched on an unknown `kid`), plus `iss`, `aud` (App A accepts `force-fab-app-a`, App B `force-fab-app-b`) and `exp`, with 30 s leeway.
- **Protected API without a session:** returns 401 JSON with a `login_url`, never a redirect. The UI performs the redirect.
- **Open paths:** `/health`, `/healthz`, `/readyz`, `/metrics`, `/auth/*`, and `GET` of `/`, `/index.html`, `/assets/*`.

### 3.2 Roles and separation of duties
- **Accepted roles:** RT-01..RT-06 plus FF-ADMIN, FF-AUDITOR and SVC. Keep your existing action-to-role map (`dispose`→RT-01, `approve_agent`→RT-02, `recipe_hold_or_release`→RT-03, `policy_pick`/`keep_wait`→RT-04, `replay_confirm`→RT-05, `assign_owner`→RT-06).
- **SoD:** the signer can't be the proposer (new error class `sod_violation`). FF-ADMIN and FF-AUDITOR can't approve. Model actors are still always rejected.

### 3.3 E-signatures on `POST /api/approvals` (21 CFR Part 11-style)
- **Request body:** the existing payload plus `signature: {meaning: approve|reject|release|dispose, reason}`. Without it, return 400 `signature_required`.
- **Step-up:** requires `acr=mfa` with `auth_time` no older than 5 min. Otherwise return 401 `step_up_required` with a `stepup_url`.
- **Signature record:** a new `approval_signatures` table linked to the audit row stores `signer_sub`, `signer_name`, `meaning`, `reason`, `signed_at`, `token_jti`, and `signature_hash` (sha256 of the canonical JSON of decision + signer + time).

### 3.4 Site-based access (ABAC)
- **Lists:** filtered to the user's `sites`.
- **Detail records:** a record outside the user's sites returns 403 `site_forbidden`.

### 3.5 Lake access
- **Lake REST and MCP:** accept only a bearer service token with `aud=force-fab-lake` and role SVC. The API key is accepted only in legacy-test mode.
- **Service tokens:** each app gets one via `client_credentials` and caches it until 60 s before expiry.

### 3.6 Test-only legacy mode
`FF_ALLOW_LEGACY_HEADERS=1` re-enables the old header identity, for tests that spawn legacy processes. The server **refuses to start** with it when `FF_ENV=production`.

### 3.7 New error classes
`unauthenticated`, `token_invalid`, `token_expired`, `step_up_required`, `site_forbidden`, `csrf_failed`, `rate_limited`, `sod_violation`, `signature_required`. Keep the existing envelope: `ok, error_class, message, correlation_id, waiting_role, lake_item_ids`.

### 3.8 Test migration (important)
- **Test fixtures:** in `conftest.py`, generate an RSA test key per session, write a JWKS file, and point `FF_JWKS_FILE` at it. Provide `mint_token(sub, roles, sites, acr, aud, ...)`.
  - `api_headers` becomes `Authorization: Bearer <RT-01 mfa token>`.
  - `lake_headers` becomes a service token.
  - Default test tokens carry both app audiences.
- **Existing tests:** 21 files used the old headers; most migrate automatically through the fixtures.
- **New tests:**
  - Forged headers are ignored.
  - Missing, invalid, expired, wrong-aud, wrong-iss and unknown-kid tokens all return 401.
  - Login redirect contains S256 and state; callback sets an HttpOnly cookie.
  - CSRF.
  - Step-up and SoD; admin can't approve.
  - Site refusal.
  - Security headers, CORS, rate limit, metrics, readiness, traceparent.
  - Lake rejects requests without a token.
  - Legacy mode is refused in production.

---

## 4. Platform hardening (both apps)

- **Security headers:**
  - CSP `default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'`
  - `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Permissions-Policy`
- **CORS:** exact origins only (8100 and 8110 on 127.0.0.1 and localhost). App B previously allowed `*`.
- **Rate limit:** token bucket per principal and IP (`FF_RATE_LIMIT_PER_MIN`, default 300), returning 429 with `Retry-After`.
- **`/healthz`:** liveness.
- **`/readyz`:** checks the DB, lake, IdP and model mode, and returns JSON.
- **`/metrics`:** Prometheus text format (requests, latency histograms, auth failures, AI calls, rate-limited count). No extra library needed.
- **Tracing:** W3C `traceparent` is parsed or generated, added to every JSON log line, and echoed in responses.

---

## 5. Business feature API (both apps)

One shared router, included **before** your existing routers. Otherwise `/api/audit/{correlation_id}` shadows `/api/audit/search`.
- **Data source:** the legacy SQLite, read-only (`file:...?mode=ro`).
- **List shape:** every list returns `{ok, items, total, limit, offset}` (limit max 200, default 50) and respects site access.
- **Site mapping:** legacy `cases.site` values map to FAB-01 Taiwan (JP-KN, IN-BLR, DE-BY) or FAB-02 Arizona (US-TX, BR-SP, GB-ENG). Lots inherit the site of their tool's chamber.
- **No invented numbers:** every estimate or derived figure is labelled (`label: "estimate"`, `measured: true/false`, `source`).

| Endpoint | What it returns |
|---|---|
| `GET /api/dashboard` | Open cases by status, severity and site. Engineering holds with hold age and **24 h SLA** timer. Scrap cost by chamber (estimate: **1,500 USD per defect**, an assumption). Yield. MTTA/MTTR from events. |
| `GET /api/cases?status&severity&segment&site&q` | Case list |
| `GET /api/cases/{id}/detail` | Case, event timeline, related lot and tool, policy exceptions, lineage ids (App B also returns lake item ids) |
| `GET /api/approvals/pending` | Queue items waiting for the user's role and sites. Each item carries **`action_type`** (derived from the waiting role via the action map) and **`proposed_by`**. Without these, every Sign click is rejected — a bug we hit. |
| `GET /api/domain/{process_steps,metrology,engineering_changes,supplier_parts}` | Filtered domain tables |
| `GET /api/lots/{lot}/genealogy` | Lot → process steps → tool → recipe version → engineering change effective at step time → supplier parts → metrology. Flags `recipe_mismatch` and `ecn_conflict`. |
| `GET /api/spc/{parameter}` | Series with spec limits, mean, sigma, 1/2/3σ limits and **Western Electric rules 1–4** flags. Warns about mixed units (nm and Å). |
| `GET /api/partners/{partner_feeds,batch_runs,reference_versions,upstream_outages,policy_exceptions}` | Partner tables plus a summary: retry rate, rejection rate, reference-version drift |
| `GET /api/audit/search?actor&case&from&to[&format=csv]` | Audit rows. The CSV escapes formula-like cells. |
| `GET /api/semantic/terms?q` | Semantic-layer terms with definitions and cross-system name mappings |
| `GET /api/graph` | 12 best-connected Context Lake items (suggested starting points) |
| `GET /api/graph/{item_id}` | Neighbourhood, 2 hops, max 60 nodes. **Ids are lake item ids** (`rule.recipe_release.limit`), not case ids. Default the page to the best-connected item; we first defaulted to a case id and the page always errored. |
| `GET /api/kpi/compare` | A vs B vs legacy cells `{value, source, measured, note}`. Unmeasured cells show `null` and "Unknown". |
| `GET /api/costs` | Cost per case by period, plus the scrap estimate |
| `GET /api/scenarios/faults` | Four detectors, each with findings, recommended action and required role: **tool drift** (defect trend per chamber), **outlier wafer** (out of spec or beyond 3σ), **unqualified supplier** (non-qualified parts on active tools), **lot genealogy** (step recipe conflicts with the effective ECN) |
| `GET /api/flags` | Feature flags from a JSON file, per app |
| `GET /api/notifications` | Outbox (SLA breaches, break-glass). Teams webhook stub, posted only when `FF_TEAMS_WEBHOOK` is set. |
| `GET /api/i18n/{en,zh-TW}` | UI strings |
| `POST /api/ask` | See §7 |

**Data caveats to keep visible:**
- The legacy data ends in Feb 2023, and "now" = the latest `process_steps` timestamp, so all 8 holds show SLA-breached.
- Cases link to lots by sequence number, not by foreign key; say so in the response.

---

## 6. AI safety controls (App A model path)

- **Daily token budget per user (OWASP LLM10):**
  - Estimate prompt tokens (characters / 4) before calling the model.
  - If the user's daily budget is exceeded (`FF_LLM_DAILY_TOKENS`, default 50,000), don't call the model; return `error_class: llm_budget_exceeded`.
  - The auth middleware sets the current user in a context variable.
- **Recipe-value masking (OWASP LLM02):** mask recipe set-points in model output before grounding and caching. That covers parameter=value pairs (temperature, pressure, power, flows, times…) and bare values with process units (mTorr, sccm, °C…). Recipe revision ids like `R01` stay visible.
- **Write-once replay cache:** a live answer is saved under its prompt hash **only if no file exists**. Never overwrite a frozen answer: in live mode, one demo question overwrote a frozen golden answer and broke two evaluation tests. When the file already exists, report `replay_save: "kept_frozen"`.
- **Encoding:** React already escapes text, so don't HTML-encode answers a second time (users would see `&amp;`).

**Tests:**
- Masking is applied and the cache never stores raw set-points.
- An exhausted budget means no model call.
- The frozen file is unchanged after a live call.

---

## 7. "Ask Force Fab AI" panel and source badges

### 7.1 Source badge on every answer
Every answer response gets `model` and `source_badge: {kind, tone, model, label}`. That covers `/api/query`, `/api/agent/run` and `/api/ask` in both apps.

| Situation | Label |
|---|---|
| App A, live model answered | `Generated by <your model service> · <model name>` (append "(fallback)" if a fallback model answered) |
| App A, model call failed | `<model service> did not answer · no claim made` |
| App A offline, saved answer | `Saved <model> answer (offline replay) · no model call` |
| App B, saved answer replayed | `Replayed saved answer · no model call` |
| App B, answered from lake statements | `Reviewed lake answer · no model` |
| No saved answer (offline) | `No saved answer for this question (offline) · no claim made` |

**Rules:**
- A policy **BLOCK** is not a model failure; badge the answer itself.
- Don't call replayed answers "reviewed": they may be answers App A just generated live.
- App B must never import or load the model client. Use a lazy import inside the "model answered" branch only, because your vendor-risk test checks this.
- To name the model, carry the model name and fallback flag from your model client through `generate()` and the agent state to the response.

### 7.2 `POST /api/ask` — `{subject: case|lot|fault, id, mode: explain|plan}`
1. **Load the record** with the §5 functions: case detail, lot genealogy, or fault scenario findings. Enforce site access (403) and existence (404); a bad subject or mode is 400.
2. **Build a short factual question,** at most 8 facts. For example: status, severity, site, lot yield and hold, tool and chamber, dispatch vs equipment recipe, effective ECN, mismatch and conflict flags, out-of-spec metrology, or a fault's policy, count, role, recommended action and the first 3 findings.
3. **Pass lake retrieval hints** per subject, so answers cite the agreed meaning:
   - case: `term.case, term.lot, term.tool, term.source_message, term.engineering_hold`
   - lot: `term.lot, term.lot_genealogy, term.process_step, term.engineering_change, term.recipe_revision_dispatch, term.recipe_revision_equipment, term.recipe_mismatch, data.join.recipe_mismatch, decision.bp1.recipe_mismatch, data.missing.lot_genealogy`
   - fault `tool_drift`: `term.tool, term.chamber, term.excursion, domain.profile.policies`
   - fault `outlier_wafer`: `term.metrology_sample, term.wafer, term.excursion, domain.profile.policies`
   - fault `unqualified_supplier`: `domain.profile.parts, term.tool, domain.profile.policies`
   - fault `lot_genealogy`: `term.lot_genealogy, term.engineering_change, term.recipe_revision_change, data.missing.lot_genealogy, decision.bp1.recipe_mismatch`
   - Add a test that every hint id exists in the lake.
4. **Answer through each app's normal path.** The prompt is `P-EXPLAIN-CONFLICT` for explain and `P-DRAFT-PLAN` for plan, with the same cite-or-abstain grounding.
   - **App A:** your model client.
   - **App B:** replay or lake statements only.
5. **Response:** `{subject, subject_id, mode, question, facts, sentence, draft_plan, verdict, citations, grounded, source_badge, latency_ms, next_step}`, where `next_step` = "Plans are proposals. Changes go through Approvals with an e-signature."
6. **App B rule trace.** App B also returns `rule_trace`: for each cited lake item, its kind, statement, trust, status and links. When nothing was cited, it falls back to the subject's defining items, with `rule_trace_basis: "subject_definitions"`, labelled in the UI as "not an answer".

**Observed on our side:**

| | App A | App B |
|---|---|---|
| lot `L00000016` explain | ANSWER from the live model in about 9 s, 8 citations | Same answer in under 1 s once saved, no model call, 8-item rule trace |
| fault `tool_drift` plan | ANSWER in about 16 s | Replayed in 0.3 s |
| unsupported case | ABSTAIN | ABSTAIN plus the defining items |

---

## 8. UI — Force Fab shell (shared by both apps)

- **Shared source:** one folder (`apps/ui_shared/src`), imported by both Vite builds through an alias (`@ff`, with `server.fs.allow` for the folder). Each app's `main.jsx` passes `{variant: "A"|"B", appName}`.
- **No new npm packages.** Routing is a hash router; charts, the tree and the graph are inline SVG.
- **Remove** each app's `src/api.js` and `ui/assets/app.js`, which sent `X-Api-Key`, and the role picker and actor-id field.

**Auth client:**
- On load: `GET /auth/me`. On 401, go to `/auth/login?next=<hash>`.
- Send `X-CSRF-Token` from `me.csrf` on every POST.
- Same-origin credentials and a correlation id header.
- An aria-live toast region for notices.
- On `step_up_required`: open a dialog, then go to `stepup_url`.
- Logout goes to the returned `logout_url`.

**Header:**
- Wordmark, "by B_soft", and the app badge **A · AI** or **B · Lake**.
- Site switcher.
- Locale switch (English / 繁體中文).
- User menu: name, roles, MFA badge, sign out.

**Left navigation (role-aware) and landing page per role:**

| Page | Contents |
|---|---|
| Dashboard | KPIs, holds and SLA, scrap estimate, notifications |
| Cases | Filters and pagination. Click a row for detail plus the **Ask panel**. |
| Approvals | Inbox. E-sign dialog: meaning, reason, "I am signing as <name>", step-up prompt. |
| Scenarios | Your original 7-tab demo (Replay, Recipe, Clocks, Policy, Outage, Rule trace, Compare), unchanged. Its five bands keep the class names and strings your tests check. The Result band now shows the source badge. |
| Lot genealogy & SPC | Lot id → genealogy tree plus the **Ask panel**. SPC control chart with spec lines and rule flags. Recent metrology. |
| Partner feeds | Tabs per partner table, with summary |
| Knowledge graph | Suggested-item buttons, SVG graph, edge table |
| Glossary | Searchable terms with mappings |
| Audit | Filters, CSV download |
| A-vs-B KPIs | Bars, with estimates hatched and marked "(est.)", and Unknown shown as such |
| Fault scenarios | One card per scenario, titled with the scenario name, plus the **Ask panel** |
| Admin | FF-ADMIN only; links to the IdP console |

**Landing page per role:** RT-01 → Cases, RT-02 → Approvals, RT-03 → Lot genealogy & SPC, RT-04 → Approvals, RT-05 → Partner feeds, RT-06 → Dashboard, FF-AUDITOR → Audit, FF-ADMIN → Dashboard.

**Ask panel** (shared component):
- **Title:** App A "Ask Force Fab AI", App B "Context Lake answer".
- **Buttons:** Explain / Draft a plan.
- **While waiting:** the message "<model> is reading the evidence (up to 30 seconds)".
- **Shows:** verdict badge, source badge, latency, sentence, draft plan, citation chips, and (App B) the rule-trace table.
- **ABSTAIN:** shown as "No grounded answer … no claim is made".

**Pages must code defensively:** generic tables infer their columns, so a missing field doesn't break a page.

**Build:** `npm ci && npm run build` for both apps, then **delete `node_modules`**, because one of your tests scans the files.

---

## 9. Theme — one blended dark theme, distinct accent per app

**CSS variables** (single stylesheet, byte-identical in both apps; brand-inspired tokens, **no third-party logos**):

| Token | Value | Use |
|---|---|---|
| `--ff-bg` | #0B0F14 | page |
| `--ff-surface` | #151B23 | cards |
| `--ff-raised` | #1F2731 | raised elements |
| `--ff-border` | #2D3743 | borders |
| `--ff-text` | #E6EDF3 | text |
| `--ff-muted` | #9AA7B4 | secondary text |
| `--ff-primary` | #76B900 | NVIDIA-inspired green: primary, healthy |
| `--ff-primary-ink` | #0B0F14 | text on green or blue |
| `--ff-info` | #4DA3FF | Foxconn-inspired blue: links, info, citations |
| `--ff-danger` | #FF4D55 | AMD-inspired red: holds, danger |
| `--ff-warning` | #F5A524 | warning |

- **Per-app accent:** `.ff-app { --ff-accent: var(--ff-primary) }` and `.ff-app[data-variant="B"] { --ff-accent: var(--ff-info) }`. The accent colours the header top bar, the current nav item, primary buttons, the scenario tab, the Ask panel border and the focus ring. App A reads green "AI", App B blue "Lake".
- **Font:** Inter / Segoe UI / system sans; mono for ids.
- **WCAG 2.2 AA:**
  - `:focus-visible` 2px outline with offset.
  - Targets at least 24px.
  - `prefers-reduced-motion` respected.
  - **Status is never shown by colour alone** (icon or text too).
- **Tests:**
  - Rewrite the presenter-layout test for the new tokens, Inter, identical CSS between apps, the Force Fab titles, "by B_soft" without `<img>`, no API key or `X-Actor` in UI source, all nav pages present, and the 7 scenario tabs still present.
  - Add a **contrast test** that computes WCAG luminance ratios: each text token ≥ 4.5:1 on bg, surface and raised; ink on primary and info ≥ 4.5:1; focus ring ≥ 3:1.

---

## 10. Native one-click launcher (Windows + WSL, no Docker)

- **Script:** `run_local.sh start|stop|status|restart`.
  - Starts with `setsid nohup`, using the same ports, env and PYTHONPATH as compose.
  - Order: **identity 8095** → legacy 8080 → source-gateway 8090 → bridge (one shot) → lake-rest 8091 / lake-mcp 8092 → model sign-in check (fall back to replay mode on failure) → App A 8100 → App B 8110.
  - Health-waits each service, writes pid files under `.run/`, and frees ports on stop.
- **Env set by the launcher:** `FF_IDP_URL`, `FF_IDP_PUBLIC_URL`, `FF_STATE_DIR`, `FF_DEMO_HINTS=1`, `FF_ENV=local`, the service secrets, and a random `FF_COOKIE_SECRET` kept in `.run/`.
- **Windows bats:**
  - `Start_App.bat`: **stops running services first**, syncs code to WSL, starts, then opens both apps.
  - `Start_App_Offline.bat`: same, in replay mode.
  - `Stop_App.bat`, `Status.bat` (7 services).
- **Sync safety:** never copy SQLite `-wal` / `-shm` / `-journal` files, and never copy over a running app. Restoring a database under a running app corrupted it ("database disk image is malformed"), and every scenario then hung on its loading message.

---

## 11. End-to-end smoke test (live stack)

A script drives the real browser path with one cookie jar. Note that the IdP renders attributes single-quoted or bare, and redirects may be relative.
1. Unauthenticated `/auth/me` → 401; protected API → 401.
2. Login redirect has S256 + state → password → TOTP → callback → session with `acr=mfa`.
3. Every feature endpoint returns JSON. The page is served with CSP.
4. Forged `X-Actor-*` headers are ignored.
5. AI query answers; golden question GQ-01 is a grounded ANSWER with citations; POST without CSRF → 403.
6. Approvals inbox → e-signed approval → 200. Unsigned approval → 400. Audit search shows the signer.
7. SSO into App B without a password.
8. `/healthz`, `/readyz`, `/metrics` all return 200; logout ends the session.

Ours: **29/29 checks pass**. Each pending item can only be signed once, so rehearse with a user other than your demo user. For example, `analyst.az` has 36 items at FAB-02.

---

## 12. Suggested order of work

1. Rename (§1).
2. IdP service and its tests (§2).
3. App auth, then migrate the tests (§3). Expect around 70 temporary failures until the fixtures are in.
4. Platform hardening (§4).
5. Feature API with route order and the `action_type` fix (§5).
6. AI safety (§6) and badges / Ask (§7).
7. UI shell and pages (§8), then theme and contrast (§9).
8. Launcher (§10) and E2E (§11).
9. Full suite: the target is only your pre-existing environment failures.

## 13. Known limitations (state them in the demo)

- The IdP is a local mock with dummy users and one shared demo TOTP secret.
- The scrap cost unit (1,500 USD per defect) is assumed.
- Hold age is measured against Feb 2023 data.
- Model latency and cost aren't yet measured, so the KPI page shows Unknown.
- App A's grounded accuracy isn't measured; App B shows the recorded 42/42.
- The OPA binary isn't installed in our environment, so the built-in evaluator applies the same rules.
