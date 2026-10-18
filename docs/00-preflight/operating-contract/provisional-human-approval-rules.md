# Provisional human-approval rules

| Field | Value |
|---|---|
| Stage | Phase 0 / 0B Provisional operating contract |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL |
| Evidence sources | `Decision_Tracker.md` sections 1, 5, 5.1, 5.2, and 7; BO-03, BO-08, BO-09; `Project_Intent.md` sections 10.2 and 10.3; `Execution_Plan.md` section 11 |
| Assumptions | BO-03 is accepted and still PROPOSED. The working answer is used here and is not written into code. |
| Unresolved issues | Company job titles that match the SME role map are unconfirmed. The named Business Owner signer is Unknown. |
| Residual risks | A later builder could treat a PROPOSED approval rule as executable policy. Affected cases must still route to HOLD_FOR_REVIEW until the owner signs. |

These rules are PROVISIONAL.

## Delivery-time approvals

**Verified Fact.** `Decision_Tracker.md` and `Execution_Plan.md` section 11.

| Decision kind | Who approves | What happens if it is open |
|---|---|---|
| Engineering and method (Group A) | Team-Force. A separate reviewer accepts the files on disk | The phase waits, or it uses the stated default and marks DEFERRED |
| Industry fact (SME rows) | FDE SME (Semiconductor) | The phase that needs the fact does not invent it |
| Company liability (Group B) | Business Owner. The SME recommendation must be shown first | An accepted PROPOSED row does not pause the run. The artifact stays unsigned. A policy number is not written into code |
| Reviewer verdict | Fresh reviewer on Composer 2.5 | The next unit does not start |
| Live test that needs a key or a running service | Human. From Phase 8 on this is `NEEDS_HUMAN` | The agent pauses |

**Verified Fact.** The reviewer never signs a Business Owner row. The executor never sets a Business Owner or SME policy value.

## Run-time approvals (later, when the apps exist)

**Verified Fact.** `Decision_Tracker.md` section 7 and BO-09. The SME set these standard roles. The company has not confirmed its own job titles.

| ID | Decision | Role | Gap |
|---|---|---|---|
| RT-01 | Dispose a case that routed to HOLD_FOR_REVIEW | Fab Exception Reviewer | Company title Unknown |
| RT-02 | Approve, hold, or block an agent-proposed action | Shift Lead or Process Engineer (Approver) | Company title Unknown |
| RT-03 | Approve a recipe-mismatch case | Process Engineer | Company title Unknown |
| RT-04 | Accept an abstain or pick a policy on overlap | Policy Owner | Company title Unknown |
| RT-05 | Confirm a replay duplicate before it is dropped | Operations Analyst | Company title Unknown |
| RT-06 | Assign the follow-up owner for an incident with no owner | Operations Lead | Company title Unknown. Current INC-2025-014 owner is also Unknown |

**Verified Fact.** BO-09. The proposer of an action is never its approver.

## Working AI approval rule

**Verified Fact.** BO-03 working answer, accepted 2026-10-18, still PROPOSED. AI explains and proposes. A person approves every record-changing action. No autonomous writes.

**Verified Fact.** BO-08 working answer. Where the governed source is silent, the case routes to review. No new threshold is invented.

**Verified Fact.** `Project_Intent.md` section 10.2. Authorization, state transitions, numeric KPIs, and final reconciliation stay deterministic.

## What this page does not invent

It does not name a person. It does not pick a company job title. It does not set a numeric approval limit.
