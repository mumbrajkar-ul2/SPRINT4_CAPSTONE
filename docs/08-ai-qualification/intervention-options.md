# Intervention options

| Field | Value |
|---|---|
| Stage | Phase 2 / 8 AI-versus-no-AI qualification |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p2-fix-20261018-001 |
| Status | COMPLETE. This fix pass records FD-04 and FD-05 as DECIDED in Decision_Tracker.md v1.13. |
| Evidence sources | `docs/05-current-state/conflict-catalogue.md`; `Project_Intent.md` sections 10 and 15.2; `app/legacy_logic.py`; `app/partner_feeds.py`; read-only SQLite URI `mode=ro` on `data/legacy.sqlite3` and `data/enterprise_legacy.sqlite3` on 2026-10-18; `Decision_Tracker.md` FD-04, FD-05, BO-03, section 5.1 |
| Assumptions | The packaged 125-lot `wafer_lots` table is the measurement population for this freeze. BO-03 stays PROPOSED. The working answer is used as the agency bound. |
| Unresolved issues | BO-03 stays PROPOSED and unsigned. Token counts and model unit prices stay Unknown. |
| Residual risks | A later builder who treats every option as a model task will add cost and write-risk where code already has a test. |

This file names the four ways a capability can be built. It does not change a record. The chosen label for each capability is in `ai-vs-no-ai-matrix.md` and `qualification-decision.md`.

## The four options

| Option | What it does | When this note allows it |
|---|---|---|
| Deterministic code | A written test on stored fields returns one result. The same inputs give the same output. | The test already exists, or the fields needed for the test already exist. |
| GenAI | A language model drafts text, a summary, or a plan from retrieved records. A person still approves any write. | The task is a language job and this unit measured text variety. |
| Machine learning | A fitted model predicts a label from lot fields. | Only if the null test beats the majority-class guess on `engineering_hold`. |
| Neither | A person does the work with no model and no new rule. | The evidence is too thin to pick the other three. That case routes to review. |

**Verified Fact.** FD-04 is DECIDED. Triage, rule evaluation, reconciliation, and intake de-duplication are deterministic. Conflict explanation, natural-language query, and agentic planning are GenAI. Predicting engineering_hold is ML-rejected.

**Verified Fact.** FD-05 is DECIDED: Reject ML. Majority and leave-one-out logistic regression are both 117/125.

**Verified Fact.** BO-03 working answer, accepted 2026-10-18, status PROPOSED. AI explains and proposes. A person approves every record-changing action. No autonomous writes.

Worked example. `priority('OPEN', 'CRITICAL', 1)` in `app/legacy_logic.py` returns `urgent`. That is deterministic code. The function reads status, severity, and amount. It does not call a model.

## Options per capability

### Triage

| Option | Allowed here | Why |
|---|---|---|
| Deterministic code | Yes. Recommended. | `priority()` already ranks on status, severity, and amount. Two packaged cases are urgent because severity is CRITICAL. Amount above 50,000 is 0 on `cases`. **Verified Fact.** |
| GenAI | No for ranking. | Ranking does not read `cases.note`. The 13 distinct notes are unused by `priority()`. **Verified Fact.** |
| Machine learning | No. | Predicting `engineering_hold` scored 117 of 125. The majority guess also scored 117 of 125. **Verified Fact.** Honesty: REAL. |
| Neither | No. | The ranking test already exists. |

**Finding.** Queue order can be produced by the existing four-branch function.
**Evidence.** `app/legacy_logic.py`. Catalogue BP4 and BP5. Null test in `minimum-intelligence-assessment.md`.
**Impact.** The next case to touch is chosen by stored fields.
**Risk.** A model score added to the queue would change order without beating the majority hold guess.
**Confidence.** High.
**Open questions.** None for ranking. Language about why a case is next is the conflict-explanation job.

### Conflict explanation

| Option | Allowed here | Why |
|---|---|---|
| Deterministic code | Yes for the mismatch flags. | SQL already counts 91 recipe mismatches, 11,985 clock splits, 67 REPLAY feeds, 34 active policies, and 2,090 REVIEW objects. **Verified Fact.** |
| GenAI | Yes. Recommended for the English (and mixed-language) explanation. | The disagreement type changes by case. Notes use 13 texts in three languages. Emails are 210 distinct files. Evidence payloads are 12,500 distinct strings. **Verified Fact.** |
| Machine learning | No. | The job is to name why two sources disagree. It is not to predict a hold label. |
| Neither | No. | The demo must explain S7 to S11. `Project_Intent.md` section 15.2. **Verified Fact.** |

**Finding.** Code can raise the flag. A language model can draft the explanation a person reads.
**Evidence.** Conflict catalogue BP1 to BP7. Text-variety counts in `minimum-intelligence-assessment.md`. Intent section 10.1.
**Impact.** A reviewer sees both values and a cited sentence.
**Risk.** Untrusted feed text tells a reader to approve. BP7 counted 86 feeds, 150 lake instruction rows, 22 source-document hits, and 3 emails. A model that follows that text can propose a bad write. **Verified Fact** for the counts. **Inference** for the write risk.
**Confidence.** High.
**Open questions.** Citation and abstention numeric floors stay Unknown (FD-14, FD-18).

### Natural-language query

| Option | Allowed here | Why |
|---|---|---|
| Deterministic code | Yes for the lookup. | The answer still has to come from a row, a file, or a lake item. |
| GenAI | Yes. Recommended for the question wording. | The seven demo jobs in `Project_Intent.md` section 15.2 are seven different English requests. The stores they read have measured variety. **Verified Fact.** |
| Machine learning | No. | There is no labelled query-intent table. |
| Neither | No. | The defence must answer those seven jobs in words. |

**Finding.** A person will ask in different words. Code fetches the rows. A model drafts the answer with citations.
**Evidence.** Intent 15.2. Text-variety table in `minimum-intelligence-assessment.md`.
**Impact.** One question can span recipe, clock, and policy rows.
**Risk.** No stored user-query log exists. The seven demo texts are the measured question set. **Verified Fact.**
**Confidence.** High for the demo set. The live wording beyond those seven is Unknown.
**Open questions.** FD-10 later names the golden-question set.

### Agentic planning

| Option | Allowed here | Why |
|---|---|---|
| Deterministic code | Yes for tool allow-lists and stop rules. | FD-02. The model gets read-only tools only. **Verified Fact.** |
| GenAI | Yes. Recommended for the draft plan. | Intent section 10.3 names five draft jobs: investigation, feed disposition, change-impact, evidence pack, and handoff. **Verified Fact.** |
| Machine learning | No. | Planning here is draft text for a person. It does not predict a hold label. |
| Neither | No. | Intent section 10.1 already names draft plans as a language job. |

**Finding.** A model may draft a plan. A person accepts or rejects it.
**Evidence.** Intent 10.1 and 10.3. BO-03 working answer. Decision_Tracker section 7 (RT-01 to RT-06).
**Impact.** A reviewer receives a proposed next step with citations.
**Risk.** A draft that is applied without RT-02 approval becomes a write. BO-03 forbids that write. The row is still PROPOSED. **Verified Fact.**
**Confidence.** High on the agency bound. Plan-text variety in a future app is Inference.
**Open questions.** FD-15 (tool allow-list and recursion limit) is later.

### Rule evaluation

| Option | Allowed here | Why |
|---|---|---|
| Deterministic code | Yes. Recommended. | Four programs already apply tests. FD-08 names the governed archive as canonical. **Verified Fact.** |
| GenAI | No for the pass-or-fail result. | A fifth wording of the same rule would add another disagreement. That is BP4. **Verified Fact** for the four files. **Inference** for the fifth-wording harm. |
| Machine learning | No. | The archive already stores the threshold. |
| Neither | No. | The night batch and the API already evaluate. |

**Finding.** The pass-or-fail result stays in code that reads the archive.
**Evidence.** Catalogue BP4. FD-08. Intent section 10.2.
**Impact.** Queue size and month-end totals can share one test.
**Risk.** A model that restates a limit can drift from the archive number.
**Confidence.** High.
**Open questions.** None for the evaluation method. BO-08 stays PROPOSED for a silent threshold.

### Reconciliation

| Option | Allowed here | Why |
|---|---|---|
| Deterministic code | Yes. Recommended. | `reconcile()` already tests missing key, unsupported schema, REPLAY, and negative quantity. **Verified Fact.** |
| GenAI | No for the accept-or-duplicate result. | Intent section 10.2 keeps final reconciliation deterministic. **Verified Fact.** |
| Machine learning | No. | The tests are written comparisons. |
| Neither | No. | The function already exists. |

**Finding.** Accept, reject, and duplicate are code outcomes.
**Evidence.** `app/partner_feeds.py` `reconcile()`. Catalogue BP2 (67 REPLAY rows). Intent 10.2.
**Impact.** A replay is marked by a status test.
**Risk.** A model that guesses "looks like a duplicate" can drop a new feed.
**Confidence.** High.
**Open questions.** This unit did not run `reconcile()`. The 67 rows remain REPLAY. **Verified Fact.**

### Intake de-duplication

| Option | Allowed here | Why |
|---|---|---|
| Deterministic code | Yes. Recommended. | A REPLAY status, a `REPLAY-` feed id, and a repeated `message_id` are stored tests. **Verified Fact.** |
| GenAI | No for the duplicate mark. | The identifier is already on the row. |
| Machine learning | No. | The packaged duplicate rule uses an identifier and a status. |
| Neither | No. | The replay rows already exist to be marked. |

**Finding.** Duplicate intake is an identifier and status test.
**Evidence.** Catalogue BP2. `app/partner_feeds.py`. `docs/07-repo-assessment/baseline-behaviour.md` (repeated `message_id` is a duplicate).
**Impact.** A replay stays visible and can be confirmed at RT-05.
**Risk.** A language guess can treat two different lots as one.
**Confidence.** High.
**Open questions.** None for the mark. A person still confirms the drop (RT-05).

## Related option that is not one of the seven capabilities

Predicting `engineering_hold` from lot fields was the FD-05 machine-learning check. The recommended option is Neither for a production model, recorded as ML-rejected in the matrix. See `minimum-intelligence-assessment.md`.

## What this file does not do

This file does not edit `Decision_Tracker.md`. It does not write `data/legacy.sqlite3`.
