# Before-versus-after analysis

| Field | Value |
|---|---|
| Stage | Phase 14 / 35 Before-versus-after and value leakage |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | MEASURED. Comparability confirmed. Headlines stay Unknown. BO-11 stays PROPOSED. |
| Evidence sources | `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `docs/34-after-kpis/after-intervention-kpi-sheet.md`; `docs/34-after-kpis/kpi-comparability-check.md`; `docs/26-tevv/tevv-results.md`; `docs/32-finops/baseline-vs-actual-token-analysis.md`; `docs/16-repo-validation/regression-results.md`; this-unit parity pytest |
| Assumptions | Before is Phase 0 on the packaged file. After is this unit on the same packaged file plus the built apps. `MODEL_MODE=replay`. |
| Unresolved issues | Cycle time Unknown on both sides. Aged backlog Unknown on both sides. Dollars Unknown on both sides. |
| Residual risks | Reading a zero delta on 89 open cases as a business win. Reading 0 replay tokens as a signed saving. |

This file compares the Phase 0 frozen sheet with the after-intervention sheet. `kpi-comparability-check.md` already confirmed the frozen definitions. This page does not change a definition to improve a result.

---

## Finding

**Finding.** The six supporting baseline fields are unchanged: records 125, open_cases 89, urgent_cases 2, mean_amount 4982.61 SIMULATED, sites 6, hours_per_case 0.603 SIMULATED. Headline exception cycle time stays Unknown before and after, so variance is Unknown. Aged backlog stays Unknown before and after, so variance is Unknown. Supporting eval and harness integers now exist after: 14 parity rows with 12 matched and 2 differed, freeze 42 of 42 cite-or-abstain, shown replay tokens 0 and 0. Those after numbers have no matching Phase 0 numeric baseline, because Phase 0 had no model call and no server. Dollars stay Unknown. ROI stays EDUCATIONAL.
**Evidence.** Phase 0 baseline JSON twice. This-unit baseline JSON. Pytest `PARITY matched=12 differing=2`. Phase 12 freeze print. Phase 13 HB-32-01.
**Impact.** Packaged queue volume did not move. New supporting evidence exists on quality, replay tokens, and two-app compare. Headline delay is still unmeasured.
**Risk.** Filling Unknown headlines with the six-field match.
**Confidence.** High on the six-field delta of zero. Unknown on headlines.
**Open questions.** Named clocks. Named age threshold. BO-11 signer.

---

## Business outcome

| Measure | Before (Phase 0) | After (this unit) | Variance | Honesty | Claim |
|---|---|---|---|---|---|
| Exception cycle time | Unknown | Unknown | Unknown | SIMULATED when modelled | No headline movement claimed |
| Aged backlog | Unknown | Unknown | Unknown | SIMULATED when modelled | No headline movement claimed |
| records | 125 | 125 | 0 | REAL | Exact match |
| open_cases | 89 | 89 | 0 | REAL for `status != CLOSED` | Exact match |
| urgent_cases | 2 | 2 | 0 | REAL for `priority()` | Exact match |
| sites | 6 | 6 | 0 | REAL | Exact match |
| mean_amount | 4982.61 | 4982.61 | 0 | SIMULATED | Exact match of the synthetic field |
| hours_per_case | 0.603 | 0.603 | 0 | SIMULATED | Exact match of the synthetic field |

Worked example. Phase 0 and this unit both printed `open_cases` 89. The packaged cases were not closed by the transform. The Python open volume is the same.

---

## Decision quality

| Measure | Before | After | Variance | Honesty |
|---|---|---|---|---|
| Correct disposition versus expert labels | Unknown | Unknown | Unknown | PRECOMPUTED |
| Harness matched rows | No harness | 12 of 14 | After-only integer | REAL. No percent |
| Harness differing rows | No harness | 2 of 14, each with lake ids | After-only integer | REAL |
| Recipe pair PS000000016 | Unknown at Phase 0 tools | R02 and R01 both apps | After-only | REAL |
| Limit 2023 EMEA | Unknown at Phase 0 tools | 18600 both apps | After-only | REAL |

Worked example. Phase 0 had no expert-label run. Phase 14 still has no expert-label percent. The 12 matched harness rows are REAL dispositions. They are not an expert-agreement score.

---

## Engineering productivity

| Measure | Before | After | Variance | Honesty |
|---|---|---|---|---|
| Discovery time | Unknown | Unknown | Unknown | REAL later |
| Tests accepted | Unknown in Phase 0 unit | Characterization 70 passed in Phase 7 | After-only prior REAL | REAL |
| Lineage view | No apps | Application A `view_absent`. Application B returns the item | Designed gap | REAL |

Worked example. Phase 7 recorded `Ran 70 tests in 5.775s` and OK. This unit did not re-run that suite. The 70 stays prior REAL.

---

## Performance

| Measure | Before | After | Variance | Honesty |
|---|---|---|---|---|
| API p95 | Unknown. Server not started | Unknown | Unknown | REAL later |
| Retrieval p95 | Unknown | Unknown | Unknown | REAL later |
| Agent time | Unknown | Unknown | Unknown | REAL later |
| One-request `duration_ms` | None captured | Captured on harness HTTP lines | After-only one-request times | REAL for that request. Not p95 |

Worked example. This unit's harness log includes Application A `GET /api/cases/REPLAY-000000000` `duration_ms` 99.272. That is the time for that one request. API p95 stays Unknown.

---

## Reliability

| Measure | Before | After | Variance | Honesty |
|---|---|---|---|---|
| Recovery time | Unknown | Unknown | Unknown | REAL later |
| upstream_outages rows | 72 | 72 | 0 | REAL row count |
| Replay candidate count | Feed volume 8567. Rate Unknown | 67 on both apps | After-only integer 67 | REAL |
| Duplicate candidate | Unknown at Phase 0 HTTP | true on both apps for REPLAY-000000000 | After-only | REAL |
| Quotes-without-id approve | Not measured in Phase 0 | Application B after SC-26-01 is HTTP 409 BLOCK | After-only | REAL |

Worked example. Phase 0 counted 8,567 partner_feeds rows. That is a volume. The after replay candidate count is 67. Those two numbers use different formulas. This page does not subtract 67 from 8567 as a rate.

---

## AI quality

| Measure | Before | After | Variance | Honesty |
|---|---|---|---|---|
| Groundedness | Unknown. No model call | 42 of 42 | After-only | REAL. Floor Unknown |
| Citation recall | Unknown | 40 of 41 | After-only | REAL. Floor Unknown |
| Citation precision | Unknown | 79 of 79 | After-only | REAL. Floor Unknown |
| Abstention | Unknown | 6 of 42 | After-only | REAL. Floor Unknown |
| Rejected schema claims | Unknown | 0 | After-only | REAL |
| Replay sentence text | None | Saved replay files | After-only | PRECOMPUTED |

Worked example. Phase 0 made no model call. Phase 0 groundedness stayed Unknown. The 42 of 42 figure is an after-only supporting integer from the freeze suite.

---

## Cost and ROI

| Measure | Before | After | Variance | Honesty |
|---|---|---|---|---|
| Shown replay prompt_tokens | Unknown | 0 | After-only on the shown path | REAL for that path |
| Shown replay completion_tokens | Unknown | 0 | After-only on the shown path | REAL for that path |
| Dollars | Unknown | Unknown | Unknown | Unknown |
| hours_per_case | 0.603 | 0.603 | 0 | SIMULATED |
| mean_amount | 4982.61 | 4982.61 | 0 | SIMULATED |
| ROI dollars | Unknown | Unknown | Unknown | EDUCATIONAL |

Worked example. Phase 13 wrote `prompt_tokens=0` and `completion_tokens=0` on the Application A replay query `Which port does the Context Lake REST listener use?`. This unit's harness also wrote those zeros on `/api/query`. Honesty: REAL for the replay path. Dollar cost stays Unknown. This page claims no monetary benefit.

---

## Improvement and deterioration (quantified)

Improvement that this page can name as supporting evidence, with no headline dollar:

- After-only freeze 42 of 42 cite-or-abstain. Honesty: REAL. Floor Unknown.
- After-only injection HTTP BLOCK 7 of 7 on Application B. Honesty: REAL.
- After-only person hold recorded on both apps. Honesty: REAL.
- After-only Application B lineage view. Honesty: REAL.
- After-only replay tokens 0 and 0 on the shown path. Honesty: REAL. Dollars Unknown.

No movement (delta 0) on frozen supporting counts:

- records 125, open_cases 89, urgent_cases 2, sites 6, mean_amount 4982.61 SIMULATED, hours_per_case 0.603 SIMULATED, outages 72, policy_exceptions 224.

Designed differences, not KPI deterioration of a shared field:

- PH-S12-01 Application A `view_absent`. Cites `decision.fd06.two_apps` and `arch.graph.edges_table`.
- PH-RANK-02 Application A label `absent`, Application B `proposed`. Cites the three threshold lake items.

Remaining supporting miss, after-only:

- Citation recall 40 of 41. GQ-19 cited `data.missing.lot_genealogy` and abstained. It did not also list `term.lot_genealogy`. Honesty: REAL.

Headline deterioration: Unknown. Headline improvement: Unknown. Both headlines stay Unknown.

**Verified Fact** of BO-11. This page claims no monetary benefit.
