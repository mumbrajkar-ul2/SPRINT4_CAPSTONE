# API contracts

| Field | Value |
|---|---|
| Stage | Phase 6 / 12 Spec-driven design |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. FD-11 recommended. No API is added beyond the initial PRD and the locked listeners. |
| Evidence sources | `docs/09-initial-prd/functional-requirements.md`; `docs/05-current-state/system-landscape.md`; `docs/11-data-context/data-contracts.md`; `docs/10-architecture/adrs/adr-ports-and-compose.md`; lake items listed per route. Confirmed in `context-lake.sqlite3` on 2026-10-18. |
| Assumptions | Lake read envelope fields in `read-envelope.schema.json` stay required. Phase 6 adds optional pagination on list reads. It does not remove envelope fields. Application A and Application B host ports stay Unknown. |
| Unresolved issues | Identity token or header format stays Unknown (FD-13, FD-18). Default page size stays Unknown. Audit column list stays Unknown (FD-23). Recursion-limit number stays Unknown (FD-15). |
| Residual risks | A POST that writes lake items would skip the YAML-to-SQLite build. A comparison HTTP API would add a surface the PRD does not name. Copying the 8080 no-identity behaviour onto Application A would leave BP8 open. |

This file names every HTTP and MCP contract this product uses. Each route traces to a PRD workflow or to a locked listener. Write methods on the lake are absent.

Engineering decision ED-P6-01, authority: team-force. Lake REST paths on port 8091 map the four lake tools already named in `docs/11-data-context/data-contracts.md`.

Engineering decision ED-P6-02, authority: team-force. Application A and Application B share one operational resource list. Application B adds the lineage read. Host ports stay Unknown.

Engineering decision ED-P6-03, authority: team-force. Person writes use one approval resource. Action type selects the Group C row.

---

## Finding

**Finding.** Four listener families cover the PRD: the inherited legacy GET API on 8080, the inherited source gateway on 8090, the lake read API on 8091 and 8092, and the Application A / Application B operational API whose host ports are Unknown.
**Evidence.** `arch.listener.legacy_8080`, `arch.listener.gateway_8090`, `arch.listener.lake_rest_8091`, `arch.listener.lake_mcp_8092`, `decision.fd06.two_apps`. `docs/05-current-state/system-landscape.md`.
**Impact.** Later build phases implement these paths. They do not add a ninth-problem API.
**Risk.** Inventing a user-admin API, a billing API, or a compare-apps HTTP API would grow past BO-04.
**Confidence.** High on the four families. Unknown on Application A and Application B host ports and on identity format.
**Open questions.** Host ports. Identity format. Default page size.

---

## Shared rules for every new application route

These rules bind Application A and Application B. They do not rewrite the inherited 8080 baseline.

| Rule | Statement | Label | Lake item |
|---|---|---|---|
| Identity | Every case read and every record-changing write carries an actor identity | Verified Fact that 8080 is missing it. Mechanism later | `decision.bp8.auth_and_owner` |
| Correlation id | Every agent step and every approval is keyed by a correlation id | Locked idea. Minting later (FD-23) | `decision.fd06.two_apps` |
| Model writes | The model has no write route | Verified Fact of FD-02 and BO-03 working answer | `rule.hold.person_only` |
| Untrusted text | Approve-or-ignore strings travel in a flagged quotes list. They do not sit in an instruction field | Verified Fact | `rule.untrusted_text.block` |
| App independence | Application A does not call Application B. Application B does not call Application A | Verified Fact | `decision.fd06.two_apps` |
| Rule source | Application A evaluates pass or fail from transformed code. Application B evaluates pass or fail from the lake | Verified Fact | `decision.fd06.two_apps` |

Missing identity on Application A or Application B is an error. See `error-handling-spec.md`. The identity format (header name, token, cookie) stays Unknown until FD-13.

---

## API-L — Lake REST on port 8091

**Verified Fact.** `arch.listener.lake_rest_8091`. `docs/11-data-context/data-contracts.md`. Schema `context-lake/schemas/read-envelope.schema.json`.

All lake REST methods are GET. A POST, PUT, PATCH, or DELETE that would change `items` fails the read-time gate.

Every successful body uses the read envelope. Required fields: `ok`, `lake_version`, `items`, `edges`, `citations`, `trust_summary`, `untrusted_quotes`, `verdict`, `block`. Extra properties are rejected.

`verdict` is `ANSWER`, `ABSTAIN`, or `HOLD_FOR_REVIEW`. `block` is true when the injection path must stop an action.

Optional pagination, added in this unit: query fields `limit` and `offset`. Both are integers. If they are omitted, the server returns the ranked accepted hits. The maximum `limit` number is Unknown. This spec does not invent a default page size.

`lake_version` matches the generated manifest. Lake 1.0.0 is the current pin. Lake item `decision.fd22.lake_version_policy`.

### API-L-01 Health

| Field | Value |
|---|---|
| Method and path | `GET /health` |
| Port | 8091 |
| PRD justification | Operability of the laptop demo. Compose must show the listener is up |
| Lake item | `arch.listener.lake_rest_8091` |
| Request body | none |
| Success | `200`. Body includes `{ "ok": true }` |
| Identity | Not required on health |

### API-L-02 Version

| Field | Value |
|---|---|
| Method and path | `GET /v1/version` |
| Port | 8091 |
| PRD justification | Application B pins the lake file. Scenario 13 traces a miss to a lake version |
| Lake item | `decision.fd22.lake_version_policy`, `arch.lake.yaml_sqlite` |
| Success | `200`. Body includes `lake_version` and `sqlite_sha256` from `generated/manifest.json` |

Worked example. Manifest recorded `lake_version` 1.0.0 and `item_count` 148. Honesty: REAL.

### API-L-03 Search items (`search_items`)

| Field | Value |
|---|---|
| Method and path | `GET /v1/items` |
| Port | 8091 |
| Query | `q` (string), optional `kind`, optional `on_date`, optional `limit`, optional `offset` |
| PRD justification | FR-11 cited natural-language answer. FR-10 cited conflict explanation. FR-15 lineage |
| Lake item | `arch.lake.yaml_sqlite` |
| Success | `200` envelope. `items` are FTS5 hits. FTS5 is the SQLite word-search index over item text |
| Empty | `verdict: ABSTAIN`. `items` empty |

`kind` must be one of the seven values in the item schema. An eighth kind is rejected.

### API-L-04 Get item (`get_item`)

| Field | Value |
|---|---|
| Method and path | `GET /v1/items/{id}` |
| Port | 8091 |
| PRD justification | FR-04, FR-15. Application B reads one rule item |
| Lake item | `arch.lake.yaml_sqlite` |
| Success | `200` envelope with one item |
| Missing id | `404` envelope. `ok: false`. `verdict: ABSTAIN` |

Worked example. `GET /v1/items/rule.recipe_release.limit.v2023.emea` returns the 2023 EMEA limit 18,600 USD. Honesty: REAL. Golden question GQ-01.

### API-L-05 Get links (`get_links`)

| Field | Value |
|---|---|
| Method and path | `GET /v1/items/{id}/links` |
| Port | 8091 |
| Query | optional `type`, optional `depth` |
| PRD justification | FR-15 rule lineage. Scenario 12 |
| Lake item | `arch.graph.edges_table` |
| Success | `200` envelope with `items` plus `edges` from the recursive SQL walk |

`type` must be one of the eight link types: `conflicts_with`, `depends_on`, `evidenced_by`, `governs`, `implements`, `maps_to`, `supersedes`, `tested_by`. Lake 1.0.0 holds 180 edges. Honesty: REAL.

`depth` is a non-negative integer. The maximum depth number is Unknown. This spec does not invent it.

### API-L-06 Rule at (`rule_at`)

| Field | Value |
|---|---|
| Method and path | `GET /v1/rules/at` |
| Port | 8091 |
| Query | `rule_id` (required), `on_date` (required), `site_code` (canonical, required when the lookup is a location). Optional `country_code`. Optional `sales_region` |
| PRD justification | FR-04, FR-06. Application B pass-or-fail |
| Lake item | `rule.recipe_release.limit`, `rule.region.site_canonical`, `rule.region.disagreement`, `rule.recipe_release.no_match` |
| Success | `200` envelope with the valid rule row. `verdict: ANSWER` |
| No archive row | `verdict: HOLD_FOR_REVIEW`. Lake item `rule.recipe_release.no_match` |
| Site and stored region disagree | `verdict: HOLD_FOR_REVIEW`. Lake item `rule.region.disagreement` |
| Overlap | `verdict: HOLD_FOR_REVIEW`. Lake item `rule.policy.overlap_or_invalid` |

Worked example. `rule_id=rule.recipe_release.limit`, `on_date=2023-07-01`, `sales_region=EMEA` returns limit 18,600 USD. Honesty: REAL.

Worked example. Site `IN-BLR` with stored sales region `AMER` on 2026-06-01 returns `HOLD_FOR_REVIEW`. 84 of 125 packaged cases have this shape of disagreement. Honesty: REAL.

---

## API-M — Lake MCP on port 8092

**Verified Fact.** `arch.listener.lake_mcp_8092`. Four tool names already locked in `data-contracts.md`. FD-15 may add more later. It may not remove these four.

| Tool | Maps to REST | Input | Output |
|---|---|---|---|
| `search_items` | API-L-03 | query string, optional `kind`, optional date | read envelope |
| `get_item` | API-L-04 | `id` | read envelope |
| `get_links` | API-L-05 | `id`, optional `type`, optional depth | read envelope |
| `rule_at` | API-L-06 | `rule_id`, `on_date`, `site_code`, optional country, optional sales region | read envelope |

Write tools are absent. A tool that would change `cases.status`, `engineering_hold`, a feed status, or an owner is rejected by FD-02.

---

## API-G — Source gateway on port 8090 (inherited)

**Verified Fact.** `arch.listener.gateway_8090`. `docs/05-current-state/system-landscape.md`.

These routes already exist. This spec records them. It does not add a new gateway route.

| Path | What it returns | PRD link |
|---|---|---|
| `GET /health` | Listener up | W5, S11 |
| `GET /api/catalog` | Simulated upstream catalog | W1 |
| `GET /api/events` | Events with `occurred_at` and `published_at` | FR-03, S9 |
| `GET /api/record/{id}` | One source record | W1 |
| `GET /api/failure` | Modes `timeout`, `schema`, `rate_limit` | FR-08, S11 |

The file has no authentication code today. Identity on the gateway stays later (FD-13). Scenario 11 uses the failure modes as the outage and schema-mismatch fixture.

Worked example. A metrology event keeps `occurred_at` as event time and `published_at` as arrival time. The two clocks stay two fields. Lake item `rule.clock.event_vs_arrival`.

---

## API-8080 — Legacy API on port 8080 (baseline)

**Verified Fact.** `arch.listener.legacy_8080`. `docs/05-current-state/system-landscape.md`.

These routes already exist. They stay the 0-to-8-minute baseline. Application A does not replace this port.

| Path | What it returns today |
|---|---|
| `GET /health` | Listener up |
| `GET /` | Root |
| `GET /api/cases` | Case list |
| `GET /api/cases/{id}` | One case |
| `GET /api/metrics` | Metrics |
| `GET /api/incidents` | Incidents. Body contains INC-2019-0082. It does not contain an owner for INC-2025-014 |
| `GET /api/partners/{table}` | Partner table |
| `GET /api/domain/{table}` | Domain table |

**Verified Fact.** The handler does not check identity. Characterization check CT-35 records `GET /api/cases` without an identity header as HTTP 200 on the current server. That record is current behaviour. It is not an approval of open access on Application A or Application B.

This spec does not add a new 8080 route.

---

## API-A / API-B — Application operational API

Host ports: Unknown. Phase 8 assigns them. Base path in this spec is `/api` on each application's own listener.

Application A and Application B expose the same routes unless a row says Application B only.

No compare-apps HTTP API. Scenario 13 is a test harness (FD-17 later). FR-14 does not name a product URL for that harness.

### API-Q-01 Health

| Field | Value |
|---|---|
| Method and path | `GET /health` |
| Apps | Application A and Application B |
| PRD justification | Laptop demo operability |
| Lake item | `decision.fd06.two_apps` |
| Success | `200` `{ "ok": true }` |

### API-Q-02 Queue

| Field | Value |
|---|---|
| Method and path | `GET /api/queue` |
| Apps | Application A and Application B |
| PRD justification | W2. FR-09. FR-05 |
| Lake item | `code.legacy_logic.priority`, `rule.open_closed.operational`, `term.open_operational` |
| Identity | Required |
| Success | `200`. Ordered case summaries. Order uses status, severity, and amount. It does not call a model. It does not read untrusted note text to rank |

Each summary includes: case id, operational open or closed, status word, severity, amount, and a next-action hint that names the waiting RT role when the case is waiting.

REVIEW and HOLD count as open. Finance-closed and audit-closed stay separate labels. Lake item `rule.open_closed.finance_audit`. BO-06b stays PROPOSED.

Worked example. `priority('OPEN', 'CRITICAL', 1)` returns urgent. Two packaged cases are urgent because severity is CRITICAL. Zero packaged cases have `amount > 50000`. Honesty: REAL.

### API-Q-03 Case

| Field | Value |
|---|---|
| Method and path | `GET /api/cases/{id}` |
| Apps | Application A and Application B |
| PRD justification | W3. FR-01, FR-03, FR-06, FR-07, FR-08, FR-10, FR-12 |
| Lake item | `term.case`, `rule.recipe.mismatch_show_both`, `rule.clock.event_vs_arrival`, `rule.policy.overlap_or_invalid`, `rule.untrusted_text.block` |
| Identity | Required |
| Success | `200`. One case. Both disagreeing values are present when the case is a conflict. Event time and arrival time are two fields. Untrusted quotes are a flagged list. A draft plan, if one exists, sits on this resource. The draft does not change the record |

Required case fields for the conflict types:

| Conflict | Fields the body must show | Lake item |
|---|---|---|
| Recipe mismatch | `recipe_version` (dispatch) and `recipe_rev` (equipment). Both. No winner picked | `rule.recipe.mismatch_show_both` |
| Late result | `event_time` and `arrival_time` | `rule.clock.event_vs_arrival` |
| Policy overlap | The overlapping policy ids and the wait | `rule.policy.overlap_or_invalid` |
| Replay | `processing_status` and duplicate-candidate mark | `rule.feed.replay_duplicate` |
| Injection text | `untrusted_quotes` list. Case does not close from that text | `rule.untrusted_text.block` |
| Missing owner | Owner field may be empty. Body must not invent a name | `decision.inc_2025_014` |

OPA verdict on the case, when a gate has run, is one of EXECUTE, HOLD_FOR_REVIEW, or BLOCK. OPA is Open Policy Agent. It loads a policy file and returns that verdict. Rule bodies stay later (FD-16).

### API-Q-04 Approval (person write)

| Field | Value |
|---|---|
| Method and path | `POST /api/approvals` |
| Apps | Application A and Application B |
| PRD justification | W4. FR-13. Group C rows RT-01 to RT-06 |
| Lake item | `term.approval`, `rule.hold.person_only`, `rule.feed.replay_duplicate`, `rule.recipe.mismatch_show_both`, `rule.policy.overlap_or_invalid`, `decision.inc_2025_014` |
| Identity | Required. Actor must match the RT role for the action type |
| Separation | `actor_id` must differ from `proposed_by`. BO-09 |

Request body fields:

| Field | What it holds |
|---|---|
| `case_id` | The case |
| `action_type` | One of `dispose`, `approve_agent`, `recipe_hold_or_release`, `policy_pick`, `replay_confirm`, `assign_owner` |
| `decision` | One of `approve`, `hold`, `block`, `drop_duplicate`, `keep_duplicate`, `keep_wait`, `assign` |
| `actor_role` | `RT-01` to `RT-06` |
| `actor_id` | The person. Format Unknown until FD-13 |
| `proposed_by` | The proposer. Must differ from `actor_id` |
| `correlation_id` | Joins the audit rows. Minting later (FD-23) |
| `owner_id` | Required when `action_type` is `assign_owner`. Must not be invented for INC-2025-014 until a person supplies it |
| `policy_id` | Required when `action_type` is `policy_pick` and `decision` is not `keep_wait` |
| `hold_value` | Required when `action_type` is `recipe_hold_or_release` |

The model cannot call this route. A request with no actor identity is rejected. A request whose actor is the proposer is rejected. A request whose role does not match the action type is rejected. See `business-rules.md` and `error-handling-spec.md`.

Worked example. Recipe mismatch on step R02 and tool R01. `action_type` is `recipe_hold_or_release`. `actor_role` is `RT-03`. The Process Engineer records hold or release. The model draft is not the write.

### API-Q-05 Recovery status

| Field | Value |
|---|---|
| Method and path | `GET /api/recovery` |
| Apps | Application A and Application B |
| PRD justification | W5. FR-08. Scenario 11 |
| Lake item | `term.outage`, `decision.bp8.auth_and_owner`, `arch.listener.gateway_8090` |
| Identity | Required |
| Success | `200`. Retry state, last error class (`timeout`, `schema`, `rate_limit`, or none), and whether a follow-up owner is recorded |

The numeric recovery-time target stays Unknown. This route shows status. It does not claim an 8-hour recovery.

### API-Q-06 Cited query

| Field | Value |
|---|---|
| Method and path | `POST /api/query` |
| Apps | Application A and Application B |
| PRD justification | FR-10, FR-11 |
| Lake item | `arch.lake.yaml_sqlite`, `rule.untrusted_text.block` |
| Identity | Required |
| Request | `{ "question": "...", "case_id": optional }` |
| Success | `200`. A sentence, a citations list of lake item ids or stored-row locators, and a verdict `ANSWER`, `ABSTAIN`, or `HOLD_FOR_REVIEW` |
| Injection | If the question or retrieved text is an injection locator and the implied action is approve, release, ignore-validation, or close-from-text, `block` is true and no write is offered |

If retrieval returns nothing, the model abstains. Percent floors stay Unknown (FD-14, FD-18).

Application A may retrieve lake items for citations. Application A still takes pass-or-fail from transformed code. Application B retrieves lake items and takes pass-or-fail from those items.

### API-Q-07 Audit trace

| Field | Value |
|---|---|
| Method and path | `GET /api/audit/{correlation_id}` |
| Apps | Application A and Application B |
| PRD justification | NFR audit later. Locked audit-chain idea. Scenario 12 lineage shows the id |
| Lake item | `decision.fd06.two_apps` |
| Identity | Required |
| Success | `200`. The full list of agent-step rows and human-approval rows for that id, in order |

Column names stay Unknown (FD-23). This spec names the read. It does not invent the column list.

### API-Q-08 Lineage (Application B only)

| Field | Value |
|---|---|
| Method and path | `GET /api/lineage/{item_id}` |
| Apps | Application B required. Application A evaluates the same rule without this view |
| PRD justification | W6. FR-15. Scenario 12 |
| Lake item | `arch.graph.edges_table`, `decision.bp4.four_programs`, `decision.fd08.canonical_archive`, `test.rule.recipe_release.emea_2023` |
| Identity | Required |
| Success | `200`. The rule item, its `implements` and `tested_by` edges, the four local programs as deviations, and the correlation id when one exists |
| Writes | This view does not write a case |

Worked example. Item `rule.recipe_release.limit.v2023.emea` traces to archive 18,600 USD, to `code.legacy_policy.js_allow` as a deviation, and to `test.rule.recipe_release.emea_2023`. Honesty on 18,600: REAL.

---

## Routes this file does not add

| Omitted surface | Why |
|---|---|
| Compare-apps HTTP API | Scenario 13 is a harness (FD-17). The PRD does not name a product URL for it |
| User or role admin CRUD | Identity design is later. Company titles are Unknown |
| Lake POST, PUT, PATCH, DELETE | YAML in Git is the source of truth. `build.py` writes SQLite |
| `engineering_hold` scorer | FD-05 rejected |
| Queue rank-by-model | FD-04. Ranking is a written test |
| Billing or ROI API | BO-11 forbids a monetary benefit claim |

---

## What this file does not do

This file does not write server code. It does not assign Application A or Application B ports. It does not choose a token format. It does not invent a page-size number. It does not start Phase 7.
