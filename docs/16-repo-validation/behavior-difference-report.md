# Behaviour difference report

| Field | Value |
|---|---|
| Stage | Phase 7 / 16 Validate. Half B. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7b-doc-20261018-001 |
| Status | COMPLETE for this unit. Every listed difference is preserved or approved. |
| Evidence sources | Phase 0 baseline; Phase 7 SH-FI, SH-RC, SH-RE; `evaluate_live_policy` live calls; BR-05; BR-11 |
| Assumptions | A difference that only exists on the new live-policy function is the approved change named in Half A. |
| Unresolved issues | Exception cycle time stays Unknown. Aged backlog stays Unknown. Those are not differences against Phase 0. They were already Unknown. |
| Residual risks | An unexplained later change to `priority()` would move `urgent_cases` without a new approved row. |

This file lists every behaviour difference against the Phase 7 baseline. Each row is preserved or approved.

The Phase 7 baseline is the Phase 0 six-field tool output plus the current function outputs locked by the characterization tests.

---

## Finding

**Finding.** Intake, reconcile, night batch, and `priority()` match the locked current outputs. The only approved difference is `evaluate_live_policy` returning HOLD_FOR_REVIEW on silence or no archive match.
**Evidence.** Shadow numbers. Live policy calls. Suite 70 OK.
**Impact.** A reviewer can accept the live-policy wait without treating 999,999 or 50,000 as signed code.
**Risk.** Calling the default-limit `duplicate` of 7 a miss of the 67 REPLAY rows. That is current `reconcile()` with `limit=1000`.
**Confidence.** High
**Open questions.** BO-08 signer. Owner: Business Owner.

---

## Six-field baseline

| Field | Phase 0 | After Half B on a copy | Mark |
|---|---|---|---|
| records | 125 | 125 | Preserved |
| open_cases | 89 | 89 | Preserved |
| urgent_cases | 2 | 2 | Preserved |
| mean_amount | 4982.61 | 4982.61 | Preserved |
| sites | 6 | 6 | Preserved |
| hours_per_case | 0.603 | 0.603 | Preserved |

Exception cycle time: Unknown before and after. Not a difference.
Aged backlog: Unknown before and after. Not a difference.

---

## Feed intake

| Difference | Mark | Note |
|---|---|---|
| `accepted` / `duplicates` / `invalid` / `received` on the four-event list | Preserved | Both functions 1 / 1 / 2 / 4 |
| Inbox columns in SH-FI | Preserved | Exact match |
| Inbox `received_at` | Preserved, omitted from equality | Current insert uses the clock. Omit is PROPOSED, owner Team-Force |
| Required-field reject and unknown-lot reject | Preserved | `apply` tests still pass |

No approved intake change.

---

## Reconciliation

| Difference | Mark | Note |
|---|---|---|
| Status machine on NEW / RETRY / REPLAY | Preserved | Same four rules, same order |
| Default `limit=1000` counts | Preserved | 922 accepted, 71 rejected, 7 duplicate, 0 skipped |
| Per-`feed_id` status and reason | Preserved | Exact match on two copies |
| Row count 8,567 | Preserved | No delete |
| Untrusted notes | Preserved | Text stays data |
| REPLAY row with missing key or unsupported schema | Preserved | Becomes REJECTED first. Worked example: `REPLAY-000002921` |
| 59 REPLAY rows still REPLAY after default limit | Preserved | They were outside the first 1,000 pending rows |

No approved reconcile change. The job still does not delete a row.

---

## Rule evaluation

| Difference | Mark | Note |
|---|---|---|
| `priority()` on every packaged case | Preserved | archive 36, queue 70, review 17, urgent 2 |
| `priority('OPEN','LOW',50001)` = urgent | Preserved | Current Python deviation. 50,000 stays PROPOSED |
| `manual_review_required` | Preserved | Same helper |
| Night batch HOLD and REVIEW flag | Preserved | `processed` 500, `flagged_count` 210 on `limit=500` |
| JS `threshold('APAC', 2026)` = 25,000 | Preserved | Live Node. Honesty REAL |
| JS `legacyAllows(26250, 'APAC', 2026)` = true | Preserved | 25,000 * 1.05 = 26,250 |
| JS `legacyAllows(27000, 'APAC', 2026)` = false | Preserved | Live Node |
| JS `threshold('APAC', 1999)` = 999,999 | Preserved on the old function | Deviation. Not live policy |
| Java blank amount skip | Preserved | Live `count=1 total=10.50` |
| `GET /api/cases` ranking | Preserved | Still calls `priority()` |
| `evaluate_live_policy('APAC', 1999)` = HOLD_FOR_REVIEW | Approved | BR-05. Old `threshold` still returns 999,999 |
| `evaluate_live_policy(question='urgent_amount_cutoff')` = HOLD_FOR_REVIEW | Approved | BR-11. Old `priority` still uses the 50,000 branch |
| `evaluate_live_policy('APAC', 2026)` limit 25,000 USD | Approved path, archive match | Same number as the archive row and as old `threshold` |

---

## What did not change and is not a difference

REVIEW and HOLD stay open.

Finance-closed and audit-closed stay separate. BO-06b stays PROPOSED.

No aged-backlog day cutoff was written.

No exception-cycle-time field was added to `baseline()`.

---

## What this file does not do

This file does not start Phase 8. It does not sign BO-08.
