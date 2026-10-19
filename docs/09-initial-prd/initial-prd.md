# Initial PRD

| Field | Value |
|---|---|
| Stage | Phase 3 / 9 Initial PRD and product intent |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p3-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED. BO-04 recorded as PROPOSED. |
| Evidence sources | `docs/05-current-state/conflict-catalogue.md`; `docs/08-ai-qualification/` (seven files); `Project_Intent.md` sections 3, 8, 10, 14, 15; `Execution_Plan.md` sections 3, 4, 8, 10; `Decision_Tracker.md` BO-02, BO-03, BO-04, section 5.1, FD-04, FD-05, section 7 |
| Assumptions | BO-02, BO-03, and BO-04 working answers hold. Company job titles stay unmapped. Ports 8080, 8090, 8091, and 8092 stay later-phase facts. |
| Unresolved issues | BO-04 signer name is Unknown. Exception cycle time is Unknown. Aged backlog cutoff is Unknown. INC-2025-014 follow-up owner is Unknown until a person assigns one at RT-06. |
| Residual risks | A later author who adds a ninth business problem would grow the product past this PRD. A later author who treats this unsigned file as a signed gate would hide the deferred signature. |

This file is the initial product requirements document. It names both applications, the AI limits, the eight business problems, and the 40-minute demo flow. It does not specify implementation code. It does not sign BO-04.

---

## BO-04 recorded as PROPOSED / unsigned

**Verified Fact.** `Decision_Tracker.md` BO-04. The Business Owner accepted the working answer on 2026-10-18. The owner has not signed this artifact DECIDED. This file stays UNSIGNED. The run does not pause at this row.

Working answer in force: approve the initial PRD once it names both applications, the AI limits, the eight business problems, and the demo flow, and nothing beyond.

SME recommendation from `Decision_Tracker.md` section 5.1. Shown here because the owner must see it beside the row.

| ID | SME recommendation | Why |
|---|---|---|
| BO-04 | Approve the initial PRD once it names both apps, the AI limits, the eight business problems, and the demo flow, and nothing beyond them. | Scope held to the evidenced defects keeps the build demoable on the laptop and honest. |

This file copies that recommendation. It does not invent a signer name.

---

## Product intent

Fabpulse Group handles fab-lot and equipment exceptions. External messages, process records, policy versions, case workflows, archived documents, and local rule programs do not always agree.

**Verified Fact.** `Project_Intent.md` section 6. Operators then spend extra time reconciling. Queues grow. Two teams can report a different open count for the same week. A disputed outage can sit with no owner.

This product is two applications that run the same fab-exception workflow. Application A is rebuilt from the current program. Application B is built from the Context Lake. The Context Lake is the stored, versioned set of rules, evidence, and decisions. Both applications are measured on the same scenarios and the same KPI families.

**Verified Fact.** BO-02 working answer. The two headline business KPIs are exception cycle time and aged backlog. Both measured values are Unknown. No target percent is set. No dollar benefit is claimed. The other six KPI families are supporting measures.

---

## The two applications

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 8.

| Name | How it is built | Where it reads its rules | What the user sees |
|---|---|---|---|
| Application A | Rebuild of the current fab-exception program, with language-model help only where Phase 2 allowed it | From its own rebuilt program | The exception queue, case evidence, approval gate, and recovery status |
| Application B | Built from the Context Lake | Only from the Context Lake | The same workflow as Application A, plus a context view that shows the lake item behind a rule |

Worked example. Application A can read a pass-or-fail test that still lives in the rebuilt program. Application B can read that same test only if the Context Lake holds it. If the lake leaves out the JavaScript 1.05 tolerance, Application B can mark a case differently from Application A. The team then traces that difference to the missing lake item.

**Verified Fact.** Both applications run without calling the other at run time. Both run demo scenarios 7 to 11 with the same inputs. Both are scored on the same KPI families.

Ports 8080 (legacy), 8090 (source gateway), 8091 (lake REST), and 8092 (lake MCP) are later-phase facts. This PRD does not specify servers, languages, or file layout.

---

## Users and the outcome each needs

These are roles. Company job titles that match them are Unknown. No personal name is assigned.

**Verified Fact.** `Decision_Tracker.md` section 7. `docs/03-problem-value/personas.md`.

| Role | Run-time id | Outcome the role needs | Linked problems |
|---|---|---|---|
| Fab Exception Reviewer | RT-01 | A case that waited for review has a recorded disposition and a recorded actor | BP4, BP5, BP7 |
| Shift Lead or Process Engineer (Approver) | RT-02 | A proposed write is approved, held, or blocked by a person who did not propose it | BP1, BP2, BP6, BP8 |
| Process Engineer | RT-03 | Both recipe revisions are visible. The engineer approves a hold or a release | BP1 |
| Policy Owner | RT-04 | An overlapping-policy case waits. The owner picks a policy or keeps the wait | BP6 |
| Operations Analyst | RT-05 | A replayed delivery is marked. The analyst confirms before it is dropped | BP2 |
| Operations Lead | RT-06 | A case or incident with no owner gets a named follow-up owner | BP8 |
| Integration lead | — | A late or retried feed stays visible. Event time and arrival time stay two fields | BP2, BP3, BP8 |
| Finance partner | — | Month-end counts use one open-and-closed meaning. No invented dollar benefit | BP4, BP5 |
| Risk and security partner | — | A reader of a case has an identity. An untrusted note does not close the case | BP7, BP8 |
| Enterprise application owner | — | Each application runs on its own. A recovery status is visible to the user | BP8 |

**Verified Fact.** BO-09. The person who proposes an action is a different person from the person who approves it.

---

## Workflows both applications run

**Verified Fact.** `docs/05-current-state/current-process-map.md`. The current human path is: message arrives, integration reconciles or imports, operations ranks the queue, a person records a decision, month-end measures are reviewed.

Both future applications run that path on the eight business problems. The steps below are the product workflows. They are not code.

| Workflow | What the user finishes | Acceptance for this PRD | Linked problems |
|---|---|---|---|
| W1 Intake and de-duplication | A new feed is accepted, rejected, or marked duplicate. A replay waits for RT-05 | The 67 packaged REPLAY rows are visible as duplicates. Honesty: REAL | BP2 |
| W2 Queue ranking | The next case to touch is chosen from stored fields | Ranking uses status, severity, and amount. It does not call a model | BP4, BP5 |
| W3 Exception investigation | The user sees both disagreeing values, with event time and arrival time kept apart | Scenarios 8, 9, and 10 show the two values and wait for a person | BP1, BP3, BP6, BP7 |
| W4 Approval and disposition | A person approves, holds, or blocks every record-changing action | The model drafts. The write waits for RT-01, RT-02, RT-03, or RT-04 | BP1, BP2, BP6, BP8 |
| W5 Outage and recovery visibility | The user sees retry status after an outage or a schema mismatch. An owner can be assigned | Scenario 11 shows a user-visible status. RT-06 can assign an owner | BP8 |
| W6 Rule lineage | The user sees one rule traced from document and code to a test | Scenario 12 runs on Application B's context view. Application A still evaluates the same rule from its rebuilt program | BP4 |
| W7 Two-application comparison | Scenarios 7 to 11 run on both applications. Each difference is named | Scenario 13. Each difference traces to a lake item | BP4, BP5 |

Worked example for W1. A partner row `REPLAY-000000000` has `processing_status = 'REPLAY'`. Code marks it as a duplicate candidate. An Operations Analyst at RT-05 confirms before it is dropped. A language model may explain why it is a duplicate. The model does not drop the row.

---

## The eight business problems in scope

**Verified Fact.** `Execution_Plan.md` section 3. `docs/05-current-state/conflict-catalogue.md`. Honesty for each count: REAL.

| ID | Business problem | Measured finding | Demo scenario |
|---|---|---|---|
| BP1 | Recipe revision differs between dispatch and equipment | 91 of 125 process steps have a `recipe_version` that differs from the joined tool `recipe_rev` | 8 Recipe mismatch |
| BP2 | Replayed deliveries inflate the exception queue | 67 partner feeds are stored as REPLAY | 7 Replay inflation |
| BP3 | Event time, arrival time, and effective date are confused | 11,985 of 12,500 evidence events have `arrival_time` different from `event_time`. 45 overlapping reference-version pairs | 9 Late metrology |
| BP4 | The same rule is built four ways, and they disagree | 2,090 REVIEW objects. Four programs apply different tests | 12 Rule trace. 13 Both apps |
| BP5 | Open and closed differ across sites and systems | 89 of 125 cases have `status != 'CLOSED'`. Five status word lists | 13 Both apps |
| BP6 | Three region vocabularies and overlapping policies | 34 active policy rows on eight country codes. Each country has 4 or 5 active rows | 10 Overlapping policies |
| BP7 | Untrusted text tries to drive decisions | 86 partner feeds, 150 bundled lake events, 3 emails, and 22 source documents carry approve-or-ignore text | Control on scenarios 7 to 11. Demo minutes 36 to 39 |
| BP8 | No API authorization; disputed ownership; manual reconciliation | `app/server.py` has no identity check. 695 workflow tasks have no assignee. INC-2025-014 follow-up owner is Unknown | 11 Outage or schema mismatch |

**Verified Fact.** `Execution_Plan.md` section 8. Demo scenarios 7 to 13 map to these eight problems. This PRD adds no ninth problem.

BP7 has no own row in the section 8 table. It is still in scope. Untrusted approve-or-ignore text is shown as data on every write-path scenario. Minutes 36 to 39 of the demo show an injection that is blocked.

---

## AI limits

These limits bind both applications.

**Verified Fact.** BO-03 working answer, accepted 2026-10-18, status PROPOSED. AI explains and proposes. A person approves every record-changing action. The model does not write a case, a hold, or a feed status on its own.

SME recommendation from `Decision_Tracker.md` section 5.1:

| ID | SME recommendation | Why |
|---|---|---|
| BO-03 | AI explains and proposes. A person approves every action that changes a record. No autonomous writes. | A wrong auto-action in a fab can scrap material. Human approval caps that risk at review, not loss. |

**Verified Fact.** FD-04 DECIDED 2026-10-18.

| Capability | How it is built | What the user sees |
|---|---|---|
| Triage (queue ranking) | Written test on stored fields | Next case ordered by status, severity, and amount |
| Rule evaluation | Written test against the governed archive | Pass, fail, or wait for a person |
| Reconciliation | Written tests on key, schema, REPLAY, and quantity | Accepted, rejected, or duplicate |
| Intake de-duplication | Written test on `message_id` or REPLAY status | Duplicate mark, then RT-05 confirm |
| Conflict explanation | Language model drafts a cited sentence | Both disagreeing values named, with citations |
| Natural-language query | Language model drafts a cited answer | One of the seven demo questions answered from a stored row or a lake item. If none, the model abstains |
| Agentic planning | Language model drafts a plan and waits | Investigation plan, feed disposition, or handoff for a person |
| `engineering_hold` prediction | Rejected | No production hold scorer |

**Verified Fact.** FD-05 DECIDED. Reject machine learning for `engineering_hold`. 125 lots. 8 held. 117 not held. Majority guess 117/125. Leave-one-out logistic regression 117/125. Honesty: REAL.

**Verified Fact.** FD-02. The model gets read-only tools only.

**Verified Fact.** Catalogue BP7. Strings such as `auto approve` and `disregard validation` stay data. The model may quote them as a conflict flag. The model may not treat them as an order to write.

Worked example. Lot L has a process step whose `recipe_version` is R02 and a tool whose `recipe_rev` is R01. Code raises the mismatch. A model may write: step recipe R02 and tool recipe R01 differ, with those two columns cited. A Process Engineer at RT-03 approves any hold or release. The model does not write `engineering_hold`.

---

## 40-minute demo flow

**Verified Fact.** `Execution_Plan.md` section 10. `Project_Intent.md` section 15.2. FD-21 (the later freeze of this flow) stays PENDING. This PRD uses the section 10 path as the working demo flow.

| Time | What the audience sees | Scenarios | Problems shown |
|---|---|---|---|
| 0 to 8 min | The eight business problems and the packaged baseline counts | — | BP1 to BP8 as the problem set |
| 8 to 13 min | The two applications and the code-versus-model split | — | FD-04 and BO-03 |
| 13 to 25 min | Application A live. Agent trace. Approval gate | 7, 8, 9, 10, 11 | BP2, BP1, BP3, BP6, BP8. BP7 as a control |
| 25 to 32 min | Application B on the same scenarios, plus a rule trace from the lake | 7 to 11, then 12 | Same problems, then BP4 lineage |
| 32 to 36 min | Before-and-after scorecard under the same inputs | 13 | BP4, BP5. Each difference traces to a lake item |
| 36 to 39 min | An injection that is blocked. A restart while an approval is waiting | — | BP7 untrusted text. BP8 recovery status |
| 39 to 40 min | Four or five lessons | — | — |

The seven demo jobs, from `Project_Intent.md` section 15.2:

| ID | What the system must do | Problem |
|---|---|---|
| S7 | Detect a replayed delivery and explain the duplicate evidence | BP2 |
| S8 | Show two recipe revisions and route for approval | BP1 |
| S9 | Keep event time and arrival time apart on a late result | BP3 |
| S10 | Name a policy overlap and wait for a person | BP6 |
| S11 | Show retry and status after an outage or schema mismatch | BP8 |
| S12 | Trace one rule from historical decision and code to a test | BP4 |
| S13 | Run S7 to S11 on both applications. Name each difference | BP4, BP5 |

**Assumption.** Demo replay (`MODEL_MODE=replay`) is the planned laptop mode in `Execution_Plan.md` section 10. Live token count in that mode is later work. Token cells stay Unknown.

Headline KPI values are not shown as a percent change. Exception cycle time is Unknown. Aged backlog is Unknown. Supporting families may be shown only with their honesty labels.

---

## Success measures for this product

**Verified Fact.** BO-02 working answer. FD-03.

| Family | Role | Measure | Baseline today | Target |
|---|---|---|---|---|
| Business outcome | Headline | Exception cycle time. Aged backlog | Unknown. Unknown | Not set |
| Decision quality | Supporting | Correct disposition versus expert labels | Unknown | Not set |
| Engineering productivity | Supporting | Discovery time. Tests accepted | Unknown | Not set |
| Performance | Supporting | API p95. Retrieval p95. Agent time | Unknown | Not set |
| Reliability | Supporting | Recovery. Duplicate rate. Replay correctness | Row counts exist. Rates Unknown | Not set |
| AI quality | Supporting | Groundedness. Citation. Abstention | Unknown. FD-14 PENDING | Not set |
| Cost | Supporting | Tokens. Cost per resolved scenario | Unknown | Not set |
| ROI | Supporting | Avoided effort minus cost | Unknown. BO-11 forbids a monetary benefit claim | Not set |

Honesty labels stay as written in `Execution_Plan.md` section 9. Business outcome numbers, when later modelled on this synthetic set, are SIMULATED. ROI numbers are EDUCATIONAL.

Related packaged counts that already exist, honesty REAL: 125 cases, 89 not CLOSED, 2 urgent cases, 67 REPLAY feeds, 91 recipe mismatches.

---

## What this file does not do

This file does not specify implementation code. It does not add a ninth business problem. It does not invent a cycle-time number, an aged-backlog cutoff, a target percent, or a dollar benefit. It does not sign BO-04. It does not name a signer.
