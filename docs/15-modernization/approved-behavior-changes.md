# Approved behaviour changes

| Field | Value |
|---|---|
| Stage | Phase 7 / 15 Transform. Half B code. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7b-doc-20261018-001 |
| Status | COMPLETE for this unit |
| Evidence sources | BR-05; BR-11; ED-P7A-02; `legacy_logic.evaluate_live_policy`; characterization tests `test_evaluate_live_policy_*` |
| Assumptions | `priority()` stays the ranking function. The approved change is the new live-policy function only. |
| Unresolved issues | BO-08 stays PROPOSED. The signer is Unknown. Owner: Business Owner. |
| Residual risks | Copying the JavaScript 1.05 line or the 999,999 default into `evaluate_live_policy` would undo this change. |

This file names the one approved behaviour change in Phase 7. Feed intake and reconciliation have no approved difference.

---

## Finding

**Finding.** `evaluate_live_policy` returns HOLD_FOR_REVIEW when the archive has no matching row, and when the question is a silent urgent amount cutoff. On a matching APAC 2026 row it returns the archive limit 25,000 USD.
**Evidence.** BR-05. BR-11. Live calls in this unit. Tests `test_evaluate_live_policy_no_match_is_hold`, `test_evaluate_live_policy_silent_urgent_cutoff_is_hold`, `test_evaluate_live_policy_archive_apac_2026`.
**Impact.** Scenario 12 can show the JavaScript 999,999 default and the live-policy wait side by side.
**Risk.** Replacing `priority()` in place with this function would still leave `urgent_cases` at 2 on this fixture, and would still need an approved-change write-up. This unit left `priority()` in place.
**Confidence.** High
**Open questions.** Signer of BO-08. Owner: Business Owner.

---

## The approved change

| Item | Old function | New function | Source |
|---|---|---|---|
| No archive row for APAC 1999 | `threshold('APAC', 1999)` returns 999,999 | `evaluate_live_policy('APAC', 1999)` returns HOLD_FOR_REVIEW | BR-05 |
| Archive silent on an urgent amount cutoff | `priority(..., amount > 50000)` returns urgent | `evaluate_live_policy(question='urgent_amount_cutoff')` returns HOLD_FOR_REVIEW | BR-11. 50,000 stays PROPOSED |
| Archive match APAC 2026 | `threshold('APAC', 2026)` returns 25,000 | `evaluate_live_policy('APAC', 2026)` returns limit 25,000 USD | BR-04 archive row. Honesty REAL |

Worked example. `evaluate_live_policy('APAC', 1999)` returned HOLD_FOR_REVIEW in this unit. The old `threshold('APAC', 1999)` still returned 999,999 on the live Node run. Characterization test CT-20 still calls `threshold`.

Worked example. `evaluate_live_policy(question='urgent_amount_cutoff')` returned HOLD_FOR_REVIEW. `priority('OPEN', 'LOW', 50001)` still returned `urgent`. The 50,000 branch stays a recorded Python deviation. It is not decided live policy.

---

## What is not an approved change

`intake_apply` matches `apply` on the SH-FI fields.

`reconcile_feeds` matches `reconcile` on the SH-RC fields.

`run_flag` matches `run` on `processed`, `by_tenant`, `flagged_count`, and `flagged_preview`.

`GET /api/cases` still ranks with `priority()`.

REVIEW and HOLD stay open (BO-06a). This unit did not merge finance-closed into operational-closed.

This unit did not write 50,000 as signed policy. This unit did not write 999,999 as live policy.

---

## What this file does not do

This file does not start Application A. It does not sign BO-08.
