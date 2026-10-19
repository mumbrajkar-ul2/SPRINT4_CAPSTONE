# Loop control policy

| Field | Value |
|---|---|
| Stage | Phase 10 / 22 Agentic engineering. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | FD-15; LangGraph 1.0.3 `recursion_limit` and `GraphRecursionError`; `graph-definition.md` in this folder |
| Assumptions | The only cycle is the `gather_tools` self-edge. Other nodes run once per invoke or once per resume. |
| Unresolved issues | Measured gather visits per scenario stay Half B. |
| Residual risks | Leaving `recursion_limit` at the library default of 25 would spend the 40-minute demo in a gather loop. |

This file names how the graph stops a cycle. The numbers are engineering defaults. They are not quality floors. They are not Business Owner policy.

Engineering decisions ED-P10A-01 and ED-P10A-02, authority: team-force.

---

## Finding

**Finding.** Three counters bound the gather cycle: LangGraph `recursion_limit` 12, application `step_count` 8, and `tool_call_count` 8. `gather_tools` may run at most 3 times.
**Evidence.** FD-15 asks this half to name the recursion limit and the step budget. LangGraph counts supersteps and raises `GraphRecursionError` when the limit is reached.
**Impact.** Half B can implement the counters in `apps/app_a/agent/budget.py` without asking for a policy number.
**Risk.** Treating 8 as a groundedness floor would invent an FD-14 percent.
**Confidence.** High on the need for a cap. The specific integers are a team-force default.
**Open questions.** None for Half B implementation.

---

## Counters

| Counter | Scope | Cap | When it increases | When the cap is hit |
|---|---|---|---|---|
| `recursion_limit` | One `invoke`, including resume | 12 | Each LangGraph superstep | Library raises `GraphRecursionError`. Application A catches it, writes an audit row, sets `opa_verdict=HOLD_FOR_REVIEW`, does not apply the draft |
| `step_count` | One thread | 8 | `plan_draft`, each `gather_tools` visit, `assemble_evidence`, `ground_and_cite` | Set `budget_exhausted=true`. Skip further gather. Go to `assemble_evidence` then OPA. OPA-R-10 returns HOLD_FOR_REVIEW |
| `tool_call_count` | One thread | 8 | Each allow-listed tool function return | No further tool call. Leave gather |
| `gather_visits` | One thread | 3 | Each entry to `gather_tools` | Leave gather even if citations are still empty |

Control nodes `load_case`, `opa_gate`, `route_verdict`, `interrupt_wait`, `apply_human_decision`, and `write_audit` do not increase `step_count`.

Worked example. A run calls `plan_draft` (step 1), `gather_tools` visit 1 with 2 tools (step 2, tools 2), `gather_tools` visit 2 with 2 tools (step 3, tools 4), then `assemble_evidence` (step 4) and `ground_and_cite` (step 5). The remaining budget is 3 steps and 4 tool calls. A normal scenario 8 run stays under every cap.

Worked example. A broken gather keeps finding nothing. Visit 3 ends the cycle. Citations stay empty. FD-14 sets ABSTAIN. If `record_change` is still true, OPA-R-10 or OPA-R-12 returns HOLD_FOR_REVIEW.

---

## What is not a loop control

| Item | Why it stays out |
|---|---|
| A token budget | Replay spends 0 live tokens. Live token caps stay Unknown |
| A wall-clock SLA | No numeric SLO exists |
| A groundedness percent | FD-14 has no percent floor |
| A dollar amount | BO-08 stays PROPOSED. OPA has no amount comparison |

---

## Resume and the counters

`interrupt()` then `Command(resume=...)` continues the same thread. `step_count` and `tool_call_count` stay as stored in the checkpoint. Resume does not reset the budget. `apply_human_decision` does not need a new gather. A second `POST /api/agent/run` on the same case mints a new correlation id unless the caller sends the old header on purpose.

---

## What this file does not do

This file does not tune the numbers after a measured run. A later change needs a new team-force note.
