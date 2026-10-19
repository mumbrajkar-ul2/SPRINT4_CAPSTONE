# Requirement disposition matrix

| Field | Value |
|---|---|
| Stage | Phase 16 / Final as-built PRD |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p16-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED. BO-13 stays PROPOSED. |
| Evidence sources | `docs/09-initial-prd/functional-requirements.md`; `docs/09-initial-prd/nfrs.md`; `docs/17-implementation-prd/implementation-prd.md`; `docs/17-implementation-prd/finalized-nfrs.md`; `docs/12-specs/acceptance-criteria.md`; `docs/13-traceability/requirements-traceability-matrix.md`; `docs/10-architecture/adrs/`; `docs/26-tevv/tevv-results.md`; `docs/34-after-kpis/after-intervention-kpi-sheet.md`; `docs/model-comparison/scorecard.md`; `docs/22-agentic-engineering/agent-test-results.md`; `docs/18-delivery/evidence-checklist.md`; `Decision_Tracker.md` BO-13 |
| Assumptions | `MODEL_MODE=replay`. Packaged 125-case file is the population. BO rows that are PROPOSED stay unsigned. |
| Unresolved issues | Exception cycle time Unknown. Aged backlog Unknown. Numeric percent floors Unknown. Company titles Unknown. INC-2025-014 owner Unknown. Live Azure NEEDS_HUMAN. Official Birlasoft assets not arrived. BO-13 unsigned. |
| Residual risks | Marking a row Delivered from a title with no spec, test, KPI, or ADR. Treating this unsigned matrix as a signed baseline. |

This file classifies every original requirement from the Initial PRD and the Implementation PRD. It does not copy those files. It does not add a feature.

Disposition values: Delivered, Changed, Deferred, Rejected, Superseded. Unknown is used when acceptance evidence is missing. Unknown waits for the Business Owner.

Engineering decision ED-P16-01, authority: team-force. Implementation platform rows use ids IP-01 to IP-10. Initial NFR rows use ids NFR-01 to NFR-33. SLO-B1 to SLO-B10 keep the Phase 8 ids. Evidence: `implementation-prd.md` platform sections; `finalized-nfrs.md`; `nfrs.md`.

---

## Finding

**Finding.** Fifteen functional requirements from the Initial PRD are classified. Fourteen are Delivered. FR-08 is Changed. Thirty-three NFR rows, ten Implementation platform rows, ten SLO-B rows, three deferred rows, one extra rejected row, and three extra Unknown rows are classified. Seventy-five rows in all. No Delivered row sits without a spec, a test, a KPI, or an ADR. Headline measures and percent floors stay Unknown. Hold prediction stays Rejected. Phase 8 app stubs are Superseded by the later Application A and Application B routes. BO-13 stays PROPOSED.
**Evidence.** Matrix below. `docs/12-specs/acceptance-criteria.md`. `docs/26-tevv/tevv-results.md`. `docs/model-comparison/scorecard.md`. `docs/22-agentic-engineering/agent-test-results.md`. `Decision_Tracker.md` BO-13.
**Impact.** Operations and audit can see what shipped and what still waits.
**Risk.** A later author who copies a Phase 3 sentence as if it were the as-built product.
**Confidence.** High on rows that cite a measured test. Unknown on headline clocks and live Azure.
**Open questions.** BO-13 signer. Cycle-time start and end fields. Aged-backlog age in days. Company titles. INC-2025-014 owner.

---

## How to read a row

| Column | Meaning |
|---|---|
| Source | Initial PRD or Implementation PRD |
| Disposition | Delivered, Changed, Deferred, Rejected, Superseded, or Unknown |
| Rationale | Why that label is the as-built fact |
| Evidence | A spec, a test, a KPI, or an ADR. Honesty of a measured number is REAL unless the cell says otherwise |

A Delivered row must have at least one of those four evidence kinds. If that link is missing, the row is Unknown.

Worked example. FR-01 is Delivered because PH-S8-01 shows recipe pair R02 and R01 on both applications. That test is in `docs/model-comparison/scorecard.md`. Spec AC-S8 sits in `docs/12-specs/acceptance-criteria.md`.

---

## Count

| Disposition | Count | Honesty |
|---|---|---|
| Delivered | 54 | REAL count of rows in this file |
| Changed | 3 | REAL count of rows in this file |
| Deferred | 3 | REAL count of rows in this file |
| Rejected | 2 | REAL count of rows in this file |
| Superseded | 1 | REAL count of rows in this file |
| Unknown | 12 | REAL count of rows in this file |
| Total | 75 | REAL |

---

## Functional requirements (Initial PRD FR-01 to FR-15)

Each block states finding, evidence, impact, risk, confidence, and open questions.

### FR-01 Recipe mismatch detection and approval route — Delivered

**Finding.** Both applications show step recipe R02 and tool recipe R01 on case PS000000016. The hold waits for RT-03. The model does not write `engineering_hold`.
**Evidence.** Spec AC-S8. Test PH-S8-01. KPI after-sheet recipe pair. Agent T-TRACE and T-KILL. ADR `adr-two-applications.md`. Honesty: REAL.
**Impact.** A reviewer sees both revisions on one case.
**Risk.** A later hold scorer would skip RT-03. FD-05 already rejects that scorer.
**Confidence.** High.
**Open questions.** Company title for Process Engineer. Person Unknown.
**Rationale.** Acceptance from the Initial PRD is met on the packaged fixture. No requirement text was rewritten.

### FR-02 Replay duplicate detection and confirmation — Delivered

**Finding.** Both applications mark `REPLAY-000000000` as a duplicate candidate. Both count 67 replay candidates. Dropping a replay waits for RT-05.
**Evidence.** Spec AC-S7. Tests PH-S7-01 and PH-S7-02. KPI replay candidate count 67. TEVV SP-07. Honesty: REAL.
**Impact.** A replay is visible as duplicate work.
**Risk.** A language guess that two lots look alike would drop a new feed. Ranking and de-duplication stay in code.
**Confidence.** High.
**Open questions.** Phase 2 did not run `reconcile()`. The 67 rows remain REPLAY in the packaged store.
**Rationale.** The identifier and status test is in place. The 67 count matches the packaged store.

### FR-03 Event time and arrival time kept apart — Delivered

**Finding.** Both applications show event time 2020-12-30 and arrival time 2021-01-01 as two fields.
**Evidence.** Spec AC-S9. Test PH-S9-01. TEVV SP-09. KPI clock pair. Honesty: REAL.
**Impact.** A late result stays a late result.
**Risk.** An invented month-end cut-off would skip the unsigned owner.
**Confidence.** High.
**Open questions.** Cut-off owner. Exception cycle time start and end fields stay Unknown.
**Rationale.** The two clocks are visible. The missing cut-off number is a known limitation, not a miss of this requirement.

### FR-04 One governed rule evaluation — Delivered

**Finding.** Application A evaluates pass or fail from transformed code. Application B evaluates the same archive item from the lake. Both return limit 18600 for 2023 EMEA. A second check returns 25000 for 2026 APAC.
**Evidence.** Spec AC-RULE. Test PH-RULE-01. ADR `adr-app-b-reads-only-the-lake.md`. KPI limit_value. Honesty: REAL.
**Impact.** Queue size and month-end totals can share one archive test when the lake holds the item.
**Risk.** A fifth wording of the same rule. Application B importing transformed code.
**Confidence.** High.
**Open questions.** Silent threshold still routes to review. Demo 50,000 stays PROPOSED (BO-08).
**Rationale.** The rule-source split from the Initial PRD is the as-built split.

### FR-05 Open and closed shown with one operational meaning — Delivered

**Finding.** Both applications count REVIEW and HOLD as open. Five scenario cases have `open_operational` true on both. Finance-closed and audit-closed stay separate labels.
**Evidence.** Spec AC-S13. Test PH-RANK-01. BO-06a DECIDED. KPI open_cases 89 for `status != CLOSED`. Honesty: REAL for those integers.
**Impact.** Both applications report the same operational open meaning on the fixture.
**Risk.** Merging finance-closed into operational-closed would book a number the owner has not signed. BO-06b stays PROPOSED.
**Confidence.** High on the operational meaning. Unknown on aged backlog.
**Open questions.** Aged backlog age threshold. Company titles. BO-06b signer.
**Rationale.** Operational meaning is in code. The three-state working answer is still unsigned and is listed as a known limitation.

### FR-06 Overlapping policy detect and abstain — Delivered

**Finding.** Both applications name five overlapping policy ids on FAB-00000002. The case waits. The model does not pick the policy.
**Evidence.** Spec AC-S10. Test PH-S10-01. TEVV SP-10 HOLD_FOR_REVIEW. BO-07 DECIDED. Honesty: REAL.
**Impact.** Overlap is visible as one wait, not as five independent flags.
**Risk.** Auto-selecting one policy would hide the overlap.
**Confidence.** High.
**Open questions.** None for the wait.
**Rationale.** Detect-and-wait is the as-built path.

### FR-07 Untrusted text isolated as data — Delivered

**Finding.** Approve-or-ignore text stays a flagged quote. Application A and Application B return HTTP 409 BLOCK on the named injection posts. After SC-26-01, Application B quotes-without-id approve on `REPLAY-000000000` returns HTTP 409 BLOCK and writes no record.
**Evidence.** Spec AC-BP7. Tests PH-BP7-01, HB-26-01 after, HB-26-02, TV-26-07, T-INJECT-01, T-INJECT-ALL. Honesty: REAL.
**Impact.** A feed note cannot close a case.
**Risk.** A later path that treats the note as an order.
**Confidence.** High on the measured HTTP rows. Unknown on live Azure injection.
**Open questions.** Live Azure.
**Rationale.** The control is measured on both applications.

### FR-08 Identity, owner assignment, and recovery status — Changed

**Finding.** A reader of a case on Application A or Application B must send `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role`. A missing set returns HTTP 401 `missing_identity`. Scenario 11 shows retry and a user-visible recovery status. RT-06 may assign a follow-up owner. INC-2025-014 `owner_id` stays empty. Port 8080 still serves cases with no identity check. The Initial PRD left identity design later and named no headers.
**Evidence.** Spec AC-S11. EH-01. Tests for 401 on 8100 and 8110 in Phase 8 and Phase 12. PH-S11-01 and PH-S11-02 empty `owner_id`. HB-25-06. Recovery GET in Phase 13. ADR `adr-ports-and-compose.md`. Implementation PRD ED-P8A-02. Honesty: REAL for the empty owner field and the 401 path.
**Impact.** Application A and Application B no longer copy the open 8080 GET. The packaged incident still has no named owner.
**Risk.** Writing `demo-rt06-1` as the INC-2025-014 owner. Copying the 8080 open path onto 8100.
**Confidence.** High on identity and on the empty owner field. Unknown on the company person who will assign the owner.
**Open questions.** INC-2025-014 owner. Company titles. Live Azure recovery time.
**Rationale.** The need is met. The mechanism was named after the Initial PRD. The incident owner cell stays Unknown. That is a change from a later-design statement to a named three-header check, with the owner name still empty.

### FR-09 Queue ranking from stored fields — Delivered

**Finding.** Queue order uses status, severity, and amount. It does not call a model. Two packaged cases are urgent from CRITICAL severity. Application A queue body has no amount cutoff label. Application B labels demo 50,000 as `proposed`. Live silent cutoff stays HOLD_FOR_REVIEW.
**Evidence.** Spec AC-RANK. Tests PH-RANK-01 and PH-RANK-02. FD-04. FD-05 117/125. Honesty: REAL.
**Impact.** The next case is chosen from stored fields.
**Risk.** Storing 50,000 as decided policy. Using 999,999 as a live limit.
**Confidence.** High.
**Open questions.** BO-08 signer.
**Rationale.** Ranking is code. The PH-RANK-02 difference is a lake label, not a model ranker.

### FR-10 Cited conflict explanation — Delivered

**Finding.** Scenarios 7 to 11 return a sentence that names both disagreeing values and cites lake item ids, or the model abstains. Freeze scored 42 of 42 cite-or-abstain. Replay sentences are PRECOMPUTED. Percent floors stay Unknown.
**Evidence.** Spec AC-CITE. Test PH-CITE-01. TEVV TV-26-01 42 of 42. KPI groundedness row. Honesty: REAL for the count. PRECOMPUTED for sentence wording. Floor Unknown.
**Impact.** A reader sees both values and the ids used.
**Risk.** Copying 42 of 42 into a 90 or 95 floor.
**Confidence.** High on the behavior. Unknown on a percent target.
**Open questions.** FD-14 percent floor.
**Rationale.** The required behavior is measured. The missing percent is a known limitation.

### FR-11 Cited natural-language answer — Delivered

**Finding.** Golden questions GQ-01 to GQ-26 and scenarios 7 to 13 can be asked in words. The answer cites a lake item or abstains. Forced ungrounded queries abstain.
**Evidence.** Spec AC-CITE. TEVV slice GQ-01 to GQ-26. TV-26-04 and TV-26-05. FD-10 26 questions. Honesty: REAL.
**Impact.** A person can ask in words and still receive a cited row.
**Risk.** Treating wording beyond this set as scored. Inventing a percent floor.
**Confidence.** High for the scored set. Unknown beyond that set.
**Open questions.** FD-14 and FD-18 numeric floors.
**Rationale.** The demo set is measured. Live Azure wording is not claimed.

### FR-12 Draft investigation plan, then wait — Delivered

**Finding.** The agent drafts a plan at `plan_draft`, then waits at `interrupt()`. A restart keeps the wait. The draft does not become a write until a person at RT-02 or the matching role records a choice. The proposer and the approver are different people.
**Evidence.** Spec AC-PERSON. Tests T-TRACE, T-RESTART, T-KILL, T-SEP, T-REPLAY. ADR `adr-langgraph-interrupt-approval.md`. Honesty: REAL.
**Impact.** Minutes 13 to 25 can show a draft and a gate.
**Risk.** Applying the draft without the approval row.
**Confidence.** High on the measured restart and separation check. Unknown on live Azure token cost.
**Open questions.** Live Azure. Company titles.
**Rationale.** Draft-then-wait is the as-built agent path.

### FR-13 Person on every record-changing action — Delivered

**Finding.** Hold, release, duplicate drop, policy pick, owner assign, and case disposition wait for the matching RT role. `WRITE_TOOLS` is empty. A resume with the same `actor_id` as `proposed_by` returns HTTP 403. BO-03 stays PROPOSED.
**Evidence.** Spec AC-PERSON. Tests PH-PERSON-01, T-NO-WRITE-TOOL, T-SEP. BO-09 DECIDED. Honesty: REAL for the tests. Verified Fact of the unsigned BO-03 row.
**Impact.** A wrong auto-action stops at review.
**Risk.** Treating the unsigned BO-03 row as signed code.
**Confidence.** High on the working path. Unknown on the signer name.
**Open questions.** BO-03 signer. Policy numbers behind PROPOSED rows.
**Rationale.** The behavior is measured. The signature is listed as a known limitation.

### FR-14 Same-scenario run on both applications — Delivered

**Finding.** The harness posted the same S7 to S11, RANK, CITE, PERSON, RULE, and BP7 inputs to Application A on 8100 and Application B on 8110. Fourteen rows. Twelve matched. Two differed. Each difference cites lake items. Application B does not call port 8100.
**Evidence.** Spec AC-S13. Test `tests/platform/test_parity_harness.py` print `PARITY matched=12 differing=2`. KPI harness integers. ADR `adr-two-applications.md`. FD-17. Honesty: REAL. No match percent.
**Impact.** A missing or extra lake item shows as a named difference.
**Risk.** Publishing 12 divided by 14 as a score.
**Confidence.** High.
**Open questions.** None for the integer compare.
**Rationale.** Scenario 13 is the as-built harness.

### FR-15 Rule lineage in the Application B context view — Delivered

**Finding.** Application B shows rule `rule.recipe_release.limit.v2023.emea`, correlation id `corr-p10b-doc-20261018-001`, and 12 T-TRACE steps. Application A returns `view_absent`. The view does not write a case.
**Evidence.** Spec AC-S12. Test PH-S12-01. ADR `adr-app-b-reads-only-the-lake.md`. KPI lineage view. Honesty: REAL.
**Impact.** A judge can see why Application B produced its result.
**Risk.** A view that edits a rule would skip governed change control.
**Confidence.** High.
**Open questions.** None for the read-only view.
**Rationale.** Lineage is Application B only, as the Initial PRD required.

---

## Implementation platform requirements

These rows come from the Implementation PRD. They serve BP1 to BP8. They do not add a ninth problem.

### IP-01 Host port map — Delivered

**Finding.** The running listeners are legacy 8080, source gateway 8090, lake REST 8091, lake MCP 8092, Application A 8100, Application B 8110.
**Evidence.** `compose.yaml`. ADR `adr-ports-and-compose.md`. FD-13. Health rows EV-H8080 to EV-H8110. Honesty: REAL for those health bodies.
**Impact.** The speaker can name six ports.
**Risk.** Replacing 8080 with Application A would hide the current-system baseline.
**Confidence.** High on the map. Unknown on a later live seven-container recreate.
**Open questions.** Who runs the next `docker compose up --build`.
**Rationale.** Phase 4 left Application A and Application B ports Unknown. Phase 8 named 8100 and 8110. Those are the ports that run.

### IP-02 Seven named containers — Delivered

**Finding.** `compose.yaml` names `fabpulse-legacy`, `fabpulse-source-gateway`, `fabpulse-bridge`, `fabpulse-lake-rest`, `fabpulse-lake-mcp`, `fabpulse-app-a`, and `fabpulse-app-b`.
**Evidence.** `compose.yaml`. `docker compose config` exit 0 in Phase 8. GNG-30-04 binds. Honesty: REAL for the file. Live recreate NEEDS_HUMAN.
**Impact.** One Compose file starts the stack.
**Risk.** Calling host uvicorn the finished seven-container run.
**Confidence.** High on the file. Unknown on a later recreate.
**Open questions.** Live Compose after the Phase 13 bind-mounts.
**Rationale.** The named set matches FD-13.

### IP-03 Identity scaffolding — Delivered

**Finding.** Application A and Application B require the three headers on case reads and writes. Lake REST and lake MCP require `X-Api-Key` except health. The documented local default `local-demo-only` lives in `.env.example`.
**Evidence.** Implementation PRD ED-P8A-02. EH-01. Phase 8 identity 401 checks. Phase 12 CLOSED_ROLES. Honesty: REAL.
**Impact.** A case body is not returned without an actor.
**Risk.** Hard-coding the key in application source.
**Confidence.** High.
**Open questions.** How a company would issue actor ids.
**Rationale.** The Phase 8 platform need is in place.

### IP-04 Lake REST on 8091 — Delivered

**Finding.** Port 8091 serves the Phase 6 read routes from lake version 1.0.0. POST to a write path returns HTTP 405 `lake_write_rejected`.
**Evidence.** Phase 8 lake tests. `api-contracts.md`. EV-H8091. Honesty: REAL.
**Impact.** Screens read lake items on a named port.
**Risk.** A lake write method.
**Confidence.** High.
**Open questions.** None for the read-only bound.
**Rationale.** The Implementation PRD lake listener is running.

### IP-05 Lake MCP on 8092 — Delivered

**Finding.** Port 8092 lists tools `search_items`, `get_item`, `get_links`, and `rule_at`. The lake file is read-only.
**Evidence.** EV-H8092 body. FD-13. Honesty: REAL.
**Impact.** Agents read the same lake as tools.
**Risk.** Binding both lake listeners to 8000.
**Confidence.** High.
**Open questions.** None for the four tools.
**Rationale.** The Implementation PRD MCP listener is running.

### IP-06 Replay wiring — Delivered

**Finding.** `MODEL_MODE=replay` plays back a file named by the SHA-256 hash of the prompt. A missing file returns `replay_miss` and opens no public-network socket. Seventy-seven replay files sit on disk besides README. Shown Application A replay tokens are prompt_tokens 0 and completion_tokens 0.
**Evidence.** `compose.yaml` default. `operations/model-replay/`. T-REPLAY. Phase 13 HB-32-01. Phase 15 file count 77. Honesty: REAL for the count and the zeros. PRECOMPUTED for file bodies.
**Impact.** The laptop path can start with the public network off.
**Risk.** Inventing a third offline mode.
**Confidence.** High on replay. Unknown on live Azure.
**Open questions.** Azure endpoint, deployment name, and API version.
**Rationale.** Replay is the as-built laptop model path.

### IP-07 Capstone CI — Delivered

**Finding.** Capstone `.github/workflows/verify.yml` runs tests, lake gates, compose config, and identity 401. It omits `python -m app.generate --reset`. It omits a live model call.
**Evidence.** GNG-30-07. Implementation PRD ED-P8A-06. Honesty: REAL.
**Impact.** A push does not replace the packaged store.
**Risk.** Re-adding `--reset`.
**Confidence.** High.
**Open questions.** GitHub runner availability on a later day.
**Rationale.** The CI bound from the Implementation PRD holds.

### IP-08 JSON request logs — Delivered

**Finding.** Listeners write one JSON object per line to stdout with `service`, `event`, `level`, and `correlation_id`.
**Evidence.** Implementation PRD ED-P8A-07. `docs/31-observability/telemetry-results.md`. Honesty: REAL for measured lines in that file.
**Impact.** A later walk can find a request by correlation id.
**Risk.** Treating those lines as the audit chain.
**Confidence.** High on the log shape. Unknown on numeric p95.
**Open questions.** API p95. Availability percent.
**Rationale.** Observability scaffolding is in place. Numeric floors stay Unknown.

### IP-09 Phase 8 app stubs only — Superseded

**Finding.** Phase 8 released health and identity stubs with no queue, case, approval, query, or lineage feature. Phase 9 built Application A scenario routes. Phase 11 built Application B scenario routes and the lineage view.
**Evidence.** `docs/17-implementation-prd/release-boundaries.md` Phase 8 increment. Phase 9 and Phase 11 tests. PH-S7-01 to PH-S12-01.
**Impact.** The stub bound was a release cut, not the final product.
**Risk.** Reading the Phase 8 stub list as the as-built feature set.
**Confidence.** High.
**Open questions.** None.
**Rationale.** Later phases replaced the stubs. The product requirements FR-01 to FR-15 remain the features.

### IP-10 One Compose command for a live six-port start — Changed

**Finding.** `compose.yaml` publishes the six host ports. `docker compose config` passed. Health bodies exist for all six listeners. A later live `docker compose up --build` recreate is NEEDS_HUMAN. Phase 15 did not start Compose.
**Evidence.** `compose.yaml`. EV-H8080 to EV-H8110. `docs/demo/paper-rehearsal.md`. GNG-30-02 live 8100 after recreate NEEDS_HUMAN. Honesty: REAL for the file and the prior health bodies. Unknown for a new recreate today.
**Impact.** The map is recorded. A person must start the stack for a room rehearsal.
**Risk.** Calling the paper walk a watched live stack.
**Confidence.** High on the file. Unknown on live health today.
**Open questions.** Who runs the first live Compose drill after handover.
**Rationale.** The Implementation PRD required one command. The file is present. A fresh live start is still a human step.

---

## Initial and Implementation NFR rows

### NFR-01 Local synthetic records — Delivered

**Finding.** Packaged records stay local and synthetic.
**Evidence.** FD-02. BO-10 working answer. T-READONLY-DB `mode=ro`. Honesty: REAL for the open mode.
**Impact.** The demo does not load customer data.
**Risk.** Pasting a live fab extract into the packaged file.
**Confidence.** High.
**Open questions.** BO-10 signer.
**Rationale.** The bound is in force.

### NFR-02 Model tools read-only — Delivered

**Finding.** The tool list that reaches the model has six read names. `WRITE_TOOLS` is empty.
**Evidence.** FD-02. T-NO-WRITE-TOOL. HB-25-07. Honesty: REAL.
**Impact.** The model cannot write a case from a tool call.
**Risk.** Adding a write name later.
**Confidence.** High.
**Open questions.** None for the empty write list.
**Rationale.** The Initial NFR is the as-built tool list.

### NFR-03 Record writes wait for a person — Delivered

**Finding.** Same as FR-13. A person records every write.
**Evidence.** AC-PERSON. PH-PERSON-01. T-SEP. Honesty: REAL.
**Impact.** A wrong auto-action stops at review.
**Risk.** Unsigned BO-03 treated as optional.
**Confidence.** High.
**Open questions.** BO-03 signer.
**Rationale.** Duplicate of FR-13, kept because the Initial NFR listed it separately.

### NFR-04 Untrusted text is data — Delivered

**Finding.** Same as FR-07.
**Evidence.** AC-BP7. HB-26-02. Honesty: REAL.
**Impact.** A note cannot close a case.
**Risk.** Instruction text copied into a system prompt.
**Confidence.** High.
**Open questions.** Live Azure.
**Rationale.** Same evidence as FR-07.

### NFR-05 Classification internal synthetic — Delivered

**Finding.** Working answer treats records as internal and synthetic. Process data is confidential. Packaged rows do not contain personal data. BO-10 stays PROPOSED.
**Evidence.** BO-10 working answer. Phase 12 governance files. Honesty: Verified Fact of the working answer. Signature Unknown.
**Impact.** Handling stays on the working answer.
**Risk.** Treating the unsigned row as a signed classification.
**Confidence.** High on the working text. Unknown on the signer.
**Open questions.** BO-10 signer.
**Rationale.** The handling is applied. The signature is a known limitation.

### NFR-06 No production hold predictor — Rejected

**Finding.** Predicting `engineering_hold` stays rejected. Majority guess 117 of 125. Leave-one-out logistic regression 117 of 125. No hold-scorer file sits under `apps/`.
**Evidence.** FD-05. `docs/09-initial-prd/non-goals.md`. HB-25-07 note that no `engineering_hold` model file sits under `apps/`. Honesty: REAL for 117/125.
**Impact.** Ranking and hold stay with stored fields and a person.
**Risk.** Adding a scorer later with no gain over the majority guess.
**Confidence.** High.
**Open questions.** None.
**Rationale.** The Initial PRD rejected this capability. The as-built product still rejects it.

### NFR-07 App independence — Delivered

**Finding.** Application A does not call Application B at run time. Application B does not call Application A at run time. Application B source has no inherited-repo path and no Application A rule import.
**Evidence.** AC-S13. Phase 11 reviewer check. ADR `adr-two-applications.md`. Honesty: REAL.
**Impact.** A down Application A does not hide an unfinished Application B.
**Risk.** A hidden HTTP call between the two ports.
**Confidence.** High.
**Open questions.** None.
**Rationale.** Independence is the as-built runtime.

### NFR-08 Same scenarios on both applications — Delivered

**Finding.** Scenarios 7 to 11 run on both applications with the same inputs.
**Evidence.** AC-S13. Parity harness. Honesty: REAL.
**Impact.** Differences are comparable.
**Risk.** Scoring the two apps on different cases.
**Confidence.** High.
**Open questions.** None.
**Rationale.** Same as FR-14 inputs.

### NFR-09 Same KPI families — Delivered

**Finding.** Both applications are scored on the eight families in Execution_Plan section 9. No invented target sits in those sheets.
**Evidence.** `docs/34-after-kpis/after-intervention-kpi-sheet.md`. FD-03. FD-20. Honesty labels on that sheet.
**Impact.** The scorecard can show labelled families.
**Risk.** Filling a target cell with 90 or 95.
**Confidence.** High.
**Open questions.** Headline clocks.
**Rationale.** Families exist. Targets stay empty.

### NFR-10 Headline exception cycle time — Unknown

**Finding.** Exception cycle time has no start field and no end field. After-intervention value is Unknown.
**Evidence.** BO-02. After-KPI sheet headline row. `app/baseline.py` still has no cycle-time field.
**Impact.** No cycle-time win is claimed.
**Risk.** Calling open_cases 89 a cycle-time win.
**Confidence.** High that the cell is empty.
**Open questions.** Start and end fields. Business Owner.
**Rationale.** No acceptance evidence for a delivered number. The row waits for the Business Owner.

### NFR-11 Headline aged backlog — Unknown

**Finding.** Aged backlog has no age threshold. Python `open_cases` is 89. That integer is not aged backlog.
**Evidence.** BO-02. After-KPI sheet. Honesty: REAL for 89. Unknown for aged backlog.
**Impact.** No aged-backlog win is claimed.
**Risk.** Calling 89 a reduced backlog.
**Confidence.** High that the threshold is missing.
**Open questions.** Age in days. Business Owner.
**Rationale.** Evidence for a delivered cutoff is missing.

### NFR-12 Honesty labels — Delivered

**Finding.** Demo and KPI numbers carry REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.
**Evidence.** FD-20. Scorecard. After-KPI sheet. Honesty: Verified Fact of those files.
**Impact.** A judge can see how a number was produced.
**Risk.** Dropping a label on a slide.
**Confidence.** High.
**Open questions.** None for the label set.
**Rationale.** The Initial NFR is applied on the measured sheets.

### NFR-13 Rule source split — Delivered

**Finding.** Application A reads rules from transformed code. Application B reads rules only from the lake.
**Evidence.** AC-RULE. ADR `adr-app-b-reads-only-the-lake.md`. PH-RULE-01. Honesty: REAL.
**Impact.** A missing lake item can show as an Application B difference.
**Risk.** Importing `legacy_logic.py` into Application B.
**Confidence.** High.
**Open questions.** None.
**Rationale.** Same as FR-04.

### NFR-14 No monetary benefit claim — Delivered

**Finding.** No dollar benefit is claimed. ROI cells stay EDUCATIONAL. Dollars stay Unknown.
**Evidence.** BO-11 working answer. `docs/36-benefits/verified-benefits.md`. `docs/36-benefits/benefits-signoff.md` UNSIGNED. Honesty: Verified Fact of those pages.
**Impact.** The as-built baseline does not invent a saving.
**Risk.** Copying 0.603 as recovered labor.
**Confidence.** High.
**Open questions.** BO-11 signer.
**Rationale.** The constraint is met by leaving the dollar cell empty.

### NFR-15 Identity on Application A and Application B — Delivered

**Finding.** Case reads and writes require the three headers.
**Evidence.** EH-01. Phase 8 and Phase 12 identity tests. Honesty: REAL.
**Impact.** A case body is not returned without an actor.
**Risk.** Copying the 8080 open GET.
**Confidence.** High.
**Open questions.** Company title map.
**Rationale.** The Initial identity need is implemented as the named headers.

### NFR-16 Legacy 8080 stays without an identity check — Delivered

**Finding.** Port 8080 still serves the current GET path with no identity header.
**Evidence.** CT-35. Implementation PRD ED-P8A-03. GNG-30-05. Honesty: REAL.
**Impact.** Minutes 0 to 8 can still show the current system.
**Risk.** Adding a key check on 8080 would hide the baseline.
**Confidence.** High.
**Open questions.** None.
**Rationale.** The Implementation NFR kept 8080 as the baseline.

### NFR-17 Gateway 8090 stays without an identity check — Delivered

**Finding.** Port 8090 stays the scenario 11 fixture.
**Evidence.** ED-P8A-03. GNG-30-05. Honesty: REAL.
**Impact.** Outage modes stay on the inherited gateway.
**Risk.** Wrapping 8090 with the three headers.
**Confidence.** High.
**Open questions.** None.
**Rationale.** The fixture stays open.

### NFR-18 Lake reads require X-Api-Key except health — Delivered

**Finding.** Ports 8091 and 8092 require the key on every route except health.
**Evidence.** ED-P8A-04. Phase 8 lake tests. Honesty: REAL.
**Impact.** A lake read without a key is rejected.
**Risk.** Leaving a write method on the lake.
**Confidence.** High.
**Open questions.** None.
**Rationale.** The Implementation NFR is in place.

### NFR-19 Approval recorded with actor — Delivered

**Finding.** A human approval writes an audit row with the actor.
**Evidence.** T-TRACE human_approval row. AC-PERSON. ADR `adr-audit-chain.md`. Honesty: REAL.
**Impact.** A later read can show who approved.
**Risk.** A write with no audit row.
**Confidence.** High.
**Open questions.** Company titles.
**Rationale.** Recording is measured.

### NFR-20 Audit row per agent step and approval — Delivered

**Finding.** Scenario 8 wrote 12 audit rows under one correlation id. Each row has 27 columns.
**Evidence.** T-TRACE. FD-23. ADR `adr-audit-chain.md`. Honesty: REAL.
**Impact.** A restart and a review can replay the same id.
**Risk.** Treating JSON request logs as that chain.
**Confidence.** High.
**Open questions.** None for the measured 12 rows.
**Rationale.** The Initial "audit later" need was built in Phase 10.

### NFR-21 User-visible recovery — Delivered

**Finding.** Scenario 11 and `GET /api/recovery` show retry and park status. Parked row `DLQ-28-BAD` and later `DLQ-30-ROLL` stay listed.
**Evidence.** AC-S11. HB-29-01. GNG-30-03. Honesty: REAL.
**Impact.** A failed intake stays visible.
**Risk.** Deleting a parked row to clean the list.
**Confidence.** High on the park list. Unknown on recovery-time seconds.
**Open questions.** Recovery time. Recovery point.
**Rationale.** Status is user-visible. Numeric RTO stays Unknown.

### NFR-22 Separation of duties — Delivered

**Finding.** The proposer and the approver are different people. A match returns HTTP 403 `forbidden_role`.
**Evidence.** BO-09. T-SEP. EH-02. Honesty: REAL.
**Impact.** One person cannot propose and approve the same write.
**Risk.** Reusing the same actor id on resume.
**Confidence.** High.
**Open questions.** Company titles that match RT-01 to RT-06.
**Rationale.** The Initial NFR is measured.

### NFR-23 Forty-minute demo path — Changed

**Finding.** The paper walk of the spoken blocks takes 39 minutes. Section 10 order is kept. Injection BLOCK and the pid 29320 restart appear in the script. Live six-port clicks were not run in that walk. Live Compose is NEEDS_HUMAN.
**Evidence.** `docs/demo/paper-rehearsal.md`. `docs/42-executive/demo-day-script.md`. FD-21 paper length. Honesty: REAL for the 39-minute sum. Unknown for live health today.
**Impact.** The path can be read in under 40 minutes. A room rehearsal still needs a person to start the stack.
**Risk.** Calling the paper walk a watched live demo.
**Confidence.** High on the paper sum. Unknown on live clicks.
**Open questions.** Who runs P1 in the pre-show list.
**Rationale.** The Initial PRD asked for the section 10 flow on a laptop. The script exists and times to 39. The live stack step is still a human step.

### NFR-24 Offline replay as the laptop model path — Delivered

**Finding.** Replay is the default. Live Azure stays NEEDS_HUMAN.
**Evidence.** FD-13. `compose.yaml`. Phase 15 replay file count 77. Honesty: REAL.
**Impact.** The laptop path does not need a public-network model call.
**Risk.** Setting `MODEL_MODE=azure` on the laptop without a person.
**Confidence.** High.
**Open questions.** Azure endpoint values.
**Rationale.** The Initial assumption is now the as-built default.

### NFR-25 Live tokens in replay are 0 on the shown path — Delivered

**Finding.** Shown Application A replay query writes prompt_tokens 0 and completion_tokens 0.
**Evidence.** Phase 13 HB-32-01. After-KPI cost row. Honesty: REAL for that path.
**Impact.** Replay does not spend live tokens on that path.
**Risk.** Calling those zeros an invoice saving.
**Confidence.** High on that path. Unknown on live Azure.
**Open questions.** Live Azure token count.
**Rationale.** Assumption A-W2 is measured on the shown path.

### NFR-26 Health of the six listeners — Delivered

**Finding.** Each listener has answered `GET /health`. Legacy returned `{"status": "ok", "service": "fabpulse-legacy"}`. Gateway returned `{"status": "ok", "service": "source-gateway", "domain": "High Tech"}`. Lake REST, Application A, and Application B returned `{"ok":true}`. Lake MCP returned HTTP 200 plus the four tool names.
**Evidence.** EV-H8080 to EV-H8110. Honesty: REAL for those dated bodies.
**Impact.** Liveness was shown once per listener.
**Risk.** Treating those dated bodies as a later recreate pass.
**Confidence.** High on the dated rows. Unknown on health today.
**Open questions.** Live recreate.
**Rationale.** The Implementation health need has dated REAL evidence.

### NFR-27 Availability percent — Unknown

**Finding.** Inherited 99.5 percent is not adopted. No project availability target exists.
**Evidence.** Initial `nfrs.md`. FD-19. GNG no-go NG-30-07.
**Impact.** No availability win is claimed.
**Risk.** Copying 99.5 into a go cell.
**Confidence.** High that the cell is empty.
**Open questions.** Business Owner if a later target is needed.
**Rationale.** Evidence for a delivered percent is missing.

### NFR-28 Recovery time — Unknown

**Finding.** Inherited 8 hours is not adopted. Measured recreate seconds stay Unknown.
**Evidence.** Initial `nfrs.md`. `docs/29-incident-bcdr/rto-rpo.md`.
**Impact.** No RTO win is claimed.
**Risk.** Writing 8 hours as this product's floor.
**Confidence.** High that the cell is empty.
**Open questions.** Business Owner.
**Rationale.** No signed recovery-time number.

### NFR-29 Recovery point — Unknown

**Finding.** Inherited 24 hours is not adopted.
**Evidence.** Initial `nfrs.md`. `rto-rpo.md`.
**Impact.** No RPO win is claimed.
**Risk.** Writing 24 hours as this product's floor.
**Confidence.** High that the cell is empty.
**Open questions.** Business Owner.
**Rationale.** No signed recovery-point number.

### NFR-30 API p95 — Unknown

**Finding.** `duration_ms` on a log line is a measured field for one request. It is not a p95 target.
**Evidence.** FD-11. FD-19. After-KPI performance row.
**Impact.** No latency win is claimed.
**Risk.** Copying one `duration_ms` as a p95.
**Confidence.** High that the target is empty.
**Open questions.** Business Owner.
**Rationale.** No governed millisecond target.

### NFR-31 Retrieval p95 — Unknown

**Finding.** No retrieval p95 target exists.
**Evidence.** Initial `nfrs.md`. After-KPI sheet.
**Impact.** No retrieval win is claimed.
**Risk.** Inventing a millisecond floor.
**Confidence.** High that the cell is empty.
**Open questions.** Business Owner.
**Rationale.** Evidence for a delivered number is missing.

### NFR-32 Groundedness, citation, and abstention percent floors — Unknown

**Finding.** Every scored AI answer cites a lake item or abstains. Freeze 42 of 42. Citation recall 40 of 41. Citation precision 79 of 79. Abstention 6 of 42. Expected-abstain 6 of 6. Those integers are REAL. The percent floors stay Unknown.
**Evidence.** TEVV TV-26-01 to TV-26-05. FD-14. FD-18. Honesty: REAL for integers. Unknown for floors.
**Impact.** Release uses the behavior gate, not a 90 or 95 line.
**Risk.** Copying 42 of 42 into a decided percent.
**Confidence.** High on the integers. Unknown on a later signed floor.
**Open questions.** Business Owner for any later floor.
**Rationale.** Behavior is Delivered under FR-10 and FR-11. The numeric floors have no acceptance evidence.

### NFR-33 Token cost in dollars — Unknown

**Finding.** Dollars stay Unknown. Replay zeros are not an invoice.
**Evidence.** After-KPI cost row. `docs/32-finops/`. BO-11.
**Impact.** No cost saving is claimed.
**Risk.** Multiplying 0.603 by a wage.
**Confidence.** High that the dollar cell is empty.
**Open questions.** Unit price. Business Owner.
**Rationale.** No invoice exists.

---

## Implementation SLO-B rows

These ten rows were carried forward in `finalized-nfrs.md`.

| Id | Statement | Disposition | Rationale | Evidence |
|---|---|---|---|---|
| SLO-B1 | A person approves every record-changing action | Delivered | Same as FR-13 | AC-PERSON. PH-PERSON-01. T-SEP |
| SLO-B2 | The proposer and the approver are different people | Delivered | Same as NFR-22 | T-SEP. BO-09 |
| SLO-B3 | Untrusted approve-or-ignore text stays data | Delivered | Same as FR-07 | HB-26-02. PH-BP7-01 |
| SLO-B4 | A GenAI answer cites a lake item or abstains | Delivered | Same as FR-10 and FR-11 | TV-26-01 42 of 42 |
| SLO-B5 | Application B takes rules only from the lake | Delivered | Same as FR-04 | ADR app-b-reads-only-the-lake. PH-RULE-01 |
| SLO-B6 | The two applications do not call each other at run time | Delivered | Same as NFR-07 | Phase 11 independence check. AC-S13 |
| SLO-B7 | Event time and arrival time stay two fields | Delivered | Same as FR-03 | PH-S9-01 |
| SLO-B8 | REVIEW and HOLD count as open | Delivered | Same as FR-05 | PH-RANK-01. BO-06a |
| SLO-B9 | A reader of a case on Application A or Application B has an identity | Delivered | Same as NFR-15 | EH-01. 401 tests |
| SLO-B10 | Every agent step and every human approval writes an audit row keyed by a correlation id | Delivered | Same as NFR-20 | T-TRACE 12 rows |

Each SLO-B row: finding is the statement; impact is the matching FR or NFR; risk is treating the row as a numeric SLO; confidence is High on the cited test; open questions follow the matching FR.

---

## Deferred rows

### DEF-01 Official Birlasoft brand assets — Deferred

**Finding.** Official Birlasoft files have not arrived. The deck stays on the neutral placeholder.
**Evidence.** BO-12 PROPOSED. `docs/demo/placeholder-deck.md`. Handover HA-07.
**Impact.** Rehearsal can proceed on the placeholder.
**Risk.** Claiming official brand sign-off.
**Confidence.** High that the files are absent.
**Open questions.** Who supplies the assets.
**Rationale.** The Implementation out-of-release list and BO-12 keep this later.

### DEF-02 Live Azure model path — Deferred

**Finding.** Azure endpoint, deployment name, and API version stay Unknown. Live Azure stays NEEDS_HUMAN. Replay is the laptop path.
**Evidence.** Phase 15 paper rehearsal. Model card. FD-13.
**Impact.** The demo uses saved files.
**Risk.** Marking a live Azure pass that was not run.
**Confidence.** High that the live path was not run.
**Open questions.** Who supplies the Azure values.
**Rationale.** The Implementation PRD said live model is not a Phase 8 Done test. It remains a human step.

### DEF-03 BO-13 as-built signature — Deferred

**Finding.** This matrix classifies every original requirement. Known limitations are listed. BO-13 stays PROPOSED. The sign-off file stays UNSIGNED.
**Evidence.** `Decision_Tracker.md` BO-13. `final-product-baseline-signoff.md`.
**Impact.** The phase may complete under the default. The baseline is not a signed gate.
**Risk.** Inventing a signer.
**Confidence.** High that the signature is absent.
**Open questions.** Named signer.
**Rationale.** SME recommendation: sign once every requirement is classified with evidence and the known limitations are listed. That classification is this file. The signature is still the owner's.

---

## Rejected rows

### REJ-01 Production `engineering_hold` predictor — Rejected

Covered as NFR-06. FD-05. 117/125 versus 117/125. Honesty: REAL.

### REJ-02 Ninth business problem — Rejected

**Finding.** No ninth business problem was added. Scope stays BP1 to BP8.
**Evidence.** BO-04 working answer. `non-goals.md`. This matrix has no FR-16.
**Impact.** The demo stays on the eight defects.
**Risk.** A later feature outside BP1 to BP8.
**Confidence.** High.
**Open questions.** None.
**Rationale.** The Initial PRD forbade a ninth problem. The as-built set still has fifteen FRs and no sixteenth problem.

---

## Unknown rows that wait for the Business Owner

These rows have no acceptance evidence for a delivered value.

| Id | What is missing | Why it waits | Evidence that the cell is empty |
|---|---|---|---|
| NFR-10 | Exception cycle time | No signed start and end fields | After-KPI headline row |
| NFR-11 | Aged backlog cutoff | No signed age in days | After-KPI headline row |
| NFR-27 | Availability percent | Inherited 99.5 not adopted | FD-19 |
| NFR-28 | Recovery time | Inherited 8 hours not adopted | `rto-rpo.md` |
| NFR-29 | Recovery point | Inherited 24 hours not adopted | `rto-rpo.md` |
| NFR-30 | API p95 | No governed millisecond target | FD-11 |
| NFR-31 | Retrieval p95 | No governed millisecond target | After-KPI sheet |
| NFR-32 | Groundedness, citation, abstention percent floors | FD-14 and FD-18 leave the floor empty | TEVV results |
| NFR-33 | Token cost in dollars | No invoice | FinOps sheets |
| UNK-01 | Company job titles for RT-01 to RT-06 | No company map | `business-rules.md` Person and title columns |
| UNK-02 | INC-2025-014 follow-up owner | RT-06 has not supplied a name | PH-S11-01. HB-25-06 |
| UNK-03 | Expert-label disposition percent | No expert-label set | After-KPI decision quality row |

---

## What this file does not do

This file does not copy the Initial PRD or the Implementation PRD. It does not add a feature. It does not mark a row Delivered without a spec, a test, a KPI, or an ADR. It does not invent a dollar benefit. It does not sign BO-13. It does not invent a signer.
