# Characterization test plan

| Field | Value |
|---|---|
| Stage | Phase 7 / 14 Transformation plan. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Plan only. No tests written in this unit. Inherited repo not edited. |
| Evidence sources | `docs/07-repo-assessment/characterization-test-plan.md` CT-01 to CT-40; `docs/07-repo-assessment/baseline-behaviour.md`; `docs/07-repo-assessment/critical-workflow-inventory.md`; `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `docs/12-specs/business-rules.md`; `app/legacy_logic.py`; `app/partner_feeds.py`; `app/gateway_bridge.py`; `app/baseline.py`; `app/integration.py`; `legacy_js/legacy_policy.js`; `legacy_java/ReconcileLegacy.java`; `legacy_batch/shift_reconciliation.py` |
| Assumptions | Half B writes tests under `tests/characterization/` after HALF_A_ACCEPTED. Every write test sets `LEGACY_DB` to a temporary file. Night-batch tests pass a copied enterprise database into `run(db=...)`. |
| Unresolved issues | Node and Java availability stay Unknown. Live HTTP on 8080 and 8090 stay Unknown until Half B starts those listeners or calls the handler functions. FD-12 is DECIDED. This file uses that order. |
| Residual risks | Calling `gateway_bridge.apply()` on the default `LEGACY_DB` writes the packaged inbox. Running `reconcile()` on the packaged file flips the 67 REPLAY rows. |

This file names the tests Half B must write before each change. It names the behaviour each test locks. It does not contain test code.

A characterization test records what the current program returns. It does not change the program to make the test pass.

**Verified Fact.** FD-12. Write the feed-intake tests and keep them green before slice 1 changes. Write the reconciliation tests and keep them green before slice 2 changes. Write the rule-evaluation tests and keep them green before slice 3 changes. Baseline and harness tests run before the first change and after every cutover.

Phase 1 check ids CT-01 to CT-40 stay in this file. Half B uses the function names in the tables. Do not drop a Phase 1 check.

Honesty on packaged counts is REAL.

---

## Finding

**Finding.** Sixty-five named tests cover the work. Twelve lock feed intake. Eleven lock reconciliation. Twenty-nine lock current rule evaluation. Three lock the new live-policy path after slice 3 exists. Two lock the six-field baseline. Eight lock the harness. They lock current behaviour. They leave live policy numbers unsigned.
**Evidence.** Phase 1 CT-01 to CT-40. The four rule files. `app/partner_feeds.py` `reconcile()`. `app/gateway_bridge.py` `apply()`. Phase 0 baseline JSON.
**Impact.** Half B can write each function without choosing a threshold.
**Risk.** A test that asserts 50,000 as decided live policy, or 999,999 as live policy, or an aged-backlog day count.
**Confidence.** High on the documented outputs. Unknown on live Node and Java.
**Open questions.** Whether Half B starts the HTTP listeners.

---

## Shared harness rules

Engineering decision ED-P7A-01, authority: team-force. Five modules:

| Module | Path | Write before |
|---|---|---|
| Feed intake | `tests/characterization/test_char_feed_intake.py` | Slice 1 |
| Reconciliation | `tests/characterization/test_char_reconciliation.py` | Slice 2 |
| Rule evaluation | `tests/characterization/test_char_rule_evaluation.py` | Slice 3 |
| Baseline parity | `tests/characterization/test_char_baseline_parity.py` | First change, and every cutover |
| Harness safety | `tests/characterization/test_char_harness_safety.py` | First change, and every cutover |

Engineering decision ED-P7A-05, authority: team-force. JavaScript and Java tests prefer a live Node or `java` run. When those tools are missing, the test asserts the source literals and the Phase 1 expected values. The live run is then labelled Unknown. The fixture values stay REAL as already recorded.

Engineering decision ED-P7A-02, authority: team-force. These tests call the current function names. New functions added in Half B are tested separately. Old-name tests stay green after cutover.

Use `unittest`. That matches the seven current test modules.

Read packaged SQLite with `mode=ro` when the test only counts. Copy the file when the test writes.

---

## Feed intake — write before slice 1

Module: `tests/characterization/test_char_feed_intake.py`.

Current functions: `gateway_bridge.apply`, source-gateway event JSON, `integration.consume_source_messages`.

| Test function | Phase 1 id | Behaviour it locks | Expected |
|---|---|---|---|
| `test_packaged_inbox_one_received` | (gap fill from baseline-behaviour) | Packaged `gateway_inbox` on a read-only open | 1 row. `message_id` is `CHECK-semiconductor_lot`. Status RECEIVED. |
| `test_apply_rejects_missing_required_fields` | (gap fill from `apply`) | `apply([{'message_id': 'bad'}])` | `invalid` is 1. `accepted` is 0. |
| `test_apply_rejects_missing_occurred_at` | (gap fill from `apply`) | Payload with `message_id`, `business_key`, `system`, `event_type` and no `occurred_at` | `invalid` increases by 1. |
| `test_apply_rejects_unknown_lot` | (gap fill from `apply`) | `business_key` that is not a `wafer_lots.lot_id` | `invalid` increases by 1. |
| `test_apply_accepts_new_valid_event` | (gap fill from `apply`) | New `message_id`, `business_key` equal to a real `lot_id`, plus `system`, `event_type`, `occurred_at` | `accepted` increases by 1. Inbox status RECEIVED. `event_time` equals `occurred_at`. |
| `test_apply_duplicate_message_id` | (existing thin test) | Same `message_id` sent twice on a temp DB | Second call `duplicates` is 1. |
| `test_gateway_event_json_has_both_clocks` | CT-16 | Event object the gateway builds | Keys `occurred_at` and `published_at` both present. |
| `test_evidence_clock_mismatch_count` | CT-13 | Read-only count on packaged enterprise DB | `evidence_events` where `arrival_time != event_time` is 11,985. |
| `test_partner_feed_clock_mismatch_count` | CT-14 | Read-only count on packaged `partner_feeds` | Rows where `ingest_ts != source_ts` is 7,471. |
| `test_reference_version_overlap_count` | CT-15 | Overlapping `reference_versions` pairs on the same `ref_key` | 45. |
| `test_consume_source_messages_returns_list` | (CW-10 thin test) | `consume_source_messages(3)` on a copy | A list. Length at most 3. |
| `test_packaged_source_messages_count` | (Phase 0 inventory) | Read-only count | 15. |

Worked example for `test_apply_rejects_missing_required_fields`. Half B sets `LEGACY_DB` to a temp file that already has the `wafer_lots` table and one lot. It calls `apply` with `{'message_id': 'bad'}`. The current function adds 1 to `invalid`. The test asserts that number.

How to build the gateway JSON without starting port 8090: import the handler or copy the record-building lines from `services/source_gateway/server.py` into the test as a call of a small helper that Half B extracts without changing the response keys. Live HTTP, if started, is extra. The key lock is both clock fields present.

---

## Reconciliation — write before slice 2

Module: `tests/characterization/test_char_reconciliation.py`.

Current function: `partner_feeds.reconcile`.

| Test function | Phase 1 id | Behaviour it locks | Expected |
|---|---|---|---|
| `test_packaged_replay_count_before_reconcile` | CT-06 | Copy of packaged `partner_feeds`, before `reconcile` | `processing_status = 'REPLAY'` count is 67. |
| `test_packaged_new_and_retry_counts` | (baseline-behaviour) | Same copy, before `reconcile` | NEW 8,000. RETRY 500. |
| `test_reconcile_replay_becomes_duplicate` | CT-07 | `reconcile()` on that copy | Those REPLAY ids become DUPLICATE. Reason `replayed source message`. Count 67 if the default limit reaches them all. If the default limit of 1,000 leaves some REPLAY rows unprocessed, the test records the actual flipped count and the remaining REPLAY count. It does not invent a new reason. |
| `test_reconcile_unsupported_schema_rejected` | CT-08 | A NEW row with `schema_rev = 'unsupported'` on a temp DB | Status REJECTED. Reason `schema/key validation`. |
| `test_reconcile_missing_business_key_rejected` | (gap fill from `reconcile`) | A NEW row whose `raw_json` has no `business_key` | Status REJECTED. Reason `schema/key validation`. |
| `test_reconcile_negative_quantity_rejected` | CT-09 | A NEW row with negative quantity | Status REJECTED. Reason `quantity out of range`. |
| `test_reconcile_valid_new_accepted` | (gap fill from `reconcile`) | A NEW row with a key, supported schema, quantity 0 or above | Status ACCEPTED. `error_reason` is None. |
| `test_reconcile_does_not_use_untrusted_note` | CT-31 | The 86 packaged feeds whose `raw_json` contains `auto approve` or `disregard validation` | After `reconcile` on a copy, each of those rows changes status only by the key, schema, replay, and quantity rules. The note text stays data. |
| `test_untrusted_feed_note_count` | CT-30 | Read-only count | 86. |
| `test_reconcile_does_not_delete_rows` | (AC-S7 / BR-02) | Row count of the copy before and after `reconcile` | Same count. |
| `test_reconcile_default_limit_is_1000` | (gap fill from signature) | Source of `reconcile` | Default `limit=1000`. The test may read the signature or call with no limit on a temp table of 1,001 NEW rows and assert 1,000 were updated. |

Worked example for CT-07. Half B copies `data/legacy.sqlite3`. Sets `LEGACY_DB` to the copy. Counts REPLAY = 67. Calls `reconcile()`. Asserts each of those `feed_id` values is DUPLICATE with reason `replayed source message`, or records how many the default limit left untouched. The packaged file is not the copy.

Untrusted-text counts that are not feed rows sit in the harness module: bundled lake events 150, archive `.eml` files 3, source documents 22. Those are CT-32, CT-33, CT-34.

---

## Rule evaluation — write before slice 3

Module: `tests/characterization/test_char_rule_evaluation.py`.

Current functions: `legacy_logic.priority`, `legacy_logic.manual_review_required`, `legacy_batch.shift_reconciliation.run`, `legacy_js` `threshold` and `legacyAllows`, Java `ReconcileLegacy`.

The 50,000 branch locks current Python output. The test label says PROPOSED. The test does not treat 50,000 as live policy.

The 999,999 default locks current JavaScript output. The test label says deviation. The test does not treat 999,999 as live policy.

| Test function | Phase 1 id | Behaviour it locks | Expected |
|---|---|---|---|
| `test_priority_closed_is_archive` | CT-02 | `priority('CLOSED', 'LOW', 99999)` | `archive` |
| `test_priority_critical_open_is_urgent` | CT-03 | `priority('OPEN', 'CRITICAL', 1)` | `urgent` |
| `test_priority_amount_above_50000_is_urgent` | CT-04 | `priority('OPEN', 'LOW', 50001)` | `urgent`. Label: current Python deviation. 50,000 stays PROPOSED. |
| `test_priority_high_is_review` | (gap fill from `priority`) | `priority('OPEN', 'HIGH', 1)` | `review` |
| `test_priority_escalated_is_review` | (gap fill from `priority`) | `priority('ESCALATED', 'LOW', 1)` | `review` |
| `test_priority_other_is_queue` | (gap fill from `priority`) | `priority('OPEN', 'LOW', 1)` | `queue` |
| `test_packaged_amount_above_50000_count` | CT-05 | Read-only count on packaged cases | 0 |
| `test_manual_review_required_true_cases` | (baseline-behaviour) | HIGH, CRITICAL, ESCALATED, REOPENED | True |
| `test_manual_review_required_false_for_open_low` | (baseline-behaviour) | status OPEN, severity LOW | False |
| `test_night_batch_review_object_in_flagged` | CT-17 | `run` on a copy or fixture with a known REVIEW object | That `object_id` is in `flagged` |
| `test_night_batch_hold_object_in_flagged` | (BO-06a / code) | A HOLD object on that copy | That `object_id` is in `flagged` |
| `test_night_batch_flags_review_as_open` | CT-25 | Night-batch status list in the flag test | REVIEW is in `('HOLD', 'REVIEW')`. BO-06a match. The test does not rewrite the file. |
| `test_night_batch_default_limit_500` | (gap fill from signature) | `run` default | `limit=500` |
| `test_operational_review_count` | CT-18 | Read-only count | 2,090 |
| `test_js_allows_26250_apac_2026` | CT-19 | `legacyAllows(26250, 'APAC', 2026)` | true, because 25,000 * 1.05 = 26,250 |
| `test_js_allows_27000_apac_2026` | (file main block) | `legacyAllows(27000, 'APAC', 2026)` | false |
| `test_js_threshold_apac_2026` | (archive) | `threshold('APAC', 2026)` | 25,000 |
| `test_js_threshold_apac_1999_is_999999` | CT-20 | `threshold('APAC', 1999)` | 999999. Label: current deviation. Not live policy. |
| `test_java_skips_blank_amount_cell` | CT-21 | Parser on a CSV line with a blank field index 4 | That line is omitted from count |
| `test_vendor_blank_amount_count` | CT-22 | Read-only count on a copy of vendor rows | 10 |
| `test_cases_status_values` | CT-23 | Distinct `cases.status` | CLOSED, ESCALATED, OPEN, REOPENED, UNDER_REVIEW |
| `test_operational_status_values` | CT-24 | Distinct `operational_objects.status` | CLOSED, ESCALATED, HOLD, OPEN, REOPENED, REVIEW |
| `test_active_policy_count` | CT-26 | Active `policy_register` count | 34 |
| `test_active_policy_count_per_region` | CT-27 | Active count per country code | AU 4, BR 4, DE 5, GB 4, IN 4, JP 4, US 5, ZA 4 |
| `test_cases_region_values` | CT-28 | Distinct `cases.region` | APAC, EMEA, AMER |
| `test_operational_region_values` | CT-29 | Distinct `operational_objects.region` | eight country codes |
| `test_recipe_mismatch_count` | CT-10 | `process_steps` joined to `fab_tools` where `recipe_version != recipe_rev` | 91 |
| `test_process_steps_count` | CT-11 | Count of `process_steps` | 125 |
| `test_unjoined_process_steps` | CT-12 | Process steps with no `fab_tools` row on `tool_id` | 0 |

New-function tests Half B adds in slice 3, after the table above is green:

| Test function | Behaviour it locks | Expected |
|---|---|---|
| `test_evaluate_live_policy_no_match_is_hold` | Archive has no row for that region and year | HOLD_FOR_REVIEW. Does not return 999,999. |
| `test_evaluate_live_policy_silent_urgent_cutoff_is_hold` | Archive is silent on an urgent amount cutoff | HOLD_FOR_REVIEW. Does not write 50,000 as decided. |
| `test_evaluate_live_policy_archive_apac_2026` | Archive match | Limit 25,000 USD from the archive row. Honesty REAL. |

Those three tests lock the approved live-policy path. They are not a rewrite of `priority()` or `threshold()`.

Worked example for CT-04. The current function returns `urgent` for `priority('OPEN', 'LOW', 50001)`. The test asserts that string. The docstring says the 50,000 cutoff stays PROPOSED. Live policy for a silent cutoff is HOLD_FOR_REVIEW, checked in `test_evaluate_live_policy_silent_urgent_cutoff_is_hold` after that function exists.

---

## Baseline parity — write before the first change

Module: `tests/characterization/test_char_baseline_parity.py`.

Current function: `app.baseline.baseline`.

| Test function | Phase 1 id | Behaviour it locks | Expected |
|---|---|---|---|
| `test_baseline_six_fields_exact_match` | CT-01 | `baseline()` on a copy of the packaged 125-case file | `records` 125, `open_cases` 89, `urgent_cases` 2, `mean_amount` 4982.61, `sites` 6, `hours_per_case` 0.603. Exact match. No tolerance percent. |
| `test_headline_kpis_remain_unknown` | CT-40 | The test body | Writes Unknown for exception cycle time. Writes Unknown for aged backlog. Does not invent a close-time field. Does not invent an age cutoff. Does not treat 89 as aged backlog. |

Formulas Half B must use, from `docs/04-baseline-kpis/measurement-methodology.md`:

- `records` = number of rows from `SELECT status, severity, amount, site FROM cases`.
- `open_cases` = count where `status != 'CLOSED'`.
- `urgent_cases` = count where `priority(status, severity, amount) == 'urgent'`.
- `mean_amount` = `statistics.fmean(amount)` rounded to 2 decimals.
- `sites` = number of distinct `site` values.
- `hours_per_case` = sum of `labor_hours` divided by sum of `total_cases` from `operating_costs`, rounded to 3 decimals.

---

## Harness safety — write before the first change

Module: `tests/characterization/test_char_harness_safety.py`.

| Test function | Phase 1 id | Behaviour it locks | Expected |
|---|---|---|---|
| `test_write_tests_set_temp_legacy_db` | CT-38 | The characterization write tests | Every write test sets `LEGACY_DB` to a temporary file. Half B can assert this by reading the module source or by checking `os.environ` inside those tests' `setUp`. |
| `test_packaged_db_hashes_unchanged` | CT-39 | Packaged `data/legacy.sqlite3` and `data/enterprise_legacy.sqlite3` after the suite | Hashes match the source register. |
| `test_get_cases_without_identity_returns_200` | CT-35 | Current server `GET /api/cases` with no identity header | HTTP 200. This records current behaviour. Identity on Application A is a later decision (FD-13). If the server is not started, assert from `app/server.py` that the handler skips an identity header, and label live HTTP Unknown. |
| `test_unassigned_workflow_tasks` | CT-36 | Read-only count | 695 rows with `assigned_to` IS NULL. |
| `test_incidents_body` | CT-37 | `GET /api/incidents` body, or the handler that builds it | Contains INC-2019-0082. Does not contain an owner for INC-2025-014. |
| `test_untrusted_bundled_lake_events` | CT-32 | Bundled lake events with `source_claim` | 150 |
| `test_untrusted_archive_eml` | CT-33 | Archive `.eml` files containing approve or ignore | 3 |
| `test_untrusted_source_documents` | CT-34 | Source documents whose body contains approve, ignore, or release all holds | 22 |

CT-35 records current 8080 behaviour. Application A and Application B are later phases and use the identity rule in `error-handling-spec.md`.

---

## Order Half B writes and runs

1. Harness safety and baseline parity.
2. Feed-intake module. Run it. Then slice 1 may add `intake_apply`.
3. Reconciliation module. Run it. Then slice 2 may add `reconcile_feeds`.
4. Rule-evaluation module on the old names. Run it. Then slice 3 may add `evaluate_live_policy` and the three live-policy tests.
5. After every cutover: baseline parity, harness hashes, and the old-name tests for slices already cut over.

---

## What Half B must not assert

A test does not assert a decided live cutoff of 50,000.

A test does not assert 999,999 as live policy.

A test does not assert a finance-closed or audit-closed merge.

A test does not assert an aged-backlog day number.

A test does not assert an exception-cycle-time hour number.

A test does not call `python -m app.generate --reset`.

---

## What this file does not do

This file does not include test source. It does not run `unittest`. It does not edit the inherited repo. It does not start Half B.
