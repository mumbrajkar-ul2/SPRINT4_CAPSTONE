# Application B lineage view

| Field | Value |
|---|---|
| Stage | Phase 11 / 20p Application B from the lake. Half B build. |
| Date / version | 2026-10-18, v1.2 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p11b-doc-20261018-001 |
| Status | IMPLEMENTED. Lineage route and screen are live on 8110. Awaits reviewer. |
| Evidence sources | `docs/12-specs/api-contracts.md` API-Q-08; `docs/12-specs/acceptance-criteria.md` AC-S12; `docs/23-human-control/audit-chain.md`; `docs/22-agentic-engineering/agent-test-results.md`; `context-lake/items/decisions/decision.bp4.four_programs.yaml`; `context-lake/items/code/test.rule.recipe_release.emea_2023.yaml`; FD-23; FD-06 |
| Assumptions | Lake 1.0.0 holds 180 edges. Honesty: REAL. Application B reads those edges from lake REST or from the pinned SQLite file. Application B does not call Application A. |
| Unresolved issues | Later Application B correlation ids after this process stay Unknown. Retention and redaction stay Phase 12 and Phase 13. Company job titles stay Unknown. |
| Residual risks | Fetching `/api/audit` on port 8100 would make lineage depend on Application A. Writing a case from the lineage view would break AC-S12. |

This file names the Application B lineage view. Scenario 12 uses this view. The view shows one rule, the four local programs as deviations, a test, and the correlation id from the Phase 10 audit chain. Half B wrote the route and the screen.

Engineering decision ED-P11A-05, authority: team-force. The payload fields, the worked item, and the Phase 10 id below.

---

## Finding

**Finding.** `GET /api/lineage/{item_id}` on port 8110 returns the rule item, its `implements` and `tested_by` edges, the four local programs as deviations, and `phase10_correlation_id=corr-p10b-doc-20261018-001`.
**Evidence.** API-Q-08. AC-S12. T-TRACE in `agent-test-results.md`. That read returned 12 rows, `seq` 1 to 12, same id `corr-p10b-doc-20261018-001`. Honesty: REAL.
**Impact.** Half B can build the route and the screen from this page. A speaker can open the view with Application A stopped and still see the Phase 10 join key.
**Risk.** Calling Application A for the 12 rows would fail the independence check.
**Confidence.** High on the Phase 10 id and the 12-row order. Unknown on Application B’s own later correlation ids.
**Open questions.** Whether Half B also shows `corr-p10b-kill-20261018-001` as a second documented chain on the same case.

---

## Route

**Verified Fact.** API-Q-08. Host port is now 8110 (FD-13).

| Field | Value |
|---|---|
| Method and path | `GET /api/lineage/{item_id}` |
| App | Application B only |
| Identity | Required. `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` |
| Writes | None. The view does not change a case |
| Missing item | HTTP 404. `error_class: not_found`. `verdict: ABSTAIN` |
| Lake reads | `GET /v1/items/{id}` and `GET /v1/items/{id}/links` on port 8091, or the same calls through `lake_runtime` against the pinned file |

Application A evaluates the same archive rule from transformed code. Application A has no lineage route. The harness records that gap as `view_absent` and cites `decision.fd06.two_apps`.

---

## Worked item

**Verified Fact.** Archive 2023 EMEA limit is 18,600 USD. Honesty: REAL. Golden question GQ-01. Test item `test.rule.recipe_release.emea_2023`.

| Field | Value |
|---|---|
| Default item | `rule.recipe_release.limit.v2023.emea` |
| Parent card | `rule.recipe_release.limit` |
| Test | `test.rule.recipe_release.emea_2023`. Amount 18000, region EMEA, date 2023-07-01, within 18600 |
| Four deviations | Python priority, JavaScript allow, Java totals, night batch |
| Decision item | `decision.bp4.four_programs` |
| Canonical archive | `decision.fd08.canonical_archive` |

The four deviation lake items Half B must show:

| Program | Lake item | What the view says |
|---|---|---|
| Python priority | `code.legacy_logic.priority`, `rule.urgent.amount.impl.python` | Observed ranking from legacy Python. Demo may show 50000 labelled proposed per rule.threshold.demo_50000. Live silent amount cutoff waits per rule.threshold.silent (HOLD_FOR_REVIEW). |
| JavaScript allow | `code.legacy_policy.js_allow`, `rule.recipe_release.limit.impl.js`, `rule.recipe_release.limit.impl.js_default` | Observed 1.05 and 999999. Those numbers are deviations |
| Java totals | `code.reconcile_legacy.java_total`, `rule.month_end.float.impl.java` | Observed float total. Canonical money type stays Unknown |
| Night batch | `code.shift_reconciliation.night_batch`, `rule.open_flag.impl.night_batch`, `rule.night_batch.join_multiply` | Observed open-flag and join multiply |

The view does not copy those programs into Application B as live rules. The archive card stays the pass-or-fail source.

---

## Lineage payload (SCH-10)

Engineering decision ED-P11A-05 continued. Phase 6 named the lineage read and left the body to this phase. Extra properties stay out.

| Field | Required | What it holds |
|---|---|---|
| `ok` | yes | true on a found item |
| `item_id` | yes | The requested id |
| `item` | yes | The accepted lake item |
| `edges` | yes | `implements`, `tested_by`, `evidenced_by`, `conflicts_with`, `governs`, `depends_on`, `maps_to`, `supersedes` from the walk |
| `citations` | yes | Lake item ids used on this page |
| `lake_version` | yes | Pin version. Current `1.0.0` |
| `pin_sqlite_sha256` | yes | Pin hash |
| `phase10_correlation_id` | yes | `corr-p10b-doc-20261018-001` |
| `phase10_kill_correlation_id` | no | `corr-p10b-kill-20261018-001` when the screen shows the kill-restart chain |
| `phase10_row_count` | yes | 12. Honesty: REAL |
| `phase10_trace_summary` | yes | The 12-step list below, copied from the published Phase 10 result |
| `app_b_correlation_id` | no | Application B mint when this process ran the same case |
| `app` | yes | `app_b` |
| `verdict` | yes | `ANSWER` when the item exists. `ABSTAIN` when it does not |

The view does not fetch port 8100. The 12-step list is the published T-TRACE order. Honesty: REAL.

---

## Phase 10 audit chain the view must show

**Verified Fact.** `GET /api/audit/corr-p10b-doc-20261018-001` on Application A returned these 12 rows. Honesty: REAL.

| `seq` | `row_kind` | `event_type` | `step_name` | Note |
|---|---|---|---|---|
| 1 | control | EV-08 | `load_case` | Case `PS000000016` |
| 2 | control | EV-04 | `load_case` | Recipe mismatch mark |
| 3 | agent_step | EV-08 | `plan_draft` | Model draft. No write |
| 4 | agent_step | EV-08 | `gather_tools` | Tool `get_case` |
| 5 | agent_step | EV-08 | `gather_tools` | Tool `get_item` |
| 6 | agent_step | EV-08 | `assemble_evidence` | |
| 7 | agent_step | EV-08 | `ground_and_cite` | FD-14 |
| 8 | control | EV-07 | `opa_gate` | HOLD_FOR_REVIEW |
| 9 | control | EV-08 | `interrupt_wait` | notes `paused` |
| 10 | control | EV-08 | `interrupt_wait` | notes `resumed` |
| 11 | human_approval | EV-09 | `apply_human_decision` | RT-03 recorded hold |
| 12 | control | EV-08 | `write_audit` | |

The screen prints `corr-p10b-doc-20261018-001` as its own line. A reader must see that string without opening Application A.

A second documented id exists for the same case after the coordinator kill: `corr-p10b-kill-20261018-001`. After `taskkill` of pid 29320 and a new process, that id stayed on `PS000000016`. `engineering_hold` stayed 0 because nobody resumed. Honesty: REAL. The lineage screen may show that id as the kill-restart chain. It is optional. The required id is `corr-p10b-doc-20261018-001`.

---

## Screen

Half B builds one React view served from the same FastAPI process on 8110.

| Region | What the user sees |
|---|---|
| Rule | Item id, statement, authority, `policy_status`, archive limit when present |
| Edges | Each edge type and the target id |
| Deviations | The four programs named as deviations |
| Test | `test.rule.recipe_release.emea_2023` and the 18600 USD expect |
| Phase 10 chain | The string `corr-p10b-doc-20261018-001` and the 12-step list |
| Application B chain | `app_b_correlation_id` when this process wrote rows |

Worked example. The speaker opens `http://127.0.0.1:8110`, picks `demo-rt01-1` / RT-01, and opens lineage for `rule.recipe_release.limit.v2023.emea`. The page shows 18,600 USD, the test, the four deviations, and `corr-p10b-doc-20261018-001`. Application A can stay stopped.

---

## Application B audit store

`docs/23-human-control/audit-chain.md` left the Application B file path to this phase.

Engineering decision ED-P11A-06, authority: team-force.

| Item | Value |
|---|---|
| File | `apps/app_b/audit/audit_chain.sqlite3` |
| Table | `audit_chain` |
| Columns | The same 27 columns named in the Phase 10 audit design |
| `app` | `app_b` |
| Mint | If `X-Correlation-Id` is present, use that string. Else `corr-app-b-` plus 12 hex digits |
| Read | `GET /api/audit/{correlation_id}` on 8110. Identity required |

Lineage uses the published Phase 10 id for Scenario 12. Application B writes its own rows for new runs. Those rows do not replace the Phase 10 id on the lineage page.

---

## Half B implementation

`GET /api/lineage/{item_id}` is mounted on Application B. The worked item is `rule.recipe_release.limit.v2023.emea`. The body prints `phase10_correlation_id=corr-p10b-doc-20261018-001` and the 12-step list. Honesty: REAL.

The view reads the pinned lake. It does not call Application A. The screen is served from `apps/app_b/ui/` on port 8110. Application B audit rows go to `apps/app_b/audit/audit_chain.sqlite3` with `app=app_b`.

---

## What this file does not do

This file does not copy Application A audit rows at run time. It does not invent a signer. It does not start Phase 12.
