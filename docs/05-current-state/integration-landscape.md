# Integration landscape

| Field | Value |
|---|---|
| Stage | Phase 1 / 5 Current process and landscape |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `app/partner_feeds.py`; `app/gateway_bridge.py`; `app/integration.py`; `app/historical_estate.py`; `services/source_gateway/server.py`; `integration/source-gateway.json`; `integration/source-contract-v1.json`; `legacy_batch/shift_reconciliation.py`; read-only queries on 2026-10-18 |
| Assumptions | Packaged rows show current integration state. This unit did not start the gateway or the bridge. |
| Unresolved issues | Whether Compose runs on this laptop is Unknown. INC-2025-014 owner is Unknown. |
| Residual risks | `tests/test_source_gateway.py` calls `gateway_bridge.apply()` through the default `LEGACY_DB`. A test run can write `gateway_inbox` on the packaged file. |

This file names how data enters the current stores. It does not propose a new interface.

## Inbound paths

| Path | Code | Write target | Auth | Label |
|---|---|---|---|---|
| Source gateway HTTP | `services/source_gateway/server.py` | None. Reads `wafer_lots` in `mode=ro` and returns JSON | None in the file | Verified Fact |
| Gateway bridge | `app/gateway_bridge.py` `apply()` and `pull()` | `gateway_inbox`, `gateway_checkpoints` | None | Verified Fact |
| Partner feed generate and reconcile | `app/partner_feeds.py` | `partner_feeds` status in place | None | Verified Fact |
| Source message consume | `app/integration.py` | None. Reads `source_messages` in arrival order | None | Verified Fact |
| Vendor CSV import | `app/historical_estate.py` `import_csv()` | `vendor_file_imports`, `vendor_file_rows` | None | Verified Fact |
| Night batch | `legacy_batch/shift_reconciliation.py` | None. Reads `enterprise_legacy.sqlite3` | None | Verified Fact |

**Verified Fact.** `integration/source-gateway.json` points the gateway at parent table `wafer_lots` key `lot_id` and child table `process_steps` key `lot_id`. Sources are `mes`, `equipment`, and `metrology`. Event types are `lot_started`, `process_step`, `metrology_review`, and `engineering_hold`.

## What each path does with time

**Verified Fact.** The source gateway returns both `occurred_at` and `published_at`. The published clock is two hours and 15 minutes later in the generator loop.

**Verified Fact.** `gateway_bridge.apply()` stores `occurred_at` as `event_time` and writes `received_at` as the local clock at insert.

**Verified Fact.** `partner_feeds` stores `source_ts` and `ingest_ts`. Query on 2026-10-18: 2,110 rows have ingest before source. 5,361 rows have ingest after source. 1,096 rows match.

**Verified Fact.** `evidence_events` stores `event_time` and `arrival_time`. Query on 2026-10-18: 11,985 of 12,500 rows differ.

## Replay and retry

**Verified Fact.** `app/partner_feeds.py` inserts a `REPLAY-` row when the generator index is a multiple of 127. Packaged count: 67 rows with `processing_status = 'REPLAY'` and `feed_id` starting `REPLAY-`.

**Verified Fact.** `reconcile()` sets a REPLAY row to `DUPLICATE` with reason `replayed source message`. This unit did not run `reconcile()`. The 67 rows remain REPLAY.

**Verified Fact.** `docs/historic-decisions.md` records a 2025 rollback after a replayed partner delivery inflated the exception queue.

**Verified Fact.** `gateway_bridge.apply()` treats a repeated `message_id` as a duplicate through a primary-key error. Packaged `gateway_inbox` has 1 row with `message_id = 'CHECK-semiconductor_lot'`.

## Schema and failure modes already in the code

**Verified Fact.** Partner schema values in `partner_feeds.schema_rev` include `1.0`, `1.1`, `2.0`, and `unsupported`. `reconcile()` rejects `unsupported`.

**Verified Fact.** `GET /api/failure?mode=timeout` returns HTTP 503. `mode=schema` returns `unexpected_schema: v3`. `mode=rate_limit` returns HTTP 429.

**Verified Fact.** `integration_attempts` has 2,500 rows. Status counts: SUCCESS 625, FAILED 625, TIMEOUT 625, RETRY 625.

**Verified Fact.** `batch_runs` has 60 rows: SUCCESS 22, PARTIAL 21, FAILED 17.

**Verified Fact.** `upstream_outages` has 72 rows. 8 have `resolved` empty.

## Night batch join

**Verified Fact.** `shift_reconciliation.py` joins every `operational_objects` row to every active `policy_register` row on the same country code. Default `LIMIT 500` applies to the joined rows, not to distinct objects.

Worked example. Region US has 5 active policies. One US object becomes 5 joined rows. The job can count the same object more than once before the limit is reached.

**Verified Fact.** A full join with no limit produced 23,168 flagged joined rows and 6,279 distinct flagged objects. Those two numbers differ because of the 4-to-5 active policies per region.

## What is not on the wire

**Verified Fact.** `app/server.py` and the source gateway accept GET with no identity header.

**Verified Fact.** There is no retry queue table for INC-2025-014. The incident file says staff used a spreadsheet.

**Verified Fact.** Ports 8091 and 8092 are later-phase lake ports in `Execution_Plan.md`. They are not listeners in `compose.yaml`.

## Material finding

**Finding.** Integration is several local writers and readers. Replay, late clocks, and schema variants are already in the packaged rows.
**Evidence.** 67 REPLAY feeds. 7,471 partner rows with ingest time different from source time. 11,985 evidence rows with arrival different from event time. 1,875 integration attempts that are not SUCCESS.
**Impact.** A later app that treats arrival time as event time, or treats a REPLAY as a new case, will grow the queue.
**Risk.** Starting Compose or running `test_source_gateway.py` writes inbox rows on the working database.
**Confidence.** High.
**Open questions.** INC-2025-014 owner remains Unknown.

## What this file does not do

This file records the current inbound paths. It does not add authentication.
