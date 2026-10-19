# Agent telemetry specification

| Field | Value |
|---|---|
| Stage | Phase 13 / 31 Observability and service levels. Half B evidence. SC-31-01 / HB-31-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-31b-doc-20261018-001 |
| Status | MEASURED for the query miss line only. Half B did not change the audit table. Agent completion time stays Unknown. |
| Evidence sources | FD-19; FD-11; FD-15; FD-23; `docs/23-human-control/audit-chain.md`; `docs/12-specs/event-contracts.md`; `apps/app_a/agent/graph.py`; `apps/app_a/audit/writer.py`; `apps/app_a/audit/store.py`; `apps/app_a/routes/audit.py`; `apps/app_a/server.py`; `apps/app_a/agent/tools.py` |
| Assumptions | `MODEL_MODE=replay`. Graph name stays `app_a_investigate`. `thread_id` equals `correlation_id`. BO rows that are PROPOSED stay PROPOSED. `WRITE_TOOLS` stays empty. |
| Unresolved issues | Agent completion time stays Unknown. Retention days stay Unknown. Application B audit bind after a recreate stays as built in sub-stage 30. |
| Residual risks | Treating middleware `request_ok` as the only agent record would hide a step. Letting the model write the only audit paragraph would drop a control row. Adding an agent metrics product would add a collector this stack does not run. |

This file names what the Application A graph records. The graph is the named step list `app_a_investigate`. Each finished step writes one audit row. Each human approval writes one audit row. Stdout still writes one request line for the HTTP call that started or resumed the graph.

Half B does not change the audit table. Half B does not add an agent stdout event. The one Half B check stays the query `replay_miss` line in `observability-architecture.md`.

Engineering decision ED-P13-31A-02 applies here. Audit rows stay in `apps/app_a/audit/audit_chain.sqlite3`. Request logs stay on stdout.

---

## Finding

**Finding.** Table `audit_chain` has 27 named columns. `GET /api/audit/{correlation_id}` returns every row for that id ordered by `seq`. Graph nodes are `load_case`, `plan_draft`, `gather_tools`, `assemble_evidence`, `ground_and_cite`, `opa_gate`, `route_verdict`, `interrupt_wait`, `apply_human_decision`, and `write_audit`. `thread_id` equals `correlation_id`. Recursion limit is 12. Step budget is 8. Max tool calls is 8. Max gather visits is 3. Those integers are engineering defaults. They are not a latency floor. `WRITE_TOOLS` is `[]`. Middleware still emits `request_ok` for `POST /api/agent` and `POST /api/approvals`. That line is the HTTP wrapper. It is not the step list.
**Evidence.** `audit-chain.md`. `graph.py`. FD-15. FD-23. `apps/app_a/server.py` emit after `call_next`.
**Impact.** A person joins stdout and the audit GET with the same `correlation_id`. Half B leaves this join as built.
**Risk.** A later author who logs only stdout would lose `opa_verdict` and `decision`.
**Confidence.** High on the column list and the node names. Unknown on a measured step duration.
**Open questions.** Reviewer grades HB-31-01. Retention days. Application B audit host bind.

---

## Locked facts this design applies

**Verified Fact.** FD-15. Read tools only: `search_items`, `get_item`, `get_links`, `rule_at`, `get_case`, `get_recovery_status`. `WRITE_TOOLS` is empty. Recursion limit 12. Step budget 8. Max tool calls 8. Max gather visits 3. Checkpoint file `apps/app_a/runtime/checkpoints.sqlite3`. `thread_id` equals `correlation_id`.

**Verified Fact.** FD-23. One audit row per agent step and one audit row per human approval. Read by correlation id.

**Verified Fact.** FD-19. Numeric latency, availability, error-budget, and recovery floors stay Unknown. This half invents no percent.

**Verified Fact** of BO-03 working answer. A person approves every record-changing action. BO-03 stays PROPOSED.

---

## Graph steps the person can name

| `step_name` | What that node does | Audit `row_kind` |
|---|---|---|
| `load_case` | Opens the case. Missing case can stop the run | `agent_step` |
| `plan_draft` | Builds a draft under replay | `agent_step` |
| `gather_tools` | Calls one allow-listed read tool | `agent_step` |
| `assemble_evidence` | Collects retrieved ids and quotes | `agent_step` |
| `ground_and_cite` | Checks the claim against retrieve | `agent_step` |
| `opa_gate` | Asks Open Policy Agent for EXECUTE, HOLD_FOR_REVIEW, or BLOCK | `agent_step` |
| `route_verdict` | Picks wait, block, or continue | `agent_step` |
| `interrupt_wait` | Pauses for a person | `agent_step` |
| `apply_human_decision` | Applies the resume payload | `human_approval` when a person decided |
| `write_audit` | Writes the closing row | `control` or `agent_step` as already coded |

Worked example. Scenario 8 under `corr-p10b-doc-20261018-001` wrote 12 audit rows. Honesty: REAL in the Phase 10 record. A later run with a new correlation id writes a new list. That later count stays Unknown until it is measured.

---

## Audit columns the person reads

**Verified Fact.** `audit-chain.md`.

The 27 columns are `audit_id`, `correlation_id`, `seq`, `row_kind`, `event_type`, `occurred_at`, `recorded_at`, `actor_id`, `actor_role`, `case_id`, `app`, `step_name`, `tool_name`, `draft_present`, `proposed_action`, `opa_verdict`, `action_type`, `decision`, `proposed_by`, `lake_item_ids`, `thread_id`, `graph_name`, `interrupt_id`, `checkpoint_id`, `error_class`, `untrusted_quote_present`, `notes`.

`occurred_at` and `recorded_at` stay two fields. **Verified Fact.** Lake item `rule.clock.event_vs_arrival`. SLO-B7.

`event_type` uses `EV-01` to `EV-12` from `event-contracts.md`. Agent steps use `EV-08`. Human approvals use `EV-09`. Injection BLOCK uses `EV-12`.

---

## How stdout and the audit table sit together

| Call | Stdout `event` today | Audit rows |
|---|---|---|
| `POST /api/agent` | `request_ok` after the handler | One row per finished node |
| `POST /api/approvals` | `request_ok` after resume | One `human_approval` row |
| `GET /api/audit/{correlation_id}` | `request_ok` | None added. This is a read |
| Identity miss on those routes | `identity_missing` or `server_key_missing` | None. The graph did not start |
| Forbidden role | `forbidden_role` | None |

Worked example. The person sends `POST /api/agent` with `X-Correlation-Id: corr-p13-31a-doc-20261018-001`. Stdout has `service=app-a`, `event=request_ok`, `path` for the agent route, `correlation_id` that string. `GET /api/audit/corr-p13-31a-doc-20261018-001` then returns `rows` in `seq` order. Empty `rows` means the graph wrote nothing for that id.

Half B does not emit a per-node stdout line. The audit GET is the step list.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-31-07 | Agent ran and audit GET is empty | `request_ok` on the agent path. `rows` `[]` or HTTP 404 | Re-run with a known correlation id. Do not invent a step |
| AG-budget | Recursion 12 or step budget 8 | HOLD_FOR_REVIEW. Draft stays a draft | Person at the mapped RT role resumes |
| AG-block | Injection write-from-text | HTTP 409. `error_class=blocked`. `EV-12` | Leave the case unchanged |
| AG-tool | Name outside the six reads | Tool helper returns `forbidden_role` | Leave `WRITE_TOOLS` empty |
| AG-replay | Draft generate misses the file | Agent draft abstains. Query Half B line is separate | Keep `MODEL_MODE=replay` |
| AG-checkpoint | Process exit mid-wait | Host bind from SC-30-01 keeps `checkpoints.sqlite3` | Resume the same `thread_id` |

Dead-letter parking stays on invalid intake. An agent BLOCK is not parked as a later EXECUTE.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| Audit rows for one id | `GET /api/audit/{id}` | SLO-B10 for that run | Agent completion p95 |
| `opa_verdict=BLOCK` | Audit column | SLO-B3 for that action | An availability percent |
| `row_kind=human_approval` | Audit column | SLO-B1 for that write | A cycle-time floor |
| `proposed_by` differs from `actor_id` | Audit columns | SLO-B2 when both are people | A signed SLA |
| `event=request_ok` on the agent path | stdout | The HTTP call finished | The step list |
| Recursion limit 12 | `graph.py` | The engineering default | A latency SLO |

Agent completion time stays Unknown. **Verified Fact.** FD-19. FD-11.

---

## Cost and the 0C envelope

Agent draft under replay adds no live model token. Line B1 stays 0 and 0. Lines B2 to B7 stay Unknown. This half claims no dollar benefit. **Verified Fact.** FD-19.

---

## Half B check

Half B did not change this file's store. The one small check is HB-31-01 on Application A query. Measured cells are in `telemetry-results.md`. Honesty: REAL.

---

## What this file does not do

This file does not add a per-node stdout event. It does not add a write tool. It does not invent an agent duration floor. It does not write code.
