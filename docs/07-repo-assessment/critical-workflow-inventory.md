# Critical workflow inventory

| Field | Value |
|---|---|
| Stage | Phase 1 / 7 Deep repo assessment |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `app/server.py`; `app/partner_feeds.py`; `app/gateway_bridge.py`; `app/baseline.py`; `legacy_batch/shift_reconciliation.py`; `legacy_js/legacy_policy.js`; `legacy_java/ReconcileLegacy.java`; `app/operational_report.py`; `sql/legacy_reports.sql` |
| Assumptions | A critical workflow is a path that operators or month-end staff already use, or a path that BP1 to BP8 already touch. |
| Unresolved issues | Time to finish each workflow is Unknown. |
| Residual risks | Changing any of these paths before a characterization test will hide the baseline. |

This file names the current critical workflows. It does not rewrite them.

## Inventory

| ID | Workflow | Entry | What it does today | Data it reads or writes | Linked BP | Current test cover |
|---|---|---|---|---|---|---|
| CW-01 | Case list and priority | `GET /api/cases` | Returns case rows. Adds `priority()` to each row | Reads `cases`. No write | BP4, BP5 | `test_workflow.py` checks priority on two synthetic inputs. It does not call the HTTP route |
| CW-02 | Case detail and review flag | `GET /api/cases/{id}` | Returns one case, its events, and `manual_review_required` | Reads `cases`, `events` | BP3, BP5 | No HTTP test |
| CW-03 | Metrics and monthly cost | `GET /api/metrics` | Case total, status counts, `operating_costs` | Reads `cases`, `operating_costs` | BP5 | No HTTP test |
| CW-04 | Incident list | `GET /api/incidents` | Returns a hard-coded INC-2019-0082 row | No table | BP8 | No test. INC-2025-014 is absent |
| CW-05 | Partner resource read | `GET /api/partners/{table}` | Reads partner_feeds, reference_versions, policy_exceptions, upstream_outages, batch_runs | Read. `init()` can CREATE TABLE IF NOT EXISTS | BP2, BP3, BP6 | Table-name test only |
| CW-06 | Domain resource read | `GET /api/domain/{table}` | Reads process_steps, metrology, engineering_changes, supplier_parts | Read | BP1 | `test_enterprise.py` checks row presence |
| CW-07 | Partner feed reconcile | `python -m app.partner_feeds --reconcile` | Writes ACCEPTED, REJECTED, or DUPLICATE | Writes `partner_feeds` | BP2, BP7 | No reconcile test |
| CW-08 | Source gateway publish | `GET /api/events` on port 8090 | Builds events from `wafer_lots` with `occurred_at` and `published_at` | Reads `wafer_lots` ro | BP3 | No gateway HTTP test |
| CW-09 | Bridge ingest | `python -m app.gateway_bridge` | Inserts `gateway_inbox`. Records offset | Writes inbox and checkpoints | BP2, BP3, BP8 | `test_source_gateway.py` apply duplicate and invalid. Writes default DB |
| CW-10 | Source message consume | `app/integration.py` | Reads `source_messages` by `received_at` | Read | BP3 | `test_workflow.py` checks a list is returned |
| CW-11 | Night batch flag | `legacy_batch/shift_reconciliation.py` | Flags HOLD, REVIEW, or over threshold | Reads enterprise DB | BP4, BP5, BP6 | `test_enterprise_legacy_v6.py` checks processed=80 on a 120-row temp DB |
| CW-12 | JavaScript allow | `legacy_js/legacy_policy.js` | Compares amount to archive limit times 1.05 | Reads the JSON archive | BP4, BP6 | No test |
| CW-13 | Java month-end total | `ReconcileLegacy.java` | Sums CSV amounts as floats. Skips blanks | Reads a CSV | BP4 | No test |
| CW-14 | Baseline snapshot | `python -m app.baseline` | Emits records, open_cases, urgent_cases, mean_amount, sites, hours_per_case | Reads `cases`, `operating_costs` | BP5 | `test_workflow.py` checks records=125 on a temp DB |
| CW-15 | Recipe join | Ad-hoc SQL or domain reads | `process_steps` joined to `fab_tools` on `tool_id` | Read | BP1 | No test asserts 91 mismatches |
| CW-16 | Operational parent-child report | `python -m app.operational_report` | Counts wafer_lots and process_steps and the join | Read | BP1 | `test_source_gateway.py` checks counts > 0 |
| CW-17 | Untuned region report | `sql/legacy_reports.sql` | Counts cases by region and status. Sums amount | Read | BP5, BP6 | No test |
| CW-18 | Vendor CSV import | `app/historical_estate.py` | Inserts raw amount_text | Writes vendor tables | BP4 | No test on the packaged 10 blanks |
| CW-19 | Outage recovery | Incident file plus spreadsheet | INC-2025-014 path | No table for this incident | BP8 | No test. Owner Unknown |

## Workflows that change packaged rows

**Verified Fact.** CW-07, CW-09, CW-18, and any generate reset write the operational store.

**Verified Fact.** CW-01 through CW-06 GET routes read. `partner_feeds.init()` and `store.setup()` can CREATE TABLE IF NOT EXISTS.

## What this file does not do

This file names the paths. It does not add a route.
