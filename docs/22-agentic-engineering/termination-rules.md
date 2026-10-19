# Termination rules

| Field | Value |
|---|---|
| Stage | Phase 10 / 22 Agentic engineering. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `graph-definition.md`; `docs/12-specs/error-handling-spec.md`; FD-14; BO-03; injection corpus |
| Assumptions | Every terminal path writes the audit rows already produced. `write_audit` always runs before `END`. |
| Unresolved issues | Measured path frequencies stay Half B. |
| Residual risks | Ending on EXECUTE and then writing a record in the same node would skip the person. |

This file names every way a thread reaches `END`. Half B must implement each row.

---

## Finding

**Finding.** A thread ends in one of seven terminals. Four terminals change no record. One terminal writes only after a person. Two terminals stop a forbidden write.
**Evidence.** OPA three verdicts. FD-14 abstain. BO-03 person write. Corpus BLOCK.
**Impact.** Tests can assert the terminal name and the stored case.
**Risk.** A hidden eighth terminal that auto-applies a draft would skip the gate.
**Confidence.** High
**Open questions.** None for the terminal list.

---

## Terminals

| Id | When | Record change | OPA | Person | Audit must include |
|---|---|---|---|---|---|
| TERM-01 | `opa_verdict=BLOCK` | None | BLOCK | None offered | EV-07, EV-12, every prior agent_step |
| TERM-02 | `verdict=ABSTAIN` and `record_change` is false | None | EXECUTE or unused | None | EV-08 rows. Sentence empty |
| TERM-03 | `opa_verdict=EXECUTE` and `record_change` is false | None | EXECUTE | None | EV-07 plus agent steps. Explanation only |
| TERM-04 | Person records approve, hold, drop, keep, pick, or assign | Yes, the mapped mutation | HOLD_FOR_REVIEW before the wait | Required | EV-09 or EV-10 plus every prior step |
| TERM-05 | Person records `block` or `keep_duplicate` or `keep_wait` | None or keep-wait only | HOLD_FOR_REVIEW before the wait | Required | EV-09. Case still open when keep-wait |
| TERM-06 | `GraphRecursionError` or `budget_exhausted` | None | HOLD_FOR_REVIEW via OPA-R-10 or the catch path | RT-01 may later dispose | EV-07 or a control row with `error_class=wait_for_person` |
| TERM-07 | Case id missing or identity rejected before invoke | None | Not run | None | Control row if a correlation id exists |

Worked example. IC-01 proposes approve from a partner note. TERM-01. The feed status stays REPLAY. No approval resource is offered.

Worked example. Scenario 9 explains two clocks. `record_change` is false. TERM-03. The evidence row is unchanged.

Worked example. Scenario 8 waits. RT-03 records hold. TERM-04. `engineering_hold` becomes 1 on the overlay.

---

## Terminals that must not exist

| Forbidden end | Why |
|---|---|
| Auto-apply draft on EXECUTE | BO-03 working answer. EXECUTE on a record change still waits |
| End with no audit row for the last step | FD-23 |
| End by calling Azure on a replay miss | `MODEL_MODE=replay` |
| End by inventing `owner_id` | `decision.inc_2025_014` |
| End by inserting a substitute archive limit | BR-05 |

---

## After `END`

The checkpoint keeps the last state. A later `GET /api/cases/{id}` shows `draft_plan`, `waiting_role`, `blocked`, and recorded approvals. A later `GET /api/audit/{correlation_id}` returns the full list in `seq` order.

---

## What this file does not do

This file does not add an eighth terminal. It does not write the `END` handler.
