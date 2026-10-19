# Agent security controls

| Field | Value |
|---|---|
| Stage | Phase 12 / 24 Security, privacy, responsible AI. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-24a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No security code in this half. |
| Evidence sources | FD-02; FD-15; FD-16; FD-18; FD-23; BO-03; BO-09; `docs/22-agentic-engineering/tool-permission-map.md`; `apps/app_a/agent/tools.py`; `apps/app_a/agent/graph.py`; `apps/app_a/agent/budget.py`; `apps/app_a/agent/nodes.py`; `docs/22-agentic-engineering/agent-test-results.md` |
| Assumptions | `MODEL_MODE=replay`. Graph name stays `app_a_investigate`. Application B keeps the same tool bound: no write tool. |
| Unresolved issues | Live Azure token cost stays Unknown. Company titles stay Unknown. |
| Residual risks | Registering `record_approval` as a LangGraph tool would skip the person. SC-24-01 is still missing on `load_case`. |

This file names the agent bounds Half B must keep while it tightens injection detection. The model has no write tool. This half adds no tool.

---

## Finding

**Finding.** Graph `app_a_investigate` already limits the model to node `plan_draft`, six read tools, budget caps, an OPA gate, a human pause, and an audit row per step. The missing agent control is feeding OPA from untrusted quotes plus write-from-text when the caller omits a corpus id.
**Evidence.** FD-15. `READ_TOOLS` six names. `WRITE_TOOLS = []`. `recursion_limit` 12. Phase 10 T-NO-WRITE-TOOL, T-BUDGET, T-RECURSION, T-INJECT-01. Honesty REAL.
**Impact.** Half B edits `load_case` and `build_opa_input`. It does not add a node or a tool.
**Risk.** Binding `record_approval` in `gather_tools` would give the model a write.
**Confidence.** High on the existing bounds. Inference on the quotes-without-id path until HB-24-01.
**Open questions.** HALF_A_ACCEPTED.

---

## Tool allow-list (must stay)

**Verified Fact.** FD-15. `apps/app_a/agent/tools.py`.

| Tool | Who may invoke it | What it may write |
|---|---|---|
| `search_items` | Node `gather_tools` | Nothing |
| `get_item` | Node `gather_tools` | Nothing |
| `get_links` | Node `gather_tools` | Nothing |
| `rule_at` | Node `gather_tools` | Nothing |
| `get_case` | Node `gather_tools` | Nothing |
| `get_recovery_status` | Node `gather_tools` | Nothing |

`WRITE_TOOLS` is `[]`. `call_tool` rejects a name that is absent or that sits on the write list. Reject body uses `error_class: forbidden_role`.

Half B re-asserts this list in `test_app_a_phase12_security.py`. A new write name fails the test.

Functions that must not reach the model: `store.record_approval`, `store.mark_blocked`, `Command(resume=...)`, `opa_client.evaluate`, `audit.writer.append`.

---

## Graph bounds (must stay)

**Verified Fact.** FD-15. `graph.py`. `budget.py`.

| Bound | Value | What happens at the cap |
|---|---|---|
| Graph name | `app_a_investigate` | One named graph |
| Model node | `plan_draft` only | Other nodes run code |
| Write node | `apply_human_decision` after resume | Person required |
| `recursion_limit` | 12 | `GraphRecursionError` caught. HOLD_FOR_REVIEW. No write |
| Step budget | 8 | `budget_exhausted` true. OPA-R-10 HOLD_FOR_REVIEW |
| Max tool calls | 8 | Same exhaustion path |
| Max gather visits | 3 | Stop gathering. Assemble evidence |
| Checkpoint file | `apps/app_a/runtime/checkpoints.sqlite3` | Restart keeps the wait |
| `thread_id` | Equals `correlation_id` | Audit and saver join |

Those numbers are engineering defaults from FD-15. They are not quality floors and not Business Owner policy.

---

## OPA gate in the agent

**Verified Fact.** Node `opa_gate` calls `evaluate(build_opa_input(state))`. The model does not choose the verdict.

| `opa_verdict` | Next node | HTTP from `/api/agent/run` |
|---|---|---|
| BLOCK | `write_audit` | 409, `error_class: blocked`, `waiting` false |
| HOLD_FOR_REVIEW | `interrupt_wait` | 200 with `waiting` true, or 409 `wait_for_person` on budget failure |
| EXECUTE and `record_change` | `interrupt_wait` | Wait for the person under BO-03 |
| EXECUTE and read | `write_audit` | 200 with citations |

SC-24-01 must produce the BLOCK row when quotes plus write-from-text are present.

---

## Cite or abstain inside the graph

**Verified Fact.** Node `ground_and_cite` calls `ground()`. FD-18: a hallucination is an AI answer that does not cite a lake item.

If citations are empty and `block` is false, the node sets verdict ABSTAIN and clears the sentence. If `block` is true, citations must include `rule.untrusted_text.block` from the retrieved set.

HB-24-01 after SC-24-01: the response body is a BLOCK, not an ANSWER. If a sentence is present, it still cites a lake item. Empty citations on a served ANSWER fail the test. Percent floor stays Unknown.

---

## Human control the agent must keep

**Verified Fact.** BO-09. BO-03 working answer.

- Record-changing EXECUTE still waits.
- BLOCK skips the wait.
- Resume checks `check_write_action`.
- `actor_id` must differ from `proposed_by`.
- `X-Actor-Role` must match `action_type`.
- A role or actor that starts with `model` is refused.

Demo actors stay `demo-rt01-1` through `demo-rt06-1`. They are not company staff.

---

## Audit the agent must keep

**Verified Fact.** FD-23.

On HB-24-01 after:

- At least one row with `event_type=EV-12` (injection stop)
- At least one row with `opa_verdict=BLOCK`
- Zero rows with `row_kind=human_approval`
- `untrusted_quote_present=1` on the injection rows
- Raw injection text stays out of `notes` as an instruction

---

## Application B

**Verified Fact.** Phase 11. Application B has its own `policy/opa/app_b.rego` with the same corpus ids and write-from-text set. Retrieve calls `block_untrusted`. The model has no write tool.

This Half B does not edit Application B. Sub-stage 26 runs the corpus on both applications. Residual: Application B HTTP coverage for quotes-without-corpus-id stays Unknown until that run.

---

## What Half B may and may not change

| May change after HALF_A_ACCEPTED | Must not change |
|---|---|
| `load_case` flag logic for quotes plus write-from-text | Tool allow-list membership |
| `build_opa_input` injection flag from the same pair | Write-tool list (stays empty) |
| New pytest file for HB-24-01 and HB-24-02 | Graph node list, except no new write node |
| Optional use of existing `untrusted_quote_present` with write-from-text | Amount comparison in Rego |
|  | New RT role |
|  | Identity on port 8080 |
|  | A percent floor |

---

## What this file does not do

This file does not bind a new tool. It does not start Half B. It does not give the model a write.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
