# Tool permission map

| Field | Value |
|---|---|
| Stage | Phase 10 / 22 Agentic engineering. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | FD-02; FD-15; `docs/11-data-context/data-contracts.md`; `apps/app_a/intelligence/generate.py` `WRITE_TOOLS`; `apps/shared/identity.py` `ACTION_ROLE_MAP` |
| Assumptions | The model sees only the allow-list. Person writes stay on `POST /api/approvals`. |
| Unresolved issues | Company titles for RT-01 to RT-06 stay Unknown. |
| Residual risks | Registering `record_approval` in the LangGraph tool node would give the model a write. |

This file is the FD-15 allow-list. Tools that reach the model stay read-only.

Engineering decision ED-P10A-03, authority: team-force.

---

## Finding

**Finding.** The model may call six tools: `search_items`, `get_item`, `get_links`, `rule_at`, `get_case`, and `get_recovery_status`. The write-tool list is empty.
**Evidence.** FD-02. The four lake names are locked and must stay. `WRITE_TOOLS = []` already sits in `generate.py`. BO-03 working answer: a person approves every record-changing action.
**Impact.** Half B passes this list into the gather node. A unit test fails if a write name appears.
**Risk.** A later helper that posts approvals from a tool wrapper would skip the person.
**Confidence.** High
**Open questions.** None for the names.

---

## Allow-list (reaches the model)

| Tool | Who may invoke it | What it may read | What it may write |
|---|---|---|---|
| `search_items` | Node `gather_tools` | Lake items | Nothing |
| `get_item` | Node `gather_tools` | One lake item | Nothing |
| `get_links` | Node `gather_tools` | Lake edges | Nothing |
| `rule_at` | Node `gather_tools` | One archive rule or a wait verdict | Nothing |
| `get_case` | Node `gather_tools` | One Application A case | Nothing |
| `get_recovery_status` | Node `gather_tools` | Last recovery probe | Nothing |

Worked example. Scenario 7. `get_case("REPLAY-000000000")` returns `processing_status=REPLAY` and any flagged notes. The model may draft a drop proposal. The drop itself waits for RT-05 on `POST /api/approvals`.

---

## Deny-list (must not reach the model)

| Function or route | Who may call it |
|---|---|
| `store.record_approval` | `POST /api/approvals` after role check |
| `store.mark_blocked` | Application A code on OPA BLOCK |
| `store.set_draft` | Node `plan_draft` in process. Not a model tool |
| `Command(resume=...)` | `POST /api/approvals` |
| `opa_client.evaluate` | Node `opa_gate` |
| `audit.writer.append` | Every node in process |
| Azure or replay `complete` | Node `plan_draft` in process. Not a tool the model chooses |

---

## Role map on the person route

**Verified Fact.** BO-09. Group C.

The model is never `X-Actor-Role` on a write. `approvals.py` already rejects a role or actor that starts with `model`.

| `action_type` | Allowed role | Forbidden |
|---|---|---|
| `dispose` | RT-01 | Model. Same person as `proposed_by` |
| `approve_agent` | RT-02 | Proposing agent. Same person as `proposed_by` |
| `recipe_hold_or_release` | RT-03 | Operations Analyst acting alone. The model |
| `policy_pick` | RT-04 | The model |
| `keep_wait` | RT-04 | The model |
| `replay_confirm` | RT-05 | An unattended job. The model |
| `assign_owner` | RT-06 | A made-up name. The model |

---

## Half B test

File a test that imports the allow-list constant and asserts:

1. The set equals the six names above.
2. The write list is `[]`.
3. None of `update`, `write`, `approve`, `hold`, `drop`, `assign`, or `delete` appears in a tool name.

Honesty on that test: Unknown until Half B. The design names the assertion now.

---

## What this file does not do

This file does not bind the tools in Python. It does not give the model a write tool.
