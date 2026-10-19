# Value leakage analysis

| Field | Value |
|---|---|
| Stage | Phase 14 / 35 Before-versus-after and value leakage |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | ANALYSED. No monetary benefit claimed. BO-11 stays PROPOSED. |
| Evidence sources | `before-after-analysis.md`; `kpi-variance-table.md`; `docs/34-after-kpis/exception-metrics.md`; BO-02; BO-11; FD-14; FD-19; FD-20; `docs/32-finops/cost-per-outcome.md` |
| Assumptions | Value on the headlines means movement in exception cycle time or aged backlog. Supporting integers stay supporting. |
| Unresolved issues | Cycle time Unknown. Aged backlog Unknown. Dollars Unknown. Unit price Unknown. Wage Unknown. |
| Residual risks | Treating freeze 42 of 42 as a cycle-time cut. Treating 0 replay tokens as a signed saving. Treating 0.603 as recovered labor. |

Value leakage here means a supporting gain that does not show up as headline business movement. Headline business movement is exception cycle time and aged backlog (BO-02). Both stay Unknown. Packaged open_cases stays 89.

---

## Finding

**Finding.** Supporting after-only evidence exists: 12 matched harness rows, freeze 42 of 42 cite-or-abstain, injection BLOCK, person hold, Application B lineage, and replay tokens 0 and 0 on the shown path. Exception cycle time stays Unknown. Aged backlog stays Unknown. open_cases stays 89. Dollars stay Unknown. Those supporting gains therefore do not convert into a measured headline improvement or a monetary benefit on this laptop.
**Evidence.** Variance table. Exception metrics. Phase 12 TEVV. Phase 13 FinOps. BO-02. BO-11.
**Impact.** Quality and safety evidence is visible. Cycle time stays Unknown. Dollar return stays unclaimed.
**Risk.** Writing an EDUCATIONAL labor product as if it were booked savings.
**Confidence.** High on the missing headline numbers. Unknown on what a later signed clock would show.
**Open questions.** Named clocks. Age threshold. Unit price. BO-11 signer.

---

## Leakage rows

Each row names the supporting gain, the headline it does not fill, and the honesty labels.

| Id | Supporting gain | What stays empty | Honesty of the gain | Honesty of the empty cell |
|---|---|---|---|---|
| VL-01 | Freeze 42 of 42 cite or abstain | Exception cycle time | REAL. Floor Unknown | Unknown |
| VL-02 | 12 matched harness dispositions | Aged backlog | REAL. No percent | Unknown |
| VL-03 | Injection HTTP 409 BLOCK | open_cases still 89 | REAL | REAL for the 89 |
| VL-04 | Person hold on PS000000016 | Cycle time for that case | REAL | Unknown |
| VL-05 | Application B lineage view | Discovery time | REAL | Unknown |
| VL-06 | Replay prompt_tokens 0 and completion_tokens 0 | Dollars per case | REAL for that path | Unknown |
| VL-07 | hours_per_case 0.603 unchanged | Labor dollars | SIMULATED | Unknown |
| VL-08 | mean_amount 4982.61 unchanged | Customer money saved | SIMULATED | Unknown |
| VL-09 | Replay candidate count 67 visible | Duplicate rate over time | REAL | Unknown as a rate |
| VL-10 | Citation recall 40 of 41 | A groundedness percent floor | REAL | Unknown |

Worked example for VL-01. The freeze suite scored 42 rows and printed `rows=42 pass=42 fail=0`. Every scored AI answer cited a lake item or abstained. Exception cycle time still has no start field and no end field. The 42 of 42 figure does not become a shorter case clock.

Worked example for VL-06. Application A replay wrote `prompt_tokens=0` and `completion_tokens=0`. Honesty: REAL for that path. Unit price stays Unknown. Tokens times Unknown price stays Unknown dollars. The zeros do not become a booked saving.

Worked example for VL-07. hours_per_case is 0.603 before and after. Honesty: SIMULATED. A wage is unnamed. This page does not multiply 0.603 by 125 and a wage.

---

## Why the headlines stay empty

**Verified Fact.** `app/baseline.py` still emits no cycle-time field.

**Verified Fact.** No age threshold sits in the governed source. BO-08 stays PROPOSED for silent numbers.

**Verified Fact.** The packaged 125 rows were not closed by Application A or Application B as a batch. open_cases is still 89.

**Verified Fact.** FD-19. Numeric cost floors stay Unknown. This phase invents no dollar benefit.

The intervention added routes, a lake, a freeze suite, and a person gate. It did not rewrite the packaged `status` column on the 89 open rows. Queue volume on that file therefore stays 89.

---

## What is allowed to be called verified later

Only a gain that keeps its honesty label and that fills a frozen measure. See `docs/36-benefits/verified-benefits.md`. A modelled ROI figure stays EDUCATIONAL. A SIMULATED money field stays SIMULATED.

This page claims no monetary benefit.
