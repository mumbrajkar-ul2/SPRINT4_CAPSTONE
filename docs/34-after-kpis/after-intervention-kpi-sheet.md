# After-intervention KPI sheet

| Field | Value |
|---|---|
| Stage | Phase 14 / 34 After-intervention KPIs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | MEASURED. Comparability confirmed in `kpi-comparability-check.md` before the family table. BO-11 stays PROPOSED. |
| Evidence sources | `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `docs/04-baseline-kpis/kpi-dictionary.md`; `Execution_Plan.md` section 9; FD-03; FD-14; FD-17; FD-19; FD-20; BO-02; BO-11; this-unit `python -m app.baseline`; this-unit `python -m app.workshop_check`; this-unit `python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s`; `docs/model-comparison/parity-results.json`; `docs/26-tevv/tevv-results.md`; `docs/32-finops/baseline-vs-actual-token-analysis.md`; `docs/16-repo-validation/regression-results.md` |
| Assumptions | Packaged database is the population. `MODEL_MODE=replay`. Freeze integers stay the Phase 12 measured run. |
| Unresolved issues | Exception cycle time Unknown. Aged backlog Unknown. API p95 Unknown. Recovery time Unknown. Dollars Unknown. Expert-label percent Unknown. Discovery time Unknown. |
| Residual risks | Presenting a modelled number as a real business benefit. Copying 0.603 as a labor saving. Copying 42 of 42 as a 90 or 95 floor. |

Numbers on this page use the frozen Phase 0 definitions. `kpi-comparability-check.md` confirmed those definitions before this table. FD-20 is DECIDED. Every number has one honesty label: REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.

---

## Finding

**Finding.** After the transform, Application A, and Application B, the packaged six-field baseline is unchanged: records 125, open_cases 89, urgent_cases 2, mean_amount 4982.61 SIMULATED, sites 6, hours_per_case 0.603 SIMULATED. Exception cycle time stays Unknown. Aged backlog stays Unknown. The parity harness this unit re-ran scored 14 rows, 12 matched, 2 differed. Freeze scored 42 of 42 cite-or-abstain. Shown Application A replay tokens are prompt_tokens 0 and completion_tokens 0. Dollars stay Unknown. ROI stays EDUCATIONAL.
**Evidence.** This-run `python -m app.baseline`. Pytest print `PARITY matched=12 differing=2`. `tevv-results.md` print `rows=42 pass=42 fail=0`. Phase 13 HB-32-01.
**Impact.** Supporting counts can be compared by exact match. Headline business movement stays unclaimed.
**Risk.** Calling the six-field match a cycle-time win.
**Confidence.** High on the six fields, the harness integers, and the token zeros. Unknown on headlines and dollars.
**Open questions.** Cycle-time clocks. Age threshold. BO-11 signer.

---

## Command lines this unit ran

Working directory for baseline and inventory: `c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE\fabpulse-legacy-workshop-v8-Semiconductor\fabpulse-legacy`.

```text
python -m app.baseline
python -m app.workshop_check
```

`python -m app.baseline` this unit:

```text
{"records": 125, "open_cases": 89, "urgent_cases": 2, "mean_amount": 4982.61, "sites": 6, "hours_per_case": 0.603}
```

Honesty: records, open_cases, urgent_cases, and sites are REAL. mean_amount and hours_per_case are SIMULATED.

`python -m app.workshop_check` this unit:

```text
{"profile": "Semiconductor lot process and excursion review", "counts": {"cases": 125, "events": 145, "source_messages": 15, "partner_feeds": 8567, "reference_versions": 180, "policy_exceptions": 224, "upstream_outages": 72, "batch_runs": 60}, "foreign_key_errors": 0, "integrity": "ok", "ok": true}
```

Honesty: REAL row counts.

Working directory for parity: `c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE`.

```text
python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s
```

Print line: `PARITY matched=12 differing=2`. Result: 7 passed in 17.58s. Honesty: REAL.

---

## Frozen family sheet after intervention

| Family | Measure | After value | Honesty | Label |
|---|---|---|---|---|
| Business outcome (headline) | Exception cycle time | Unknown | SIMULATED when later modelled | Unknown. `app/baseline.py` still has no field |
| Business outcome (headline) | Aged backlog | Unknown | SIMULATED when later modelled | Unknown. No age threshold. Python open_cases is 89 |
| Business outcome (supporting count) | records | 125 | REAL | Verified Fact of this-run tool output |
| Business outcome (supporting count) | open_cases | 89 | REAL for `status != CLOSED` | Verified Fact |
| Business outcome (supporting count) | urgent_cases | 2 | REAL for Python `priority()` | Verified Fact |
| Business outcome (supporting count) | sites | 6 | REAL | Verified Fact |
| Business outcome (queue flags) | Five scenario cases `open_operational` | All true on both apps (PH-RANK-01) | REAL | Verified Fact of harness |
| Decision quality | Correct disposition versus expert labels | Unknown percent | PRECOMPUTED | Unknown. No expert-label set |
| Decision quality | Harness disposition matches | 12 matched rows of 14 | REAL | Verified Fact of this pytest. No percent published |
| Decision quality | Recipe pair on PS000000016 | R02 and R01 on both apps | REAL | PH-S8-01 |
| Decision quality | Overlapping policy ids on FAB-00000002 | Five ids on both apps | REAL | PH-S10-01 |
| Decision quality | Recipe-release limit 2023 EMEA | 18600 | REAL | PH-RULE-01 |
| Decision quality | Recipe-release limit 2026 APAC | 25000 | REAL | Second check on PH-RULE-01 |
| Engineering productivity | Discovery time | Unknown | REAL later | Unknown |
| Engineering productivity | Tests accepted | Characterization 70 passed (Phase 7) | REAL | Prior Verified Fact. This unit did not re-run unittest |
| Engineering productivity | Lineage view | Application A `view_absent`. Application B returns the 2023 EMEA item | REAL | PH-S12-01 |
| Performance | API p95 | Unknown | REAL later | Unknown. One-request `duration_ms` is the time for that request |
| Performance | Retrieval p95 | Unknown | REAL later | Unknown |
| Performance | Agent time | Unknown | REAL later | Unknown |
| Reliability | Recovery time | Unknown | REAL later | Unknown |
| Reliability | Replay candidate count | 67 on both apps | REAL | PH-S7-02 |
| Reliability | Duplicate candidate on REPLAY-000000000 | true on both apps | REAL | PH-S7-01 |
| Reliability | INC-2025-014 owner_id | empty on both apps | REAL | PH-S11-01 and PH-S11-02 |
| Reliability | upstream_outages rows | 72 | REAL row count | This-run workshop_check |
| AI quality | Groundedness | 42 of 42 freeze rows cite or abstain | REAL. Floor Unknown | Phase 12 TV-26-01 |
| AI quality | Citation recall | 40 of 41 declared | REAL. Floor Unknown | Phase 12 TV-26-02 |
| AI quality | Citation precision | 79 of 79 | REAL. Floor Unknown | Phase 12 TV-26-03 |
| AI quality | Abstention | 6 of 42 | REAL. Floor Unknown | Phase 12 TV-26-04 |
| AI quality | Rejected schema claims | 0 | REAL | Phase 12 TV-26-06 |
| AI quality | Injection HTTP BLOCK | 7 of 7 Application B corpus posts | REAL | Phase 12 HB-26-02 |
| AI quality | Replay sentence wording | Saved file text | PRECOMPUTED | Phase 12 |
| Cost | Shown Application A replay query tokens | prompt_tokens 0, completion_tokens 0 | REAL for that path | Phase 13 HB-32-01. This pytest also wrote the same zeros on `/api/query` |
| Cost | Dollars | Unknown | Unknown | No invoice |
| Cost | hours_per_case | 0.603 | SIMULATED | Verified Fact of tool output |
| Cost | mean_amount | 4982.61 | SIMULATED | Verified Fact of tool output |
| ROI | Avoided effort minus cost | Unknown dollars | EDUCATIONAL | BO-11. See `docs/36-benefits/roi-model.md` |

Worked example. records is 125 after intervention. Phase 0 records was 125. The tool still counts rows in `cases`. The packaged file still has 125 rows.

Worked example. PH-CITE-01 posts the same recipe-mismatch question to both apps. Both return verdict `ANSWER` and citations `rule.recipe.mismatch_show_both` and `data.join.recipe_mismatch`. Honesty: REAL.

---

## Targets

None. Every target cell stays empty. FD-20 does not set a percent floor. BO-02 stays PROPOSED for success use of the headline pair.

---

## Honesty confirmation (FD-20)

**Verified Fact.** `Execution_Plan.md` section 9.

| Family | Plan honesty label | This sheet |
|---|---|---|
| Business outcome | SIMULATED | Headlines Unknown. Supporting counts REAL. mean_amount SIMULATED |
| Decision quality | PRECOMPUTED | Expert percent Unknown. Harness integers REAL |
| Engineering productivity | REAL | 70 tests prior REAL. Discovery time Unknown |
| Performance | REAL | p95 Unknown |
| Reliability | REAL | 67 and duplicate true are REAL. Recovery time Unknown |
| AI quality | REAL | Freeze integers REAL. Replay sentences PRECOMPUTED |
| Cost | REAL | Tokens 0 and 0 REAL on the shown replay path. Dollars Unknown. 0.603 SIMULATED |
| ROI | EDUCATIONAL | EDUCATIONAL |

A SIMULATED or EDUCATIONAL number is a modelled figure on synthetic data. This sheet claims no business dollar benefit.
