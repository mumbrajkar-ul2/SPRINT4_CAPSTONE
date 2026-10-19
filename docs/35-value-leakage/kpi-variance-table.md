# KPI variance table

| Field | Value |
|---|---|
| Stage | Phase 14 / 35 Before-versus-after and value leakage |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | MEASURED. Frozen definitions unchanged. |
| Evidence sources | `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `docs/34-after-kpis/after-intervention-kpi-sheet.md`; `docs/35-value-leakage/before-after-analysis.md`; this-unit baseline JSON; this-unit pytest; `docs/26-tevv/tevv-results.md` |
| Assumptions | Variance is after minus before when both sides are numbers from the same formula. Unknown minus Unknown stays Unknown. |
| Unresolved issues | Headline variances Unknown. Dollar variance Unknown. |
| Residual risks | Inventing a percent change from 42 of 42. Inventing a match percent from 12 and 2. |

This table is the numeric companion to `before-after-analysis.md`. Comparability was confirmed first in `docs/34-after-kpis/kpi-comparability-check.md`.

---

## Finding

**Finding.** Every frozen six-field variance is 0. Headline variances are Unknown. Harness after-only integers are matched 12 and differed 2 on 14 rows. Freeze after-only groundedness is 42 of 42. Shown replay tokens are 0 and 0. No cell publishes a percent change as a business benefit.
**Evidence.** Phase 0 tool JSON. This-unit tool JSON. Pytest print `PARITY matched=12 differing=2`. Phase 12 freeze print.
**Impact.** A reader can scan one table for delta 0, Unknown, and after-only.
**Risk.** Dividing 12 by 14.
**Confidence.** High on delta 0 and the after-only integers. Unknown on headlines.
**Open questions.** Cycle-time clocks. Age threshold.

---

## Frozen supporting fields (same formula both sides)

| Field | Before | After | After minus before | Honesty |
|---|---|---|---|---|
| records | 125 | 125 | 0 | REAL |
| open_cases | 89 | 89 | 0 | REAL for `status != CLOSED` |
| urgent_cases | 2 | 2 | 0 | REAL for `priority()` |
| sites | 6 | 6 | 0 | REAL |
| mean_amount | 4982.61 | 4982.61 | 0 | SIMULATED |
| hours_per_case | 0.603 | 0.603 | 0 | SIMULATED |
| cases (workshop_check) | 125 | 125 | 0 | REAL |
| events | 145 | 145 | 0 | REAL |
| partner_feeds | 8567 | 8567 | 0 | REAL |
| policy_exceptions | 224 | 224 | 0 | REAL |
| upstream_outages | 72 | 72 | 0 | REAL |
| batch_runs | 60 | 60 | 0 | REAL |

Worked example. hours_per_case is 0.603 before and 0.603 after. The formula is still sum of `operating_costs.labor_hours` divided by sum of `operating_costs.total_cases`, rounded to 3 decimals. The variance is 0. Honesty: SIMULATED. Labor dollars stay Unknown.

---

## Headline pair (same definition, no number)

| Field | Before | After | Variance | Honesty |
|---|---|---|---|---|
| Exception cycle time | Unknown | Unknown | Unknown | SIMULATED when modelled |
| Aged backlog | Unknown | Unknown | Unknown | SIMULATED when modelled |

Worked example. Aged backlog is the count of open cases older than an agreed age. The age is unnamed. Python open_cases is 89 on both sides. Aged backlog stays Unknown.

---

## After-only supporting integers

These cells were Unknown in Phase 0 because the tool, the server, or the eval did not exist yet. Variance is after-only. Honesty of the after integer is REAL unless noted.

| Measure | After | Honesty | Do not derive |
|---|---|---|---|
| Parity rows | 14 | REAL | A match percent |
| Parity matched | 12 | REAL | 12 divided by 14 |
| Parity differed | 2 | REAL | 2 divided by 14 |
| Characterization tests passed | 70 | REAL prior | A productivity percent |
| Freeze rows | 42 | REAL | A 90 or 95 floor |
| Freeze pass | 42 | REAL | Same |
| Freeze fail | 0 | REAL | Same |
| Groundedness | 42 of 42 | REAL. Floor Unknown | A decided percent target |
| Citation recall | 40 of 41 | REAL. Floor Unknown | Same |
| Citation precision | 79 of 79 | REAL. Floor Unknown | Same |
| Abstention | 6 of 42 | REAL. Floor Unknown | Same |
| Rejected schema claims | 0 | REAL | A pass percent |
| App B HTTP BLOCK | 7 of 7 | REAL | Same |
| Replay prompt_tokens (shown path) | 0 | REAL for that path | A dollar invoice |
| Replay completion_tokens (shown path) | 0 | REAL for that path | A dollar invoice |
| Recipe-release limit 2023 EMEA | 18600 | REAL | A new policy number |
| Recipe-release limit 2026 APAC | 25000 | REAL | A new policy number |
| Replay candidates | 67 | REAL | 67 divided by 8567 as a decided rate |

Worked example. Matched row count is 12. Differing row count is 2. 12 plus 2 is 14. The harness writes those integers. It does not write a match percent.

---

## Application A versus Application B (same scenarios)

| Row | Match | Honesty | Lake items if different |
|---|---|---|---|
| PH-S7-01 | true | REAL | empty |
| PH-S7-02 | true | REAL | empty |
| PH-S8-01 | true | REAL | empty |
| PH-S9-01 | true | REAL | empty |
| PH-S10-01 | true | REAL | empty |
| PH-S11-01 | true | REAL | empty |
| PH-S11-02 | true | REAL | empty |
| PH-S12-01 | false | REAL | `decision.fd06.two_apps`, `arch.graph.edges_table` |
| PH-RANK-01 | true | REAL | empty |
| PH-RANK-02 | false | REAL | `rule.threshold.demo_50000`, `rule.threshold.silent`, `decision.bo08.silent_threshold` |
| PH-CITE-01 | true | REAL | empty |
| PH-PERSON-01 | true | REAL | empty |
| PH-RULE-01 | true | REAL | empty |
| PH-BP7-01 | true | REAL | empty |

Totals: matched 12. Differed 2. Honesty: REAL. No percent.
