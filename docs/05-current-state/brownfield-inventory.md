# Brownfield inventory

| Field | Value |
|---|---|
| Stage | Phase 1 / 5 Current process and landscape |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | Inherited tree under `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`; read-only SQLite on 2026-10-18; `docs/00-preflight/discovery/repository-overview.md`; test modules in `tests/` |
| Assumptions | Phase 0 file walk of 1,590 hashed files remains the tree inventory. This unit did not re-hash the tree. |
| Unresolved issues | Live unittest count on 2026-10-18 is Unknown. This unit did not run tests, because one test writes the packaged database. |
| Residual risks | `python -m app.generate --reset` replaces packaged rows. The GitHub verify workflow includes that command. |

This file lists what is already in the inherited tree. It does not change a file under `fabpulse-legacy`.

## Application code

**Verified Fact.** `app/` holds the HTTP server, SQLite helper, generators, reports, and rule module.

| File | Role |
|---|---|
| `app/server.py` | GET API on port 8080. No auth |
| `app/store.py` | Opens `data/legacy.sqlite3` unless `LEGACY_DB` is set |
| `app/legacy_logic.py` | Priority and manual-review functions |
| `app/partner_feeds.py` | Feed tables, generate, reconcile |
| `app/integration.py` | Reads `source_messages` |
| `app/gateway_bridge.py` | Writes inbox and checkpoints |
| `app/baseline.py` | Records, open_cases, urgent_cases, mean_amount, sites, hours_per_case |
| `app/workshop_check.py` | Offline table counts and integrity |
| `app/operational_report.py` | Parent and child join counts |
| `app/generate.py` | Builds cases, events, messages, then domain tables |
| `app/domain_data.py` | Builds `fab_tools` and `wafer_lots` |
| `app/enterprise_data.py` | Builds process_steps, metrology, engineering_changes, supplier_parts |
| `app/enterprise_legacy.py` | Builds `data/enterprise_legacy.sqlite3` |
| `app/generate_documents.py` | Writes `data/documents/source_documents.jsonl` |
| `app/archived_documents.py` | Writes archive `.eml` and `.html` |
| `app/historical_fixture.py` | Writes lake tiny and bundled tiers |
| `app/historical_estate.py` | Imports a vendor CSV into SQLite |

## Four rule sources

**Verified Fact.** Locked list.

1. Python `app/legacy_logic.py`
2. JavaScript `legacy_js/legacy_policy.js`
3. Java `legacy_java/ReconcileLegacy.java`
4. Night batch `legacy_batch/shift_reconciliation.py`

**Verified Fact.** Canonical archive: `contracts/decision-policies-archive.json`. 15 historical versions. Regions APAC, EMEA, AMER. Years 2022 through 2026. 2026 APAC limit 25,000. 2026 EMEA limit 26,100. 2026 AMER limit 27,200.

## Tests

**Verified Fact.** Seven test modules exist.

| Module | What it checks | What it does not check |
|---|---|---|
| `tests/test_workflow.py` | 125 cases on a temp DB. Baseline records. CLOSED -> archive. CRITICAL -> urgent. Feed parser returns a list | Recipe mismatch. REPLAY. Auth. Time fields |
| `tests/test_domain.py` | 30 tools and 180 lots on a temp DB. Foreign keys | `recipe_version` versus `recipe_rev` |
| `tests/test_enterprise.py` | Domain tables have rows. Foreign keys | Open or closed meaning |
| `tests/test_partner_feeds.py` | Profile lists and table names | Generate, REPLAY, or reconcile |
| `tests/test_historical_fixture.py` | Tiny lake counts in a temp folder | Untrusted `source_claim` text |
| `tests/test_enterprise_legacy_v6.py` | 120-row generate and night batch processed=80 | REVIEW meaning versus BO-06a |
| `tests/test_source_gateway.py` | Operational report counts. Bridge duplicate and invalid | Uses default `LEGACY_DB`. Can write packaged `gateway_inbox` |

**Unknown.** How many tests pass on 2026-10-18. This unit did not run `unittest`.

## Data stores

**Verified Fact.** Two operational SQLite files: 19 tables and 12 tables. Counts in `system-landscape.md`.

**Verified Fact.** Lake tiny and bundled tiers are on disk. Workshop 500k and stress 2M tiers are not in this archive (`PRELOADED_DATA.md`, Phase 0).

**Verified Fact.** `data/documents/source_documents.jsonl` has 1,200 documents. 22 bodies contain ignore-or-release instruction text.

**Verified Fact.** Archive folder has 3 `.eml` files whose text contains approve-or-ignore instruction language.

## Contracts and integration files

**Verified Fact.**

- `contracts/decision-policies-archive.json`
- `integration/source-gateway.json`
- `integration/source-contract-v1.json`
- `domain-profile.json`
- `domain.json`
- `sql/legacy_reports.sql`

## Operations files

**Verified Fact.**

- `operations/runbook.md`
- `operations/baseline-evidence.md`
- `operations/incidents/INC-2025-014.md` — follow-up owner unknown

## Scripts and packaging

**Verified Fact.** `scripts/verify_preloaded.py`, `scripts/offline_inventory.py`, `scripts/smoke.py`, `scripts/rehearse_local.py`. `compose.yaml`. `Dockerfile`. `.github/workflows/verify.yml`.

## Headline KPI columns checked

**Verified Fact.** `cases` columns are `id`, `account_id`, `segment`, `site`, `region`, `created_at`, `status`, `severity`, `amount`, `note`, `version`. There is no `closed_at`, `resolved_at`, or `disposition_at`.

**Verified Fact.** `events` columns are `id`, `case_id`, `recorded_at`, `event_type`, `payload`. Event types are CASE_CREATED (125) and STATUS_REVIEWED (20). STATUS_REVIEWED is not a final close for every case.

**Verified Fact.** `state_history` has one row per object. It does not store a start-to-close pair for a cycle-time formula.

**Unknown.** Exception cycle time. The columns above do not support a close-time measure on `cases`.

**Unknown.** Aged backlog. `cases.created_at` exists. No age cutoff exists in `policy_register` or `decision-policies-archive.json`. A cutoff is not invented here.

## Material finding

**Finding.** The brownfield is a small Python API, four disagreeing rule programs, two SQLite estates, and a large packaged archive.
**Evidence.** File list and table counts in this unit. Phase 0 tree walk of 1,590 files.
**Impact.** Discovery can catalogue defects from packaged rows without generating data.
**Risk.** A generate reset or a write-capable test changes the freeze.
**Confidence.** High.
**Open questions.** Live test count remains Unknown because tests were not run.

## What this file does not do

This file lists current assets. It does not add a test or a table.
