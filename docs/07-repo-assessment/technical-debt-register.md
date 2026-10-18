# Technical debt register

| Field | Value |
|---|---|
| Stage | Phase 1 / 7 Deep repo assessment |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | Code files and query counts in this unit; `sql/legacy_reports.sql`; `tests/test_source_gateway.py`; `.github/workflows/verify.yml` |
| Assumptions | Debt here means a current-state condition that later work must keep visible. It is not a repair list. |
| Unresolved issues | Who may run `generate --reset` is Unknown. |
| Residual risks | A later phase that "cleans" a debt item before a characterization test will hide the baseline. |

This register catalogues current-state debt. It does not change the code.

## Register

| ID | Debt | Evidence | Impact | Confidence | Label |
|---|---|---|---|---|---|
| TD-01 | Four rule programs | The four source files. BP4 | Totals and priorities disagree | High | Verified Fact |
| TD-02 | Night batch join has no policy_code predicate | `shift_reconciliation.py` join on region and active only. 23,168 joined flags vs 6,279 distinct objects | Flagged_count can exceed distinct objects | High | Verified Fact |
| TD-03 | Night batch LIMIT applies to joined rows | `ORDER BY object_id LIMIT ?` on the join | Default 500 is not 500 objects | High | Verified Fact |
| TD-04 | Java float totals and skipped blanks | `ReconcileLegacy.java`. 10 blank `amount_text` rows | Month-end total omits those rows | High | Verified Fact |
| TD-05 | JavaScript 1.05 band and 999,999 default | `legacy_policy.js` | An amount above the archive limit can still pass | High | Verified Fact |
| TD-06 | Python 50,000 cutoff unused on this 125-case set | `amount > 50000` count 0 | Urgent in this set is CRITICAL only | High | Verified Fact |
| TD-07 | No authentication | `app/server.py` | GET cases is open on the port | High | Verified Fact |
| TD-08 | SQL injection surface on partner and domain table names | `app/server.py` builds `SELECT * FROM ` + table after an allow-list check | Allow-list reduces the range. The query is still concatenated | High that the allow-list exists. Medium on residual risk | Verified Fact of the code |
| TD-09 | `test_source_gateway.py` writes default `LEGACY_DB` | Test file has no temp DB | Packaged `gateway_inbox` can change | High | Verified Fact |
| TD-10 | Generate reset in CI | `.github/workflows/verify.yml` includes generate `--reset` | Packaged 125-case freeze can be replaced | High | Verified Fact |
| TD-11 | `state_history` is one row per object | MAX rows per object = 1 | Cycle time cannot be taken from that table | High | Verified Fact |
| TD-12 | No `closed_at` on cases | `PRAGMA table_info(cases)` | Exception cycle time stays Unknown | High | Verified Fact |
| TD-13 | Three region vocabularies, no map | Distinct 3 / 8 / 6 | A join on region text fails across stores | High | Verified Fact |
| TD-14 | Untuned report SQL | `sql/legacy_reports.sql` joins cases to events with no date filter | Gross amount is a float sum across all events | High | Verified Fact |
| TD-15 | Untrusted instruction text stored in operational fields | BP7 counts 86 / 150 / 3 / 22 | A reader can treat a note as a decision | High | Verified Fact |
| TD-16 | Partner reconcile mutates status in place | `partner_feeds.reconcile()` UPDATE | Prior status is overwritten | High | Verified Fact |
| TD-17 | Gateway bridge uses a named Compose volume | `compose.yaml` `legacy_data` | Compose may not read the packaged file this unit queried | High | Verified Fact |
| TD-18 | Incidents endpoint is a hard-coded row | `GET /api/incidents` returns INC-2019-0082 | INC-2025-014 is not on that route | High | Verified Fact |

## What stays out of this register

A missing age cutoff is an Unknown policy value, not code debt.

An unknown incident owner is an Unknown person, not code debt.

BO-06b is an unsigned policy row, not code debt.

## What this file does not do

This file does not schedule a cleanup. It does not edit the inherited tree.
