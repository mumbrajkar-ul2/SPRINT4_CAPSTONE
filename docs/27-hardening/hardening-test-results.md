# Hardening test results

| Field | Value |
|---|---|
| Stage | Phase 13 / 27 Hardening. Half B measured results. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-27b-doc-20261018-001 |
| Status | MEASURED. SC-27-01 is in `identity.py` and the four gated listeners. HB-27-01 before and after are REAL. |
| Evidence sources | `identity-rbac-hardening.md`; `secrets-hardening.md`; `apps/shared/identity.py`; `apps/app_a/server.py`; `apps/app_b/server.py`; `context-lake/rest_server.py`; `context-lake/mcp_server.py`; `compose.yaml`; `tests/platform/test_phase13_hardening.py`; FD-13; FD-18; FD-19 |
| Assumptions | `MODEL_MODE=replay`. Tests supply `X-Api-Key` from `.env.example`. Application source stays without that literal. |
| Unresolved issues | Numeric availability stays Unknown. A company production key stays unissued. Rotation days stay Unknown. |
| Residual risks | Port 8080 and port 8090 stay ungated. Compose still injects the documented laptop default when the host omits `FABPULSE_API_KEY`. |

This file records the Half B before-and-after run for control SC-27-01. Test output is REAL. This half invents no CVE and no percent.

Engineering decision ED-P13-27A-01 continued, authority: team-force. Check id HB-27-01. Test path `tests/platform/test_phase13_hardening.py`.

---

## Finding

**Finding.** Before SC-27-01, a missing process `FABPULSE_API_KEY` returned HTTP 401 `missing_identity` on identity-checked routes. After SC-27-01 the same call returns HTTP 503 `missing_server_key`. Health stays HTTP 200 `{"ok": true}`. A restored key with no headers stays HTTP 401. A restored key with the three headers stays HTTP 200. Role `ADMIN` on `/api/queue` stays HTTP 403. Port 8080 and port 8090 stay without `FABPULSE_API_KEY` in Compose.
**Evidence.** Live before probe at `2026-10-18T19:12:21+00:00`. Live after probe at `2026-10-18T19:13:56+00:00`. Correlation id `corr-p13-27b-doc-20261018-001`. Honesty: REAL.
**Impact.** A caller who sent the three headers can now tell the process has no key. Compose healthchecks still pass.
**Risk.** Port 8080 still serves case reads with no identity check. Port 8090 still serves the fixture feed with no identity check.
**Confidence.** High on the measured HTTP rows. Unknown on a company production key.
**Open questions.** Company production key. Rotation days.

---

## Probe used for both rows

Process environment: `FABPULSE_API_KEY` unset. `MODEL_MODE=replay`.

Headers (supplied by the probe and by the pytest file, not by application source):

| Header | Value |
|---|---|
| `X-Api-Key` | the documented laptop default from `.env.example` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |
| `X-Correlation-Id` | `corr-p13-27b-doc-20261018-001` |

Primary call: `GET /api/identity-check` on Application A.

Same missing-env probe also hit Application B `/api/identity-check`, lake REST `/v1/version`, and lake MCP `/v1/tools`.

---

## HB-27-01 before (code still today's `identity.py`)

Command shape recorded:

`python` probe with `FABPULSE_API_KEY` popped, then FastAPI `TestClient` GET on the four listeners. JSON line timestamp: `2026-10-18T19:12:21+00:00`.

`configured_api_key()` returned `None`. Honesty: REAL.

| Listener | Path | HTTP | `error_class` | JSON `event` | `GET /health` | Case body | Honesty |
|---|---|---|---|---|---|---|---|
| Application A | `/api/identity-check` | 401 | `missing_identity` | `identity_missing`, `status=401` | 200 `{"ok": true}` | Absent | REAL |
| Application B | `/api/identity-check` | 401 | `missing_identity` | `identity_missing`, `status=401` | 200 `{"ok": true}` | Absent | REAL |
| Lake REST | `/v1/version` | 401 | `missing_identity` | `identity_missing`, `status=401` | 200 `{"ok": true}` | Absent | REAL |
| Lake MCP | `/v1/tools` | 401 | `missing_identity` | `identity_missing`, `status=401` | 200 `{"ok": true}` plus the four tool names | Absent | REAL |

Worked example. Application A JSON line: `service=app-a`, `event=identity_missing`, `path=/api/identity-check`, `status=401`. The line had no `api_key` field. Honesty: REAL.

---

## HB-27-01 after (SC-27-01 landed)

Same unset environment. Same three headers. Same four listeners. JSON line timestamp: `2026-10-18T19:13:56+00:00`.

`configured_api_key()` returned `None`. Honesty: REAL.

| Listener | Path | HTTP | `error_class` | JSON `event` | `GET /health` | Case body | Honesty |
|---|---|---|---|---|---|---|---|
| Application A | `/api/identity-check` | 503 | `missing_server_key` | `server_key_missing`, `status=503` | 200 `{"ok": true}` | Absent | REAL |
| Application B | `/api/identity-check` | 503 | `missing_server_key` | `server_key_missing`, `status=503` | 200 `{"ok": true}` | Absent | REAL |
| Lake REST | `/v1/version` | 503 | `missing_server_key` | `server_key_missing`, `status=503` | 200 `{"ok": true}` | Absent | REAL |
| Lake MCP | `/v1/tools` | 503 | `missing_server_key` | `server_key_missing`, `status=503` | 200 `{"ok": true}` plus the four tool names | Absent | REAL |

Worked example. Application A JSON line: `service=app-a`, `event=server_key_missing`, `path=/api/identity-check`, `status=503`. That line contained no documented laptop key value, no `X-Api-Key`, and no `api_key` field. Honesty: REAL.

The HTTP message said the process has no `FABPULSE_API_KEY` and that the documented local default lives in `.env.example`. The message did not contain the laptop key value. Honesty: REAL.

### Control cases after (process key restored in the test environment)

| Call | Measured | Honesty |
|---|---|---|
| `GET /api/identity-check` on Application A with no headers | HTTP 401 `missing_identity` | REAL |
| `GET /api/identity-check` on Application A with the three headers | HTTP 200, actor `demo-rt01-1`, role `RT-01` | REAL |
| `GET /api/queue` on Application A with valid key and `X-Actor-Role: ADMIN` | HTTP 403 `forbidden_role` | REAL |
| Compose `legacy` (8080) and `source-gateway` (8090) environment | No `FABPULSE_API_KEY` field. Comment still says those ports stay without an identity check | REAL |

---

## Pytest the reviewer can re-run

```text
python -m pytest tests/platform/test_phase13_hardening.py -q --tb=short
```

Measured on 2026-10-18: 11 passed, 1 skipped in 3.02s. Honesty: REAL.

The before function is skipped after SC-27-01. The before snapshot stays in this file. The after functions assert HTTP 503 `missing_server_key`, health 200, restored-key 401 and 200, `ADMIN` 403, and ungated 8080 and 8090.

---

## What this file does not do

This file does not start sub-stage 28. It does not add a login server. It does not gate ports 8080 or 8090. It does not put the laptop key value into application source. It does not invent a CVE. It does not invent a percent. It does not sign a Business Owner row.
