# Transformation gates

| Field | Value |
|---|---|
| Stage | Phase 7 / 14 Transformation plan. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Documents only. No tests written. Inherited repo not edited. |
| Evidence sources | FD-12; Phase 7 locked facts; `docs/04-baseline-kpis/baseline-kpi-sheet.md`; `docs/04-baseline-kpis/kpi-dictionary.md`; `docs/07-repo-assessment/characterization-test-plan.md`; `docs/12-specs/business-rules.md`; `docs/12-specs/acceptance-criteria.md`; `app/baseline.py`; `app/gateway_bridge.py` |
| Assumptions | Half B records each gate in `docs/15-modernization/test-execution-log.md` and `docs/16-repo-validation/repo-quality-gate.md`. |
| Unresolved issues | Exception cycle time stays Unknown. Aged backlog stays Unknown. Node and Java availability stay Unknown. |
| Residual risks | A behaviour change that is not in the shadow field list. A live-policy number compiled as decided. |

This file names the checks that catch a slipped behaviour change. It does not change a function.

---

## Finding

**Finding.** Nine gates cover Half A acceptance, the characterization suite, each slice shadow run, each slice cutover, the six-field exact match, and the difference report.
**Evidence.** Phase 7 completion gate. Phase 0 two matching `app.baseline` runs. FD-12.
**Impact.** Half B stops at the first failed gate. The reviewer reads the gate id.
**Risk.** Comparing only the six fields and skipping per-`feed_id` status would miss a reconcile change that leaves `cases` alone.
**Confidence.** High on the six-field exact match. Unknown on live Node and Java.
**Open questions.** Node and `javac`.

---

## Parity target

**Verified Fact.** Phase 0, both runs, honesty REAL for the tool output:

```text
{"records": 125, "open_cases": 89, "urgent_cases": 2, "mean_amount": 4982.61, "sites": 6, "hours_per_case": 0.603}
```

**Parity rule.** Exact match on those six fields. This plan does not invent a tolerance percent.

Exact match can hold. The six fields come from `cases` and `operating_costs`. Feed intake writes `gateway_inbox`. Reconciliation writes `partner_feeds`. Night batch does not write `operational_objects` in the current `run()`. `priority()` is computed on read. None of those writes change the six fields when `priority()` stays the current function.

The six-field rule stays exact match.

Exception cycle time is Unknown. Aged backlog is Unknown. Phase 7 pass checks are the six fields and the named shadow lists. A later modelled headline number is SIMULATED.

**Verified Fact.** `open_cases` 89 is `status != CLOSED` in `app/baseline.py`. The parity field stays that Python tool field. BO-06a is the operational meaning of open: REVIEW and HOLD are open.

---

## Shadow-run comparison design

Engineering decision ED-P7A-03, authority: team-force. Each slice has a named field list. Half B compares those fields and no others as pass/fail.

Engineering decision ED-P7A-04, authority: team-force. Inbox `received_at` is omitted from SH-FI equality. Current `apply()` writes the clock at insert time. Two runs on the same event write different clock strings. The omit is PROPOSED. Owner: Team-Force. This half leaves the omit as a plan note.

Engineering decision ED-P7A-06, authority: team-force. The six-field check is `python -m app.baseline` on a copy of the packaged cases. Compare the JSON field by field. Run twice. Both runs must match each other and match Phase 0.

### SH-FI Feed intake

| Compared item | Rule | Why |
|---|---|---|
| `accepted`, `duplicates`, `invalid`, `received` | Exact match | Current `apply()` return keys. |
| Inbox `message_id`, `external_ref`, `source_system`, `event_type`, `event_time`, `status` | Exact match | Written columns that do not use the wall clock. |
| Inbox `received_at` | Omit. PROPOSED, owner Team-Force | Current insert uses `datetime.now`. |
| Inbox `raw_payload` | Exact match after `json.dumps(e, sort_keys=True)` | Current insert. |

Fixture: the same event list. Include one missing-field event, one unknown `lot_id`, one new valid event, then the same `message_id` again.

### SH-RC Reconciliation

| Compared item | Rule | Why |
|---|---|---|
| `accepted`, `rejected`, `duplicate`, `skipped` | Exact match | Current `reconcile()` return keys. |
| Each compared `feed_id` `processing_status` | Exact match | The four status rules. |
| Each compared `feed_id` `error_reason` | Exact match | Reasons in the function. |
| Row count of the copy | Exact match | The job does not delete. |

Fixture: two copies of packaged `partner_feeds`. Same `limit`. Default 1,000 unless the test names another limit. Order stays `ingest_ts, feed_id`.

### SH-RE Rule evaluation

| Compared item | Rule | Why |
|---|---|---|
| `priority(status, severity, amount)` on every packaged case | Exact match on the old function | Ranking deviation. |
| `manual_review_required` on every packaged case | Exact match on the old function | Current helper. |
| Night batch `processed`, `by_tenant`, flagged `object_id` set | Exact match on the same copy and the same limit | Current `run()`. Compare the full flagged set, not only `flagged_preview` of 12. |
| JS `threshold('APAC', 2026)` | 25,000 on the old function | Archive row. Honesty REAL. |
| JS `legacyAllows(26250, 'APAC', 2026)` | true on the old function | 25,000 * 1.05 = 26,250. |
| JS `legacyAllows(27000, 'APAC', 2026)` | false on the old function | File main block. |
| JS `threshold('APAC', 1999)` | 999,999 on the old function | Current default. Deviation. Not live policy. |
| `evaluate_live_policy` on APAC 1999 | HOLD_FOR_REVIEW on the new function | Approved difference. BR-05. |
| Java count and total on the named CSV fixture | Exact match on the old program or the documented skip rules | Blank amount cell is omitted. |

---

## Gate list

| Id | When | Pass | Fail / stop |
|---|---|---|---|
| TG-00 | Before Half B | Reviewer returns HALF_A_ACCEPTED | Half B does not start |
| TG-01 | After TB-01 to TB-04 | Every named characterization test is green on current functions. Packaged hashes match | Do not add a new function |
| TG-02 | After SH-FI | SH-FI counts and inbox columns match. `received_at` omitted as PROPOSED | Do not cut over intake |
| TG-03 | After intake cutover | FI tests still green on `apply`. Six-field exact match. Hashes match | Roll back intake |
| TG-04 | After SH-RC | SH-RC counts and per-`feed_id` status and reason match | Do not cut over reconcile |
| TG-05 | After reconcile cutover | RC tests still green on `reconcile`. Six-field exact match. Hashes match | Roll back reconcile |
| TG-06 | After SH-RE | Old-function outputs match. Live-policy silence and no-match return HOLD_FOR_REVIEW. Any other difference has a named source | Do not cut over rule evaluation |
| TG-07 | After rule cutover | RE tests still green on old names. Six-field exact match. Hashes match | Roll back rule evaluation |
| TG-08 | End of Half B | Six-field exact match twice. Every behaviour difference has a preserved or approved row. Headline KPIs still Unknown | BLOCKED |

---

## Risk that a behaviour change slips through, and the gate that catches it

| Slipped change | How it would show | Gate |
|---|---|---|
| Intake drops `occurred_at` | Gateway JSON test FI-16 fails, or inbox `event_time` empty | TG-01, TG-02 |
| Intake accepts an unknown lot | SH-FI `invalid` count drops | TG-02 |
| Reconcile uses note text | A row in the 86 untrusted feeds changes status for a reason other than the four rules | TG-04, RC-31 |
| Reconcile deletes a REPLAY row | Copy row count drops | TG-04 |
| Reconcile marks REPLAY as ACCEPTED | `duplicate` count drops. CT-07 fails | TG-01, TG-04 |
| `priority()` stops treating CRITICAL as urgent | `urgent_cases` becomes 0 | TG-08, BP-01 |
| `priority()` treats CLOSED as urgent | `urgent_cases` rises or `open_cases` pairing changes | TG-08 |
| Night batch stops flagging REVIEW | Known REVIEW object leaves the flagged set | TG-06, RE-17 |
| Live policy uses 999,999 | `evaluate_live_policy` on APAC 1999 returns a number | TG-06 |
| Live policy uses 50,000 as decided | New function stores 50,000 as the live cutoff | TG-06, TG-08 write-up |
| Finance-closed merged into operational-closed | A new closed test appears without a BO-06b signature | TG-08 difference report |
| Aged-backlog cutoff invented | A test asserts a day number | TG-01 BP-40 |
| Packaged freeze written | Hash mismatch | TG-01, TG-03, TG-05, TG-07 |
| Six-field drift with no case-table write | `priority()` changed in place | TG-08 |

---

## Commands Half B records

Working directory: `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`.

Characterization suite: the five modules in ED-P7A-01. Use the inherited unittest runner or pytest if it already collects unittest. This plan does not invent a third runner.

Baseline:

```text
python -m app.baseline
```

Run twice. Diff the JSON. Every field must match Phase 0.

Do not pass `--reset` to generate.

---

## What this file does not do

This file does not write test source. It does not edit the inherited repo. It does not start Half B. It does not apply the `received_at` omit in code.
