# Minimum agency assessment

| Field | Value |
|---|---|
| Stage | Phase 2 / 8 AI-versus-no-AI qualification |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p2-doc-20261018-001 |
| Status | COMPLETE. BO-03 recorded as PROPOSED. |
| Evidence sources | `Decision_Tracker.md` BO-03, section 5.1, section 5.2, section 7, BO-09, FD-02; `Project_Intent.md` sections 10.2 and 10.3; `docs/00-preflight/operating-contract/provisional-human-approval-rules.md`; `ai-vs-no-ai-matrix.md` |
| Assumptions | The BO-03 working answer holds for this unit. A policy value behind a PROPOSED row is not written into code. |
| Unresolved issues | BO-03 is accepted and unsigned. Company job titles that match RT-01 to RT-06 are Unknown. The named signer is Unknown. |
| Residual risks | A later agent that writes `cases.status` or `wafer_lots.engineering_hold` would apply a PROPOSED bound as if it were signed code. |

A person approves every record-changing action. That sentence is the working agency bound for this phase.

## BO-03 status

| Field | Value | Label |
|---|---|---|
| Tracker status | PROPOSED | Verified Fact |
| Business Owner review | Accepted on 2026-10-18, section 5.2 | Verified Fact |
| Signed DECIDED | No | Verified Fact |
| Working answer | AI explains and proposes. A person approves every record-changing action. No autonomous writes. | Verified Fact of the working answer |

SME recommendation from `Decision_Tracker.md` section 5.1. This block must be shown with the owner row.

| ID | SME recommendation | Why |
|---|---|---|
| BO-03 | AI explains and proposes. A person approves every action that changes a record. No autonomous writes. | A wrong auto-action in a fab can scrap material. Human approval caps that risk at review, not loss. |

This note copies that recommendation. It does not sign the row.

## Where agency is needed

Agency here means: the program may start a next step that a person still has to accept.

| Capability | Recommended intelligence | Agency this unit allows | Who accepts a write | Label |
|---|---|---|---|---|
| Triage | deterministic | None. Ranking returns a queue word. It does not write a case. | No write in ranking. A later disposition uses RT-01 or RT-02. | Verified Fact for `priority()`. |
| Conflict explanation | GenAI | Draft text only. | Any hold or release after the explanation uses RT-02 or RT-03. | Verified Fact of the working answer. |
| Natural-language query | GenAI | Draft text only. | A follow-up write uses RT-01 to RT-06. | Verified Fact of the working answer. |
| Agentic planning | GenAI | Draft a plan and wait. | RT-02 for a proposed action. BO-09: the person who proposes an action is a different person from the person who approves it. | Verified Fact |
| Rule evaluation | deterministic | None. The archive test returns pass, fail, or route-to-review. | A silent threshold routes to RT-04 (BO-08 working answer). | Verified Fact |
| Reconciliation | deterministic | None. Status becomes ACCEPTED, REJECTED, or DUPLICATE in code. | Dropping a duplicate still waits for RT-05. | Verified Fact of RT-05. Inference that the later app keeps that confirm step. |
| Intake de-duplication | deterministic | None. The mark is an identifier test. | RT-05 confirms the drop. | Verified Fact |
| `engineering_hold` prediction | ML-rejected | None. No model is shipped. | A person already owns hold and release. | Verified Fact |

Worked example. Scenario 8: the step recipe is R02 and the tool recipe is R01. Code raises the mismatch. A model may name both revisions. A Process Engineer at RT-03 approves the hold or the release. The model does not update `engineering_hold`.

## Where agency is not needed

These steps finish without a model choosing a next action:

- Compute `priority()` from status, severity, and amount.
- Count open cases with `status != 'CLOSED'`.
- Compare `recipe_version` to `recipe_rev`.
- Compare `event_time` to `arrival_time`.
- Mark REPLAY as a duplicate candidate.
- Read a threshold from the governed archive.

Those steps return a value or a flag. They do not write a disposition.

## Run-time roles that hold the write

**Verified Fact.** `Decision_Tracker.md` section 7.

| ID | Decision | Role |
|---|---|---|
| RT-01 | Dispose a HOLD_FOR_REVIEW case | Fab Exception Reviewer |
| RT-02 | Approve, hold, or block a proposed action | Shift Lead or Process Engineer (Approver) |
| RT-03 | Approve a recipe-mismatch case | Process Engineer |
| RT-04 | Accept an abstain or pick a policy | Policy Owner |
| RT-05 | Confirm a replay duplicate before it is dropped | Operations Analyst |
| RT-06 | Assign a follow-up owner | Operations Lead |

**Verified Fact.** FD-02. The model gets read-only tools only.

**Verified Fact.** BO-09. The person who proposes an action is a different person from the person who approves it.

Company job titles remain Unknown. INC-2025-014 follow-up owner remains Unknown.

## What happens while BO-03 is PROPOSED

The run does not pause at this row. The working answer is used in these notes. A policy value is still not written into application code. A later write path still routes the case to HOLD_FOR_REVIEW until the owner signs.

## What this file does not do

This file does not name a person. It does not set FD-16. It does not edit the tracker.
