# Spec to test map

| Field | Value |
|---|---|
| Stage | Phase 6 / 13 Traceability |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. Each spec in `docs/12-specs/` names at least one test. Existing lake tests are marked EXISTING. Later app tests are marked PLANNED. |
| Evidence sources | `docs/12-specs/`; `context-lake/tests/`; `context-lake/eval/golden-questions.yaml`; `docs/07-repo-assessment/characterization-test-plan.md`; lake item ids confirmed on 2026-10-18. |
| Assumptions | Planned tests keep the ids in this file when later phases write them. |
| Unresolved issues | AT-* source does not exist yet. CT-* source does not exist yet. FD-17 harness design is PENDING. |
| Residual risks | Scoring EXISTING lake tests as Application A scenario coverage would hide that S7 to S13 still need app tests. |

This file maps each spec id to the test that will protect it. A test that already runs in the lake job is EXISTING. A test that later phases must write is PLANNED.

---

## Finding

**Finding.** Lake tests already protect schema, gates, golden questions, injection BLOCK, graph walks, and rule-card parity. Application scenario tests, identity tests, restart tests, and the two-app harness remain PLANNED.
**Evidence.** Files `context-lake/tests/test_schema.py`, `test_gates.py`, `test_golden.py`, `test_injection.py`, `test_graph.py`, `test_parity.py`. Characterization plan CT-01 to CT-40.
**Impact.** Phase 5 coverage is not lost. Phases 7 to 11 still owe AT-*.
**Risk.** Calling GQ-17 a complete S7 demo test would skip the RT-05 UI path.
**Confidence.** High on EXISTING lake tests. Unknown on later AT-* pass rate.
**Open questions.** FD-12 characterization order. FD-17 harness.

---

## System and SLO specs

| Spec | Test | State | Lake item cited by the spec |
|---|---|---|---|
| SS locked listeners | GQ-23. Planned AT-HEALTH on 8080, 8090, 8091, 8092 | EXISTING + PLANNED | `arch.listener.lake_rest_8091` |
| SS rule-source split | Planned AT-RULE, AT-PARITY | PLANNED | `decision.fd06.two_apps` |
| SLO-B1 person on writes | Planned AT-PERSON | PLANNED | `rule.hold.person_only` |
| SLO-B2 proposer and approver are different people | Planned AT-SOD | PLANNED | `term.approval` |
| SLO-B3 injection BLOCK | `test_injection.py`. GQ-18. Planned AT-INJECT | EXISTING + PLANNED | `rule.untrusted_text.block` |
| SLO-B4 cite or abstain | `test_golden.py`. Planned AT-CITE | EXISTING + PLANNED | `arch.lake.yaml_sqlite` |
| SLO-B5 App B lake-only rules | Planned AT-RULE with Application A stopped | PLANNED | `decision.fd06.two_apps` |
| SLO-B6 app independence | Planned AT-PARITY | PLANNED | `decision.fd06.two_apps` |
| SLO-B7 two clocks | GQ-16. Planned AT-S9 | EXISTING + PLANNED | `rule.clock.event_vs_arrival` |
| SLO-B8 REVIEW and HOLD open | GQ-07, GQ-08. Planned CT-25 | EXISTING + PLANNED | `rule.open_closed.operational` |
| SLO-B9 identity on App A / App B | Planned AT-ID. CT-35 records 8080 gap | PLANNED | `arch.listener.legacy_8080` |
| SLO-B10 audit by correlation id | Planned AT-AUDIT | PLANNED | `decision.fd06.two_apps` |
| Numeric SLO cells Unknown | No numeric pass test. GAP-01 | PLANNED as a gap, not a fake target | NFR file |

---

## API specs

| Spec | Test | State | Lake item |
|---|---|---|---|
| API-L-01 Health | Planned AT-HEALTH | PLANNED | `arch.listener.lake_rest_8091` |
| API-L-02 Version | Planned AT-PIN versus `generated/manifest.json` | PLANNED | `decision.fd22.lake_version_policy` |
| API-L-03 Search | `test_golden.py` retrieve(). Planned AT-L-SEARCH | EXISTING + PLANNED | `arch.lake.yaml_sqlite` |
| API-L-04 Get item | `get_item` in lake tests. GQ-01 | EXISTING | `rule.recipe_release.limit.v2023.emea` |
| API-L-05 Get links | `test_graph.py` | EXISTING | `arch.graph.edges_table` |
| API-L-06 Rule at | `rule_at` branches in `test_golden.py` (GQ-01, GQ-02, GQ-03, GQ-09, GQ-12) | EXISTING | `rule.recipe_release.limit` |
| API-M four tools | Same as API-L-03 to API-L-06, over MCP, planned AT-MCP | PLANNED | `arch.listener.lake_mcp_8092` |
| API-G gateway | Current `test_source_gateway.py`. Planned CT-16. Planned AT-S11 | EXISTING + PLANNED | `arch.listener.gateway_8090` |
| API-8080 baseline | Current tests do not call HTTP. Planned CT-35, CT-37 | PLANNED | `arch.listener.legacy_8080` |
| API-Q-02 Queue | Planned AT-RANK | PLANNED | `code.legacy_logic.priority` |
| API-Q-03 Case | Planned AT-S7 to AT-S11 | PLANNED | `term.case` |
| API-Q-04 Approval | Planned AT-PERSON, AT-SOD | PLANNED | `term.approval` |
| API-Q-05 Recovery | Planned AT-S11 | PLANNED | `term.outage` |
| API-Q-06 Query | Planned AT-QUERY. Existing golden retrieval | EXISTING + PLANNED | `arch.lake.yaml_sqlite` |
| API-Q-07 Audit | Planned AT-AUDIT | PLANNED | `decision.fd06.two_apps` |
| API-Q-08 Lineage | Planned AT-S12. Existing `test_graph.py` | EXISTING + PLANNED | `arch.graph.edges_table` |

Lake POST rejected: planned AT-L-WRITE mapped to EH-08.

---

## Event specs

| Spec | Test | State | Lake item |
|---|---|---|---|
| EV-01 FeedIntakeAccepted | Planned AT-S7 | PLANNED | `term.source_message` |
| EV-02 FeedDuplicateCandidate | Planned AT-S7. GQ-17 | EXISTING + PLANNED | `rule.feed.replay_duplicate` |
| EV-03 FeedRejected | Planned CT-08, CT-09 | PLANNED | `code.partner_feeds.reconcile` |
| EV-04 RecipeMismatchRaised | Planned AT-S8. GQ-15 | EXISTING + PLANNED | `rule.recipe.mismatch_show_both` |
| EV-05 ClocksKeptApart | Planned AT-S9. GQ-16 | EXISTING + PLANNED | `rule.clock.event_vs_arrival` |
| EV-06 PolicyOverlapRaised | Planned AT-S10. GQ-21 | EXISTING + PLANNED | `rule.policy.overlap_or_invalid` |
| EV-07 OpaVerdictRecorded | Planned AT-OPA (Phase 10). Existing lake BLOCK fixture | EXISTING + PLANNED | `rule.untrusted_text.block` |
| EV-08 AgentStepRecorded | Planned AT-PLAN, AT-AUDIT | PLANNED | `rule.hold.person_only` |
| EV-09 HumanApprovalRecorded | Planned AT-PERSON, AT-RESTART | PLANNED | `term.approval` |
| EV-10 OwnerAssigned | Planned AT-S11. GQ-22 (abstain until assigned) | EXISTING + PLANNED | `decision.inc_2025_014` |
| EV-11 RecoveryStatusChanged | Planned AT-S11 | PLANNED | `term.outage` |
| EV-12 InjectionBlocked | `test_injection.py`. GQ-18. Planned AT-INJECT | EXISTING + PLANNED | `rule.untrusted_text.block` |

---

## Schema specs

| Spec | Test | State | Lake item |
|---|---|---|---|
| SCH-01 Item | `test_schema.py`. `test_gates.py` | EXISTING | `arch.lake.yaml_sqlite` |
| SCH-02 Link | `test_graph.py`. `test_schema.py` | EXISTING | `arch.graph.edges_table` |
| SCH-03 Rule card | `test_parity.py` | EXISTING | `rule.recipe_release.limit` |
| SCH-04 Term | `test_schema.py` | EXISTING | `term.open_operational` |
| SCH-05 Read envelope | lake runtime tests plus planned AT-L-SEARCH | EXISTING + PLANNED | `arch.lake.yaml_sqlite` |
| SCH-06 Case payload | Planned AT-S8, AT-S9 | PLANNED | `term.case` |
| SCH-07 Approval payload | Planned AT-PERSON | PLANNED | `term.approval` |
| SCH-08 Recovery payload | Planned AT-S11 | PLANNED | `term.outage` |
| SCH-09 Query payload | Planned AT-CITE | PLANNED | `arch.lake.yaml_sqlite` |

Parent-lot absence: GQ-19 EXISTING. Lake item `data.missing.lot_genealogy`.

---

## Business-rule specs

| Spec | Test | State | Lake item |
|---|---|---|---|
| BR role map | Planned AT-SOD, AT-PERSON | PLANNED | `term.approval` |
| BR-01 | GQ-14, GQ-15. Planned AT-S8 | EXISTING + PLANNED | `rule.recipe.mismatch_show_both` |
| BR-02 | GQ-17. Planned AT-S7, CT-06 | EXISTING + PLANNED | `rule.feed.replay_duplicate` |
| BR-03 | GQ-16. Planned AT-S9, CT-13 | EXISTING + PLANNED | `rule.clock.event_vs_arrival` |
| BR-04 | GQ-01, GQ-02. `test_parity.py` | EXISTING | `rule.recipe_release.limit` |
| BR-05 | GQ-03, GQ-05 | EXISTING | `rule.recipe_release.no_match` |
| BR-06 | GQ-12, GQ-13, GQ-21. Planned AT-S10 | EXISTING + PLANNED | `rule.policy.overlap_or_invalid` |
| BR-07 | GQ-07, GQ-08. Planned CT-25 | EXISTING + PLANNED | `rule.open_closed.operational` |
| BR-08 | GQ-09 HOLD_FOR_REVIEW | EXISTING | `rule.open_closed.finance_audit` |
| BR-09 | GQ-10, GQ-11 | EXISTING | `rule.region.site_canonical` |
| BR-10 | GQ-12, GQ-13 | EXISTING | `rule.region.disagreement` |
| BR-11 | GQ-06 | EXISTING | `rule.threshold.silent` |
| BR-12 | GQ-18. `test_injection.py` | EXISTING | `rule.untrusted_text.block` |
| BR-13 | Planned AT-S8. FD-05 recorded 117/125 | PLANNED | `rule.hold.person_only` |
| BR-14 | Planned AT-RANK, CT-02 to CT-05 | PLANNED | `code.legacy_logic.priority` |
| BR-15 | GQ-20. `test_parity.py` | EXISTING | `decision.bp4.four_programs` |

---

## Error-handling specs

| Spec | Test | State | Lake item |
|---|---|---|---|
| EH-01 missing identity | Planned AT-ID. CT-35 (current 8080 200) | PLANNED | `decision.bp8.auth_and_owner` |
| EH-02 separation of duties | Planned AT-SOD | PLANNED | `term.approval` |
| EH-03 role mismatch | Planned AT-PERSON | PLANNED | `rule.recipe.mismatch_show_both` |
| EH-04 wait for person | GQ-03, GQ-09, GQ-12. Planned AT-S10 | EXISTING + PLANNED | `rule.threshold.silent` |
| EH-05 injection stop | `test_injection.py` | EXISTING | `rule.untrusted_text.block` |
| EH-06 abstain | GQ-19, GQ-22 | EXISTING | `data.missing.lot_genealogy` |
| EH-07 upstream recovery | Planned AT-S11 | PLANNED | `term.outage` |
| EH-08 lake write rejected | Planned AT-L-WRITE | PLANNED | `arch.lake.yaml_sqlite` |
| EH-09 validation | `test_schema.py`, `test_gates.py` | EXISTING | `arch.lake.yaml_sqlite` |
| EH-10 8080 baseline | Planned CT-35 | PLANNED | `arch.listener.legacy_8080` |

---

## Acceptance criteria

| Spec | Test | State |
|---|---|---|
| AC-S7 | Planned AT-S7. GQ-17. CT-06 | EXISTING + PLANNED |
| AC-S8 | Planned AT-S8. GQ-14, GQ-15. CT-10 | EXISTING + PLANNED |
| AC-S9 | Planned AT-S9. GQ-16. CT-13 | EXISTING + PLANNED |
| AC-S10 | Planned AT-S10. GQ-21. CT-26 | EXISTING + PLANNED |
| AC-S11 | Planned AT-S11. GQ-22. CT-36, CT-37 | EXISTING + PLANNED |
| AC-S12 | Planned AT-S12. `test_graph.py`. GQ-20 | EXISTING + PLANNED |
| AC-S13 | Planned AT-PARITY | PLANNED |
| AC-BP7 | `test_injection.py`. GQ-18. CT-30 | EXISTING + PLANNED |
| AC-RANK | Planned AT-RANK. CT-02 to CT-05 | PLANNED |
| AC-CITE | `test_golden.py`. Planned AT-CITE | EXISTING + PLANNED |
| AC-PERSON | Planned AT-PERSON, AT-SOD, AT-RESTART | PLANNED |
| AC-RULE | `test_parity.py`. GQ-01. Planned AT-RULE | EXISTING + PLANNED |
| AC-MVP | Planned AT-MVP rehearsal checklist | PLANNED |

---

## What this file does not do

This file does not write AT-* source. It does not run the 40-minute demo. It does not start Phase 7.
