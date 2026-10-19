# Event contracts

| Field | Value |
|---|---|
| Stage | Phase 6 / 12 Spec-driven design |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. FD-11 recommended. Transport and audit column list stay later. |
| Evidence sources | `docs/09-initial-prd/functional-requirements.md`; `docs/10-architecture/adrs/adr-audit-chain.md`; `docs/10-architecture/adrs/adr-langgraph-interrupt-approval.md`; `docs/10-architecture/adrs/adr-opa-gates.md`; lake items listed per event. Confirmed in `context-lake.sqlite3` on 2026-10-18. |
| Assumptions | Each event type below is one record the application writes. The audit chain stores agent steps and human approvals. A message bus product is not named. FD-23 still designs the column list. |
| Unresolved issues | How the correlation id is minted stays Unknown. Table or file name stays Unknown. Whether Application B writes to the same store as Application A stays Inference. Retention stays later. |
| Residual risks | Inventing Kafka topics or column names here would skip FD-23. Logging only to stdout would mix cases. Letting the language model be the only event writer would drop a step. |

This file names the event types both applications record. Each type traces to a PRD workflow or to a locked control. This file does not pick a queue product.

Engineering decision ED-P6-04, authority: team-force. The event type names and required payload fields below are the FD-11 event contract. Transport, file path, and column list stay with FD-23 and Phase 10.

---

## Finding

**Finding.** Twelve event types cover intake, ranking flags, investigation, the OPA verdict, the agent pause, the human approval, recovery, and injection BLOCK. Each row carries a correlation id.
**Evidence.** `docs/10-architecture/adrs/adr-audit-chain.md`. Lake items `decision.fd06.two_apps`, `term.approval`, `rule.untrusted_text.block`.
**Impact.** Phase 10 writes one audit row per agent step and per human approval. The types in this file are what those rows must distinguish.
**Risk.** One summary row per case would hide the approval as its own record.
**Confidence.** High on the type list. Unknown on the column names.
**Open questions.** FD-23 schema. Id minting. Application B store layout.

---

## Shared envelope

Every event record includes these fields. Extra transport headers stay later.

| Field | What it holds | Label |
|---|---|---|
| `event_type` | One name from the table below | Engineering decision ED-P6-04 |
| `correlation_id` | Joins every step of one case | Verified Fact of the locked audit idea |
| `occurred_at` | When the fact happened | Verified Fact of FR-03. Lake item `rule.clock.event_vs_arrival` |
| `recorded_at` | When this row was written | Verified Fact of FR-03. Arrival stays a second clock |
| `actor_id` | Person or `system`. Empty is an error on a human approval | Verified Fact of FR-08 |
| `actor_role` | `RT-01` to `RT-06`, or `system`, or `model_draft` | Verified Fact of BO-09 |
| `case_id` | The case when one exists | Verified Fact of `term.case` |
| `app` | `legacy`, `app_a`, `app_b`, `gateway`, or `lake` | Verified Fact of `decision.fd06.two_apps` |
| `lake_item_ids` | Citations used, possibly empty | Verified Fact of FR-10 |
| `opa_verdict` | `EXECUTE`, `HOLD_FOR_REVIEW`, `BLOCK`, or empty if OPA has not run | Verified Fact of the OPA ADR |

`occurred_at` and `recorded_at` stay two fields. They are not merged. Lake item `rule.clock.event_vs_arrival`. 11,985 of 12,500 evidence events already differ on those two clocks. Honesty: REAL.

The model may appear as `actor_role: model_draft` on a plan or explanation event. The model does not appear as the actor on a record-changing approval. Lake item `rule.hold.person_only`.

---

## Event types

### EV-01 FeedIntakeAccepted

| Field | Value |
|---|---|
| When it is written | A new feed is accepted |
| Workflow | W1 |
| Lake item | `term.source_message`, `code.partner_feeds.reconcile` |
| Extra payload | `feed_id`, `processing_status` |
| Human required | No |

### EV-02 FeedDuplicateCandidate

| Field | Value |
|---|---|
| When it is written | A feed is marked REPLAY or otherwise duplicate-candidate |
| Workflow | W1. Scenario 7 |
| Lake item | `rule.feed.replay_duplicate`, `data.feed.replay`, `term.replay`, `term.duplicate` |
| Extra payload | `feed_id`, `processing_status` (`REPLAY` or `DUPLICATE`), `waiting_role` (`RT-05`) |
| Human required | Drop waits for EV-09 with `action_type: replay_confirm` |

Worked example. 67 packaged partner feeds have `processing_status = 'REPLAY'`. Honesty: REAL. Each one can raise EV-02. None is dropped until RT-05 records a decision.

### EV-03 FeedRejected

| Field | Value |
|---|---|
| When it is written | A feed fails the written key, schema, or quantity test |
| Workflow | W1 |
| Lake item | `code.partner_feeds.reconcile` |
| Extra payload | `feed_id`, `reason` (`unsupported_schema` or `negative_quantity`) |
| Human required | No for the mark. A later disposition still waits if the case is open |

Untrusted note text is not a reject reason. Lake item `rule.untrusted_text.block`.

### EV-04 RecipeMismatchRaised

| Field | Value |
|---|---|
| When it is written | Dispatch `recipe_version` differs from equipment `recipe_rev` |
| Workflow | W3. Scenario 8 |
| Lake item | `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch`, `decision.bp1.recipe_mismatch` |
| Extra payload | `recipe_version`, `recipe_rev`, `waiting_role` (`RT-03`) |
| Human required | Yes. Hold or release is EV-09 |

Worked example. 91 of 125 process steps mismatch. Honesty: REAL. The event stores both revisions. It does not pick a winner.

### EV-05 ClocksKeptApart

| Field | Value |
|---|---|
| When it is written | A late result is shown with two clocks |
| Workflow | W3. Scenario 9 |
| Lake item | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence`, `decision.bp3.two_clocks` |
| Extra payload | `event_time`, `arrival_time` |
| Human required | A signed cut-off choice routes to HOLD_FOR_REVIEW. Cut-off owner is Unknown |

### EV-06 PolicyOverlapRaised

| Field | Value |
|---|---|
| When it is written | Two active policies match one object, or `valid_from` is after `valid_to` |
| Workflow | W3. Scenario 10 |
| Lake item | `rule.policy.overlap_or_invalid`, `data.policy_register.overlap`, `decision.bp6.region_overlap` |
| Extra payload | overlapping policy ids, `waiting_role` (`RT-04`) |
| Human required | Yes. Pick or keep-wait is EV-09 |

Worked example. US has 5 active `policy_register` rows. Honesty: REAL. One US object matching those rows raises EV-06. The model does not pick the policy.

### EV-07 OpaVerdictRecorded

| Field | Value |
|---|---|
| When it is written | Open Policy Agent returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK |
| Workflow | W4. Control on S7 to S11. Minutes 36 to 39 |
| Lake item | `rule.untrusted_text.block`, `rule.threshold.silent`, `rule.policy.overlap_or_invalid` |
| Extra payload | `verdict`, `proposed_action` |
| Human required | HOLD_FOR_REVIEW waits. BLOCK stops. EXECUTE on a record change still waits under BO-03 |

Rego rule bodies stay later (FD-16). The three verdict strings are locked.

Silent threshold (BO-08 PROPOSED) records HOLD_FOR_REVIEW. This event does not store 50,000 or 999,999 as a live policy number. Lake items `rule.threshold.silent`, `rule.threshold.never_999999`.

### EV-08 AgentStepRecorded

| Field | Value |
|---|---|
| When it is written | One LangGraph step finishes, including a read-only tool call, a draft sentence, or a draft plan |
| Workflow | W3, W4. Minutes 13 to 25 |
| Lake item | `term.approval`, `rule.hold.person_only` |
| Extra payload | `step_name`, `tool_name` (if any), `draft_present` (true or false) |
| Human required | The draft does not change a record |

LangGraph is the library that runs a named graph of steps. `interrupt()` stops the graph and saves state when a person must decide. SqliteSaver writes that saved state to a SQLite file. Recursion-limit number stays Unknown (FD-15). Tool names stay Unknown except the four lake-read tools.

`actor_role` on this event is `system` or `model_draft`. It is never a write.

### EV-09 HumanApprovalRecorded

| Field | Value |
|---|---|
| When it is written | A person at RT-01 to RT-06 records approve, hold, block, drop, keep-wait, or assign |
| Workflow | W4. FR-13 |
| Lake item | `term.approval`, `rule.hold.person_only` |
| Extra payload | `action_type`, `decision`, `proposed_by`, `actor_id`, `actor_role` |
| Human required | Yes. This is the write |

`actor_id` and `proposed_by` must differ. Company job titles stay Unknown. The SME role names in Group C are the contract.

A process restart mid-wait keeps the pending EV-09. SqliteSaver holds the pause. Minutes 36 to 39 show that restart.

### EV-10 OwnerAssigned

| Field | Value |
|---|---|
| When it is written | RT-06 assigns a follow-up owner |
| Workflow | W5. Scenario 11 |
| Lake item | `decision.inc_2025_014`, `data.task.unassigned`, `decision.bp8.auth_and_owner` |
| Extra payload | `owner_id` supplied by the person. Must not be invented |
| Human required | Yes |

Worked example. 695 workflow tasks have `assigned_to` empty. Honesty: REAL. INC-2025-014 follow-up owner is Unknown. EV-10 stays unwritten for that incident until a person at RT-06 supplies a name.

### EV-11 RecoveryStatusChanged

| Field | Value |
|---|---|
| When it is written | Retry starts, retry ends, or schema mismatch is shown |
| Workflow | W5. Scenario 11 |
| Lake item | `term.outage`, `arch.listener.gateway_8090` |
| Extra payload | `status` visible to the user, `error_class` (`timeout`, `schema`, `rate_limit`) |
| Human required | Owner assign is EV-10. Status itself is user-visible without a numeric RTO |

### EV-12 InjectionBlocked

| Field | Value |
|---|---|
| When it is written | Retrieved text is an injection locator and the proposed action is approve, release, ignore-validation, or close-from-text |
| Workflow | BP7 control. Minutes 36 to 39 |
| Lake item | `rule.untrusted_text.block`, `data.injection.partner_feeds`, `decision.bp7.untrusted_text` |
| Extra payload | `block: true`, quote in `untrusted_quotes`, `proposed_action` |
| Human required | No approval is offered. The case stays unchanged |

Worked example. 86 partner feeds carry auto-approve or disregard-validation language. Honesty: REAL. Those strings stay in `untrusted_quotes`. EV-12 records BLOCK.

---

## What is not an event type in this spec

| Omitted | Why |
|---|---|
| Model-written audit paragraph as the only record | The chain is one row per step written by the application |
| A finance-closed or audit-closed auto event | BO-06b stays PROPOSED. Mismatch routes to review |
| A numeric SLO breach event | No numeric target exists |
| Cross-app call events | The two applications do not call each other |

---

## What this file does not do

This file does not invent the audit column list. It does not pick a message bus. It does not set the recursion-limit number. It does not start Phase 10.
