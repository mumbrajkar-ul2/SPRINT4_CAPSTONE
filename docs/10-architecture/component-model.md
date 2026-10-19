# Component model

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | COMPLETE. Names the locked components. Does not write code. |
| Evidence sources | `Execution_Plan.md` sections 4, 5, 9, 10, 11; `Project_Intent.md` sections 7.1, 8, 9, 10.3; `docs/09-initial-prd/capability-map.md`; `docs/00-preflight/discovery/high-level-architecture.md`; `Decision_Tracker.md` FD-02, FD-06, FD-22, FD-23 |
| Assumptions | FD-06 remains DECIDED. Shared lake reads are allowed. Hidden Application A to Application B calls at run time stay forbidden. |
| Unresolved issues | Internal module names inside `apps/app_a/` and `apps/app_b/` stay later. Host ports for those two apps stay Unknown. Checkpoint file path stays Unknown. |
| Residual risks | Treating the inherited 8080 API as Application A would mix the baseline with the transformed app. Treating Compose as a third application would hide that it only starts the others. |

This file names each locked component and what it does. It names who talks to whom.

This file does not write code. This file does not sign a Business Owner row.

---

## Component list

**Verified Fact.** `Execution_Plan.md` section 4 and the phase output paths in section 5.

| Component | What it does | When it is built |
|---|---|---|
| Legacy API | Serves the current GET routes for cases, metrics, partners, and domain tables | Already present. Stays on 8080 |
| Source gateway | Serves simulated upstream events | Already present. Stays on 8090 |
| Harvest scripts | Read schemas, counts, and code. Draft lake YAML. Do not copy raw lot rows into the lake | Phase 5 |
| YAML items in Git | One knowledge item per file, reviewed in Git | Phase 5 |
| Semantic layer YAML | Canonical names and cross-system mappings | Phase 5 |
| `build.py` | Validates YAML and writes `context-lake.sqlite3` | Phase 5 |
| `context-lake.sqlite3` | Holds `items`, `edges`, `terms`, and FTS5 | Phase 5 generated output |
| Lake REST | Read API for screens, port 8091 | Phase 5 serving, Phase 8 compose |
| Lake MCP | Read tools for agents, port 8092 | Phase 5 serving, Phase 8 compose |
| Application A API and React UI | Fab-exception workflow. Rules from transformed code | Phase 7 transform, Phase 9 app |
| Application B API and React UI | Same workflow. Rules only from the lake. Context view for lineage | Phase 11 |
| LangGraph agent | Named steps, read-only tools, recursion limit | Phase 10 in Application A. Same control pattern in Application B |
| SqliteSaver | Writes paused agent state so a restart keeps the wait | Phase 10 |
| OPA | Returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK | Phase 10, `policy/opa/` |
| Audit chain | One row per agent step and per human approval, keyed by a correlation id | Phase 10. Schema then. |
| Approval queue | Shows a waiting case to RT-01 through RT-06 | Phase 10 |
| Parity harness | Runs the same scenarios on both applications | Phase 11 |
| Docker Compose | One command starts the listeners on this laptop | Inherited file, extended from Phase 8 |

---

## Who talks to whom

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 8.1.

```text
Harvest scripts --> YAML in Git --> build.py --> context-lake.sqlite3
                                                    |
                                    +---------------+---------------+
                                    v                               v
                             Lake REST :8091                  Lake MCP :8092
                                    |                               |
                    +---------------+---------------+               |
                    v               v               v               v
             App A screens   App B screens    App A agent ---- tools
             App B context view                 App B agent ---- tools
                    |                               |
                    v                               v
                  OPA  <-------------------- proposed action
                    |
                    v
            interrupt() / approval queue
                    |
                    v
            audit chain (correlation id)
```

**Verified Fact.** Application A does not call Application B at run time. Application B does not call Application A at run time.

**Verified Fact.** Both applications may read the shared lake. Application A still takes its rules from its own transformed code. Application B takes its rules only from the lake.

The legacy API on 8080 stays a baseline listener. Application A does not replace that port in this architecture.

---

## Runtime stores

| Store | Writer | Readers | Label |
|---|---|---|---|
| `data/legacy.sqlite3` | Current bridge and partner reconcile. Later Application A writes wait on a person | Legacy API. Application A operational path | Verified Fact of current writers. Inference that Application A remains the operational writer after Phase 9 |
| `data/enterprise_legacy.sqlite3` | Night batch and related jobs today | Harvest. Reports | Verified Fact of current tree |
| YAML in Git | People and harvest scripts | `build.py` | Verified Fact |
| `context-lake.sqlite3` | Only `build.py` | Lake REST, lake MCP, Application B rule path, both apps' evidence path | Verified Fact of the lock |
| SqliteSaver checkpoint file | LangGraph during `interrupt()` | LangGraph on resume and after restart | Verified Fact of the lock. Path Unknown |
| Audit chain store | Agent step writer. Human approval writer | Read by correlation id | Verified Fact of the idea. Schema Unknown until Phase 10 |

Worked example. `build.py` writes `context-lake.sqlite3`. Application B opens that file through port 8091 or 8092. Application B does not open `app/legacy_logic.py` to decide pass or fail.

---

## Agent and gate components

**Verified Fact.** `Execution_Plan.md` Phase 10. `Project_Intent.md` section 10.3.

| Piece | Bound |
|---|---|
| Tool allow-list | Read-only. Names later (FD-15) |
| Recursion limit | Exists. Number later (FD-15) |
| `interrupt()` | Stops the graph and saves state |
| `Command(resume=...)` | Continues after a person decides |
| SqliteSaver | Survives a process restart |
| OPA | Three verdicts only |
| Audit writer | One row per step. One row per approval |

**Verified Fact.** BO-09. The person who proposes an action is a different person from the person who approves it.

Company job titles for RT-01 to RT-06 stay Unknown.

---

## UI and demo components

**Verified Fact.** `Execution_Plan.md` section 10. `docs/09-initial-prd/capability-map.md`.

| Surface | What the audience sees | Minutes |
|---|---|---|
| Legacy API / baseline | Packaged counts on the current system | 0 to 8 |
| Architecture talk | Two apps, code-versus-model split | 8 to 13 |
| Application A | Scenarios 7 to 11, agent trace, approval gate | 13 to 25 |
| Application B | Same scenarios, then scenario 12 lineage | 25 to 32 |
| Scorecard | Scenario 13 matches and lake-traced differences | 32 to 36 |
| Security slot | Injection BLOCK. Restart mid-approval | 36 to 39 |

Replay mode (`MODEL_MODE=replay`) plays saved model responses. **Assumption.** That is the planned laptop mode until Phase 15 freezes FD-21.

---

## Finding

**Finding.** The locked system is a set of named listeners and stores: 8080, 8090, 8091, 8092, two FastAPI and React applications, one generated SQLite lake, one OPA gate, one LangGraph pause, and one correlation-id audit chain.
**Evidence.** `Execution_Plan.md` section 4. FD-06.
**Impact.** Phase 8 compose and later app folders must match these names and ports.
**Risk.** Inventing Application A and Application B host ports here would collide with Phase 8.
**Confidence.** High on the named components. Unknown on internal module layout.
**Open questions.** Checkpoint path. App host ports. Audit store file name. FD-07 item columns.

---

## What this file does not do

This file does not write code. It does not assign Application A or Application B ports. It does not invent the audit schema. It does not sign a Business Owner row.
