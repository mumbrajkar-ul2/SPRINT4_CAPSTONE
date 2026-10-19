# Test to evidence map

| Field | Value |
|---|---|
| Stage | Phase 6 / 13 Traceability |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. Existing tests point at lake items or packaged counts. Planned tests name the evidence they must produce. |
| Evidence sources | `context-lake/tests/`; `context-lake/eval/golden-questions.yaml`; `docs/07-repo-assessment/characterization-test-plan.md`; `generated/manifest.json` lake 1.0.0; `context-lake.sqlite3` queried read-only on 2026-10-18. |
| Assumptions | Honesty on packaged counts cited below is REAL. Lake tests already ran in Phase 5 Half B (46 tests passed, recorded in the tracker change log). This unit did not re-run them. |
| Unresolved issues | AT-* evidence files do not exist yet. CT-* evidence files do not exist yet. Numeric p95 evidence cannot exist until a measured run exists. |
| Residual risks | Pointing a test at an id that is not in the lake would fail the Done test. Every lake id in this file was confirmed present. |

This file says what a passing test must leave behind. Existing tests leave pytest output and golden-question verdicts. Planned tests will leave run logs in later phases.

---

## Finding

**Finding.** Existing lake tests already cite item ids that exist in lake 1.0.0. Characterization checks already name packaged counts. Application scenario tests still need run logs that name the same ids.
**Evidence.** Manifest `item_count` 148, `edge_count` 180, `lake_version` 1.0.0. Honesty: REAL.
**Impact.** A reviewer can pick GQ-01 and find `rule.recipe_release.limit.v2023.emea` in SQLite.
**Risk.** Re-using Phase 5 pytest output as Application A demo evidence would skip the UI path.
**Confidence.** High on EXISTING ids. Unknown on later AT-* logs.
**Open questions.** Where Phase 9 stores AT-* artifacts.

---

## Existing lake tests

| Test | What it checks | Evidence it produces | Lake item ids it must hit |
|---|---|---|---|
| `context-lake/tests/test_schema.py` | Item, link, term, envelope extra properties false | pytest PASS. Honesty: REAL when re-run | `arch.lake.yaml_sqlite` |
| `context-lake/tests/test_gates.py` | Five contract gates | pytest PASS | `arch.lake.yaml_sqlite`, `decision.fd22.lake_version_policy` |
| `context-lake/tests/test_golden.py` | GQ-01 to GQ-26 retrieval and verdict | pytest PASS. Verdict ANSWER, ABSTAIN, HOLD_FOR_REVIEW, or BLOCK | See GQ table below |
| `context-lake/tests/test_injection.py` | Every corpus row yields BLOCK | pytest PASS. No leak ids | `rule.untrusted_text.block`, `data.injection.partner_feeds` |
| `context-lake/tests/test_graph.py` | Recursive walk of `edges` | pytest PASS | `arch.graph.edges_table` |
| `context-lake/tests/test_parity.py` | Canonical versus deviation cards | pytest PASS | `rule.recipe_release.limit`, `rule.recipe_release.limit.impl.js`, `decision.fd08.canonical_archive` |

Worked example. `test_golden.py` GQ-01 calls `rule_at` for EMEA on 2023-07-01. Expected item `rule.recipe_release.limit.v2023.emea`. Expected answer 18,600 USD. Honesty: REAL.

---

## Golden questions to lake items

| Test id | Expected verdict | Evidence item ids (must exist) |
|---|---|---|
| GQ-01 | ANSWER | `rule.recipe_release.limit.v2023.emea` |
| GQ-02 | ANSWER | `rule.recipe_release.limit.v2026.apac` |
| GQ-03 | HOLD_FOR_REVIEW | `rule.recipe_release.no_match` |
| GQ-04 | ANSWER | `rule.recipe_release.limit.impl.js`, `rule.recipe_release.limit.v2022.apac` |
| GQ-05 | ANSWER | `rule.recipe_release.limit.impl.js_default`, `rule.recipe_release.no_match` |
| GQ-06 | ANSWER | `rule.urgent.amount.impl.python`, `rule.threshold.demo_50000`, `rule.threshold.silent` |
| GQ-07 | ANSWER | `rule.open_closed.operational`, `decision.bo06a.open_closed` |
| GQ-08 | ANSWER | `rule.open_closed.operational` |
| GQ-09 | HOLD_FOR_REVIEW | `rule.open_closed.finance_audit`, `decision.bo06b.three_closures` |
| GQ-10 | ANSWER | `rule.region.site_canonical`, `decision.bo07.site_canonical` |
| GQ-11 | ANSWER | `map.site.IN-BLR` |
| GQ-12 | HOLD_FOR_REVIEW | `rule.region.disagreement` |
| GQ-13 | HOLD_FOR_REVIEW | `rule.region.disagreement` |
| GQ-14 | ANSWER | `data.join.recipe_mismatch`, `decision.bp1.recipe_mismatch` |
| GQ-15 | ANSWER | `rule.recipe.mismatch_show_both`, `term.recipe_revision_dispatch`, `term.recipe_revision_equipment` |
| GQ-16 | HOLD_FOR_REVIEW | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence` |
| GQ-17 | ANSWER | `rule.feed.replay_duplicate`, `data.feed.replay` |
| GQ-18 | BLOCK | `rule.untrusted_text.block`, `decision.bp7.untrusted_text` |
| GQ-19 | ABSTAIN | `data.missing.lot_genealogy`, `term.lot_genealogy` |
| GQ-20 | ANSWER | `code.legacy_logic.priority`, `code.legacy_policy.js_allow`, `code.reconcile_legacy.java_total`, `code.shift_reconciliation.night_batch` |
| GQ-21 | ANSWER | `rule.night_batch.join_multiply`, `data.policy_register.overlap` |
| GQ-22 | ABSTAIN | `decision.inc_2025_014` |
| GQ-23 | ANSWER | `arch.listener.lake_rest_8091` |
| GQ-24 | ANSWER | `code.shift_reconciliation.night_batch`, `dep.night_batch_reads_enterprise` |
| GQ-25 | ANSWER | `decision.historic.2025_replay_rollback` |
| GQ-26 | ANSWER | `rule.month_end.blank.impl.java` |

Those ids were present in `items` on 2026-10-18.

---

## Planned characterization checks (CT-*)

These are named in `docs/07-repo-assessment/characterization-test-plan.md`. They are not yet test source. Evidence when they run is a REAL count from a read-only or copied database.

| Test id | Expected evidence | Linked lake item | Spec |
|---|---|---|---|
| CT-01 | records 125, open_cases 89, urgent_cases 2, sites 6 | `decision.bp5.open_closed_words` | FR-05 |
| CT-02 | `priority('CLOSED','LOW',99999)` returns archive | `code.legacy_logic.priority` | FR-09 |
| CT-03 | `priority('OPEN','CRITICAL',1)` returns urgent | `rule.urgent.severity.impl.python` | FR-09 |
| CT-04 | `priority('OPEN','LOW',50001)` returns urgent on the Python deviation | `rule.urgent.amount.impl.python` | BR-11, BR-14 |
| CT-05 | Count amount > 50000 is 0 | `rule.urgent.amount.impl.python` | FR-09 |
| CT-06 | 67 REPLAY rows | `data.feed.replay` | FR-02 |
| CT-07 | After reconcile on a copy, 67 DUPLICATE | `code.partner_feeds.reconcile` | FR-02 |
| CT-08 | unsupported schema REJECTED | `code.partner_feeds.reconcile` | EV-03 |
| CT-09 | negative quantity REJECTED | `code.partner_feeds.reconcile` | EV-03 |
| CT-10 | 91 recipe mismatches | `data.join.recipe_mismatch` | FR-01 |
| CT-13 | 11,985 clock disagreements | `data.clock.event_vs_arrival_evidence` | FR-03 |
| CT-25 | REVIEW is open | `rule.open_closed.operational` | FR-05 |
| CT-26 | 34 active policies | `data.policy_register.overlap` | FR-06 |
| CT-30 | 86 injection feeds | `data.injection.partner_feeds` | FR-07 |
| CT-35 | current 8080 GET /api/cases with no identity returns 200 | `arch.listener.legacy_8080` | EH-10 |
| CT-36 | 695 unassigned tasks | `data.task.unassigned` | FR-08 |
| CT-37 | INC-2025-014 has no owner in the body | `decision.inc_2025_014` | FR-08 |
| CT-40 | Headline KPI tests write Unknown when cutoff is absent | BO-02 | NFR Unknown cells |

CT-04 records the Python deviation. It does not sign 50,000 as live policy. Canonical live policy remains HOLD_FOR_REVIEW (`rule.threshold.silent`).

---

## Planned application tests (AT-*)

| Test id | When it is written | Evidence it must leave | Spec |
|---|---|---|---|
| AT-S7 | Phase 9 / 11 | Screenshot or log: 67 REPLAY visible. Drop waits. Citation to `rule.feed.replay_duplicate` | AC-S7 |
| AT-S8 | Phase 9 / 11 | Both revisions shown. Wait for RT-03. No model write of hold | AC-S8 |
| AT-S9 | Phase 9 / 11 | Two clock fields on a late result | AC-S9 |
| AT-S10 | Phase 9 / 11 | Overlap named. Wait for RT-04 | AC-S10 |
| AT-S11 | Phase 9 / 11 / 13 | User-visible retry status. Identity present. Owner empty until assigned | AC-S11 |
| AT-S12 | Phase 11 | Lineage view with item id and correlation id | AC-S12 |
| AT-PARITY | Phase 11 (FD-17) | S7 to S11 on both apps. Each difference names a lake item | AC-S13 |
| AT-INJECT | Phase 10 / 12 | BLOCK. Event EV-12. Case unchanged | AC-BP7 |
| AT-RANK | Phase 9 | Order from status, severity, amount. No model call | AC-RANK |
| AT-CITE / AT-QUERY | Phase 9 | Sentence plus lake item ids, or abstain | AC-CITE |
| AT-PERSON | Phase 10 | Approval row. Model has no write tool | AC-PERSON |
| AT-SOD | Phase 10 | `actor_id == proposed_by` rejected | EH-02 |
| AT-RESTART | Phase 10 | Kill process mid-wait. Wait remains | AC-PERSON |
| AT-AUDIT | Phase 10 | Read by correlation id returns the step list | API-Q-07 |
| AT-ID | Phase 8 / 12 | App A / App B case read without identity returns 401 | EH-01 |
| AT-HEALTH | Phase 8 | 8080, 8090, 8091, 8092 `/health` 200 | API-L-01 |
| AT-MCP | Phase 8 / 10 | Four lake tools over 8092 | API-M |
| AT-L-WRITE | Phase 8 | POST to 8091 returns 405 | EH-08 |
| AT-RULE | Phase 11 | App B without App A. Pass or fail from lake items | AC-RULE |
| AT-MVP | Phase 15 | Rehearsal checklist of the 40-minute path | AC-MVP |
| AT-OPA | Phase 10 | EXECUTE / HOLD_FOR_REVIEW / BLOCK on fixtures | EV-07 |

Honesty on those later logs: REAL when the test runs against the packaged fixture.

---

## Current inherited tests (limited evidence)

**Verified Fact.** `docs/07-repo-assessment/characterization-test-plan.md`. Current modules do not assert the eight catalogue counts. They do not call the HTTP routes. They do not run the Java or JavaScript programs.

| File | What it can evidence today | What it cannot |
|---|---|---|
| `tests/test_workflow.py` | Some workflow behaviour in the inherited tree | Catalogue counts |
| `tests/test_source_gateway.py` | Gateway helpers. Can write the packaged database if mis-aimed | Safe HTTP characterization unless `LEGACY_DB` is a temp file |
| `tests/test_partner_feeds.py` | Partner helpers | 67 REPLAY assertion |
| Other `test_*.py` in the inherited tree | Domain and enterprise helpers | BP1 to BP8 demo path |

CT-38 and CT-39 exist so later write tests use a temporary file and leave packaged hashes unchanged.

---

## Evidence that must not be invented

| Claim | Required handling | Lake item |
|---|---|---|
| INC-2025-014 owner | Stay Unknown. GQ-22 abstains | `decision.inc_2025_014` |
| Parent lot | Abstain. No column | `data.missing.lot_genealogy` |
| API p95 | No pass number | NFR Unknown |
| Availability percent | No pass number | NFR Unknown |
| 50,000 as decided | Fail if a test marks it decided | `rule.threshold.demo_50000` |
| 999,999 as live policy | Fail if a test uses it as canonical | `rule.threshold.never_999999` |
| Company job title | Stay Unknown | BO-09 leftover |

---

## What this file does not do

This file does not re-run pytest. It does not write AT-* source. It does not invent a p95. It does not start Phase 7.
