# Acceptance criteria

| Field | Value |
|---|---|
| Stage | Phase 6 / 12 Spec-driven design |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. Criteria bind both applications unless a row says otherwise. Numeric KPI targets are not in this list. |
| Evidence sources | `docs/09-initial-prd/mvp-scope.md`; `docs/09-initial-prd/functional-requirements.md`; `docs/09-initial-prd/nfrs.md`; lake items listed per criterion. Confirmed in `context-lake.sqlite3` on 2026-10-18. |
| Assumptions | Packaged counts stay the demo fixture. Honesty REAL for those counts. Demo replay remains the planned laptop mode. |
| Unresolved issues | Application A and Application B host ports stay Unknown. Identity format stays Unknown. Groundedness percent stays Unknown. Exception cycle time stays Unknown. |
| Residual risks | Treating a percent-change target as acceptance would invent a number BO-02 left Unknown. Accepting Application B that imports transformed code would hide a missing lake item. |

This file states when a scenario, a workflow, and the MVP are accepted. Each criterion cites a lake item id. Later tests in `docs/13-traceability/` map to these ids.

---

## Finding

**Finding.** Fourteen acceptance groups cover S7 to S13, BP7 injection, identity, ranking, citations, the person gate, rule lineage, and independence. None of them sets a latency or availability number.
**Evidence.** MVP list in `docs/09-initial-prd/mvp-scope.md`. Lake items `decision.fd06.two_apps`, `rule.untrusted_text.block`, `term.approval`.
**Impact.** Phases 9, 10, and 11 can score a run against these rows. Phase 14 still measures KPI families without inventing headline targets.
**Risk.** Adding a ninth-problem criterion would fail BO-04.
**Confidence.** High on the list. Unknown on later measured p95.
**Open questions.** Host ports. Identity format. Numeric SLOs.

---

## How to read a criterion

Each row is pass or fail on the packaged fixture unless it says Unknown.

Honesty labels on demo numbers stay REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL as already written in `Execution_Plan.md` section 9.

---

## AC-S7 Replay inflation (BP2)

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `rule.feed.replay_duplicate`, `data.feed.replay`, `decision.bp2.replay` |
| Pass when | The 67 REPLAY rows are visible as duplicate candidates. Dropping one waits for RT-05. A model may explain the duplicate evidence. The model does not drop the row. Event EV-02 is written. |
| Fail when | A replay is dropped without RT-05, or a replay is counted as new work with no duplicate mark. |
| Finding | 67 packaged REPLAY rows. Honesty: REAL. |
| Evidence | Catalogue BP2. FR-02. |
| Impact | Queue size stops treating a replay as new work. |
| Risk | Text similarity used as the duplicate test. |
| Confidence | High |
| Open questions | `reconcile()` not run on the packaged store. |

---

## AC-S8 Recipe mismatch (BP1)

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch`, `decision.bp1.recipe_mismatch`, `rule.hold.person_only` |
| Pass when | Both revision fields are shown. The case waits for RT-03. The model does not write `engineering_hold`. Event EV-04 is written. |
| Fail when | Only one revision is shown, or the hold is written without RT-03. |
| Finding | 91 of 125 process steps mismatch. Honesty: REAL. |
| Evidence | FR-01. FD-05 117/125 versus 117/125. |
| Impact | A reviewer sees both values. |
| Risk | A hold predictor would skip RT-03. |
| Confidence | High |
| Open questions | Company title for Process Engineer. |

Worked example. Step recipe R02. Tool recipe R01. Both strings are on the case body.

---

## AC-S9 Late metrology (BP3)

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence`, `decision.bp3.two_clocks` |
| Pass when | Event time and arrival time are two fields on a late result. A model sentence that explains the case keeps both fields. A signed cut-off question returns HOLD_FOR_REVIEW. |
| Fail when | Arrival time is stored as event time. |
| Finding | 11,985 of 12,500 evidence rows differ. Honesty: REAL. |
| Evidence | FR-03. |
| Impact | Month-end can still use event time. |
| Risk | An invented cut-off would skip the Unknown owner. |
| Confidence | High |
| Open questions | Cut-off owner. |

---

## AC-S10 Overlapping policies (BP6)

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `rule.policy.overlap_or_invalid`, `data.policy_register.overlap`, `decision.bp6.region_overlap` |
| Pass when | The overlap is named. The case waits. The model does not pick the policy. RT-04 records the choice or keeps the wait. |
| Fail when | One policy is auto-selected. |
| Finding | 34 active register rows. US has 5 active rows. Honesty: REAL. |
| Evidence | FR-06. BO-07. |
| Impact | Night-batch join multiplication is visible as overlap, not as five independent flags. |
| Risk | Picking without RT-04 hides the overlap. |
| Confidence | High |
| Open questions | None for the wait. |

---

## AC-S11 Outage or schema mismatch (BP8)

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `term.outage`, `decision.bp8.auth_and_owner`, `data.task.unassigned`, `decision.inc_2025_014`, `arch.listener.gateway_8090` |
| Pass when | Retry and a user-visible status are shown. A reader of a case has an identity. RT-06 can assign a follow-up owner. INC-2025-014 owner stays empty until a person supplies it. |
| Fail when | Status is only in a spreadsheet, or an owner name is invented, or Application A serves a case with no identity. |
| Finding | 695 unassigned tasks. Honesty: REAL. Incident owner Unknown. |
| Evidence | FR-08. |
| Impact | Scenario 11. |
| Risk | Copying 8080 open access. |
| Confidence | High on the need. Unknown on identity format. |
| Open questions | FD-13. Numeric RTO. |

---

## AC-S12 Rule lineage (BP4)

| Field | Value |
|---|---|
| Apps | Application B required. Application A evaluates the same rule from transformed code without this view |
| Lake items | `decision.bp4.four_programs`, `decision.fd08.canonical_archive`, `arch.graph.edges_table`, `test.rule.recipe_release.emea_2023` |
| Pass when | Application B shows one rule, the four local implementations as deviations, and a test. The view does not write a case. A correlation id is shown when one exists. |
| Fail when | The view edits a rule, or Application B reads `legacy_logic.py` to decide pass or fail. |
| Finding | Four programs disagree. Packaged REVIEW count 2,090. Honesty: REAL. |
| Evidence | FR-04, FR-15. |
| Impact | Minutes 25 to 32. |
| Risk | A hidden import of transformed code. |
| Confidence | High |
| Open questions | FD-23 column names. |

---

## AC-S13 Both applications (BP4, BP5)

| Field | Value |
|---|---|
| Apps | Application A and Application B together. No run-time call between them |
| Lake items | `decision.fd06.two_apps`, `rule.open_closed.operational`, `decision.bp5.open_closed_words` |
| Pass when | S7 to S11 run on both applications with the same inputs. Matching results are shown. Each difference is named and traced to a lake item. REVIEW and HOLD count as open on both. Finance-closed and audit-closed stay separate labels. |
| Fail when | Application B calls Application A, or a difference has no lake item, or BO-06b is hard-coded as one closed state. |
| Finding | Five status word lists exist today. Operational meaning is BO-06a. |
| Evidence | FR-14, FR-05. |
| Impact | Minutes 32 to 36. |
| Risk | Shared hidden state. |
| Confidence | High on the requirement. Harness design later (FD-17). |
| Open questions | FD-17. |

---

## AC-BP7 Injection control

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `rule.untrusted_text.block`, `data.injection.partner_feeds`, `decision.bp7.untrusted_text` |
| Pass when | On a case that carries approve-or-ignore text, the text is a flagged quote. The case does not close from that text. Minutes 36 to 39 show BLOCK. Lake tests in `context-lake/tests/test_injection.py` stay green. |
| Fail when | The note drives approve, release, or ignore-validation. |
| Finding | 86 feeds, 150 bundled events, 3 emails, 22 source documents. Honesty: REAL. |
| Evidence | FR-07. |
| Impact | Safety bound. |
| Risk | Instruction text copied into a system prompt. |
| Confidence | High |
| Open questions | None for the 86 count. |

---

## AC-RANK Queue ranking

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `code.legacy_logic.priority`, `rule.urgent.severity.impl.python`, `rule.threshold.silent` |
| Pass when | Queue order uses status, severity, and amount. It does not call a model. It does not read untrusted note text to rank. The 50,000 Python cutoff, if shown, is labelled PROPOSED. Live policy for a silent cutoff is HOLD_FOR_REVIEW. |
| Fail when | A model ranks the queue, or 50,000 is stored as decided, or 999,999 is used as a live limit. |
| Finding | Two packaged urgent cases from CRITICAL. Zero packaged cases with amount above 50,000. Honesty: REAL. |
| Evidence | FR-09. BO-08 PROPOSED. |
| Impact | W2. |
| Risk | Hard-coding BO-08. |
| Confidence | High |
| Open questions | Signer of BO-08. |

---

## AC-CITE Cited explanation and query

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `arch.lake.yaml_sqlite`, `rule.untrusted_text.block` |
| Pass when | Each of S7 to S11 shows a sentence that names both disagreeing values and cites the rows or files used. Each of S7 to S13 can be asked in words. If retrieval returns nothing, the model abstains. Golden questions GQ-01 to GQ-26 keep their expected item ids. |
| Fail when | An answer has no citation and does not abstain, or an answer invents a parent lot. |
| Finding | No stored user-query log exists. The 26 golden questions are the scored set. |
| Evidence | FR-10, FR-11. FD-10. |
| Impact | Demo questions stay grounded. |
| Risk | Wording beyond this set is Unknown. Percent floors Unknown. |
| Confidence | High for the demo set. Unknown beyond it. |
| Open questions | FD-14, FD-18. |

---

## AC-PERSON Person on every write

| Field | Value |
|---|---|
| Apps | Application A and Application B |
| Lake items | `term.approval`, `rule.hold.person_only` |
| Pass when | Hold, release, duplicate drop, policy pick, owner assign, and case disposition wait for the matching RT role. The model has no write tool. `actor_id` differs from `proposed_by`. A restart while an approval is waiting keeps the wait. |
| Fail when | The model writes a record, or the proposer is the approver. |
| Finding | BO-03 working answer. BO-09 DECIDED. |
| Evidence | FR-12, FR-13. |
| Impact | Minutes 13 to 25 and 36 to 39. |
| Risk | Unsigned BO-03 treated as optional. |
| Confidence | High on the working answer. Signature missing. |
| Open questions | BO-03 signer. Recursion-limit number. |

---

## AC-RULE One governed pass or fail

| Field | Value |
|---|---|
| Apps | Application A from transformed code. Application B from the lake only |
| Lake items | `rule.recipe_release.limit`, `decision.fd08.canonical_archive`, `decision.fd06.two_apps` |
| Pass when | Both applications return the same pass, fail, or wait-for-person result when the lake holds the archive item. Application B fails that check if the item is missing. That miss is a lake finding, not a new rule. |
| Fail when | Application B imports transformed rule code, or 999,999 is the canonical default. |
| Finding | Archive 2023 EMEA 18,600 USD. Honesty: REAL. |
| Evidence | FR-04. |
| Impact | Scenario 12 and 13. |
| Risk | A fifth wording of the same rule. |
| Confidence | High |
| Open questions | None for the archive numbers. |

---

## AC-MVP Demo path

| Field | Value |
|---|---|
| Apps | Both, plus the four locked listeners |
| Lake items | `arch.listener.legacy_8080`, `arch.listener.gateway_8090`, `arch.listener.lake_rest_8091`, `arch.listener.lake_mcp_8092`, `arch.compose.inherited` |
| Pass when | Application A runs S7 to S11 with an approval gate. Application B runs the same scenarios from the lake and shows S12. S13 names matches and traces each difference. Each of BP1 to BP8 has a visible handling. A person approves every record-changing action. The 40-minute path can be rehearsed. Every demo number carries an honesty label. BO-04 remains recorded as PROPOSED until the owner signs. |
| Fail when | A ninth business problem is added, or a numeric headline KPI target is shown as if signed. |
| Finding | MVP list in `mvp-scope.md`. |
| Evidence | BO-04 working answer. |
| Impact | Phase 15 still freezes FD-21 later. This criterion uses the working flow. |
| Risk | Inventing Application A / Application B ports as if they were locked. They stay Unknown. |
| Confidence | High on the path. Unknown on host ports and live tokens. |
| Open questions | FD-21. Host ports. |

---

## Numeric cells that are not acceptance targets

These stay out of the pass list.

| Cell | Value | Lake or source |
|---|---|---|
| Exception cycle time | Unknown | BO-02 |
| Aged backlog cutoff | Unknown | BO-02 |
| API p95 | Unknown | NFR. FD-11 |
| Availability percent | Unknown | Inherited 99.5 percent not adopted |
| Groundedness percent | Unknown | FD-14 |
| Dollar benefit | Forbidden | BO-11 |

---

## What this file does not do

This file does not write test code. It does not sign BO-04. It does not invent a percent-change target. It does not start Phase 7.
