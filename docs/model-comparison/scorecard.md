# Before-and-after scorecard

| Field | Value |
|---|---|
| Stage | Phase 14 / 36 ROI and benefits. Two-app scorecard |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | COMPLETE for this unit. Every number labelled. BO-11 recorded PROPOSED, deferred, UNSIGNED |
| Evidence sources | `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `docs/34-after-kpis/after-intervention-kpi-sheet.md`; `docs/34-after-kpis/kpi-comparability-check.md`; `docs/35-value-leakage/kpi-variance-table.md`; `docs/36-benefits/roi-model.md`; `docs/36-benefits/benefits-signoff.md`; `docs/model-comparison/parity-harness.md`; `docs/model-comparison/parity-results.json`; this-unit `python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s`; `docs/26-tevv/tevv-results.md`; FD-17; FD-20; BO-11 |
| Assumptions | `MODEL_MODE=replay`. Packaged 125-case file is the population. Freeze integers stay the Phase 12 measured run |
| Unresolved issues | Exception cycle time Unknown. Aged backlog Unknown. Dollars Unknown. API p95 Unknown. Discovery time Unknown. Signer name Unknown |
| Residual risks | Publishing a match percent. Presenting EDUCATIONAL ROI as a booked return. Changing a frozen KPI definition |

This scorecard is the Phase 14 compare sheet. Comparability was confirmed in `docs/34-after-kpis/kpi-comparability-check.md` before these claims. FD-20 is DECIDED. Honesty labels are REAL, PRECOMPUTED, SIMULATED, and EDUCATIONAL as in `Execution_Plan.md` section 9. Every number on this page carries one of those labels.

Engineering decision ED-P14-04, authority: team-force. The scorecard prints integer matched 12 and differing 2. It does not print a match percent. Those integers come from this unit's pytest run.

---

## Finding

**Finding.** Frozen six-field baseline after intervention is records 125, open_cases 89, urgent_cases 2, mean_amount 4982.61 SIMULATED, sites 6, hours_per_case 0.603 SIMULATED. Headlines stay Unknown. This unit re-ran the parity harness: 14 rows, matched 12, differed 2. Each difference cites lake items. Shown Application A replay tokens are prompt_tokens 0 and completion_tokens 0. Dollars stay Unknown. All ROI cells are EDUCATIONAL. BO-11 stays PROPOSED and UNSIGNED.
**Evidence.** This-unit `python -m app.baseline`. Pytest print `PARITY matched=12 differing=2`. `parity-results.json` `matched_row_count` 12 and `differing_row_count` 2. Phase 13 HB-32-01. `benefits-signoff.md`.
**Impact.** The 40-minute path can show a labelled scorecard. Dollar return stays unclaimed. BO-11 stays UNSIGNED.
**Risk.** Dividing 12 by 14. Copying 0.603 as recovered labor.
**Confidence.** High on the six fields, the harness integers, and the token zeros. Unknown on headlines and dollars.
**Open questions.** BO-11 signer. Cycle-time clocks. Age threshold. Unit price.

---

## BO-11 (deferred)

**Tracker status.** PROPOSED. Accepted 2026-10-18. Not signed DECIDED.

**SME recommendation (mandatory to show).** Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit. The data is synthetic. An EDUCATIONAL label keeps the claim honest and defensible to judges.

**This unit.** `docs/36-benefits/benefits-signoff.md` stays UNSIGNED. Signer name Unknown. This scorecard does not sign BO-11. This scorecard does not invent a signer.

---

## FD-20 honesty labels

| Family | Plan label | How this scorecard uses it |
|---|---|---|
| Business outcome | SIMULATED | Headlines Unknown. Supporting counts REAL. mean_amount SIMULATED |
| Decision quality | PRECOMPUTED | Expert percent Unknown. Harness integers REAL |
| Engineering productivity | REAL | 70 tests prior REAL. Lineage REAL. Discovery time Unknown |
| Performance | REAL | p95 Unknown |
| Reliability | REAL | 67 and duplicate true REAL. Recovery time Unknown |
| AI quality | REAL | Freeze integers REAL. Replay sentences PRECOMPUTED |
| Cost | REAL | Tokens 0 and 0 REAL on the shown replay path. Dollars Unknown. 0.603 SIMULATED |
| ROI | EDUCATIONAL | EDUCATIONAL. Unknown dollars |

A SIMULATED or EDUCATIONAL number is a modelled figure on synthetic data. This scorecard claims no monetary benefit.

---

## Headline pair (BO-02)

| Measure | Before | After | Application A | Application B | Honesty |
|---|---|---|---|---|---|
| Exception cycle time | Unknown | Unknown | Unknown | Unknown | SIMULATED when later modelled |
| Aged backlog | Unknown | Unknown | Unknown | Unknown | SIMULATED when later modelled |

Worked example. Python open_cases is 89 before and 89 after. Honesty: REAL for `status != CLOSED`. Aged backlog stays Unknown. An age threshold is still unnamed.

---

## Frozen supporting counts

| Measure | Before | After | Variance | Honesty |
|---|---|---|---|---|
| records | 125 | 125 | 0 | REAL |
| open_cases | 89 | 89 | 0 | REAL for `status != CLOSED` |
| urgent_cases | 2 | 2 | 0 | REAL for Python `priority()` |
| sites | 6 | 6 | 0 | REAL |
| mean_amount | 4982.61 | 4982.61 | 0 | SIMULATED |
| hours_per_case | 0.603 | 0.603 | 0 | SIMULATED |

Worked example. This unit ran `python -m app.baseline` in `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` and received `{"records": 125, "open_cases": 89, "urgent_cases": 2, "mean_amount": 4982.61, "sites": 6, "hours_per_case": 0.603}`. Phase 0 printed the same JSON.

---

## Application A versus Application B (parity)

This unit command:

```text
python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s
```

Print line: `PARITY matched=12 differing=2`. Result: 7 passed in 17.58s. Honesty: REAL.

`docs/model-comparison/parity-results.json` records `matched_row_count` 12 and `differing_row_count` 2. Honesty: REAL. Lake version 1.0.0. Pin `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`.

| Row | Compared field | Match | Application A | Application B | Lake items if different | Honesty |
|---|---|---|---|---|---|---|
| PH-S7-01 | duplicate_candidate | true | true | true | empty | REAL |
| PH-S7-02 | replay_candidate_count | true | 67 | 67 | empty | REAL |
| PH-S8-01 | recipe_pair | true | R02 / R01 | R02 / R01 | empty | REAL |
| PH-S9-01 | clock_pair | true | 2020-12-30 / 2021-01-01 | same pair | empty | REAL |
| PH-S10-01 | overlapping_policy_ids | true | five POL ids | same five ids | empty | REAL |
| PH-S11-01 | owner_id | true | empty | empty | empty | REAL |
| PH-S11-02 | owner_id | true | empty | empty | empty | REAL |
| PH-S12-01 | lineage_view | false | view_absent | 2023 EMEA item, corr-p10b-doc-20261018-001, 12 rows | decision.fd06.two_apps, arch.graph.edges_table | REAL |
| PH-RANK-01 | open_operational | true | five scenario cases true | same five true | empty | REAL |
| PH-RANK-02 | amount_cutoff_label | false | absent | proposed | rule.threshold.demo_50000, rule.threshold.silent, decision.bo08.silent_threshold | REAL |
| PH-CITE-01 | query_verdict | true | ANSWER plus two ids | same | empty | REAL |
| PH-PERSON-01 | approval_recorded | true | hold, engineering_hold=1 | same | empty | REAL |
| PH-RULE-01 | limit_value | true | 18600 | 18600. Second check 25000 | empty | REAL |
| PH-BP7-01 | block | true | true | true | empty | REAL |

Totals: 14 rows. Matched 12. Differed 2. Honesty: REAL. No match percent is written.

Worked example. PH-S12-01. Application A has no lineage route, so the disposition is `view_absent`. Application B returns item `rule.recipe_release.limit.v2023.emea` and prints `corr-p10b-doc-20261018-001`. The difference cites `decision.fd06.two_apps` and `arch.graph.edges_table`.

Worked example. PH-RANK-02. Application A queue body has no amount cutoff label. Application B labels demo 50000 as `proposed`. Live silent cutoff stays HOLD_FOR_REVIEW.

---

## Other families

| Family | Measure | After | Honesty |
|---|---|---|---|
| Decision quality | Expert-label percent | Unknown | PRECOMPUTED |
| Engineering productivity | Discovery time | Unknown | REAL later |
| Engineering productivity | Tests accepted | 70 characterization passed | REAL prior |
| Performance | API p95 | Unknown | REAL later |
| Performance | Retrieval p95 | Unknown | REAL later |
| Performance | Agent time | Unknown | REAL later |
| Reliability | Recovery time | Unknown | REAL later |
| Reliability | upstream_outages rows | 72 | REAL |
| AI quality | Groundedness | 42 of 42 | REAL. Floor Unknown |
| AI quality | Citation recall | 40 of 41 | REAL. Floor Unknown |
| AI quality | Citation precision | 79 of 79 | REAL. Floor Unknown |
| AI quality | Abstention | 6 of 42 | REAL. Floor Unknown |
| AI quality | Rejected schema claims | 0 | REAL |
| AI quality | App B HTTP BLOCK | 7 of 7 | REAL |
| AI quality | Replay sentence wording | Saved files | PRECOMPUTED |
| Cost | Shown App A replay prompt_tokens | 0 | REAL for that path |
| Cost | Shown App A replay completion_tokens | 0 | REAL for that path |
| Cost | Dollars | Unknown | Unknown |
| ROI | Avoided effort minus cost | Unknown dollars | EDUCATIONAL |

Worked example. Freeze print `rows=42 pass=42 fail=0` is prior REAL from Phase 12. Percent floors stay Unknown. This scorecard does not write 90 or 95 as a target.

---

## ROI block (EDUCATIONAL)

| Cell | Value | Honesty |
|---|---|---|
| Avoided effort | Unknown | EDUCATIONAL |
| Cost dollars | Unknown | EDUCATIONAL |
| ROI | Unknown | EDUCATIONAL |
| Monetary benefit claimed | None | Verified Fact of this page |
| BO-11 | PROPOSED, UNSIGNED | Verified Fact of `benefits-signoff.md` |

Assumptions are listed in `docs/36-benefits/roi-model.md`. Scenario R, A, and L are in `docs/36-benefits/scenario-analysis.md`.

---

## Phase boundary

This unit stops at the Phase 14 scorecard. Phase 15 stays unstarted. Frozen KPI definitions stay as written in `docs/04-baseline-kpis/kpi-dictionary.md`. Tracker files stay for the coordinator.
