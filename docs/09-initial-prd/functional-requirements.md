# Functional requirements

| Field | Value |
|---|---|
| Stage | Phase 3 / 9 Initial PRD and product intent |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p3-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED with the initial PRD. |
| Evidence sources | `docs/05-current-state/conflict-catalogue.md`; `docs/08-ai-qualification/` (seven files); `Project_Intent.md` sections 8, 10, 15.2; `Execution_Plan.md` sections 3, 8, 10; `Decision_Tracker.md` BO-03, BO-06a, FD-04, FD-05, section 7 |
| Assumptions | Each requirement binds Application A and Application B unless the row says otherwise. BO-03 working answer holds for every write. |
| Unresolved issues | Groundedness and abstention numeric floors stay Unknown (FD-14, FD-18). Company job titles stay Unknown. Aged backlog cutoff stays Unknown. |
| Residual risks | A requirement that names a ninth problem would fail the Phase 3 Done test. A requirement that lets a model write a record would ignore BO-03. |

One requirement per feature. Each traces to a business problem BP1 to BP8. This file does not specify implementation code.

For every requirement: finding, evidence, impact, risk, confidence, open questions.

---

## FR-01 Recipe mismatch detection and approval route

| Field | Value |
|---|---|
| Feature | F-01 |
| Business problem | BP1 |
| Apps | Application A and Application B |
| Demo | Scenario 8 |

**Finding.** 91 of 125 process steps have a `recipe_version` that differs from the joined tool `recipe_rev`. Both values must be visible. A Process Engineer at RT-03 approves a hold or a release.

**Evidence.** Catalogue BP1 query result 91. Honesty: REAL. Intent 15.2 scenario 8. Decision_Tracker RT-03. FD-04: compare in code, explain with a language model.

**Impact.** A reviewer who reads only the step, or only the tool, sees a different revision today. The requirement puts both revisions on one case.

**Risk.** A model that writes `engineering_hold` would skip RT-03. FD-05 already rejects a hold predictor.

**Confidence.** High.

**Open questions.** Company title for Process Engineer is Unknown. Person Unknown.

**Acceptance.** On a packaged mismatch, both revision fields are shown. The case waits for RT-03. The model does not write `engineering_hold`.

Worked example. Step recipe R02. Tool recipe R01. Code raises the mismatch. A model may name both values and cite the two columns. The Process Engineer approves the hold or the release.

---

## FR-02 Replay duplicate detection and confirmation

| Field | Value |
|---|---|
| Feature | F-02 |
| Business problem | BP2 |
| Apps | Application A and Application B |
| Demo | Scenario 7 |

**Finding.** 67 partner feeds are stored as REPLAY. Duplicate intake is an identifier and status test. An Operations Analyst at RT-05 confirms before a duplicate is dropped.

**Evidence.** Catalogue BP2 query result 67. Honesty: REAL. Phase 2 reconciliation and de-duplication labels: code. Intent 10.2 keeps final reconciliation in code.

**Impact.** Replay rows sit with 8,000 NEW rows today. A count of unfinished feeds treats a replay as new work.

**Risk.** A language guess that two lots "look alike" can drop a new feed.

**Confidence.** High.

**Open questions.** Phase 2 did not run `reconcile()`. The 67 rows remain REPLAY in the packaged store. **Verified Fact.**

**Acceptance.** The 67 REPLAY rows are visible as duplicate candidates. Dropping one waits for RT-05. A model may explain the duplicate evidence.

---

## FR-03 Event time and arrival time kept apart

| Field | Value |
|---|---|
| Feature | F-03 |
| Business problem | BP3 |
| Apps | Application A and Application B |
| Demo | Scenario 9 |

**Finding.** 11,985 of 12,500 evidence events have `arrival_time` different from `event_time`. 45 overlapping reference-version pairs exist. Both clocks stay visible. Overlapping effective dates stay visible.

**Evidence.** Catalogue BP3. Honesty: REAL. Intent 15.2 scenario 9. FD-04: the split stays in code. A language model may explain a late result.

**Impact.** A late result can be read as a current fact if arrival time is used as event time.

**Risk.** Month-end cut-off and late-event handling will disagree if the two clocks are merged.

**Confidence.** High.

**Open questions.** No signed cut-off owner. Exception cycle time start and end fields stay Unknown.

**Acceptance.** Scenario 9 shows event time and arrival time as two fields on a late result. A model that explains the case keeps both fields.

---

## FR-04 One governed rule evaluation

| Field | Value |
|---|---|
| Feature | F-04 |
| Business problem | BP4 |
| Apps | Application A from its rebuilt program. Application B from the Context Lake only |
| Demo | Scenario 12 |

**Finding.** Four programs apply different tests. Packaged REVIEW count is 2,090. Pass or fail stays a written test against the governed archive.

**Evidence.** Catalogue BP4. Honesty: REAL. FD-08: governed, effective-dated archive is canonical. FD-04: rule evaluation is code. Intent 10.2.

**Impact.** Queue size and month-end totals can share one test.

**Risk.** A model result would be a fifth test of the same rule.

**Confidence.** High.

**Open questions.** A silent threshold still routes to review (BO-08 PROPOSED). Demo value, if needed later, is the Python 50,000 cutoff and stays PROPOSED. Never use 999,999 as a live policy number.

**Acceptance.** Both applications return the same pass, fail, or wait-for-person result when the lake holds the archive item. Application B fails that check if the item is missing. That miss is a lake finding, not a new rule.

---

## FR-05 Open and closed shown with one operational meaning

| Field | Value |
|---|---|
| Feature | F-05 |
| Business problem | BP5 |
| Apps | Application A and Application B |
| Demo | Scenario 13 |

**Finding.** 89 of 125 cases have `status != 'CLOSED'`. Five word lists name in-progress work with different words. Operational meaning is already decided: REVIEW and HOLD are open. Closed requires a final disposition and no pending engineering action.

**Evidence.** Catalogue BP5. Honesty: REAL for 89 and for the five lists. BO-06a DECIDED. BO-06b working answer keeps operational, finance, and audit closure as three states.

**Impact.** Two systems can report a different open count for the same week.

**Risk.** A backlog number moves when the word list changes. Merging finance-closed into operational-closed would book a number the owner has not signed.

**Confidence.** High on the operational meaning. Aged backlog cutoff is Unknown.

**Open questions.** Aged backlog age threshold stays Unknown. Company titles stay Unknown. BO-06b stays PROPOSED.

**Acceptance.** Both applications count a REVIEW or HOLD case as open. Scenario 13 names any A-versus-B difference in that count and traces it to a lake item. Finance-closed and audit-closed stay separate labels.

---

## FR-06 Overlapping policy detect and abstain

| Field | Value |
|---|---|
| Feature | F-06 |
| Business problem | BP6 |
| Apps | Application A and Application B |
| Demo | Scenario 10 |

**Finding.** 34 active `policy_register` rows sit on eight country codes. Each country code has 4 or 5 active rows. Three region vocabularies exist. When two policies overlap, the application waits. A Policy Owner at RT-04 picks a policy or keeps the wait.

**Evidence.** Catalogue BP6. Honesty: REAL. Intent 15.2 scenario 10. BO-07 DECIDED: site code is the canonical key; where two scopes disagree, the case routes to review. FD-04: detect in code, explain with a language model.

**Impact.** One object can match several active thresholds on the same country code. The night batch join multiplies one object into several flagged rows.

**Risk.** Picking a policy without RT-04 would hide the overlap.

**Confidence.** High.

**Open questions.** FD-09 (the stored region map) is later. This requirement still shows the overlap and waits.

**Acceptance.** Scenario 10 names the overlap and waits. The model does not pick the policy. RT-04 records the choice.

---

## FR-07 Untrusted text isolated as data

| Field | Value |
|---|---|
| Feature | F-07 |
| Business problem | BP7 |
| Apps | Application A and Application B |
| Demo | Control on scenarios 7 to 11. Minutes 36 to 39 |

**Finding.** Packaged text tells a reader to approve, ignore, or release. Counted stores: 86 partner feeds, 150 bundled lake events, 3 emails, 22 source documents.

**Evidence.** Catalogue BP7. Honesty: REAL. Phase 2 boundary: those strings stay data. FD-02: read-only tools.

**Impact.** A person or a later model can treat a feed note as a decision.

**Risk.** A hold can be released from untrusted text.

**Confidence.** High.

**Open questions.** None for the counts.

**Acceptance.** On a case that carries approve-or-ignore text, the text is visible as a flagged quote. The case does not close from that text. Minutes 36 to 39 show an injection that is blocked.

---

## FR-08 Identity, owner assignment, and recovery status

| Field | Value |
|---|---|
| Feature | F-08 |
| Business problem | BP8 |
| Apps | Application A and Application B |
| Demo | Scenario 11 |

**Finding.** The current GET API has no identity check. 695 workflow tasks have no assignee. INC-2025-014 follow-up owner is Unknown. Recovery today is manual.

**Evidence.** Catalogue BP8. Honesty: REAL for 695 and for the missing identity check. Unknown for the incident owner. Intent 15.2 scenario 11. RT-06.

**Impact.** Anyone who can reach the current legacy port can read cases. A disputed outage has no named owner.

**Risk.** Recovery stays a spreadsheet, as on 2025-11-18 at 04:00 UTC.

**Confidence.** High on the gap. Design of identity is later (FD-13, FD-18 PENDING).

**Open questions.** Identity design stays later. INC-2025-014 owner stays Unknown until a person assigns one at RT-06. Do not invent a name.

**Acceptance.** Scenario 11 shows retry and a user-visible status after an outage or schema mismatch. A reader of a case has an identity. RT-06 can assign a follow-up owner. This requirement does not specify servers or ports.

---

## FR-09 Queue ranking from stored fields

| Field | Value |
|---|---|
| Feature | F-09 |
| Business problem | BP4 (four ranking tests). BP5 (open queue) |
| Apps | Application A and Application B |
| Demo | Queue under scenarios 7 to 11 |

**Finding.** Ranking is a four-branch function on status, severity, and amount. Two packaged cases are urgent from CRITICAL severity. Zero packaged cases have `amount > 50000`. Predicting `engineering_hold` scored 117 of 125, matching the majority guess.

**Evidence.** Phase 2 matrix row for triage. `app/legacy_logic.py` cited in that note. FD-04 deterministic. FD-05 117/125. Honesty: REAL.

**Impact.** The next case to touch is chosen by stored fields.

**Risk.** A hold-probability column would change order with no gain over the majority guess.

**Confidence.** High.

**Open questions.** None for ranking. Language about why a case is next is FR-10.

**Acceptance.** Queue order uses status, severity, and amount. It does not call a model. It does not read untrusted note text to rank.

---

## FR-10 Cited conflict explanation

| Field | Value |
|---|---|
| Feature | F-10 |
| Business problem | BP1 to BP7 (each is a disagreement type) |
| Apps | Application A and Application B |
| Demo | Scenarios 7 to 11 |

**Finding.** Code can raise a mismatch flag. A reader needs a cited sentence that names both values. Measured variety: 13 case notes in three languages, 210 emails, 12,500 evidence payloads, ten disagreement types.

**Evidence.** Catalogue BP1 to BP7 counts. Phase 2 text-variety table. Intent 10.1. FD-04 GenAI for the sentence.

**Impact.** Demo scenarios 7 to 11 can show the two values and an explanation.

**Risk.** Instruction text in 86 feeds and 150 lake rows can be copied into the draft.

**Confidence.** High.

**Open questions.** Citation and abstention numeric floors stay Unknown (FD-14, FD-18).

**Acceptance.** Each of S7 to S11 shows a sentence that names both disagreeing values and cites the rows or files used. If retrieval returns nothing, the model abstains.

---

## FR-11 Cited natural-language answer

| Field | Value |
|---|---|
| Feature | F-11 |
| Business problem | BP1 to BP8 through the seven demo jobs |
| Apps | Application A and Application B |
| Demo | Scenarios 7 to 13 |

**Finding.** The seven demo jobs are seven different English requests. Code fetches the row or lake item. A language model drafts the cited answer. No stored user-query log exists.

**Evidence.** Intent 15.2. Phase 2 natural-language-query row. FD-04 GenAI. FD-10 (golden questions) is later.

**Impact.** A person can ask in words and still receive a cited row.

**Risk.** Wording beyond scenarios 7 to 13 is Unknown.

**Confidence.** High for the demo set. Unknown beyond that set.

**Open questions.** FD-10 later freezes the golden questions.

**Acceptance.** Each of S7 to S13 can be asked in words. The answer cites a stored row or a lake item, or the model abstains.

---

## FR-12 Draft investigation plan, then wait

| Field | Value |
|---|---|
| Feature | F-12 |
| Business problem | BP1, BP2, BP6, BP8 (investigation, feed disposition, policy wait, missing owner) |
| Apps | Application A and Application B |
| Demo | Agent trace, minutes 13 to 25 |

**Finding.** Draft plans, tests, and handoffs are language jobs. Writes stay with a person. Intent names five draft jobs: investigation, feed disposition, change-impact, evidence pack, and handoff. This PRD keeps those five jobs inside the eight business problems. Change-impact and evidence pack serve BP4 rule trace and BP8 recovery. They do not add a ninth problem.

**Evidence.** Intent 10.1 and 10.3. BO-03 working answer. RT-02. FD-04 GenAI for planning. FD-02 read-only tools.

**Impact.** A reviewer receives a proposed next step with citations.

**Risk.** Applying the draft without RT-02 approval writes a record. A wrong write can scrap material. **Verified Fact** of the SME reason in section 5.1.

**Confidence.** High on the bound. Later plan wording is Inference.

**Open questions.** FD-15 later sets the tool allow-list and recursion limit.

**Acceptance.** Minutes 13 to 25 show a draft plan and an approval gate. The draft does not become a write until RT-02 records a choice. The proposer and the approver are different people (BO-09).

---

## FR-13 Person on every record-changing action

| Field | Value |
|---|---|
| Feature | F-13 |
| Business problem | BP1, BP2, BP6, BP8 (every path that changes a record) |
| Apps | Application A and Application B |
| Demo | Approval gate on scenarios 7, 8, 10, and 11 |

**Finding.** A person approves every record-changing action. The model explains and proposes. The tracker row is PROPOSED. The Business Owner accepted it on 2026-10-18.

**Evidence.** BO-03 working answer. Section 5.1 SME recommendation. Phase 2 `minimum-agency-assessment.md`. RT-01 to RT-06.

**Impact.** A wrong auto-action stops at review.

**Risk.** A later path that writes `cases.status` or `wafer_lots.engineering_hold` from a model proposal would apply a PROPOSED bound as if it were signed code.

**Confidence.** High on the working answer. The signature is still missing.

**Open questions.** Signer name Unknown. Policy numbers behind PROPOSED rows still wait for a person. The case stays in review until that person acts.

**Acceptance.** Hold, release, duplicate drop, policy pick, owner assign, and case disposition wait for the matching RT role. The model has no write tool.

---

## FR-14 Same-scenario run on both applications

| Field | Value |
|---|---|
| Feature | F-14 |
| Business problem | BP4, BP5 (rule drift and open-count drift are what parity exposes) |
| Apps | Application A and Application B together |
| Demo | Scenario 13 |

**Finding.** Application A reads rules from its rebuilt program. Application B reads rules only from the Context Lake. Both run scenarios 7 to 11 with the same inputs. Each difference traces to a lake item.

**Evidence.** Intent section 8. Execution_Plan sections 4 and 8. Catalogue BP4 (four rule files) and BP5 (five status lists) as the Phase 1 findings that parity must expose.

**Impact.** A missing lake item shows up as a wrong Application B result.

**Risk.** Shared hidden state between the two applications would hide an unfinished workflow.

**Confidence.** High on the requirement. The harness design (FD-17) is later.

**Open questions.** FD-17 PENDING. This requirement still names the comparison. It does not specify the harness code.

**Acceptance.** Scenario 13 runs S7 to S11 on both applications. Matching results are shown. Each difference is named and traced to a lake item.

---

## FR-15 Rule lineage in the Application B context view

| Field | Value |
|---|---|
| Feature | F-15 |
| Business problem | BP4 |
| Apps | Application B required. Application A evaluates the same rule without this view |
| Demo | Scenario 12 |

**Finding.** Four local programs disagree. The demo must trace one rule from a historical decision and code to a specification and a test.

**Evidence.** Catalogue BP4. Intent 15.2 scenario 12. Execution_Plan section 10 minutes 25 to 32.

**Impact.** A judge can see why Application B produced its pass-or-fail result.

**Risk.** A view that edits a rule would skip governed change control. This view is read-only.

**Confidence.** High.

**Open questions.** Lake item schema is later (FD-07 PENDING). This requirement still asks for the trace.

**Acceptance.** Scenario 12 on Application B shows one rule, the four local implementations as deviations, and a test. The view does not write a case.

---

## What this file does not do

This file does not specify implementation code. It does not add a requirement outside BP1 to BP8. It does not invent a citation percent, a cycle-time number, or a dollar benefit.
