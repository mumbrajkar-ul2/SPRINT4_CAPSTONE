# Agent budget policy

| Field | Value |
|---|---|
| Stage | Phase 10 / 22 Agentic engineering. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | FD-15; `loop-control-policy.md`; `docs/19-intelligence/model-configuration.md`; `Execution_Plan.md` section 10 |
| Assumptions | Replay spends 0 live model tokens. Azure cost stays Unknown until a person sets `MODEL_MODE=azure`. |
| Unresolved issues | Live token price. Measured milliseconds per node. |
| Residual risks | Publishing 8 as a quality score would invent an FD-14 floor. |

This file records the FD-15 numeric bounds in one place. They are engineering defaults. Authority: team-force. They are not quality floors. They are not Business Owner policy.

---

## Finding

**Finding.** The Phase 10 agent may use 12 LangGraph supersteps, 8 model-or-tool nodes, 8 tool calls, and 3 gather visits. Replay adds 0 live tokens.
**Evidence.** ED-P10A-01. ED-P10A-02. `MODEL_MODE=replay`. LangGraph 1.0.3 default recursion limit is 25. This design lowers it to 12 for the laptop demo.
**Impact.** Half B writes these integers as named constants. Tests assert the constants.
**Risk.** A later live Azure run could spend tokens inside the same step budget. That cost is Unknown.
**Confidence.** High on the constant names. Unknown on measured duration.
**Open questions.** Live token cost. FD-19 retry milliseconds stay out of this budget.

---

## Named constants Half B must write

| Constant | Value | File |
|---|---|---|
| `RECURSION_LIMIT` | 12 | `apps/app_a/agent/budget.py` |
| `STEP_BUDGET` | 8 | same |
| `MAX_TOOL_INVOCATIONS` | 8 | same |
| `MAX_GATHER_VISITS` | 3 | same |
| `CHECKPOINT_PATH` | `apps/app_a/runtime/checkpoints.sqlite3` | `apps/app_a/agent/checkpointer.py` |
| `GRAPH_NAME` | `app_a_investigate` | `apps/app_a/agent/graph.py` |
| `WRITE_TOOLS` | `[]` | `apps/app_a/agent/tools.py` |
| `READ_TOOLS` | the six names | same |

A later change of any integer is a new team-force decision. Half B does not raise a cap to make a test pass.

---

## What the budget does not buy

The step budget does not score groundedness. FD-14 stays cite-or-abstain with no percent.

The recursion limit does not replace OPA. A run that hits 12 still writes HOLD_FOR_REVIEW. It does not become EXECUTE.

The tool cap does not replace the allow-list. Call 8 still has to be one of the six names.

---

## Token and time

| Meter | Bound in this half | Label |
|---|---|---|
| Live tokens | 0 in `MODEL_MODE=replay` | Verified Fact of replay |
| Azure tokens | Unknown | Unknown |
| Per-node wall time | Unknown | Unknown |
| Demo slot | Minutes 13 to 25 for the trace. Minutes 36 to 39 for restart | Verified Fact of the plan |

This file does not invent a 30-second model timeout as a decided SLO. Half B may use the existing retrieve HTTP timeout of 5 seconds and the gateway probe timeout of 3 seconds. Those two numbers already sit in Application A code. Honesty: REAL for the current code. They are client timeouts, not business policy.

---

## What this file does not do

This file does not measure a run. It does not set a dollar cutoff.
