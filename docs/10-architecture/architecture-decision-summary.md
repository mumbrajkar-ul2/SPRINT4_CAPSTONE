# Architecture decision summary

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | COMPLETE. One line per ADR. Does not change FD-06. |
| Evidence sources | `docs/10-architecture/adrs/`; `Execution_Plan.md` section 4; `Decision_Tracker.md` FD-06, FD-22, FD-23 |
| Assumptions | Each ADR file on disk matches the line below. |
| Unresolved issues | FD-22 remains PENDING for Phase 5. FD-23 row schema remains open for Phase 10. |
| Residual risks | A later writer who expands a one-line summary into a new choice would reopen a locked ADR. |

This file is the one-line index of every Phase 4 ADR. Each line names the choice and the main rejected option.

Business Owner rows that are PROPOSED stay PROPOSED. This file does not sign them.

---

## Summary

**Verified Fact.** FD-06 DECIDED. The ADR files in `docs/10-architecture/adrs/` record the lock.

| ADR | Choice | Main rejected option |
|---|---|---|
| `adrs/adr-two-applications.md` | Two FastAPI and React applications: Application A from its own transformed code, Application B from the lake, same scenarios and KPI families | One application, or a second app that is only a screen on the first |
| `adrs/adr-lake-yaml-to-sqlite.md` | YAML in Git, built by `build.py` into `context-lake.sqlite3` (`items`, `edges`, `terms`, FTS5) | Generated JSON as the only runtime store, or a separate server database as the lake |
| `adrs/adr-knowledge-graph-edges-table.md` | An `edges` table plus recursive CTEs inside the lake SQLite file | A separate graph database |
| `adrs/adr-langgraph-interrupt-approval.md` | LangGraph `interrupt()` and `Command(resume=...)`, SqliteSaver checkpoints, a recursion limit, read-only tools | In-memory pause flags, write tools on the model, or an unbounded multi-agent chat |
| `adrs/adr-opa-gates.md` | OPA returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK | The language model as the policy gate, or allow-or-deny with no wait state |
| `adrs/adr-ports-and-compose.md` | 8080 legacy, 8090 source gateway, 8091 lake REST, 8092 lake MCP, started by Compose | Putting both lake listeners on 8000, or replacing 8080 with Application A |
| `adrs/adr-app-b-reads-only-the-lake.md` | Application B takes its rules only from the Context Lake | Application B importing transformed code, or calling Application A at run time |
| `adrs/adr-audit-chain.md` | One audit row per agent step and per human approval, keyed by a correlation id. Schema open for Phase 10 | Log lines only, or inventing the column list in this phase |
| `adrs/adr-context-lake-review-loop.md` | Default in force: one review round before Phase 6, version starts at 1.0.0, a later change raises the version with an ADR. FD-22 still open for Phase 5 | No version file, or this unit deciding FD-22 itself |

Worked example. Open `adrs/adr-knowledge-graph-edges-table.md`. The chosen store is the `edges` table. The rejected store is a graph database such as Neo4j.

---

## Status of the two still-open rows

| ID | What this phase recorded | What stays open | Label |
|---|---|---|---|
| FD-22 | The default in force | How the loop runs in detail, and when the version string changes. Phase 5 | Verified Fact of PENDING |
| FD-23 | The locked idea: one row per step and per approval, correlation id, full-trace read | The row schema and the read path design. Phase 10 | Verified Fact of PENDING |

---

## Finding

**Finding.** Nine ADRs cover every fixed choice in `Execution_Plan.md` section 4, including the audit chain and the Context Lake review loop.
**Evidence.** The nine files under `docs/10-architecture/adrs/`.
**Impact.** A reviewer can open any ADR and see the rejected options.
**Risk.** A missing alternatives section would fail the Phase 4 Done test.
**Confidence.** High that the nine files are the required set.
**Open questions.** FD-22. FD-23 schema.

---

## What this file does not do

This file does not add a tenth architecture choice. It does not write code. It does not start Phase 5. It does not sign a Business Owner row.
