# Changed components

| Field | Value |
|---|---|
| Stage | Phase 7 / 15 Transform. Half B code. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7b-doc-20261018-001 |
| Status | COMPLETE for this unit |
| Evidence sources | Inherited files listed below; ED-P7A-02 names |
| Assumptions | Old function bodies stay in the tree so rollback is a caller change. |
| Unresolved issues | Compose command lines were not started. Live HTTP stays Unknown. |
| Residual risks | A later delete of `apply` or `reconcile` would remove the rollback path. |

This file lists every inherited file Half B changed. Paths are under `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`.

---

## Finding

**Finding.** Four application files gained a new function beside the old one. One gateway helper was extracted without changing event keys. One existing test module now uses a temporary database. Five new test modules were added.
**Evidence.** The file list below.
**Impact.** Callers can move back to the old names without deleting the new functions.
**Risk.** Editing `priority()` later would change ranking and `urgent_cases`.
**Confidence.** High
**Open questions.** None for the file list.

---

## Application files

| File | What changed | Old name still importable |
|---|---|---|
| `app/gateway_bridge.py` | Added `intake_apply`. `pull()` calls `intake_apply`. `apply` body stays. | Yes. `apply` |
| `app/partner_feeds.py` | Added `reconcile_feeds`. `--reconcile` calls `reconcile_feeds`. `reconcile` body stays. | Yes. `reconcile` |
| `app/legacy_logic.py` | Added `evaluate_live_policy`. `priority` and `manual_review_required` stay. | Yes. `priority` |
| `legacy_batch/shift_reconciliation.py` | Added `run_flag`. CLI calls `run_flag`. `run` body stays. | Yes. `run` |
| `services/source_gateway/server.py` | Extracted `build_event_record`. `/api/events` still returns the same keys, including `occurred_at` and `published_at`. | Yes. Same JSON keys |

`app/server.py` was not edited. `GET /api/cases` still calls `priority()`.

`app/baseline.py` was not edited.

---

## Test files

| File | What changed |
|---|---|
| `tests/characterization/test_char_feed_intake.py` | New. Locks `apply` and SH-FI. |
| `tests/characterization/test_char_reconciliation.py` | New. Locks `reconcile` and SH-RC. |
| `tests/characterization/test_char_rule_evaluation.py` | New. Locks old rule names, live Node and Java, and `evaluate_live_policy`. |
| `tests/characterization/test_char_baseline_parity.py` | New. Locks the six Phase 0 fields. |
| `tests/characterization/test_char_harness_safety.py` | New. Locks hashes and harness rules. |
| `tests/characterization/harness.py` | New. Copies packaged SQLite files and points `store.DB` at the copy. |
| `tests/test_source_gateway.py` | Harness fix only. `setUp` copies `data/legacy.sqlite3` and points `store.DB` at that copy. Behaviour of `apply` is unchanged. |

---

## Callers after cutover

| Command or route | Function after Half B |
|---|---|
| `python -m app.gateway_bridge` through `pull()` | `intake_apply` |
| `python -m app.partner_feeds --reconcile` | `reconcile_feeds` |
| Night-batch CLI `python legacy_batch/shift_reconciliation.py` | `run_flag` |
| `GET /api/cases` | `priority` still |
| Live-policy questions | `evaluate_live_policy` |

---

## What this file does not do

This file does not list Application A or Application B. Those are later phases.
