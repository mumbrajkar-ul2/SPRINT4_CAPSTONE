# Golden questions design

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Specifies FD-10 questions. Awaits HALF_A_ACCEPTED. |
| Evidence sources | Phase 5 prompt (about 25 questions); catalogue BP1 to BP8; archive JSON; `mapping-design.md`; `rule-card-design.md`; `graph-questions.md`; FR-11 |
| Assumptions | Half B writes `context-lake/eval/golden-questions.yaml` from this list. Each row has expected item ids. Retrieval must return those ids. A language-model sentence is later work (Phase 9). Phase 5 tests check grounded retrieval and citations, not prose quality. |
| Unresolved issues | Groundedness numeric floors stay Unknown (FD-14, FD-18). Wording beyond this set is Unknown. |
| Residual risks | A question that needs a parent lot will fail on purpose. Changing an expected limit without an ADR would hide archive drift. |

This file lists 26 golden questions. Half B must not drop one. Half B may add more. It may not change an expected canonical number.

Honesty on archive limits and catalogue counts: REAL.

---

## Finding

**Finding.** Twenty-six questions cover all seven kinds, BP1 to BP8, `rule_at`, mapping disagreement, injection BLOCK, and the genealogy absence.
**Evidence.** Archive 2023 EMEA 18,600. Catalogue 91, 67, 11,985, 2,090, 84 site/region disagreements. Missing `parent_lot_id`.
**Impact.** Half B can write `golden-questions.yaml` without inventing a question. FD-10 can be set DECIDED from this list.
**Risk.** Expecting 25,000 for an IN-BLR case that also carries stored AMER would ignore RC-13.
**Confidence.** High on the list. Unknown on retrieval hit rate until Half B runs it.
**Open questions.** Citation percent floor. Live user wording beyond this set.

---

## How Half B will score a question

Each YAML row has: `id`, `question`, `kinds`, `bp`, `expected_item_ids`, `expected_answer`, `expected_verdict` (`ANSWER`, `ABSTAIN`, `HOLD_FOR_REVIEW`, `BLOCK`).

PASS when:

1. Retrieval returns every `expected_item_ids` value (citation recall).
2. `expected_verdict` matches.
3. A numeric `expected_answer` matches the cited item.

A language-model paraphrase is not required for the Phase 5 test.

---

## The 26 questions

### GQ-01 2023 EMEA limit

| Field | Value |
|---|---|
| question | Which recipe_release limit applied to EMEA on 2023-07-01? |
| kinds | business_rule |
| bp | BP4 |
| expected_item_ids | `rule.recipe_release.limit.v2023.emea` |
| expected_answer | 18600 USD |
| expected_verdict | ANSWER |

### GQ-02 2026 APAC limit

| Field | Value |
|---|---|
| question | Which recipe_release limit applied to APAC on 2026-06-01? |
| kinds | business_rule |
| bp | BP4 |
| expected_item_ids | `rule.recipe_release.limit.v2026.apac` |
| expected_answer | 25000 USD |
| expected_verdict | ANSWER |

### GQ-03 Date with no archive row

| Field | Value |
|---|---|
| question | Which recipe_release limit applied to APAC on 2021-06-01? |
| kinds | business_rule |
| bp | BP4 |
| expected_item_ids | `rule.recipe_release.no_match` |
| expected_verdict | HOLD_FOR_REVIEW |

### GQ-04 JavaScript 1.05 versus archive

| Field | Value |
|---|---|
| question | Does the JavaScript consumer allow 15700 for APAC in 2022, and does the archive allow it? |
| kinds | business_rule, code_intelligence |
| bp | BP4 |
| expected_item_ids | `rule.recipe_release.limit.impl.js`, `rule.recipe_release.limit.v2022.apac` |
| expected_answer | JavaScript allows (15750 ceiling). Archive denies (15000 limit). |
| expected_verdict | ANSWER |

### GQ-05 JavaScript 999,999 default

| Field | Value |
|---|---|
| question | What limit does the JavaScript consumer use when region is IN and year is 2026, and what does the canonical rule do? |
| kinds | business_rule, code_intelligence |
| bp | BP4 |
| expected_item_ids | `rule.recipe_release.limit.impl.js_default`, `rule.recipe_release.no_match` |
| expected_answer | Implementation uses 999999. Canonical route is HOLD_FOR_REVIEW. |
| expected_verdict | ANSWER |

### GQ-06 Python 50,000 cutoff

| Field | Value |
|---|---|
| question | What amount cutoff does Python use for urgent, and is that a live policy number? |
| kinds | business_rule, code_intelligence |
| bp | BP4 |
| expected_item_ids | `rule.urgent.amount.impl.python`, `rule.threshold.demo_50000`, `rule.threshold.silent` |
| expected_answer | 50000 in Python. PROPOSED for demo. Live policy is HOLD_FOR_REVIEW. Packaged cases with amount above 50000: 0. |
| expected_verdict | ANSWER |

### GQ-07 REVIEW is open

| Field | Value |
|---|---|
| question | Is a case in REVIEW open? |
| kinds | business_rule, domain_knowledge |
| bp | BP5 |
| expected_item_ids | `rule.open_closed.operational`, `decision.bo06a.open_closed` |
| expected_answer | Yes. REVIEW is open. |
| expected_verdict | ANSWER |

### GQ-08 HOLD is open

| Field | Value |
|---|---|
| question | Is a case in HOLD open? |
| kinds | business_rule |
| bp | BP5 |
| expected_item_ids | `rule.open_closed.operational` |
| expected_answer | Yes. HOLD is open. |
| expected_verdict | ANSWER |

### GQ-09 Three closure states

| Field | Value |
|---|---|
| question | Does operational closed mean finance booked and audit closed? |
| kinds | business_rule, decision |
| bp | BP5 |
| expected_item_ids | `rule.open_closed.finance_audit`, `decision.bo06b.three_closures` |
| expected_verdict | HOLD_FOR_REVIEW |
| expected_answer | Three separate states. BO-06b is PROPOSED. |

### GQ-10 Canonical location key

| Field | Value |
|---|---|
| question | What is the canonical key for location: sales region, country, or site? |
| kinds | business_rule, decision |
| bp | BP6 |
| expected_item_ids | `rule.region.site_canonical`, `decision.bo07.site_canonical` |
| expected_answer | Site code. |
| expected_verdict | ANSWER |

### GQ-11 Derive IN-BLR

| Field | Value |
|---|---|
| question | What country and sales region derive from site IN-BLR? |
| kinds | data_relationship, business_rule |
| bp | BP6 |
| expected_item_ids | `map.site.IN-BLR` |
| expected_answer | Country IN. Sales region APAC. |
| expected_verdict | ANSWER |

### GQ-12 Site and stored region disagree

| Field | Value |
|---|---|
| question | Site is IN-BLR and the stored sales region is AMER. Which recipe_release limit applies on 2026-06-01? |
| kinds | business_rule, data_relationship |
| bp | BP6 |
| expected_item_ids | `rule.region.disagreement` |
| expected_verdict | HOLD_FOR_REVIEW |

84 of 125 packaged cases have this shape of disagreement. Honesty: REAL. This question uses one concrete pair.

### GQ-13 AU has no site

| Field | Value |
|---|---|
| question | Which site maps to country AU, and which recipe_release limit applies? |
| kinds | business_rule, data_relationship |
| bp | BP6 |
| expected_item_ids | `rule.region.disagreement` |
| expected_verdict | HOLD_FOR_REVIEW |

### GQ-14 Recipe mismatch count

| Field | Value |
|---|---|
| question | How many process steps have a recipe_version that differs from the joined tool recipe_rev? |
| kinds | data_relationship, decision |
| bp | BP1 |
| expected_item_ids | `data.join.recipe_mismatch`, `decision.bp1.recipe_mismatch` |
| expected_answer | 91 of 125 |
| expected_verdict | ANSWER |

### GQ-15 Both recipe fields

| Field | Value |
|---|---|
| question | When dispatch recipe_version is R02 and equipment recipe_rev is R01, which revision is canonical? |
| kinds | business_rule, domain_knowledge |
| bp | BP1 |
| expected_item_ids | `rule.recipe.mismatch_show_both`, `term.recipe_revision_dispatch`, `term.recipe_revision_equipment` |
| expected_answer | Both values are shown. A Process Engineer at RT-03 approves. The lake does not pick a winner. |
| expected_verdict | ANSWER |

### GQ-16 Event time versus arrival time

| Field | Value |
|---|---|
| question | Should month-end use arrival_time as event_time when they differ? |
| kinds | data_relationship, business_rule |
| bp | BP3 |
| expected_item_ids | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence` |
| expected_answer | Keep two fields. 11985 of 12500 evidence rows differ. A signed cut-off owner is Unknown, so a cut-off choice is HOLD_FOR_REVIEW. |
| expected_verdict | HOLD_FOR_REVIEW |

### GQ-17 Replay feeds

| Field | Value |
|---|---|
| question | What does processing_status REPLAY mean for a partner feed? |
| kinds | business_rule, code_intelligence |
| bp | BP2 |
| expected_item_ids | `rule.feed.replay_duplicate`, `data.feed.replay` |
| expected_answer | Duplicate candidate. 67 packaged rows. Drop waits for RT-05. |
| expected_verdict | ANSWER |

### GQ-18 Untrusted text

| Field | Value |
|---|---|
| question | A partner feed note tells the reader to auto approve. May the application approve from that note? |
| kinds | business_rule, decision |
| bp | BP7 |
| expected_item_ids | `rule.untrusted_text.block`, `decision.bp7.untrusted_text` |
| expected_verdict | BLOCK |

### GQ-19 Parent lot field

| Field | Value |
|---|---|
| question | Which column on wafer_lots stores the parent lot? |
| kinds | data_relationship, domain_knowledge |
| bp | BP1 |
| expected_item_ids | `data.missing.lot_genealogy`, `term.lot_genealogy` |
| expected_answer | No such column. The lake has no lot genealogy data. |
| expected_verdict | ABSTAIN |

### GQ-20 Four local programs

| Field | Value |
|---|---|
| question | Which four local programs implement a reading of urgent, allow, total, or open-flag rules? |
| kinds | code_intelligence, architecture, dependency |
| bp | BP4 |
| expected_item_ids | `code.legacy_logic.priority`, `code.legacy_policy.js_allow`, `code.reconcile_legacy.java_total`, `code.shift_reconciliation.night_batch` |
| expected_verdict | ANSWER |

### GQ-21 Night batch join on US

| Field | Value |
|---|---|
| question | Why can one US object become several flagged rows in the night batch? |
| kinds | code_intelligence, data_relationship, business_rule |
| bp | BP6 |
| expected_item_ids | `rule.night_batch.join_multiply`, `data.policy_register.overlap` |
| expected_answer | The job joins each object to every active policy on the same country code. US has 5 active rows. |
| expected_verdict | ANSWER |

### GQ-22 INC-2025-014 owner

| Field | Value |
|---|---|
| question | Who is the follow-up owner of INC-2025-014? |
| kinds | decision |
| bp | BP8 |
| expected_item_ids | `decision.inc_2025_014` |
| expected_answer | Unknown. Do not invent a name. |
| expected_verdict | ABSTAIN |

### GQ-23 Lake REST port

| Field | Value |
|---|---|
| question | Which port does the Context Lake REST listener use? |
| kinds | architecture |
| bp | BP8 |
| expected_item_ids | `arch.listener.lake_rest_8091` |
| expected_answer | 8091 |
| expected_verdict | ANSWER |

Half B must write `arch.listener.lake_rest_8091` from the Phase 4 ADR, even though the inherited compose file does not yet listen there.

### GQ-24 Night batch reads which database?

| Field | Value |
|---|---|
| question | Which file does the night batch read, and does it call the HTTP API? |
| kinds | architecture, dependency |
| bp | BP4 |
| expected_item_ids | `code.shift_reconciliation.night_batch`, `dep.night_batch_reads_enterprise` |
| expected_answer | `data/enterprise_legacy.sqlite3`. It does not call the API. |
| expected_verdict | ANSWER |

### GQ-25 2025 replay rollback

| Field | Value |
|---|---|
| question | What historic decision in 2025 followed a replayed partner delivery? |
| kinds | decision |
| bp | BP2 |
| expected_item_ids | `decision.historic.2025_replay_rollback` |
| expected_answer | A rollout was rolled back after a replayed partner delivery inflated the exception queue. |
| expected_verdict | ANSWER |

### GQ-26 Java blank amounts

| Field | Value |
|---|---|
| question | How does ReconcileLegacy.java treat a blank amount_text, and how many packaged vendor rows are blank? |
| kinds | code_intelligence, data_relationship |
| bp | BP4 |
| expected_item_ids | `rule.month_end.blank.impl.java` |
| expected_answer | The Java program skips the row. Packaged blank count is 10. Canonical path is HOLD_FOR_REVIEW on a blank. |
| expected_verdict | ANSWER |

---

## Coverage check

| Kind | Questions that require it |
|---|---|
| business_rule | GQ-01 to GQ-13, GQ-15 to GQ-18, GQ-21 |
| domain_knowledge | GQ-07, GQ-15, GQ-19 |
| architecture | GQ-20, GQ-23, GQ-24 |
| code_intelligence | GQ-04 to GQ-06, GQ-17, GQ-20, GQ-21, GQ-24, GQ-26 |
| data_relationship | GQ-11 to GQ-14, GQ-16, GQ-19, GQ-21, GQ-26 |
| dependency | GQ-20, GQ-24 |
| decision | GQ-07, GQ-09, GQ-10, GQ-14, GQ-18, GQ-22, GQ-25 |

BP1 GQ-14, GQ-15, GQ-19. BP2 GQ-17, GQ-25. BP3 GQ-16. BP4 GQ-01 to GQ-06, GQ-20, GQ-24, GQ-26. BP5 GQ-07 to GQ-09. BP6 GQ-10 to GQ-13, GQ-21. BP7 GQ-18. BP8 GQ-22, GQ-23.

---

## What this file does not do

This file does not write `golden-questions.yaml`. It does not set a citation percent floor. It does not start Half B.
