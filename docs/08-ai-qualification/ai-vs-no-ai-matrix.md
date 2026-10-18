# AI versus no-AI matrix

| Field | Value |
|---|---|
| Stage | Phase 2 / 8 AI-versus-no-AI qualification |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p2-fix-20261018-001 |
| Status | COMPLETE. This fix pass records FD-04 and FD-05 as DECIDED in Decision_Tracker.md v1.13. |
| Evidence sources | `intervention-options.md`; `minimum-intelligence-assessment.md`; `docs/05-current-state/conflict-catalogue.md`; `Project_Intent.md` sections 10 and 15.2; `app/legacy_logic.py`; `app/partner_feeds.py`; read-only null test on `wafer_lots.engineering_hold` on 2026-10-18 |
| Assumptions | A GenAI label is allowed only where this unit measured text variety. Agency follows the BO-03 working answer and stays PROPOSED. |
| Unresolved issues | Live user-query wording beyond the seven demo jobs is Unknown. Citation percent floors are Unknown. |
| Residual risks | Copying a GenAI label onto rule evaluation, reconciliation, or de-duplication would add a fifth written test of the same rule (BP4). |

Each capability has one label: GenAI, deterministic, or ML-rejected. Each row has a reason.

FD-04 is DECIDED in Decision_Tracker.md v1.13. Triage, rule evaluation, reconciliation, and intake de-duplication are deterministic. Conflict explanation, natural-language query, and agentic planning are GenAI. Predicting engineering_hold is ML-rejected. FD-05 is DECIDED: Reject ML. Majority and leave-one-out logistic regression are both 117/125.

## Matrix

| Capability | Recommended label | Reason | Claim label | Honesty |
|---|---|---|---|---|
| Triage | deterministic | `priority()` ranks on status, severity, and amount. The hold predictor did not beat 117 of 125. | Verified Fact | REAL for the two urgent cases and the null-test scores |
| Conflict explanation | GenAI | Flags stay in SQL. The explanation is a language job across 13 notes, 210 emails, 12,500 evidence payloads, and seven disagreement types. | Verified Fact for the counts. Inference that one template sentence will miss a type. | REAL for the counts |
| Natural-language query | GenAI | Seven demo jobs use different English. Code fetches the row. The model drafts the cited answer. | Verified Fact for the seven jobs and the corpus counts. | REAL for the counts |
| Agentic planning | GenAI | Intent 10.3 names five draft jobs. The model proposes. A person approves any write. | Verified Fact for the five named jobs. Inference for later plan-text variety. | REAL for the named jobs |
| Rule evaluation | deterministic | Four programs already disagree. FD-08 names the archive. The pass-or-fail result stays in code. | Verified Fact | REAL for 2,090 REVIEW objects |
| Reconciliation | deterministic | `reconcile()` tests key, schema, REPLAY, and quantity. Intent 10.2 keeps the final result in code. | Verified Fact | REAL for 67 REPLAY rows |
| Intake de-duplication | deterministic | Duplicate is a `message_id` or REPLAY status test. | Verified Fact | REAL for 67 REPLAY ids |
| `engineering_hold` prediction (FD-05 check) | ML-rejected | Leave-one-out logistic regression scored 117 of 125. The majority guess scored 117 of 125. | Verified Fact | REAL |

Worked example for triage. `priority('OPEN', 'CRITICAL', 1)` returns `urgent`. Two packaged cases have CRITICAL severity. Zero packaged cases have `amount > 50000`. The queue order uses those fields.

Worked example for the hold row. 117 lots have `engineering_hold = 0`. 8 lots have `engineering_hold = 1`. Always guessing 0 is right 117 times. The fitted model was right 117 times. Same score.

## Per-capability analysis

### Triage

**Finding.** Ranking is a four-branch function on stored fields.
**Evidence.** `app/legacy_logic.py`. Baseline urgent count 2. Null test 117/125 versus 117/125.
**Impact.** The next case is chosen without a model.
**Risk.** Adding a hold-probability column would change order with no gain over the majority guess.
**Confidence.** High.
**Open questions.** None for ranking.

### Conflict explanation

**Finding.** Each business problem is a different disagreement. A reader needs a cited sentence that names both values.
**Evidence.** Catalogue: 91 recipe mismatches; 11,985 clock splits; 67 REPLAY feeds; four rule files; five status lists; 34 active policies; 86 untrusted feeds. Text variety: 13 notes, 210 emails, 12,500 evidence payloads.
**Impact.** Demo scenarios S7 to S11 can show the two values and an explanation.
**Risk.** Instruction text in 86 feeds and 150 lake rows can be copied into the draft.
**Confidence.** High.
**Open questions.** Groundedness and abstention floors (FD-14, FD-18) stay Unknown.

### Natural-language query

**Finding.** The seven demo jobs are seven different questions. The stores they read vary in wording and structure.
**Evidence.** `Project_Intent.md` 15.2. Corpus counts in `minimum-intelligence-assessment.md`. No query-log table exists.
**Impact.** A person can ask in words and still receive a cited row.
**Risk.** An unseen wording after the demo set is Unknown.
**Confidence.** High for S7 to S13. Unknown beyond that set.
**Open questions.** FD-10 later freezes the golden questions.

### Agentic planning

**Finding.** Draft plans, tests, and handoffs are language jobs. Writes stay with a person.
**Evidence.** Intent 10.1 and 10.3. BO-03 working answer. RT-02.
**Impact.** A reviewer receives a proposed plan.
**Risk.** Applying the draft without approval writes a record. A wrong write can scrap material. **Verified Fact** of the SME reason in section 5.1.
**Confidence.** High on the bound. Medium on later plan wording.
**Open questions.** FD-15 later sets the tool allow-list.

### Rule evaluation

**Finding.** The same business test is already written four ways.
**Evidence.** Catalogue BP4. FD-08. REVIEW count 2,090.
**Impact.** One archive read can replace four local tests.
**Risk.** A model result would be a fifth test.
**Confidence.** High.
**Open questions.** A silent threshold still routes to review (BO-08 PROPOSED).

### Reconciliation

**Finding.** Accept, reject, and duplicate are written comparisons.
**Evidence.** `reconcile()` in `app/partner_feeds.py`. 67 REPLAY rows. Intent 10.2.
**Impact.** Month-end totals can use one status set.
**Risk.** A language guess can drop a new feed.
**Confidence.** High.
**Open questions.** `reconcile()` was not run in this unit. Rows stay REPLAY.

### Intake de-duplication

**Finding.** A replay is already marked on the row.
**Evidence.** 67 rows with `processing_status = 'REPLAY'` and `feed_id LIKE 'REPLAY-%'`. Repeated `message_id` is a duplicate in the gateway tests.
**Impact.** RT-05 can confirm the drop.
**Risk.** Text similarity can merge two lots.
**Confidence.** High.
**Open questions.** None for the mark.

### `engineering_hold` prediction

**Finding.** The model matched the majority guess.
**Evidence.** 8 of 125 lots held. Leave-one-out logistic regression 117/125. Majority 117/125. Honesty: REAL.
**Impact.** No production model is built.
**Risk.** Shipping a hold scorer would claim a skill the table does not show.
**Confidence.** High.
**Open questions.** None for this packaged table.

## What this file does not do

This file does not edit `Decision_Tracker.md`. FD-04 and FD-05 are already DECIDED there. It does not start Phase 3.
