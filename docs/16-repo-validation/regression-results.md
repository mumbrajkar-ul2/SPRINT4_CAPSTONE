# Regression results

| Field | Value |
|---|---|
| Stage | Phase 7 / 16 Validate. Half B. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7b-doc-20261018-001 |
| Status | COMPLETE for this unit |
| Evidence sources | Final `python -m unittest discover -s tests/characterization -t . -v`; `python -m app.baseline` twice on a copy |
| Assumptions | The characterization suite is the regression set for this phase. Inherited modules other than the harness fix were not the pass gate. |
| Unresolved issues | Full inherited `tests/` suite was not the Phase 7 gate. `test_source_gateway.py` was updated only to use a temp copy. |
| Residual risks | Running inherited tests that still import `store` before setting `LEGACY_DB` can write a default path if another module is added later. |

Honesty on counts is REAL.

---

## Finding

**Finding.** 70 characterization tests passed. The six Phase 0 fields matched twice. Packaged hashes matched.
**Evidence.** Commands in `docs/15-modernization/test-execution-log.md`.
**Impact.** Old-name tests stayed green after cutover.
**Risk.** Calling 89 the aged backlog. That field stays Unknown.
**Confidence.** High
**Open questions.** None for the six fields.

---

## Characterization suite

Command:

```text
python -m unittest discover -s tests/characterization -t . -v
```

Working directory: `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`.

```text
Ran 70 tests in 5.775s

OK
```

Breakdown by module on the final run:

| Module | Tests | Result |
|---|---|---|
| `test_char_baseline_parity.py` | 2 | OK |
| `test_char_feed_intake.py` | 13 | OK |
| `test_char_harness_safety.py` | 8 | OK |
| `test_char_reconciliation.py` | 11 | OK |
| `test_char_rule_evaluation.py` | 36 | OK |

Old-name tests that must stay green after cutover: `apply`, `reconcile`, `priority`, `run`, `threshold`, `legacyAllows`, Java `ReconcileLegacy`. All passed.

---

## Baseline regression

On a temp copy of `data/legacy.sqlite3`:

| Field | Phase 0 | Run 1 | Run 2 |
|---|---|---|---|
| records | 125 | 125 | 125 |
| open_cases | 89 | 89 | 89 |
| urgent_cases | 2 | 2 | 2 |
| mean_amount | 4982.61 | 4982.61 | 4982.61 |
| sites | 6 | 6 | 6 |
| hours_per_case | 0.603 | 0.603 | 0.603 |

Exact match. No tolerance percent.

Exception cycle time: Unknown.
Aged backlog: Unknown.

---

## Packaged files

Hashes after the suite match `sources/register.yaml`. The packaged databases were not written.

---

## What this file does not do

This file does not claim a live HTTP pass. Ports 8080 and 8090 were not started.
