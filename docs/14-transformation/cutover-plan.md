# Cutover plan

| Field | Value |
|---|---|
| Stage | Phase 7 / 14 Transformation plan. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Documents only. No tests written. Inherited repo not edited. |
| Evidence sources | FD-12; `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `docs/04-baseline-kpis/measurement-methodology.md`; `docs/07-repo-assessment/baseline-behaviour.md`; `app/gateway_bridge.py`; `app/partner_feeds.py`; `app/baseline.py`; `app/server.py` |
| Assumptions | One slice cuts over at a time. The old function stays importable. Packaged SQLite files stay unread for write. |
| Unresolved issues | Whether Compose is used for the cutover check stays Unknown. Identity on port 8080 stays the current open GET. That is recorded, not approved. |
| Residual risks | Moving the caller before the shadow run is recorded would hide a difference. A generate reset would replace the packaged cases used for the six-field check. |

This file says how each slice goes live. It does not change a function.

**Verified Fact.** Phase 7 is the first phase that may change application behaviour. Phases 0 to 6 changed no application behaviour.

---

## Finding

**Finding.** Cutover is a one-line caller change after the characterization tests and the shadow run match. The old function stays in the file.
**Evidence.** FD-12. Current CLIs in `gateway_bridge.main`, `partner_feeds.main`, and `legacy_batch.shift_reconciliation`.
**Impact.** Rollback is a one-line caller change back. See `rollback-strategy.md`.
**Risk.** Deleting the old function at cutover would remove the rollback path.
**Confidence.** High
**Open questions.** Compose on this laptop.

---

## Shared cutover steps

Half B does these steps for every slice. The slice-specific rows follow.

1. The characterization tests for that slice are green on the current function. Test names are in `characterization-test-plan.md`.
2. The harness-safety tests are green. Packaged hashes match the source register.
3. The new function exists beside the current one. The current body is unchanged.
4. The shadow run is recorded in `docs/15-modernization/test-execution-log.md`. Compared fields are in `transformation-gates.md`.
5. Every difference has a row: preserved, or approved with a locked source. Approved rows in this phase are only the live-policy HOLD_FOR_REVIEW path in slice 3.
6. The caller imports the new function.
7. `python -m app.baseline` on a copy of the packaged cases prints the six fields exactly: records 125, open_cases 89, urgent_cases 2, mean_amount 4982.61, sites 6, hours_per_case 0.603.
8. Characterization tests that call the old names are still green.

Honesty on the six fields is REAL. Label: Verified Fact of the Phase 0 tool output.

Exception cycle time stays Unknown. Aged backlog stays Unknown. Those two are not a cutover check.

---

## Slice 1 — feed intake

| Field | Value |
|---|---|
| Caller today | `python -m app.gateway_bridge` calls `pull` then `apply`. |
| Caller after cutover | Same command calls `intake_apply` inside `pull` or `apply`'s caller. |
| Finding | `apply` is the write path into `gateway_inbox`. |
| Evidence | `app/gateway_bridge.py`. Packaged inbox has 1 RECEIVED row. |
| Impact | New events enter through `intake_apply`. |
| Risk | `test_source_gateway.py` still calls `apply` on the default database. Half B sets `LEGACY_DB` in that module or leaves it unrun against the packaged file. |
| Confidence | High |
| Open questions | Whether the inherited `tests/test_source_gateway.py` is updated in Half B only to set a temporary database. That is a harness fix, not a behaviour change. |
| Go live when | FI tests green. SH-FI match. Six-field exact match. Packaged hashes unchanged. |
| Stay on old function when | Any FI test fails, or SH-FI counts differ, or hashes move. |

Worked example. Half B copies `data/legacy.sqlite3` to a temp file. Sets `LEGACY_DB` to that copy. Sends the same three events through `apply` and `intake_apply`. Both return `invalid=1` for a payload that lacks `message_id`. Both accept one new `message_id` that points at a real `lot_id`. Both count the second send as a duplicate. Then the CLI import changes to `intake_apply`.

---

## Slice 2 — reconciliation

| Field | Value |
|---|---|
| Caller today | `python -m app.partner_feeds --reconcile` calls `reconcile()`. |
| Caller after cutover | Same flag calls `reconcile_feeds()`. |
| Finding | Default limit is 1,000. Order is `ingest_ts, feed_id`. Packaged REPLAY count is 67. |
| Evidence | `app/partner_feeds.py`. CT-06, CT-07. |
| Impact | A later operator who runs `--reconcile` on a working copy hits the new function. The packaged file is not that copy. |
| Risk | Running the command without `LEGACY_DB` pointed at a copy. |
| Confidence | High |
| Open questions | None for the four status rules. |
| Go live when | RC tests green. SH-RC per-`feed_id` exact match on two copies. Six-field exact match. Packaged hashes unchanged. |
| Stay on old function when | Any REPLAY row on the copy is missing, or a status reason differs. |

Worked example. Copy A and copy B each start with 67 REPLAY rows. `reconcile(limit=1000)` on copy A and `reconcile_feeds(limit=1000)` on copy B both report `duplicate=67` if every REPLAY row is in the first 1,000 NEW/RETRY/REPLAY rows by `ingest_ts, feed_id`. Half B records the actual counts from the copies. The 67-row lock is the before-reconcile count on the packaged copy, then the after-reconcile DUPLICATE count on that same copy.

The job does not delete a row. A person at RT-05 still confirms a drop in later application work.

---

## Slice 3 — rule evaluation

| Field | Value |
|---|---|
| Caller today | `GET /api/cases` calls `priority()`. Night batch CLI calls `run()`. JavaScript and Java are optional programs. |
| Caller after cutover | `GET /api/cases` still calls `priority()`. Night batch CLI may call `run_flag()` with the same HOLD and REVIEW test. Live-policy questions call `evaluate_live_policy()`. |
| Finding | Two packaged urgent cases come from CRITICAL. Changing live policy does not change those two rows. |
| Evidence | Phase 0 `urgent_cases` 2. CT-05 count of `amount > 50000` is 0. BR-11. BR-05. |
| Impact | The six-field baseline can stay exact while live policy starts returning HOLD_FOR_REVIEW on silence. |
| Risk | Replacing `priority()` in place. This plan leaves `priority()` in place. |
| Confidence | High on the packaged urgent count. |
| Open questions | Node and `javac` for the deviation fixtures. |
| Go live when | RE tests green on the old names. SH-RE old-function outputs match. `evaluate_live_policy` has tests for silence and no-match returning HOLD_FOR_REVIEW. Six-field exact match. Packaged hashes unchanged. |
| Stay on old function when | Any `priority()` string on a packaged case changes, or night-batch flagged `object_id` set changes on the same copy and limit. |

Worked example. `evaluate_live_policy` for region APAC year 1999, when no archive row starts with 1999, returns HOLD_FOR_REVIEW. The old `threshold('APAC', 1999)` still returns 999,999. Characterization test CT-20 still calls `threshold`. The difference is written as an approved change with source BR-05.

---

## After the last slice

Half B writes `docs/16-repo-validation/behavior-difference-report.md`. Every difference is preserved or approved.

Half B writes `docs/16-repo-validation/validation-signoff.md` only after the six-field exact match and the difference report.

This cutover does not start Application A. This cutover does not start Application B.

---

## What this file does not do

This file does not write test source. It does not edit the inherited repo. It does not start Half B.
