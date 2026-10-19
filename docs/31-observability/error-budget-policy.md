# Error-budget policy

| Field | Value |
|---|---|
| Stage | Phase 13 / 31 Observability and service levels. Half B evidence. SC-31-01 / HB-31-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-31b-doc-20261018-001 |
| Status | MEASURED for the listed `replay_miss` line. The budget number SLO-N7 stays Unknown. |
| Evidence sources | FD-19; FD-11; `slo-sla-definitions.md`; `docs/12-specs/system-spec.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/28-resilience/failure-injection-results.md`; `apps/shared/jsonlog.py`; `apps/app_a/runtime/dlq.py` |
| Assumptions | `MODEL_MODE=replay`. BO rows that are PROPOSED stay PROPOSED. A numeric service level must exist before a numeric budget can exist. |
| Unresolved issues | Error-budget count SLO-N7 stays Unknown. Availability percent SLO-N4 stays Unknown. Company owner who may later spend a budget stays Unknown. |
| Residual risks | Writing a miss allowance as a percent would invent SLO-N7. Treating every HTTP 200 as budget remaining would hide parked failures. Deleting a parked row to keep the list small would hide a miss. |

This file names what an error budget is on this product and what a person does while the number is empty. An error budget is the count of allowed misses against a numeric service level. This product has no numeric service level. The budget number stays Unknown.

Engineering decision ED-P13-31A-04, authority: team-force. Policy id `EBP-31-01`. Until SLO-N4 or another numeric cell is filled, the person records each named failure as a listed event. The person does not compute a remaining percent. This rule is an engineering default. It is not Business Owner policy.

---

## Finding

**Finding.** FD-19 left availability, latency, recovery, and cost floors Unknown. SLO-N7 is the error-budget cell. It stays Unknown because SLO-N4 stays Unknown. Events that would count as misses against a future numeric cell already exist: identity miss, server key miss, forbidden role, lake write reject, intake park, replay miss, upstream probe 503, and injection BLOCK. HB-28-01 already keeps a parked intake listed after replay. This half invents no miss allowance.
**Evidence.** FD-19. FD-11. `slo-sla-definitions.md` SLO-N4 and SLO-N7. `jsonlog` event names. `failure-injection-results.md` REAL park rows.
**Impact.** Half B adds `event=replay_miss` so that miss is listed. Half B does not start a budget clock.
**Risk.** A later author who writes a miss allowance would skip FD-19.
**Confidence.** High on the empty cell and the named events. Unknown on a future numeric budget.
**Open questions.** Reviewer grades HB-31-01. Who may later set SLO-N4. SLO-N7 stays Unknown.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric latency, availability, error-budget, and recovery floors stay Unknown. A failed intake stays visible. Replay is the path when the live model is off. This half invents no percent and no dollar benefit.

**Verified Fact.** FD-11. Numeric availability percent stays Unknown.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

---

## What the person does while the number is empty

| Step | What the person does | What it produces |
|---|---|---|
| 1 | Keep `MODEL_MODE=replay` | No live model socket |
| 2 | Grep stdout for `event` names in the miss table | A list of lines for that run |
| 3 | Open `GET /api/recovery` | Parked intake rows stay listed |
| 4 | Open `GET /api/audit/{correlation_id}` | Agent steps and approvals for that id |
| 5 | Leave SLO-N7 Unknown | No invented percent |

Worked example. One identity miss writes `event=identity_missing` and HTTP 401. One health GET writes `event=health_ok` and HTTP 200. Those two lines are two events. They do not become an availability percent. **Verified Fact.** FD-19.

---

## Events that would consume a future budget

These events stay listed today. They become budget spends only after a later decision fills SLO-N4 or another numeric cell.

| Event or result | Where it lives | Why it would count later | Why it does not fill SLO-N7 today |
|---|---|---|---|
| `identity_missing` | stdout | A gated read or write was refused | No availability floor exists |
| `server_key_missing` | stdout | The process has no key | Same |
| `forbidden_role` | stdout | Role missed the action | Same |
| `lake_write_rejected` | stdout | A write method hit a read listener | Same |
| `intake_parked` | stdout and dead-letter file | Intake failed the schema | Same |
| `replay_miss` after Half B | stdout | The model path abstained | Same |
| Probe HTTP 503 | Recovery probe | Upstream timeout, schema, or throttle | Same |
| HTTP 409 `blocked` | Query or agent | Injection stopped a write | A block is a control success for SLO-B3 |

Worked example. HB-28-01 parked `message_id` `DLQ-28-BAD`. `GET /api/recovery` listed `status` `PARKED`. Replay of that same body stayed `PARKED`. The row stayed in `parked_intakes`. Honesty: REAL. That listed row is a visible miss for intake. It is not a percent of SLO-N7.

HTTP 409 `blocked` is the injection stop. Count it as SLO-B3 held. Do not treat that 409 as an availability miss. **Verified Fact.** FD-18. SLO-B3.

---

## Events that stay successes for process up

| Event or result | What it means |
|---|---|
| `health_ok` HTTP 200 | That process accepted a GET |
| `request_ok` HTTP 200 with `verdict=ABSTAIN` | The read worked and knowledge was missing |
| `intake_replayed` with the row still listed | Replay ran and the original failure stayed visible |
| Audit rows present for a correlation id | SLO-B10 held for that id |

`request_ok` with HTTP 401 does not occur. Identity miss uses `identity_missing`. **Verified Fact.** middleware return before `call_next`.

---

## Release rule while the number is empty

| Check | Go | No-go |
|---|---|---|
| Named failure is visible | The event line or parked row exists | The failure was deleted or hidden |
| Replay stays on | `MODEL_MODE=replay` | Azure variables set to force a live call |
| Numeric cell | SLO-N7 left Unknown | A percent written as a floor |
| BO row | Stays PROPOSED | A demo name signed as owner of a budget |

These are engineering checks. They are not a customer agreement. **Verified Fact.** FD-19. BO rows PROPOSED.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-31-05 | A percent is written into SLO-N7 | A later file shows a miss allowance | Leave SLO-N7 Unknown |
| FM-31-08 | A parked row is deleted | Recovery list looks empty | Restore the sqlite file. Leave the row |
| EBP-hide-409 | Injection 409 is counted as downtime | A miss tally rises on a control success | Keep 409 as SLO-B3 held |
| EBP-health-ratio | Person divides health 200 by probe 503 | A homemade percent | Leave SLO-N4 Unknown |

Dead-letter replay stays as built. Replay of `DLQ-28-BAD` keeps `PARKED`. That listed row is the recovery for the intake miss.

---

## SLOs and observability

| Signal | What it proves | What it does not prove |
|---|---|---|
| Listed `event` lines | Those misses happened | SLO-N7 |
| Parked row still listed | FD-19 intake visibility | An availability percent |
| `event=replay_miss` after Half B | The model miss is listed | A token budget |
| Empty SLO-N7 cell | The policy held | A signed agreement |

---

## Cost and the 0C envelope

An error budget counts misses against a numeric service level. Token line B1 stays 0 and 0 under replay. Lines B2 to B7 stay Unknown. This half claims no dollar benefit. **Verified Fact.** FD-19. BO-11 working answer stays PROPOSED.

---

## Half B check

HB-31-01 added the `replay_miss` line so that miss is listed. Before: the miss lived on the HTTP body only. Honesty: REAL. After: stdout also carries `event=replay_miss`. Honesty: REAL in `telemetry-results.md`. SLO-N7 stays Unknown.

---

## What this file does not do

This file does not invent a miss allowance. It does not start a burn clock. It does not sign a Business Owner row. It does not write code.
