# Audit chain

| Field | Value |
|---|---|
| Stage | Phase 10 / 23 Human control and audit chain. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Names the FD-23 column list. Does not create the SQLite table. |
| Evidence sources | `docs/10-architecture/adrs/adr-audit-chain.md`; `docs/12-specs/event-contracts.md`; `apps/app_a/events.py`; `apps/app_a/routes/audit.py`; FD-23 DECIDED |
| Assumptions | Sprint 3 S05-14 practice holds: one correlation id joins the full trace. Envelope fields from ED-P6-04 stay. |
| Unresolved issues | Retention and redaction stay Phase 12 and Phase 13. Application B store layout stays Phase 11. |
| Residual risks | Logging only to stdout would mix cases. One summary row per case would hide the approval. Letting the model write the only audit paragraph would drop a step. |

This file names the audit table Half B must create. FD-23 is DECIDED. One audit row per agent step and one audit row per human approval. The key is the correlation id. A read by that id returns the full trace. Half B must not drop a step or an approval.

Engineering decision ED-P10A-07, authority: team-force. File path, table name, mint format, and column list below.

---

## Finding

**Finding.** Table `audit_chain` in `apps/app_a/audit/audit_chain.sqlite3` holds 27 named columns. `GET /api/audit/{correlation_id}` returns every row for that id ordered by `seq`.
**Evidence.** FD-23. Event envelope in `event-contracts.md`. Current in-memory writer in `events.py` already stores the envelope and says the column list stays Phase 10.
**Impact.** Half B can `CREATE TABLE` from this page without inventing a column.
**Risk.** An `extra` JSON blob as the only place for `step_name` would hide a step from a typed read.
**Confidence.** High
**Open questions.** Retention. Application B file path.

---

## Store

| Item | Value |
|---|---|
| File | `apps/app_a/audit/audit_chain.sqlite3` |
| Table | `audit_chain` |
| Writer | `apps/app_a/audit/writer.py` |
| Reader | `apps/app_a/audit/reader.py` |
| Schema helper | `apps/app_a/audit/store.py` |
| Mint | If `X-Correlation-Id` is present, use that string. Else `corr-app-a-` plus 12 hex digits. Keep `mint_correlation_id()` |
| `thread_id` | Same string as `correlation_id` |
| Read | `GET /api/audit/{correlation_id}`. Identity required. HTTP 200 with `rows` ordered by `seq`. HTTP 404 `not_found` when no rows |
| In-memory list | `apps/app_a/events.py` `_EVENTS` is replaced by this file in Half B. Tests may still reset the store |

---

## Column list

Half B creates these columns. Extra columns stay out until a later ADR.

| # | Column | SQLite type | Required | What it holds |
|---|---|---|---|---|
| 1 | `audit_id` | TEXT | yes | Primary key. UUID hex |
| 2 | `correlation_id` | TEXT | yes | Join key for the trace |
| 3 | `seq` | INTEGER | yes | 1-based order inside one correlation id |
| 4 | `row_kind` | TEXT | yes | `agent_step`, `human_approval`, or `control` |
| 5 | `event_type` | TEXT | yes | `EV-01` to `EV-12` |
| 6 | `occurred_at` | TEXT | yes | When the fact happened. ISO-8601 UTC |
| 7 | `recorded_at` | TEXT | yes | When this row was written. ISO-8601 UTC. Second clock |
| 8 | `actor_id` | TEXT | no | Person, `system`, or `model_draft` |
| 9 | `actor_role` | TEXT | no | `RT-01` to `RT-06`, `system`, or `model_draft` |
| 10 | `case_id` | TEXT | no | Case when one exists |
| 11 | `app` | TEXT | yes | `app_a` on this writer |
| 12 | `step_name` | TEXT | no | LangGraph node name |
| 13 | `tool_name` | TEXT | no | One of the six allow-listed names |
| 14 | `draft_present` | INTEGER | yes | 0 or 1 |
| 15 | `proposed_action` | TEXT | no | Graph `proposed_action` |
| 16 | `opa_verdict` | TEXT | no | `EXECUTE`, `HOLD_FOR_REVIEW`, `BLOCK`, or empty |
| 17 | `action_type` | TEXT | no | Approval `action_type` |
| 18 | `decision` | TEXT | no | Person `decision` |
| 19 | `proposed_by` | TEXT | no | Must differ from `actor_id` on a human_approval when both are people |
| 20 | `lake_item_ids` | TEXT | yes | JSON array of ids. Empty array allowed |
| 21 | `thread_id` | TEXT | no | LangGraph thread. Same as `correlation_id` on agent runs |
| 22 | `graph_name` | TEXT | no | `app_a_investigate` |
| 23 | `interrupt_id` | TEXT | no | LangGraph interrupt id when paused |
| 24 | `checkpoint_id` | TEXT | no | SqliteSaver checkpoint id |
| 25 | `error_class` | TEXT | no | EH class when one applies |
| 26 | `untrusted_quote_present` | INTEGER | yes | 0 or 1. Raw injection text stays out of this table as an instruction |
| 27 | `notes` | TEXT | no | Short application note. Not a model-written audit paragraph |

Constraints Half B must add:

- Primary key `audit_id`
- Unique `(correlation_id, seq)`
- Index on `correlation_id`
- `row_kind` in (`agent_step`, `human_approval`, `control`)
- `occurred_at` and `recorded_at` stay two columns

---

## When a row is written

| Moment | `row_kind` | `event_type` | Must exist |
|---|---|---|---|
| Each finished graph node that is `plan_draft`, `assemble_evidence`, or `ground_and_cite` | `agent_step` | EV-08 | yes |
| Each allow-listed tool return | `agent_step` | EV-08 | yes. `tool_name` set |
| `load_case` | `control` | EV-08 | yes |
| OPA returns a verdict | `control` | EV-07 | yes |
| Injection stop | `control` | EV-12 | yes when BLOCK |
| `interrupt()` pause | `control` | EV-08 | yes. `step_name=interrupt_wait` |
| `Command(resume=...)` | `control` | EV-08 | yes. Same step name, `notes=resumed` |
| Person approval | `human_approval` | EV-09 | yes. Do not drop |
| Owner assign | `human_approval` | EV-10 | yes when `assign_owner` |
| Replay candidate mark | `control` | EV-02 | when SP-07 loads |
| Recipe mismatch mark | `control` | EV-04 | when SP-08 loads |
| Two clocks shown | `control` | EV-05 | when SP-09 loads |
| Policy overlap mark | `control` | EV-06 | when SP-10 loads |
| Recovery probe | `control` | EV-11 | when SP-11 probes |

FD-23 requires every agent step and every human approval. The control rows keep the full trace a reader can follow. Half B may not skip an EV-08 tool row to save space.

Worked example. Scenario 8 happy path, counts Half B must meet or exceed:

1. load_case
2. plan_draft
3. get_case tool
4. get_item tool
5. assemble_evidence
6. ground_and_cite
7. opa_gate HOLD_FOR_REVIEW
8. interrupt pause
9. interrupt resume
10. human_approval RT-03

A read by that correlation id returns those rows in `seq` order. Honesty on the exact count: Unknown until Half B runs T-TRACE.

---

## Read body

`GET /api/audit/{correlation_id}` returns:

```text
{
  "ok": true,
  "correlation_id": "...",
  "rows": [ { every column above }, ... ]
}
```

The current `known_event_types` stub note is removed in Half B. The column list is this file.

Empty id or unknown id: HTTP 404, `error_class: not_found`.

---

## What stays out of a row

| Item | Why |
|---|---|
| Raw injection paragraph as `notes` | Quotes stay in the case `untrusted_quotes`. The audit row stores `untrusted_quote_present=1` |
| A model summary of the trace | The chain is one row per step written by the application |
| Live amount cutoff | No policy number in this table |
| Application B rows | Phase 11. Same column idea. Separate file later |

---

## What this file does not do

This file does not run `CREATE TABLE`. It does not start Half B. It does not set retention.
