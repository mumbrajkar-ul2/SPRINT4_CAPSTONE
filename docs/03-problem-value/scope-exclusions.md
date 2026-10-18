# Scope exclusions

| Field | Value |
|---|---|
| Stage | Phase 0 / 3 Frame problem and value |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `docs/00-preflight/operating-contract/scope-boundaries.md`; FD-01; FD-02; `PRELOADED_DATA.md`; `Execution_Plan.md` unresolved issues; `Project_Intent.md` section 14.1 |
| Assumptions | The 0B scope file remains the governing list. This page restates it for the problem stage |
| Unresolved issues | BO-04 can narrow the demo later. That is not an exclusion invented here |
| Residual risks | A later feature that is interesting but outside BP1 to BP8 can grow the work |

## In scope (restated)

The inherited Fabpulse simulator. The eight defects BP1 to BP8. The eight KPI families. Two later applications that run the same workflow. Local synthetic data.

## Excluded

| Exclusion | Why | Label |
|---|---|---|
| Any other repository | FD-01 | Verified Fact |
| Real production fab control | `README.md` boundary. Educational simulator | Verified Fact |
| Real personal or customer data | FD-02. `PRELOADED_DATA.md` | Verified Fact |
| Write tools for the model | FD-02 | Verified Fact |
| Application behaviour change in Phases 0 to 6 | `Execution_Plan.md` section 11 | Verified Fact |
| Invented KPI targets or dollar benefits | `Project_Intent.md` 14.1. BO-02. BO-11 | Verified Fact |
| Packaged-data reset in this phase | Write-boundary file | Verified Fact |
| Workshop 500k and stress 2M lake tiers | Not packaged. `PRELOADED_DATA.md` | Verified Fact |
| Official Birlasoft brand files | Not in hand | Verified Fact |
| A signed charter or signed KPI sheet in this unit | BO-01 and BO-02 stay unsigned | Verified Fact |
| Autonomous record writes | BO-03 working answer | Verified Fact |
| Merging operational, finance, and audit closed | BO-06b working answer keeps them separate | Verified Fact |
| The 999,999 JavaScript default as a live policy number | BO-08 working answer | Verified Fact |

## Not excluded, only later

Identity, Compose on this laptop, lake ports 8091 and 8092, agents, and Application B. Those are later phases. They are not Phase 0 work. They are not out of the whole engagement.
