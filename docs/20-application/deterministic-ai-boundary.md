# Deterministic versus AI boundary in Application A

| Field | Value |
|---|---|
| Stage | Phase 9 / 20 Application and services. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p9a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `Decision_Tracker.md` FD-04, FD-05, BO-03; `docs/08-ai-qualification/deterministic-vs-ai-boundaries.md`; `docs/09-initial-prd/capability-map.md`; `docs/15-modernization/approved-behavior-changes.md`; Phase 9 locked facts |
| Assumptions | BO-03 working answer holds and stays PROPOSED. The model gets no write tool in this phase. |
| Unresolved issues | Recursion-limit number stays Unknown (FD-15). OPA rule bodies stay Unknown (FD-16). Company titles stay Unknown. |
| Residual risks | A later path that writes `engineering_hold` from a model proposal would apply an unsigned bound as if it were signed code. A ranking call to the model would add a fifth test of urgency. |

This file says where Application A code ends and the language model begins. Half B must keep each job on the side named here.

---

## Finding

**Finding.** Application A has four deterministic jobs, three GenAI jobs, one rejected ML job, and six person jobs. The lake is a citation store on the GenAI jobs. The lake is not the Application A rule engine.
**Evidence.** FD-04 DECIDED. FD-05 DECIDED. Capability map F-01 to F-13. Phase 7 `evaluate_live_policy`.
**Impact.** Half B can wire routes without asking whether queue ranking needs a prompt.
**Risk.** Calling `rule_at` and skipping `evaluate_live_policy` would move pass-or-fail onto the lake.
**Confidence.** High
**Open questions.** FD-15 tool names for Phase 10. BO-03 signer.

---

## Deterministic (code)

**Verified Fact.** FD-04.

| Job | Function or test | Input fields | Output |
|---|---|---|---|
| Triage ranking | `priority()` | status, severity, amount | archive, urgent, review, or queue |
| Rule evaluation | `evaluate_live_policy()` | region, year, or silent-cutoff question | archive limit dict, or HOLD_FOR_REVIEW |
| Reconciliation | `reconcile_feeds()` | key, schema, REPLAY, quantity | accepted, rejected, duplicate, skipped |
| Intake de-duplication | `intake_apply()` plus REPLAY / `message_id` | feed record | accept, reject, or duplicate candidate |
| Two clocks kept apart | store and schema | `event_time`, `arrival_time` | two fields |
| Recipe mismatch flag | join of `recipe_version` and `recipe_rev` | those two columns | both values shown |
| Policy overlap flag | active `policy_register` rows on one country, or invalid interval | register rows | wait |
| Identity and role match | header check | `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` | 401, 403, or continue |
| Open versus closed | BO-06a operational meaning | status word | REVIEW and HOLD are open |

Worked example. `priority('OPEN', 'CRITICAL', 1)` returns urgent. Two packaged cases are urgent because severity is CRITICAL. Zero packaged cases have `amount > 50000`. Honesty: REAL. The 50,000 Python branch stays a recorded deviation. Live cutoff policy is HOLD_FOR_REVIEW via `evaluate_live_policy(question='urgent_amount_cutoff')`.

Worked example. 67 REPLAY rows. Honesty: REAL. Duplicate is the status word and key test. A model does not vote.

These jobs have no prompt in `prompt-registry.md`.

---

## GenAI (model drafts, then code checks)

**Verified Fact.** FD-04. FD-14.

| Job | Prompt id | What the model returns | What code still does |
|---|---|---|---|
| Conflict explanation | P-EXPLAIN-CONFLICT | SCH-09 sentence | Retrieve, `check_claim`, block untrusted orders, keep both values |
| Natural-language query | P-NL-QUERY | SCH-09 sentence | Same |
| Draft plan | P-DRAFT-PLAN | `draft_plan` text plus citations | Store as proposal. No write. Phase 10 adds `interrupt()` |

The model may cite lake item ids from the retrieved set. The model may not:

- rank the queue
- mark a duplicate
- return pass or fail as the governed result
- write `engineering_hold`
- drop a replay
- pick a policy
- assign an owner
- invent a parent lot

Worked example. Scenario 8. Code lists R02 and R01. The model says those two revisions differ and cites `rule.recipe.mismatch_show_both`. RT-03 records hold or release.

---

## Rejected

**Verified Fact.** FD-05.

Predicting `engineering_hold` is ML-rejected. Majority accuracy 117/125. Leave-one-out logistic regression 117/125. Honesty: REAL. Application A has no hold-probability column and no hold scorer.

---

## Person

**Verified Fact.** Group C. BO-03 working answer, still PROPOSED. BO-09 DECIDED.

| Role | Action the person records | Scenario |
|---|---|---|
| RT-01 | `dispose` on HOLD_FOR_REVIEW | overlap, silence, unsigned policy |
| RT-02 | `approve_agent` on a draft plan | later write; Phase 9 only stores the draft |
| RT-03 | `recipe_hold_or_release` | 8 |
| RT-04 | `policy_pick` or `keep_wait` | 10 |
| RT-05 | `replay_confirm` | 7 |
| RT-06 | `assign_owner` | 11 |

The proposer of an action is never its approver. The model is never the actor on `POST /api/approvals`.

OPA may later return EXECUTE, HOLD_FOR_REVIEW, or BLOCK (FD-16). EXECUTE on a record change still waits for the person under the BO-03 working answer.

---

## Boundary in each scenario

| Scenario | Code | Model | Person |
|---|---|---|---|
| 7 Replay | Mark duplicate candidate | Explain with `rule.feed.replay_duplicate` | RT-05 confirms drop |
| 8 Recipe | Show both revisions | Name both, cite mismatch rule | RT-03 hold or release |
| 9 Clocks | Keep two fields | Explain lateness. Cut-off question HOLD_FOR_REVIEW | Cut-off owner Unknown, so wait |
| 10 Overlap | Detect overlap | Name it. Do not pick | RT-04 picks or keeps wait |
| 11 Outage | Identity, retry status, empty owner | Cite `term.outage`. Abstain on INC owner | RT-06 assigns a supplied name |

BP7 injection is a control on 7 to 11. Code and retrieval set `block: true`. The model does not approve from the note.

---

## Lake versus transformed code

| Need | Store |
|---|---|
| Pass, fail, duplicate, rank | Transformed code |
| Citation ids, golden questions, missing-data facts | Lake REST |
| Untrusted quote locators | Lake items with `trust: untrusted_text` plus flagged case field |

If the lake is unreachable, deterministic jobs still run. GenAI jobs abstain.

---

## What this file does not do

This file does not write OPA Rego. It does not sign BO-03. It does not start Half B.
