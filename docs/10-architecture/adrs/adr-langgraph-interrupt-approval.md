# ADR: LangGraph interrupt and approval

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | ACCEPTED. Documents FD-06. Does not change the lock. Recursion-limit number and tool names stay later (FD-15). |
| Evidence sources | `Execution_Plan.md` section 4 and Phase 10; `Project_Intent.md` sections 10.2 and 10.3; `docs/08-ai-qualification/minimum-agency-assessment.md`; `Decision_Tracker.md` FD-02, FD-06, FD-15, BO-03, BO-09 |
| Assumptions | BO-03 working answer remains in force and unsigned. SqliteSaver is the LangGraph SQLite checkpointer named in the Phase 10 locked facts. |
| Unresolved issues | FD-15 PENDING: tool allow-list, recursion-limit number, checkpoint file path. Company titles for RT-01 to RT-06 stay Unknown. |
| Residual risks | Giving the model a write tool would bypass FD-02. Skipping SqliteSaver would fail the mid-approval restart in minutes 36 to 39. |

This ADR records the locked agent-control choice. Agents run in LangGraph. The approval pause uses `interrupt()` and `Command(resume=...)`. SqliteSaver writes checkpoints. A recursion limit caps steps. Tools that reach the model are read-only.

---

## Decision

**Verified Fact.** `Execution_Plan.md` section 4 and Phase 10 locked facts. FD-02.

- LangGraph runs a named graph of steps.
- `interrupt()` stops the graph and saves its state when a person must decide.
- `Command(resume=...)` continues the graph after that person records a decision.
- SqliteSaver writes the saved state to a SQLite file so a process restart keeps the wait.
- A recursion limit exists. The number is Unknown here.
- Tools that reach the model are read-only. The step that changes a record is code after the human gate.

**Verified Fact.** BO-03 working answer, still PROPOSED. AI explains and proposes. A person approves every record-changing action. This ADR does not sign BO-03.

**Verified Fact.** BO-09. The person who proposes an action is a different person from the person who approves it.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected |
|---|---|---|
| Hand-built pause flags in process memory | A boolean on the running server | A restart during the demo drops the waiting case. Phase 10 requires the restart to keep state |
| Write tools on the model | The model updates `cases.status` or `engineering_hold` | FD-02 forbids write tools. BO-03 working answer forbids autonomous writes |
| No recursion limit | The graph may loop until the 40-minute slot is gone | Phase 10 requires a recursion limit. The number stays for FD-15 |
| CrewAI or AutoGen-style multi-agent chat | Agents talk to each other with a looser step list | Harder to bound. Harder to show one approval gate to a board |
| OpenAI Agents SDK as the pause mechanism | Tool and guardrail support | Approval pause and saved state would still need extra work. The lock already names LangGraph `interrupt()` |
| Microsoft Agent Framework or Semantic Kernel | A Microsoft-stack agent runtime | Nothing in the locked plan picks it. Extra setup on this laptop |
| Streamlit-only click-to-approve with no graph checkpoint | A button that is not backed by saved graph state | Restart safety would be missing |

Worked example. Scenario 8: step recipe R02, tool recipe R01. Honesty: REAL pattern on 91 of 125 steps. Code raises the mismatch. The model may name both values. `interrupt()` waits. A Process Engineer at RT-03 approves a hold or a release. The model does not write `engineering_hold`.

---

## Why this wins for a laptop demo

Minutes 13 to 25 need a visible agent trace and an approval gate. Minutes 36 to 39 need a restart while an approval is waiting.

`interrupt()` is the pause the audience can see. SqliteSaver is the file that makes the restart work. Both run in-process with a SQLite file. No extra queue server.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Runaway loops | Recursion limit. Number in FD-15 |
| Model writes a record | No write tool on the allow-list. FD-02 |
| Approver is the same person as the proposer | BO-09. Queue enforces two people |
| Untrusted feed text treated as a resume command | Text stays data. OPA can BLOCK. See `adr-opa-gates.md` |
| Inventing the numeric limit now | Leave FD-15 PENDING |

---

## Cost and token or runtime impact

Each LangGraph step that calls the model spends prompt and completion tokens.

`interrupt()` saves a re-run of earlier steps after the person decides. That avoids paying those tokens again on resume.

**Assumption.** Replay mode spends 0 live tokens during the demo. Live token counts stay Unknown.

SqliteSaver writes local disk. No extra hosted checkpoint service.

Honesty: recursion-limit number Unknown. Packaged mismatch count 91 of 125 is REAL.

---

## Portability lesson

Use the agent's own pause and a file-backed checkpoint when the demo must restart mid-wait. Rebuild pause in application memory only if the process is guaranteed not to die. This demo has no such guarantee.

---

## Finding

**Finding.** LangGraph `interrupt()` and `Command(resume=...)`, SqliteSaver, a recursion limit, and read-only tools are the locked agent-control shape.
**Evidence.** `Execution_Plan.md` section 4 and Phase 10. FD-02. FD-06.
**Impact.** Phase 10 builds `apps/app_a/agent/`. Application B reuses the same control pattern with lake-only reads.
**Risk.** Filling the tool list or the numeric limit here would skip FD-15.
**Confidence.** High on the library and the pause. Unknown on the number and the tool names.
**Open questions.** FD-15. Checkpoint path. BO-03 still unsigned.

---

## What this ADR does not do

This ADR does not write agent code. It does not set the recursion-limit number. It does not name the tool allow-list. It does not sign BO-03.
