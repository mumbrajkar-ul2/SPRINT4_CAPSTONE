# Service level and agreement definitions

| Field | Value |
|---|---|
| Stage | Phase 13 / 31 Observability and service levels. Half B evidence. SC-31-01 / HB-31-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-31b-doc-20261018-001 |
| Status | MEASURED for HB-31-01. Numeric floors SLO-N1 to SLO-N8 stay Unknown. |
| Evidence sources | FD-19; FD-11; `docs/12-specs/system-spec.md`; `docs/17-implementation-prd/finalized-nfrs.md`; `docs/09-initial-prd/nfrs.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `Decision_Tracker.md` BO rows; `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/docs/operations-service-levels.md` |
| Assumptions | `MODEL_MODE=replay`. BO rows that are PROPOSED stay PROPOSED. Inherited service notes stay historical. |
| Unresolved issues | API p95, retrieval p95, agent completion time, availability percent, recovery time, recovery point, error-budget count, and token cost stay Unknown. Company signer stays Unknown. |
| Residual risks | Copying an inherited availability note into a target would skip FD-19 and FD-11. Treating `/health` 200 as a signed agreement would invent a customer promise. Filling a Business Owner cell with a demo name would invent a signer. |

This file names the service levels this product already uses and the numeric cells that stay empty. A service level is a behaviour or a measured number the team watches. An agreement is a signed promise to a customer. This laptop stack has behavioural service levels. It has no signed customer agreement.

Engineering decision ED-P13-31A-03, authority: team-force. Behavioural ids stay `SLO-B1` to `SLO-B10` from `system-spec.md`. Numeric ids `SLO-N1` to `SLO-N8` name the empty cells. Those eight cells stay Unknown. This half invents no percent and no millisecond target.

---

## Finding

**Finding.** FD-11 already specified HTTP, events, errors, and behavioural service needs. SLO-B1 to SLO-B10 are those behaviours. FD-19 left numeric latency, availability, recovery, retry, and cost floors Unknown. The inherited operations file records older planning notes for scheduled-hour availability, recovery time, and recovery point. Those notes stay historical. This half does not copy them as floors. No Business Owner row signs a customer agreement. BO rows stay PROPOSED.
**Evidence.** `system-spec.md` SLO-B1 to SLO-B10. FD-11 decided text. FD-19 decided text. `quality-latency-cost-envelope.md` empty numeric cells. `Decision_Tracker.md` BO status PROPOSED. Inherited `operations-service-levels.md` historical notes.
**Impact.** Half B proves one telemetry line. That line supports the miss path. It does not fill a numeric cell.
**Risk.** A later author who writes a percent into SLO-N4 would treat FD-19 as a made-up target.
**Confidence.** High on the behavioural list and the empty numeric cells. Unknown on a future measured run.
**Open questions.** Reviewer grades HB-31-01. Who may later sign an agreement. SLO-N1 to SLO-N8 stay Unknown.

---

## Locked facts this design applies

**Verified Fact.** FD-11. Specify contracts and behavioural service needs. Keep every numeric latency, availability percent, recovery time, recovery point, API p95, retrieval p95, groundedness percent, citation percent, and abstention percent as Unknown.

**Verified Fact.** FD-19. Numeric latency, availability, recovery-time, recovery-point, retry-count, and cost floors stay Unknown. Do not invent a percent or a dollar benefit.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. This half invents no signer.

---

## Words this file uses

| Word | What it means on this product |
|---|---|
| Service level | A behaviour the apps must keep, or a numeric cell the team may later fill |
| Behavioural service level | SLO-B1 to SLO-B10. A person can check the behaviour on one request |
| Numeric service level | SLO-N1 to SLO-N8. The number stays Unknown |
| Agreement | A signed customer promise. None exists on this laptop stack |
| Error budget | Room left after misses against a numeric service level. The number stays Unknown. See `error-budget-policy.md` |

Worked example. `GET /health` on 8100 returns HTTP 200. That check is SLO-B behaviour for process up. It does not fill SLO-N4 availability.

---

## Behavioural service levels

**Verified Fact.** `system-spec.md`. `finalized-nfrs.md`.

| Id | Behaviour | How a person checks it today | Numeric floor |
|---|---|---|---|
| SLO-B1 | A person approves every record-changing action | `POST /api/approvals` plus an audit `human_approval` row | None invented |
| SLO-B2 | The proposer and the approver are different people | Audit columns `proposed_by` and `actor_id` differ | None invented |
| SLO-B3 | Untrusted approve-or-ignore text stays data. Injection returns BLOCK | HTTP 409 `error_class=blocked`. `EV-12` | None invented |
| SLO-B4 | A GenAI answer cites a lake item or abstains | Query body `citations` or `verdict=ABSTAIN` | Percent stays Unknown |
| SLO-B5 | Application B takes rules only from the lake | Application B does not import Application A rule functions | None invented |
| SLO-B6 | The two applications do not call each other at run time | Ports 8100 and 8110 stay separate | None invented |
| SLO-B7 | Event time and arrival time stay two fields | Audit columns `occurred_at` and `recorded_at` | None invented |
| SLO-B8 | REVIEW and HOLD count as open | Queue and case status fields already coded | None invented |
| SLO-B9 | A reader of a case on Application A or Application B has an identity | HTTP 401 or 503 without headers or without the process key | None invented |
| SLO-B10 | Every agent step and every human approval writes an audit row keyed by a correlation id | `GET /api/audit/{correlation_id}` | None invented |

Worked example for SLO-B4. `POST /api/query` with a replay miss returns `verdict` `ABSTAIN` and empty or existing citations from retrieve. After HB-31-01, stdout also has `event=replay_miss`. That pair proves the miss stayed local. It does not prove a citation percent.

Worked example for SLO-B9. `GET /api/identity-check` with no headers returns HTTP 401. Stdout `event=identity_missing`. Honesty: REAL in `test_logs.py`.

---

## Numeric service levels that stay Unknown

Engineering decision ED-P13-31A-03 continued, authority: team-force.

| Id | Cell | Value on this page | What would fill it later | What must not fill it |
|---|---|---|---|---|
| SLO-N1 | API p95 | Unknown | A measured set of `duration_ms` values plus a later decision | One `duration_ms` on one line |
| SLO-N2 | Retrieval p95 | Unknown | A measured retrieve set plus a later decision | The 5 second client timeout in `retrieve.py` |
| SLO-N3 | Agent completion time | Unknown | A measured graph set plus a later decision | Recursion limit 12 |
| SLO-N4 | Availability percent | Unknown | A measured up or down series plus a later decision | One `/health` 200. An inherited scheduled-hour note |
| SLO-N5 | Recovery time | Unknown | A measured restore plus a later decision | An inherited 8-hour note |
| SLO-N6 | Recovery point | Unknown | A measured backup age plus a later decision | An inherited 24-hour note |
| SLO-N7 | Error-budget count | Unknown | SLO-N4 or another numeric cell plus a later decision | A guessed miss count |
| SLO-N8 | Token cost | Unknown | Measured tokens on a live path plus a later decision | Line B1 0/0 presented as a saving |

Client timeouts already in code stay client timeouts. Gateway probe 3 seconds. Lake retrieve HTTP 5 seconds. OPA eval 15 seconds. Azure complete 30 seconds. This half does not call Azure. Those integers are not SLO-N1 to SLO-N3. **Verified Fact.** `timeout-retry-policy.md`. FD-19.

---

## Agreement status

| Item | Status | Label |
|---|---|---|
| Laptop engineering go list | GNG-30-01 to GNG-30-10 already named | Verified Fact of sub-stage 30 |
| Customer availability agreement | None written | Unknown |
| Customer recovery agreement | None written | Unknown |
| Business Owner production sign-off | BO rows PROPOSED | Verified Fact of the tracker |

A go under GNG-30-01 to GNG-30-10 is an engineering check for this laptop stack. It is not a signed company launch. **Verified Fact.** `go-no-go-criteria.md`.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-31-04 | Person treats one `duration_ms` as SLO-N1 | A millisecond on one line | Leave SLO-N1 Unknown |
| FM-31-05 | Person copies an inherited availability note into SLO-N4 | A percent appears in a later file | Leave SLO-N4 Unknown |
| SLO-health-only | Person treats health 200 as an agreement | Compose healthy | Read this table. Health proves process up for that GET |
| SLO-freeze-copy | Person copies 42 of 42 into a citation percent | A freeze score | Leave the citation percent Unknown. FD-14 |

---

## SLOs and observability

| Id | Signal that supports it | What that signal does not prove |
|---|---|---|
| SLO-B1 | Audit `human_approval` | A cycle-time floor |
| SLO-B3 | HTTP 409 and `EV-12` | An availability percent |
| SLO-B4 | Query `citations` or `ABSTAIN`, plus `event=replay_miss` after Half B | A citation percent |
| SLO-B9 | `event=identity_missing` or `server_key_missing` | An error-budget percent |
| SLO-B10 | `GET /api/audit/{id}` rows | Agent p95 |
| SLO-N1 to SLO-N8 | No supporting numeric series exists | Any floor |

---

## Cost and the 0C envelope

Numeric cost stays SLO-N8 Unknown. Line B1 stays 0 and 0 under replay. Lines B2 to B7 stay Unknown. Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED. This half claims no dollar benefit. **Verified Fact.** FD-19. BO-11 working answer stays PROPOSED.

---

## Half B check

HB-31-01 proved the `replay_miss` line. Honesty: REAL in `telemetry-results.md`. That line supports SLO-B4 on the miss path. It does not fill SLO-N1 to SLO-N8. Those eight cells stay Unknown.

---

## What this file does not do

This file does not invent a percent. It does not copy an inherited availability note as a floor. It does not sign a Business Owner row. It does not write code.
