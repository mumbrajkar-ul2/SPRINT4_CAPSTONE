# Escalation matrix

| Field | Value |
|---|---|
| Stage | Phase 10 / 23 Human control and audit chain. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `Decision_Tracker.md` Group C; `docs/12-specs/business-rules.md`; `failure-semantics.md` |
| Assumptions | Escalation stays inside RT-01 to RT-06. No seventh role is added. Company titles stay Unknown. |
| Unresolved issues | Who is on shift during the demo stays Unknown. Named people stay Unknown. |
| Residual risks | Auto-assigning RT-06 a made-up owner would skip the person. |

This file names who receives a case when the first wait cannot finish. Escalation here means: the same case stays open and a named role is shown as `waiting_role`.

---

## Finding

**Finding.** Scenario waits stay on the SME role already bound. Budget and recursion waits that have no scenario role go to RT-01. Injection does not escalate. It stops.
**Evidence.** Group C. TERM-01 and TERM-06. INC-2025-014 is RT-06 only.
**Impact.** Half B can set `waiting_role` from this table.
**Risk.** A generic admin role would skip the map.
**Confidence.** High on the six roles. Unknown on who staffs them.
**Open questions.** Company titles. On-shift names.

---

## Matrix

| Trigger | First `waiting_role` | If that person cannot act | What stays closed |
|---|---|---|---|
| SP-07 replay candidate | RT-05 | Case stays on RT-05. A 403 does not move the role | Auto-drop |
| SP-08 recipe mismatch | RT-03 | Stays on RT-03 | Model write of hold |
| SP-09 two clocks, cut-off asked | empty, then HOLD via OPA-R-02 | RT-01 may dispose the review | Inventing a cut-off |
| SP-10 policy overlap | RT-04 | Stays on RT-04. `keep_wait` is the stay action | Model pick |
| SP-11 missing owner | RT-06 | Stays on RT-06 | Invented `owner_id` |
| Agent draft that would write, no more specific role | RT-02 | Stays on RT-02 | Same person as `proposed_by` |
| Archive silence | RT-01 | Stays on RT-01 | Substitute limit |
| Silent threshold | RT-01 | Stays on RT-01 | Amount comparison |
| Finance and audit mismatch | RT-01 | Stays on RT-01 | Merge of the three closures |
| Budget or recursion exhausted, scenario role already set | That scenario role | Stays | Auto-apply draft |
| Budget or recursion exhausted, no scenario role | RT-01 | Stays on RT-01 | Auto-apply draft |
| Wrong role posted | Unchanged | Caller receives 403 | Role rewrite |
| Injection BLOCK | None | None. Stop | Any approval |

Worked example. Scenario 8 hits the step budget before OPA. `waiting_role` stays RT-03. RT-01 does not take the recipe hold.

Worked example. A free-form query proposes a write and hits the recursion limit. `waiting_role` becomes RT-01. RT-01 may dispose. RT-01 still cannot be the same person as a human `proposed_by`.

---

## What is not an escalation

A 503 from the source gateway stays on the recovery screen. Owner assign is still RT-06. The probe does not invent an on-call name.

A replay miss abstains. It does not page a person.

---

## What this file does not do

This file does not name a person. It does not add RT-07.
