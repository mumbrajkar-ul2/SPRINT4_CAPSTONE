# Transformation backlog

| Field | Value |
|---|---|
| Stage | Phase 7 / 14 Transformation plan. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Documents only. No tests written. Inherited repo not edited. |
| Evidence sources | FD-12; `docs/07-repo-assessment/characterization-test-plan.md`; `docs/07-repo-assessment/baseline-behaviour.md`; `docs/07-repo-assessment/critical-workflow-inventory.md`; `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `docs/12-specs/business-rules.md`; `docs/12-specs/system-spec.md`; `docs/12-specs/acceptance-criteria.md`; `app/partner_feeds.py`; `app/gateway_bridge.py`; `app/legacy_logic.py`; `legacy_js/legacy_policy.js`; `legacy_java/ReconcileLegacy.java`; `legacy_batch/shift_reconciliation.py` |
| Assumptions | Half B runs after HALF_A_ACCEPTED. Tests use a copy or a temporary database. Packaged SQLite files stay read-only. |
| Unresolved issues | Node and Java availability on the Half B machine stay Unknown. Live HTTP on ports 8080 and 8090 stay Unknown until Half B starts those listeners or calls the handler functions. BO-06b and BO-08 stay PROPOSED. Exception cycle time and aged backlog stay Unknown. |
| Residual risks | Writing the packaged `data/legacy.sqlite3` or `data/enterprise_legacy.sqlite3` would move the freeze. Compiling 50,000 or 999,999 as live policy would treat a PROPOSED row as signed code. |

This file lists the Half B work in the locked order. It does not change a function.

**Verified Fact.** FD-12 DECIDED 2026-10-18, authority: team-force. Order: feed intake first, then reconciliation, then rule evaluation. Characterization tests lock current behaviour before each slice changes.

---

## Finding

**Finding.** Fifteen backlog items cover the tests, the three slices, the shadow runs, the baseline check, and the write-up. No item invents a policy number.
**Evidence.** FD-12. Phase 1 characterization checks CT-01 to CT-40. Phase 0 six-field tool output. Phase 6 BR-05, BR-07, BR-11.
**Impact.** Half B can open this list and write tests and slices without inventing a rule.
**Risk.** Starting slice 2 before the feed-intake tests pass would hide an intake miss inside a later reconcile change.
**Confidence.** High on the order and the six-field target. Unknown on Node and Java on the Half B machine.
**Open questions.** Whether Half B starts the HTTP listeners or calls the handler functions.

---

## How to read an item

Each item is one Half B job. Status in this file is PLANNED. Half B records done or blocked in `docs/15-modernization/transformation-log.md` after acceptance.

A **slice** is one of the three workflows. The old function stays in the tree. Callers move to the new function after the tests and the shadow run match. The playbook calls this a strangle.

Honesty on packaged counts in this file is REAL.

---

## Shared rules for every item

**Verified Fact.** Phase 0 `python -m app.baseline` twice: `records` 125, `open_cases` 89, `urgent_cases` 2, `mean_amount` 4982.61, `sites` 6, `hours_per_case` 0.603.

Parity on those six fields is exact match. This plan does not invent a tolerance percent. Exact match can hold because none of the three slices writes `cases` or `operating_costs`.

Exception cycle time stays Unknown. Aged backlog stays Unknown. Those two are not in the parity set.

**Verified Fact.** BO-06a DECIDED. REVIEW and HOLD are open. The night-batch file flags HOLD and REVIEW. Its comment says it treats REVIEW as open.

**Verified Fact.** BO-06b stays PROPOSED. Operational closed, finance booked, and audit closed stay three states. A mismatch routes to HOLD_FOR_REVIEW. This backlog does not write a merge into code.

**Verified Fact.** BO-08 stays PROPOSED. When the archive is silent, live policy is HOLD_FOR_REVIEW. The Python 50,000 cutoff stays PROPOSED. This backlog does not write 999,999 as live policy.

Undefined policy cases route to HOLD_FOR_REVIEW.

---

## Slice 0 — lock current behaviour (before any slice)

### TB-01 Write feed-intake characterization tests

| Field | Value |
|---|---|
| Slice | Feed intake. Before TB-05. |
| Files Half B writes | `tests/characterization/test_char_feed_intake.py` |
| Locks | Current `gateway_bridge.apply()`, current gateway event JSON clocks, current two-clock counts, current source-message list. Named tests in `characterization-test-plan.md` section FI. |
| Finding | Current tests do not lock the packaged inbox row, the required-field list, or the two clock keys on the gateway JSON. |
| Evidence | `docs/07-repo-assessment/characterization-test-plan.md` CT-13 to CT-16. `tests/test_source_gateway.py` can write the packaged database. |
| Impact | Slice 1 can change intake after these tests pass. |
| Risk | Calling `apply()` on the default `LEGACY_DB` writes `gateway_inbox`. |
| Confidence | High |
| Open questions | Whether Half B starts port 8090 or builds the event JSON from the handler function. |
| Pass when | Every FI test is green on a copy. Packaged hashes match the source register. |

### TB-02 Write reconciliation characterization tests

| Field | Value |
|---|---|
| Slice | Reconciliation. Before TB-08. |
| Files Half B writes | `tests/characterization/test_char_reconciliation.py` |
| Locks | Current `reconcile()` status machine and the packaged NEW / RETRY / REPLAY counts. Named tests in section RC. |
| Finding | `reconcile()` has not been run on the packaged store. Packaged rows stay NEW 8,000, RETRY 500, REPLAY 67. |
| Evidence | `app/partner_feeds.py` `reconcile()`. Phase 1 CT-06 to CT-09, CT-30, CT-31. Catalogue BP2. |
| Impact | Slice 2 can change reconcile after these tests pass on a copy. |
| Risk | Running `reconcile()` on the packaged file flips the 67 REPLAY rows. |
| Confidence | High |
| Open questions | None for the four status rules. They are in the function. |

### TB-03 Write rule-evaluation characterization tests

| Field | Value |
|---|---|
| Slice | Rule evaluation. Before TB-11. |
| Files Half B writes | `tests/characterization/test_char_rule_evaluation.py` |
| Locks | Current `priority()`, current `manual_review_required`, current night-batch flag set, current JavaScript allow arithmetic, current Java skip rules, current status-word lists, current policy counts. Named tests in section RE. |
| Finding | Four programs disagree. Python uses 50,000. JavaScript uses archive limit times 1.05 and returns 999,999 when no row matches. Night batch flags HOLD and REVIEW. Java skips a blank amount cell. |
| Evidence | The four rule files. Phase 1 CT-02 to CT-05, CT-17 to CT-29. BR-15. |
| Impact | Slice 3 can wrap the four programs after these tests pass. |
| Risk | Treating 50,000 or 999,999 as live policy in the new path. |
| Confidence | High on the documented outputs. Unknown on live Node and Java. |
| Open questions | Node and `javac` on the Half B machine. |

### TB-04 Write baseline-parity and harness-safety tests

| Field | Value |
|---|---|
| Slice | Every slice. Run before the first change and after every cutover. |
| Files Half B writes | `tests/characterization/test_char_baseline_parity.py`; `tests/characterization/test_char_harness_safety.py` |
| Locks | The six Phase 0 fields. Packaged hashes. Temporary `LEGACY_DB` on every write test. Headline KPIs stay Unknown. |
| Finding | Phase 0 matched twice on those six fields. `app/baseline.py` has no exception-cycle-time field and no aged-backlog field. |
| Evidence | `docs/04-baseline-kpis/baseline-kpi-sheet.md`. CT-01, CT-38, CT-39, CT-40. |
| Impact | A slice that moves a case count fails this test. |
| Risk | Calling 89 the aged backlog. |
| Confidence | High |
| Open questions | None for the six fields. |

---

## Slice 1 — feed intake

### TB-05 Shadow-run feed intake

| Field | Value |
|---|---|
| Depends on | TB-01 green. |
| Finding | Current `apply()` writes `received_at` from the clock at insert time. Two runs on the same event can differ on that one column. |
| Evidence | `app/gateway_bridge.py` insert uses `datetime.datetime.now(datetime.timezone.utc).isoformat()`. |
| Impact | Shadow compare uses the field list in `transformation-gates.md` SH-FI. `received_at` is omitted. That omit is PROPOSED, owner Team-Force. It is not applied in code in this half. |
| Risk | Comparing `received_at` and calling the miss a behaviour change. |
| Confidence | High that the other inbox columns can match. |
| Open questions | None for the required-field list. |
| Pass when | Current `apply()` and the new intake function return the same `accepted`, `duplicates`, `invalid`, and `received` counts on the same event list. Inbox rows match on `message_id`, `external_ref`, `source_system`, `event_type`, `event_time`, `status`. |

### TB-06 Add the new intake function beside the current one

| Field | Value |
|---|---|
| Depends on | TB-05 recorded. |
| What changes | A new function sits beside `gateway_bridge.apply`. The current function body stays. Characterization tests keep calling `apply`. |
| Approved difference | None on this slice. Intake outputs stay the current counts. |
| Finding | Feed intake is the first FD-12 slice because later reconcile reads rows that intake stored. |
| Evidence | FD-12. CW-08, CW-09, CW-10. |
| Impact | Callers can move after TB-07. |
| Risk | Editing `apply` in place would break the characterization tests that call it by name. |
| Confidence | High |
| Open questions | New function name is an engineering choice for Half B inside the names in `migration-roadmap.md`. |

### TB-07 Cut over intake callers

| Field | Value |
|---|---|
| Depends on | TB-06. TB-04 still green. |
| What changes | The CLI and any intake caller import the new function. |
| Finding | Current CLI is `python -m app.gateway_bridge`. |
| Evidence | `app/gateway_bridge.py` `main()`. |
| Impact | New messages enter through the new function. |
| Risk | Leaving a second caller on `apply` would split intake. |
| Confidence | High |
| Open questions | Compose bridge command line. Unknown whether Compose runs on this laptop. |

---

## Slice 2 — reconciliation

### TB-08 Shadow-run reconciliation

| Field | Value |
|---|---|
| Depends on | TB-02 green. TB-07 done or rolled back. Intake tests still green. |
| Finding | Current `reconcile()` updates `processing_status` and `error_reason` on NEW, RETRY, and REPLAY rows, default `limit=1000`, order `ingest_ts, feed_id`. |
| Evidence | `app/partner_feeds.py` lines of `reconcile()`. |
| Impact | Two copies of the packaged feeds, same limit. Compare counts and per-`feed_id` status and reason. Exact match can hold. |
| Risk | Running on the packaged file. |
| Confidence | High |
| Open questions | None for the four status rules. |
| Pass when | `accepted`, `rejected`, `duplicate`, `skipped` match. Every compared `feed_id` has the same `processing_status` and `error_reason`. |

### TB-09 Add the new reconcile function beside the current one

| Field | Value |
|---|---|
| Depends on | TB-08 recorded. |
| What changes | A new function sits beside `reconcile`. The current function body stays. Characterization tests keep calling `reconcile`. |
| Approved difference | None on the status machine. A REPLAY row still becomes DUPLICATE with reason `replayed source message`. The job does not delete a row. Drop of a duplicate still waits for a person at RT-05 in later application work. Phase 7 does not add a delete. Untrusted note text stays data. |
| Finding | 67 REPLAY rows. Honesty: REAL. `reconcile()` is written to mark them DUPLICATE. |
| Evidence | CT-06, CT-07. BR-02. AC-S7. |
| Impact | Queue size stops treating a replay as new work once the job runs on a copy. |
| Risk | Using text similarity as the duplicate test. |
| Confidence | High |
| Open questions | `reconcile()` has not been run on the packaged store. |

### TB-10 Cut over reconcile callers

| Field | Value |
|---|---|
| Depends on | TB-09. TB-04 still green. |
| What changes | `python -m app.partner_feeds --reconcile` calls the new function. |
| Finding | Current `main()` calls `reconcile()` when `--reconcile` is set. |
| Evidence | `app/partner_feeds.py` `main()`. |
| Impact | Month-end staff who run that command hit the new function. |
| Risk | A generate reset after cutover would replace the packaged feeds. Half B does not pass `--reset`. |
| Confidence | High |
| Open questions | None for the command flag. |

---

## Slice 3 — rule evaluation

### TB-11 Shadow-run rule evaluation

| Field | Value |
|---|---|
| Depends on | TB-03 green. TB-10 done or rolled back. Earlier characterization still green. |
| Finding | Four programs. Python `priority()` on each packaged case. Night batch on a copy with a named limit. JavaScript `(amount, region, year)` triples already named in Phase 1. Java on a fixture CSV that includes a blank amount cell. |
| Evidence | The four rule files. CT-02 to CT-05, CT-17 to CT-22. |
| Impact | Compare the named outputs in `transformation-gates.md` SH-RE. |
| Risk | Calling the JavaScript 999,999 default a live policy miss. That default is a recorded deviation. The new live-policy path routes no-match to HOLD_FOR_REVIEW. |
| Confidence | High on Python and night batch. Unknown on live Node and Java. |
| Open questions | Node and `javac`. |
| Pass when | Every packaged case has the same `priority()` string on the old function. Night-batch `processed`, `by_tenant`, and the flagged `object_id` set match on the same copy and limit. JavaScript and Java old-function outputs match the Phase 1 expected values. The new live-policy path is compared separately and any HOLD_FOR_REVIEW difference is named. |

### TB-12 Add the new rule functions beside the current ones

| Field | Value |
|---|---|
| Depends on | TB-11 recorded. |
| What changes | New functions sit beside `priority`, `legacyAllows`, `ReconcileLegacy`, and `shift_reconciliation.run`. Current bodies stay. Characterization tests keep calling the current names. A new live-policy function is added. When the archive is silent, or no archive row matches, that function returns HOLD_FOR_REVIEW. |
| Approved difference | Live policy on silence or no-match is HOLD_FOR_REVIEW. The new path does not return 999,999 as a live limit. The new path does not write 50,000 as decided live policy. The current `priority()` 50,000 branch stays as a recorded Python deviation, labelled PROPOSED. |
| Finding | Archive is canonical. 2026 APAC limit is 25,000 USD. Honesty: REAL. JavaScript no-match default is 999,999. BR-05 and BR-11. |
| Evidence | `legacy_js/legacy_policy.js`. `docs/12-specs/business-rules.md` BR-04, BR-05, BR-11. |
| Impact | Scenario 12 can show the deviation and the live-policy wait. |
| Risk | Copying the 1.05 line into the live-policy function. |
| Confidence | High |
| Open questions | Signer of BO-08. Owner: Business Owner. |

### TB-13 Cut over rule-evaluation callers

| Field | Value |
|---|---|
| Depends on | TB-12. TB-04 still green. |
| What changes | `GET /api/cases` still ranks with the current `priority()` deviation until a later approved change says otherwise. Live-policy questions use the new function. Night-batch CLI can call the new wrapper that still flags HOLD and REVIEW. |
| Finding | `GET /api/cases` adds `priority()` today. Two packaged urgent cases are the two CRITICAL rows. Zero packaged cases have `amount > 50000`. Honesty: REAL. |
| Evidence | `app/server.py` via Phase 1 baseline-behaviour. CT-01, CT-05. |
| Impact | The six-field baseline stays the same if `priority()` is unchanged. |
| Risk | Replacing `priority()` in place with HOLD_FOR_REVIEW on the 50,000 branch would still leave `urgent_cases` at 2 on this fixture, and would still be an approved-change write-up. This plan prefers leaving `priority()` in place. |
| Confidence | High on the packaged urgent count. |
| Open questions | Whether a later phase replaces ranking. Not this unit. |

---

## Close the phase

### TB-14 Record before-and-after and explain every difference

| Field | Value |
|---|---|
| Depends on | TB-07, TB-10, TB-13, or a recorded rollback of a slice. |
| Files Half B writes | `docs/15-modernization/transformation-log.md`; `changed-components.md`; `behavior-preservation-evidence.md`; `approved-behavior-changes.md`; `test-execution-log.md`; `docs/16-repo-validation/behavior-difference-report.md` |
| Finding | Phase 7 is the first phase that may change application behaviour. Phases 0 to 6 changed no application behaviour. |
| Evidence | Phase 7 locked facts. |
| Impact | A reviewer can see each difference marked preserved or approved. |
| Risk | An unexplained difference. |
| Confidence | High |
| Open questions | None for the six-field exact match. |

### TB-15 Validate against the Phase 0 baseline

| Field | Value |
|---|---|
| Depends on | TB-14. |
| Commands | From the inherited root, on a copy that still holds the packaged cases: `python -m app.baseline` twice. Diff the JSON. |
| Finding | Phase 0 both runs printed the same six fields. |
| Evidence | `docs/04-baseline-kpis/baseline-kpi-sheet.md`. |
| Impact | Gate TG-08 in `transformation-gates.md`. |
| Risk | Running `python -m app.generate --reset` before the check. |
| Confidence | High |
| Open questions | None. |
| Pass when | The six fields match exactly. Exception cycle time is still Unknown. Aged backlog is still Unknown. Every behaviour difference has a row. |

---

## Items this backlog does not include

This backlog does not build Application A or Application B. Those are later phases.

This backlog does not invent an aged-backlog day cutoff.

This backlog does not invent a cycle-time start field or end field.

This backlog does not write BO-06b or BO-08 as signed code.

This backlog does not add a delete of a REPLAY row.

---

## What this file does not do

This file does not write test source. It does not edit the inherited repo. It does not start Half B.
