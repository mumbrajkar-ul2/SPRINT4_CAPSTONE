# Business rules

| Field | Value |
|---|---|
| Stage | Phase 6 / 12 Spec-driven design |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. Role map recorded with authority: sme. Company job titles stay Unknown. BO-06b and BO-08 stay PROPOSED. |
| Evidence sources | `Decision_Tracker.md` BO-09 and section 7 Group C; `docs/09-initial-prd/initial-prd.md`; `docs/02-stakeholders/approval-authority-map.md`; lake rule items listed per row. Confirmed in `context-lake.sqlite3` on 2026-10-18. |
| Assumptions | BO-03 working answer holds: a person approves every record-changing action. The tracker row is PROPOSED. The run does not pause at it. |
| Unresolved issues | Company job titles stay Unknown. Named people stay Unknown. INC-2025-014 follow-up owner stays Unknown. Aged-backlog cutoff stays Unknown. Signer names for BO-06b and BO-08 stay Unknown. |
| Residual risks | Coding an approval to a made-up user would invent an owner. Writing 50,000 or 999,999 as a live policy number would treat a PROPOSED row as code. Merging finance-closed into operational-closed would book a number the owner has not signed. |

This file records who may approve, hold, or block each action type. It records the governed tests both applications must follow. Application A takes those tests from its transformed code. Application B takes those tests only from the lake.

---

## Finding

**Finding.** Six run-time roles cover every record-changing action in the initial PRD. The proposer of an action is never its approver. Company job titles that match these roles are unconfirmed.
**Evidence.** `Decision_Tracker.md` BO-09 DECIDED, authority: sme. Section 7 Group C. Lake items `term.approval`, `rule.hold.person_only`, `rule.feed.replay_duplicate`, `rule.recipe.mismatch_show_both`, `rule.policy.overlap_or_invalid`, `decision.inc_2025_014`.
**Impact.** The approval resource in `api-contracts.md` checks `actor_role` against this map. Phase 10 builds the queue on this map.
**Risk.** Letting the language model pick a policy, drop a replay, or write `engineering_hold` would skip the named role.
**Confidence.** High on the SME map. Unknown on company titles and named people.
**Open questions.** Company titles. Named people. INC-2025-014 owner.

---

## Role map (BO-09)

**Authority:** sme. **Tracker status:** DECIDED.

The SME set these role names as the standard fab exception-handling map. The Business Owner's remaining task is only to confirm the company's own job titles match this map. That confirmation has not happened. Company job titles stay Unknown. This unit proceeds on the SME map.

The proposer of an action is never its approver.

| Run-time id | SME role name | Company job title | Person |
|---|---|---|---|
| RT-01 | Fab Exception Reviewer | Unknown | Unknown |
| RT-02 | Shift Lead or Process Engineer (Approver) | Unknown | Unknown |
| RT-03 | Process Engineer | Unknown | Unknown |
| RT-04 | Policy Owner | Unknown | Unknown |
| RT-05 | Operations Analyst | Unknown | Unknown |
| RT-06 | Operations Lead | Unknown | Unknown |

Worked example. A language model drafts a hold on a recipe mismatch. `proposed_by` is the draft actor. RT-03 is a Process Engineer who did not propose that draft. RT-03 records hold or release. The same login cannot occupy both fields.

---

## Who may approve, hold, or block each action type

**Verified Fact.** Group C in `Decision_Tracker.md`. Lake items in the last column.

| Action type | API `action_type` | Who may record it | Who may not record it | Lake item |
|---|---|---|---|---|
| Dispose a case that routed to HOLD_FOR_REVIEW | `dispose` | RT-01 Fab Exception Reviewer | The model. The person who proposed the draft | `term.approval` |
| Approve, hold, or block an agent-proposed action | `approve_agent` | RT-02 Shift Lead or Process Engineer (Approver) | The proposing agent. The same person as `proposed_by` | `rule.hold.person_only` |
| Approve a recipe-mismatch hold or release | `recipe_hold_or_release` | RT-03 Process Engineer | Operations Analyst acting alone. The model | `rule.recipe.mismatch_show_both` |
| Pick a policy on overlap, or keep the wait | `policy_pick` | RT-04 Policy Owner | The model | `rule.policy.overlap_or_invalid` |
| Confirm a replay duplicate before it is dropped | `replay_confirm` | RT-05 Operations Analyst | An unattended job. The model | `rule.feed.replay_duplicate` |
| Assign the follow-up owner when none is recorded | `assign_owner` | RT-06 Operations Lead | A made-up name. The model | `decision.inc_2025_014` |

A permission the Business Owner has not confirmed as a company title stays PROPOSED for title mapping only. The SME role itself is DECIDED. Owner of the leftover title confirmation: Business Owner.

OPA, which is Open Policy Agent, may return EXECUTE, HOLD_FOR_REVIEW, or BLOCK before the person acts. BLOCK stops the action. HOLD_FOR_REVIEW waits for the row above. EXECUTE on a record change still waits for the person under the BO-03 working answer.

---

## Governed tests (rule cards already in the lake)

Each row is a lake item that exists in `context-lake.sqlite3`. Application A implements the canonical test in transformed code. Application B reads the same item from the lake.

### BR-01 Recipe mismatch shows both revisions

| Field | Value |
|---|---|
| Lake item | `rule.recipe.mismatch_show_both` |
| Authority | sme |
| Policy status | decided |
| Finding | 91 of 125 process steps mismatch `recipe_version` and `recipe_rev`. Honesty: REAL. Both values are shown. RT-03 approves. The lake does not pick a winner. The lake does not write `engineering_hold`. |
| Evidence | `data.join.recipe_mismatch`, `decision.bp1.recipe_mismatch` |
| Impact | Scenario 8 |
| Risk | A model write of `engineering_hold` would skip RT-03 |
| Confidence | High |
| Open questions | Company title for Process Engineer |

### BR-02 Replay is a duplicate candidate

| Field | Value |
|---|---|
| Lake item | `rule.feed.replay_duplicate` |
| Authority | policy_archive |
| Policy status | n/a |
| Finding | 67 REPLAY rows. Honesty: REAL. Drop waits for RT-05. |
| Evidence | `data.feed.replay`, `code.partner_feeds.reconcile`, `term.replay` |
| Impact | Scenario 7 |
| Risk | A language guess that two lots look alike can drop a new feed |
| Confidence | High |
| Open questions | `reconcile()` has not been run on the packaged store |

### BR-03 Two clocks

| Field | Value |
|---|---|
| Lake item | `rule.clock.event_vs_arrival` |
| Authority | policy_archive |
| Policy status | n/a |
| Finding | 11,985 of 12,500 evidence rows differ. Honesty: REAL. Month-end uses `event_time` unless a later signed rule says otherwise. A signed cut-off owner is Unknown, so a cut-off question routes HOLD_FOR_REVIEW. |
| Evidence | `data.clock.event_vs_arrival_evidence`, `decision.bp3.two_clocks` |
| Impact | Scenario 9 |
| Risk | Merging the clocks would read a late result as a current fact |
| Confidence | High |
| Open questions | Cut-off owner |

### BR-04 Canonical recipe_release limit

| Field | Value |
|---|---|
| Lake item | `rule.recipe_release.limit` and version children such as `rule.recipe_release.limit.v2023.emea` |
| Authority | policy_archive |
| Policy status | decided |
| Finding | Archive is canonical. 2023 EMEA limit is 18,600 USD. 2026 APAC limit is 25,000 USD. Honesty: REAL. |
| Evidence | `decision.fd08.canonical_archive`, `decision.bo05.recipe_authority`, `data.contract.decision_policies_archive` |
| Impact | Scenario 12. Application B `rule_at` |
| Risk | Copying the JavaScript 1.05 line into the canonical table would make the deviation the rule |
| Confidence | High |
| Open questions | None for the archive numbers |

### BR-05 No archive match

| Field | Value |
|---|---|
| Lake item | `rule.recipe_release.no_match` |
| Authority | policy_archive |
| Policy status | decided |
| Finding | When no archive row matches, route HOLD_FOR_REVIEW. Do not use 999,999. |
| Evidence | `rule.threshold.never_999999` |
| Impact | GQ-03, GQ-05 |
| Risk | The JavaScript default 999,999 would pass almost everything |
| Confidence | High |
| Open questions | None |

### BR-06 Policy overlap

| Field | Value |
|---|---|
| Lake item | `rule.policy.overlap_or_invalid` |
| Authority | policy_archive |
| Policy status | decided |
| Finding | Two active rows on one country, or `valid_from` after `valid_to`, route HOLD_FOR_REVIEW. US has 5 active rows. POL-0039 has from 2025-01-01 and to 2024-12-31. Honesty: REAL. RT-04 picks or keeps the wait. |
| Evidence | `data.policy_register.overlap`, `decision.bp6.region_overlap` |
| Impact | Scenario 10 |
| Risk | Picking a policy without RT-04 would hide the overlap |
| Confidence | High |
| Open questions | None for the wait |

### BR-07 Operational open and closed

| Field | Value |
|---|---|
| Lake item | `rule.open_closed.operational` |
| Authority | sme |
| Policy status | decided |
| Finding | REVIEW and HOLD are open. Closed needs a final disposition and no pending engineering action. BO-06a. |
| Evidence | `decision.bo06a.open_closed`, `term.open_operational` |
| Impact | Scenario 13 open count |
| Risk | Changing the word list moves the backlog number |
| Confidence | High |
| Open questions | Aged-backlog cutoff stays Unknown |

### BR-08 Finance and audit closure (PROPOSED)

| Field | Value |
|---|---|
| Lake item | `rule.open_closed.finance_audit` |
| Authority | unresolved |
| Policy status | proposed |
| Finding | Operational closed, finance booked, and audit closed stay three states. BO-06b stays PROPOSED. A mismatch routes HOLD_FOR_REVIEW. This spec does not hard-code a merge. |
| Evidence | `decision.bo06b.three_closures` |
| Impact | Queue labels stay separate |
| Risk | Booking finance from operational closed would treat an unsigned row as code |
| Confidence | High on the working answer. Signature missing |
| Open questions | Signer. Owner: Business Owner |

### BR-09 Site is canonical

| Field | Value |
|---|---|
| Lake item | `rule.region.site_canonical` |
| Authority | sme |
| Policy status | decided |
| Finding | Site code is the canonical key. Country and sales region are derived. Site IN-BLR derives country IN and sales region APAC. |
| Evidence | `decision.bo07.site_canonical`, `map.site.IN-BLR` |
| Impact | `rule_at` lookups |
| Risk | Binding on stored AMER while the site derives APAC would hide 84 packaged disagreements. Honesty: REAL |
| Confidence | High |
| Open questions | None for the six mapped sites |

### BR-10 Scope disagreement

| Field | Value |
|---|---|
| Lake item | `rule.region.disagreement` |
| Authority | sme |
| Policy status | decided |
| Finding | Site IN-BLR with stored AMER routes HOLD_FOR_REVIEW. Country AU or ZA with no site routes HOLD_FOR_REVIEW. |
| Evidence | `rule.region.specificity` |
| Impact | GQ-12, GQ-13 |
| Risk | Picking a limit anyway would hide the disagreement |
| Confidence | High |
| Open questions | None |

### BR-11 Silent threshold (PROPOSED)

| Field | Value |
|---|---|
| Lake item | `rule.threshold.silent` |
| Authority | unresolved |
| Policy status | proposed |
| Finding | The archive is silent on an urgent amount cutoff. Live policy is HOLD_FOR_REVIEW. Demo may show 50,000 labelled PROPOSED. Never use 999,999. BO-08 stays PROPOSED. This spec does not hard-code 50,000 as live policy. |
| Evidence | `decision.bo08.silent_threshold`, `rule.threshold.demo_50000`, `rule.threshold.never_999999`, `rule.urgent.amount.impl.python` |
| Impact | Queue ranking in Application A still uses the rebuilt Python function as a recorded deviation. Canonical live policy waits. |
| Risk | Compiling 50,000 into OPA as decided would sign BO-08 in code |
| Confidence | High on the working answer. Signature missing |
| Open questions | Signer. Owner: Business Owner |

### BR-12 Untrusted text is data

| Field | Value |
|---|---|
| Lake item | `rule.untrusted_text.block` |
| Authority | policy_archive |
| Policy status | n/a |
| Finding | Harvested instruction language never drives approve, release, ignore-validation, or close-from-text. Expected verdict BLOCK. 86 partner feeds carry that language. Honesty: REAL. |
| Evidence | `data.injection.partner_feeds`, `decision.bp7.untrusted_text` |
| Impact | Minutes 36 to 39 |
| Risk | Serving the string outside `untrusted_quotes` would leak an instruction |
| Confidence | High |
| Open questions | None for the 86 count |

### BR-13 Hold is a person action

| Field | Value |
|---|---|
| Lake item | `rule.hold.person_only` |
| Authority | sme |
| Policy status | proposed |
| Finding | A model that proposes `engineering_hold=1` routes HOLD_FOR_REVIEW. FD-05 rejects a hold predictor. 117 of 125 versus 117 of 125. Honesty: REAL. BO-03 working answer is unsigned. The card stays proposed. |
| Evidence | `term.engineering_hold`, `term.approval` |
| Impact | Scenario 8 write path |
| Risk | A later path that writes the hold from a model proposal would apply an unsigned bound as if it were signed code |
| Confidence | High on the bound. Signature missing |
| Open questions | BO-03 signer |

### BR-14 Queue ranking from stored fields

| Field | Value |
|---|---|
| Lake item | `code.legacy_logic.priority`, `rule.urgent.severity.impl.python` |
| Authority | unresolved on severity words. Ranking itself is FD-04 code |
| Policy status | n/a on severity. proposed on the 50,000 branch |
| Finding | Ranking uses status, severity, and amount. It does not call a model. CRITICAL returns urgent. Amount above 50,000 is a recorded Python deviation and stays PROPOSED as live policy. Packaged amount-above-50000 count is 0. Honesty: REAL. |
| Evidence | `rule.priority.closed.impl.python` |
| Impact | W2 |
| Risk | A hold-probability column would change order with no gain over the majority guess |
| Confidence | High |
| Open questions | Canonical severity ranking until an archive row states it |

### BR-15 Four programs are deviations

| Field | Value |
|---|---|
| Lake item | `decision.bp4.four_programs`, `decision.fd08.canonical_archive` |
| Authority | sme on the archive choice (BO-05) |
| Policy status | decided for the archive |
| Finding | Python priority, JavaScript allow, Java totals, and the night batch are deviations. Observed implementation cards lock the disagreement. They do not replace the archive. |
| Evidence | `code.legacy_logic.priority`, `code.legacy_policy.js_allow`, `code.reconcile_legacy.java_total`, `code.shift_reconciliation.night_batch` |
| Impact | Scenario 12 and 13 |
| Risk | Importing `legacy_logic.py` into Application B would hide a missing lake item |
| Confidence | High |
| Open questions | Canonical money type for the Java float total. Lake item `rule.month_end.float.impl.java` |

---

## Permissions marked PROPOSED with an owner

| Permission or number | Why it is PROPOSED | Owner |
|---|---|---|
| Company job titles matching RT-01 to RT-06 | Business Owner has not confirmed titles | Business Owner |
| Merge of operational, finance, and audit closed | BO-06b unsigned | Business Owner |
| Live urgent amount cutoff 50,000 | BO-08 unsigned | Business Owner |
| Use of 999,999 as a live limit | Forbidden by the working answer. Still unsigned as a tracker row | Business Owner |
| Model write of a record | BO-03 unsigned. Working answer still forbids it | Business Owner |
| Named person on INC-2025-014 | Unknown until RT-06 assigns one | Operations Lead at run time |

None of those rows is written into code as a decided number.

---

## What this file does not do

This file does not invent a company job title. It does not invent a person name. It does not sign BO-06b or BO-08. It does not hard-code 50,000 as live policy. It does not start Phase 7.
