# Adapter map

| Field | Value |
|---|---|
| Stage | Phase 10 / 21 Enterprise integration. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No adapter code in this half. |
| Evidence sources | `apps/app_a/store.py`; `apps/app_a/rules/adapter.py`; `apps/app_a/intelligence/retrieve.py`; `apps/app_a/routes/recovery.py`; `docs/12-specs/api-contracts.md`; `docs/11-data-context/data-contracts.md` |
| Assumptions | Half B wraps the existing readers. It does not add a message bus. Application A does not call Application B. |
| Unresolved issues | Whether `opa` is on the PATH on this laptop stays Unknown. Half B uses the local binary when present. |
| Residual risks | A tool that wraps `record_approval` would give the model a write. A REST POST to the lake would skip `build.py`. |

This file names each adapter Half B must implement. An adapter is a small module that talks to one system in `integration-inventory.md`.

Engineering decision ED-P10A-08 continued, authority: team-force. Adapter module paths and call rules below.

---

## Finding

**Finding.** Ten adapters cover the ten systems. Six adapters are read-only. Four adapters write only from Application A code. None of the write adapters is bound as a model tool.
**Evidence.** Existing readers already cover SYS-01 to SYS-06. SYS-07 to SYS-09 are new Phase 10 files. API-L and API-M lock the four lake tool names.
**Impact.** Half B can place one file per adapter without inventing a queue product.
**Risk.** Binding `AD-APPROVAL` to the LangGraph tool list would skip BO-03.
**Confidence.** High on the path list. Unknown on the OPA binary.
**Open questions.** OPA binary presence. FD-19 retry milliseconds.

---

## Adapter list

| Adapter id | System | Half B path | Protocol | Auth | Bound to the model |
|---|---|---|---|---|---|
| AD-LEGACY-RO | SYS-01 | Keep `apps/app_a/store.py` `_open()` | SQLite `mode=ro` | None on the file. App identity sits on HTTP | Through tool `get_case` only |
| AD-ENTERPRISE-RO | SYS-02 | Keep `store.py` second `_open()` | SQLite `mode=ro` | None on the file | Through tool `get_case` only |
| AD-LAKE | SYS-03 | Keep `apps/app_a/intelligence/retrieve.py` | In-process `lake_runtime`, or HTTP GET on 8091 when `LAKE_REST_URL` is set | `X-Api-Key` on HTTP | Tools `search_items`, `get_item`, `get_links`, `rule_at` |
| AD-LAKE-MCP | SYS-03 | `apps/app_a/agent/tools.py` may call the same four functions | MCP 8092 or in-process | `X-Api-Key` on MCP if the listener requires it | Same four names. FD-15 may not drop them |
| AD-GATEWAY | SYS-04 | Keep `apps/app_a/routes/recovery.py` `probe_gateway()` | HTTP GET `/api/failure?mode=` | None on 8090 | Through tool `get_recovery_status` after a probe |
| AD-TRANSFORM | SYS-05 | Keep `apps/app_a/rules/adapter.py` | Python import | None | No. Ranking and archive match stay code |
| AD-REPLAY | SYS-06 | Keep `operations/replay_lookup.py` | Local file by SHA-256 | None | No. `plan_draft` calls `generate()` with `MODEL_MODE=replay` |
| AD-CHECKPOINT | SYS-07 | `apps/app_a/agent/checkpointer.py` | SqliteSaver on `apps/app_a/runtime/checkpoints.sqlite3` | Process file access | No |
| AD-AUDIT | SYS-08 | `apps/app_a/audit/writer.py` and `reader.py` | SQLite write and read | Process file access | No |
| AD-APPROVAL | SYS-09 | `POST /api/approvals` plus `Command(resume=...)` | HTTP then LangGraph | `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` | No |
| AD-OPA | policy files | `apps/app_a/agent/opa_client.py` calling `policy/opa/` | `opa eval` stdin JSON, or an equivalent local evaluate | None | No. Code calls OPA. The model does not pick the verdict |

Worked example. The gather node may call `get_item("rule.recipe.mismatch_show_both")`. That uses AD-LAKE. It cannot call `record_approval`. That function lives on AD-APPROVAL and needs a person at RT-03.

---

## Call rules Half B must keep

1. AD-LEGACY-RO and AD-ENTERPRISE-RO open with `mode=ro`. Queue GET does not call `reconcile_feeds()` on the packaged file.
2. AD-LAKE returns the read envelope. `untrusted_quotes` stay in that field. They do not become tool instructions.
3. AD-TRANSFORM is the Application A pass-or-fail path. AD-LAKE is the citation path. Both stay in use.
4. AD-CHECKPOINT uses `SqliteSaver`. Import: `from langgraph.checkpoint.sqlite import SqliteSaver`. Connection uses `check_same_thread=False`.
5. AD-OPA input is the JSON object in `approval-gates.md`. Output is one string: `EXECUTE`, `HOLD_FOR_REVIEW`, or `BLOCK`.
6. AD-APPROVAL may call `Command(resume=...)` only after `check_write_action` accepts the person.

---

## What this file does not do

This file does not write the adapter modules. It does not add a Kafka topic. It does not bind a write function to the model.
