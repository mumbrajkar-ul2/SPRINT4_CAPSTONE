# Confounder analysis

| Field | Value |
|---|---|
| Stage | Phase 14 / 35 Before-versus-after and value leakage |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | NAMED. Confounders listed before any ROI claim. |
| Evidence sources | `kpi-comparability-check.md`; `before-after-analysis.md`; BO-06a; BO-08; BO-09; FD-06; FD-14; FD-17; FD-19; `docs/04-baseline-kpis/measurement-methodology.md`; `docs/32-finops/baseline-vs-actual-token-analysis.md` |
| Assumptions | `MODEL_MODE=replay`. Packaged file is still seed-packaged data. Demo actors are the only users. |
| Unresolved issues | Live Azure behaviour Unknown. Plant-user behaviour Unknown. Time window Unknown. |
| Residual risks | Attributing the six-field delta of 0 to the apps when the packaged rows never changed. Attributing 0 tokens to model efficiency when replay plays a saved file. |

A confounder here is a fact that can make a before-versus-after or A-versus-B number mean the wrong thing. Each row names the fact, the measure it touches, and what this phase does about it.

---

## Finding

**Finding.** Ten named confounders sit between the intervention and a headline claim. The strongest are: the packaged 125 rows did not change, replay plays saved answers so live tokens are 0 by design, Python open and SME open are different rules, S12 and the amount-cutoff label are designed A-versus-B gaps, and money-shaped fields are synthetic. This phase leaves headlines Unknown and labels ROI EDUCATIONAL.
**Evidence.** Baseline exact match. HB-32-01. BO-06a. PH-S12-01. PH-RANK-02. `operations/baseline-evidence.md`.
**Impact.** A reader can see that 89 open cases and 0 replay tokens leave headline savings Unknown.
**Risk.** Dropping a confounder row to make ROI look signed.
**Confidence.** High on the named rows. Unknown on a later live Azure run.
**Open questions.** Live Azure token counts. Named cycle-time clocks.

---

## Named confounders

| Id | Confounder | Measure it touches | What this phase does |
|---|---|---|---|
| CF-01 | The packaged `cases` rows were not closed or regenerated | records, open_cases, urgent_cases | Report delta 0. Do not call it a process win |
| CF-02 | Time window on the packaged file is Unknown | Cycle time, aged backlog | Leave both Unknown |
| CF-03 | Python `status != CLOSED` versus BO-06a operational open | open_cases 89 | Keep 89 labelled as the Python field |
| CF-04 | `MODEL_MODE=replay` plays saved answers | prompt_tokens, completion_tokens | Label 0 and 0 REAL for the replay path. Dollars stay Unknown |
| CF-05 | mean_amount and hours_per_case are synthetic archive fields | Cost, ROI | Honesty SIMULATED. No monetary benefit |
| CF-06 | Demo actors, not company titles | Adoption | Adoption is laptop use. Production adoption Unknown |
| CF-07 | Freeze 42 is an eval set, not plant volume | AI quality | Integers REAL. Floors Unknown. No 90 or 95 target |
| CF-08 | PH-S12-01 is a designed two-app gap | Engineering productivity, A versus B | Cite `decision.fd06.two_apps` and `arch.graph.edges_table` |
| CF-09 | PH-RANK-02 label gap. Demo 50000 is PROPOSED | Business outcome ranking | Cite the three threshold items. BO-08 stays PROPOSED |
| CF-10 | PERSON hold writes runtime state that a later reset clears | Exception flags | Record the matched hold. Do not treat it as 89 minus 1 |

Worked example for CF-01. Phase 0 `python -m app.baseline` printed records 125. This unit printed records 125. The transform added `evaluate_live_policy` and two apps. It did not delete packaged rows. The count match shows the file is still the same population.

Worked example for CF-04. Phase 13 posted `Which port does the Context Lake REST listener use?` under replay. Stdout wrote `prompt_tokens=0` and `completion_tokens=0` with `event=replay_tokens`. Azure was not called. The zeros measure the replay path. Live Azure dollars stay Unknown.

Worked example for CF-08. Application A has no lineage route. Application B returns `rule.recipe_release.limit.v2023.emea` and `corr-p10b-doc-20261018-001`. The dispositions differ. The harness lists lake item ids. That difference is the two-app design. Each differing row lists lake item ids.

Worked example for CF-10. PH-PERSON-01 records `engineering_hold=1` on `PS000000016`. The harness then finishes. The next pytest calls `reset_runtime`. Packaged open_cases stays 89.

---

## Hardware and build

| Item | Value | Honesty |
|---|---|---|
| Lake version | 1.0.0 | REAL |
| Pin hash | `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` | REAL |
| Prompt semver | 1.0.0 | REAL prior |
| Application A port in product | 8100 | REAL |
| Application B port in product | 8110 | REAL |
| This harness compare | FastAPI TestClient, then a stopped-A uvicorn on 8110 or 18110 | REAL |
| Azure variables | Unset on the replay path | REAL for this run |

**Verified Fact.** FD-06. Application B reads the Context Lake. Application B does not import Application A rule functions.

---

## What would have to change before a headline claim

| Missing piece | Owner |
|---|---|
| Start timestamp and end timestamp for cycle time | Business Owner for success use (BO-02). Team-Force for the query |
| Age threshold for aged backlog | Business Owner. SME for operational open |
| Live Azure usage object | Human with credentials. NEEDS_HUMAN |
| Unit price | Invoice or recorded list price |
| Company signer on BO-11 | Business Owner |

Until those exist, this phase keeps headlines Unknown and ROI EDUCATIONAL.
