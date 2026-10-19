# Secrets hardening

| Field | Value |
|---|---|
| Stage | Phase 13 / 27 Hardening. Half A design. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-27a-doc-20261018-001 |
| Status | DESIGN plus Half B measured. SC-27-01 is in `identity.py`. HB-27-01 before and after are REAL. |
| Evidence sources | FD-13; FD-19; `.env.example`; `compose.yaml`; `apps/shared/identity.py`; `apps/shared/jsonlog.py`; `tests/platform/test_freeze_and_bounds.py`; `tests/platform/test_logs.py`; `tests/platform/test_env_example.py`; `.github/workflows/verify.yml`; `docs/24-security-privacy/attack-surface-map.md` |
| Assumptions | The documented local default stays `local-demo-only` in `.env.example`. Application source stays without that literal. `MODEL_MODE=replay`. |
| Unresolved issues | Rotation interval in days stays Unknown. A company production key stays unissued. How a company vault stores the key stays Unknown. |
| Residual risks | Compose still injects `local-demo-only` when the host omits `FABPULSE_API_KEY`. A later author who copies that string into `apps/` would break the source scan. |

This file names where the shared key lives, how logs keep it out, and how an operator rotates it. The one Half B control is SC-27-01: a missing process key becomes visible as HTTP 503 `missing_server_key`.

Engineering decision ED-P13-27A-06, authority: team-force. The string `local-demo-only` stays in `.env.example`, the Compose fallback, the CI job environment, and tests. Half B does not write that string into application source.

---

## Finding

**Finding.** `configured_api_key()` reads `FABPULSE_API_KEY` from the environment. `.env.example` documents `FABPULSE_API_KEY=local-demo-only`. `apps/` Python has no that literal. `test_application_source_has_no_key_literal` already fails if someone adds it. JSON logs drop `api_key`, `x-api-key`, `fabpulse_api_key`, `authorization`, `password`, `secret`, and `token` as field names. When the process has no key, today's `/api` response still says `missing_identity`. Half B makes that process miss visible.
**Evidence.** `identity.py` `configured_api_key`. `.env.example` line 4. `test_freeze_and_bounds.py`. `test_logs.py`. `jsonlog.py` `FORBIDDEN_KEYS`.
**Impact.** Half B changes the missing-key response. Rotation stays a runbook. No vault product is added.
**Risk.** Writing `local-demo-only` into `identity.py` as a fallback would put the documented default into application source.
**Confidence.** High on the source scan and the log field filter. Inference on the 503 path until HB-27-01.
**Open questions.** HALF_A_ACCEPTED. Rotation days. Company vault.

---

## Locked facts this design applies

**Verified Fact.** FD-13. The documented local default is `local-demo-only` in `.env.example`. A company production key stays unissued.

**Verified Fact.** FD-19. This half invents no dollar benefit for rotation or for a vault.

**Verified Fact.** BO-10 working answer, still PROPOSED. Records are internal and synthetic. Process data is confidential. Packaged rows do not contain personal data. This half invents no signer.

---

## Where the key lives now

**Verified Fact** of the files on disk.

| Place | What it holds | Allowed |
|---|---|---|
| Process environment `FABPULSE_API_KEY` | The shared key the listeners compare | Yes. This is the runtime source |
| `.env.example` | `FABPULSE_API_KEY=local-demo-only` | Yes. Documented laptop default |
| `compose.yaml` | `${FABPULSE_API_KEY:-local-demo-only}` on lake-rest, lake-mcp, app-a, app-b | Yes. Compose laptop fallback |
| `.github/workflows/verify.yml` | Job env `FABPULSE_API_KEY: local-demo-only` | Yes. CI uses the documented default |
| `tests/platform/` | Headers and `os.environ.setdefault` with `local-demo-only` | Yes. Tests supply the same documented default |
| `apps/**/*.py` and lake servers | No `local-demo-only` literal | Required. `test_application_source_has_no_key_literal` |
| JSON stdout | No key field and no `local-demo-only` on the identity-miss line | Required. `test_at_log_json_identity_missing` |

Worked example. A laptop operator copies `.env.example` to `.env`. Compose reads `FABPULSE_API_KEY=local-demo-only` and injects it into four containers. Application source still has no that string.

---

## Failure modes and recovery

| Id | Failure | What happens | Recovery |
|---|---|---|---|
| FM-27-01 | Process has no `FABPULSE_API_KEY` | Today every `/api` call is HTTP 401 `missing_identity`. After SC-27-01 the same call is HTTP 503 `missing_server_key` | Set the variable. Restart the four gated listeners. Laptop path: copy `.env.example` to `.env` |
| FM-27-04 | Caller key does not match the process key | HTTP 401 `missing_identity` | Send the matching key. Or rotate both sides together |
| TM-27-02 | Someone writes `local-demo-only` into `apps/` | `test_application_source_has_no_key_literal` fails | Remove the literal. Keep the value in `.env.example` |
| TM-27-03 | A later `emit()` extra field is named `api_key` | `jsonlog.py` drops that field | Keep using `emit()`. Do not write the key on stdout |

Health stays HTTP 200 during FM-27-01. The listener is up. `/api` is unusable until the process has a key.

---

## Dead-letter queue and replay

A missing or wrong key is returned on the same request. It is not parked in a dead-letter store.

Language-model replay stays `MODEL_MODE=replay` and files under `operations/model-replay/`. Those files are PRECOMPUTED model JSON. They are not the shared API key. **Verified Fact.** FD-19.

Intake parking and replay stay sub-stage 28.

---

## Runbook — set or rotate the key

### Set the key on a laptop

1. Copy `.env.example` to `.env` if `.env` is missing.
2. Confirm `.env` has `FABPULSE_API_KEY=local-demo-only` for the local demo.
3. Restart `lake-rest`, `lake-mcp`, `app-a`, and `app-b`.
4. `GET /health` on 8100 returns HTTP 200.
5. `GET /api/identity-check` on 8100 with the three headers returns HTTP 200.

### Rotate the key

1. Choose a new value. Do not write it into `apps/`. Do not write it into this document.
2. Set `FABPULSE_API_KEY` in the process environment of lake-rest, lake-mcp, app-a, and app-b.
3. Restart those four listeners.
4. Tests and CI that send `X-Api-Key` must use the new value.
5. `.env.example` may keep `local-demo-only` as the documented laptop value.
6. Confirm `GET /api/identity-check` with the new header returns HTTP 200.
7. Confirm a request with the old header returns HTTP 401 `missing_identity`.

Rotation interval in days stays Unknown. This half invents no calendar.

A company vault product is out of this sub-stage. How a company stores a production key stays Unknown.

---

## SLOs and observability

The JSON line already proves an identity miss. After Half B it also proves a server-key miss. `event=server_key_missing` with `status=503` is the proof. The line must omit the key value.

Availability percent stays Unknown. **Verified Fact.** FD-19.

`duration_ms` on one line is REAL when captured. An API p95 target stays Unknown.

---

## Cost and the 0C envelope

Reading an environment variable adds no token. Token lines B2 to B7 stay Unknown. Replay line B1 stays 0 and 0 when `MODEL_MODE=replay`. This half claims no dollar saving from rotation. BO-11 stays PROPOSED.

---

## Exact Half B check HB-27-01

The same check as `identity-rbac-hardening.md`.

Before: unset `FABPULSE_API_KEY`. `GET /api/identity-check` on Application A with the three test headers. HTTP 401. `error_class=missing_identity`. Health 200. Honesty: REAL. Measured at `2026-10-18T19:12:21+00:00`.

After: same unset environment. HTTP 503. `error_class=missing_server_key`. Health 200. JSON event `server_key_missing`. That JSON line contains no documented laptop key value, no `X-Api-Key`, and no `api_key` field. Honesty: REAL. Measured at `2026-10-18T19:13:56+00:00`. Full table: `hardening-test-results.md`.

The after message may point at `.env.example`. The after message must not contain `local-demo-only`.

`test_application_source_has_no_key_literal` must still pass after Half B.

---

## What this file does not do

Half B landed SC-27-01. Measured before and after rows are in `hardening-test-results.md`. This file still does not put the laptop key value into application source. It does not add a vault. It does not invent a rotation day count. It does not sign a Business Owner row. It does not start sub-stage 28.
