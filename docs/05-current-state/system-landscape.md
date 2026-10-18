# System landscape

| Field | Value |
|---|---|
| Stage | Phase 1 / 5 Current process and landscape |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | Read-only `PRAGMA` and `SELECT` on both SQLite files on 2026-10-18; `compose.yaml`; `app/server.py`; `services/source_gateway/server.py`; `docs/00-preflight/discovery/system-landscape.md`; `domain-profile.json` |
| Assumptions | Phase 0 landscape remains true. This file adds measured table counts from this unit. |
| Unresolved issues | Docker Compose on this laptop is still Unknown. INC-2025-014 owner is Unknown. |
| Residual risks | `compose.yaml` mounts a named volume for the API database. A Compose start can run against a copy, not the packaged file this unit queried. |

This file names the current systems and stores. It does not pick a target stack.

## Table counts confirmed in this unit

**Verified Fact.** `data/legacy.sqlite3` has 19 tables. Opened with URI `mode=ro` on 2026-10-18.

| Table | Rows | What the table holds |
|---|---:|---|
| `batch_runs` | 60 | Partner batch result, accepted count, rejected count |
| `cases` | 125 | Exception cases with site, region, status, amount |
| `engineering_changes` | 30 | Recipe revision change with approval_state |
| `events` | 145 | Case events with `recorded_at` |
| `fab_tools` | 30 | Tool family, chamber site, `recipe_rev` |
| `gateway_checkpoints` | 0 | Bridge offset. Empty in the packaged file |
| `gateway_inbox` | 1 | One ingested source event, status RECEIVED |
| `metrology` | 125 | Measured value and spec limits |
| `operating_costs` | 36 | Monthly labor hours and case totals |
| `partner_feeds` | 8,567 | Partner rows with source time, ingest time, status |
| `policy_exceptions` | 224 | Policy outcome OPEN, WAIVED, BLOCKED, or REVIEW |
| `process_steps` | 125 | Dispatch step with `recipe_version` |
| `reference_versions` | 180 | Reference rows with `valid_from` and `valid_to` |
| `source_messages` | 15 | Raw JSON messages in arrival order |
| `supplier_parts` | 30 | Vendor part qualification_state |
| `upstream_outages` | 72 | Outage start and optional resolve time |
| `vendor_file_imports` | 1 | One accepted `partner_export.csv` import |
| `vendor_file_rows` | 2,400 | Raw CSV lines, including blank `amount_text` |
| `wafer_lots` | 125 | Lot, tool, yield, engineering_hold |

**Verified Fact.** `data/enterprise_legacy.sqlite3` has 12 tables. Opened with URI `mode=ro` on 2026-10-18.

| Table | Rows | What the table holds |
|---|---:|---|
| `access_audit` | 4,167 | Actor, action, access_reason |
| `cross_references` | 4,166 | Object-to-object link |
| `document_links` | 12,500 | Document kind, language, source name |
| `evidence_events` | 12,500 | Event time, arrival time, payload |
| `financial_adjustments` | 3,125 | Booked amount and entry type |
| `integration_attempts` | 2,500 | Provider call status |
| `operational_objects` | 12,500 | Enterprise case-like object |
| `organizations` | 96 | Tenant, country code, name |
| `policy_register` | 40 | Region policy, active flag, money threshold |
| `retention_events` | 2,084 | Retention class and legal_hold |
| `state_history` | 12,500 | One from_state / to_state row per object |
| `workflow_tasks` | 6,250 | Queue, status, assigned_to, due_at |

## Running HTTP pieces

**Verified Fact.** `app/server.py` listens on host 127.0.0.1 port 8080 by default. Routes: `GET /health`, `GET /`, `GET /api/cases`, `GET /api/cases/{id}`, `GET /api/metrics`, `GET /api/incidents`, `GET /api/partners/{table}`, `GET /api/domain/{table}`. The file has no authentication code.

**Verified Fact.** `services/source_gateway/server.py` listens on port 8090. Routes: `GET /health`, `GET /api/catalog`, `GET /api/events`, `GET /api/record/{id}`, `GET /api/failure` with modes `timeout`, `schema`, and `rate_limit`. The file has no authentication code.

**Verified Fact.** `domain-profile.json` names upstream systems MESDispatch and PLM-Metrology. Event kinds are RECIPE_CHANGE, METROLOGY_RESULT, and YIELD_EXCURSION.

## Side programs that are not HTTP

**Verified Fact.** Four rule programs sit beside the API.

| Program | File | What it does today |
|---|---|---|
| Python priority | `app/legacy_logic.py` | Urgent at CRITICAL or amount above 50,000 |
| JavaScript allow | `legacy_js/legacy_policy.js` | Allows amount up to archive limit times 1.05. Missing match returns 999,999 |
| Java totals | `legacy_java/ReconcileLegacy.java` | Sums CSV amounts as floats. Skips a blank or unreadable cell |
| Night batch | `legacy_batch/shift_reconciliation.py` | Flags HOLD, REVIEW, or value above the joined threshold |

**Verified Fact.** FD-08 DECIDED. Canonical source is `contracts/decision-policies-archive.json` and `policy_register`. The four programs are deviations.

## Other stores

**Verified Fact.** `data/documents/source_documents.jsonl` has 1,200 rows.

**Verified Fact.** `data/archive_documents` has 210 `.eml` files, 210 `.html` files, and `manifest.json`.

**Verified Fact.** Lake tiny tier has 2,400 CSV transactions, 9,500 events, and 360 documents. Lake bundled tier has 50,000 CSV transactions, 100,000 events, and 600 documents. Those counts come from the files on disk in this unit.

## Keys that link the stores

**Verified Fact.** From `PRAGMA table_info` and the create statements in `app/store.py`, `app/domain_data.py`, `app/enterprise_data.py`, and `app/enterprise_legacy.py`.

| From | Key | To | Key |
|---|---|---|---|
| `process_steps` | `lot_id` | `wafer_lots` | `lot_id` |
| `process_steps` | `tool_id` | `fab_tools` | `tool_id` |
| `metrology` | `lot_id` | `wafer_lots` | `lot_id` |
| `wafer_lots` | `tool_id` | `fab_tools` | `tool_id` |
| `events` | `case_id` | `cases` | `id` |
| `operational_objects` | `org_id` | `organizations` | `org_id` |
| Child enterprise tables | `object_id` | `operational_objects` | `object_id` |
| Night batch join | `operational_objects.region` | `policy_register.region` | country code |

**Verified Fact.** `cases.region` uses APAC, EMEA, AMER. `operational_objects.region` uses eight country codes. Those two region columns do not share a stored map.

## Material finding

**Finding.** The current estate is two SQLite files, two HTTP listeners, and four rule programs that read overlapping facts.
**Evidence.** Table counts above. `app/server.py`. `compose.yaml`. The four rule files.
**Impact.** The same lot or case can receive a different priority, open reading, or total from each program.
**Risk.** A later before-versus-after number that mixes those readings will report a false change.
**Confidence.** High.
**Open questions.** Who owns INC-2025-014 remains Unknown.

## What this file does not do

This file records the current systems. It does not add a service.
