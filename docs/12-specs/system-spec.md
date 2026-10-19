# System specification

| Field | Value |
|---|---|
| Stage | Phase 6 / 12 Spec-driven design |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. FD-11 recommended, authority: team-force. Numeric latency, availability, and SLO numbers stay Unknown. |
| Evidence sources | `docs/09-initial-prd/`; `docs/10-architecture/`; `Decision_Tracker.md` FD-11, BO-09, Group C; lake 1.0.0 in `context-lake/generated/context-lake.sqlite3` (148 accepted or draft items). Confirmed read-only on 2026-10-18. |
| Assumptions | BO-03 working answer holds: a person approves every record-changing action. Demo replay (`MODEL_MODE=replay`) remains the planned laptop mode. Lake version 1.0.0 holds. |
| Unresolved issues | Application A and Application B host ports stay Unknown. Identity mechanism stays later (FD-13, FD-18). API p95, retrieval p95, availability percent, recovery time, and recovery point stay Unknown. Company job titles stay Unknown. BO-06b and BO-08 stay PROPOSED. |
| Residual risks | Copying 99.5 percent availability from inherited notes would invent a target. Adding a ninth business problem, or an API outside the initial PRD, would grow the product past BO-04. Writing 50,000 or 999,999 as a live policy number would treat a PROPOSED row as code. |

This file names the system both applications must satisfy. It names the scenarios, the workflows, and the service-level behaviours. It does not write code. It does not invent a latency number.

---

## FD-11 recommended answer

**Authority:** team-force. **Status in the tracker:** DEFERRED until the coordinator records acceptance.

**Recommended text.** Specify the HTTP and MCP contracts, the event records, the error families, and the behavioural service needs in `docs/12-specs/`. Keep every numeric latency, availability percent, recovery time, recovery point, API p95, retrieval p95, groundedness percent, citation percent, and abstention percent as Unknown. Do not copy the inherited 99.5 percent availability note. Do not copy the inherited 8-hour recovery note. Do not copy the inherited 24-hour recovery-point note. Phase 13 (FD-19) measures reliability numbers later. Phase 9 (FD-14) and Phase 12 (FD-18) set language-model quality floors later. Identity design stays Phase 8 and Phase 12 (FD-13, FD-18). After the reviewer accepts these specs, the coordinator may mark FD-11 DECIDED with this answer.

**Label.** Inference from the Phase 6 prompt, `docs/09-initial-prd/nfrs.md`, and `Decision_Tracker.md` FD-11 default. The numeric cells are Unknown.

---

## Finding

**Finding.** Two independently running FastAPI and React applications, one generated Context Lake on ports 8091 and 8092, the inherited legacy API on 8080, and the inherited source gateway on 8090, together run workflows W1 to W7 on business problems BP1 to BP8.
**Evidence.** Lake item `decision.fd06.two_apps`. Lake items `arch.listener.legacy_8080`, `arch.listener.gateway_8090`, `arch.listener.lake_rest_8091`, `arch.listener.lake_mcp_8092`. `docs/09-initial-prd/initial-prd.md`. Honesty on packaged counts cited below: REAL.
**Impact.** Later phases build to this shape. Application A takes rules from its transformed code. Application B takes rules only from the lake.
**Risk.** A shared run-time call between the two applications would hide a missing lake item.
**Confidence.** High on the locked shape. Unknown on Application A and Application B host ports.
**Open questions.** Host ports. Identity mechanism. Numeric service targets.

---

## Locked listeners

**Verified Fact.** `arch.listener.legacy_8080`, `arch.listener.gateway_8090`, `arch.listener.lake_rest_8091`, `arch.listener.lake_mcp_8092`, `arch.compose.inherited`.

| Port | Listener | What it does in this spec |
|---|---|---|
| 8080 | Legacy API | Current-system baseline. GET routes for cases, metrics, partners, and domain tables. No identity check today. |
| 8090 | Source gateway | Simulated upstream. Returns `occurred_at` and `published_at`. Failure modes: timeout, schema, rate_limit. |
| 8091 | Lake REST | Screens read lake items here. Write methods are absent. |
| 8092 | Lake MCP | Agents read the same lake as tools. MCP is the Model Context Protocol. It exposes lake reads as tools. |

Application A and Application B host ports are Unknown. Phase 8 compose work assigns them. This file does not invent those numbers.

Worked example. FastAPI and the MCP SDK both default to 8000 in common samples. This system uses 8091 for lake REST and 8092 for lake MCP so the two listeners do not share one port.

---

## Rule-source split

**Verified Fact.** `decision.fd06.two_apps`. `docs/10-architecture/adrs/adr-app-b-reads-only-the-lake.md`.

| Application | Where it reads its rules | What else it may read |
|---|---|---|
| Application A | Its own transformed code | The lake, for evidence, citations, and explanation |
| Application B | Only the Context Lake | The lake, including the context view that shows the item behind a rule |

Both applications run without calling the other at run time.

Both applications run demo scenarios 7 to 11 with the same inputs. Scenario 13 names each difference and traces it to a lake item.

Worked example. Packaged REVIEW count is 2,090. Honesty: REAL. Lake item `decision.bp4.four_programs`. Application A can still evaluate a rebuilt archive test in its own code. Application B evaluates that test when the archive item is in the lake. If the lake leaves out the JavaScript 1.05 tolerance, Application B can mark a case differently. The team then traces that difference to the missing item.

---

## Scenarios both applications run

**Verified Fact.** `docs/09-initial-prd/initial-prd.md`. `Execution_Plan.md` section 8.

| Id | What the user sees | Problem | Lake items the spec cites |
|---|---|---|---|
| S7 | A replayed delivery is marked as a duplicate candidate. Drop waits for RT-05. | BP2 | `rule.feed.replay_duplicate`, `data.feed.replay`, `decision.bp2.replay` |
| S8 | Both recipe revisions are shown. The case waits for RT-03. | BP1 | `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch`, `decision.bp1.recipe_mismatch` |
| S9 | Event time and arrival time stay two fields on a late result. | BP3 | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence`, `decision.bp3.two_clocks` |
| S10 | Overlapping policies are named. The case waits for RT-04. | BP6 | `rule.policy.overlap_or_invalid`, `data.policy_register.overlap`, `decision.bp6.region_overlap` |
| S11 | Retry and a user-visible status after an outage or schema mismatch. RT-06 can assign an owner. | BP8 | `decision.bp8.auth_and_owner`, `data.task.unassigned`, `decision.inc_2025_014`, `term.outage` |
| S12 | Application B traces one rule from a historical decision and code to a test. | BP4 | `decision.bp4.four_programs`, `decision.fd08.canonical_archive`, `test.rule.recipe_release.emea_2023` |
| S13 | S7 to S11 run on both applications. Each difference traces to a lake item. | BP4, BP5 | `decision.fd06.two_apps`, `rule.open_closed.operational`, `decision.bp5.open_closed_words` |

BP7 is a control on S7 to S11. Minutes 36 to 39 of the demo show an injection that is blocked. Lake items: `rule.untrusted_text.block`, `data.injection.partner_feeds`, `decision.bp7.untrusted_text`.

Worked example for S7. Packaged partner feeds with `processing_status = 'REPLAY'`: 67. Honesty: REAL. Code marks each row as a duplicate candidate. An Operations Analyst at RT-05 confirms before a row is dropped. A language model may explain the duplicate evidence. The model does not drop the row.

Worked example for S8. 91 of 125 process steps have `recipe_version` different from the joined tool `recipe_rev`. Honesty: REAL. Step recipe R02 and tool recipe R01 both stay on the case. A Process Engineer at RT-03 approves a hold or a release.

---

## Workflows

**Verified Fact.** `docs/09-initial-prd/initial-prd.md` workflows W1 to W7.

| Workflow | What the user finishes | Capabilities | Lake items |
|---|---|---|---|
| W1 Intake and de-duplication | A new feed is accepted, rejected, or marked duplicate. A replay waits for RT-05. | FR-02, FR-07, FR-13 | `rule.feed.replay_duplicate`, `code.partner_feeds.reconcile` |
| W2 Queue ranking | The next case to touch is chosen from stored fields. | FR-09, FR-05 | `code.legacy_logic.priority`, `rule.open_closed.operational` |
| W3 Exception investigation | The user sees both disagreeing values, with the two clocks kept apart. | FR-01, FR-03, FR-06, FR-07, FR-10, FR-11, FR-12 | `rule.recipe.mismatch_show_both`, `rule.clock.event_vs_arrival`, `rule.policy.overlap_or_invalid` |
| W4 Approval and disposition | A person approves, holds, or blocks every record-changing action. | FR-13, FR-01, FR-02, FR-06, FR-08 | `rule.hold.person_only`, `term.approval` |
| W5 Outage and recovery visibility | The user sees retry status. An owner can be assigned. | FR-08, FR-13 | `term.outage`, `decision.inc_2025_014` |
| W6 Rule lineage | The user sees one rule traced from document and code to a test. Application B required. | FR-04, FR-15 | `arch.graph.edges_table`, `decision.fd08.canonical_archive` |
| W7 Two-application comparison | Scenarios 7 to 11 run on both applications. Each difference is named. | FR-14, FR-04, FR-05 | `decision.fd06.two_apps` |

Ranking uses status, severity, and amount. It does not call a model. Lake item `code.legacy_logic.priority`. Two packaged cases are urgent because severity is CRITICAL. Zero packaged cases have `amount > 50000`. Honesty: REAL.

The 50,000 Python cutoff stays PROPOSED. Live policy when the archive is silent is HOLD_FOR_REVIEW. Lake items `rule.threshold.silent`, `rule.threshold.demo_50000`, `decision.bo08.silent_threshold`. This spec does not hard-code 50,000 as a live policy number.

---

## Users and roles

**Verified Fact.** `Decision_Tracker.md` section 7. BO-09 DECIDED, authority: sme. Lake items `term.approval`, `rule.hold.person_only`.

The role map lives in `business-rules.md`. The proposer of an action is never its approver. Company job titles stay Unknown. This file proceeds on the SME map.

| Run-time id | SME role name | Action type |
|---|---|---|
| RT-01 | Fab Exception Reviewer | Dispose a case that routed to HOLD_FOR_REVIEW |
| RT-02 | Shift Lead or Process Engineer (Approver) | Approve, hold, or block an agent-proposed action |
| RT-03 | Process Engineer | Approve a recipe-mismatch case |
| RT-04 | Policy Owner | Pick a policy on overlap, or keep the wait |
| RT-05 | Operations Analyst | Confirm a replay duplicate before it is dropped |
| RT-06 | Operations Lead | Assign a follow-up owner when none is recorded |

---

## Behavioural service needs (SLO behaviours)

These rows are required behaviours. They are not numeric targets.

**Verified Fact.** `docs/09-initial-prd/nfrs.md`. Lake items listed per row.

| Id | Behaviour | Target | Label | Lake item |
|---|---|---|---|---|
| SLO-B1 | A person approves every record-changing action | In force as BO-03 working answer. Unsigned | Verified Fact of the working answer | `rule.hold.person_only` |
| SLO-B2 | The proposer and the approver are different people | BO-09 DECIDED | Verified Fact | `term.approval` |
| SLO-B3 | Untrusted approve-or-ignore text stays data. The injection path returns BLOCK | Required | Verified Fact | `rule.untrusted_text.block` |
| SLO-B4 | A GenAI answer cites a stored row or a lake item, or the model abstains | Required as a behaviour. Percent floor Unknown | Unknown for the number | `arch.lake.yaml_sqlite` |
| SLO-B5 | Application B takes rules only from the lake | Required | Verified Fact | `decision.fd06.two_apps` |
| SLO-B6 | The two applications do not call each other at run time | Required | Verified Fact | `decision.fd06.two_apps` |
| SLO-B7 | Event time and arrival time stay two fields | Required | Verified Fact | `rule.clock.event_vs_arrival` |
| SLO-B8 | REVIEW and HOLD count as open | Required. BO-06a | Verified Fact | `rule.open_closed.operational` |
| SLO-B9 | A reader of a case on Application A or Application B has an identity | Needed. Mechanism later | Verified Fact that it is missing on 8080 | `arch.listener.legacy_8080`, `decision.bp8.auth_and_owner` |
| SLO-B10 | Every agent step and every human approval writes an audit row keyed by a correlation id | Locked idea. Schema later (FD-23) | Assumption of the default | `decision.fd06.two_apps` (two-app lock). Schema Unknown |

---

## Numeric service cells that stay Unknown

**Unknown.** `docs/09-initial-prd/nfrs.md`. FD-11 default. FD-14, FD-18, FD-19 still later.

| Cell | Value in this spec | Why it stays open |
|---|---|---|
| API p95 | Unknown | No governed source states a millisecond target |
| Retrieval p95 | Unknown | Same |
| Agent step time | Unknown | Same |
| Availability percent | Unknown | Inherited 99.5 percent is not adopted |
| Recovery time | Unknown | Inherited 8 hours is not adopted |
| Recovery point | Unknown | Inherited 24 hours is not adopted |
| Groundedness percent | Unknown | FD-14 PENDING |
| Citation percent floor | Unknown | FD-14 PENDING |
| Abstention percent floor | Unknown | FD-18 PENDING |
| Exception cycle time | Unknown | BO-02. No start and end fields signed |
| Aged backlog cutoff | Unknown | No age in days is signed |
| Token cost | Unknown | Phase 13 may fill when measured |

Worked example. The inherited note says 99.5 percent availability. This product does not adopt that number. The cell stays Unknown until a later measured value exists.

---

## Open, closed, and unsigned policy

**Verified Fact.** `rule.open_closed.operational`, `decision.bo06a.open_closed`. BO-06a DECIDED.

A case is open while any disposition or engineering action is still pending, including REVIEW and HOLD. A case is closed only when a final disposition is recorded and no engineering action is pending.

**Verified Fact.** `rule.open_closed.finance_audit`, `decision.bo06b.three_closures`. BO-06b stays PROPOSED.

Operational closed, finance booked, and audit closed stay three states. A mismatch routes to HOLD_FOR_REVIEW. This spec does not merge the three flags. This spec does not hard-code a finance or audit closed rule.

**Verified Fact.** `rule.threshold.silent`, `decision.bo08.silent_threshold`. BO-08 stays PROPOSED.

When the governed archive is silent, the case routes to HOLD_FOR_REVIEW. Demo may show 50,000 labelled PROPOSED. Never use 999,999 as a live policy number. Lake items `rule.threshold.demo_50000`, `rule.threshold.never_999999`.

---

## Language-model bounds

**Verified Fact.** FD-04. `docs/09-initial-prd/capability-map.md`. Lake item `rule.hold.person_only`.

| Job | How it is built |
|---|---|
| Queue ranking | Written test on status, severity, and amount |
| Rule pass or fail | Written test against the governed archive. Application A from transformed code. Application B from the lake |
| Reconciliation and de-duplication | Written tests on key, schema, REPLAY, and quantity |
| Conflict explanation | Language model drafts a cited sentence |
| Natural-language query | Language model drafts a cited answer, or abstains |
| Agentic planning | Language model drafts a plan and waits |
| `engineering_hold` prediction | Rejected. FD-05. 117 of 125 versus 117 of 125. Honesty: REAL |

The model gets read-only tools only (FD-02). The model does not write a case, a hold, a feed status, or an owner.

---

## What this file does not do

This file does not write code. It does not assign Application A or Application B ports. It does not invent a latency number, an availability percent, or a dollar benefit. It does not sign BO-03, BO-04, BO-06b, or BO-08. It does not start Phase 7.
