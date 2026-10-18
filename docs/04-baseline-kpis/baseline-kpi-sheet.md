# Baseline KPI sheet

| Field | Value |
|---|---|
| Stage | Phase 0 / 4 Before-AI KPIs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | MEASURED. Unsigned. See `kpi-baseline-signoff.md` |
| Evidence sources | Two runs on 2026-10-18 from `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` using Python 3.13.5. Commands below. `app/baseline.py`; `app/workshop_check.py`; `scripts/verify_preloaded.py` |
| Assumptions | The packaged database is the population. No generator was run |
| Unresolved issues | Headline KPI values that the tools do not emit stay Unknown |
| Residual risks | Copying `Project_Intent.md` section 14.1 without a tool run. This sheet used the tool runs. Those runs happened to match 14.1. The source of truth is the tool output, not the sample paragraph |

Numbers on this page come only from the two tool runs. A cell the tools do not produce is Unknown.

## Command lines

Working directory: `c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE\fabpulse-legacy-workshop-v8-Semiconductor\fabpulse-legacy`.

Interpreter: Python 3.13.5 (`C:\Python313\python.exe`).

The same three commands were run twice.

```text
python scripts/verify_preloaded.py
python -m app.workshop_check
python -m app.baseline
```

### Run 1

| Command | Started UTC | Ended UTC | Exit |
|---|---|---|---|
| `python scripts/verify_preloaded.py` | 2026-10-18T08:28:20.1346937Z | 2026-10-18T08:28:21.1840581Z | 0 |
| `python -m app.workshop_check` | 2026-10-18T08:28:21.2281651Z | 2026-10-18T08:28:22.2771429Z | 0 |
| `python -m app.baseline` | 2026-10-18T08:28:22.2827498Z | 2026-10-18T08:28:23.3214677Z | 0 |

### Run 2

| Command | Started UTC | Ended UTC | Exit |
|---|---|---|---|
| `python scripts/verify_preloaded.py` | 2026-10-18T08:28:23.4203438Z | 2026-10-18T08:28:24.4461726Z | 0 |
| `python -m app.workshop_check` | 2026-10-18T08:28:24.4592021Z | 2026-10-18T08:28:25.5011182Z | 0 |
| `python -m app.baseline` | 2026-10-18T08:28:25.5188205Z | 2026-10-18T08:28:26.5692455Z | 0 |

## `python -m app.baseline` output

Run 1:

```text
{"records": 125, "open_cases": 89, "urgent_cases": 2, "mean_amount": 4982.61, "sites": 6, "hours_per_case": 0.603}
```

Run 2:

```text
{"records": 125, "open_cases": 89, "urgent_cases": 2, "mean_amount": 4982.61, "sites": 6, "hours_per_case": 0.603}
```

Diff: every field matches. No delta.

## `python -m app.workshop_check` output

Both runs:

```text
{"profile": "Semiconductor lot process and excursion review", "counts": {"cases": 125, "events": 145, "source_messages": 15, "partner_feeds": 8567, "reference_versions": 180, "policy_exceptions": 224, "upstream_outages": 72, "batch_runs": 60}, "foreign_key_errors": 0, "integrity": "ok", "ok": true}
```

Diff: match.

## `python scripts/verify_preloaded.py` output

Both runs: `ready: true`, `problems: []`. Integrity ok. Foreign-key errors 0 on every packaged database. Inventory counts matched. Diff: match.

Selected inventory counts (both runs):

| Store / item | Count |
|---|---:|
| cases | 125 |
| events | 145 |
| source_messages | 15 |
| operating_costs | 36 |
| fab_tools | 30 |
| wafer_lots | 125 |
| partner_feeds | 8,567 |
| reference_versions | 180 |
| policy_exceptions | 224 |
| upstream_outages | 72 |
| batch_runs | 60 |
| process_steps | 125 |
| metrology | 125 |
| enterprise operational_objects | 12,500 |
| tiny transactions / events / documents | 2,400 / 9,500 / 360 |
| bundled transactions / events / documents | 50,000 / 100,000 / 600 |
| archive_documents files | 421 |

## Frozen family sheet

| Family | Measure | Run 1 | Run 2 | Diff | Honesty | Label |
|---|---|---|---|---|---|---|
| Business outcome (headline) | Exception cycle time | Unknown | Unknown | n/a | SIMULATED when later modelled | Unknown. `app/baseline.py` has no field |
| Business outcome (headline) | Aged backlog | Unknown | Unknown | n/a | SIMULATED when later modelled | Unknown. No age threshold. Do not treat 89 as aged |
| Business outcome (supporting count) | records | 125 | 125 | Match | REAL | Verified Fact |
| Business outcome (supporting count) | open_cases | 89 | 89 | Match | REAL for `status != CLOSED` | Verified Fact |
| Business outcome (supporting count) | urgent_cases | 2 | 2 | Match | REAL for Python `priority()` | Verified Fact |
| Business outcome (supporting count) | sites | 6 | 6 | Match | REAL | Verified Fact |
| Decision quality | Correct disposition vs expert labels | Unknown | Unknown | n/a | PRECOMPUTED later | Unknown |
| Engineering productivity | Discovery time | Unknown | Unknown | n/a | REAL later | Unknown |
| Engineering productivity | Tests accepted | Unknown | Unknown | n/a | REAL later | Unknown. unittest not run in this unit |
| Performance | API p95, retrieval p95, agent time | Unknown | Unknown | n/a | REAL later | Unknown. Server not started |
| Reliability | Recovery time | Unknown | Unknown | n/a | REAL later | Unknown |
| Reliability | Duplicate / replay rate | Unknown | Unknown | n/a | REAL later | Unknown. Feed count 8,567 is a volume, not a rate |
| Reliability | upstream_outages rows | 72 | 72 | Match | REAL row count | Verified Fact |
| AI quality | Groundedness, citation, abstention | Unknown | Unknown | n/a | REAL later | Unknown. No model call |
| Cost | Tokens | Unknown | Unknown | n/a | REAL later | Unknown |
| Cost | hours_per_case | 0.603 | 0.603 | Match | SIMULATED | Verified Fact of tool output |
| Cost | mean_amount | 4982.61 | 4982.61 | Match | SIMULATED | Verified Fact of tool output |
| ROI | Avoided effort minus cost | Unknown | Unknown | n/a | EDUCATIONAL later | Unknown. No benefit claimed |

## Targets

None. Every target cell is empty on purpose.

## Note on `Project_Intent.md` section 14.1

That paragraph lists 125 records, 89 open cases, 2 urgent cases, mean amount 4,982.61, 6 sites, and 0.603 hours per case. The 2026-10-18 tool runs produced the same figures. This sheet records the tool runs. It does not copy 14.1 in place of a run.
