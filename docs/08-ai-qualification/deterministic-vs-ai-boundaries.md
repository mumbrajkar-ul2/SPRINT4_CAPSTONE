# Deterministic versus AI boundaries

| Field | Value |
|---|---|
| Stage | Phase 2 / 8 AI-versus-no-AI qualification |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p2-fix-20261018-001 |
| Status | COMPLETE. This fix pass records FD-04 and FD-05 as DECIDED in Decision_Tracker.md v1.13. |
| Evidence sources | `ai-vs-no-ai-matrix.md`; `Project_Intent.md` sections 10.1, 10.2, and 10.3; `Decision_Tracker.md` FD-02, FD-08, BO-03 section 5.1, section 7; `app/legacy_logic.py`; `app/partner_feeds.py` |
| Assumptions | BO-03 working answer holds for agency. FD-02 holds for tools. The DECIDED FD-04 labels in the matrix are the boundary used here. |
| Unresolved issues | Company job titles that match RT-01 to RT-06 are unmapped. FD-15 and FD-16 are later. |
| Residual risks | A later agent that writes a case field would cross this boundary while BO-03 is still PROPOSED. |

This file says which work stays in code, which work a model may draft, and which work a person must finish.

## Work that stays in code

**Verified Fact.** `Project_Intent.md` section 10.2 and the DECIDED FD-04 labels.

| Work | Why it stays in code | Linked evidence |
|---|---|---|
| Queue ranking (triage) | `priority()` already returns archive, urgent, review, or queue. | `app/legacy_logic.py` |
| Hold, release, and status writes | A write changes the record. A person must approve it. | BO-03 working answer. FD-02 |
| Rule pass or fail | Four local programs already disagree. The archive is canonical. | BP4. FD-08 |
| Accept, reject, duplicate on a feed | `reconcile()` tests key, schema, REPLAY, and quantity. | `app/partner_feeds.py` |
| Intake de-duplication | A repeated `message_id` or a REPLAY status is the test. | BP2. Baseline behaviour note |
| Numeric KPI math | Hours, counts, and amounts are field arithmetic. | Intent 10.2. FD-03 |
| Spec-limit compare | `metrology` already stores `measured`, `spec_low`, and `spec_high`. | Domain schema |
| Authorization | The current GET API has no identity check. A later gate is code. | BP8. FD-02 |

Worked example. A feed with `processing_status = 'REPLAY'` is marked DUPLICATE when `reconcile()` runs. The test is the status word. A model does not vote on that mark.

## Work a model may draft

**Verified Fact.** Intent section 10.1. DECIDED GenAI labels in the matrix.

| Work | What the model returns | What it must cite |
|---|---|---|
| Conflict explanation | A sentence that names both values and the disagreement type | The two rows or files it used |
| Natural-language answer | A cited answer to one of the seven demo jobs, or a later golden question | A lake item or a stored row. If none, it abstains |
| Draft plan | An investigation plan, a test list, a handoff note, or a proposed mapping | The records it retrieved |
| Case or lot timeline summary | An ordered list of events with conflict flags | Event time and arrival time kept as two fields (BP3) |

**Verified Fact.** FD-02. The model gets read-only tools only. This unit adds no write tool.

**Verified Fact.** BO-03 working answer. The draft is a proposal. It does not become a write until a person approves it.

## Work a person must finish

**Verified Fact.** `Decision_Tracker.md` section 7 and BO-09.

| ID | Work | Role |
|---|---|---|
| RT-01 | Dispose a case that routed to HOLD_FOR_REVIEW | Fab Exception Reviewer |
| RT-02 | Approve, hold, or block a proposed action | Shift Lead or Process Engineer (Approver) |
| RT-03 | Approve a recipe-mismatch case | Process Engineer |
| RT-04 | Accept an abstain or pick a policy on overlap | Policy Owner |
| RT-05 | Confirm a replay duplicate before it is dropped | Operations Analyst |
| RT-06 | Assign a follow-up owner when none exists | Operations Lead |

Company job titles that match these role names are Unknown.

**Verified Fact.** BO-09. The person who proposes an action is a different person from the person who approves it.

## Boundary in one case

Lot L has a process step whose `recipe_version` is R02 and a tool whose `recipe_rev` is R01. SQL raises the mismatch. That is code. A model may write: step recipe R02 and tool recipe R01 differ, with those two columns cited. A Process Engineer at RT-03 approves any hold or release. The model does not write `engineering_hold`.

**Verified Fact** for the 91 packaged mismatches. **Inference** that a later lot will follow the same split of flag, sentence, and approval.

## What the model must do with untrusted text

**Verified Fact.** Catalogue BP7. 86 partner feeds contain `auto approve` or `disregard validation`. 150 bundled lake rows carry an approve-or-ignore instruction. 22 source-document lines and 3 emails also match those words.

Those strings stay data. The model may quote them as a conflict flag. The model may not treat them as an order to write.

## BO-03 status on this boundary

The agency bound above uses the working answer. The tracker row is PROPOSED. The Business Owner accepted it on 2026-10-18. The owner has not signed it DECIDED.

SME recommendation from `Decision_Tracker.md` section 5.1:

| ID | SME recommendation | Why |
|---|---|---|
| BO-03 | AI explains and proposes. A person approves every action that changes a record. No autonomous writes. | A wrong auto-action in a fab can scrap material. Human approval caps that risk at review, not loss. |

## What this file does not do

This file does not write an OPA rule. FD-16 is later. It does not name a company job title.
