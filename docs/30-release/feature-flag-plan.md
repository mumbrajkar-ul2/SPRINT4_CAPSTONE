# Feature flag plan

| Field | Value |
|---|---|
| Stage | Phase 13 / 30 Release and rollback. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-30a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No new flag product and no new env var in this half. |
| Evidence sources | FD-19; FD-13; FD-04; `compose.yaml`; `.env.example`; `.github/workflows/verify.yml`; `docs/28-resilience/ai-disabled-mode.md`; `docs/28-resilience/timeout-retry-policy.md`; `apps/app_a/runtime/dlq.py`; `apps/app_a/agent/checkpointer.py`; `apps/app_a/audit/store.py` |
| Assumptions | `MODEL_MODE=replay` stays the laptop default. Azure variables stay unset. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Azure endpoint, deployment name, and API version stay Unknown. A company flag service stays unused. |
| Residual risks | Setting `MODEL_MODE=azure` on the laptop would call the public network. Adding a login flag on 8080 would change CT-35. |

This file names the environment variables that already switch behaviour. A flag here is a process environment variable Compose already reads. This half adds no flag service.

Engineering decision ED-P13-30A-04, authority: team-force. The switch list stays the env vars already in Compose, `.env.example`, and Application A path overrides. Half B adds no new flag name.

---

## Finding

**Finding.** Compose already sets `MODEL_MODE: ${MODEL_MODE:-replay}` on Application A, Application B, lake REST, and lake MCP. `.env.example` documents `FABPULSE_API_KEY=local-demo-only` and `MODEL_MODE=replay`. CI sets `MODEL_MODE: replay`. Application A already reads `APP_A_DLQ_PATH`, `APP_A_CHECKPOINT_PATH`, and `APP_A_AUDIT_PATH` when tests need a temp file. `UPSTREAM_RETRY_COUNT` is a Python constant of 1 in `recovery.py`, not an env var. There is no separate flag-service file, no flag HTTP route, and no login switch. Half B leaves that list as built. SC-30-01 is a Compose volume line, not a new env var.
**Evidence.** `compose.yaml` environment blocks. `.env.example`. `verify.yml` `env`. `dlq.py` `dlq_path()`. `checkpointer.py` `checkpoint_path()`. FD-13 modes `replay` and `azure`.
**Impact.** Operators keep using `.env` copies of `.env.example`. Half B does not add `FEATURE_*` names.
**Risk.** A new `MODEL_MODE=offline` would invent a third mode. FD-13 already closed that.
**Confidence.** High on the current env list. Unknown on a live Azure switch.
**Open questions.** HALF_A_ACCEPTED. Azure variable values when a later live run is allowed.

---

## Locked facts this design applies

**Verified Fact.** FD-13. Modes `replay` and `azure`. No third offline mode.

**Verified Fact.** FD-19. Replay is the path when the live model is off. This half keeps `MODEL_MODE=replay`.

**Verified Fact.** FD-04. Ranking, intake de-duplication, rule evaluation, and reconciliation are deterministic. Those paths do not wait on a model flag.

**Verified Fact.** Ports 8080 and 8090 stay ungated. This file adds no identity flag on those listeners.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

---

## Switches already in force

| Name | Where it is read | Laptop value for this release | What a wrong value does |
|---|---|---|---|
| `MODEL_MODE` | Compose on `app-a`, `app-b`, `lake-rest`, `lake-mcp` | `replay` | `azure` opens a public-network model call |
| `FABPULSE_API_KEY` | Compose on the four gated listeners | `.env.example` documents `local-demo-only` | Missing key: `/api` HTTP 503 `missing_server_key` after SC-27-01. `/health` stays 200 |
| `HOST_PORT` and the other host port vars | Compose `ports` | 8080, 8090, 8091, 8092, 8100, 8110 | Bind fail if the host port is taken |
| `APP_A_DLQ_PATH` | `dlq.py` | Unset in Compose. Default file `apps/app_a/runtime/dlq.sqlite3` | Tests set a temp path |
| `APP_A_CHECKPOINT_PATH` | `checkpointer.py` | Unset in Compose. Default file `apps/app_a/runtime/checkpoints.sqlite3` | Tests set a temp path |
| `APP_A_AUDIT_PATH` | `audit/store.py` | Unset in Compose. Default file `apps/app_a/audit/audit_chain.sqlite3` | Tests set a temp path |
| `UPSTREAM_RETRY_COUNT` | Python constant in `apps/app_a/routes/recovery.py` | `1`. One extra gateway probe on timeout or throttle | Changing it would be a new engineering default, not this Half B |

Worked example. `.env` holds `MODEL_MODE=replay` and omits Azure variables. Application A reads a file under `operations/model-replay/{sha256}` or returns `replay_miss` and abstains. Token line B1 stays 0 and 0.

Worked example. A pytest sets `APP_A_DLQ_PATH` to a temp sqlite file. That temp file is the dead-letter store for the test. Compose default still uses `apps/app_a/runtime/dlq.sqlite3` inside the container, and after SC-30-01 that path is the host file.

---

## What this release does not switch

| Change | This sub-stage |
|---|---|
| New flag service | Not added |
| New `FEATURE_*` env var | Not added |
| Login server or identity on 8080 and 8090 | Not added. Ports stay ungated |
| Third `MODEL_MODE` value | Not added |
| Flag that deletes parked rows | Not added. FD-19 keeps failed intake visible |

SC-30-01 is three Compose volume lines. It is not a feature flag.

---

## Failure modes and recovery

| Id | Failure | Recovery | Numeric floor |
|---|---|---|---|
| FM-30-03 | `MODEL_MODE=azure` on the laptop | Set `replay`. Unset Azure. Restart the four platform listeners | Token cells stay Unknown for a live call |
| FM-27-01 continued | Process key missing | Set `FABPULSE_API_KEY`. Restart the four gated listeners. Health stayed 200 | None invented |
| FM-30-07 | Identity copied onto 8080 | Leave `legacy` without identity env | None invented |

---

## Dead-letter queue and replay

Path overrides `APP_A_DLQ_PATH` already exist for tests. Compose after SC-30-01 uses the default host file. Replay stays `POST /api/recovery/dlq/replay`. No flag hides a parked row.

Language-model replay stays `MODEL_MODE=replay`.

---

## Runbook — keep replay on for a release

1. Read `.env` or Compose. `MODEL_MODE` is `replay`.
2. Confirm Azure endpoint, key, and deployment name are unset for the laptop demo.
3. `GET /health` on 8100. HTTP 200.
4. Ask a GenAI path. A saved replay file answers. A miss abstains.
5. If the body says a live Azure call ran, stop. Set `replay` and restart.

---

## SLOs and observability

`MODEL_MODE` in the process environment proves which model path is on. JSON `event` lines from replay miss and from intake park prove those paths ran. Those cells do not prove an availability percent. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

Keeping `MODEL_MODE=replay` keeps token line B1 at 0 and 0. Lines B2 to B7 stay Unknown. This half claims no dollar benefit for leaving Azure unset.

---

## Exact Half B check

HB-30-01 asserts Compose `MODEL_MODE` default stays `replay` and that no new flag name was added. The volume lines are SC-30-01. They are not a feature flag.

---

## What this file does not do

This file names the env vars already in use. It adds no flag product. It leaves `MODEL_MODE=replay`. It starts no Half B. It signs no Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
