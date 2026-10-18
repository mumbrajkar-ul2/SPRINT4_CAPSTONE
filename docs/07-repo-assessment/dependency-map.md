# Dependency map

| Field | Value |
|---|---|
| Stage | Phase 1 / 7 Deep repo assessment |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `pyproject.toml`; `app/store.py`; `app/server.py`; `app/partner_feeds.py`; `app/gateway_bridge.py`; `legacy_js/legacy_policy.js`; `legacy_batch/shift_reconciliation.py`; `compose.yaml`; `integration/source-gateway.json` |
| Assumptions | Optional Java and Node runtimes are used only when a person runs those two programs. |
| Unresolved issues | Whether Java or Node is installed on this laptop is Unknown. |
| Residual risks | Setting `LEGACY_DB` to the packaged path lets any writer in this map change the freeze. |

This file maps what talks to what. It does not add a package.

## External runtimes

| Runtime | Used by | Required for the Python API | Label |
|---|---|---|---|
| Python 3.10+ standard library | API, tests, scripts, night batch | Yes | Verified Fact |
| SQLite | `app/store.py`, night batch, lake reference and finance files | Yes | Verified Fact |
| Node / JavaScript | `legacy_js/legacy_policy.js` | No | Verified Fact |
| Java | `legacy_java/ReconcileLegacy.java` | No | Verified Fact |
| Docker / Compose | `compose.yaml` three services | No for laptop Python start | Verified Fact |

**Verified Fact.** `pyproject.toml` lists no FastAPI, React, LangGraph, or OPA package. Those names are later-phase choices in `Execution_Plan.md`.

## Internal module edges

```text
app/server.py
  -> app/store.connect  -> data/legacy.sqlite3
  -> app/legacy_logic.priority
  -> app/legacy_logic.manual_review_required
  -> app/partner_feeds.init  (creates partner tables if missing)
  -> app/enterprise_data.TABLES  (domain route allow-list)
  -> domain.json

app/partner_feeds.py
  -> app/store
  -> domain-profile.json
  -> partner_feeds, reference_versions, policy_exceptions, upstream_outages, batch_runs

app/gateway_bridge.py
  -> app/store
  -> integration/source-gateway.json
  -> HTTP GET source-gateway /api/events
  -> gateway_inbox, gateway_checkpoints

app/integration.py
  -> source_messages

app/baseline.py
  -> cases, operating_costs
  -> app/legacy_logic.priority

legacy_batch/shift_reconciliation.py
  -> data/enterprise_legacy.sqlite3
  -> operational_objects LEFT JOIN policy_register

legacy_js/legacy_policy.js
  -> contracts/decision-policies-archive.json

legacy_java/ReconcileLegacy.java
  -> a CSV path passed on the command line
  -> vendor-style columns tenant, kind, amount at index 4

services/source_gateway/server.py
  -> integration/source-gateway.json
  -> wafer_lots in mode=ro
```

**Verified Fact.** Those edges come from the import lines and SQL strings in the files.

## Data-key edges

| From | Column | To | Column | Label |
|---|---|---|---|---|
| `events` | `case_id` | `cases` | `id` | Verified Fact |
| `process_steps` | `lot_id` | `wafer_lots` | `lot_id` | Verified Fact |
| `process_steps` | `tool_id` | `fab_tools` | `tool_id` | Verified Fact |
| `metrology` | `lot_id` | `wafer_lots` | `lot_id` | Verified Fact |
| `wafer_lots` | `tool_id` | `fab_tools` | `tool_id` | Verified Fact |
| enterprise children | `object_id` | `operational_objects` | `object_id` | Verified Fact |
| `operational_objects` | `org_id` | `organizations` | `org_id` | Verified Fact |
| night batch | `region` | `policy_register.region` | country code | Verified Fact |

**Verified Fact.** There is no stored edge from `cases.region` (APAC) to `operational_objects.region` (IN). There is no stored edge from `cases.id` to `operational_objects.object_id`.

## Write-capable edges

| Writer | Target | When it writes | Label |
|---|---|---|---|
| `partner_feeds.reconcile()` | `partner_feeds.processing_status` | When someone runs reconcile | Verified Fact |
| `gateway_bridge.apply()` | `gateway_inbox` | When the bridge or `test_source_gateway` runs | Verified Fact |
| `gateway_bridge.pull()` | `gateway_checkpoints` | After an HTTP pull | Verified Fact |
| `historical_estate.import_csv()` | vendor tables | When a CSV is imported | Verified Fact |
| `generate --reset` | cases and domain tables | When someone passes `--reset` | Verified Fact |
| Compose bridge | named volume copy of the DB | When Compose starts | Verified Fact |

**Verified Fact.** `app/server.py` `do_GET` reads. It does not UPDATE cases.

## What this file does not do

This file records current edges. It does not add a new one.
