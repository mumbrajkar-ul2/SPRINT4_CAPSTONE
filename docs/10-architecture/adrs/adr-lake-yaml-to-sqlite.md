# ADR: lake YAML built into SQLite

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | ACCEPTED. Documents FD-06. Does not change the lock. |
| Evidence sources | `Execution_Plan.md` sections 4, 5, 11; `Project_Intent.md` section 9; `00-Best Practices/Semantic_Layer_capture.pdf` format as cited in the plan; `Decision_Tracker.md` FD-06, FD-07 |
| Assumptions | SQLite on this laptop supports FTS5 and recursive queries. That support is treated as a Verified Fact of the local Python SQLite build used in earlier discovery. Column lists inside `items` stay later (FD-07). |
| Unresolved issues | FD-07 lake item schema is PENDING for Phase 5. Five contract gates are Phase 5 work. |
| Residual risks | Editing `context-lake.sqlite3` by hand would make Git YAML and the generated file disagree. Copying the 125 lot rows into the lake would break the Phase 5 exclude. |

This ADR records the locked choice that the Context Lake is authored as YAML in Git and built by `build.py` into one SQLite file, `context-lake.sqlite3`, with tables `items`, `edges`, `terms`, and an FTS5 search index.

---

## Decision

**Verified Fact.** `Execution_Plan.md` section 4.

- People and harvest scripts write YAML files in Git.
- Markdown explains. YAML defines. JSON Schema validates. Tests protect. Generated output serves. That is the Sprint 3 semantic-layer format, reused here.
- `build.py` writes `context-lake.sqlite3`.
- The generated file holds `items`, `edges`, `terms`, and FTS5.
- The YAML is the source of truth. A later file that disagrees is fixed or gets an ADR.
- The lake stores knowledge about the estate. It does not copy raw operational rows.

The semantic layer sits inside this file as the `terms` table. The knowledge graph sits inside this file as the `edges` table. `Project_Intent.md` section 9 asked for that placement to be recorded. This ADR records it.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected |
|---|---|---|
| Generated JSON as the only runtime store | Lookup by item id, as in Sprint 3 | Application B needs word search, date filters, and link walks. JSON files make those queries harder |
| A vector database (Chroma or similar) as the source of truth | Embeddings and similarity search | People review YAML in Git. A vector index would become a second source. Add a vector extension later only if a golden question fails without it. That later add is not chosen here |
| PostgreSQL or another server database | Multi-writer and network share | This demo runs on one laptop. An extra server is another process to fail during `docker compose up` |
| A data lakehouse (Delta Lake, Databricks) | Store of data rows | The Context Lake stores knowledge about the data. Phase 5 excludes copying raw rows |
| Serving YAML files directly at run time | Skip `build.py` | No FTS5 index. No single hashable artifact for Application B to build from |
| Semantic layer beside the lake as its own server | Extra listener | Section 4 already puts `terms` in the same SQLite file |

Worked example. A user asks which `recipe_release` limit was valid for a region on 2023-07-01. One SQL filter on `items` by validity dates answers that. A folder of JSON files would need a custom walk.

---

## Why this wins for a laptop demo

**Verified Fact.** `Execution_Plan.md` section 10. One Compose command starts the lake REST API and the lake MCP server.

SQLite is one file. It needs no separate database container. The file can be hashed. Application B is built from that hashed version.

FTS5 is SQLite full-text search. It finds every item that mentions a phrase such as "recipe revision" without a second search server.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Hand edits to the generated SQLite file | Only `build.py` writes it. Runtime opens it read-only |
| YAML and SQLite drift | The YAML wins. Rebuild. Or write an ADR |
| Schema invented too early | FD-07 stays PENDING. This ADR names tables, not columns |
| Search misses a paraphrased question | Golden questions in Phase 5 (FD-10) will show a miss. A vector add stays a later choice if those tests fail |

---

## Cost and token or runtime impact

Build time is local CPU. No model tokens to compile YAML into SQLite.

Harvest may use a model to draft items from documents. **Assumption.** A person reviews those drafts. Token cost of harvest is Unknown until Phase 5 measures it.

Runtime word search and link walks are SQLite queries. They add no model tokens.

Honesty: lake item counts are Unknown until Phase 5. Packaged lot count 125 is REAL and stays in `legacy.sqlite3`, not in the lake.

---

## Portability lesson

Keep knowledge in files people can review in Git. Generate one read-only artifact the next team can hash and hand to Application B. A server database can wait until more than one person writes the lake at the same time outside Git.

---

## Finding

**Finding.** YAML in Git built by `build.py` into `context-lake.sqlite3` (`items`, `edges`, `terms`, FTS5) is the locked lake store.
**Evidence.** `Execution_Plan.md` section 4. FD-06.
**Impact.** Phase 5 writes `build.py` and the YAML. Application B reads the generated file.
**Risk.** Inventing `items` columns here would skip FD-07.
**Confidence.** High on the store. Unknown on the schema.
**Open questions.** FD-07. FD-10. Exact generated path under `context-lake/generated/` is named by Phase 5 and is not re-decided here.

---

## What this ADR does not do

This ADR does not write `build.py`. It does not invent the item schema. It does not start Phase 5. It does not copy raw rows into the lake.
