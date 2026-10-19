# Reconciliation rules

| Field | Value |
|---|---|
| Stage | Phase 10 / 21 Enterprise integration. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/12-specs/business-rules.md` BR-01 to BR-13; `apps/app_a/rules/adapter.py`; `docs/05-current-state/integration-landscape.md`; lake items listed per row |
| Assumptions | Queue GET still does not call `reconcile_feeds()` on the packaged store. Duplicate is a candidate mark until RT-05. |
| Unresolved issues | Signed month-end cut-off owner stays Unknown. Canonical money type for the Java float total stays Unknown. |
| Residual risks | Treating a REPLAY row as a new case would grow the queue. Merging `event_time` into `arrival_time` would read a late result as a current fact. |

This file names how Application A joins and marks inbound records. The language model does not vote on a match.

---

## Finding

**Finding.** Seven deterministic marks cover Phase 10 intake and investigation. Four of those marks wait for a named person. Injection text is never a match reason.
**Evidence.** BR-01, BR-02, BR-03, BR-05, BR-06, BR-10, BR-12. `replay_is_duplicate_candidate()` already tests `processing_status == 'REPLAY'`.
**Impact.** The agent may read the mark. OPA then returns HOLD_FOR_REVIEW or BLOCK. The person writes the disposition.
**Risk.** A language guess that two lots look alike can drop a new feed.
**Confidence.** High on the packaged marks. Unknown on a live `reconcile()` run.
**Open questions.** Cut-off owner. Live reconcile on a temp store only.

---

## Rule list

### REC-01 Replay is a duplicate candidate

| Field | Value |
|---|---|
| Finding | A partner feed with `processing_status = 'REPLAY'` is a duplicate candidate. Drop waits for RT-05. |
| Evidence | Lake item `rule.feed.replay_duplicate`. 67 packaged rows. Honesty: REAL. |
| Impact | Scenario 7. EV-02 then EV-09 `replay_confirm`. |
| Risk | Auto-drop from a model sentence would skip RT-05. |
| Confidence | High |
| Open questions | `reconcile()` has not been run on the packaged store. |
| Code | `replay_is_duplicate_candidate(status)` returns true when status is `REPLAY`. |
| OPA | OPA-R-06. HOLD_FOR_REVIEW |
| Person | RT-05. Decisions `drop_duplicate` or `keep_duplicate`. |

### REC-02 Gateway message id

| Field | Value |
|---|---|
| Finding | `gateway_bridge.apply()` treats a repeated `message_id` as a duplicate through a primary-key error. |
| Evidence | Packaged `gateway_inbox` has 1 row with `message_id = 'CHECK-semiconductor_lot'`. Honesty: REAL. |
| Impact | Intake de-duplication stays an identifier test. |
| Risk | A fuzzy lot match would invent a join key. |
| Confidence | High |
| Open questions | None for the packaged key. |
| Person | None for the mark. A later open case still waits if it needs a disposition. |

### REC-03 Two clocks stay two fields

| Field | Value |
|---|---|
| Finding | `event_time` and `arrival_time` stay two columns. Month-end uses `event_time` until a later signed rule says otherwise. A cut-off question routes HOLD_FOR_REVIEW. |
| Evidence | Lake item `rule.clock.event_vs_arrival`. 11,985 of 12,500 evidence rows differ. Honesty: REAL. |
| Impact | Scenario 9. EV-05. |
| Risk | One merged clock would treat a 2021 arrival as a 2020 fact. |
| Confidence | High on the two fields. Unknown on the cut-off owner. |
| Open questions | Cut-off owner. |
| OPA | Silence on cut-off uses OPA-R-02. |
| Person | Wait. No Group C row invents the cut-off. |

### REC-04 Recipe mismatch shows both revisions

| Field | Value |
|---|---|
| Finding | Dispatch `recipe_version` and equipment `recipe_rev` are both shown when they differ. Code does not pick a winner. |
| Evidence | Lake item `rule.recipe.mismatch_show_both`. 91 of 125 steps. Honesty: REAL. Fixture `PS000000016` is R02 versus R01. |
| Impact | Scenario 8. EV-04 then RT-03. |
| Risk | A model write of `engineering_hold` would skip RT-03. |
| Confidence | High |
| Open questions | Company title for Process Engineer. |
| OPA | OPA-R-06 on a proposed hold or release. |
| Person | RT-03. |

### REC-05 Policy overlap waits

| Field | Value |
|---|---|
| Finding | Two active rows on one country, or `valid_from` after `valid_to`, wait. The model does not pick a policy. |
| Evidence | Lake item `rule.policy.overlap_or_invalid`. US has 5 active rows. Honesty: REAL. Fixture `FAB-00000002`. |
| Impact | Scenario 10. EV-06 then RT-04. |
| Risk | Picking POL-0002 in code would hide the other four. |
| Confidence | High |
| Open questions | None for the wait. |
| OPA | OPA-R-04. |
| Person | RT-04. `policy_pick` or `keep_wait`. |

### REC-06 Site is canonical

| Field | Value |
|---|---|
| Finding | Site code is the lookup key. Site and stored sales region that disagree wait. Country AU or ZA with no site waits. |
| Evidence | Lake items `rule.region.site_canonical`, `rule.region.disagreement`. 84 packaged cases store AMER while site IN-BLR derives APAC. Honesty: REAL. |
| Impact | `rule_at` and `evaluate_live_policy` stay on site first. |
| Risk | Binding on stored AMER would hide those 84 rows. |
| Confidence | High on the six mapped sites. |
| Open questions | None for those sites. |
| OPA | OPA-R-05. |

### REC-07 Untrusted text is not a match key

| Field | Value |
|---|---|
| Finding | Harvested approve-or-ignore language stays in `untrusted_quotes`. It is not a reason to accept, drop, or close. |
| Evidence | Lake item `rule.untrusted_text.block`. Corpus IC-01 to IC-06. 86 partner feeds. Honesty: REAL. |
| Impact | Minutes 36 to 39. EV-12. |
| Risk | Serving the string as a tool instruction would drive a write. |
| Confidence | High on the 86 count. |
| Open questions | None for the 86. |
| OPA | OPA-R-01. BLOCK. |

---

## Archive match

When `evaluate_live_policy` or `rule_at` finds one archive row, Application A may show that limit as a citation. The 2023 EMEA limit is 18,600 USD. The 2026 APAC limit is 25,000 USD. Honesty: REAL.

When no archive row matches, the case waits. Live policy does not insert a substitute number. Lake item `rule.recipe_release.no_match`. OPA-R-02.

---

## What this file does not do

This file does not run `reconcile()` on the packaged store. It does not sign a cut-off. It does not write a dollar comparison into OPA.
