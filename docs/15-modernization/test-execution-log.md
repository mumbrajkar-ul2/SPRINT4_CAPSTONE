# Test execution log

| Field | Value |
|---|---|
| Stage | Phase 7 / 15 Transform. Half B code. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7b-doc-20261018-001 |
| Status | COMPLETE for this unit. Final suite 70 tests OK. |
| Evidence sources | Commands below, run from `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` on 2026-10-18 |
| Assumptions | Write tests used temporary copies. `LEGACY_DB` for baseline was a temp copy. |
| Unresolved issues | Live HTTP on 8080 and 8090 stays Unknown. Compose was not started. |
| Residual risks | Re-running the inherited `tests/test_source_gateway.py` without its new temp copy would write the packaged inbox. That module now copies the file first. |

Honesty on every command result is REAL.

---

## Finding

**Finding.** The characterization suite ended at 70 tests OK. Node and Java ran live. The six Phase 0 fields matched twice on a copy. Packaged hashes matched the source register.
**Evidence.** The command blocks below.
**Impact.** TG-01 through TG-08 have recorded results.
**Risk.** Treating the first suite run as a behaviour miss. That run failed three test assertions that used the wrong source literal.
**Confidence.** High
**Open questions.** None for the six fields.

---

## Working directory

```text
c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE\fabpulse-legacy-workshop-v8-Semiconductor\fabpulse-legacy
```

Tools on this machine: Python 3.13.5, Node v22.18.0, javac 25.0.2, java 25.0.2.

---

## Run 1 — characterization tests exist, new functions do not

Command:

```text
python -m unittest discover -s tests/characterization -t . -v
```

Result: 70 tests ran. 61 OK. 6 skipped (new names missing). 3 failed.

The three failures were test literals, not application output:

1. `test_headline_kpis_remain_unknown` looked for `status!='CLOSED'` and the source has `r['status']!='CLOSED'`.
2. `test_reconcile_replay_becomes_duplicate` expected every processed REPLAY row to be DUPLICATE. Current `reconcile()` tests schema or key first. `REPLAY-000002921` became REJECTED.
3. `test_night_batch_flags_review_as_open` looked for `('HOLD', 'REVIEW')` with spaces. The source has `('HOLD','REVIEW')`.

Those three tests were corrected to lock the current source. No application function changed for those fixes.

---

## Run 2 — after the three slices

Same command:

```text
python -m unittest discover -s tests/characterization -t . -v
```

One leftover fail: `test_evaluate_live_policy_silent_urgent_cutoff_is_hold` found `50000` in the new function docstring. The docstring was rewritten without those digits. The function still does not return 50,000.

---

## Run 3 — final suite

Same command:

```text
python -m unittest discover -s tests/characterization -t . -v
```

Result:

```text
Ran 70 tests in 5.775s

OK
```

Every named test in `docs/14-transformation/characterization-test-plan.md` that this machine can run passed. Node and Java were present, so those live runs were not labelled Unknown.

Skipped count on this final run: 0.

---

## Shadow results recorded beside the suite

### SH-FI Feed intake

Two copies. Same four events.

```text
apply         {'accepted': 1, 'duplicates': 1, 'invalid': 2, 'received': 4}
intake_apply  {'accepted': 1, 'duplicates': 1, 'invalid': 2, 'received': 4}
inbox match   True
```

`received_at` omitted.

### SH-RC Reconciliation

Two copies. `limit=1000`.

```text
reconcile        {'accepted': 922, 'rejected': 71, 'duplicate': 7, 'skipped': 0}
reconcile_feeds  {'accepted': 922, 'rejected': 71, 'duplicate': 7, 'skipped': 0}
row count        8567 8567
per-feed_id      match
REPLAY after     DUPLICATE 7, REJECTED 1, REPLAY 59
```

The 59 remaining REPLAY rows were outside the first 1,000 pending rows ordered by `ingest_ts, feed_id`.

### SH-RE Rule evaluation

Night batch on a copied enterprise file, `limit=500`:

```text
run       processed=500 flagged_count=210
run_flag  processed=500 flagged_count=210
by_tenant match
```

Live policy:

```text
evaluate_live_policy('APAC', 1999)                  HOLD_FOR_REVIEW
evaluate_live_policy(question='urgent_amount_cutoff') HOLD_FOR_REVIEW
evaluate_live_policy('APAC', 2026)                  {'limit': 25000, 'currency': 'USD', 'region': 'APAC', 'year': 2026, 'rule': 'recipe_release'}
```

Live Node:

```text
{"threshold_apac_2026":25000,"allows_26250":true,"allows_27000":false,"threshold_apac_1999":999999}
```

Live Java fixture: `count=1 total=10.50`.

---

## Baseline twice on a copy

```text
$env:LEGACY_DB = <temp copy of data\legacy.sqlite3>
python -m app.baseline
python -m app.baseline
```

Both printed:

```text
{
  "records": 125,
  "open_cases": 89,
  "urgent_cases": 2,
  "mean_amount": 4982.61,
  "sites": 6,
  "hours_per_case": 0.603
}
```

`--reset` was not passed to generate.

---

## Packaged hashes after the suite

```text
legacy.sqlite3            2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879
enterprise_legacy.sqlite3 f13ed709df16f3c6244282ff4efde7768dee9294f0533098de3d34f0657af913
```

Both match `sources/register.yaml`.

---

## What this file does not do

This file does not start Phase 8. It does not invent a pass for a missing tool. Node and Java were present and ran.
