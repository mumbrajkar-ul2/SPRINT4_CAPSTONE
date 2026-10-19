# Requirements traceability matrix

| Field | Value |
|---|---|
| Stage | Phase 6 / 13 Traceability |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. No critical requirement is an orphan. App and characterization tests that are not yet code are named as planned. |
| Evidence sources | `docs/09-initial-prd/functional-requirements.md`; `docs/09-initial-prd/nfrs.md`; `docs/12-specs/`; lake items confirmed in `context-lake.sqlite3` on 2026-10-18; existing lake tests under `context-lake/tests/`; planned checks in `docs/07-repo-assessment/characterization-test-plan.md`. |
| Assumptions | Feature ids F-01 to F-15 remain the feature set. Planned test ids AT-* are written in later phases. They are mapped here so no requirement sits without a test name. |
| Unresolved issues | Many AT-* tests are not yet source. Identity tests wait on FD-13. Numeric SLO tests wait on a measured number that does not exist. |
| Residual risks | Treating a planned test as already run would hide a coverage gap. Those gaps are listed in `coverage-gap-register.md`. They are not critical orphans of a requirement. |

This file maps each requirement to a spec, a test, and an evidence item. A critical orphan is a requirement with no spec. This matrix has none.

How to read one row. FR-01 is the recipe-mismatch requirement. Specs AC-S8 and BR-01 describe it. Tests AT-S8 (later) and GQ-14, GQ-15, CT-10 (named now) check it. Evidence is lake item `data.join.recipe_mismatch`.

---

## Finding

**Finding.** FR-01 to FR-15 and the NFR behaviours each have a spec in `docs/12-specs/`, a named test, and a lake item id that exists in `context-lake.sqlite3`.
**Evidence.** This matrix. Read-only query on 2026-10-18 returned 148 items including every id cited below.
**Impact.** Phase 7 and later can implement without an unmapped requirement.
**Risk.** A later feature outside BP1 to BP8 would be an orphan the moment it appears.
**Confidence.** High on the map. Unknown on later measured p95.
**Open questions.** When AT-* source is written. FD-17 harness. FD-13 identity.

---

## Functional requirements

| Requirement | Specs | Tests (existing or planned) | Evidence (lake item) | Problem | Orphan? |
|---|---|---|---|---|---|
| FR-01 Recipe mismatch detection and approval route | AC-S8. BR-01. API-Q-03. API-Q-04. EV-04 | Planned AT-S8. Existing GQ-14, GQ-15. Planned CT-10, CT-11, CT-12 | `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch`, `decision.bp1.recipe_mismatch` | BP1 | No |
| FR-02 Replay duplicate detection and confirmation | AC-S7. BR-02. API-Q-04. EV-02 | Planned AT-S7. Existing GQ-17, GQ-25. Planned CT-06, CT-07 | `rule.feed.replay_duplicate`, `data.feed.replay`, `decision.bp2.replay` | BP2 | No |
| FR-03 Event time and arrival time kept apart | AC-S9. BR-03. API-Q-03. EV-05 | Planned AT-S9. Existing GQ-16. Planned CT-13, CT-14, CT-15, CT-16 | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence`, `decision.bp3.two_clocks` | BP3 | No |
| FR-04 One governed rule evaluation | AC-RULE. BR-04. BR-05. BR-15. API-L-06 | Planned AT-RULE. Existing GQ-01, GQ-02, GQ-03, GQ-04, GQ-05. Existing `test_parity.py`. Existing `test.rule.recipe_release.emea_2023` | `rule.recipe_release.limit`, `decision.fd08.canonical_archive`, `decision.bp4.four_programs` | BP4 | No |
| FR-05 Open and closed shown with one operational meaning | AC-S13. BR-07. BR-08. API-Q-02 | Planned AT-S13. Existing GQ-07, GQ-08, GQ-09. Planned CT-01, CT-23, CT-24, CT-25 | `rule.open_closed.operational`, `term.open_operational`, `decision.bo06a.open_closed` | BP5 | No |
| FR-06 Overlapping policy detect and abstain | AC-S10. BR-06. API-Q-03. EV-06 | Planned AT-S10. Existing GQ-12, GQ-13, GQ-21. Planned CT-26, CT-27 | `rule.policy.overlap_or_invalid`, `data.policy_register.overlap`, `decision.bp6.region_overlap` | BP6 | No |
| FR-07 Untrusted text isolated as data | AC-BP7. BR-12. EV-12. EH-05 | Existing `test_injection.py`. Existing GQ-18. Planned CT-30 to CT-34. Planned AT-INJECT | `rule.untrusted_text.block`, `data.injection.partner_feeds`, `decision.bp7.untrusted_text` | BP7 | No |
| FR-08 Identity, owner assignment, recovery status | AC-S11. API-Q-01, API-Q-05, API-Q-07. EV-10, EV-11. EH-01, EH-07 | Planned AT-S11, AT-ID. Planned CT-35, CT-36, CT-37. Existing GQ-22, GQ-23 | `decision.bp8.auth_and_owner`, `arch.listener.legacy_8080`, `data.task.unassigned`, `decision.inc_2025_014`, `term.outage` | BP8 | No |
| FR-09 Queue ranking from stored fields | AC-RANK. BR-14. API-Q-02 | Planned AT-RANK. Planned CT-02, CT-03, CT-04, CT-05 | `code.legacy_logic.priority`, `rule.urgent.severity.impl.python`, `rule.threshold.silent` | BP4, BP5 | No |
| FR-10 Cited conflict explanation | AC-CITE. API-Q-06. SCH-09 | Planned AT-CITE. Existing GQ-01 to GQ-26 retrieval in `test_golden.py` | `arch.lake.yaml_sqlite`, `rule.untrusted_text.block` | BP1 to BP7 | No |
| FR-11 Cited natural-language answer | AC-CITE. API-Q-06. API-L-03 | Planned AT-QUERY. Existing `test_golden.py` | `arch.lake.yaml_sqlite`, `data.missing.lot_genealogy` | BP1 to BP8 | No |
| FR-12 Draft investigation plan, then wait | AC-PERSON. API-Q-03 `draft_plan`. EV-08 | Planned AT-PLAN. Planned AT-RESTART (Phase 10) | `rule.hold.person_only`, `term.approval` | BP1, BP2, BP6, BP8 | No |
| FR-13 Person on every record-changing action | AC-PERSON. BR role map. API-Q-04. EV-09. EH-02, EH-03, EH-04 | Planned AT-PERSON, AT-SOD. Planned AT-RESTART | `term.approval`, `rule.hold.person_only` | BP1, BP2, BP6, BP8 | No |
| FR-14 Same-scenario run on both applications | AC-S13. SS rule-source split | Planned AT-PARITY (FD-17 later). Existing lake `test_parity.py` for rule cards | `decision.fd06.two_apps` | BP4, BP5 | No |
| FR-15 Rule lineage in the Application B context view | AC-S12. API-Q-08. API-L-05 | Planned AT-S12. Existing `test_graph.py`. Existing GQ-20 | `arch.graph.edges_table`, `decision.bp4.four_programs`, `test.rule.recipe_release.emea_2023` | BP4 | No |

Worked example. FR-01 cites `data.join.recipe_mismatch`. That id is an accepted `data_relationship` item in lake 1.0.0. GQ-14 expects that id. AT-S8 is the later Application A / Application B scenario test.

---

## Non-functional behaviours

Numeric NFR cells that are Unknown are mapped to a spec that says Unknown. That is coverage, not a target.

| NFR behaviour | Specs | Tests | Evidence | Orphan? |
|---|---|---|---|---|
| Local synthetic records. Read-only model tools | `system-spec.md` language-model bounds. API-M write tools absent | Planned AT-PERSON (no write tool). Existing injection tests | FD-02. `rule.hold.person_only` | No |
| Person on writes | AC-PERSON. BR role map | Planned AT-PERSON | `term.approval` | No |
| Untrusted text is data | AC-BP7. EH-05 | Existing `test_injection.py` | `rule.untrusted_text.block` | No |
| No hold predictor | BR-13. `non-goals.md` | Planned AT-S8 (model does not write hold). FD-05 numbers already recorded | `rule.hold.person_only` | No |
| App independence | AC-S13. API shared rules | Planned AT-PARITY with Application A stopped | `decision.fd06.two_apps` | No |
| Same scenarios and KPI families | AC-S13. AC-MVP | Planned AT-S7 to AT-S13 | `decision.fd06.two_apps` | No |
| Honesty labels | AC-MVP | Planned AT-MVP demo checklist | `Execution_Plan.md` section 9 | No |
| Rule source split | AC-RULE | Planned AT-RULE. Existing `test_parity.py` | `decision.fd06.two_apps` | No |
| No monetary benefit claim | AC-MVP numeric cells | No ROI API exists in `api-contracts.md` | BO-11 | No |
| Identity on App A / App B | EH-01. API-Q-03 | Planned AT-ID. CT-35 records current 8080 gap | `arch.listener.legacy_8080` | No |
| Separation of duties | EH-02. BR role map | Planned AT-SOD | `term.approval` | No |
| Audit row per step and approval | API-Q-07. EV-08, EV-09 | Planned AT-AUDIT (Phase 10) | `decision.fd06.two_apps` | No |
| User-visible recovery | AC-S11. API-Q-05. EH-07 | Planned AT-S11 | `term.outage` | No |
| Citations or abstain | AC-CITE. EH-06 | Existing `test_golden.py`. Planned AT-CITE | `arch.lake.yaml_sqlite` | No |
| API p95, availability, RTO, RPO | `system-spec.md` numeric cells stay Unknown | No numeric SLO test is claimed | NFR file. FD-11 recommended Unknown | No |

---

## Business problems

| Problem | Requirements | Specs | Lake decision item | Orphan? |
|---|---|---|---|---|
| BP1 | FR-01, FR-10, FR-11, FR-12, FR-13 | AC-S8 | `decision.bp1.recipe_mismatch` | No |
| BP2 | FR-02, FR-10, FR-11, FR-12, FR-13 | AC-S7 | `decision.bp2.replay` | No |
| BP3 | FR-03, FR-10, FR-11 | AC-S9 | `decision.bp3.two_clocks` | No |
| BP4 | FR-04, FR-09, FR-10, FR-11, FR-14, FR-15 | AC-S12, AC-S13, AC-RULE | `decision.bp4.four_programs` | No |
| BP5 | FR-05, FR-09, FR-11, FR-14 | AC-S13, BR-07 | `decision.bp5.open_closed_words` | No |
| BP6 | FR-06, FR-10, FR-11, FR-12, FR-13 | AC-S10 | `decision.bp6.region_overlap` | No |
| BP7 | FR-07, FR-10, FR-11 | AC-BP7 | `decision.bp7.untrusted_text` | No |
| BP8 | FR-08, FR-11, FR-12, FR-13 | AC-S11 | `decision.bp8.auth_and_owner` | No |

Each of BP1 to BP8 has at least one requirement and one spec. No ninth problem sits in this matrix.

---

## What this file does not do

This file does not write test source. It does not mark a planned test as already run. It does not start Phase 7.
