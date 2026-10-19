# Human-in-the-loop workflow

| Field | Value |
|---|---|
| Stage | Phase 10 / 23 Human control and audit chain. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/10-architecture/adrs/adr-langgraph-interrupt-approval.md`; `docs/12-specs/api-contracts.md` API-Q-04; `apps/app_a/routes/approvals.py`; LangGraph 1.0.3 `interrupt()` and `Command(resume=...)` |
| Assumptions | SqliteSaver file path is `apps/app_a/runtime/checkpoints.sqlite3`. `thread_id` equals `correlation_id`. |
| Unresolved issues | Company titles stay Unknown. Named demo actors stay the Phase 9 `demo-rt0N-1` ids. |
| Residual risks | Keeping approvals only in the in-memory `_APPROVALS` dict would lose the wait on process stop. |

This file names the person path from a waiting case to a recorded decision.

---

## Finding

**Finding.** A record-changing draft pauses in `interrupt_wait`. SqliteSaver stores the thread. A person at the mapped RT role posts `POST /api/approvals`. Code checks identity, then sends `Command(resume=...)`.
**Evidence.** Locked agent control. Existing approval route. BO-09 separation.
**Impact.** Minutes 36 to 39 can kill the process and still finish the wait.
**Risk.** Resuming from a UI click that never reaches SqliteSaver would fail the Done test.
**Confidence.** High on the API names. Unknown until the restart test runs.
**Open questions.** HALF_A_ACCEPTED.

---

## Steps

1. A person with a closed role starts `POST /api/agent/run` for a `case_id`. Headers carry `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role`, and optional `X-Correlation-Id`.
2. Application A mints `corr-app-a-` plus 12 hex digits when the correlation header is empty. That string is `thread_id`.
3. The graph loads the case, drafts, gathers, grounds, and calls OPA.
4. HOLD_FOR_REVIEW, or EXECUTE with `record_change` true, enters `interrupt_wait`.
5. `interrupt({case_id, proposed_action, waiting_role, draft_plan, citations, correlation_id})` pauses the graph. SqliteSaver writes the file. An audit control row records the pause.
6. The case overlay shows `waiting_role` and `draft_plan`. The queue lists the case.
7. A person at the mapped role, with `actor_id` different from `proposed_by` when `proposed_by` is a person, posts `POST /api/approvals`.
8. `check_write_action` accepts or returns 403.
9. On accept, Application A calls `graph.invoke(Command(resume=payload), {"configurable": {"thread_id": correlation_id}, "recursion_limit": 12})`.
10. `apply_human_decision` writes the overlay mutation and EV-09 or EV-10.
11. `GET /api/audit/{correlation_id}` returns the full list.

Worked example. Start with `X-Actor-Id: demo-rt01-1` on scenario 8. The draft is `proposed_by=model_draft`. Resume with `X-Actor-Id: demo-rt03-1`, `X-Actor-Role: RT-03`, `action_type: recipe_hold_or_release`, `decision: hold`. The overlay sets `engineering_hold` to 1.

---

## Restart in the middle of step 5

1. The process stops after the checkpoint write and before the person posts.
2. Half B starts Application A again. `checkpointer.py` opens the same SQLite file.
3. `GET /api/cases/PS000000016` still shows `waiting_role=RT-03`. Half B rebuilds that view from `graph.get_state(config)` and from audit rows.
4. RT-03 posts. Resume works on the stored `thread_id`.

If the checkpoint file is gone and no approval row exists, the case shows the packaged wait and a new `POST /api/agent/run` starts a new correlation id.

---

## BLOCK path

OPA-R-01 returns BLOCK. The graph skips `interrupt_wait`. No approval resource is offered. `mark_blocked(case_id)` stays. A later `POST /api/approvals` on that case returns 409 `blocked`. That behaviour already exists in `approvals.py`.

---

## What this file does not do

This file does not write the resume call. It does not sign BO-03.
