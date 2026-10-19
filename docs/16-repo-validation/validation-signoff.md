# Validation signoff

| Field | Value |
|---|---|
| Stage | Phase 7 / 16 Validate. Half B. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7b-doc-20261018-001 |
| Status | COMPLETE for this unit. Executor read: PASS. The reviewer makes the real call. |
| Evidence sources | Characterization suite 70 OK; two matching `python -m app.baseline` runs on a copy; packaged hashes; `behavior-difference-report.md` |
| Assumptions | Signoff here is the executor record. It does not replace the reviewer gate. |
| Unresolved issues | Exception cycle time stays Unknown. Aged backlog stays Unknown. Live HTTP stays Unknown. BO-06b and BO-08 stay PROPOSED. |
| Residual risks | A later generate reset, or an in-place edit of `priority()`, would void this signoff. |

This file records that the Half B done test was run. It does not start Phase 8.

---

## Finding

**Finding.** Characterization parity holds for every transformed path. Every behaviour difference is marked preserved or approved. The six Phase 0 fields match exactly on a copy, twice.
**Evidence.** `test-execution-log.md`. `behavior-difference-report.md`. Hash check.
**Impact.** The coordinator can send this unit to the reviewer.
**Risk.** Treating Unknown headline KPIs as a fail. Those cells were already Unknown in Phase 0.
**Confidence.** High
**Open questions.** Reviewer verdict.

---

## Done test

| Check | Result | Honesty |
|---|---|---|
| Characterization suite | 70 tests OK | REAL |
| Shadow SH-FI | Counts and inbox columns match | REAL |
| Shadow SH-RC | Counts and per-`feed_id` match | REAL |
| Shadow SH-RE old names | `priority`, night batch, Node, Java match | REAL |
| Live-policy silence and no-match | HOLD_FOR_REVIEW | REAL |
| `python -m app.baseline` twice on a copy | Exact six-field match | REAL |
| Packaged hashes | Match `sources/register.yaml` | REAL |
| Every difference explained | Preserved or approved | REAL |
| Headline KPIs | Unknown | Unknown |

Six fields:

```text
{"records": 125, "open_cases": 89, "urgent_cases": 2, "mean_amount": 4982.61, "sites": 6, "hours_per_case": 0.603}
```

---

## Executor signoff

| Item | Value |
|---|---|
| Unit | Phase 7 Half B |
| Executor read | PASS |
| Authority of this line | team-force record only. Not the reviewer grade |
| Date | 2026-10-18 |
| Correlation id | corr-p7b-doc-20261018-001 |

Phase 8 is not started.

---

## What this file does not do

This file does not update `STATUS.md`, `Decision_Tracker.md`, the playbook log, or `PROJECT_ACRONYMS.md`.
