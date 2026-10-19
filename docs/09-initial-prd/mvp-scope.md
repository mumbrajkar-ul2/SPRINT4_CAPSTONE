# MVP scope

| Field | Value |
|---|---|
| Stage | Phase 3 / 9 Initial PRD and product intent |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p3-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED with the initial PRD. |
| Evidence sources | `Execution_Plan.md` sections 3, 8, 10; `Project_Intent.md` sections 8, 15.2, 17.4; `docs/05-current-state/conflict-catalogue.md`; `docs/08-ai-qualification/qualification-decision.md`; BO-02, BO-03, BO-04, FD-04, FD-05 |
| Assumptions | MVP here means the first product both applications must demonstrate. Later phases still implement this MVP. They do not add a ninth business problem. |
| Unresolved issues | BO-04 stays PROPOSED. Exception cycle time and aged backlog stay Unknown. Identity design stays later. |
| Residual risks | Treating Phase 4 architecture work as extra product scope would hide that it still serves BP1 to BP8. Treating workshop 500k data as MVP would grow the demo past the packaged set. |

MVP is the smallest product that names both applications, the AI limits, the eight business problems, and the 40-minute demo flow. BO-04 says to approve once those four things are named, and nothing beyond.

---

## In the MVP

**Verified Fact.** Execution_Plan sections 3, 8, and 10. FD-04. BO-03 working answer.

| Item | What the user can finish | Bound |
|---|---|---|
| Application A | Fab-exception workflow on scenarios 7 to 11, with an approval gate | Rules from the rebuilt program |
| Application B | The same workflow on scenarios 7 to 11, plus scenario 12 lineage | Rules only from the Context Lake |
| Shared comparison | Scenario 13 | Same inputs. Each difference traces to a lake item |
| BP1 | See both recipe revisions. Wait for RT-03 | Code flag. Language-model sentence. Person writes |
| BP2 | See 67 REPLAY rows as duplicates. Wait for RT-05 | Code mark. Person confirms |
| BP3 | See event time and arrival time as two fields | Code split. Language-model sentence |
| BP4 | One governed pass-or-fail test. Lineage on Application B | Code. No fifth wording |
| BP5 | Count REVIEW and HOLD as open | BO-06a meaning |
| BP6 | Name a policy overlap. Wait for RT-04 | Code detect. Person picks |
| BP7 | Show approve-or-ignore text as data. Block an injection in minutes 36 to 39 | Text stays data |
| BP8 | Identity on a case. User-visible retry status. RT-06 can assign an owner | Design of identity is later. The need is in MVP |
| Ranking | Next case from status, severity, and amount | Code. FD-04 |
| Language-model jobs | Conflict explanation. Natural-language answer. Draft plan | Propose and wait |
| Person on writes | RT-01 to RT-06 | BO-03 working answer |
| 40-minute path | Section 10 time boxes | Working demo flow |
| Packaged data | The 125-case, 125-lot packaged set | Honesty: REAL for those counts |

Worked example. MVP includes showing 91 of 125 recipe mismatches. Honesty: REAL. MVP does not include a target such as "cut mismatches by 30 percent." That percent does not exist in a governed source.

---

## Later work that still serves this MVP

These are how later phases build the MVP. They are not extra product features.

| Later work | Why it still sits inside BP1 to BP8 |
|---|---|
| Phase 4 architecture decisions | They say how the two applications and the lake are arranged. They do not add a ninth problem |
| Phase 5 Context Lake items | Application B reads a rule only when the Context Lake holds that rule (BP4) |
| Phase 6 contracts | They freeze the same workflows |
| Phases 7 to 11 build and parity | They implement Application A, Application B, and scenario 13 |
| Phase 12 identity and threat model | They implement BP8 and BP7 controls |
| Phase 13 recovery and operability | They implement scenario 11 |
| Phase 14 scorecard | They measure the eight KPI families. They do not invent a dollar benefit |
| Phase 15 rehearsal | They freeze the 40-minute path (FD-21) |

Ports 8080, 8090, 8091, and 8092 are later-phase facts for that build. They are not extra MVP features.

---

## Not in the MVP

| Item | Why it stays out | Label |
|---|---|---|
| A ninth business problem | BO-04 working answer. Scope is BP1 to BP8 | Verified Fact |
| Production `engineering_hold` predictor | FD-05. 117/125 versus 117/125 | Verified Fact |
| Language-model ranking, pass-or-fail, reconcile, or duplicate mark | FD-04 | Verified Fact |
| Model write of a case, hold, or feed status | BO-03 working answer | Verified Fact |
| Invented cycle-time target or aged-backlog cutoff | BO-02. Both values Unknown | Unknown |
| Monetary benefit claim | BO-11 | Verified Fact of the working answer |
| Workshop 500k and stress 2M lake tiers | Not packaged | Verified Fact of PRELOADED_DATA.md via Phase 0 exclusions |
| Official Birlasoft brand files | Not in hand. BO-12 | Verified Fact |
| Named company job titles | Unmapped. BO-09 leftover | Unknown |
| Signed BO-04 | Explicitly deferred. This PRD stays UNSIGNED | Verified Fact |
| Live token prices and citation percent floors | Unknown. FD-14 PENDING | Unknown |

---

## MVP acceptance in one list

The MVP is accepted for demo use when all of these are true. Numeric KPI targets are not in this list.

1. Application A runs scenarios 7 to 11 with an approval gate.
2. Application B runs the same scenarios from the Context Lake and shows scenario 12.
3. Scenario 13 names matches and traces each difference to a lake item.
4. Each of BP1 to BP8 has a visible handling on that path.
5. A person approves every record-changing action.
6. The 40-minute path in Execution_Plan section 10 can be rehearsed.
7. Every demo number carries an honesty label.
8. BO-04 remains recorded as PROPOSED until the owner signs.

---

## What this file does not do

This file does not add scope beyond the eight business problems. It does not specify implementation code. It does not sign BO-04.
