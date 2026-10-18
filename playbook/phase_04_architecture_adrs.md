# Phase 4 — Target architecture and ADRs

> Spine unit: 10 | Guidelines 1, 11 | Decision gate: FD-06

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test before Phase 5 starts.

## Inputs

- `Execution_Plan.md` section 4 (the locked architecture)
- Phase 3 PRD `docs/09-initial-prd/`
- `Project_Intent.md`
- `Decision_Tracker.md` (section 6 row for Phase 4)

## Prompt

```text
# Phase 4 — Target architecture and ADRs

## Objective
Write the target architecture and an ADR for every fixed choice in `Execution_Plan.md` section 4, including the audit chain and the Context Lake review loop. Each ADR records the alternatives, the risks, the cost, and why the choice was made.

## Scope
Analyse across the two-application design, the lake as YAML built into one SQLite file, the `edges` table instead of a graph server, LangGraph `interrupt()` and `Command(resume=...)`, OPA gates, the fixed ports, App B reading only the lake, the correlation-id audit chain, and the Context Lake review loop. Exclude: code.

## Sub-stages
- 10 Target architecture and ADRs. `docs/10-architecture/`: `architecture-options.md`, `target-architecture.md`, `component-model.md`, `security-architecture.md`, `architecture-decision-summary.md`. `docs/10-architecture/adrs/`: one ADR per fixed choice, including `adr-two-applications.md`, `adr-lake-yaml-to-sqlite.md`, `adr-knowledge-graph-edges-table.md`, `adr-langgraph-interrupt-approval.md`, `adr-opa-gates.md`, `adr-ports-and-compose.md`, `adr-app-b-reads-only-the-lake.md`, `adr-audit-chain.md`, `adr-context-lake-review-loop.md`. Sub-gate: every fixed choice has an ADR that lists its rejected options.

## Required analysis
For each fixed choice: the options considered; why this one wins for a laptop-demoable, portable capstone; the risks and mitigation; the cost and token or runtime impact; the portability lesson. For each ADR: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
Each ADR names the rejected options. Classify claims as Verified Fact, Inference, Assumption, or Unknown. Cite the PRD and the plan.

## Constraints and guardrails
Do not change the fixed choices; they are locked. Do not write code. Do not omit an alternative; an ADR without rejected options is incomplete. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Two apps | App A from its own transformed code; App B only from the lake |
| Lake build | YAML in Git built by `build.py` into `context-lake.sqlite3` (items, edges, terms, FTS5) |
| Knowledge graph | An `edges` table plus recursive CTEs, not a graph database |
| Agent control | LangGraph `interrupt()` and `Command(resume=...)`, SqliteSaver checkpoints, recursion limit, read-only tools |
| Policy gate | OPA returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK |
| Audit chain | One row per agent step and per human approval, keyed by a correlation id |
| Ports | 8080 legacy, 8090 gateway, 8091 lake REST, 8092 lake MCP |

## Decision gate (before you start)
FD-06 the locked architecture is DECIDED; this phase documents it, including the two new choices (audit chain, review loop). No Business Owner decision is required.

## Required artifacts
The `docs/10-architecture/` and `docs/10-architecture/adrs/` folders, each file with the standard header and, for ADRs, an alternatives section.

## Completion gate
Complete only when the sub-gate passes: every fixed choice has an ADR with alternatives, including the audit chain and the review loop.

## Required final response
Return the seven items.

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `target-architecture.md` | Header. The two-app design, the lake build, the edges table, the agent control, OPA, the audit chain, the ports. |
| `docs/10-architecture/adrs/*` | Header. One ADR per fixed choice in section 4, each with an alternatives section listing the rejected options. Includes `adr-audit-chain.md` and `adr-context-lake-review-loop.md`. |
| `architecture-decision-summary.md` | Header. A one-line summary per ADR with the choice and the main rejected option. |

## Done test

Each fixed choice in `Execution_Plan.md` section 4 has a matching ADR file, including `adr-audit-chain.md` and `adr-context-lake-review-loop.md`. Open any ADR; it lists rejected options.
