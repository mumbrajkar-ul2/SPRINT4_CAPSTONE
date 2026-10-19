# Integration inventory

| Field | Value |
|---|---|
| Stage | Phase 10 / 21 Enterprise integration. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No adapter code in this half. |
| Evidence sources | `docs/05-current-state/integration-landscape.md`; `docs/10-architecture/adrs/adr-ports-and-compose.md`; `docs/12-specs/api-contracts.md`; `apps/app_a/store.py`; `apps/app_a/rules/adapter.py`; `apps/app_a/routes/recovery.py`; `Execution_Plan.md` section 4 |
| Assumptions | Packaged SQLite files stay read-only in the demo. Approvals, checkpoints, and audit rows are the writable stores. `MODEL_MODE=replay` stays. |
| Unresolved issues | FD-19 retry count stays Unknown. Compose-up on this laptop stays Unknown until Half B runs it. INC-2025-014 owner stays Unknown. |
| Residual risks | Calling `reconcile()` on the packaged partner-feed store would change 67 REPLAY rows. Writing the packaged `legacy.sqlite3` would break the Phase 9 freeze hashes. |

This file names every system Application A talks to in Phase 10. It names what each system stores and whether the agent may write it.

Engineering decision ED-P10A-08, authority: team-force. The adapter ids and writable-store list below.

---

## Finding

**Finding.** Phase 10 uses ten systems. Six are read-only sources. Four are local writable files that Application A owns. The language model reaches none of the writable files.
**Evidence.** `store.py` opens `legacy.sqlite3` and `enterprise_legacy.sqlite3` with `mode=ro`. `adapter.py` imports transformed functions. Recovery probes port 8090. Lake citations use port 8091 or in-process `lake_runtime`. FD-15 names SqliteSaver. FD-23 names the audit chain.
**Impact.** Half B can write one adapter per row without inventing a ninth source.
**Risk.** Giving the model a tool that opens those files for write would skip FD-02.
**Confidence.** High on the packaged paths. Unknown on measured probe latency.
**Open questions.** FD-19 retry count. Named owner for INC-2025-014.

---

## Systems of record

| Id | System | Path or port | What it holds | Direction | Honesty |
|---|---|---|---|---|---|
| SYS-01 | Packaged fab store | `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/data/legacy.sqlite3` | Cases, partner feeds, process steps, tools, wafer lots | Read | REAL packaged rows |
| SYS-02 | Packaged enterprise store | `.../data/enterprise_legacy.sqlite3` | Evidence events, policy register, operational objects, workflow tasks, outages | Read | REAL packaged rows |
| SYS-03 | Context Lake | `context-lake/generated/context-lake.sqlite3` on ports 8091 and 8092 | Citations, edges, terms. Lake 1.0.0 | Read | REAL pin |
| SYS-04 | Source gateway | Host 8090 | Failure fixtures: timeout, schema, rate_limit | Read | SIMULATED probe body |
| SYS-05 | Transformed rule functions | `apps/app_a/rules/adapter.py` imports from the inherited tree | `priority`, `evaluate_live_policy`, `intake_apply`, `reconcile_feeds` | Read of functions. Write only in temp-store tests | REAL import path |
| SYS-06 | Model replay files | `operations/model-replay/` | Saved prompt hashes for `MODEL_MODE=replay` | Read | PRECOMPUTED fixtures |
| SYS-07 | LangGraph checkpoint | `apps/app_a/runtime/checkpoints.sqlite3` | Paused graph state for one `thread_id` | Write by SqliteSaver | SIMULATED until Half B measures a restart |
| SYS-08 | Audit chain | `apps/app_a/audit/audit_chain.sqlite3` | One row per agent step and per human approval | Write by Application A code | SIMULATED until Half B measures a trace |
| SYS-09 | Approval overlay | Checkpoint state plus audit rows | Waiting role, draft, recorded decisions | Write after a person acts | SIMULATED until Half B |
| SYS-10 | Legacy API | Host 8080 | Baseline GET cases | Unused by Application A agents | REAL baseline |

Worked example. Scenario 8 reads step `PS000000016` from SYS-01. Dispatch `recipe_version` is R02. Equipment `recipe_rev` is R01. Honesty: REAL. The model may name both values. SqliteSaver in SYS-07 stores the wait for RT-03. The packaged row stays unread-write.

---

## What the model may reach

**Verified Fact.** FD-02. FD-15.

The model may call the six read-only tools in `tool-permission-map.md`. Those tools read SYS-01, SYS-02, SYS-03, and SYS-04.

The model has no tool for SYS-07, SYS-08, or SYS-09. Code writes those files after a person records a decision, or after a graph node finishes.

---

## Demo numbers already counted

These counts sit in the packaged stores. Honesty: REAL.

| Fact | Count | Store |
|---|---|---|
| Partner feeds with `processing_status = 'REPLAY'` | 67 | SYS-01 |
| Process steps whose `recipe_version` differs from `recipe_rev` | 91 of 125 | SYS-01 |
| Evidence rows whose `event_time` differs from `arrival_time` | 11,985 of 12,500 | SYS-02 |
| Active US `policy_register` rows | 5 | SYS-02 |
| Partner feeds with auto-approve or disregard-validation notes | 86 | SYS-01 |
| Integration attempts that are not SUCCESS | 1,875 of 2,500 | SYS-02 |
| Upstream outages with empty `resolved` | 8 of 72 | SYS-02 |
| Workflow tasks with empty `assigned_to` | 695 | SYS-02 |

---

## What this file does not do

This file does not open a write connection to SYS-01 or SYS-02. It does not start Half B. It does not set a retry count.
