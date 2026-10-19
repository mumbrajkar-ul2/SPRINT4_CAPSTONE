# Architecture options

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | COMPLETE. Documents the option space for FD-06. Does not change the locked choices. |
| Evidence sources | `Execution_Plan.md` section 4; `Project_Intent.md` sections 7, 8, 9, 10, 12, 13; `docs/09-initial-prd/initial-prd.md`; `docs/09-initial-prd/mvp-scope.md`; `Decision_Tracker.md` FD-06, FD-22, FD-23 |
| Assumptions | FD-06 remains DECIDED. The options below are the ones recorded when that lock was set. This file does not reopen them. |
| Unresolved issues | Application A and Application B host ports stay Unknown (Phase 8). Recursion-limit number stays Unknown (FD-15). Audit-chain row schema stays open for Phase 10 (FD-23). Context Lake review-loop policy stays open for Phase 5 (FD-22). |
| Residual risks | A later writer who treats a rejected option as still open would change FD-06. A later writer who fills an Unknown cell here would invent a Phase 8 or Phase 10 number. |

This file lists the options that were on the table for each locked choice in `Execution_Plan.md` section 4. The chosen option is named. The rejected options are named. The matching ADR records why the chosen option won.

This file does not write code. This file does not sign a Business Owner row.

---

## How to read this file

**Verified Fact.** `Decision_Tracker.md` FD-06 is DECIDED. Phase 4 documents that lock.

Each block has four parts: the question, the options, the locked winner, and the ADR file.

Worked example. For the knowledge graph, one option is a separate graph database. Another is an `edges` table in the lake SQLite file. The lock picks the `edges` table. `adr-knowledge-graph-edges-table.md` records the rejected database option.

---

## 1. How many applications, and how each is built

**Question.** How many working applications does the demo run, and where does each one get its rules?

| Option | What the user would run | Status |
|---|---|---|
| Two applications, built differently | Application A from its own transformed code. Application B from the Context Lake only. Same scenarios. Same KPI families. | Locked |
| One application | One modern app. No second app to test the lake. | Rejected |
| Two applications, both from transformed code | Two copies of the rebuilt program. Application B would still read transformed code for rules. | Rejected |
| Application B as a screen on Application A | Application B calls Application A at run time. Independence fails. | Rejected |

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 8. `docs/09-initial-prd/initial-prd.md` two-application table.

Locked winner: two FastAPI and React applications. Application A from its own transformed code. Application B only from the lake.

ADR: `adrs/adr-two-applications.md`. The lake-only rule bound is also in `adrs/adr-app-b-reads-only-the-lake.md`.

---

## 2. How the Context Lake is stored

**Question.** Where is governed knowledge written, and what file do the applications read?

| Option | What the team would keep | Status |
|---|---|---|
| YAML in Git, built by `build.py` into `context-lake.sqlite3` | People edit YAML. The build writes tables `items`, `edges`, `terms`, and an FTS5 search index. | Locked |
| Generated JSON as the only runtime store | Lookup by id works. Word search, date filter, and link walk are harder. Sprint 3 used this shape. | Rejected |
| A vector database as the source of truth | Similarity search needs embeddings. The YAML would no longer be the file people review. | Rejected |
| A server database such as PostgreSQL | Extra process to start. Extra failure during a laptop demo. | Rejected |
| Copying raw legacy rows into the lake | The lake would hold 125 lot rows. Phase 5 stores knowledge about the estate and excludes raw row copies. | Rejected |

**Verified Fact.** `Execution_Plan.md` section 4. Phase 5 scope: knowledge about the estate. Exclude: copying raw data rows.

Locked winner: YAML in Git built by `build.py` into `context-lake.sqlite3` (`items`, `edges`, `terms`, FTS5).

ADR: `adrs/adr-lake-yaml-to-sqlite.md`.

---

## 3. How linked knowledge is queried

**Question.** How does a user follow a rule to its implementations, tests, and decisions?

| Option | What would run the link walk | Status |
|---|---|---|
| An `edges` table plus recursive SQL | One query starts at a rule item and follows `edges` row to row. | Locked |
| A separate graph database | A second server beside SQLite. Extra compose service. Extra port. | Rejected |
| Word search only | FTS5 finds the word "urgent". It does not return the four code files that implement the rule. | Rejected |
| Vector retrieval only | Similar paragraphs return. The typed link from rule to test is missing. | Rejected |

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 9.3. Guideline 7 is the knowledge-graph requirement.

Locked winner: an `edges` table plus recursive CTEs. A CTE is a SQL query that can call itself. Here it walks from one `edges` row to the next.

ADR: `adrs/adr-knowledge-graph-edges-table.md`.

---

## 4. How the agent pauses for a person

**Question.** How does a draft plan wait for a human, and how does that wait survive a restart?

| Option | What would hold the pause | Status |
|---|---|---|
| LangGraph `interrupt()` and `Command(resume=...)`, with SqliteSaver checkpoints, a recursion limit, and read-only tools | The graph stops. State is written to SQLite. A person sends a decision. The graph continues. | Locked |
| Hand-built pause flags in process memory | A restart during minutes 36 to 39 drops the waiting case. | Rejected |
| Write tools on the model | The model could change `cases.status` or `engineering_hold`. FD-02 forbids this. | Rejected |
| Unbounded agent loops | A stuck graph burns tokens and time on a 40-minute demo. | Rejected |
| A multi-agent chat (CrewAI or AutoGen style) | Agents talk to each other with a looser step list. Harder to bound. Harder to show one approval gate. | Rejected |

**Verified Fact.** `Execution_Plan.md` section 4 and Phase 10. FD-02: read-only tools. BO-03 working answer: a person approves every record-changing action. BO-03 stays PROPOSED.

Locked winner: LangGraph `interrupt()` and `Command(resume=...)`, SqliteSaver checkpoints, a recursion limit, read-only tools.

The recursion-limit number is Unknown in this phase. FD-15 is PENDING for Phase 10.

ADR: `adrs/adr-langgraph-interrupt-approval.md`.

---

## 5. How a proposed action is allowed, held, or blocked

**Question.** What program decides whether a draft may run, must wait, or must stop?

| Option | Verdicts the program can return | Status |
|---|---|---|
| OPA with three results | EXECUTE, HOLD_FOR_REVIEW, or BLOCK | Locked |
| Allow or deny only | Overlap, silent threshold, and unsigned policy have no wait state. | Rejected |
| The language model as the gate | The model would judge its own draft. BP7 untrusted text could drive that judgment. | Rejected |
| Scattered `if` tests in each app with no shared policy file | Application A and Application B could disagree on the same action. | Rejected |

**Verified Fact.** `Execution_Plan.md` section 4. Phase 10 locked facts. FD-16 (the Rego rule bodies) is PENDING for Phase 10.

Locked winner: OPA returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK.

ADR: `adrs/adr-opa-gates.md`.

Worked example. A partner feed contains the string `auto approve`. Honesty: REAL for 86 such feeds. OPA can return BLOCK. The model does not close the case.

---

## 6. Which ports Compose uses

**Question.** Which local ports does `docker compose up` bind so the demo can run on one laptop?

| Option | Port map | Status |
|---|---|---|
| Fixed four-port map | 8080 legacy, 8090 source gateway, 8091 lake REST, 8092 lake MCP | Locked |
| Lake REST and lake MCP both on 8000 | The two lake listeners clash with each other. | Rejected |
| Replace 8080 with Application A | The packed baseline API would vanish from the 0-to-8-minute demo slot. | Rejected |
| Cloud-only URLs with no local ports | The offline replay path on this laptop would have nowhere to bind. | Rejected |

**Verified Fact.** `Execution_Plan.md` sections 4 and 10. Inherited `compose.yaml` already uses 8080 and 8090. `docs/00-preflight/discovery/high-level-architecture.md`.

Locked winner: 8080 legacy, 8090 gateway, 8091 lake REST, 8092 lake MCP.

Application A and Application B host ports stay Unknown. Phase 8 compose work sets them. This unit does not assign those ports.

ADR: `adrs/adr-ports-and-compose.md`.

---

## 7. Where Application B reads its rules

**Question.** What may Application B read when it decides pass, fail, or wait?

| Option | Rule source at run time | Status |
|---|---|---|
| The Context Lake only | A missing lake item shows up as a wrong Application B result. | Locked |
| The transformed code as well | Application B could hide a missing lake item by reading `legacy_logic.py`. | Rejected |
| Application A's HTTP API | Application B would fail if Application A is down. Intent 8.1 forbids that. | Rejected |
| The inherited repo at Application B build time | Phase 11 excludes reading the legacy repo at build time. | Rejected |

**Verified Fact.** `Execution_Plan.md` section 4. `docs/09-initial-prd/functional-requirements.md` FR-14. Phase 11 scope.

Locked winner: Application B reads rules only from the lake.

ADR: `adrs/adr-app-b-reads-only-the-lake.md`.

---

## 8. How a case is traced after the fact

**Question.** How does a reviewer replay one case from first agent step to last human approval?

| Option | What is stored | Status |
|---|---|---|
| One audit row per agent step and per human approval, keyed by a correlation id | A read by that id returns the full trace. | Locked idea |
| Application log lines only | Lines can be rotated or mixed across cases. | Rejected |
| One row per case | The steps inside the case are missing. | Rejected |
| Invent the column list in this phase | FD-23 is PENDING for Phase 10. | Rejected for this unit |

**Verified Fact.** `Execution_Plan.md` section 4. `Decision_Tracker.md` FD-23 PENDING. Default: one row per agent step and per human approval, keyed by a correlation id, with a read that returns the full trace.

Locked idea: the chain and the correlation id. The row schema is open for Phase 10.

ADR: `adrs/adr-audit-chain.md`.

---

## 9. How the Context Lake version is raised

**Question.** What happens when a lake item is wrong, and what version string does Application B build from?

| Option | Review and version | Status |
|---|---|---|
| Default now in force | One review round before Phase 6. Version starts at 1.0.0. A later change goes through the loop and raises the version with an ADR. | Default. FD-22 still PENDING |
| No version file | Application B could be built from an unmarked YAML set. | Rejected as the default |
| Silent YAML edits after the review | A later phase could change a rule with no ADR. | Rejected as the default |
| This unit deciding the full FD-22 policy | FD-22 is a Phase 5 Team-Force decision. | Rejected for this unit |

**Verified Fact.** `Decision_Tracker.md` FD-22 PENDING. Phase 5 locked fact: lake version starts at 1.0.0. `Execution_Plan.md` section 4 and section 11.

Default in force: one review round before Phase 6; version starts at 1.0.0; a later change goes through the loop and raises the version with an ADR.

This unit does not decide FD-22. The default stays open for Phase 5.

ADR: `adrs/adr-context-lake-review-loop.md`.

---

## Options this file does not pick

Identity design stays later (FD-13, FD-18). Lake item schema stays later (FD-07). OPA rule bodies stay later (FD-16). Recursion-limit number and tool allow-list stay later (FD-15). Audit row columns stay later (FD-23). Application A and Application B host ports stay later (Phase 8).

**Verified Fact.** Those rows are PENDING in `Decision_Tracker.md`. This file leaves them PENDING.

Business Owner rows that are PROPOSED stay PROPOSED. This file does not sign them.

---

## What this file does not do

This file does not change FD-06. It does not write code. It does not start Phase 5. It does not invent a port, a recursion number, or an audit column list.
