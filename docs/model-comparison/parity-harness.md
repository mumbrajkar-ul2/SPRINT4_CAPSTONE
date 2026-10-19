# Parity harness design (FD-17)

| Field | Value |
|---|---|
| Stage | Phase 11 / 20p Application B from the lake. Half B results. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p11b-doc-20261018-001 |
| Status | IMPLEMENTED. Half B ran the harness. Honesty: REAL. Awaits reviewer. |
| Evidence sources | `Decision_Tracker.md` FD-17, FD-06, FD-14; `docs/12-specs/acceptance-criteria.md` AC-S7 to AC-S13, AC-RANK, AC-CITE, AC-PERSON, AC-RULE, AC-BP7; `docs/12-specs/api-contracts.md` API-Q-01 to API-Q-08; `apps/app_a/eval/freeze-set.yaml`; `context-lake/generated/app-b-pin.json`; `docs/22-agentic-engineering/agent-test-results.md` |
| Assumptions | Application A stays on port 8100. Application B stays on port 8110. Lake version 1.0.0 and pin `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` hold. `MODEL_MODE=replay`. BO-03, BO-06b, and BO-08 stay PROPOSED. |
| Unresolved issues | Company job titles stay Unknown. Numeric groundedness, citation, and abstention percent floors stay Unknown (FD-14). |
| Residual risks | Publishing a match percent would invent an FD-17 number. Letting Application B import Application A rule functions would hide a missing lake item. Opening the inherited store from Application B would put a legacy-repo path in the build inputs. |

This file names the parity harness and records the Half B run. FD-17 is DECIDED. Authority for the field list: team-force.

The harness compares Application A and Application B on the same scenario packs. A row matches when both apps return the same disposition. A row that does not match must list one or more lake item ids that explain the difference. The harness does not publish a match percent. Harness output is REAL.

Engineering decision ED-P11A-01, authority: team-force. The field list, the disposition vocabulary, the scenario table, and the runner path below.

---

## FD-17 recommended answer

**Authority:** team-force. **Tracker status:** DECIDED.

**Recommended text.** The parity harness is a pytest runner, not a product HTTP API. It posts the same scenario inputs to Application A on 8100 and Application B on 8110. Each result row stores the named fields in this file. `disposition_match` is true or false. When it is false, `difference_lake_item_ids` is a non-empty list of lake item ids. The runner may print the integer count of matched rows and the integer count of differing rows. It does not compute or publish a match percent. Half B writes those integers into the results section of this file. Honesty: REAL.

**Label.** Inference from the Phase 11 prompt, AC-S13, and the FD-17 default. Half B measured 12 matched rows and 2 differing rows. Honesty: REAL.

---

## Finding

**Finding.** Twelve compare rows cover S7 to S11, S12, RANK, CITE, PERSON, RULE, and BP7. Each row uses the same case id and the same request fields on both apps. S12 is present only on Application B. That designed gap cites `decision.fd06.two_apps`.
**Evidence.** AC-S13. FR-14. Freeze packs SP-07 to SP-11. API-Q-01 to API-Q-08. Pin `context-lake/generated/app-b-pin.json`.
**Impact.** Half B wrote `tests/platform/test_parity_harness.py` from this page. It did not invent a field or a percent target.
**Risk.** Scoring “pass if 95 percent match” would invent an FD-17 number.
**Confidence.** High on the field list, the scenario ids, and the Half B integers.
**Open questions.** Whether a later lake version adds a 67-id feed list.

---

## How the harness runs

The harness is a test. It is not a compare-apps route. API contracts omit that product URL.

| Step | What happens |
|---|---|
| 1 | Read `context-lake/generated/app-b-pin.json`. Record `lake_version` and `sqlite_sha256`. |
| 2 | For each compare row, send the same method, path, identity headers, and body fields to port 8100 and port 8110. |
| 3 | Fill one result record with the fields below. |
| 4 | Set `disposition_match` true when the two dispositions are equal. |
| 5 | When `disposition_match` is false, fill `difference_lake_item_ids`. An empty list on a miss fails the row. |
| 6 | Write the result records into this file under Half B results. Also write `docs/model-comparison/parity-results.json`. Honesty: REAL. |

Application B must also pass a second run with Application A stopped. That run checks health, the five scenario cases, lineage, and query on 8110 only. It does not fill Application A disposition cells.

Identity headers on every `/api` call except health: `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role`. Optional `X-Correlation-Id` joins the audit rows. Demo actors stay `demo-rt01-1` through `demo-rt06-1`. Company titles stay Unknown.

`MODEL_MODE=replay`. No live model. The model has no write tool.

---

## Harness record fields

Engineering decision ED-P11A-01 continued. Half B creates one record per compare row. Extra fields stay out until a later ADR.

| # | Field | Required | What it holds |
|---|---|---|---|
| 1 | `harness_row_id` | yes | Stable id. Example `PH-S7-01`. |
| 2 | `scenario_id` | yes | `S7`, `S8`, `S9`, `S10`, `S11`, `S12`, `RANK`, `CITE`, `PERSON`, `RULE`, or `BP7`. |
| 3 | `pack_id` | yes when a freeze pack exists | `SP-07` to `SP-11`, or empty. |
| 4 | `case_id` | yes when the row has a case | Packaged fixture id. |
| 5 | `route` | yes | Method and path. Example `GET /api/cases/PS000000016`. |
| 6 | `actor_role` | yes | `RT-01` to `RT-06`. |
| 7 | `input_fields` | yes | The request fields that must match on both apps. The API key value stays out of the file. |
| 8 | `lake_version` | yes | Pin value. Current `1.0.0`. |
| 9 | `pin_sqlite_sha256` | yes | Pin hash. Current `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. |
| 10 | `compared_field` | yes | One name from the disposition vocabulary. |
| 11 | `app_a_disposition` | yes on a two-app row | The Application A value. On S12 this is `view_absent`. |
| 12 | `app_b_disposition` | yes | The Application B value. |
| 13 | `disposition_match` | yes | `true` or `false`. |
| 14 | `difference_lake_item_ids` | yes | JSON array of lake item ids. Empty only when `disposition_match` is true. |
| 15 | `app_a_verdict` | when a query or gate ran | `ANSWER`, `ABSTAIN`, `HOLD_FOR_REVIEW`, `BLOCK`, `EXECUTE`, or empty. |
| 16 | `app_b_verdict` | when a query or gate ran | Same closed list. |
| 17 | `app_a_citations` | when a sentence exists | Lake item ids from Application A. |
| 18 | `app_b_citations` | when a sentence exists | Lake item ids from Application B. |
| 19 | `waiting_role` | when the case waits | `RT-01` to `RT-06`. |
| 20 | `open_operational` | when the row is a queue or case | `true` or `false` from `rule.open_closed.operational`. |
| 21 | `correlation_id` | when an audit or lineage row exists | Join key. Phase 10 worked id is `corr-p10b-doc-20261018-001`. |
| 22 | `kpi_family` | yes | One of the eight families in `Execution_Plan.md` section 9. This cell names the family. It does not set a target. |
| 23 | `honesty` | yes | `REAL` on harness output. Replay sentences stay `PRECOMPUTED`. |
| 24 | `notes` | no | Short application note. No invented percent. |

Worked example. Row `PH-S8-01`. `case_id` is `PS000000016`. `compared_field` is `recipe_pair`. Application A returns `recipe_version=R02` and `recipe_rev=R01`. Application B returns the same pair after reading `rule.recipe.mismatch_show_both`. `disposition_match` is true. `difference_lake_item_ids` is `[]`. Honesty on the pair: REAL.

Worked example. Row `PH-S12-01`. `route` is `GET /api/lineage/rule.recipe_release.limit.v2023.emea`. Application A has no lineage route. `app_a_disposition` is `view_absent`. Application B returns the item, the `tested_by` edge to `test.rule.recipe_release.emea_2023`, and `correlation_id=corr-p10b-doc-20261018-001`. `disposition_match` is false. `difference_lake_item_ids` is `["decision.fd06.two_apps", "arch.graph.edges_table"]`.

---

## Disposition vocabulary

Engineering decision ED-P11A-07, authority: team-force. The harness compares these named fields. It does not compare source file paths.

| `compared_field` | Equal when both apps return | Lake item used on Application B |
|---|---|---|
| `duplicate_candidate` | The same true or false mark | `rule.feed.replay_duplicate` |
| `replay_candidate_count` | The same integer 67 | `data.feed.replay` |
| `recipe_pair` | Both `recipe_version` and `recipe_rev` | `rule.recipe.mismatch_show_both` |
| `clock_pair` | Both `event_time` and `arrival_time` | `rule.clock.event_vs_arrival` |
| `overlapping_policy_ids` | The same policy id list | `rule.policy.overlap_or_invalid` |
| `waiting_role` | The same RT id | `term.approval` |
| `open_operational` | The same true or false | `rule.open_closed.operational` |
| `owner_id` | The same value, empty allowed | `decision.inc_2025_014` |
| `query_verdict` | The same `ANSWER`, `ABSTAIN`, or `HOLD_FOR_REVIEW` | FD-14 plus the cited item |
| `citations` | The same lake item id set, order ignored | `arch.lake.yaml_sqlite` |
| `block` | The same true or false | `rule.untrusted_text.block` |
| `opa_verdict` | The same `EXECUTE`, `HOLD_FOR_REVIEW`, or `BLOCK` | The lake item that produced the wait or stop |
| `approval_recorded` | The same `decision` after the same person post | `rule.hold.person_only` |
| `engineering_hold` | The same 0 or 1 after the person post | `rule.hold.person_only` |
| `limit_value` | The same archive number | `rule.recipe_release.limit` |
| `finance_closed` | The same separate flag. Not merged | `rule.open_closed.finance_audit` |
| `audit_closed` | The same separate flag. Not merged | `rule.open_closed.finance_audit` |
| `lineage_view` | Both return the lineage body. Application A is `view_absent` | `decision.fd06.two_apps` |
| `amount_cutoff_label` | Both label 50000 as `proposed`, or both wait | `rule.threshold.silent`, `rule.threshold.demo_50000` |

BO-06b stays PROPOSED. `finance_closed` and `audit_closed` stay two flags. The harness fails a row that merges them into `open_operational`.

BO-08 stays PROPOSED. Live policy for a silent amount cutoff is `HOLD_FOR_REVIEW`. A demo 50000 display must stay labelled `proposed`. The harness fails a row that stores 50000 as decided. The harness fails a row that uses 999999. Lake item `rule.threshold.never_999999`.

---

## Compare rows Half B must run

The route names come from Application A so the inputs stay the same. Application B implements the same paths plus lineage. Application B does not take pass-or-fail from Application A functions.

| `harness_row_id` | Scenario | Case | Route | `compared_field` | Expected lake items on B |
|---|---|---|---|---|---|
| PH-S7-01 | S7 | `REPLAY-000000000` | `GET /api/cases/REPLAY-000000000` | `duplicate_candidate` | `rule.feed.replay_duplicate`, `data.feed.replay` |
| PH-S7-02 | S7 | `REPLAY-000000000` | `GET /api/queue` | `replay_candidate_count` | `data.feed.replay` |
| PH-S8-01 | S8 | `PS000000016` | `GET /api/cases/PS000000016` | `recipe_pair` | `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch` |
| PH-S9-01 | S9 | `E-00000000` | `GET /api/cases/E-00000000` | `clock_pair` | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence` |
| PH-S10-01 | S10 | `FAB-00000002` | `GET /api/cases/FAB-00000002` | `overlapping_policy_ids` | `rule.policy.overlap_or_invalid`, `data.policy_register.overlap` |
| PH-S11-01 | S11 | `INC-2025-014` | `GET /api/cases/INC-2025-014` | `owner_id` | `decision.inc_2025_014` |
| PH-S11-02 | S11 | `INC-2025-014` | `GET /api/recovery` | `owner_id` | `term.outage`, `decision.inc_2025_014` |
| PH-S12-01 | S12 | `PS000000016` | `GET /api/lineage/rule.recipe_release.limit.v2023.emea` | `lineage_view` | `decision.bp4.four_programs`, `test.rule.recipe_release.emea_2023` |
| PH-RANK-01 | RANK | queue | `GET /api/queue` | `open_operational` | `rule.open_closed.operational` |
| PH-RANK-02 | RANK | queue | `GET /api/queue` | `amount_cutoff_label` | `rule.threshold.silent`, `rule.threshold.demo_50000` |
| PH-CITE-01 | CITE | `PS000000016` | `POST /api/query` | `query_verdict` and `citations` | FD-14. Expected ids from SP-08 |
| PH-PERSON-01 | PERSON | `PS000000016` | `POST /api/approvals` | `approval_recorded` | `rule.hold.person_only`, `term.approval` |
| PH-RULE-01 | RULE | archive | Application A live-policy path. Application B `GET` lake `/v1/rules/at` | `limit_value` | `rule.recipe_release.limit`. Worked values: 2023 EMEA 18600, 2026 APAC 25000 |
| PH-BP7-01 | BP7 | injection | `POST /api/query` or agent run with IC-01 | `block` | `rule.untrusted_text.block`, `data.injection.partner_feeds` |

Freeze questions stay the freeze-set wording. SP-07 question: “This partner feed has processing_status REPLAY. Explain the duplicate.” Expected ids: `rule.feed.replay_duplicate`, `data.feed.replay`. Expected verdict: ANSWER.

SP-11 question: “Who is the follow-up owner of INC-2025-014?” Expected id: `decision.inc_2025_014`. Expected verdict: ABSTAIN. Owner stays empty until RT-06 supplies one.

PERSON row uses `action_type=recipe_hold_or_release`, `actor_role=RT-03`, `actor_id=demo-rt03-1`, `proposed_by` a different id. BO-03 stays PROPOSED. The person still writes the hold.

RULE row uses `rule_id=rule.recipe_release.limit`, `on_date=2023-07-01`, `sales_region=EMEA`. Expected limit 18600 USD. Honesty: REAL. A second check uses `on_date=2026-06-01`, `sales_region=APAC`, limit 25000 USD.

---

## How a difference is traced

A miss without a lake item id fails the harness.

| Kind of difference | Lake item the row must cite |
|---|---|
| Application B waits on a silent amount cutoff while Application A still applies the Python 50000 branch as transformed code | `rule.threshold.silent`, `rule.urgent.amount.impl.python` |
| Application B labels 50000 `proposed` while Application A shows it as an applied rank input | `rule.threshold.demo_50000`, `decision.bo08.silent_threshold` |
| Application B holds on site and stored region disagreement | `rule.region.disagreement` |
| Application B holds on no archive row | `rule.recipe_release.no_match` |
| Application B holds on overlap | `rule.policy.overlap_or_invalid` |
| Application B lists the 67 count from the lake item and Application A lists 67 packaged rows | Match on the integer 67. If the HTTP list length differs, cite `data.feed.replay` and `decision.fd06.two_apps` |
| Application A has no lineage view | `decision.fd06.two_apps`, `arch.graph.edges_table` |
| Application B missing a pin card | The missing card id. That is a lake finding |

Packaged amount above 50000 is 0. Honesty: REAL. PH-RANK-02 may still match on order and differ only on the label. The label cell still records the lake items.

---

## KPI families the harness informs

The harness names a family on each row. It does not set a target.

| Family | Rows that inform it | What stays Unknown |
|---|---|---|
| Decision quality | PH-S7-01, PH-S8-01, PH-S10-01, PH-RULE-01 | A quality percent |
| Business outcome | PH-RANK-01 | Exception cycle time. Aged backlog cutoff |
| AI quality | PH-CITE-01 | Groundedness percent floor (FD-14) |
| Reliability | PH-S11-02 | Recovery time |
| Engineering productivity | PH-S12-01 | A productivity percent |

BO-02 stays PROPOSED. The harness does not invent a cycle-time number.

---

## Runner and independence

Engineering decision ED-P11A-01 continued.

| Item | Value |
|---|---|
| Test path | `tests/platform/test_parity_harness.py` |
| Result file | `docs/model-comparison/parity-results.json` |
| Result section | Half B fills the empty table below |
| Application A base | `http://127.0.0.1:8100` |
| Application B base | `http://127.0.0.1:8110` |
| Lake pin check | Fail if Application B `lake_version` or sqlite hash disagrees with `app-b-pin.json` |
| Legacy-path check | `rg` on `apps/app_b/` for `fabpulse-legacy-workshop`. Zero hits required |
| App A import check | `rg` on `apps/app_b/` for `apps.app_a.rules`. Zero hits required |
| Stopped-A check | Start Application B. Leave Application A down. `GET /health` on 8110 returns 200. S7 to S11 and S12 still run |

The harness may start Application A for the two-app rows. The stopped-A check is a separate test. Application B does not call port 8100.

---

## Half B results

Filled after `python -m pytest tests/platform/test_parity_harness.py`. Honesty: REAL. Machine-readable copy: `docs/model-comparison/parity-results.json`.

| `harness_row_id` | `disposition_match` | `app_a_disposition` | `app_b_disposition` | `difference_lake_item_ids` | Honesty |
|---|---|---|---|---|---|
| PH-S7-01 | true | `duplicate_candidate=true` | `duplicate_candidate=true` | `[]` | REAL |
| PH-S7-02 | true | `67` | `67` | `[]` | REAL |
| PH-S8-01 | true | `recipe_version=R02`, `recipe_rev=R01` | `recipe_version=R02`, `recipe_rev=R01` | `[]` | REAL |
| PH-S9-01 | true | `event_time=2020-12-30T00:00:00+00:00`, `arrival_time=2021-01-01T00:00:00+00:00` | same pair | `[]` | REAL |
| PH-S10-01 | true | POL-0002, POL-0010, POL-0018, POL-0026, POL-0034 | same five ids | `[]` | REAL |
| PH-S11-01 | true | `owner_id` empty | `owner_id` empty | `[]` | REAL |
| PH-S11-02 | true | `owner_id` empty | `owner_id` empty | `[]` | REAL |
| PH-S12-01 | false | `view_absent` | item `rule.recipe_release.limit.v2023.emea`, `phase10_correlation_id=corr-p10b-doc-20261018-001`, 12 rows | `decision.fd06.two_apps`, `arch.graph.edges_table` | REAL |
| PH-RANK-01 | true | five scenario cases `open_operational=true` | same five flags | `[]` | REAL |
| PH-RANK-02 | false | label absent | label `proposed` | `rule.threshold.demo_50000`, `rule.threshold.silent`, `decision.bo08.silent_threshold` | REAL |
| PH-CITE-01 | true | verdict `ANSWER`, ids `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch` | same verdict and ids | `[]` | REAL |
| PH-PERSON-01 | true | decision `hold`, `engineering_hold=1` | decision `hold`, `engineering_hold=1` | `[]` | REAL |
| PH-RULE-01 | true | limit `18600` | limit `18600`. Second check 2026 APAC `25000` | `[]` | REAL |
| PH-BP7-01 | true | `block=true` | `block=true` | `[]` | REAL |

Matched row count: 12. Differing row count: 2. No percent is written.

Worked example. PH-S12-01. Application A has no lineage route. Application B returns the 2023 EMEA item and prints `corr-p10b-doc-20261018-001`. The miss cites `decision.fd06.two_apps` and `arch.graph.edges_table`.

Worked example. PH-RANK-02. Application A queue body has no amount cutoff label. Application B labels demo 50000 as `proposed` from `rule.threshold.demo_50000`. Live silent cutoff stays `HOLD_FOR_REVIEW` from `rule.threshold.silent`.

---

## What this file does not do

This file does not invent a match percent. It does not sign BO-06b or BO-08. It does not start Phase 12.
