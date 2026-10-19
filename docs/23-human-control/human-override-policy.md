# Human override policy

| Field | Value |
|---|---|
| Stage | Phase 10 / 23 Human control and audit chain. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | BO-03; BO-09; `docs/12-specs/business-rules.md`; `approval-gates.md` in this folder |
| Assumptions | BO-03 working answer holds. A person may choose among the decisions listed for their role. |
| Unresolved issues | Company titles stay Unknown. A later signed policy may add a decision. It has not. |
| Residual risks | A UI control that posts approve on a BLOCKED case would skip OPA-R-01. |

This file names what a person may record after the graph pauses, and what stays closed.

---

## Finding

**Finding.** A mapped person may record the decisions in the Group C table. That person may not approve their own proposal. That person may not turn a BLOCK into EXECUTE.
**Evidence.** API-Q-04 decision list. `approvals.py` already returns 409 on a blocked case. OPA-R-01.
**Impact.** Half B can hide the approve button on a blocked case.
**Risk.** An "override injection" control would treat harvested text as an order.
**Confidence.** High
**Open questions.** None for the closed BLOCK path.

---

## Allowed decisions after HOLD_FOR_REVIEW

| Waiting role | `action_type` | Allowed `decision` values | Effect on the overlay |
|---|---|---|---|
| RT-01 | `dispose` | `approve`, `block` | Clears `waiting_role` on approve. Leaves the case blocked on block |
| RT-02 | `approve_agent` | `approve`, `hold`, `block` | Applies the mapped write only on approve. Hold keeps a person-recorded hold. Block stops |
| RT-03 | `recipe_hold_or_release` | `hold`, `approve` as release | `engineering_hold` 1 or 0 |
| RT-04 | `policy_pick` | `approve` with `policy_id`, or `keep_wait` | Sets `chosen_policy_id` or keeps the wait |
| RT-05 | `replay_confirm` | `drop_duplicate`, `keep_duplicate` | Status `DUPLICATE` or stay REPLAY |
| RT-06 | `assign_owner` | `assign` with person-supplied `owner_id` | Sets `owner_id` |

`keep_wait` is the allowed "do not pick" for RT-04. The case stays open.

---

## Closed actions

| Action | What the application does |
|---|---|
| Approve a case with `blocked=true` | HTTP 409. `error_class: blocked`. Already in `approvals.py` |
| Approve with `actor_id == proposed_by` when `proposed_by` is a person | HTTP 403. OPA-R-07 |
| Resume with the wrong RT role | HTTP 403 |
| Supply `owner_id` from the model | OPA-R-09 BLOCK. Route requires a person-typed value |
| Change operational closed into finance closed in this phase | Wait. BO-06b PROPOSED |
| Insert a live amount cutoff while disposing a silent case | Wait. OPA-R-03 |

---

## Draft text

The person reads `draft_plan`. The person may ignore the draft and record a different allowed decision for that role. The audit row stores the person's `decision`, not a rewritten model paragraph.

The person may not edit lake items from this path. Lake changes still go through `build.py`.

---

## What this file does not do

This file does not add an admin override role. It does not write the UI.
