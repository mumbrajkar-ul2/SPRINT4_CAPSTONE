# Preliminary FinOps baseline

| Field | Value |
|---|---|
| Stage | Phase 0 / 0C AI-economics envelope |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL. Reconcile at Phase 2 and Phase 13 |
| Evidence sources | `app/baseline.py` both runs; `app/workshop_check.py` both runs; `scripts/verify_preloaded.py` both runs; `Execution_Plan.md` section 9; BO-11; `operations/baseline-evidence.md` |
| Assumptions | Synthetic `operating_costs` rows are the only money-shaped fields the current tools expose |
| Unresolved issues | Cloud bill, model invoice, and laptop-hour cost are Unknown |
| Residual risks | Reporting 4982.61 or 0.603 as a customer saving would break BO-11 and the honesty labels |

This is the money picture we can defend today. It is small. Phase 13 replaces it with measured run-time cost.

## What the tools produced

**Verified Fact.** Both runs of `python -m app.baseline` on 2026-10-18, Python 3.13.5, working directory `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`:

```text
{"records": 125, "open_cases": 89, "urgent_cases": 2, "mean_amount": 4982.61, "sites": 6, "hours_per_case": 0.603}
```

The two runs matched. Diff: no field differed.

**Verified Fact.** `operations/baseline-evidence.md` says values in this archive are synthetic and cannot be claimed as observed enterprise financial benefits.

## Allocation view

| Cost bucket | What exists now | Amount | Honesty | Label |
|---|---|---|---|---|
| Synthetic case amount | Mean of `cases.amount` | 4982.61 | SIMULATED | Verified Fact of tool output |
| Synthetic labor | `operating_costs.labor_hours / total_cases` | 0.603 hours per case | SIMULATED | Verified Fact of tool output |
| Synthetic infrastructure field | Column `infrastructure_usd` exists in `operating_costs` | Not emitted by `app/baseline.py` | Unknown as a reported number | Unknown |
| Model inference | No call was made | Unknown | Unknown | Unknown |
| Context Lake compute | Service does not exist | Unknown | Unknown | Unknown |
| Delivery agent tokens | Not metered in this unit | Unknown | Unknown | Unknown |
| Cloud platform | Not selected | Unknown | Unknown | Unknown |

## Rules for later money claims

**Verified Fact.** `Execution_Plan.md` section 9. Cost honesty is REAL when tokens and spend are measured. ROI honesty is EDUCATIONAL.

**Verified Fact.** BO-11 working answer. Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit.

**Verified Fact.** `Project_Intent.md` section 14.1. This document leaves targets open rather than manufacturing success criteria.

## Reconciliation

- Phase 2: retire cost assumptions for capabilities that will not use a model.
- Phase 13: write `docs/32-finops/` against this page.
- Phase 14: only verified improvements become value.

No dollar benefit is stated on this page.
