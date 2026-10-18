# Characterization test plan

| Field | Value |
|---|---|
| Stage | Phase 1 / 7 Deep repo assessment |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE. Plan only. No tests written in this unit |
| Evidence sources | `critical-workflow-inventory.md`; `baseline-behaviour.md`; `conflict-catalogue.md`; the seven current test modules |
| Assumptions | Later tests run against a copy or a temporary database. They do not write the packaged files used for this catalogue. |
| Unresolved issues | FD-12 (characterization approach and strangle order) is still PENDING. This plan names checks. It does not set that decision. |
| Residual risks | Adding tests that call `gateway_bridge.apply()` on the default `LEGACY_DB` will change the freeze. |

This file says what a later test must check. It does not contain test code.

## Rule for later authors

A characterization test records what the current program returns. It does not change the program to make the test pass.

Use a temporary database or a copied file. Do not open the packaged SQLite files for write.

## Where coverage is thin today

**Verified Fact.** Current tests do not assert the eight catalogue counts. They do not call the HTTP routes. They do not run the Java or JavaScript programs. `test_source_gateway.py` can write the packaged database.

## Checks a later test must make

### CW-01 and CW-14 Case priority and baseline

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-01 | `baseline()` on the packaged 125-case file | records 125, open_cases 89, urgent_cases 2, sites 6 | BP5 |
| CT-02 | `priority('CLOSED', 'LOW', 99999)` | archive | BP4 |
| CT-03 | `priority('OPEN', 'CRITICAL', 1)` | urgent | BP4 |
| CT-04 | `priority('OPEN', 'LOW', 50001)` | urgent | BP4 |
| CT-05 | Count of cases with `amount > 50000` on the packaged file | 0 | BP4 |

### CW-07 Partner replay

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-06 | Count of `processing_status = 'REPLAY'` on a copy of the packaged file, before reconcile | 67 | BP2 |
| CT-07 | After `reconcile()` on a copy, those REPLAY ids become DUPLICATE with reason `replayed source message` | 67 rows flipped on that copy | BP2 |
| CT-08 | A NEW row with `schema_rev = 'unsupported'` becomes REJECTED | status REJECTED | BP2 |
| CT-09 | A NEW row with negative quantity becomes REJECTED | status REJECTED | BP2 |

### CW-15 Recipe join

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-10 | Count of `process_steps` joined to `fab_tools` where `recipe_version != recipe_rev` | 91 | BP1 |
| CT-11 | Count of process_steps | 125 | BP1 |
| CT-12 | Unjoined process_steps | 0 | BP1 |

### CW-02 and CW-08 Clocks

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-13 | Count of `evidence_events` where `arrival_time != event_time` | 11,985 | BP3 |
| CT-14 | Count of `partner_feeds` where `ingest_ts != source_ts` | 7,471 | BP3 |
| CT-15 | Count of overlapping `reference_versions` pairs on the same `ref_key` | 45 | BP3 |
| CT-16 | Gateway JSON includes both `occurred_at` and `published_at` | both keys present | BP3 |

### CW-11, CW-12, CW-13 Four rule outputs on one fixture

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-17 | Night batch on a known REVIEW object | object is in `flagged` | BP4, BP5 |
| CT-18 | Count of `operational_objects` with status REVIEW | 2,090 | BP4 |
| CT-19 | JavaScript `legacyAllows(26250, 'APAC', 2026)` | true, because 25,000 * 1.05 = 26,250 | BP4 |
| CT-20 | JavaScript `threshold('APAC', 1999)` | 999999 | BP4 |
| CT-21 | Java parser on a CSV line with a blank amount cell | that line is omitted from count | BP4 |
| CT-22 | Count of blank `amount_text` on a copy of vendor rows | 10 | BP4 |

### CW-01 Status words

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-23 | Distinct `cases.status` values | CLOSED, ESCALATED, OPEN, REOPENED, UNDER_REVIEW | BP5 |
| CT-24 | Distinct `operational_objects.status` values | CLOSED, ESCALATED, HOLD, OPEN, REOPENED, REVIEW | BP5 |
| CT-25 | A REVIEW object is treated as open under BO-06a | REVIEW is in the open set of the test fixture | BP5 |

CT-25 records the SME meaning. It does not rewrite the night batch.

### CW-11 and policies

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-26 | Active `policy_register` count | 34 | BP6 |
| CT-27 | Active count per region is 4 or 5 | AU 4, BR 4, DE 5, GB 4, IN 4, JP 4, US 5, ZA 4 | BP6 |
| CT-28 | Distinct `cases.region` | APAC, EMEA, AMER | BP6 |
| CT-29 | Distinct `operational_objects.region` | eight country codes | BP6 |

### CW-05 Untrusted text

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-30 | Count of partner_feeds whose `raw_json` contains `auto approve` or `disregard validation` | 86 | BP7 |
| CT-31 | Those 86 rows stay data. `reconcile()` does not change status because of that note | status change follows the key, schema, replay, and quantity rules only | BP7 |
| CT-32 | Bundled lake events with `source_claim` | 150 | BP7 |
| CT-33 | Archive `.eml` files containing approve or ignore | 3 | BP7 |
| CT-34 | Source documents whose body contains approve, ignore, or release all holds | 22 | BP7 |

### CW-01 and CW-04 Auth and ownership

| Check id | What to assert | Expected from this unit | Linked BP |
|---|---|---|---|
| CT-35 | `GET /api/cases` without an identity header | HTTP 200 on the current server | BP8 |
| CT-36 | Count of `workflow_tasks` with `assigned_to` IS NULL | 695 | BP8 |
| CT-37 | `GET /api/incidents` body | contains INC-2019-0082 and does not contain an owner for INC-2025-014 | BP8 |

CT-35 records current behaviour. It is not an approval of open access.

### Safety checks for the test harness itself

| Check id | What to assert |
|---|---|
| CT-38 | Every write test sets `LEGACY_DB` to a temporary file |
| CT-39 | The packaged `data/legacy.sqlite3` and `data/enterprise_legacy.sqlite3` hashes match the source register after the test run |
| CT-40 | Headline KPI tests write Unknown when close-time or age cutoff is absent. They do not invent a cutoff |

## Order hint from the tracker

**Verified Fact.** FD-12 default text says feed intake first, then reconciliation, then rule evaluation. FD-12 is still PENDING. This plan lists checks. It does not lock that order.

## What this file does not do

This file does not include test source. It does not run `unittest`.
