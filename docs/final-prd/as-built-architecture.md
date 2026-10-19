# As-built architecture

| Field | Value |
|---|---|
| Stage | Phase 16 / Final as-built PRD |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p16-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED with the as-built baseline. |
| Evidence sources | `compose.yaml`; `docs/10-architecture/target-architecture.md`; `docs/10-architecture/component-model.md`; `docs/10-architecture/adrs/adr-ports-and-compose.md`; `docs/10-architecture/adrs/adr-two-applications.md`; `docs/10-architecture/adrs/adr-app-b-reads-only-the-lake.md`; `docs/18-delivery/evidence-checklist.md`; `docs/17-implementation-prd/implementation-prd.md`; FD-13 |
| Assumptions | `MODEL_MODE=replay`. Lake version 1.0.0. Packaged `legacy.sqlite3` stays the operational fixture. |
| Unresolved issues | Live seven-container recreate today Unknown. Live Azure NEEDS_HUMAN. Company titles Unknown. |
| Residual risks | Treating host uvicorn as the finished Compose run. Treating port 8080 as Application A. |

This file records the architecture that runs. It compares that picture to the Phase 4 target. It does not add a service.

---

## Finding

**Finding.** The running listeners are legacy 8080, source gateway 8090, lake REST 8091, lake MCP 8092, Application A 8100, and Application B 8110. Application A takes pass or fail from transformed code. Application B takes pass or fail from the lake. Replay is the laptop model path. Phase 4 left Application A and Application B ports Unknown. Phase 8 named 8100 and 8110. Those names match `compose.yaml`.
**Evidence.** `compose.yaml`. EV-H8080 to EV-H8110. ADR ports. ADR two applications. ADR Application B reads only the lake. Honesty: REAL for the dated health bodies and the file.
**Impact.** A later change can point at the ports that exist.
**Risk.** Binding a new listener to 8000. Replacing 8080 with Application A.
**Confidence.** High on the port map and the rule-source split. Unknown on a later live recreate.
**Open questions.** Who starts Compose for a room rehearsal.

---

## Services that run

| Host port | Container name | Compose service | What it does | Identity | Health evidence |
|---|---|---|---|---|---|
| 8080 | `fabpulse-legacy` | `legacy` | Current-system baseline API | None. Current behaviour | EV-H8080 REAL. Body `{"status": "ok", "service": "fabpulse-legacy"}` |
| 8090 | `fabpulse-source-gateway` | `source-gateway` | Simulated upstream for scenario 11 | None. Inherited fixture | EV-H8090 REAL. Body `{"status": "ok", "service": "source-gateway", "domain": "High Tech"}` |
| none | `fabpulse-bridge` | `bridge` | One-shot seed. `restart: "no"` | n/a | Named in `compose.yaml` |
| 8091 | `fabpulse-lake-rest` | `lake-rest` | Read lake items for screens | `X-Api-Key` except health | EV-H8091 REAL. HTTP 200 `{"ok":true}` |
| 8092 | `fabpulse-lake-mcp` | `lake-mcp` | Read lake items as tools | `X-Api-Key` except health | EV-H8092 REAL. HTTP 200 plus `search_items`, `get_item`, `get_links`, `rule_at` |
| 8100 | `fabpulse-app-a` | `app-a` | Application A API and React screens. Rules from transformed code | Three headers on case reads and writes | EV-H8100 REAL. HTTP 200 `{"ok":true}` |
| 8110 | `fabpulse-app-b` | `app-b` | Application B API and React screens. Rules from the lake. Lineage view | Three headers on case reads and writes | EV-H8110 REAL. HTTP 200 `{"ok":true}` |

Worked example. The speaker opens `http://127.0.0.1:8080` for the current system, `http://127.0.0.1:8100` for Application A, and `http://127.0.0.1:8110` for Application B.

A later live `docker compose up --build` recreate is NEEDS_HUMAN. Phase 15 did not start Compose. The dated health bodies stay the acceptance evidence for those listeners.

---

## Picture that runs

```text
legacy.sqlite3 (packaged operational store)
        |
        v
 Legacy API :8080          Source gateway :8090
        |
YAML in Git --> build.py --> context-lake.sqlite3 (version 1.0.0)
                                    |
                    +---------------+---------------+
                    v                               v
             Lake REST :8091                  Lake MCP :8092
                    |                               |
        +-----------+-----------+                   |
        v                       v                   v
 Application A :8100      Application B :8110     agent tools
 rules from transformed   rules only from
 code                     the lake
        |                       |
        +-----------+-----------+
                    v
     Same scenarios. Same KPI families.
     MODEL_MODE=replay
```

**Verified Fact.** Application A does not call Application B at run time. Application B does not call Application A at run time.

**Verified Fact.** Replay plays back a file named by the SHA-256 hash of the prompt. A missing file returns `replay_miss` and opens no public-network socket.

---

## Compared to the Phase 4 target

Phase 4 locked two FastAPI and React applications over one YAML-built SQLite lake, with an `edges` table, LangGraph `interrupt()`, OPA three-verdict gates, a correlation-id audit chain, and ports 8080, 8090, 8091, and 8092. Application A and Application B host ports were Unknown.

| Phase 4 statement | As-built fact | Label |
|---|---|---|
| Two applications. Application A from transformed code. Application B from the lake | Same split. Application A on 8100. Application B on 8110 | Verified Fact |
| Lake YAML to `context-lake.sqlite3` | Lake version 1.0.0. Pin `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` | Verified Fact |
| Lake REST 8091. Lake MCP 8092 | Those listeners run | Verified Fact of EV-H8091 and EV-H8092 |
| Application host ports Unknown | 8100 and 8110 | Verified Fact of `compose.yaml` and FD-13 |
| Identity design later | Three headers on 8100 and 8110. 8080 and 8090 stay open | Verified Fact |
| LangGraph `interrupt()` later | Built in Phase 10. T-RESTART and T-KILL | Verified Fact |
| OPA three verdicts later | EXECUTE, HOLD_FOR_REVIEW, BLOCK. T-INJECT | Verified Fact |
| Audit column list later | 27 columns. 12 rows on scenario 8 | Verified Fact of T-TRACE |
| Recursion limit Unknown | Engineering default 12. T-RECURSION | Verified Fact of the measured default. Not a latency floor |
| Offline replay planned | `MODEL_MODE=replay` default. 77 files | Verified Fact |
| One `docker compose up` | File present. Later recreate NEEDS_HUMAN | Verified Fact of the file. Unknown for a new start |

Worked example. Phase 4 said the speaker would later learn the Application A URL. The as-built URL is `http://127.0.0.1:8100`.

---

## Stores that run

| Store | Writer | Readers | Label |
|---|---|---|---|
| Packaged `legacy.sqlite3` | Person-approved Application A writes. Bridge seed | Legacy API. Application A operational path | Verified Fact. Hash must still match `sources/register.yaml` |
| `context-lake.sqlite3` | Only `build.py` | Lake REST, lake MCP, Application B rule path, both apps' evidence path | Verified Fact. Version 1.0.0 |
| `operations/model-replay/` | Rehearsal when a live prompt is saved | Replay lookup | Verified Fact. 77 files besides README |
| Application A checkpoint file | LangGraph during `interrupt()` | LangGraph on resume | Verified Fact. Path `apps/app_a/runtime/checkpoints.sqlite3` |
| Application A audit chain | Agent step writer. Human approval writer | `GET /api/audit/{correlation_id}` | Verified Fact. 27 columns |
| Dead-letter file | Park of a failed intake | `GET /api/recovery` | Verified Fact of HB-29-01 and GNG-30-03 |

Application B does not open inherited sqlite for rule evaluation. **Verified Fact.** Phase 11 and Phase 12 TEVV.

---

## Control path that runs

1. A request on 8100 or 8110 sends the three identity headers.
2. Code loads the case and the lake items.
3. Replay returns the saved sentence, or the path abstains on a miss.
4. `check_claim` accepts a cited lake item id or rejects an invented fact.
5. OPA returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK.
6. A record-changing action waits at `interrupt()`.
7. A different person resumes. The audit chain writes the approval row.

**Verified Fact.** `WRITE_TOOLS` is empty. FD-02. T-NO-WRITE-TOOL.

Worked example. Scenario 8 on PS000000016 paused for RT-03. After `taskkill /F` of pid 29320, a new process still carried correlation id `corr-p10b-kill-20261018-001`. `engineering_hold` stayed 0 until a person resumed. Honesty: REAL.

---

## What this file does not do

This file does not add a container. It does not invent a live Compose pass for today. It does not sign BO-13. It does not invent a dollar benefit.
