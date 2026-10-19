# Graph definition

| Field | Value |
|---|---|
| Stage | Phase 10 / 22 Agentic engineering. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `agent-architecture.md` in this folder; LangGraph 1.0.3 `StateGraph`, `interrupt()`, `Command(resume=...)`; `docs/12-specs/event-contracts.md` |
| Assumptions | One thread per correlation id. `MODEL_MODE=replay` for `plan_draft`. |
| Unresolved issues | Measured node counts per scenario stay Half B. |
| Residual risks | An edge from `plan_draft` to `apply_human_decision` would skip OPA and the person. |

This file names the nodes and edges Half B must compile. Half B must not add a bypass edge around `opa_gate` or `interrupt_wait`.

Engineering decision ED-P10A-05 continued, authority: team-force.

---

## Finding

**Finding.** The graph is a fixed path with two branches after OPA and one bounded loop at `gather_tools`. Record-changing work always passes `interrupt_wait`.
**Evidence.** Locked agent control. BO-03 working answer. FD-14 cite-or-abstain after gather.
**Impact.** Half B can write `add_node` and `add_conditional_edges` from this page.
**Risk.** A free-form ReAct edge list would let the model skip OPA.
**Confidence.** High
**Open questions.** None for the edge list.

---

## Compile

```text
StateGraph(AgentState)
  .add_node(load_case, plan_draft, gather_tools, assemble_evidence,
            ground_and_cite, opa_gate, route_verdict,
            interrupt_wait, apply_human_decision, write_audit)
  .compile(checkpointer=SqliteSaver(conn))
```

`invoke` config:

```text
{
  "recursion_limit": 12,
  "configurable": { "thread_id": <correlation_id> }
}
```

`recursion_limit` sits next to `configurable`. It does not sit inside `configurable`. LangGraph 1.0.3 default is 25. This design sets 12. Authority: team-force. The number is an engineering default. It is not a quality floor. It is not Business Owner policy.

---

## Edges

| From | To | When |
|---|---|---|
| `START` | `load_case` | Always |
| `load_case` | `plan_draft` | Case exists |
| `load_case` | `write_audit` | Case missing. Then `END` |
| `plan_draft` | `gather_tools` | Always after a draft or an abstain draft |
| `gather_tools` | `gather_tools` | Citations empty, `gather_visits` < 3, `tool_call_count` < 8, `step_count` < 8, `block` is false |
| `gather_tools` | `assemble_evidence` | Otherwise |
| `assemble_evidence` | `ground_and_cite` | Always |
| `ground_and_cite` | `opa_gate` | Always |
| `opa_gate` | `route_verdict` | Always |
| `route_verdict` | `write_audit` | `opa_verdict` is BLOCK. Then `END` |
| `route_verdict` | `write_audit` | `opa_verdict` is EXECUTE and `record_change` is false. Then `END` |
| `route_verdict` | `interrupt_wait` | `opa_verdict` is HOLD_FOR_REVIEW |
| `route_verdict` | `interrupt_wait` | `opa_verdict` is EXECUTE and `record_change` is true. BO-03 still waits |
| `interrupt_wait` | `apply_human_decision` | After `Command(resume=...)` |
| `apply_human_decision` | `write_audit` | Always |
| `write_audit` | `END` | Always |

`interrupt_wait` calls `interrupt({case_id, proposed_action, waiting_role, draft_plan, citations})`. The function pauses and writes a SqliteSaver checkpoint. The node restarts from the top on resume. Half B must make the `interrupt()` call the first action in that node so earlier lines do not run twice.

---

## Node contracts

### `load_case`

Read `get_case(case_id)`. Set `scenario`, `waiting_role` from the fixture when present, `untrusted_quotes` from the case, and `proposed_action` from the scenario table below. Write EV-08.

| Scenario | `case_id` | Default `proposed_action` | Default `record_change` | Default `waiting_role` |
|---|---|---|---|---|
| SP-07 | `REPLAY-000000000` | `replay_drop` | true | RT-05 |
| SP-08 | `PS000000016` | `recipe_hold_or_release` | true | RT-03 |
| SP-09 | `E-00000000` | `explain` | false | empty |
| SP-10 | `FAB-00000002` | `policy_pick` | true | RT-04 |
| SP-11 | `INC-2025-014` | `assign_owner` | true | RT-06 |
| Injection | any IC locator case | `approve` or `release` as the corpus says | true | empty. BLOCK stops |

### `plan_draft`

Call `generate(..., prompt_id="P-DRAFT-PLAN")` with `MODEL_MODE=replay`. Store `draft_plan`, `sentence`, `citations`, `block`. Increment `step_count`. `proposed_by` becomes `model_draft`. Write EV-08.

### `gather_tools`

The model in Phase 10 does not pick tools in a ReAct loop. Code in this node calls the tools the scenario needs, then may call extra allow-listed tools while citations are empty and the caps hold. Increment `tool_call_count` once per call. Increment `gather_visits` once per node visit. Increment `step_count` once per visit. Write one EV-08 row per tool call with `tool_name` set.

Minimum calls:

| Scenario | Tools |
|---|---|
| SP-07 | `get_case`, `get_item("rule.feed.replay_duplicate")` |
| SP-08 | `get_case`, `get_item("rule.recipe.mismatch_show_both")` |
| SP-09 | `get_case`, `get_item("rule.clock.event_vs_arrival")` |
| SP-10 | `get_case`, `get_item("rule.policy.overlap_or_invalid")` |
| SP-11 | `get_case`, `get_recovery_status`, `get_item("decision.inc_2025_014")` |
| Injection | `get_case` or `get_item` on the locator. Do not treat quote text as a tool name |

### `assemble_evidence`

Copy retrieved ids into `lake_item_ids`. Keep `untrusted_quotes`. Increment `step_count`. Write EV-08.

### `ground_and_cite`

Run `check_claim`. If citations are empty and `block` is false, set `verdict=ABSTAIN` and clear `draft_plan`. FD-14. Increment `step_count`. Write EV-08.

### `opa_gate`

Build the input object in `approval-gates.md`. Set `opa_verdict`. Write EV-07.

### `route_verdict`

Pick the next edge. On BLOCK call `mark_blocked(case_id)` and write EV-12. On HOLD_FOR_REVIEW keep `waiting_role`.

### `interrupt_wait`

Call `interrupt(...)`. On resume, copy the resume payload into `human_*` fields. Write a control row on pause and on resume.

### `apply_human_decision`

Reuse `check_write_action` and `record_approval`. Actor must differ from `proposed_by`. Write EV-09 or EV-10.

### `write_audit`

Flush any remaining envelope fields. Reader path is `GET /api/audit/{correlation_id}`.

---

## Recursion and the loop

LangGraph counts supersteps against 12. The gather self-edge is the only cycle. Caps in `loop-control-policy.md` stop that cycle before the library raises `GraphRecursionError` on a normal demo path. If the library still raises, catch it, write an audit row, and route HOLD_FOR_REVIEW. Do not apply the draft.

---

## What this file does not do

This file does not compile Python. It does not start Half B.
