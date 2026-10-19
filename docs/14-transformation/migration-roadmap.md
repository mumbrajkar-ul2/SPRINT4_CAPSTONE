# Migration roadmap

| Field | Value |
|---|---|
| Stage | Phase 7 / 14 Transformation plan. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Documents only. No tests written. Inherited repo not edited. |
| Evidence sources | FD-12; `docs/07-repo-assessment/critical-workflow-inventory.md`; `docs/07-repo-assessment/baseline-behaviour.md`; `docs/04-baseline-kpis/measurement-methodology.md`; `docs/12-specs/system-spec.md`; `docs/12-specs/business-rules.md`; the four rule files; `app/gateway_bridge.py`; `app/partner_feeds.py` |
| Assumptions | Half B works in `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`. Tests set `LEGACY_DB` to a temporary file. Night-batch tests pass a copied `enterprise_legacy.sqlite3` into `run(db=...)`. |
| Unresolved issues | Node and Java availability stay Unknown. Application A and Application B host ports stay Unknown. Those ports are later work. |
| Residual risks | Editing a current function in place would break the tests that lock it by name. A generate reset would replace the packaged population. |

This file gives the order of the three slices and the names Half B uses. It does not change a function.

**Verified Fact.** FD-12. Feed intake, then reconciliation, then rule evaluation.

---

## Finding

**Finding.** Each slice has the same four steps: write the tests, run them on the current functions, add a new function beside the current one, move the caller after the shadow run matches.
**Evidence.** FD-12. Phase 7 required work. `transformation-backlog.md` TB-01 to TB-15.
**Impact.** Half B can finish one slice and stop. The next slice starts only when the earlier tests are still green.
**Risk.** Changing `priority()` before the intake and reconcile tests exist would hide a case-count miss.
**Confidence.** High
**Open questions.** Compose on this laptop. Unknown.

---

## Current behaviour of the three workflows

Honesty on packaged counts is REAL.

### Feed intake (slice 1)

**Verified Fact.** CW-08, CW-09, CW-10.

The source gateway on port 8090 builds events from `wafer_lots`. Each event JSON includes `occurred_at` and `published_at`.

`gateway_bridge.apply(events)` does this:

| Condition | Result field |
|---|---|
| Payload is not a dict, or any of `message_id`, `business_key`, `system`, `event_type`, `occurred_at` is missing or empty | `invalid` increases by 1. No row. |
| `business_key` is not a `wafer_lots.lot_id` | `invalid` increases by 1. No row. |
| `message_id` already exists in `gateway_inbox` | `duplicates` increases by 1. |
| Else | Insert with status RECEIVED. `accepted` increases by 1. |

Packaged `gateway_inbox` has 1 row, `message_id` `CHECK-semiconductor_lot`, status RECEIVED.

`consume_source_messages(limit)` reads `source_messages` ordered by `received_at` and returns a list of `{message_id, payload}`. Packaged `source_messages` count is 15.

Partner-feed rows already sit in `partner_feeds`. Intake of those rows was the earlier generate step. This slice does not run generate.

### Reconciliation (slice 2)

**Verified Fact.** CW-07. `reconcile(limit=1000)`.

On each row in NEW, RETRY, or REPLAY, in order `ingest_ts, feed_id`:

| Condition | New status | Reason |
|---|---|---|
| Missing `business_key` or `schema_rev` is `unsupported` | REJECTED | schema/key validation |
| Current status is REPLAY | DUPLICATE | replayed source message |
| Quantity is below 0 | REJECTED | quantity out of range |
| Else | ACCEPTED | none |

Packaged rows are still NEW 8,000, RETRY 500, REPLAY 67. This unit did not run `reconcile()`.

Untrusted note text does not change status. Status follows the four rows above only.

The job does not delete a row.

### Rule evaluation (slice 3)

**Verified Fact.** The four programs.

`priority(status, severity, amount)`:

| Input | Output |
|---|---|
| status CLOSED | archive |
| severity CRITICAL, status not CLOSED | urgent |
| amount above 50,000, status not CLOSED | urgent |
| severity HIGH or status ESCALATED | review |
| any other row | queue |

The 50,000 branch is a recorded Python deviation. It stays PROPOSED as live policy. Packaged `amount > 50000` count is 0. The two urgent cases are the two CRITICAL rows.

`manual_review_required` is true when severity is HIGH or CRITICAL, or status is ESCALATED or REOPENED.

Night batch `run(limit=500)` reads `operational_objects` left-joined to active `policy_register` on `region`, order `object_id`. It flags a joined row when status is HOLD or REVIEW, or when `value` is above `threshold`. REVIEW is treated as open. That matches BO-06a. Packaged REVIEW objects: 2,090. HOLD objects: 2,083.

JavaScript `threshold(region, year)` returns the archive `limit` for the first `historical_versions` row whose region matches and whose `effective_from` starts with that year. Otherwise it returns 999,999. `legacyAllows` is true when `Number(amount) <= threshold * 1.05`. Worked example: APAC 2026 archive limit 25,000. Allow line 26,250. `legacyAllows(27000,'APAC',2026)` is false on that arithmetic.

Java `ReconcileLegacy` skips a header that starts `tenant,`. It needs at least 6 comma fields. It adds field index 4 as a float. A `NumberFormatException` is ignored. Ten packaged `vendor_file_rows` have blank `amount_text`.

---

## Roadmap in time order

Worked example. Half B writes `test_char_feed_intake.py` on day one. Those tests call `apply`. They pass. Half B then adds `intake_apply` beside `apply`. The shadow run matches. The CLI moves to `intake_apply`. Only then does Half B write the remaining reconcile tests if they are not already green, and start slice 2.

| Step | Backlog | What exists after the step | What stays untouched |
|---|---|---|---|
| R0 | TB-01 to TB-04 | Five test modules under `tests/characterization/`. All green on current functions. | All application functions. |
| R1 | TB-05 to TB-07 | New intake function. Intake CLI uses it. Old `apply` still importable. | `reconcile()`, the four rule programs, `cases` rows. |
| R2 | TB-08 to TB-10 | New reconcile function. `--reconcile` uses it. Old `reconcile` still importable. | The four rule programs, `cases` rows. |
| R3 | TB-11 to TB-13 | New live-policy function. Current `priority()` still ranks. Old JS 999,999 function still importable. | Application A, Application B, lake items. |
| R4 | TB-14 to TB-15 | Logs and the six-field exact match. | Packaged file hashes. |

---

## Names Half B uses

Engineering decision ED-P7A-01, authority: team-force. Test modules:

| Module | Path |
|---|---|
| Feed intake | `tests/characterization/test_char_feed_intake.py` |
| Reconciliation | `tests/characterization/test_char_reconciliation.py` |
| Rule evaluation | `tests/characterization/test_char_rule_evaluation.py` |
| Baseline parity | `tests/characterization/test_char_baseline_parity.py` |
| Harness safety | `tests/characterization/test_char_harness_safety.py` |

Engineering decision ED-P7A-02, authority: team-force. New function names sit beside the current ones. Characterization tests keep calling the current names.

| Current name | New name | Slice |
|---|---|---|
| `gateway_bridge.apply` | `gateway_bridge.intake_apply` | Feed intake |
| `partner_feeds.reconcile` | `partner_feeds.reconcile_feeds` | Reconciliation |
| `legacy_logic.priority` | stays `priority` for ranking | Rule evaluation |
| (none today) | `legacy_logic.evaluate_live_policy` | Rule evaluation |
| `legacy_batch.shift_reconciliation.run` | `legacy_batch.shift_reconciliation.run_flag` | Rule evaluation |
| `legacyAllows` / `threshold` | stay as deviation functions | Rule evaluation |

`evaluate_live_policy` returns HOLD_FOR_REVIEW when the archive is silent or no row matches. It does not return 999,999. It does not return 50,000 as a decided live limit.

Evidence for the names: current functions already exist. A new name lets the old tests keep passing.

---

## What each slice may change

| Slice | Preserved behaviour | Approved difference | Forbidden in this phase |
|---|---|---|---|
| Feed intake | `accepted` / `duplicates` / `invalid` / `received` on the same event list. Inbox columns listed in SH-FI. | None. | Writing the packaged database. Dropping `occurred_at` or `published_at`. |
| Reconciliation | The four status rules. Untrusted notes stay data. No delete. | None on the status machine. | Text-similarity de-dupe. Compiling a new reject reason. Running on the packaged file. |
| Rule evaluation | `priority()` strings on packaged cases. Night batch flags HOLD and REVIEW. JS and Java deviation outputs on the named fixtures. | Live policy on silence or no-match is HOLD_FOR_REVIEW. | 999,999 as live policy. 50,000 as decided live policy. Merging finance-closed into operational-closed. Inventing an age cutoff. |

---

## Dependencies Half B must not skip

1. TB-01 green before TB-06.
2. TB-02 green before TB-09.
3. TB-03 green before TB-12.
4. TB-04 green before every cutover and after every cutover.
5. Slice 1 cutover or a recorded rollback before slice 2 cutover.
6. Slice 2 cutover or a recorded rollback before slice 3 cutover.

A failed six-field exact match blocks the next cutover.

---

## What this file does not do

This file does not write test source. It does not edit the inherited repo. It does not start Half B.
