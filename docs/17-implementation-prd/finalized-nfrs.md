# Finalized non-functional requirements

| Field | Value |
|---|---|
| Stage | Phase 8 / 17 Implementation PRD. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Numeric percents stay Unknown. BO rows that are PROPOSED stay PROPOSED. |
| Evidence sources | `docs/09-initial-prd/nfrs.md`; `docs/12-specs/system-spec.md`; `docs/17-implementation-prd/implementation-prd.md`; `Execution_Plan.md` sections 9 and 10; FD-02, FD-03, FD-11, FD-13, BO-03, BO-10 |
| Assumptions | Inherited 99.5 percent availability stays historical. It is not this product's target. Token, price, and latency cells that Phase 0C left Unknown stay Unknown. |
| Unresolved issues | Availability, API p95, retrieval p95, groundedness percent, abstention percent, recovery time, and recovery point stay Unknown. FD-14, FD-18, and FD-19 stay later. |
| Residual risks | Copying 99.5 percent from inherited notes would invent a target. Putting a model cost on ranking, rules, reconcile, or de-duplication would restore retired lines R-P2-03 to R-P2-06. |

These are needs for both applications and for the Phase 8 platform. They support BP1 to BP8. They do not add a ninth problem. No numeric SLO is invented on this page.

---

## Finding

**Finding.** Behavioural needs from the Initial PRD still bind. Identity format and the two app host ports are now named. Every numeric service percent stays Unknown.
**Evidence.** `docs/09-initial-prd/nfrs.md`. `system-spec.md` SLO-B1 to SLO-B10. ED-P8A-01. ED-P8A-02.
**Impact.** Half B can test health, identity 401, and replay without a latency floor.
**Risk.** A later author who writes 99.5 percent into compose would treat a historical note as a signed target.
**Confidence.** High on the behaviours. Unknown on the empty numeric cells.
**Open questions.** FD-14, FD-18, FD-19 measured values.

---

## Safety and data

| Need | Statement | Target | Label | Linked problem |
|---|---|---|---|---|
| Local synthetic records | All records stay local and synthetic | In force now (FD-02) | Verified Fact | BP8 |
| Model tools | Read-only | In force now (FD-02) | Verified Fact | BP7, BP8 |
| Record writes | A person approves each one | BO-03 working answer. Unsigned | Verified Fact of the working answer | BP1, BP2, BP6, BP8 |
| Untrusted text | Feed, email, and document text is data | Catalogue BP7 counts. Honesty: REAL | Verified Fact | BP7 |
| Classification | Internal synthetic. Process data confidential. No personal data | BO-10 working answer. Unsigned | Assumption of the working answer | BP8 |
| Hold prediction | No production machine-learning scorer | FD-05 Reject ML. 117/125 versus 117/125. Honesty: REAL | Verified Fact | BP1 |
| Secrets | Shared key from `FABPULSE_API_KEY`. Documented local default `local-demo-only` in `.env.example` | Required for Phase 8 | Inference. ED-P8A-02 | BP8 |

Worked example. 86 partner feeds contain `auto approve` or `disregard validation`. Those strings remain visible as flagged data. They do not close a case.

---

## Integrity and comparison

| Need | Statement | Target | Label | Linked problem |
|---|---|---|---|---|
| App independence | Each application runs without calling the other at run time | Required for scenario 13 | Verified Fact | BP4, BP5 |
| Same scenarios | Scenarios 7 to 11 run on both applications with the same inputs | Required | Verified Fact | BP1, BP2, BP3, BP6, BP8 |
| Same KPI families | Both applications use the eight families in Execution_Plan section 9 | Required. No invented target | Verified Fact. FD-03 | BO-02 headlines |
| Headline values | Exception cycle time and aged backlog | Unknown. Unknown. Not set as targets | Unknown | BP5 |
| Honesty labels | REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL on every demo number | In force now | Verified Fact | All |
| Rule source split | Application A reads rules from its rebuilt program. Application B reads rules only from the Context Lake | Required | Verified Fact | BP4 |
| ROI | No monetary benefit claim | BO-11 working answer | Verified Fact of the working answer | — |
| Host ports | Application A 8100. Application B 8110 | Named now | Inference. ED-P8A-01 | Demo operability |

Worked example. Application A marks a case queue. Application B marks the same case urgent. The scorecard names that difference and traces it to a missing or wrong lake item. Phase 8 only guarantees the two apps listen on different ports so that comparison can run later.

---

## Identity, audit, and recovery

| Need | Statement | Target | Label | Linked problem |
|---|---|---|---|---|
| Identity on a case read or write | Application A and Application B require `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role` | Named now. HTTP 401 when missing | Inference of headers. Verified Fact of 401 | BP8 |
| Legacy baseline | Port 8080 serves cases with no identity check | Current behaviour. CT-35 | Verified Fact | BP8 |
| Gateway fixture | Port 8090 stays without an identity check | Inherited failure modes | Verified Fact of the fixture. Inference to keep it open | BP8 |
| Lake reads | Ports 8091 and 8092 require `X-Api-Key` except health | Named now | Inference. ED-P8A-04 | BP8 |
| Approval recorded | Every hold, release, drop, policy pick, owner assign, and disposition records the actor | RT-01 to RT-06. Feature later | Verified Fact of the role map | BP1, BP2, BP6, BP8 |
| Audit later | One row per agent step and per approval, with a correlation id | FD-23 default. Schema later | Assumption of the default | BP8 |
| Request logs | JSON lines on stdout with `service`, `event`, `correlation_id` | Required for Phase 8 | Inference. ED-P8A-07 | Operability |
| User-visible recovery | Retry and status after an outage or schema mismatch | Scenario 11. Feature later | Verified Fact of the demo job | BP8 |
| Separation of duties | The person who proposes an action is a different person from the person who approves it | BO-09 DECIDED | Verified Fact | BP1, BP8 |

This page now specifies ports as platform facts. It still does not make ports a ninth business problem.

---

## Operability of the laptop demo

| Need | Statement | Target | Label |
|---|---|---|---|
| One command | `docker compose up` starts 8080, 8090, 8091, 8092, 8100, and 8110 | Required | Verified Fact of section 10. Inference of 8100 and 8110 |
| 40-minute path | The section 10 flow runs on a laptop | Working demo flow. FD-21 later freezes it | Verified Fact of Execution_Plan section 10 |
| Offline replay | `MODEL_MODE=replay` plays back the file named by the SHA-256 hash of the prompt | Required wiring in Phase 8 | Verified Fact of section 10. Inference of the directory |
| Missing replay file | Structured error. No public-network call. No invented sentence | Required | Inference. ED-P8A-08 |
| Live tokens in replay | 0 if replay is used as designed | Assumption A-W2 from Phase 0C, still in force | Assumption |
| Health of the six listeners | `GET /health` returns 200 with `{ "ok": true }` | Required when those services exist | Inference of the body. Verified Fact that health exists on 8080 and 8090 today |
| Availability | Inherited note 99.5 percent | Not adopted | Unknown as a project target |
| Recovery time | Inherited note 8 hours | Not adopted | Unknown |
| Recovery point | Inherited note 24 hours | Not adopted | Unknown |
| API p95 | Needed later | Unknown (FD-19) | Unknown |

Worked example. Compose marks `app-a` healthy when `http://127.0.0.1:8100/health` returns 200. That check does not claim a 200-millisecond p95.

---

## Language-model quality

These rows apply only to conflict explanation, natural-language query, and agentic planning.

| Need | Statement | Target | Label |
|---|---|---|---|
| Citations | A GenAI answer cites a stored row or a lake item | Required as a behavior. Percent floor Unknown (FD-14) | Unknown for the number. Verified Fact for the behavior |
| Abstention | If retrieval returns nothing, or policies overlap, the model waits | Working rule. Percent floor Unknown (FD-18) | Assumption of the working rule |
| Untrusted instruction | Approve-or-ignore text stays data. The case waits for a person | Required. BP7 | Verified Fact |
| Token cost | Prompt and completion tokens | Unknown. Phase 13 may fill when measured | Unknown |
| Model cost on code paths | Ranking, rule pass-or-fail, reconciliation, and de-duplication have no model-cost line | Retired as R-P2-03 to R-P2-06 | Verified Fact of the Phase 2 reconciliation |
| Replay honesty | Tell the audience when replay is on | Required by section 10 | Verified Fact |

No groundedness percent is invented here.

---

## Behavioural service needs carried forward

**Verified Fact.** `docs/12-specs/system-spec.md` SLO-B1 to SLO-B10.

| Id | Behaviour | Phase 8 change |
|---|---|---|
| SLO-B1 | A person approves every record-changing action | Unchanged. Feature later. BO-03 still PROPOSED |
| SLO-B2 | The proposer and the approver are different people | Unchanged. Enforced when `POST /api/approvals` is built |
| SLO-B3 | Untrusted approve-or-ignore text stays data | Unchanged |
| SLO-B4 | A GenAI answer cites a stored row or a lake item, or the model abstains | Unchanged. Percent still Unknown |
| SLO-B5 | Application B takes rules only from the lake | Unchanged. Lake listeners added in Phase 8 |
| SLO-B6 | The two applications do not call each other at run time | Unchanged. Separate ports 8100 and 8110 |
| SLO-B7 | Event time and arrival time stay two fields | Unchanged. Feature later |
| SLO-B8 | REVIEW and HOLD count as open | Unchanged |
| SLO-B9 | A reader of a case on Application A or Application B has an identity | Mechanism named. Probe in Phase 8. Case body later |
| SLO-B10 | Every agent step and every human approval writes an audit row keyed by a correlation id | Schema still FD-23. Request logs are not that row |

---

## Numeric service cells that stay Unknown

**Unknown.** `docs/09-initial-prd/nfrs.md`. FD-11. FD-14, FD-18, FD-19 still later.

| Cell | Value on this page | Why it stays open |
|---|---|---|
| API p95 | Unknown | No governed source states a millisecond target |
| Retrieval p95 | Unknown | Same |
| Agent step time | Unknown | Same |
| Availability percent | Unknown | Inherited 99.5 percent is not adopted |
| Recovery time | Unknown | Inherited 8 hours is not adopted |
| Recovery point | Unknown | Inherited 24 hours is not adopted |
| Groundedness percent | Unknown | FD-14 PENDING |
| Citation percent floor | Unknown | FD-14 PENDING |
| Abstention percent floor | Unknown | FD-18 PENDING |
| Exception cycle time | Unknown | BO-02. No start and end fields signed |
| Aged backlog cutoff | Unknown | No age in days is signed |
| Token cost | Unknown | Phase 13 may fill when measured |

`duration_ms` on a log line is a measured field when Half B runs. It is not a target.

---

## What this file does not do

This file does not invent a latency number, an availability percent, a citation percent, a cycle-time target, or a dollar benefit. It does not write compose or CI files. It does not sign a Business Owner row.
