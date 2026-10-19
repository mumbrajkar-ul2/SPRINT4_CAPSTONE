# Behaviour preservation evidence

| Field | Value |
|---|---|
| Stage | Phase 7 / 15 Transform. Half B code. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7b-doc-20261018-001 |
| Status | COMPLETE for this unit |
| Evidence sources | Characterization suite 70 OK; SH-FI, SH-RC, SH-RE numbers; `python -m app.baseline` twice on a copy; packaged hashes |
| Assumptions | Shadow compare used temporary copies. Packaged files were not the write target. |
| Unresolved issues | Exception cycle time stays Unknown. Aged backlog stays Unknown. Live HTTP stays Unknown. |
| Residual risks | Comparing `received_at` would look like a miss because `apply` writes the clock at insert time. |

This file shows which current outputs stayed the same. Honesty on numbers is REAL.

---

## Finding

**Finding.** Feed intake counts matched. Reconcile counts and per-`feed_id` status matched. Night-batch `processed`, `by_tenant`, and flagged count matched. Every packaged case still gets the same `priority()` string. The six Phase 0 fields still match.
**Evidence.** Commands and results in `test-execution-log.md`.
**Impact.** The three slices did not move the Phase 0 baseline.
**Risk.** Reading the default-limit reconcile `duplicate` of 7 as a loss of the 67 REPLAY rows. Fifty-nine REPLAY rows were outside the first 1,000 pending rows.
**Confidence.** High
**Open questions.** None for the six fields.

---

## Six-field baseline

Command, from the inherited root, with `LEGACY_DB` set to a temp copy of `data/legacy.sqlite3`:

```text
python -m app.baseline
python -m app.baseline
```

Both runs printed:

```text
{"records": 125, "open_cases": 89, "urgent_cases": 2, "mean_amount": 4982.61, "sites": 6, "hours_per_case": 0.603}
```

Label: REAL. Exact match to Phase 0. No tolerance percent.

Exception cycle time is Unknown. Aged backlog is Unknown.

On that same copy, `priority()` on the 125 cases returned archive 36, queue 70, review 17, urgent 2. The two urgent rows are the two CRITICAL rows. Label: REAL.

---

## Feed intake (preserved)

Same four events on two copies. One missing-field event, one unknown lot, one new valid event, then the same `message_id` again.

| Field | `apply` | `intake_apply` |
|---|---|---|
| accepted | 1 | 1 |
| duplicates | 1 | 1 |
| invalid | 2 | 2 |
| received | 4 | 4 |

Inbox rows matched on `message_id`, `external_ref`, `source_system`, `event_type`, `event_time`, `status`, and `raw_payload`. `received_at` was omitted. That omit is PROPOSED, owner Team-Force (ED-P7A-04).

---

## Reconciliation (preserved)

Two copies of packaged `partner_feeds`. Both called with `limit=1000`.

| Field | `reconcile` | `reconcile_feeds` |
|---|---|---|
| accepted | 922 | 922 |
| rejected | 71 | 71 |
| duplicate | 7 | 7 |
| skipped | 0 | 0 |
| row count | 8567 | 8567 |

Per-`feed_id` `processing_status` and `error_reason` matched.

Of the 67 packaged REPLAY rows after that default-limit run: 7 became DUPLICATE, 1 became REJECTED because schema or key failed first, 59 stayed REPLAY because they were not in the first 1,000 pending rows. Label: REAL. This is current `reconcile()` order. The new function keeps that order.

Untrusted note text stayed in `raw_json`. Status followed the four rules only.

---

## Rule evaluation (preserved on old names)

`priority()` strings on packaged cases stayed the same. Night batch on a copy with `limit=500`:

| Field | `run` | `run_flag` |
|---|---|---|
| processed | 500 | 500 |
| flagged_count | 210 | 210 |
| by_tenant | same map | same map |

`flagged_preview` is the first 12 flagged rows. The full flagged set on that copy and limit is 210. REVIEW object `FAB-00000011` and HOLD object `FAB-00000022` are in that set.

Live Node, working directory the inherited root:

```text
{"threshold_apac_2026":25000,"allows_26250":true,"allows_27000":false,"threshold_apac_1999":999999}
```

Label: REAL. The 999,999 value is the current JavaScript default. It is not live policy.

Live Java on a three-row fixture plus a short line: `count=1 total=10.50`. The blank amount cell and the unreadable amount were omitted. Label: REAL.

---

## Packaged freeze

After the suite:

| File | sha256 |
|---|---|
| `data/legacy.sqlite3` | `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879` |
| `data/enterprise_legacy.sqlite3` | `f13ed709df16f3c6244282ff4efde7768dee9294f0533098de3d34f0657af913` |

Both match `sources/register.yaml`. Label: REAL.

---

## What this file does not do

This file does not treat 50,000 as decided live policy. It does not treat 999,999 as live policy.
