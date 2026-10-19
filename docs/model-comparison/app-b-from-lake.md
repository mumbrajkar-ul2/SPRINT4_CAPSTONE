# Application B from the lake

| Field | Value |
|---|---|
| Stage | Phase 11 / 20p Application B from the lake. Half B build. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p11b-doc-20261018-001 |
| Status | IMPLEMENTED. Application B reads the pin and the lake cards. Awaits reviewer. |
| Evidence sources | `docs/10-architecture/adrs/adr-app-b-reads-only-the-lake.md`; `docs/11-data-context/contract-gates.md` Gate 5; `context-lake/generated/app-b-pin.json`; `context-lake/generated/manifest.json`; `docs/12-specs/business-rules.md`; `docs/12-specs/api-contracts.md`; FD-06, FD-07, FD-13, FD-14; `apps/app_b/server.py` Phase 8 stub |
| Assumptions | Lake 1.0.0 and the pin hash hold. Compose already publishes 8110. `MODEL_MODE=replay`. BO-03, BO-06b, and BO-08 stay PROPOSED. |
| Unresolved issues | Company job titles stay Unknown. INC-2025-014 owner stays Unknown. Azure deployment name stays Unknown. Numeric percent floors stay Unknown. |
| Residual risks | Adding the inherited repo to Application B `PYTHONPATH` would hide a missing lake item. Importing `apps.app_a.rules` would make the comparison false. Compiling 50000 or 999999 as decided would sign a PROPOSED row. |

This file is the build note for Application B. Application B takes every pass, fail, or wait from the Context Lake. The Phase 8 stub on 8110 is now the full listener.

Engineering decisions ED-P11A-02, ED-P11A-03, ED-P11A-04, ED-P11A-06, and ED-P11A-08, authority: team-force.

---

## Finding — portability

**Finding.** Application B build inputs are the pinned lake file, the pin JSON, the lake schemas, and `apps/app_b/`. The inherited repo path stays out of Application B source and out of the Application B compose `PYTHONPATH`.
**Evidence.** FD-06. Gate 5. Current `compose.yaml` already omits `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` on `app-b`. Application A still has that path. Pin `lake_version` 1.0.0. `sqlite_sha256` `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Honesty: REAL.
**Impact.** Half B can grep `apps/app_b/` for `fabpulse-legacy-workshop` and expect zero hits.
**Risk.** Opening `legacy.sqlite3` for the 67 REPLAY rows would put that path back.
**Confidence.** High
**Open questions.** None for the pin hash. A later lake extract of 67 feed ids would need a version raise.

---

## Finding — rule resolution

**Finding.** Every Application B rule read is `get_item`, `get_links`, `search_items`, or `rule_at` against the pinned lake. Each result cites the item id it used.
**Evidence.** API-L-03 to API-L-06. Gate 5 canonical card list in `app-b-pin.json`. Business-rule cards BR-01 to BR-15.
**Impact.** Half B writes `apps/app_b/rules/resolver.py` as a lake client. It does not copy Application A adapter functions.
**Risk.** Hard-coding 18600 in Application B without a `get_item` call would invent a second archive.
**Confidence.** High
**Open questions.** None for the archive numbers.

---

## Pin Half B must load

**Verified Fact.** `context-lake/generated/app-b-pin.json`.

| Field | Value |
|---|---|
| `lake_version` | `1.0.0` |
| `sqlite_sha256` | `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` |
| `enum_sha256` | `3c2aa3ae047e8b4f3edc350aefd8e042d2787b92f7fc9cc5d2af13ef351f1ce3` |
| SQLite file | `context-lake/generated/context-lake.sqlite3` |
| Enum file | `context-lake/generated/enums.generated.json` |

Start fails when the opened file hash disagrees with the pin. Gate 5.

The pin lists 25 canonical rule-card ids. Half B must resolve each one from the lake. Half B must not add a 26th live card in code.

---

## Rule-resolution path

Engineering decision ED-P11A-02, authority: team-force.

1. Open the pinned SQLite file read-only, or call lake REST on 8091 with `X-Api-Key`.
2. Read `get_item(id)` for the card named in the table below.
3. Apply that card’s `decision_table` and `tests`.
4. Put the item id on the case `citations` list and on the audit `lake_item_ids` list.
5. If the card is missing, superseded without a current child, or silent, return `HOLD_FOR_REVIEW` and cite `rule.recipe_release.no_match` or `rule.threshold.silent` as the card states.
6. Run `check_claim` on every AI sentence. Empty citations on ANSWER become ABSTAIN. FD-14. No percent floor.

Lake REST paths Application B may call:

| Need | Call |
|---|---|
| One card | `GET /v1/items/{id}` |
| Edges | `GET /v1/items/{id}/links` |
| Search | `GET /v1/items?q=` |
| Dated limit | `GET /v1/rules/at?rule_id=&on_date=&site_code=` |
| Version check | `GET /v1/version` |

Write methods on the lake stay absent. MCP on 8092 exposes the same four read tools. The model may use those tools. The model has no write tool.

In-process `lake_runtime` against the pinned file is allowed when lake REST is down, so Application B can still run with Application A stopped. The opened file must still match the pin hash.

---

## Which lake item answers which job

Engineering decision ED-P11A-08, authority: team-force. Application B applies the card. It does not import `priority`, `evaluate_live_policy`, `intake_apply`, or `reconcile_feeds`.

| Job | Lake item ids | What Application B does |
|---|---|---|
| Replay mark | `rule.feed.replay_duplicate`, `data.feed.replay` | `processing_status=REPLAY` sets `duplicate_candidate=true`. Drop waits for RT-05 |
| Recipe pair | `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch` | Show `R02` and `R01`. Do not write `engineering_hold` |
| Two clocks | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence` | Keep `event_time` and `arrival_time`. A cut-off question waits |
| Policy overlap | `rule.policy.overlap_or_invalid`, `data.policy_register.overlap` | Name the five US ids. Wait for RT-04 |
| Owner empty | `decision.inc_2025_014`, `data.task.unassigned` | Leave `owner_id` empty until RT-06 |
| Open or closed | `rule.open_closed.operational` | REVIEW and HOLD are open |
| Finance and audit flags | `rule.open_closed.finance_audit` | Keep two extra flags. BO-06b stays PROPOSED |
| Queue order | `rule.urgent.severity.impl.python`, `rule.threshold.silent`, `rule.threshold.demo_50000` | CRITICAL is urgent as an observed implementation. Amount 50000 is display-only and labelled PROPOSED. Live silent cutoff waits |
| Archive limit | `rule.recipe_release.limit`, version children, `rule.recipe_release.no_match` | Call `rule_at`. 2023 EMEA 18600. 2026 APAC 25000. Honesty: REAL |
| Site map | `rule.region.site_canonical`, `rule.region.disagreement`, `map.site.IN-BLR` | Site is the key. IN-BLR plus stored AMER waits |
| Injection | `rule.untrusted_text.block`, `data.injection.partner_feeds` | `block=true`. No write |
| Person write | `rule.hold.person_only`, `term.approval` | Model draft waits. Proposer differs from approver |
| Forbidden default | `rule.threshold.never_999999` | Do not use 999999 |

Worked example. Queue ranking on Application B reads `rule.open_closed.operational` and `rule.urgent.severity.impl.python`. A CRITICAL case is urgent. An amount of 60000 with a silent archive routes `HOLD_FOR_REVIEW` from `rule.threshold.silent`. The screen may show 50000 labelled PROPOSED from `rule.threshold.demo_50000`. Application A may still apply the rebuilt Python 50000 branch. The harness traces that label or wait gap to those lake items.

---

## Scenario fixtures without the inherited store

Engineering decision ED-P11A-03, authority: team-force.

Application B does not open `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/data/legacy.sqlite3`. Half B writes `apps/app_b/fixtures/scenarios.yaml` from the lake data items and the published freeze ids.

| Pack | `case_id` | Fields Half B stores | Lake items that justify the fields |
|---|---|---|---|
| SP-07 | `REPLAY-000000000` | `processing_status=REPLAY`, `waiting_role=RT-05` | `rule.feed.replay_duplicate`, `data.feed.replay` |
| SP-08 | `PS000000016` | `recipe_version=R02`, `recipe_rev=R01`, lot `L00000016` | `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch` |
| SP-09 | `E-00000000` | `event_time=2020-12-30T00:00:00+00:00`, `arrival_time=2021-01-01T00:00:00+00:00` | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence` |
| SP-10 | `FAB-00000002` | US object. Policies POL-0002, POL-0010, POL-0018, POL-0026, POL-0034 | `rule.policy.overlap_or_invalid`, `data.policy_register.overlap` |
| SP-11 | `INC-2025-014` | `owner_id` empty. `waiting_role=RT-06` | `decision.inc_2025_014` |

`data.feed.replay` states 67 REPLAY rows. Honesty: REAL. Application B shows that integer as a cited count from the lake item. The worked case is `REPLAY-000000000`. Application B does not scan the packaged table for 67 ids. The harness matches on the integer 67 and on the worked-case mark.

`data.join.recipe_mismatch` states 91 of 125 steps mismatch. Honesty: REAL. Application B cites that count. The worked pair is R02 and R01.

---

## Process, ports, and independence

**Verified Fact.** FD-13. ED-P8A-01. Phase 8 stub `apps/app_b/server.py` already listens through `create_app("app-b")`.

| Piece | Bind | What it does |
|---|---|---|
| Application B | Host 8110 | `/api` and the React screens |
| Lake REST | Host 8091 | Rule cards, edges, `rule_at`, citations |
| Lake MCP | Host 8092 | The same four read tools for the agent |
| Source gateway | Host 8090 | Scenario 11 failure fixture |
| Application A | Host 8100 | Out of Application B’s call list |

Engineering decision ED-P11A-04, authority: team-force. Half B adds `LAKE_REST_URL` and a `depends_on` lake-rest health check to the `app-b` compose service. Half B does not add the inherited repo to `PYTHONPATH`. Half B does not add `depends_on` Application A.

Identity stays `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role`. Static UI GET paths stay open so the browser can load HTML and JavaScript. Every `/api` path except `/health` requires the three headers. Demo actors stay `demo-rt01-1` through `demo-rt06-1`.

`MODEL_MODE=replay`. Replay miss abstains. No Azure socket on the automated path. No write tool for the model.

---

## Half B module map

Engineering decision ED-P11A-04 continued. Paths are under the capstone root. Half B may split a file. It may not drop a row’s responsibility. It may not import `apps.app_a.rules`.

| Path | Responsibility |
|---|---|
| `apps/app_b/server.py` | FastAPI app. Keep health. Mount routes and static UI |
| `apps/shared/identity.py` | Existing header check. Reuse. Do not fork |
| `apps/app_b/routes/queue.py` | `GET /api/queue`. Rank from lake cards |
| `apps/app_b/routes/cases.py` | `GET /api/cases/{id}`. SCH-06 body |
| `apps/app_b/routes/query.py` | `POST /api/query`. Retrieve from the lake. FD-14 |
| `apps/app_b/routes/recovery.py` | `GET /api/recovery`. Gateway status |
| `apps/app_b/routes/approvals.py` | `POST /api/approvals`. Person only |
| `apps/app_b/routes/audit.py` | `GET /api/audit/{correlation_id}` |
| `apps/app_b/routes/lineage.py` | `GET /api/lineage/{item_id}` |
| `apps/app_b/routes/agent.py` | `POST /api/agent/run` when the graph is present |
| `apps/app_b/rules/resolver.py` | Lake client. Pin check. `decision_table` apply |
| `apps/app_b/fixtures/scenarios.yaml` | The five packs |
| `apps/app_b/intelligence/` | Replay generate, retrieve, ground. Cite or abstain |
| `apps/app_b/audit/` | Store, writer, reader. `app=app_b` |
| `apps/app_b/runtime/checkpoints.sqlite3` | Graph pause file if the agent graph is built |
| `apps/app_b/ui/` | Role picker, queue, case, query, recovery, approval, lineage |
| `policy/opa/app_b.rego` | Package `app_b`. Three verdicts. Each rule comments the lake item id it applies |

OPA on Application B encodes the lake cards for injection, person write, overlap, silence, and proposer-versus-approver. Half B writes that file from the cards. Half B does not copy `policy/opa/app_a.rego` as the rule source.

Prompts may reuse the Phase 9 registry ids `P-EXPLAIN-CONFLICT`, `P-NL-QUERY`, and `P-DRAFT-PLAN` at 1.0.0. Half B copies the JSON into `apps/app_b/prompts/`. That is a prompt file, not a rule function.

---

## HTTP routes Half B implements

| Route | Identity | Model | Person write |
|---|---|---|---|
| `GET /health` | No | No | No |
| `GET /` and `GET /assets/*` | No. Page must load | No | No |
| `GET /api/identity-check` | Yes | No | No |
| `GET /api/queue` | Yes | No | No |
| `GET /api/cases/{id}` | Yes | Optional cited sentence | No |
| `POST /api/query` | Yes | Yes. Cite or abstain | No |
| `GET /api/recovery` | Yes | Optional cited status | No |
| `POST /api/approvals` | Yes. Role must match | No | Yes |
| `GET /api/audit/{correlation_id}` | Yes | No | No |
| `GET /api/lineage/{item_id}` | Yes | No | No |
| `POST /api/agent/run` | Yes | Draft only | No |

---

## Gate 5 checks Half B must pass

| Check | Pass when |
|---|---|
| Pin hash | Opened SQLite matches `app-b-pin.json` |
| Enum names | Application B uses only names in `enums.generated.json` |
| No inherited import | No `legacy_logic.py`, `legacy_policy.js`, `ReconcileLegacy.java`, or `shift_reconciliation.py` |
| No inherited path | `rg` on `apps/app_b/` finds no `fabpulse-legacy-workshop` |
| No Application A rules import | `rg` finds no `apps.app_a.rules` |
| Card tests | 2023 EMEA 18000 is within 18600. 19000 is outside |
| 999999 | Absent as live policy |
| 50000 | Labelled PROPOSED. Live path waits |
| Three closures | Operational, finance, and audit stay three flags |
| Independence | Application B serves 8110 with Application A stopped |

---

## Half B implementation

Half B wrote the module map under `apps/app_b/`. The opened SQLite hash is `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Lake version is `1.0.0`. Honesty: REAL.

`GET /api/queue` returns `replay_candidate_count=67` from `data.feed.replay`. It also returns `amount_cutoff_label=proposed` from `rule.threshold.demo_50000`. Live silent cutoff stays `HOLD_FOR_REVIEW` from `rule.threshold.silent`. The code does not store 50000 or 999999 as signed live policy.

`compose.yaml` service `app-b` sets `LAKE_REST_URL=http://lake-rest:8091` and waits on lake-rest health. Application B `PYTHONPATH` stays `/opt/platform:/opt/platform/context-lake`. The inherited repo is not on that path. Application B does not depend on Application A.

A child process imported Application B, served the five scenario cases and lineage, and left Application A out of `sys.modules`. Honesty: REAL.

---

## What this file does not do

This file does not sign a Business Owner row. It does not start Phase 12.
