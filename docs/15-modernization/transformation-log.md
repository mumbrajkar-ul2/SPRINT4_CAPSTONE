# Transformation log

| Field | Value |
|---|---|
| Stage | Phase 7 / 15 Transform. Half B code. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7b-doc-20261018-001 |
| Status | COMPLETE for this unit. Characterization suite 70 tests OK. Six-field exact match twice on a copy. Packaged hashes unchanged. |
| Evidence sources | FD-12; ED-P7A-01 through ED-P7A-06; `docs/14-transformation/`; `tests/characterization/`; `python -m unittest discover -s tests/characterization -t . -v`; `python -m app.baseline` on a temp copy |
| Assumptions | Half A was accepted before this unit. Tests used temporary copies. Packaged SQLite files stayed unread for write. |
| Unresolved issues | Exception cycle time stays Unknown. Aged backlog stays Unknown. Live HTTP on ports 8080 and 8090 stays Unknown. Compose was not started. BO-06b and BO-08 stay PROPOSED. |
| Residual risks | A later run of `python -m app.generate --reset` would replace the packaged cases. A later edit of `priority()` would move `urgent_cases`. |

This file records what Half B did, in FD-12 order. Honesty on counts and command output is REAL.

**Verified Fact.** FD-12 order used: write characterization tests first, then feed intake, then reconciliation, then rule evaluation.

---

## Finding

**Finding.** Five characterization modules lock the current functions. Three new functions sit beside the old names. Callers moved after the shadow fields matched. The six Phase 0 fields still match exactly on a copy.
**Evidence.** Suite output 70 tests OK. Baseline JSON twice. Shadow counts in `test-execution-log.md`.
**Impact.** A later reviewer can replay the commands.
**Risk.** Treating the default-limit reconcile result as a full 67-row flip. The default limit of 1,000 left 59 REPLAY rows untouched on this copy.
**Confidence.** High
**Open questions.** BO-08 signer. Owner: Business Owner.

---

## Backlog status

| Id | Status | What Half B did |
|---|---|---|
| TB-01 | DONE | Wrote `tests/characterization/test_char_feed_intake.py`. Tests call `apply`. |
| TB-02 | DONE | Wrote `tests/characterization/test_char_reconciliation.py`. Tests call `reconcile`. |
| TB-03 | DONE | Wrote `tests/characterization/test_char_rule_evaluation.py`. Tests call `priority`, `run`, `threshold`, and the Java program. |
| TB-04 | DONE | Wrote `test_char_baseline_parity.py` and `test_char_harness_safety.py`. |
| TB-05 | DONE | SH-FI on two copies. `accepted` 1, `duplicates` 1, `invalid` 2, `received` 4 on both. Inbox columns match. `received_at` omitted. |
| TB-06 | DONE | Added `gateway_bridge.intake_apply` beside `apply`. |
| TB-07 | DONE | `pull()` now calls `intake_apply`. |
| TB-08 | DONE | SH-RC on two copies, `limit=1000`. Both returned `accepted` 922, `rejected` 71, `duplicate` 7, `skipped` 0. Per-`feed_id` status matched. Row count stayed 8,567. |
| TB-09 | DONE | Added `partner_feeds.reconcile_feeds` beside `reconcile`. |
| TB-10 | DONE | `python -m app.partner_feeds --reconcile` now calls `reconcile_feeds`. |
| TB-11 | DONE | SH-RE on a copy, `limit=500`. `run` and `run_flag` both returned `processed` 500 and `flagged_count` 210. Old `priority()` strings on packaged cases stayed the same. Live Node and Java ran. |
| TB-12 | DONE | Added `legacy_logic.evaluate_live_policy` and `shift_reconciliation.run_flag`. |
| TB-13 | DONE | Night-batch CLI now calls `run_flag`. `GET /api/cases` still calls `priority()`. |
| TB-14 | DONE | This folder and `docs/16-repo-validation/`. |
| TB-15 | DONE | `python -m app.baseline` twice on a copy. Six fields match Phase 0. |

---

## Order actually followed

1. Wrote the five test modules. Characterization tests call the old names.
2. Ran `python -m unittest discover -s tests/characterization -t . -v` from `fabpulse-legacy`. First run had three test-literal misses. Those tests were corrected to match the source. Six new-function tests skipped until the new names existed.
3. Added `intake_apply`. Shadow matched. `pull()` moved.
4. Added `reconcile_feeds`. Shadow matched. `--reconcile` moved.
5. Added `evaluate_live_policy` and `run_flag`. Shadow matched on night batch. Live-policy tests then ran.
6. Ran the suite again. 70 tests OK.
7. Ran `python -m app.baseline` twice on a temp copy of `data/legacy.sqlite3`.

No slice ran `python -m app.generate --reset`.

---

## What this file does not do

This file does not start Phase 8. It does not write BO-06b or BO-08 as signed policy.
