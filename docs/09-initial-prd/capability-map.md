# Capability map

| Field | Value |
|---|---|
| Stage | Phase 3 / 9 Initial PRD and product intent |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p3-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED with the initial PRD. |
| Evidence sources | `docs/08-ai-qualification/ai-vs-no-ai-matrix.md`; `docs/08-ai-qualification/qualification-decision.md`; `docs/08-ai-qualification/deterministic-vs-ai-boundaries.md`; `docs/05-current-state/conflict-catalogue.md`; `Execution_Plan.md` sections 3, 8, 10; `Decision_Tracker.md` FD-04, FD-05, BO-03, section 7 |
| Assumptions | FD-04 labels stay in force. Application A and Application B share this map. Application B reads rules only from the Context Lake. |
| Unresolved issues | FD-14 citation floors stay Unknown. FD-15 tool bounds stay PENDING. Live question wording beyond scenarios 7 to 13 is Unknown. |
| Residual risks | Copying a language-model label onto ranking, rule pass-or-fail, reconciliation, or de-duplication would add a fifth written test of the same rule (BP4). |

This file maps each product capability to an application, a business problem, a demo scenario, and the Phase 2 intelligence label. It does not specify code.

---

## How to read the labels

**Verified Fact.** FD-04 DECIDED.

- **Code.** A written test on stored fields returns one result. The same inputs give the same output.
- **Language model.** A model drafts text, a summary, or a plan from retrieved records. A person still approves any write.
- **Person.** A named run-time role accepts, holds, or blocks a record-changing action.
- **Rejected.** No production model is built.

Application A and Application B both expose F-01 to F-14. F-15 is Application B's context view. Application A still evaluates the same rule from its rebuilt program.

---

## Capability grid

| ID | Capability | Application A | Application B | Intelligence | Primary problem | Demo |
|---|---|---|---|---|---|---|
| F-01 | Recipe mismatch detection and approval route | Yes | Yes | Code raises the flag. Language model drafts the sentence. Person at RT-03 approves | BP1 | S8 |
| F-02 | Replay duplicate detection and confirmation | Yes | Yes | Code marks duplicate. Language model explains. Person at RT-05 confirms | BP2 | S7 |
| F-03 | Event time and arrival time kept apart | Yes | Yes | Code keeps two fields. Language model explains a late result | BP3 | S9 |
| F-04 | One governed rule evaluation | Yes, from rebuilt program | Yes, from the Context Lake only | Code | BP4 | S12 |
| F-05 | Open and closed shown with one operational meaning | Yes | Yes | Code uses the SME meaning. REVIEW and HOLD stay open | BP5 | S13 |
| F-06 | Overlapping policy detect and abstain | Yes | Yes | Code detects overlap. Language model names it. Person at RT-04 picks | BP6 | S10 |
| F-07 | Untrusted text isolated as data | Yes | Yes | Code and retrieval keep the strings as data. Language model may quote them as a flag | BP7 | Control on S7 to S11. Minutes 36 to 39 |
| F-08 | Identity, owner assignment, recovery status | Yes | Yes | Code for identity and status. Person at RT-06 assigns an owner | BP8 | S11 |
| F-09 | Queue ranking from stored fields | Yes | Yes | Code | BP4, BP5 | Queue under S7 to S11 |
| F-10 | Cited conflict explanation | Yes | Yes | Language model. Must cite the two rows or files | BP1 to BP7 | S7 to S11 |
| F-11 | Cited natural-language answer | Yes | Yes | Language model. Code fetches the row. Abstain if none | BP1 to BP8 | S7 to S13 |
| F-12 | Draft investigation plan, then wait | Yes | Yes | Language model drafts. Person at RT-02 accepts or rejects | BP1, BP2, BP6, BP8 | Agent trace, minutes 13 to 25 |
| F-13 | Person on every record-changing action | Yes | Yes | Person. BO-03 working answer | BP1, BP2, BP6, BP8 | Approval gate |
| F-14 | Same-scenario run on both applications | Yes | Yes | Code comparison. Each difference traces to a lake item | BP4, BP5 | S13 |
| F-15 | Rule lineage in the context view | Evaluation only | Context view required | The view reads lake items. It does not change a record | BP4 | S12 |

Worked example for F-01. 91 of 125 process steps have a `recipe_version` that differs from the tool `recipe_rev`. Honesty: REAL. Code lists those two values. A model may say they differ, citing the two columns. A Process Engineer at RT-03 approves a hold or a release.

Worked example for F-04. Packaged REVIEW count is 2,090. Honesty: REAL. Four programs already apply different tests. Both applications read one governed archive for pass or fail. Application B can do that only when the archive item is in the Context Lake.

Worked example for F-09. `priority('OPEN', 'CRITICAL', 1)` returns `urgent`. Two packaged cases are urgent because severity is CRITICAL. Zero packaged cases have `amount > 50000`. Honesty: REAL. Ranking does not read the case note.

---

## Shared versus extra

| Layer | Shared by both applications | Extra on Application B |
|---|---|---|
| Workflow | W1 to W5, W7. Scenarios 7 to 11 | W6 context view. Scenario 12 |
| Rules | Same pass-or-fail result on the same input | The result must come from a lake item |
| Language model | Conflict explanation, natural-language answer, draft plan | Same three jobs. Retrieval reads only the Context Lake |
| Person | RT-01 to RT-06 | Same roles |
| Out of this map | `engineering_hold` prediction | Same rejection (FD-05) |

**Verified Fact.** FD-05. Majority and leave-one-out logistic regression are both 117/125. No hold scorer sits on this map.

---

## Capability to workflow

| Workflow | Capabilities used |
|---|---|
| W1 Intake and de-duplication | F-02, F-07, F-13 |
| W2 Queue ranking | F-09, F-05 |
| W3 Exception investigation | F-01, F-03, F-06, F-07, F-10, F-11, F-12 |
| W4 Approval and disposition | F-13, F-01, F-02, F-06, F-08 |
| W5 Outage and recovery visibility | F-08, F-13 |
| W6 Rule lineage | F-04, F-15 |
| W7 Two-application comparison | F-14, F-04, F-05 |

---

## What this file does not do

This file does not add a capability outside BP1 to BP8. It does not specify servers, ports as product requirements, or file layout. It does not set a citation percent.
