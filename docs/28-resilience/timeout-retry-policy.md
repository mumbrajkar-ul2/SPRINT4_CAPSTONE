# Timeout and retry policy

| Field | Value |
|---|---|
| Stage | Phase 13 / 28 Reliability and resilience. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-28a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No retry code in this half. |
| Evidence sources | FD-19; `apps/app_a/routes/recovery.py`; `apps/app_a/intelligence/retrieve.py`; `apps/app_a/agent/opa_client.py`; `apps/app_a/intelligence/azure_client.py`; `compose.yaml`; `docs/12-specs/error-handling-spec.md`; `docs/22-agentic-engineering/agent-budget-policy.md` |
| Assumptions | `MODEL_MODE=replay`. Client timeout numbers already in code stay as client timeouts. They are not SLOs. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Retry-count floor stays Unknown. Backoff milliseconds stay Unknown. API p95 stays Unknown. Measured extra-attempt timings stay Unknown. |
| Residual risks | Retrying OPA BLOCK would run an injection write. Retrying a schema miss would repeat a bad body. Treating `UPSTREAM_RETRY_COUNT` 1 as a quality floor would skip FD-19. |

This file names how long Application A waits on each call, which failures get one extra attempt, and which failures return on the first response.

Engineering decision ED-P13-28A-01, authority: team-force. `UPSTREAM_RETRY_COUNT` is `1`. That is one extra probe after the first `upstream_timeout` or `upstream_rate_limit`. Total attempts are 2. This integer is an engineering default. It is not Business Owner policy. It is not a quality floor.

---

## Finding

**Finding.** Four client timeouts already sit in code: gateway probe 3 seconds, lake HTTP 5 seconds, OPA eval 15 seconds, Azure complete 30 seconds. Compose health timeout is 4 seconds with 5 retries. The gateway probe runs once. This half names one extra attempt for timeout and throttle only. Schema, identity, BLOCK, abstain, and replay miss stay on the first response.
**Evidence.** `urlopen(..., timeout=3)` in `recovery.py`. `timeout=5` in `retrieve.py`. `timeout=15` in `opa_client.py`. `timeout_s: float = 30.0` in `azure_client.py`. `compose.yaml` healthcheck `timeout: 4s` and `retries: 5`. FD-19.
**Impact.** Half B can store `UPSTREAM_RETRY_COUNT = 1` next to the probe. HB-28-01 still measures park and replay, not p95.
**Risk.** Copying Compose `retries: 5` onto the probe would hide four failures before the person sees one.
**Confidence.** High on the current numbers in code. Unknown on measured durations.
**Open questions.** HALF_A_ACCEPTED. Backoff milliseconds stay Unknown.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric latency and retry-count floors stay Unknown. The integer `1` below is an engineering default. A failed intake stays visible.

**Verified Fact.** `MODEL_MODE=replay`. This half does not call Azure. The 30-second Azure timeout is recorded from the current function signature. Honesty of that signature: REAL of the file. Honesty of a live Azure duration: Unknown.

**Verified Fact.** Injection BLOCK returns on the same request. HTTP 409. No retry.

---

## Client timeouts already in code

These numbers are how long the caller waits for that socket. They are not availability targets.

| Call | Timeout | Where | Extra attempts | Label |
|---|---|---|---|---|
| Source-gateway probe | 3 seconds | `apps/app_a/routes/recovery.py` `probe_gateway` | 1 after timeout or throttle | Verified Fact of the 3. Inference of the extra attempt, authority: team-force |
| Lake REST search or get | 5 seconds | `apps/app_a/intelligence/retrieve.py` | 0. Abstain on failure | Verified Fact |
| OPA `eval` | 15 seconds | `apps/app_a/agent/opa_client.py` | 0. Use `local_evaluate` when the binary is missing or the eval fails | Verified Fact of 15 and of `local_evaluate` |
| Azure chat completions | 30 seconds | `apps/app_a/intelligence/azure_client.py` | 0 in this half. Mode stays `replay` | Verified Fact of the default argument |
| Compose health probe | 4 seconds | `compose.yaml` | Compose retries 5 | Verified Fact. Restart seconds still Unknown |
| Inherited `pull` of gateway events | 5 seconds | `gateway_bridge.py` | 0 in this sub-stage | Verified Fact |

Worked example. The source gateway fixture `mode=timeout` does not answer. Application A waits 3 seconds. Today it returns HTTP 503 after that one wait. After the engineering default, it waits 3 seconds again. If the second wait also fails, the body still shows `error_class: upstream_timeout`. `retry_shown` stays true. The person sees both attempts in the JSON extra fields `attempt_count` 2 and `first_error_class` `upstream_timeout`.

Worked example. Lake REST on 8091 is down. Application A waits 5 seconds on that GET. It does not retry. The query returns HTTP 200 `verdict: ABSTAIN`. FD-14.

---

## What gets the extra attempt

| `error_class` | Extra attempt | Why |
|---|---|---|
| `upstream_timeout` | Yes. One | Transient empty response. Person still sees the first failure |
| `upstream_rate_limit` | Yes. One | Throttle may clear. Person still sees the first 429 |
| `upstream_schema` | No | The body is wrong. A second identical GET repeats the same miss |
| `missing_identity` | No | The caller must send headers |
| `missing_server_key` | No | The process must set `FABPULSE_API_KEY` |
| `forbidden_role` | No | The mapped RT role must call |
| `blocked` | No | Injection stops. Retry would be a write attempt |
| `abstain` | No | Empty knowledge is a finished read |
| `replay_miss` | No | A second hash lookup would miss again. Azure stays off |
| `wait_for_person` | No | A person must act |
| `invalid` intake | No automatic HTTP retry | SC-28-01 parks. A person or the test replays |

Backoff milliseconds stay Unknown. The extra attempt runs immediately in the same request. This half invents no jitter number.

---

## What the extra attempt must still show

**Verified Fact.** FD-19. A failure stays visible.

The probe response after two failed attempts still uses HTTP 503. `retry_shown` is true. The body names `attempt_count`. The first `error_class` stays in the body. If the second attempt also failed, Half B still returns 503 and still names the first timeout.

If the second attempt returns `mode=normal` HTTP 200, the probe status is 200. The body still records that attempt 1 failed. Recovery GET stays readable.

---

## Idempotency on intake replay

**Verified Fact.** `gateway_inbox.message_id` is the primary key. A second insert of the same `message_id` raises `IntegrityError`. `intake_apply` counts that row as `duplicates`.

Replay of a `REPLAYED` row with the same accepted `message_id` therefore returns `duplicates` 1. It does not insert a second inbox row. The parked row stays listed with status `REPLAYED`.

---

## SLOs and observability

JSON `duration_ms` on stdout is the time for that one request. Honesty: REAL when the line is captured. It is not API p95.

Retry-count floor stays Unknown. **Verified Fact.** FD-19.

Compose `retries: 5` only marks the container unhealthy. It is not this product's retry policy for intake or for the model.

---

## Cost and the 0C envelope

An extra gateway probe adds no model token. `MODEL_MODE=replay` spends 0 live tokens. Token lines B2 to B7 stay Unknown. This half claims no dollar benefit for the extra attempt.

---

## Exact Half B check

HB-28-01 is the park-and-replay check in `resilience-architecture.md`. This file does not add a second Half B check. Measured extra-attempt cells stay Unknown until a later run.

---

## What this file does not do

This file does not write `UPSTREAM_RETRY_COUNT` into code. It does not start Half B. It does not invent backoff milliseconds. It does not copy 99.5 percent availability. It does not call Azure.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
