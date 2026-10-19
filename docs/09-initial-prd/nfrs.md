# Non-functional requirements

| Field | Value |
|---|---|
| Stage | Phase 3 / 9 Initial PRD and product intent |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p3-doc-20261018-001 |
| Status | COMPLETE. Thresholds that are not in a governed source stay Unknown or PROPOSED. |
| Evidence sources | `docs/03-problem-value/nfrs.md`; `docs/08-ai-qualification/economics-baseline-reconciliation.md`; `Project_Intent.md` sections 12, 13, 14; `Execution_Plan.md` sections 9 and 10; FD-02, FD-04, FD-05, FD-14, BO-03, BO-10, BO-11; catalogue BP7, BP8 |
| Assumptions | Inherited SLO notes such as 99.5% availability stay historical. They are not this product's targets. Token, price, and latency cells that Phase 0C left Unknown stay Unknown. |
| Unresolved issues | Availability, API p95, retrieval p95, groundedness percent, abstention percent, RTO, and RPO stay Unknown. FD-11, FD-14, FD-18, and FD-19 are PENDING. |
| Residual risks | Copying 99.5% from inherited notes would invent a target. Putting a model cost on ranking, rules, reconcile, or de-duplication would restore retired lines R-P2-03 to R-P2-06. |

These are needs for both applications. They support BP1 to BP8. They do not add a ninth problem. They do not specify implementation code. No numeric SLO is invented on this page.

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

Worked example. 86 partner feeds contain `auto approve` or `disregard validation`. Those strings remain visible as flagged data. They do not close a case.

---

## Integrity and comparison

| Need | Statement | Target | Label | Linked problem |
|---|---|---|---|---|
| App independence | Each application runs without calling the other at run time | Required for scenario 13 | Verified Fact of Intent section 8 | BP4, BP5 |
| Same scenarios | Scenarios 7 to 11 run on both applications with the same inputs | Required | Verified Fact of Execution_Plan section 8 | BP1, BP2, BP3, BP6, BP8 |
| Same KPI families | Both applications use the eight families in Execution_Plan section 9 | Required. No invented target | Verified Fact. FD-03 | BO-02 headlines |
| Headline values | Exception cycle time and aged backlog | Unknown. Unknown. Not set as targets | Unknown | BP5 |
| Honesty labels | REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL on every demo number | In force now | Verified Fact | All |
| Rule source split | Application A reads rules from its rebuilt program. Application B reads rules only from the Context Lake | Required | Verified Fact of Execution_Plan section 4 | BP4 |
| ROI | No monetary benefit claim | BO-11 working answer | Verified Fact of the working answer | — |

Worked example. Application A marks a case queue. Application B marks the same case urgent. The scorecard names that difference and traces it to a missing or wrong lake item. That comparison still serves BP4.

---

## Identity, audit, and recovery

| Need | Statement | Target | Label | Linked problem |
|---|---|---|---|---|
| Identity on a case read or write | A reader of a case has an identity | Needed. Missing on the current GET API | Verified Fact that it is missing. Design later | BP8 |
| Approval recorded | Every hold, release, drop, policy pick, owner assign, and disposition records the actor | RT-01 to RT-06 | Verified Fact of the role map | BP1, BP2, BP6, BP8 |
| Audit later | One row per agent step and per approval, with a correlation id | FD-23 default. Design PENDING | Assumption of the default | BP8 |
| User-visible recovery | Retry and status after an outage or schema mismatch | Scenario 11 | Verified Fact of the demo job | BP8 |
| Separation of duties | The person who proposes an action is a different person from the person who approves it | BO-09 DECIDED | Verified Fact | BP1, BP8 |

This page does not specify ports as product requirements. Ports 8080, 8090, 8091, and 8092 remain later-phase facts.

---

## Operability of the laptop demo

| Need | Statement | Target | Label |
|---|---|---|---|
| 40-minute path | The section 10 flow runs on a laptop | Working demo flow. FD-21 later freezes it | Verified Fact of Execution_Plan section 10 |
| Offline replay | Planned demo mode plays back saved model responses | Assumption until Phase 15 | Assumption |
| Live tokens in replay | 0 if replay is used as designed | Assumption A-W2 from Phase 0C, still in force | Assumption |
| Health of later services | Needed when those services exist | Unknown latency | Unknown |
| Availability | Inherited note 99.5% | Not adopted | Unknown as a project target |
| Recovery time | Inherited note 8 hours | Not adopted | Unknown |
| Recovery point | Inherited note 24 hours | Not adopted | Unknown |
| API p95 | Needed later | Unknown (FD-11) | Unknown |

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

No groundedness percent is invented here.

---

## What this file does not do

This file does not invent a latency number, an availability percent, a citation percent, a cycle-time target, or a dollar benefit. It does not specify implementation code.
