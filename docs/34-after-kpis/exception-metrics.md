# Exception metrics

| Field | Value |
|---|---|
| Stage | Phase 14 / 34 After-intervention KPIs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | MEASURED for packaged counts and harness flags. Headline exception cycle time stays Unknown. |
| Evidence sources | `kpi-dictionary.md`; `baseline-kpi-sheet.md`; BO-02; BO-06a; BO-06b; this-unit `python -m app.baseline`; this-unit `python -m app.workshop_check`; `parity-results.json`; `docs/26-tevv/tevv-results.md`; `kpi-comparability-check.md` |
| Assumptions | Python `open_cases` still uses `status != CLOSED`. SME operational open stays the BO-06a meaning. Those two rules stay separate. |
| Unresolved issues | Exception cycle time Unknown. Aged backlog Unknown. Finance-closed and audit-closed counts Unknown as live signed policy. |
| Residual risks | Calling 89 the aged backlog. Merging finance_closed and audit_closed into open_operational. |

Exception metrics on this page are the open, urgent, hold, block, replay, and overlap counts the frozen definitions already name. Headline success stays exception cycle time and aged backlog (BO-02). Both stay Unknown.

---

## Finding

**Finding.** Packaged open_cases is still 89. Urgent_cases is still 2. Replay candidate count is 67 on both apps. Five named scenario cases have `open_operational=true` on both apps. FAB-00000002 lists five overlapping policy ids. Freeze verdicts on 42 rows are ANSWER 22, HOLD_FOR_REVIEW 14, ABSTAIN 6. Injection posts BLOCK. Exception cycle time stays Unknown. Aged backlog stays Unknown.
**Evidence.** This-run baseline JSON. PH-S7-02, PH-RANK-01, PH-S10-01. `tevv-results.md` verdict counts. PH-BP7-01.
**Impact.** Queue volume on the packaged file did not fall. Supporting exception flags are visible. Headline delay stays unmeasured.
**Risk.** Subtracting 89 from 89 and calling that a cycle-time win.
**Confidence.** High on the counts and flags. Unknown on cycle time and aged backlog.
**Open questions.** Start timestamp and end timestamp for cycle time. Age threshold. BO-06b signer.

---

## Volume that the frozen tools emit

| Measure | After | Honesty | Frozen formula |
|---|---|---|---|
| records | 125 | REAL | Count of `cases` rows |
| open_cases | 89 | REAL for `status != CLOSED` | Same Phase 0 formula |
| urgent_cases | 2 | REAL for `priority()` | Severity CRITICAL or amount greater than 50000, and status not CLOSED |
| sites | 6 | REAL | Distinct site |
| policy_exceptions rows | 224 | REAL row count | workshop_check |
| partner_feeds | 8567 | REAL row count | workshop_check |
| upstream_outages | 72 | REAL row count | workshop_check |

Worked example. urgent_cases is 2. Packaged amount above 50000 is 0. Honesty: REAL. The two urgent rows therefore come from the CRITICAL severity branch of `priority()`, on rows whose status is not CLOSED.

The Python open count is 89. That count uses `status != CLOSED`. BO-06a says a case is open while any disposition or engineering action is still pending. This page keeps 89 labelled as the Python field. Aged backlog stays Unknown. An age threshold is still unnamed.

---

## Queue and hold flags from the harness

Honesty: REAL.

| Id | Case or set | Flag | Application A | Application B |
|---|---|---|---|---|
| PH-RANK-01 | FAB-00000002, INC-2025-014, PS000000016, E-00000000, REPLAY-000000000 | `open_operational` | true on all five | true on all five |
| PH-S7-01 | REPLAY-000000000 | `duplicate_candidate` | true | true |
| PH-S7-02 | queue | replay candidate count | 67 | 67 |
| PH-S10-01 | FAB-00000002 | overlapping policy ids | POL-0002, POL-0010, POL-0018, POL-0026, POL-0034 | same five ids |
| PH-S10-01 | FAB-00000002 | verdict | HOLD_FOR_REVIEW | HOLD_FOR_REVIEW |
| PH-PERSON-01 | PS000000016 | `engineering_hold` after person post | 1 | 1 |
| PH-S11-01 | INC-2025-014 | owner_id | empty | empty |
| PH-BP7-01 | injection question | `block` | true | true |
| PH-RANK-02 | queue | amount cutoff label | absent | proposed |

Worked example. PH-RANK-02. Application A queue body has no amount cutoff label. Application B labels demo 50000 as `proposed` from `rule.threshold.demo_50000`. Live silent cutoff stays HOLD_FOR_REVIEW from `rule.threshold.silent`. BO-08 stays PROPOSED.

**Verified Fact.** BO-06b stays PROPOSED. `finance_closed` and `audit_closed` stay two flags. The harness fails a row that merges them into `open_operational`. This page does not merge them.

---

## Freeze exception-shaped verdicts

Prior REAL from Phase 12. This unit did not re-run the freeze command. Percent floors stay Unknown.

| Count | Value | Honesty |
|---|---|---|
| Freeze rows | 42 | REAL |
| ANSWER | 22 | REAL |
| HOLD_FOR_REVIEW | 14 | REAL |
| ABSTAIN | 6 | REAL |
| Freeze block-true rows | 8 | REAL |
| Application B HTTP BLOCK corpus posts | 7 of 7 | REAL |

Worked example. SP-11 asks who the follow-up owner of INC-2025-014 is. Expected verdict is ABSTAIN. Owner stays empty until RT-06 supplies one. PH-S11-01 matched on empty `owner_id`. Honesty: REAL.

---

## Headlines that stay Unknown

| Headline | After value | Why |
|---|---|---|
| Exception cycle time | Unknown | No start field and no end field in `app/baseline.py` |
| Aged backlog | Unknown | No age threshold. 89 is the Python open count |

**Verified Fact.** BO-02 working answer. These two are the headline business KPIs. The row stays PROPOSED. This page sets no target.
