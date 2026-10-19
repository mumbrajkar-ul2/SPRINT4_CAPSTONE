# Drift framework

| Field | Value |
|---|---|
| Stage | Phase 15 / 39 Drift and continuous improvement |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE for this unit. Watch values are measured integers already on disk. Percent floors stay Unknown |
| Evidence sources | `docs/11-data-context/knowledge-model.md`; FD-14; FD-17; FD-18; FD-20; FD-22; `docs/26-tevv/tevv-results.md`; `docs/model-comparison/scorecard.md`; `docs/04-baseline-kpis/kpi-dictionary.md`; `apps/app_a/prompts/` semver 1.0.0 |
| Assumptions | Drift here means a later change that moves a frozen count, a lake version, a prompt semver, or a BLOCK behaviour. `MODEL_MODE=replay` |
| Unresolved issues | Numeric percent floors Unknown. Exception cycle time Unknown. Aged backlog Unknown. Dollar unit price Unknown |
| Residual risks | Copying 42 of 42 into a 90 percent floor. Dividing 12 by 14. Raising the lake version without an ADR |

This file names what an operator watches after handover. A watch value is a number already measured. It is not a new target.

Engineering decision ED-P15-03, authority: team-force. Drift families are lake, prompt, freeze, parity, baseline, injection, and replay files. Each family cites a phase that already ran.

---

## Finding

**Finding.** Seven families already have a measured snapshot. Lake version 1.0.0 with 148 items. Prompt semver 1.0.0. Freeze `rows=42 pass=42 fail=0`. Parity 14 rows, matched 12, differing 2. Baseline records 125, open_cases 89, urgent_cases 2, sites 6. Injection HTTP 409 BLOCK after SC-24-01 and SC-26-01. Replay folder has 77 files besides README. Percent floors stay Unknown.
**Evidence.** Phase 5, Phase 9, Phase 11, Phase 12, Phase 14, this-unit file count.
**Impact.** A later change can be compared to those snapshots.
**Risk.** Treating a snapshot as a signed SLO percent.
**Confidence.** High on the snapshots. Unknown on later hours-to-detect.
**Open questions.** Who raises the lake version. Who may retune a prompt.

---

## Families to watch

| Family | Snapshot on disk | Honesty | Phase that measured it |
|---|---|---|---|
| Lake version | 1.0.0. 148 items, 180 edges, 267 term rows | REAL | Phase 5 |
| Prompt semver | 1.0.0 in `apps/app_a/prompts/` | REAL | Phase 9 and Phase 12 |
| Freeze | `rows=42 pass=42 fail=0`. Grounded 42 of 42. Citation recall 40 of 41. Citation precision 79 of 79. Abstain 6 of 42 | REAL counts. PRECOMPUTED sentence wording. Floor Unknown | Phase 9 and Phase 12 |
| Parity | 14 rows. matched 12. differing 2. Each difference cites lake items | REAL. No match percent | Phase 11 and Phase 14 |
| Frozen baseline | records 125, open_cases 89, urgent_cases 2, mean_amount 4982.61 SIMULATED, sites 6, hours_per_case 0.603 SIMULATED | REAL for the four integer fields | Phase 0 and Phase 14 |
| Injection | App A and App B quotes-without-id approve return HTTP 409 BLOCK | REAL | Phase 12 |
| Replay files | 77 files besides `README.md` | REAL count on 2026-10-18 | Phase 8, Phase 9, this unit |

Worked example. GQ-19 expected `data.missing.lot_genealogy` and `term.lot_genealogy`. The freeze answer cited `data.missing.lot_genealogy` and abstained. It did not also list `term.lot_genealogy`. That miss is already on the Phase 12 sheet. A later prompt edit that hides that miss would be drift.

---

## What counts as drift

| Change | Why it is drift | First action |
|---|---|---|
| Lake item added, dropped, or restated | Application B reads only the lake | Review loop in FD-22. Raise the version with an ADR |
| Prompt file edited | Freeze sentences are PRECOMPUTED against semver 1.0.0 | Re-run `python apps/app_a/eval/run_freeze.py`. Do not invent a floor |
| Packaged baseline JSON changes | Phase 0 freeze is the compare sheet | Re-run `python -m app.baseline`. Compare the six fields |
| Parity differing rows move | FD-17 requires each false row to list lake item ids | Re-run `python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s` |
| Injection returns HTTP 200 on quotes-plus-approve | Phase 12 closed that path | Stop. Do not treat 200 as a wait. See CON-29-01 |
| Replay file deleted | A demo question then returns `replay_miss` | Keep replay. Add a PRECOMPUTED file only in a later rehearsal. Do not set Azure |

---

## What this framework does not watch as a floor

- Exception cycle time. Value Unknown.
- Aged backlog. Value Unknown.
- API p95. Value Unknown.
- Expert-label percent. Value Unknown.
- ROI dollars. Value Unknown. EDUCATIONAL.

**Verified Fact.** FD-19 and FD-20. Those cells stay Unknown or EDUCATIONAL until a later measured owner names a number. This page does not name one.
