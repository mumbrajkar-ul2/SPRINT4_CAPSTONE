# System landscape

| Field | Value |
|---|---|
| Stage | Phase 0 / 0A Pre-flight orientation |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `docs/source-system-landscape.md`; `docs/source-systems-and-constraints.md`; `docs/source-gateway.md`; `docs/service-boundaries.md`; `docs/partner-feed-operations.md`; `docs/archived-enterprise-interfaces.md`; `compose.yaml`; `app/server.py`; `services/source_gateway/server.py`; `domain-profile.json`; `integration/source-gateway.json` |
| Assumptions | The harvested landscape notes describe the packaged simulator, not a live fab. |
| Unresolved issues | No named owner sits on INC-2025-014. Sites still disagree on the word "closed". The company job titles for the SME roles are unconfirmed. |
| Residual risks | The landscape mixes live HTTP services, offline files, and archived jobs. A reader who treats all of them as one running system will miss the write and replay seams. |

This file maps the current systems. It does not recommend a transformation.

## Current running pieces

**Verified Fact.** `compose.yaml` defines three services.

1. `legacy` listens on container port 8080. The host port defaults to 8080. It runs `python -m app.server`.
2. `source-gateway` listens on container port 8090. The host port defaults to 8090. It runs `python -m services.source_gateway.server`.
3. `bridge` waits for both health checks, then runs `python -m app.gateway_bridge --source-url http://source-gateway:8090 --limit 50` once.

**Verified Fact.** `app/server.py` exposes `GET /health`, `GET /`, `GET /api/cases`, `GET /api/cases/{id}`, `GET /api/metrics`, `GET /api/incidents`, `GET /api/partners/{table}`, and `GET /api/domain/{table}`. There is no authentication code in that file.

**Verified Fact.** `docs/source-gateway.md` and `services/source_gateway/server.py` expose `GET /health`, `GET /api/catalog`, `GET /api/events`, `GET /api/record/{id}`, and `GET /api/failure` with modes `timeout`, `schema`, and `rate_limit`.

**Verified Fact.** Ports 8091 and 8092 are not present in `compose.yaml` or the inherited HTTP code. Those ports are locked later-phase values in `Execution_Plan.md` section 4. They are not current-state listeners.

## Upstream and domain sources

**Verified Fact.** `domain-profile.json` names two upstream systems: MESDispatch and PLM-Metrology. Event kinds are RECIPE_CHANGE, METROLOGY_RESULT, and YIELD_EXCURSION. Process areas are ETCH, LITHO, DEPOSITION, and CMP. Human queue states are QUEUED, PROCESSING, HOLD, ENGINEERING_REVIEW, and RELEASED.

**Verified Fact.** `docs/source-systems-and-constraints.md` says source timestamps, ingestion timestamps, and revision dates are separate fields.

**Verified Fact.** `integration/source-gateway.json` points the gateway at `wafer_lots.lot_id` and `process_steps`. Gateway sources are `mes`, `equipment`, and `metrology`.

## Stores and archives

**Verified Fact.** `docs/source-system-landscape.md` names five data patterns: the SQLite transactional application, the source partner gateway, domain relational tables, a document archive, and a monthly operating-cost table.

**Verified Fact.** `scripts/verify_preloaded.py` found these packaged stores:

- `data/legacy.sqlite3` — 19 tables, integrity ok, 0 foreign-key errors.
- `data/enterprise_legacy.sqlite3` — 12 tables, 12,500 operational objects, integrity ok.
- `data/lake/tiny/` and `data/lake/bundled/` — reference and finance SQLite files plus events and documents.
- `data/documents/` — 1 file.
- `data/archive_documents/` — 421 files.

**Verified Fact.** `docs/archived-enterprise-interfaces.md` says `legacy_batch/` reads `data/enterprise_legacy.sqlite3` directly. That job predates the HTTP bridge.

## Other executables

**Verified Fact.** Three more rule paths sit beside the Python API.

- `legacy_batch/shift_reconciliation.py` treats REVIEW as open when it flags rows.
- `legacy_java/ReconcileLegacy.java` sums CSV amounts as floats and skips blank or unparsable rows.
- `legacy_js/legacy_policy.js` reads `contracts/decision-policies-archive.json` and allows an amount up to the regional limit times 1.05. A missing year or region returns 999,999.

**Verified Fact.** `app/legacy_logic.py` sets urgent when severity is CRITICAL or amount is above 50,000. A CLOSED case is archive priority.

## Material finding

**Finding.** The current estate is several local programs that read overlapping facts and apply different rules.
**Evidence.** `docs/service-boundaries.md`, `app/legacy_logic.py`, `legacy_js/legacy_policy.js`, `legacy_batch/shift_reconciliation.py`, `legacy_java/ReconcileLegacy.java`, `compose.yaml`.
**Impact.** The same case can get a different priority or open-or-closed reading from each program.
**Risk.** A later comparison that mixes those readings will report a false change.
**Confidence.** High.
**Open questions.** Who owns a disputed incident after INC-2025-014 remains Unknown.

## What this file does not do

This file names the current systems and ports. It does not propose a new system.
