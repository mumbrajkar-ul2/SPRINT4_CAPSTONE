# Non-goals

| Field | Value |
|---|---|
| Stage | Phase 3 / 9 Initial PRD and product intent |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p3-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED with the initial PRD. |
| Evidence sources | `docs/03-problem-value/scope-exclusions.md`; `docs/00-preflight/operating-contract/scope-boundaries.md`; `Execution_Plan.md` sections 3 and 11; `Project_Intent.md` sections 10.2, 14.1, 17.4; BO-03, BO-04, BO-06b, BO-08, BO-11; FD-01, FD-02, FD-04, FD-05 |
| Assumptions | The eight business problems remain the product boundary. Later phases implement this boundary. They do not widen it. |
| Unresolved issues | BO-04 stays unsigned. A later owner could still reject the working answer. That would reopen this list. |
| Residual risks | An interesting feature that sits outside BP1 to BP8 can grow the work past a 40-minute laptop demo. |

This file names what the product will not do. Scope stays on BP1 to BP8. This file does not specify implementation code.

---

## Out of product scope

| Exclusion | Why | Label |
|---|---|---|
| Any business problem beyond BP1 to BP8 | BO-04 working answer. Execution_Plan section 3 is the problem list | Verified Fact |
| Any other repository | FD-01. The inherited Fabpulse simulator is the system under change | Verified Fact |
| Real production fab control | Educational simulator | Verified Fact |
| Real personal or customer data | FD-02 | Verified Fact |
| Write tools for the model | FD-02. BO-03 working answer | Verified Fact |
| A model writing a case, a hold, a feed status, or an owner | BO-03: a person approves every record-changing action | Verified Fact of the working answer |
| Language-model ranking of the queue | FD-04. Ranking is a written test on stored fields | Verified Fact |
| Language-model pass-or-fail on a rule | FD-04. Four programs already disagree (BP4) | Verified Fact |
| Language-model accept, reject, or duplicate on a feed | FD-04. `reconcile()` is written comparisons | Verified Fact |
| Language-model duplicate mark from text similarity | FD-04. Duplicate is an identifier or REPLAY status test | Verified Fact |
| Production machine-learning prediction of `engineering_hold` | FD-05. Majority and leave-one-out are both 117/125. Honesty: REAL | Verified Fact |
| Invented KPI targets or dollar benefits | Project_Intent 14.1. BO-02. BO-11 | Verified Fact |
| Merging operational, finance, and audit closed into one state | BO-06b working answer keeps them separate | Verified Fact of the working answer |
| The 999,999 JavaScript default as a live policy number | BO-08 working answer | Verified Fact of the working answer |
| Inventing a number where the governed source is silent | BO-08. Route the case to review | Verified Fact of the working answer |
| Workshop 500k and stress 2M lake tiers as this demo's data | Not packaged | Verified Fact |
| Official Birlasoft brand files as a Phase 3 deliverable | Not in hand. BO-12 is later | Verified Fact |
| A signed initial PRD in this unit | BO-04 stays PROPOSED. This folder stays UNSIGNED | Verified Fact |
| Named signer, named incident owner, or mapped company job titles invented here | Those values are Unknown | Unknown |
| Specifying implementation code in this PRD | Phase 3 constraint | Verified Fact |

Worked example. Predicting `engineering_hold` from `wafer_count`, `defect_count`, and `measured_yield` scored 117 of 125. Always guessing "not held" also scored 117 of 125. A hold scorer is a non-goal.

Worked example. 86 feeds tell a reader to auto-approve. Building a path that follows that text would be a ninth, unsafe behavior. Isolating that text as data is in scope (BP7). Following it is out of scope.

---

## In scope, restated

The eight defects BP1 to BP8. Demo scenarios 7 to 13. Application A and Application B. The Context Lake as the only rule source for Application B. Code for ranking, rules, reconcile, and de-duplication. A language model for explanation, natural-language answers, and draft plans. A person on every record-changing action. The 40-minute flow. The eight KPI families with Unknown headlines and no invented targets.

---

## What later phases may still build

Identity design, lake item schema, contracts, recovery mechanics, and the parity harness are later. They still serve BP1 to BP8. They are absent from this PRD as code. They are not listed as non-goals of the whole engagement.

Ports 8080, 8090, 8091, and 8092 are later-phase facts. This file does not make them product features. It also does not exclude them from later build phases.

---

## What this file does not do

This file does not add a feature. It does not sign BO-04. It does not invent a target percent or a dollar benefit.
