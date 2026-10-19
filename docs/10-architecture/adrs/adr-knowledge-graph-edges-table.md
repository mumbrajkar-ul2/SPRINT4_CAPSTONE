# ADR: knowledge graph as an edges table

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | ACCEPTED. Documents FD-06. Does not change the lock. |
| Evidence sources | `Execution_Plan.md` section 4; `Project_Intent.md` sections 9 and 9.3; `docs/09-initial-prd/functional-requirements.md` FR-15; `Decision_Tracker.md` FD-06 |
| Assumptions | Recursive SQL (CTEs) on this laptop's SQLite can walk the `edges` table. Edge types and the exact graph questions are Phase 5 work. |
| Unresolved issues | The list of graph questions the CTEs must answer is Phase 5 Half A. FD-07 may add edge fields. |
| Residual risks | Using the graph as the live case store would mix knowledge with operational state. Building a genealogy graph of lots would claim a parent-lot link the packaged tables do not have. |

This ADR records the locked choice that the knowledge graph is an `edges` table in `context-lake.sqlite3`, queried with recursive CTEs. A CTE is a SQL query that can call itself and follow the next `edges` row. The project does not run a graph database.

---

## Decision

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 9.3.

- Store each link as one `edges` row: from-item, link type, to-item.
- Query those rows with recursive SQL.
- Use the graph for explainable relationships, impact, lineage, and retrieval of linked items.
- Do not use the graph as the store for live case status, numeric KPI math, or the pass-or-fail rule itself.

Guideline 7 asks for a knowledge graph where the use case justifies it. This ADR records that justification for knowledge about the estate, and records the store.

Worked example. Scenario 12 traces one rule to four local implementations and a test. The `edges` walk starts at the archive rule item and follows links to the Python, JavaScript, Java, and night-batch deviation items and to the test item.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected |
|---|---|---|
| A separate graph database (Neo4j or similar) | Its own server, its own port, its own backup | Packaged volumes are small (125 lots, 30 tools, 125 steps). A few thousand knowledge links fit in SQLite. A second server is another Compose failure |
| Word search only (FTS5 with no `edges`) | Find items that mention "urgent" | It does not return the typed link from the archive rule to the four code files |
| Vector retrieval only | Return similar paragraphs | The `implements` and `tested_by` link types name the relationship. Vector search returns similar paragraphs |
| Graph of live lots, tools, and metrology as the operational store | Replace SQL joins on `wafer_lots` | Intent 9.3 keeps transactional state in the operational store. The `cases` table has no `lot_id`. That missing join stays a semantic-layer mapping or Unknown |
| Adjacency lists kept only in YAML, with no `edges` table | Walk files at run time | Application B would parse YAML on every lineage click. The lock puts links in `edges` |

---

## Why this wins for a laptop demo

Minutes 25 to 32 open Application B's context view. One SQL walk on `edges` can fill that view. No extra container starts.

The same SQLite file already holds `items` and `terms`. The graph does not need a second product.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Broken or looping links | Phase 5 build checks. Contract gates then |
| Using `relates_to` for every link | Harvest must set a real link type. `cross_references` in the operational store already uses a single weak type. Do not copy that pattern into `edges` |
| Claiming lot genealogy | No parent-lot table exists. Record Unknown. Do not draw a genealogy graph |

---

## Cost and token or runtime impact

A recursive SQL walk uses local CPU. It adds no model tokens.

A language-model explanation may still run after the walk, to write the sentence the user reads. That token cost belongs to FD-04 GenAI jobs. It is not created by the `edges` table.

A graph database would add a container's RAM and a round trip. Those costs are avoided.

Honesty: edge counts are Unknown until Phase 5. 125 lots is REAL and stays in the operational store.

---

## Portability lesson

If the questions are "what links to this rule" and the volume is thousands of links, put an `edges` table next to the items. Add a graph server when many writers, or millions of links, or a live genealogy feed, actually appear.

---

## Finding

**Finding.** The knowledge graph is the `edges` table plus recursive CTEs in the lake SQLite file.
**Evidence.** `Execution_Plan.md` section 4. `Project_Intent.md` section 9.3. FD-06.
**Impact.** Phase 5 builds `edges` and the CTE questions. Scenario 12 reads them.
**Risk.** Standing up Neo4j later without an ADR would change this lock.
**Confidence.** High on the store. Unknown on edge types.
**Open questions.** Phase 5 graph questions. FD-07 edge fields.

---

## What this ADR does not do

This ADR does not write SQL. It does not list edge types. It does not start Phase 5. It does not put live case rows into `edges`.
