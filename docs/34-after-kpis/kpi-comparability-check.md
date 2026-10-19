# KPI comparability check

| Field | Value |
|---|---|
| Stage | Phase 14 / 34 After-intervention KPIs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | CONFIRMED for the six frozen supporting fields. Headline pair stays Unknown. BO-11 stays PROPOSED. |
| Evidence sources | `docs/04-baseline-kpis/kpi-dictionary.md`; `docs/04-baseline-kpis/measurement-methodology.md`; `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `Execution_Plan.md` section 9; FD-03; FD-17; FD-20; BO-02; BO-06a; `python -m app.baseline` on 2026-10-18 this unit; `python -m app.workshop_check` this unit; `python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s` this unit |
| Assumptions | The packaged `data/legacy.sqlite3` is still the population. This unit did not pass `--reset`. `MODEL_MODE=replay`. |
| Unresolved issues | Exception cycle time start and end fields stay unnamed. Aged backlog age threshold stays unnamed. Time window stays Unknown. Company signer stays Unknown. |
| Residual risks | Calling 89 the aged backlog. Changing a frozen formula to make a later number look better. Publishing a match percent. |

This file is the comparability check. It runs before any before-versus-after claim in `docs/35-value-leakage/` and `docs/36-benefits/`. FD-20 is DECIDED. Honesty labels stay REAL, PRECOMPUTED, SIMULATED, and EDUCATIONAL as in `Execution_Plan.md` section 9.

Engineering decision ED-P14-01, authority: team-force. After-intervention measurement uses the Phase 0 formulas and the same packaged 125-case file. The six supporting fields compare by exact match. This unit invents no tolerance percent.

---

## Finding

**Finding.** The eight KPI families are the families in `Execution_Plan.md` section 9. The headline pair is still exception cycle time and aged backlog. Both headline values stay Unknown. This unit re-ran `python -m app.baseline` and received records 125, open_cases 89, urgent_cases 2, mean_amount 4982.61, sites 6, hours_per_case 0.603. Those six fields match Phase 0 exactly. `python -m app.workshop_check` still prints cases 125, partner_feeds 8567, policy_exceptions 224, upstream_outages 72. The parity harness this unit re-ran printed `PARITY matched=12 differing=2` on 14 rows. Honesty of those integers: REAL.
**Evidence.** `kpi-dictionary.md`. This-run command output in `after-intervention-kpi-sheet.md`. Pytest stdout this unit. `docs/model-comparison/parity-results.json`.
**Impact.** Supporting six-field claims may use exact match. Headline movement stays unclaimed. Application A versus Application B uses the 14 harness rows.
**Risk.** Treating Unknown cycle time as a zero change would invent a business result.
**Confidence.** High on the six-field match, the inventory match, and the harness integers. Unknown on headlines.
**Open questions.** Named cycle-time clocks. Named age threshold. Who signs BO-11.

---

## Frozen definitions this check uses

**Verified Fact.** FD-03. The eight families are Business outcome, Decision quality, Engineering productivity, Performance, Reliability, AI quality, Cost, and ROI.

**Verified Fact.** FD-20. Honesty labels are the labels in `Execution_Plan.md` section 9.

| Family | Measure in the dictionary | Honesty label | Comparable now? |
|---|---|---|---|
| Business outcome | Exception cycle time | SIMULATED when later modelled | No numeric compare. Both sides Unknown |
| Business outcome | Aged backlog | SIMULATED when later modelled | No numeric compare. Both sides Unknown |
| Business outcome | records, open_cases, urgent_cases, sites | REAL for the Python fields | Yes. Exact match |
| Business outcome | mean_amount | SIMULATED | Yes. Exact match of the synthetic field |
| Decision quality | Correct disposition versus expert labels | PRECOMPUTED | Expert-label percent stays Unknown. Harness dispositions are comparable as REAL integers |
| Engineering productivity | Discovery time. Tests accepted | REAL | Tests accepted: characterization 70 is prior REAL. Discovery time stays Unknown |
| Performance | API p95. Retrieval p95. Agent time | REAL | p95 stays Unknown. One-request `duration_ms` is REAL for that request |
| Reliability | Recovery. Duplicate rate. Replay correctness | REAL | Recovery time stays Unknown. Replay count 67 is REAL on both apps |
| AI quality | Groundedness. Citation. Abstention. Rejected schema claims | REAL | Freeze integers are REAL. Percent floors stay Unknown |
| Cost | Tokens. Cost per resolved scenario | REAL | Shown replay tokens 0 and 0 are REAL. Dollars stay Unknown |
| ROI | Avoided effort minus cost | EDUCATIONAL | Formula only. No monetary benefit |

Worked example. Phase 0 `open_cases` is 89. This unit `open_cases` is 89. The formula is the count of packaged case rows where `status != CLOSED`. That is the same formula. The pair is comparable.

Worked example. Exception cycle time has no start field and no end field in `app/baseline.py`. Phase 0 stored Unknown. This unit still has no clock pair. There is no number to subtract.

---

## Population and method

| Item | Phase 0 | This unit | Match |
|---|---|---|---|
| File | Packaged `data/legacy.sqlite3` | Same packaged file | Yes |
| Generator | Not run | Not run | Yes |
| `--reset` | Not passed | Not passed | Yes |
| Tool | `python -m app.baseline` | `python -m app.baseline` | Yes |
| Working directory | `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` | Same directory | Yes |
| Formula for records | Count of `cases` rows | Same | Yes |
| Formula for open_cases | `status != CLOSED` | Same | Yes |
| Formula for urgent_cases | `priority()` returns urgent | Same | Yes |
| Formula for mean_amount | Mean of `cases.amount`, 2 decimals | Same | Yes |
| Formula for sites | Distinct `cases.site` | Same | Yes |
| Formula for hours_per_case | Sum of labor hours divided by sum of total cases, 3 decimals | Same | Yes |
| Time window | Unknown | Unknown | Both Unknown |
| Hardware | Laptop tools, no server for baseline | Same for the six fields. Apps used TestClient for parity | Six fields comparable |

**Verified Fact.** BO-06a. A case is open while any disposition or engineering action is still pending. The Python `status != CLOSED` test is a different rule. This check keeps both meanings labelled. It does not rewrite the frozen `open_cases` formula.

**Verified Fact.** Packaged amount above 50000 is 0. Honesty: REAL. The demo 50000 cutoff stays PROPOSED (BO-08).

---

## Application A versus Application B

**Verified Fact.** FD-17. The harness posts the same inputs to Application A and Application B. A row matches when both dispositions are equal. A differing row lists lake item ids. The runner prints integer matched and differing counts. It does not publish a match percent.

This unit re-ran `python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s`. Exit 0. Print line: `PARITY matched=12 differing=2`. Test count: 7 passed in 17.58s. Honesty: REAL.

The two differing rows:

| Row | Application A | Application B | Lake items cited |
|---|---|---|---|
| PH-S12-01 | `view_absent` | Lineage body for `rule.recipe_release.limit.v2023.emea` | `decision.fd06.two_apps`, `arch.graph.edges_table` |
| PH-RANK-02 | amount cutoff label `absent` | label `proposed` | `rule.threshold.demo_50000`, `rule.threshold.silent`, `decision.bo08.silent_threshold` |

Worked example. PH-S12-01 asks both apps for `GET /api/lineage/rule.recipe_release.limit.v2023.emea`. Application A has no lineage route, so the disposition is `view_absent`. Application B returns the 2023 EMEA item and `corr-p10b-doc-20261018-001`. The difference cites the two-app decision and the graph edges table.

---

## What this check allows and what it holds back

Allowed after this page:

- Exact-match statements on records 125, open_cases 89, urgent_cases 2, mean_amount 4982.61, sites 6, hours_per_case 0.603.
- Integer harness counts 14 rows, 12 matched, 2 differed.
- Freeze integers already measured in Phase 12, labelled REAL, with percent floors Unknown.
- Replay token pair 0 and 0 on the shown Application A query, labelled REAL.
- ROI text labelled EDUCATIONAL with every assumption stated.

Held back:

- A cycle-time improvement or deterioration number.
- An aged-backlog improvement or deterioration number.
- A dollar benefit.
- A match percent.
- A changed frozen definition.

**Verified Fact** of BO-11 working answer. Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit. The row stays PROPOSED. This check does not sign it.
