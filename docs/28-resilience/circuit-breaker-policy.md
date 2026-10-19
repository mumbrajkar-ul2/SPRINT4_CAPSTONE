# Circuit policy

| Field | Value |
|---|---|
| Stage | Phase 13 / 28 Reliability and resilience. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-28a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No circuit flag in this half. |
| Evidence sources | FD-19; ED-P13-28A-01; `apps/app_a/routes/recovery.py`; `docs/12-specs/error-handling-spec.md`; `docs/21-integration/failure-semantics.md` |
| Assumptions | `MODEL_MODE=replay`. The extra-attempt default of 1 is the only new integer this concern names. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Availability percent stays Unknown. Open-duration seconds stay Unknown. Measured circuit cells stay Unknown. HB-28-01 does not require this flag. |
| Residual risks | Setting the flag on OPA BLOCK would hide injection. Setting the flag on schema would skip a readable mismatch. A second invented failure count would look like a retry floor. |

This file names a process flag on Application A. After both gateway probe attempts fail with timeout or throttle, Application A skips the next call to port 8090. The person still sees the earlier failures.

Engineering decision ED-P13-28A-04, authority: team-force. The flag becomes set when `UPSTREAM_RETRY_COUNT` 1 is exhausted on `upstream_timeout` or `upstream_rate_limit`. There is no second failure-count integer. Seconds until the flag clears by itself stay Unknown. A `mode=normal` probe is the trial that clears the flag.

---

## Finding

**Finding.** Application A calls the source gateway on every probe today. `_LAST` keeps the last visible status. There is no skip flag. This half names one flag that uses the same retry default. Half B may leave the flag unwired. HB-28-01 still passes on park and replay.
**Evidence.** `probe_gateway` always calls 8090 when `SOURCE_GATEWAY_URL` is set. Local fixture `_simulate` always returns a body. FD-19.
**Impact.** Operators can read `error_class: circuit_open` later without a new product.
**Risk.** Treating open duration as an 8-hour recovery target would copy the inherited note.
**Confidence.** High on the need to skip a dead probe. Unknown on measured skip counts.
**Open questions.** HALF_A_ACCEPTED. Open-duration seconds.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Availability stays Unknown. Recovery-time stays Unknown. Replay is the path when the live model is off.

**Verified Fact.** Injection still BLOCKS. The circuit flag does not change OPA.

**Verified Fact.** `WRITE_TOOLS` is `[]`. The model cannot clear or set this flag.

---

## Flag states

| State | What Application A does | How it gets here | How it leaves |
|---|---|---|---|
| Clear | Probe runs as today, plus the one extra attempt on timeout or throttle | Process start. Or a trial probe returned HTTP 200 | Two failed timeout or throttle attempts in one probe set the flag |
| Set | Skip port 8090. Return `error_class: circuit_open`. Recovery GET stays HTTP 200. `retry_shown` true. Earlier `error_class` stays in the body | Extra attempt exhausted on timeout or throttle | A `mode=normal` probe is allowed as the trial |
| Trial | One `mode=normal` probe is sent | Caller asks for `mode=normal` while the flag is set | HTTP 200 clears the flag. Timeout or throttle leaves it set |

Worked example. Probe `mode=timeout` fails at 3 seconds. The extra attempt also fails at 3 seconds. `attempt_count` is 2. The flag becomes set. The next probe with `mode=timeout` does not open a socket. The body says `circuit_open` and still names the first `upstream_timeout`. `GET /api/recovery` stays HTTP 200. The person can still read the failure.

Worked example. While the flag is set, `GET /api/recovery/probe?mode=normal` is the trial. The fixture returns HTTP 200. The flag becomes clear. `error_class` is `none`. `retry_shown` is false.

---

## What does not set the flag

| Event | Flag | What the person sees |
|---|---|---|
| `upstream_schema` | Stays clear | HTTP 503. Retry visible. No extra attempt |
| Identity 401 or 503 `missing_server_key` | Stays clear | Same request returns. Health stays 200 |
| OPA BLOCK | Stays clear | HTTP 409. Case unchanged |
| `replay_miss` | Stays clear | Abstain. No Azure call |
| Invalid intake | Stays clear | SC-28-01 parks the row |
| Lake abstain | Stays clear | HTTP 200 `verdict: ABSTAIN` |
| Graph HOLD_FOR_REVIEW | Stays clear | Person at the mapped RT role |

---

## Dead-letter queue and replay

The circuit flag is not the dead-letter store. A skipped probe is not parked as intake.

Intake parking stays SC-28-01 in `apps/app_a/runtime/dlq.sqlite3`.

---

## Runbook — clear a set flag

1. `GET /api/recovery`. If `error_class` is `circuit_open`, read `first_error_class` and `attempt_count`.
2. Confirm `/health` on 8100 is HTTP 200. Confirm `/health` on 8090 if the gateway should be up.
3. Send `GET /api/recovery/probe?mode=normal` with the three identity headers.
4. If that trial is HTTP 200, the flag is clear.
5. If that trial is HTTP 503, the flag stays set. The failure stays visible.

A copy of this runbook into `operations/` belongs to sub-stage 29.

---

## SLOs and observability

| Signal | What it proves | What it does not prove |
|---|---|---|
| `error_class: circuit_open` | This process skipped 8090 after two failed attempts | An availability percent |
| `attempt_count` 2 | Both attempts ran before the skip | A retry-count floor |
| `/health` 200 | The process is up | Recovery-time |

Open-duration seconds stay Unknown. This half invents no clock that auto-clears the flag.

---

## Cost and the 0C envelope

Skipping a probe adds no model token. Token line B1 stays 0 and 0 in replay. This half claims no dollar benefit for skipped calls.

---

## Exact Half B check

HB-28-01 is park and replay. Measured circuit cells stay Unknown. Half B may leave this flag unwired.

---

## What this file does not do

This file does not write the flag. It does not start Half B. It does not invent an open-duration number. It does not apply the flag to Azure, the lake, or OPA.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
