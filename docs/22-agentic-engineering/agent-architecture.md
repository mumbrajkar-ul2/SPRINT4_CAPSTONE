# Agent architecture

| Field | Value |
|---|---|
| Stage | Phase 10 / 22 Agentic engineering. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No LangGraph code in this half. |
| Evidence sources | `docs/10-architecture/adrs/adr-langgraph-interrupt-approval.md`; `docs/20-application/deterministic-ai-boundary.md`; `docs/19-intelligence/prompt-registry.md`; `apps/app_a/intelligence/generate.py`; LangGraph 1.0.3 docs for `interrupt()`, `Command`, SqliteSaver, `recursion_limit` |
| Assumptions | BO-03 working answer holds and stays PROPOSED. `MODEL_MODE=replay`. Application A rules still come from transformed code. The lake is citations. |
| Unresolved issues | Company job titles stay Unknown. Azure live path stays later. Application B reuses this control pattern in Phase 11. |
| Residual risks | A ReAct loop with no named nodes would hide the approval gate. Binding `record_approval` as a tool would skip FD-02. |

This file names the Application A agent. The agent drafts a plan, reads with allow-listed tools, asks OPA for a verdict, and waits for a person when a record would change.

Engineering decision ED-P10A-05, authority: team-force. Graph name, state fields, node list, and module paths below.

---

## Finding

**Finding.** One named graph `app_a_investigate` covers scenarios 7 to 11 and the injection path. The model runs only in node `plan_draft`. Tools run only in node `gather_tools`. Writes run only in node `apply_human_decision` after a person resume.
**Evidence.** FD-04: agentic planning is GenAI. FD-02: read-only tools. BO-03: a person approves every record-changing action. P-DRAFT-PLAN v1.0.0 already exists.
**Impact.** Half B can compile one `StateGraph` in `apps/app_a/agent/`.
**Risk.** Letting the model pick the next node name would drop the OPA gate.
**Confidence.** High on the shape. Unknown on measured step counts until Half B.
**Open questions.** HALF_A_ACCEPTED. Company titles.

---

## Runtime

**Verified Fact.** FD-13. FD-15.

| Setting | Value |
|---|---|
| Host | Application A on port 8100 |
| Graph name | `app_a_investigate` |
| Library | LangGraph. Pin in Half B requirements. Docs checked at 1.0.3 |
| Pause | `from langgraph.types import interrupt, Command` |
| Checkpoint | `from langgraph.checkpoint.sqlite import SqliteSaver` |
| Checkpoint file | `apps/app_a/runtime/checkpoints.sqlite3` |
| `thread_id` | Equal to `correlation_id` |
| `recursion_limit` | 12. Config key on `invoke`, not inside `configurable` |
| Model | `MODEL_MODE=replay`. Prompt `P-DRAFT-PLAN` v1.0.0 |
| Rules | Transformed code in `apps/app_a/rules/adapter.py` |
| Citations | Lake tools and `retrieve.py` |
| Policy | OPA three verdicts |
| Audit | One row per finished node and per human approval |

---

## Half B module map

| Path | Responsibility |
|---|---|
| `apps/app_a/agent/state.py` | Typed state fields listed below |
| `apps/app_a/agent/tools.py` | The six read-only tools. Empty write list |
| `apps/app_a/agent/nodes.py` | One function per node |
| `apps/app_a/agent/graph.py` | `StateGraph` edges and compile with SqliteSaver |
| `apps/app_a/agent/budget.py` | Step counter and tool-call counter |
| `apps/app_a/agent/checkpointer.py` | Opens the SQLite file |
| `apps/app_a/agent/opa_client.py` | Sends the named input. Reads one verdict string |
| `apps/app_a/routes/agent.py` | `POST /api/agent/run` starts a thread |

Existing `POST /api/approvals` resumes a waiting thread. Half B adds the `Command(resume=...)` call there after the role check.

---

## State fields

Half B uses these names. Extra keys stay out of the checkpoint until a later ADR.

| Field | Type | What it holds |
|---|---|---|
| `correlation_id` | string | Join key for audit rows |
| `thread_id` | string | Same string as `correlation_id` |
| `case_id` | string | Fixture or packaged id |
| `actor_id` | string | Requester who started the run |
| `actor_role` | string | `RT-01` to `RT-06` |
| `proposed_by` | string | Draft actor. Model drafts use `model_draft` |
| `proposed_action` | string | `explain`, `cite`, `recipe_hold_or_release`, `policy_pick`, `replay_drop`, `assign_owner`, `dispose`, `approve`, `release`, `ignore-validation`, `close-from-text` |
| `record_change` | bool | True when the proposed action would change a stored record |
| `draft_plan` | string | P-DRAFT-PLAN text. Empty on abstain |
| `sentence` | string | Cited sentence or empty |
| `citations` | list of string | Lake item ids |
| `untrusted_quotes` | list of string | Flagged harvested text |
| `lake_item_ids` | list of string | Same citations plus rule ids used by OPA |
| `verdict` | string | `ANSWER`, `ABSTAIN`, or `HOLD_FOR_REVIEW` from grounding |
| `block` | bool | True on the injection path |
| `opa_verdict` | string | `EXECUTE`, `HOLD_FOR_REVIEW`, `BLOCK`, or empty |
| `waiting_role` | string or empty | `RT-01` to `RT-06` |
| `step_count` | int | Model-or-tool nodes finished. Budget 8 |
| `tool_call_count` | int | Individual tool calls. Cap 8 |
| `gather_visits` | int | How many times `gather_tools` ran. Cap 3 |
| `budget_exhausted` | bool | True when a cap stopped gather or plan |
| `human_decision` | string or empty | Filled on resume |
| `human_action_type` | string or empty | Filled on resume |
| `human_actor_id` | string or empty | Person who resumed |
| `human_actor_role` | string or empty | Role that resumed |
| `error_class` | string or empty | EH class when one applies |
| `scenario` | string or empty | `SP-07` to `SP-11` when bound |

---

## Node list

| Node | Calls the model | Calls a tool | Writes a record | Audit `row_kind` |
|---|---|---|---|---|
| `load_case` | No | No. Reads store in process | No | control, EV-08 with `step_name=load_case` |
| `plan_draft` | Yes. `P-DRAFT-PLAN` | No | No | agent_step |
| `gather_tools` | No | Yes. Allow-list only | No | agent_step. One row per tool call |
| `assemble_evidence` | No | No | No | agent_step |
| `ground_and_cite` | No | No. `check_claim` | No | agent_step |
| `opa_gate` | No | No. AD-OPA | No | control, EV-07 |
| `route_verdict` | No | No | No | control |
| `interrupt_wait` | No | No. `interrupt()` | No | control. One row on pause, one row on resume |
| `apply_human_decision` | No | No | Yes. After role check | human_approval, EV-09 or EV-10 |
| `write_audit` | No | No | Audit row only | control if a trailing row is still needed |

`END` is the LangGraph terminal. It is not a custom node.

---

## Start and resume HTTP

Engineering decision ED-P10A-09, authority: team-force.

| Route | What it does |
|---|---|
| `POST /api/agent/run` | Body `{ "case_id": "..." }`. Headers include identity and optional `X-Correlation-Id`. Mints `corr-app-a-` plus 12 hex digits when the header is empty. Invokes the graph with `recursion_limit` 12. |
| `POST /api/approvals` | Existing person write. After `check_write_action`, if a checkpoint is waiting, call `graph.invoke(Command(resume=payload), config)`. |
| `GET /api/audit/{correlation_id}` | Full trace. FD-23 columns. |

Resume payload fields: `decision`, `action_type`, `actor_id`, `actor_role`, `proposed_by`, optional `owner_id`, optional `policy_id`, optional `hold_value`.

---

## Worked path: scenario 8

1. `POST /api/agent/run` with `case_id=PS000000016`.
2. `load_case` reads R02 and R01.
3. `plan_draft` writes a draft that names both revisions and RT-03.
4. `gather_tools` calls `get_case` and `get_item("rule.recipe.mismatch_show_both")`.
5. `ground_and_cite` keeps the citations.
6. `opa_gate` sees `record_change=true` and returns HOLD_FOR_REVIEW.
7. `interrupt_wait` saves state.
8. RT-03, a different person from `proposed_by`, posts `recipe_hold_or_release`.
9. `apply_human_decision` writes `engineering_hold`.
10. The audit read returns every step and the approval under one correlation id.

---

## What this file does not do

This file does not compile the graph. It does not sign BO-03. It does not add a write tool.
