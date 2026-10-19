# Tool contracts

| Field | Value |
|---|---|
| Stage | Phase 10 / 22 Agentic engineering. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/11-data-context/data-contracts.md`; `docs/12-specs/api-contracts.md` API-L and API-M; `apps/app_a/intelligence/retrieve.py`; `apps/app_a/store.py`; `apps/app_a/routes/recovery.py` |
| Assumptions | Harvested and user text that arrive as tool arguments stay data. Code copies injection strings into `untrusted_quotes`. |
| Unresolved issues | Lake MCP identity on 8092 stays the existing key check. Default lake `limit` stays the retrieve default 20. |
| Residual risks | A tool that accepts a SQL string would read past the allow-list. A tool named `update_case` would skip FD-02. |

This file names the input and output of each tool the model may call. Write tools are absent.

Engineering decision ED-P10A-03, authority: team-force. The six tool signatures below. The four lake names stay. Two Application A read tools are added.

---

## Finding

**Finding.** Six read-only tools cover investigation. Four already exist as lake tools. Two read Application A state. No tool changes `cases.status`, `engineering_hold`, a feed status, or an owner.
**Evidence.** Data-contracts minimum lake tools. FD-15 may add tools and may not remove the four lake names. `WRITE_TOOLS` in `generate.py` is already an empty list.
**Impact.** Half B binds exactly these names in `apps/app_a/agent/tools.py`.
**Risk.** Adding a seventh write-shaped tool in Half B would skip this design.
**Confidence.** High
**Open questions.** None for the name list.

---

## Shared output rules

Lake tools return the SCH-05 read envelope. Required fields: `ok`, `lake_version`, `items`, `edges`, `citations`, `trust_summary`, `untrusted_quotes`, `verdict`, `block`.

Application A read tools return a JSON object with `ok`, `case` or `recovery`, `untrusted_quotes`, and `block`. They do not return a write handle.

`verdict` on lake tools is `ANSWER`, `ABSTAIN`, or `HOLD_FOR_REVIEW`. That string is a lookup result. It is not the OPA verdict.

---

## T-01 `search_items`

| Field | Value |
|---|---|
| System | SYS-03 lake |
| Input | `q` string. Optional `kind`. Optional `on_date`. Optional `limit` integer |
| Output | Read envelope. `items` are FTS5 hits |
| Empty | `verdict: ABSTAIN`. `items` empty |
| Write | None |

`kind` must be one of the seven item kinds. An eighth kind is rejected by the lake.

---

## T-02 `get_item`

| Field | Value |
|---|---|
| System | SYS-03 lake |
| Input | `id` string |
| Output | Read envelope with one item |
| Missing | Envelope `ok: false` and `verdict: ABSTAIN` |
| Write | None |

Worked example. `id=rule.recipe_release.limit.v2023.emea` returns limit 18,600 USD. Honesty: REAL.

---

## T-03 `get_links`

| Field | Value |
|---|---|
| System | SYS-03 lake |
| Input | `id` string. Optional `type` from the eight link types. Optional `depth` non-negative integer |
| Output | Read envelope with `items` and `edges` |
| Write | None |

Lake 1.0.0 holds 180 edges. Honesty: REAL. This design does not invent a maximum depth. Half B passes `depth=1` when the model omits it.

---

## T-04 `rule_at`

| Field | Value |
|---|---|
| System | SYS-03 lake |
| Input | `rule_id` required. `on_date` required. `site_code` required when the lookup is a location. Optional `country_code`. Optional `sales_region` |
| Output | Read envelope. One valid rule, or `verdict: HOLD_FOR_REVIEW` |
| No archive row | `HOLD_FOR_REVIEW`. Lake item `rule.recipe_release.no_match` |
| Site and stored region disagree | `HOLD_FOR_REVIEW`. Lake item `rule.region.disagreement` |
| Overlap | `HOLD_FOR_REVIEW`. Lake item `rule.policy.overlap_or_invalid` |
| Write | None |

Application A still takes pass-or-fail from `evaluate_live_policy`. This tool is the citation for the same question.

---

## T-05 `get_case`

| Field | Value |
|---|---|
| System | SYS-01 and SYS-02 through `store.get_case` |
| Input | `case_id` string |
| Output | `{ "ok": true, "case": SCH-06 body, "untrusted_quotes": [...], "block": false }` |
| Missing | `{ "ok": false, "error_class": "not_found" }` |
| Write | None. The function is a deepcopy plus overlay. It does not call `record_approval` |

Untrusted notes on a REPLAY feed stay in `untrusted_quotes`. They are not steps.

---

## T-06 `get_recovery_status`

| Field | Value |
|---|---|
| System | SYS-04 last probe in `recovery.py` |
| Input | none, or optional `mode` of `timeout`, `schema`, `rate_limit`, `normal` |
| Output | SCH-08 fields: `status_visible`, `error_class`, `owner_id` (empty until a person assigns), `retry_shown` |
| Write | None. A `mode` argument may run a probe. It does not assign an owner |

INC-2025-014 `owner_id` stays empty until RT-06 supplies a name.

---

## Tools that do not exist

| Name someone might add | Why it stays out |
|---|---|
| `update_case` | Record write |
| `set_engineering_hold` | Record write |
| `drop_feed` | Record write |
| `assign_owner` | Record write |
| `pick_policy` | Record write |
| `post_approval` | Person HTTP route, not a tool |
| `opa_decide` | Code calls OPA |
| `run_sql` | Would read past the allow-list |

---

## What this file does not do

This file does not implement the six functions. It does not add a seventh tool.
