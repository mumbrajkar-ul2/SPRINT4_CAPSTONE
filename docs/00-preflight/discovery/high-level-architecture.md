# High-level architecture

| Field | Value |
|---|---|
| Stage | Phase 0 / 0A Pre-flight orientation |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `app/server.py`; `app/store.py`; `app/partner_feeds.py`; `app/legacy_logic.py`; `services/source_gateway/server.py`; `app/gateway_bridge.py` (name and compose command only); `compose.yaml`; `legacy_batch/shift_reconciliation.py`; `docs/source-gateway.md`; `docs/service-boundaries.md`; `Project_Intent.md` section 4.1 |
| Assumptions | The packaged diagrams in harvested notes match the code that is in the tree. |
| Unresolved issues | The follow-up owner for INC-2025-014 is Unknown. |
| Residual risks | The one-shot Compose bridge writes ingestion rows. A person who starts Compose on the working tree changes operational state. |

This file describes the current architecture. It does not recommend a target architecture.

## Current logical flow

**Verified Fact.** `Project_Intent.md` section 4.1 and the inherited docs describe this path:

MESDispatch / PLM-Metrology / partner files → source gateway or local staging → ingestion and reconciliation → SQLite cases and semiconductor domain records → synchronous API and operational reports → manual review and month-end reconciliation.

**Verified Fact.** `docs/business-context.md` lists the same five human steps: external messages, integration, operations review, local decisions, monthly measures.

## Current components

```text
MESDispatch, PLM-Metrology, partner files
        |
        v
source gateway HTTP  :8090
        |
        v
gateway_bridge (one-shot; writes inbox and checkpoints)
        |
        v
legacy.sqlite3 (19 tables)
        |
        +--> legacy API HTTP  :8080  (cases, metrics, partners, domain)
        +--> partner_feeds staging and reconcile (mutates status)
        +--> app.legacy_logic priority and review rules
        |
enterprise_legacy.sqlite3 (12 tables)
        |
        +--> night batch shift_reconciliation.py
        +--> Java ReconcileLegacy (CSV totals)
        +--> JavaScript legacy_policy.js (limit * 1.05)
```

**Verified Fact.** Default ports in `environments/dev.env.example` and `compose.yaml` are 8080 for the legacy API and 8090 for the source gateway.

**Verified Fact.** `app/store.py` opens `data/legacy.sqlite3` unless `LEGACY_DB` is set. It turns on foreign keys and a 15-second busy timeout.

**Verified Fact.** `app/legacy_logic.py` decides priority in the API process. CLOSED maps to archive. CRITICAL or amount above 50,000 maps to urgent. HIGH or ESCALATED maps to review. Everything else maps to queue. HIGH, CRITICAL, ESCALATED, or REOPENED requires manual review.

## Write seams

**Verified Fact.** `PRELOADED_DATA.md` says `app.gateway_bridge` writes operational ingestion state.

**Verified Fact.** `app/partner_feeds.py` `reconcile()` updates `partner_feeds.processing_status` in place.

**Verified Fact.** `app/server.py` `do_GET` only reads cases, metrics, partners, and domain tables. The runbook says the API process does not mutate core records. Partner `init()` only creates tables if they are missing.

**Verified Fact.** This Phase 0 unit did not start the server, the gateway, or the bridge. It did not run reconcile or generate.

## What is not in the current architecture

**Verified Fact.** There is no identity check on the HTTP routes in `app/server.py`.

**Verified Fact.** There is no Context Lake service, no lake REST port 8091, and no lake MCP port 8092 in the inherited Compose file. Those ports are later-phase locked values in `Execution_Plan.md` section 4.

**Verified Fact.** There is no agent runtime and no approval-gate service in this tree.

## Material finding

**Finding.** The current architecture is one SQLite operational store, one HTTP API on 8080, one upstream simulator on 8090, a write-capable bridge, and three side programs that apply their own rules.
**Evidence.** `compose.yaml`, `app/server.py`, `services/source_gateway/server.py`, `legacy_batch/shift_reconciliation.py`, `legacy_java/ReconcileLegacy.java`, `legacy_js/legacy_policy.js`.
**Impact.** Orientation can name the live pieces and the write seams before any change.
**Risk.** Starting Compose on this working copy runs the bridge and writes inbox rows.
**Confidence.** High.
**Open questions.** None for the current component list.

## What this file does not do

This file records the current arrangement. It does not pick Application A, Application B, or a lake design.
