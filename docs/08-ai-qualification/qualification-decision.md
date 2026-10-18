# Qualification decision

| Field | Value |
|---|---|
| Stage | Phase 2 / 8 AI-versus-no-AI qualification |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p2-fix-20261018-001 |
| Status | COMPLETE. This fix pass records FD-04 and FD-05 as DECIDED in Decision_Tracker.md v1.13. BO-03 stays PROPOSED. |
| Evidence sources | `intervention-options.md`; `ai-vs-no-ai-matrix.md`; `deterministic-vs-ai-boundaries.md`; `minimum-intelligence-assessment.md`; `minimum-agency-assessment.md`; `economics-baseline-reconciliation.md`; `Decision_Tracker.md` FD-04, FD-05, BO-03, section 5.1, section 5.2 |
| Assumptions | FD-04 and FD-05 are DECIDED in the tracker. This unit does not edit the tracker. |
| Unresolved issues | BO-03 stays PROPOSED. Company job titles stay unmapped. Token counts stay Unknown. Live query wording beyond S7 to S13 is Unknown. |
| Residual risks | A later phase that writes a record from a model proposal would ignore the working agency bound. A later FinOps page that prices the four deterministic capabilities as model work would restore retired lines R-P2-03 to R-P2-06. |

This file is the per-capability decision for Phase 2. Tracker v1.13 records FD-04 and FD-05 as DECIDED. BO-03 stays PROPOSED and unsigned.

## Tracker rows in force

**Verified Fact.** `Decision_Tracker.md` v1.13.

| ID | Tracker status | Answer in force |
|---|---|---|
| FD-04 | DECIDED | Triage, rule evaluation, reconciliation, and intake de-duplication are deterministic. Conflict explanation, natural-language query, and agentic planning are GenAI. Predicting engineering_hold is ML-rejected. |
| FD-05 | DECIDED | Reject ML. Majority and leave-one-out logistic regression are both 117/125. |
| BO-03 | PROPOSED | AI explains and proposes. A person approves every record-changing action. No autonomous writes. |

## FD-04 answer

Authority: team-force.

| Capability | Recommended label | Reason | Claim label |
|---|---|---|---|
| Triage | deterministic | `priority()` ranks on status, severity, and amount. | Verified Fact |
| Conflict explanation | GenAI | Language job across 10 disagreement types and measured document variety (13 notes, 210 emails, 12,500 evidence payloads). | Verified Fact for counts |
| Natural-language query | GenAI | Seven distinct demo jobs. Code fetches. The model drafts a cited answer. | Verified Fact |
| Agentic planning | GenAI | Five named draft jobs. The model proposes and waits. | Verified Fact for the named jobs |
| Rule evaluation | deterministic | Four programs already disagree. FD-08 names the archive. | Verified Fact |
| Reconciliation | deterministic | `reconcile()` is written comparisons. Intent 10.2. | Verified Fact |
| Intake de-duplication | deterministic | REPLAY status and repeated `message_id`. | Verified Fact |

No capability is labelled Unknown. The evidence was enough for each of the seven.

Worked example. For ranking, `priority('OPEN', 'CRITICAL', 1)` returns `urgent`. That uses severity. It does not read the case note. That is why triage is deterministic.

## FD-05 answer

Authority: team-force.

**Reject ML.**

| Score | Value | Honesty | Label |
|---|---|---|---|
| Lots | 125 | REAL | Verified Fact |
| Held (`engineering_hold = 1`) | 8 | REAL | Verified Fact |
| Not held (`engineering_hold = 0`) | 117 | REAL | Verified Fact |
| Majority-class accuracy | 117/125 = 0.936 | REAL | Verified Fact |
| Leave-one-out logistic regression | 117/125 = 0.936 | REAL | Verified Fact |
| In-sample logistic regression | 117/125 = 0.936 | REAL | Verified Fact |
| Best leave-one-out stump | 117/125 = 0.936 | REAL | Verified Fact |
| Beats majority? | No | REAL | Verified Fact |

The model matched the majority guess. Both scored 117 of 125. No production model is built.

Related matrix row: `engineering_hold` prediction is ML-rejected.

## BO-03 recorded as PROPOSED

This row is not DECIDED. The Business Owner accepted the working answer on 2026-10-18. The owner has not signed the artifact.

Working answer in force: AI explains and proposes. A person approves every record-changing action. No autonomous writes.

SME recommendation from `Decision_Tracker.md` section 5.1. Shown here because the owner must see it beside the row.

| ID | SME recommendation | Why |
|---|---|---|
| BO-03 | AI explains and proposes. A person approves every action that changes a record. No autonomous writes. | A wrong auto-action in a fab can scrap material. Human approval caps that risk at review, not loss. |

Section 5.2 call: Accept.

Agency in the later apps follows that working answer. A policy number is still not written into code. Writes route to HOLD_FOR_REVIEW until the owner signs.

## Per-capability decision record

### Triage

**Finding.** Deterministic.
**Evidence.** `app/legacy_logic.py`. Two urgent cases from CRITICAL. Null test 117/125.
**Impact.** Queue order uses stored fields.
**Risk.** A hold score would change order with no gain.
**Confidence.** High.
**Open questions.** None.

### Conflict explanation

**Finding.** GenAI for the sentence. Code for the flag.
**Evidence.** Catalogue BP1 to BP7. Text-variety table.
**Impact.** S7 to S11 can show both values and a cited explanation.
**Risk.** 86 feeds and 150 lake rows carry approve-or-ignore text.
**Confidence.** High.
**Open questions.** FD-14 and FD-18 floors stay Unknown.

### Natural-language query

**Finding.** GenAI for the wording. Code for the fetch.
**Evidence.** Seven demo jobs. Corpus counts. No query log.
**Impact.** A person can ask in words.
**Risk.** Wording beyond S7 to S13 is Unknown.
**Confidence.** High for the demo set.
**Open questions.** FD-10 later.

### Agentic planning

**Finding.** GenAI draft. Propose and wait.
**Evidence.** Intent 10.3. BO-03 working answer. RT-02.
**Impact.** A reviewer receives a plan.
**Risk.** A draft applied without approval writes a record.
**Confidence.** High on the bound.
**Open questions.** FD-15 later.

### Rule evaluation

**Finding.** Deterministic.
**Evidence.** BP4. FD-08. REVIEW 2,090.
**Impact.** One archive test.
**Risk.** A model result would be a fifth test.
**Confidence.** High.
**Open questions.** Silent threshold still routes to review (BO-08 PROPOSED).

### Reconciliation

**Finding.** Deterministic.
**Evidence.** `reconcile()`. 67 REPLAY rows. Intent 10.2.
**Impact.** Accept, reject, and duplicate stay in code.
**Risk.** A language guess can drop a new feed.
**Confidence.** High.
**Open questions.** `reconcile()` was not executed in this unit.

### Intake de-duplication

**Finding.** Deterministic.
**Evidence.** 67 REPLAY ids. Repeated `message_id`.
**Impact.** RT-05 can confirm the drop.
**Risk.** Text similarity can merge two lots.
**Confidence.** High.
**Open questions.** None for the mark.

## Economics reconciliation

The 0C envelope in `docs/00-preflight/ai-economics/` stays the money picture. Phase 2 retires R-P2-01 through R-P2-08 in `economics-baseline-reconciliation.md`. Model-cost lines remain only for conflict explanation, natural-language query, and agentic planning. Those token cells stay Unknown. No price is invented.

## Engineering method used in this unit

| ID | Method choice | Authority | Evidence |
|---|---|---|---|
| ED-P2-01 | Null test uses `wafer_count`, `defect_count`, and `measured_yield`. Leave-one-out logistic regression plus per-field stumps. Majority baseline is 117/125. | team-force | `lot_id` is unique. `tool_id` has 30 values on 125 rows. In-sample fit on those keys would hide the null. |
| ED-P2-02 | Language help for “why this case is next” sits under conflict explanation. Triage ranking stays deterministic. | team-force | `priority()` does not read `cases.note`. |
| ED-P2-03 | No model file is written. The null test is a one-off check. | team-force | Phase 2 scope. FD-05 DECIDED: Reject ML. |

## What later phases may use

**Verified Fact.** `Execution_Plan.md` Phase 2 lifecycle line. This note sets what Phases 9 to 11 may use a model for: conflict explanation, natural-language query, and agentic planning, each with a person on every write.

Phases 9 to 11 still need FD-14, FD-15, FD-16, and FD-18 for floors and tool bounds. Those rows stay PENDING.

## What this file does not do

This file does not edit `Decision_Tracker.md`. It does not start Phase 3. It does not write the packaged database.
