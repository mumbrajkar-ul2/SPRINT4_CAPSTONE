# Phase 14 — Measure, before-versus-after, ROI, and comparison

> Spine units: 34, 35, 36 | Guidelines 14, 23, 26 | Decision gate: FD-20, BO-11

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test before Phase 15 starts.

## Inputs

- Phase 0 baseline `docs/04-baseline-kpis/`
- Phase 11 parity harness `docs/model-comparison/parity-harness.md`
- Phase 12 eval `docs/26-tevv/tevv-results.md`
- `Execution_Plan.md` section 9 (KPI honesty labels)
- `Decision_Tracker.md` (section 6 row for Phase 14; section 5.1 for BO-11)

## Prompt

```text
# Phase 14 — Measure, before-versus-after, ROI, and comparison

## Objective
Measure the after-intervention KPIs against the frozen baseline, analyse the variance and leakage, and build the verified ROI. Run identical scenarios on both apps. Label every number with its honesty label.

## Scope
Analyse across the eight KPI families, the two-app comparison, and the ROI model. Exclude: unlabelled claims.

## Sub-stages
- 34 After-intervention KPIs. `docs/34-after-kpis/`: `after-intervention-kpi-sheet.md`, `adoption-metrics.md`, `exception-metrics.md`, `kpi-comparability-check.md`. Sub-gate: the frozen definitions are used; comparability is confirmed before any claim.
- 35 Before-versus-after and value leakage. `docs/35-value-leakage/`: `before-after-analysis.md`, `kpi-variance-table.md`, `value-leakage-analysis.md`, `confounder-analysis.md`. Sub-gate: improvement and deterioration are quantified; confounders are named.
- 36 ROI and benefits. `docs/36-benefits/`: `verified-benefits.md`, `roi-model.md`, `scenario-analysis.md`, `benefits-signoff.md`. Plus `docs/model-comparison/scorecard.md`. Sub-gate: only verified improvements become value; every number carries an honesty label; BO-11 is signed or deferred.

## Required analysis
Evaluate: each KPI family on both apps; the before-versus-after against the Phase 0 baseline; the A-versus-B comparison with each difference traced; the ROI model and its assumptions; the honesty label on every number. For every measure: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
Every number carries one honesty label: REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL. A SIMULATED or EDUCATIONAL number is a modelled figure on synthetic data, not a claimed business benefit. Classify claims as Verified Fact, Inference, Assumption, or Unknown.

## Constraints and guardrails
Do not present a modelled number as a real business benefit. Do not drop a label. Do not claim ROI without stating the assumptions. Do not change a frozen KPI definition to improve a result. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Honesty labels | REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL; set in `Execution_Plan.md` section 9 |
| Frozen baseline | The Phase 0 KPI definitions; never change one to improve a result |
| ROI (SME view for BO-11) | Label all ROI EDUCATIONAL; state each assumption; claim no monetary benefit |
| Comparison | Same scenarios on both apps; each A-versus-B difference traces to a lake item |

## Decision gate (before you start)
FD-20 honesty labels — set in `Execution_Plan.md` section 9; confirm here. BO-11 ROI assumptions — the Business Owner's; if PENDING, pause with the SME recommendation (label all ROI EDUCATIONAL; state each assumption; claim no monetary benefit).

## Required artifacts
The three folders above, plus `docs/model-comparison/scorecard.md`. Standard header on the docs.

## Completion gate
Complete only when every sub-gate passes: the scorecard is complete, every number is labelled, comparability is confirmed, and BO-11 is signed or deferred.

## Required final response
Return the seven items.

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/34-after-kpis/*` | Header. After-intervention KPI sheet using the frozen definitions. A comparability check confirmed before any claim. |
| `docs/35-value-leakage/*` | Header. Before-versus-after against the Phase 0 baseline. Improvement and deterioration quantified. Confounders named. |
| `docs/36-benefits/roi-model.md` | Header. The ROI model with every assumption stated. All ROI labelled EDUCATIONAL unless the Business Owner signs otherwise. |
| `docs/model-comparison/scorecard.md` | Header. Every number carries one honesty label. BO-11 recorded as signed or deferred with the SME recommendation shown. |

## Done test

Open `docs/model-comparison/scorecard.md`. Every number carries one honesty label. Re-run the parity harness; the comparison figures match the scorecard.
