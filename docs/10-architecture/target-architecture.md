# Target architecture

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | COMPLETE. Documents the locked FD-06 architecture. Does not change the choices. |
| Evidence sources | `Execution_Plan.md` sections 4, 5, 8, 10, 11; `Project_Intent.md` sections 7, 8, 9, 10; `docs/09-initial-prd/initial-prd.md`; `docs/09-initial-prd/capability-map.md`; `Decision_Tracker.md` FD-02, FD-04, FD-06, FD-22, FD-23 |
| Assumptions | FD-06 remains DECIDED. BO-03 working answer remains in force and unsigned. Demo replay (`MODEL_MODE=replay`) remains the planned laptop mode. |
| Unresolved issues | FD-22 PENDING for Phase 5. FD-23 schema open for Phase 10. FD-15, FD-16 PENDING for Phase 10. Application A and Application B host ports Unknown. |
| Residual risks | A builder who copies a rule from Application A into Application B by hand would hide a missing lake item. A builder who invents the audit column list here would skip FD-23. |

This file states the locked target architecture. It is the arrangement both applications, the Context Lake, the agent pause, the policy gate, the audit chain, and the ports will follow.

This file does not write code. This file does not sign a Business Owner row.

---

## Locked picture

**Verified Fact.** `Execution_Plan.md` section 4.

Two FastAPI and React applications sit over one shared, read-only Context Lake.

```text
Legacy estate (read only for harvest)
  legacy.sqlite3 (19 tables)
  enterprise_legacy.sqlite3 (12 tables)
  bundled events, docs, finance
  Python, JavaScript, Java, night-batch rules
           |
           v
YAML items + semantic layer in Git
           |
        build.py
           |
           v
context-lake.sqlite3
  tables: items, edges, terms
  search: FTS5
           |
           +--> REST on 8091
           +--> MCP on 8092
                    |
        +-----------+-----------+
        v                       v
 Application A              Application B
 rules from its own         rules only from
 transformed code           the Context Lake
        |                       |
        +-----------+-----------+
                    v
     Same scenarios. Same KPI families.
```

Worked example. Scenario 13 runs the same five cases on both applications. If Application A marks a case as needing review because its rebuilt program still has the Python 50,000 cutoff, and Application B does not, the difference traces to a missing or wrong lake item.

---

## Two applications

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 8. `docs/09-initial-prd/initial-prd.md`.

| Name | How it is built | Where it reads its rules | What else it may read |
|---|---|---|---|
| Application A | Rebuild of the current fab-exception program, with language-model help only where FD-04 allowed it | From its own transformed code | The lake, for evidence, citations, and explanation |
| Application B | Built from the Context Lake | Only from the Context Lake | The lake, including the context view that shows the item behind a rule |

**Verified Fact.** Both applications run without calling the other at run time.

**Verified Fact.** Both applications run demo scenarios 7 to 11 with the same inputs. Both are scored on the same eight KPI families.

**Verified Fact.** The service stack for both applications is FastAPI for the HTTP API and React for the screens. `Execution_Plan.md` section 4 opening sentence.

The inherited legacy API stays on port 8080 so the 0-to-8-minute baseline slot still has a running current system. Application A lives later under `apps/app_a/`. Application B lives later under `apps/app_b/`.

Application A and Application B host ports are Unknown in this phase.

ADR: `adrs/adr-two-applications.md`, `adrs/adr-app-b-reads-only-the-lake.md`.

---

## Lake build

**Verified Fact.** `Execution_Plan.md` section 4. Phase 5 output path.

People and harvest scripts write YAML in Git. `build.py` reads that YAML and writes one generated file, `context-lake.sqlite3`.

| Piece | What it holds |
|---|---|
| `items` | One row per knowledge item |
| `edges` | One row per link from one item to another |
| `terms` | One row per semantic-layer term and cross-system mapping |
| FTS5 | Word search over item text |

The YAML is the source of truth. `Execution_Plan.md` section 11. A later file that disagrees is fixed or gets an ADR.

The lake stores knowledge about the estate. It does not copy the 125 lot rows into itself. Phase 5 states that exclude.

At run time the lake file is read-only for both applications. Only `build.py` writes it.

The lake is served two ways:

- REST on port 8091, for screens.
- MCP on port 8092, for agents and other tool clients. MCP is the Model Context Protocol. It exposes the same lake reads as tools.

The item schema is later (FD-07 PENDING). This file names the four generated stores. It does not invent columns.

ADR: `adrs/adr-lake-yaml-to-sqlite.md`.

---

## Edges table

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 9.3.

The knowledge graph is the `edges` table in `context-lake.sqlite3`. A recursive SQL query (a CTE) walks those rows.

The graph answers relationship questions. Example: which four programs implement the urgent-amount rule, which test locks it, and which decision recorded the archive as canonical.

The graph does not store live case status. Live case status stays in the operational store. `Project_Intent.md` section 9.3.

A separate graph database is rejected.

ADR: `adrs/adr-knowledge-graph-edges-table.md`.

---

## Agent control

**Verified Fact.** `Execution_Plan.md` section 4 and Phase 10. FD-02.

Agents run in LangGraph. LangGraph is the library that runs a named sequence of steps.

The approval pause uses `interrupt()`. That call stops the graph and saves its state. The person later sends a decision with `Command(resume=...)`. The graph continues from the saved state.

SqliteSaver writes that saved state to a SQLite file. Minutes 36 to 39 of the demo restart a waiting approval. The waiting case is still there after the restart.

A recursion limit caps how many steps the graph may take. The number is Unknown here. FD-15 is PENDING for Phase 10.

Tools that reach the model are read-only. The model has no write tool. A record-changing action waits for a person.

**Verified Fact.** BO-03 working answer, still PROPOSED. AI explains and proposes. A person approves every record-changing action. This file does not sign BO-03.

**Verified Fact.** FD-04. Ranking, rule pass-or-fail, reconciliation, and de-duplication stay in code. Conflict explanation, natural-language answers, and draft plans may use a language model.

ADR: `adrs/adr-langgraph-interrupt-approval.md`.

---

## OPA policy gate

**Verified Fact.** `Execution_Plan.md` section 4.

OPA is Open Policy Agent. It is a program that loads a policy file and returns a verdict.

The verdict is one of three strings:

| Verdict | What the application does |
|---|---|
| EXECUTE | The next code step may run. For a record-changing action this still waits on the human gate under BO-03. |
| HOLD_FOR_REVIEW | The case waits for a named run-time role. |
| BLOCK | The action stops. The demo injection path must produce this result. |

The Rego rule bodies are later (FD-16 PENDING). This file locks the three verdicts. It does not write the policy files.

Worked example. Scenario 10: 34 active policy rows sit on eight country codes. Honesty: REAL. Overlap routes to HOLD_FOR_REVIEW. A Policy Owner at RT-04 picks a policy or keeps the wait.

ADR: `adrs/adr-opa-gates.md`.

---

## Audit chain

**Verified Fact.** `Execution_Plan.md` section 4. `Decision_Tracker.md` FD-23 PENDING.

Every agent step writes one audit row. Every human approval writes one audit row. Each row carries a correlation id. A read by that id returns the full trace for one case.

This is the Sprint 3 S05-14 practice, reused here.

The column list is open for Phase 10. This file does not invent the row schema.

ADR: `adrs/adr-audit-chain.md`.

---

## Ports

**Verified Fact.** `Execution_Plan.md` sections 4 and 10.

| Port | Listener | Already in inherited compose |
|---|---|---|
| 8080 | Legacy API | Yes |
| 8090 | Source gateway | Yes |
| 8091 | Lake REST | No. Added by this architecture |
| 8092 | Lake MCP | No. Added by this architecture |

**Verified Fact.** `Execution_Plan.md` section 10. One `docker compose up` starts the legacy app, the source gateway, the lake REST API, the lake MCP server, and both app UIs. Seed the bundled tier.

Application A and Application B host ports stay Unknown.

ADR: `adrs/adr-ports-and-compose.md`.

---

## Context Lake review loop (default in force)

**Verified Fact.** `Decision_Tracker.md` FD-22 PENDING. `Execution_Plan.md` sections 4, 5, and 11.

The Context Lake carries a version. The default now in force is:

1. One review round before Phase 6.
2. The version starts at 1.0.0.
3. A later change goes through the review, a fix round, and a revision that raises the version and records an ADR.

This unit does not decide FD-22. The default stays open for Phase 5.

ADR: `adrs/adr-context-lake-review-loop.md`.

---

## What sits outside this picture

| Topic | Why it is outside this file | Label |
|---|---|---|
| Lake item schema | FD-07 PENDING, Phase 5 | Verified Fact |
| Golden questions | FD-10 PENDING, Phase 5 | Verified Fact |
| Recursion-limit number and tool names | FD-15 PENDING, Phase 10 | Verified Fact |
| OPA rule bodies | FD-16 PENDING, Phase 10 | Verified Fact |
| Identity and RBAC design | FD-13, FD-18 PENDING | Verified Fact |
| Audit column list | FD-23 PENDING, Phase 10 | Verified Fact |
| Signed BO-03, BO-04, and other PROPOSED rows | Stay PROPOSED | Verified Fact |

---

## Finding

**Finding.** The locked architecture is two FastAPI and React applications over one YAML-built SQLite lake, with an `edges` table, LangGraph `interrupt()`, OPA three-verdict gates, a correlation-id audit chain, and ports 8080, 8090, 8091, and 8092.
**Evidence.** `Execution_Plan.md` section 4. FD-06 DECIDED.
**Impact.** Later phases implement this picture. They do not pick a second lake store or a second approval library.
**Risk.** Filling FD-15, FD-16, FD-22, or FD-23 in this file would invent a later-phase design.
**Confidence.** High on the lock. Unknown on the open later-phase numbers.
**Open questions.** See Unresolved issues in the header.

---

## What this file does not do

This file does not change FD-06. It does not write code. It does not start Phase 5. It does not invent the audit schema. It does not decide FD-22. It does not sign a Business Owner row.
