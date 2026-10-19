# Identity and role hardening

| Field | Value |
|---|---|
| Stage | Phase 13 / 27 Hardening. Half A design. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-27a-doc-20261018-001 |
| Status | DESIGN plus Half B measured. SC-27-01 is in `identity.py` and the four gated listeners. HB-27-01 before and after are REAL. |
| Evidence sources | FD-13; FD-18; FD-19; BO-09; Group C; `apps/shared/identity.py`; `apps/app_a/server.py`; `apps/app_b/server.py`; `context-lake/rest_server.py`; `context-lake/mcp_server.py`; `compose.yaml`; `docs/20-application/access-control-implementation.md`; `docs/24-security-privacy/security-control-matrix.md`; `docs/12-specs/error-handling-spec.md`; `tests/platform/test_identity.py`; `tests/platform/test_app_a_identity_and_ui.py` |
| Assumptions | Closed role list stays RT-01 to RT-06. Identity headers stay `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role`. `MODEL_MODE=replay`. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Company job titles stay Unknown. Named people stay Unknown. How a company issues actor ids stays Unknown. Numeric latency and availability stay Unknown. |
| Residual risks | Port 8080 still serves case reads with no identity check. Port 8090 still serves the fixture feed with no identity check. A later public bind of those two ports would expose the synthetic case list. |

This file names how Application A, Application B, and the Context Lake check who is calling. The Context Lake is the SQLite knowledge store. It names the one small Half B control. It leaves ports 8080 and 8090 unchanged.

Engineering decision ED-P13-27A-01, authority: team-force. Control id `SC-27-01`. Check id `HB-27-01`. Error class `missing_server_key`. HTTP 503 when `FABPULSE_API_KEY` is missing in the process.

Engineering decision ED-P13-27A-02, authority: team-force. Port 8080 and port 8090 stay ungated in this sub-stage. A later wrap in front of those ports, if release work needs one, is named for sub-stage 30. This half does not add a login server.

Engineering decision ED-P13-27A-03, authority: team-force. Threat ids `TM-27-01` to `TM-27-12`. Control ids `SC-27-01` to `SC-27-12`. Failure ids `FM-27-01` to `FM-27-08`.

---

## Finding

**Finding.** Application A on 8100 and Application B on 8110 already require `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role`. The role string must be one of RT-01 to RT-06. Writes match `action_type`. Lake REST on 8091 and lake MCP on 8092 already require `X-Api-Key`. When `FABPULSE_API_KEY` is missing in the process, those four listeners still return HTTP 401 `missing_identity`. A caller who sent the three headers cannot tell the process has no key. Half B changes that one response to HTTP 503 `missing_server_key`. Health stays HTTP 200. Port 8080 and port 8090 stay open without identity.
**Evidence.** `check_app_identity` and `check_lake_key` in `apps/shared/identity.py`. Middleware in `apps/app_a/server.py` and `apps/app_b/server.py` returns 401 for every identity error. `test_unknown_role_is_403` on `/api/queue`. CT-35 on 8080. FD-13. FD-18. FD-19.
**Impact.** Half B edits the shared helper and the four gated listeners. One pytest file records before and after.
**Risk.** Copying identity onto 8080 in this half would change the characterization baseline. Adding a login server would add a feature.
**Confidence.** High on the measured 401 before row and the measured 503 after row.
**Open questions.** HALF_A_ACCEPTED. Company titles. Named people.

---

## Locked facts this design applies

**Verified Fact.** FD-13. Identity is `FABPULSE_API_KEY` plus `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role`. The documented local default `local-demo-only` lives in `.env.example`.

**Verified Fact.** FD-18. Access control stays the closed role list RT-01 to RT-06. This phase adds no attribute-based product.

**Verified Fact.** FD-19. Numeric latency, availability, recovery-time, recovery-point, retry-count, and cost floors stay Unknown. Replay is the path when the live model is off. A failed intake stays visible to the person.

**Verified Fact.** BO-09. The proposer of an action is never its approver. Company job titles stay Unknown.

**Verified Fact** of BO-01 through BO-13 that are PROPOSED. Those rows stay PROPOSED. This half invents no signer name.

---

## Who may call which listener

**Verified Fact.** `compose.yaml`. `identity.py`. Prior Phase 8 and Phase 9 probes. Honesty of those probes: REAL.

| Listener | Port | Identity now | After this sub-stage |
|---|---|---|---|
| Application A | 8100 `/api` | Three headers. Closed role list. Writes match `action_type` | Same, plus SC-27-01 when the process key is missing |
| Application B | 8110 `/api` | Same three headers and closed role list | Same, plus SC-27-01 |
| Lake REST | 8091 except `/health` | `X-Api-Key` | Same, plus SC-27-01 |
| Lake MCP | 8092 except `/health` | `X-Api-Key` | Same, plus SC-27-01 |
| Health on 8091, 8092, 8100, 8110 | those ports `/health` | Open | Open. HTTP 200 `ok: true` even when the process key is missing |
| Static UI GET on 8100 and 8110 | `/`, `/assets/` | Open | Open |
| Legacy workshop | 8080 | None. CT-35 HTTP 200 with no header | Unchanged |
| Source gateway | 8090 | None. Fixture | Unchanged |

Worked example. `GET /api/identity-check` on 8100 with no headers returns HTTP 401 `missing_identity`. Honesty: REAL. `GET /api/queue` on 8100 with a valid key and `X-Actor-Role: ADMIN` returns HTTP 403 `forbidden_role`. Honesty: REAL. `GET /api/cases` on 8080 with no header returns HTTP 200. Honesty: REAL (CT-35).

---

## Closed role list

**Verified Fact.** Group C. `CLOSED_ROLES` in `identity.py`. `ACTION_ROLE_MAP`.

| `action_type` | Allowed `X-Actor-Role` | Who is refused |
|---|---|---|
| `dispose` | RT-01 Fab Exception Reviewer | The model. The same person as `proposed_by` |
| `approve_agent` | RT-02 Shift Lead or Process Engineer (Approver) | The proposing agent. The same person as `proposed_by` |
| `recipe_hold_or_release` | RT-03 Process Engineer | RT-05 acting alone. The model |
| `policy_pick` or `keep_wait` | RT-04 Policy Owner | The model |
| `replay_confirm` | RT-05 Operations Analyst | An unattended job. The model |
| `assign_owner` | RT-06 Operations Lead | A made-up name. The model |

Reads on `/api` allow any of those six roles after the key matches. An empty role is HTTP 401 `missing_identity`. A present unknown string is HTTP 403 `forbidden_role`.

Demo actors `demo-rt01-1` through `demo-rt06-1` are laptop labels. Company staff names stay Unknown.

Site code, country, and sales region stay fields on the case. They do not become a second access product.

---

## Failure modes and recovery

| Id | Failure | What the person sees today | Recovery | Half B change |
|---|---|---|---|---|
| FM-27-01 | `FABPULSE_API_KEY` is missing in the process | HTTP 401 `missing_identity` on `/api`, including when the caller sent three headers | Set the environment variable. Restart the listener. For a laptop demo, copy `.env.example` to `.env` | After SC-27-01: HTTP 503 `missing_server_key`. Health stays 200 |
| FM-27-02 | Caller omits a header | HTTP 401 `missing_identity`. No case body | Send `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role` | None |
| FM-27-03 | Caller sends an unknown role | HTTP 403 `forbidden_role` | Send one of RT-01 to RT-06 | None |
| FM-27-04 | Caller sends a wrong key | HTTP 401 `missing_identity` | Send the key that matches `FABPULSE_API_KEY` | None |
| FM-27-05 | Role does not match `action_type`, or actor equals proposer | HTTP 403 `forbidden_role`. Record unchanged | A different person in the mapped role retries | None |

Worked example for FM-27-01. Process environment has no `FABPULSE_API_KEY`. Caller sends `X-Api-Key: local-demo-only`, `X-Actor-Id: demo-rt01-1`, `X-Actor-Role: RT-01`. Today the body says `missing_identity` and HTTP is 401. After Half B the body says `missing_server_key` and HTTP is 503. The caller sent identity. The process has no key to compare.

---

## Dead-letter queue and replay

A failed identity check is returned on the same request. It is not stored for later replay.

Parking a bad intake message and replaying it is sub-stage 28.

When the live model is off, Application A and Application B read `operations/model-replay/` using `MODEL_MODE=replay`. **Verified Fact.** FD-19. That path stays. This half adds no third offline mode.

---

## Runbook

1. Read the JSON line on stdout. Look at `event` and `error_class` on the HTTP body.
2. If `error_class` is `missing_identity`, the caller omitted a header or sent a wrong key. Send the three headers. Use a role from RT-01 to RT-06.
3. If `error_class` is `forbidden_role`, the role does not match the action, or the actor equals `proposed_by`. Pick the mapped role. Use a different person id.
4. After Half B, if `error_class` is `missing_server_key`, the process has no `FABPULSE_API_KEY`. Set that variable. Restart Application A, Application B, lake REST, and lake MCP. For a laptop demo, copy `.env.example` to `.env`.
5. Confirm `GET /health` on 8100 returns HTTP 200 `{"ok": true}`.
6. Confirm `GET /api/identity-check` on 8100 with the three headers returns HTTP 200 and echoes the actor.

A copy of this runbook into `operations/` belongs to sub-stage 29. This half keeps the steps in this folder.

---

## SLOs and observability

JSON lines on stdout already record `service`, `event`, `correlation_id`, `actor_id`, `path`, `status`, and `duration_ms`. **Verified Fact.** `apps/shared/jsonlog.py`.

That line can prove HB-27-01 returned 503. It does not prove an availability percent.

| Measure | Value in this sub-stage | Label |
|---|---|---|
| Identity miss is visible | `event=identity_missing` and HTTP 401 | Verified Fact of today's logs |
| Server-key miss is visible after Half B | `event=server_key_missing` and HTTP 503 | Verified Fact of HB-27-01 after |
| Availability percent | Unknown | Unknown |
| API p95 | Unknown | Unknown |
| Duration number on one request | `duration_ms` on that line | REAL when the line is captured. Not an SLO |

Do not copy the inherited 99.5 percent availability note as a target.

---

## Cost and the 0C envelope

SC-27-01 adds no model call. Token lines B2 to B7 in `docs/00-preflight/ai-economics/provisional-token-budget.md` stay Unknown. Replay line B1 stays 0 prompt tokens and 0 completion tokens when `MODEL_MODE=replay`. Honesty of that envelope row: Assumption until Phase 15 proves replay.

Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED legacy fields. This half claims no dollar benefit. **Verified Fact.** FD-19. BO-11 working answer stays PROPOSED.

---

## The one small control Half B puts in code

Engineering decision ED-P13-27A-01 continued, authority: team-force.

Control id **SC-27-01**. Name: missing process key returns HTTP 503.

Today `configured_api_key()` returns `None` when `FABPULSE_API_KEY` is missing or blank. `check_app_identity` and `check_lake_key` then return `missing_identity`. Middleware returns HTTP 401.

After Half B:

1. `identity.py` adds `missing_server_key()`. The body uses `error_class: missing_server_key`. The message says the process has no `FABPULSE_API_KEY` and that the documented local default lives in `.env.example`. The message does not write `local-demo-only`.
2. `check_app_identity` and `check_lake_key` return that body when the process key is missing.
3. A helper `identity_reject(error)` returns the body, the HTTP status, and the log event name. Status is 503 and event is `server_key_missing` when `error_class` is `missing_server_key`. Status is 401 and event is `identity_missing` for the caller-miss path.
4. Middleware in `apps/app_a/server.py`, `apps/app_b/server.py`, `context-lake/rest_server.py`, and `context-lake/mcp_server.py` uses that helper.
5. `/health` stays HTTP 200. Compose healthchecks keep passing.
6. Caller missing headers, wrong key, or unknown role stay as they are now.

`app_stub.py` is leftover. Live listeners are `apps/app_a/server.py` and `apps/app_b/server.py`. Half B does not add a feature to the stub.

---

## Exact Half B check HB-27-01

Test path Half B writes: `tests/platform/test_phase13_hardening.py`.

Headers for the probe (supplied by the test the same way Phase 10 does; not written into application source):

| Header | Value |
|---|---|
| `X-Api-Key` | `local-demo-only` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |

### Before (today's `identity.py`)

Unset `FABPULSE_API_KEY` in the test process. Reload the helper so `configured_api_key()` is `None`.

`GET /api/identity-check` on Application A with the three headers.

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| HTTP status | 401 | 401 | REAL |
| `error_class` | `missing_identity` | `missing_identity` | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| Case body | Absent | Absent | REAL |

Measured at `2026-10-18T19:12:21+00:00`. JSON `event=identity_missing`. Honesty: REAL. Full table: `hardening-test-results.md`.

### After (SC-27-01 landed)

Same unset environment. Same three headers. Same `GET /api/identity-check` on Application A.

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| HTTP status | 503 | 503 | REAL |
| `error_class` | `missing_server_key` | `missing_server_key` | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| JSON `event` | `server_key_missing` | `server_key_missing`, `status=503` | REAL |
| Key literals in that JSON line | laptop key value absent. `X-Api-Key` absent. `api_key` absent | All three absent | REAL |

Measured at `2026-10-18T19:13:56+00:00`. Honesty: REAL.

### Control cases after (process key restored in the test environment)

| Call | Expected | Measured | Honesty |
|---|---|---|---|
| `GET /api/identity-check` on 8100 with no headers | HTTP 401 `missing_identity` | HTTP 401 `missing_identity` | REAL |
| `GET /api/identity-check` on 8100 with the three headers | HTTP 200, actor `demo-rt01-1`, role `RT-01` | HTTP 200, actor `demo-rt01-1`, role `RT-01` | REAL |
| `GET /api/queue` on 8100 with valid key and `X-Actor-Role: ADMIN` | HTTP 403 `forbidden_role` | HTTP 403 `forbidden_role` | REAL |
| Same missing-env probe on Application B | HTTP 503 `missing_server_key` | HTTP 503 `missing_server_key` | REAL |
| Same missing-env probe on lake REST a read path | HTTP 503 `missing_server_key` | HTTP 503 `missing_server_key` on `/v1/version` | REAL |
| Same missing-env probe on lake MCP | HTTP 503 `missing_server_key` | HTTP 503 `missing_server_key` on `/v1/tools` | REAL |

Honesty of the recorded before and after rows: REAL. Full table: `hardening-test-results.md`.

---

## Controls that stay as built

| Id | Control | Half B action |
|---|---|---|
| SC-27-02 | Closed role list RT-01 to RT-06 | Re-measure ADMIN → 403 on HB-27-01 |
| SC-27-03 | Three headers on 8100 and 8110 | Re-measure missing headers → 401 |
| SC-27-04 | `X-Api-Key` on 8091 and 8092 | Re-measure missing-env 503 on lake REST |
| SC-27-08 | Port 8080 and port 8090 stay ungated | Defer. Sub-stage 30 if a wrap is ever added |

---

## What this file does not do

Half B landed SC-27-01. Measured before and after rows are in `hardening-test-results.md`. This file still does not add identity to port 8080 or port 8090. It does not add a login server. It does not put the laptop key value into application source. It does not invent a percent or a dollar benefit. It does not sign a Business Owner row. It does not start sub-stage 28.
