# Baseline behaviour

| Field | Value |
|---|---|
| Stage | Phase 1 / 7 Deep repo assessment |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `app/legacy_logic.py`; `app/partner_feeds.py`; `app/server.py`; `app/baseline.py`; `legacy_batch/shift_reconciliation.py`; `legacy_js/legacy_policy.js`; `legacy_java/ReconcileLegacy.java`; `app/gateway_bridge.py`; Phase 0 baseline tool output; read-only counts on 2026-10-18 |
| Assumptions | Behaviour here is what the current code does on the packaged rows. Optional Java and Node programs were read, not executed. |
| Unresolved issues | HTTP latency is Unknown. The server was not started. Live unittest count is Unknown. |
| Residual risks | Running reconcile, the bridge, or generate reset will change these observed row states. |

This file records what the current programs do. It does not change that behaviour.

## Packaged population the behaviour sees

**Verified Fact.** Phase 0 `python -m app.baseline` twice: `records` 125, `open_cases` 89, `urgent_cases` 2, `mean_amount` 4982.61, `sites` 6, `hours_per_case` 0.603.

**Verified Fact.** This unit's read-only queries match those case counts: 125 cases, 89 with `status != 'CLOSED'`, 2 CRITICAL, 0 with `amount > 50000`.

Honesty labels stay as Phase 0 wrote them. The two headline KPIs stay Unknown.

## Python priority and review

**Verified Fact.** `priority(status, severity, amount)`:

| Input | Output |
|---|---|
| status CLOSED | archive |
| severity CRITICAL, status not CLOSED | urgent |
| amount above 50,000, status not CLOSED | urgent |
| severity HIGH or status ESCALATED | review |
| any other row | queue |

Worked example on this set. The two urgent cases are the two CRITICAL rows. Amount never crosses 50,000.

**Verified Fact.** `manual_review_required` is true when severity is HIGH or CRITICAL, or status is ESCALATED or REOPENED.

## HTTP GET behaviour

**Verified Fact.** `GET /api/cases` adds a `priority` field from the Python function. It does not check an identity header.

**Verified Fact.** `GET /api/cases/{id}` adds `events` ordered by `recorded_at` and `manual_review_required`. It returns 404 when the id is missing.

**Verified Fact.** `GET /api/incidents` always returns INC-2019-0082 with state `investigating`. It does not read INC-2025-014.

**Verified Fact.** `GET /api/partners/{table}` and `GET /api/domain/{table}` reject a name outside the allow-list with 404.

**Verified Fact.** Pagination on those list routes clamps `limit` to 1..100.

## Partner feed behaviour

**Verified Fact.** `reconcile()` on a row in NEW, RETRY, or REPLAY:

| Condition | New status | Reason |
|---|---|---|
| Missing `business_key` or `schema_rev` is unsupported | REJECTED | schema/key validation |
| Current status is REPLAY | DUPLICATE | replayed source message |
| Quantity is below 0 | REJECTED | quantity out of range |
| Else | ACCEPTED | none |

**Verified Fact.** Packaged rows are still NEW 8,000, RETRY 500, REPLAY 67. Reconcile has not been applied to this file in this unit.

## Bridge behaviour

**Verified Fact.** `apply()` rejects a payload that lacks `message_id`, `business_key`, `system`, `event_type`, or `occurred_at`. It rejects a `business_key` that is not a `wafer_lots.lot_id`. A repeated `message_id` is a duplicate.

**Verified Fact.** Packaged `gateway_inbox` has 1 row, `CHECK-semiconductor_lot`, status RECEIVED.

## Night batch behaviour

**Verified Fact.** The job reads `operational_objects` left-joined to active `policy_register` rows on `region`. It flags a joined row when status is HOLD or REVIEW, or when `value` is above `threshold`.

**Verified Fact.** Default `limit=500` is applied to the joined result. REVIEW objects in the full table: 2,090. HOLD objects: 2,083.

## JavaScript allow behaviour

**Verified Fact.** `threshold(region, year)` returns the archive `limit` for the first `historical_versions` row whose region matches and whose `effective_from` starts with that year. Otherwise it returns 999,999.

**Verified Fact.** `legacyAllows(amount, region, year)` is true when `Number(amount) <= threshold * 1.05`.

Worked example from the file's own main block. Region APAC, year 2026, archive limit 25,000. The allow line is 26,250. The file prints `legacyAllows(27000,'APAC',2026)`, which is false on that arithmetic. This unit did not execute Node.

## Java total behaviour

**Verified Fact.** The program skips a header that starts `tenant,`. It splits on comma. It needs at least 6 fields. It adds `Double.parseDouble` of field index 4. A `NumberFormatException` is ignored. Count and total are printed.

**Verified Fact.** 10 packaged `vendor_file_rows` have blank `amount_text`. Those rows match the skip path if that column is fed as field 4.

## What the current tools do not do

**Verified Fact.** `app/baseline.py` does not emit exception cycle time.

**Verified Fact.** `app/baseline.py` does not emit aged backlog.

**Verified Fact.** No current route returns `source_ts` and `ingest_ts` as a required pair.

**Verified Fact.** No current route compares `process_steps.recipe_version` to `fab_tools.recipe_rev`.

## Material finding

**Finding.** Current behaviour is local, synchronous, and split across four rule programs. The packaged feed rows are still unreconciled.
**Evidence.** The functions and counts above.
**Impact.** A later test can lock these outputs before Phase 7 changes code.
**Risk.** A write command will move the 67 REPLAY rows and the 1 inbox row.
**Confidence.** High.
**Open questions.** HTTP latency remains Unknown.

## What this file does not do

This file records current behaviour. It does not change a function.
