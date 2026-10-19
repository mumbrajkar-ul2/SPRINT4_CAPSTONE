# Knowledge model

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Specifies FD-07 item schema. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `Project_Intent.md` sections 9 and 9.1; `Execution_Plan.md` section 5; `00-Best Practices` Semantic Layer format as locked in `Execution_Plan.md` and `docs/10-architecture/adrs/adr-lake-yaml-to-sqlite.md`; `docs/05-current-state/conflict-catalogue.md`; `Decision_Tracker.md` FD-07, FD-08, FD-22 |
| Assumptions | Guideline 3 names seven content kinds: business rules, domain knowledge, architecture, code intelligence, data relationships, dependencies, and decisions. Conflicts are recorded as `decision` items plus `conflicts_with` edges. Rule implementations are `code_intelligence` items. `00-Best Practices/Semantic_Layer_capture.pdf` was not on disk; the locked Sprint 3 format is used. |
| Unresolved issues | FD-07 stays DEFERRED in the tracker until the coordinator records this design as DECIDED. Reviewer name for draft items is Unknown. |
| Residual risks | An eighth `kind` value invented in Half B would break this schema. Copying a lot row into `statement` would break the exclude. |

This file is the item schema. Half B must not add a field this file omits. Half B must not drop a required field.

The lake stores one fact per YAML file. `build.py` (Half B) writes those files into `context-lake.sqlite3` tables `items`, `edges`, `terms`, and FTS5.

---

## Finding

**Finding.** One closed item schema, seven `kind` values, eight link types, and a named harvest source for each kind are enough for Half B to build without inventing a field.
**Evidence.** Guideline 3 list in `Project_Intent.md` section 9. Locked semantic-layer format. Phase 4 ADRs name tables, not columns.
**Impact.** FD-07 can be set DECIDED from this file. Application B later reads only these fields.
**Risk.** Adding `parent_lot_id` as a field would claim genealogy the tables do not have.
**Confidence.** High on the field list. Unknown on how many accepted items Half B will produce.
**Open questions.** Exact accepted-item count is Unknown until Half B harvests. Draft-reviewer name is Unknown.

---

## Seven content kinds

`kind` is a closed list. JSON Schema `enum`. Extra values fail the write-time gate.

| kind | What one item states | Harvest source (see `data-source-inventory.md`) | Folder under `context-lake/items/` |
|---|---|---|---|
| `business_rule` | One governed test, or one recorded deviation, with `authority` | S1 archive, S2 register, S3 deviation cards, S11 BO/FD rows that are rules | `rules/` |
| `domain_knowledge` | One fab or workflow fact | S4 domain JSON, S5 domain-assurance and source-systems | `domain/` |
| `architecture` | One boundary, listener, or store placement | S5 service-boundaries and ADR-007, S8 compose and ports, S11 lake ADRs | `architecture/` |
| `code_intelligence` | One function, constant, or module behaviour | S3 four programs, S8 reconcile and server, S9 tests | `code/` |
| `data_relationship` | One schema, key, count, clock, or missing join | S6 and S7 SQLite profiles, S10 document metadata counts | `data/` |
| `dependency` | One reads-from or imports-from link, stated as a fact | S3, S8, S9. Edges of type `depends_on` must point at the matching item | `dependencies/` |
| `decision` | One recorded choice, conflict, or historic note | S5 historic-decisions, correspondence, INC-2025-014, S11 tracker rows, catalogue findings | `decisions/` |

Worked example. Kind `business_rule`, id `rule.recipe_release.limit.v2023.emea`. Statement: the 2023 EMEA `recipe_release` limit is 18,600 USD from 2023-01-01 through 2023-12-31. Source path is the archive JSON. Authority is `policy_archive`.

Worked example. Kind `decision`, id `decision.bp1.recipe_mismatch`. Statement: 91 of 125 process steps have `recipe_version` different from the joined tool `recipe_rev`. Edges `conflicts_with` point at the two column items. There is no eighth kind named `conflict`.

---

## Item schema (FD-07)

Every YAML item uses these fields. JSON Schema sets `additionalProperties: false`.

### Required fields

| Field | Type | Allowed values | What it records |
|---|---|---|---|
| `id` | string | Pattern `^[a-z][a-z0-9._-]+$`. Unique across the lake. | Stable item id. Golden questions cite this id. |
| `kind` | string | The seven values above | Content kind |
| `statement` | string | Plain speech. One fact. No instruction to a model. | The knowledge |
| `source.path` | string | Path relative to the inherited tree, or a capstone-root path for tracker rows | File or table the fact came from |
| `source.sha256` | string | 64 hex characters. Must match `sources/register.yaml` for inherited files | Hash at harvest |
| `recorded_at` | string | ISO date `YYYY-MM-DD` | When the lake learned the fact |
| `claim` | string | `verified_fact`, `inference`, `assumption`, `unknown` | Claim label |
| `trust` | string | `trusted_code`, `trusted_record`, `untrusted_text` | Whether retrieval may treat the text as a fact about code or records, or must quote it as data |
| `owner` | string | A role name, or `unknown` | Who maintains the fact |
| `lake_version` | string | Semver. Half B first accepted lake is `1.0.0` (FD-22) | Lake version that contains this item |
| `item_status` | string | `accepted`, `draft`, `superseded` | Whether Application B may use it as current |
| `policy_status` | string | `decided`, `proposed`, `n/a` | For a number or closure rule. PROPOSED tracker rows use `proposed` |
| `honesty` | string | `REAL`, `PRECOMPUTED`, `SIMULATED`, `EDUCATIONAL`, `n/a` | Honesty on any number inside `statement` |
| `links` | list | Zero or more link objects | Graph edges |

`business_rule` items also require `authority`.

### Optional fields

| Field | Type | Allowed values | When to use |
|---|---|---|---|
| `source.lines` | string | For example `4-5` | Code files |
| `source.locator` | string | For example `policy_register.threshold` or `process_steps.recipe_version` | Table.column |
| `valid_time.from` | string or null | ISO date | When the fact applied in the business. Archive versions always set this. |
| `valid_time.to` | string or null | ISO date. Null means still open | End of validity |
| `authority` | string or null | `policy_archive`, `sme`, `unresolved` | Required on `business_rule`. Optional on others. |
| `supersedes` | string or null | Another item `id` | Replaced item. Also add a `supersedes` edge. |
| `reviewer` | string or null | Name or `unknown` | Required before a `draft` item becomes `accepted` if a model wrote `statement` |
| `reviewed_at` | string or null | ISO date | Same condition |

Worked example of `valid_time` versus `recorded_at`. The 2023 EMEA limit applied from 2023-01-01 to 2023-12-31. The lake records it on 2026-10-18. A `rule_at` query for 2023-07-01 uses `valid_time`. A query for what the lake contained before a later revision uses `recorded_at` and `lake_version`.

### Closed lists Half B must generate into `schemas/enums.generated.json`

Build-time writes this file from the semantic layer and from `PRAGMA table_info`. Nobody edits it by hand.

- `kind` (seven)
- `claim` (four)
- `trust` (three)
- `authority` (three)
- `item_status` (three)
- `policy_status` (three)
- `honesty` (five)
- `link_type` (eight, below)
- every harvested table name and column name from both SQLite files
- site codes: `BR-SP`, `DE-BY`, `GB-ENG`, `IN-BLR`, `JP-KN`, `US-TX`
- country codes: `AU`, `BR`, `DE`, `GB`, `IN`, `JP`, `US`, `ZA`
- sales regions: `APAC`, `EMEA`, `AMER`
- archive rule name: `recipe_release`
- register codes: `FAB-RULE-0` through `FAB-RULE-4`

A model that names `wafer_lots.parent_lot_id` fails the model-output gate, because that column is absent from the generated enum.

---

## Link types

Each `links` entry is `{ type, to }`. `to` is an item `id`. Eight types. Extra types fail write-time.

| type | Meaning | Worked example |
|---|---|---|
| `implements` | Code carries out a rule | `code.legacy_policy.js_allow` implements `rule.recipe_release.limit` |
| `conflicts_with` | Two facts disagree | `data.join.recipe_mismatch` conflicts with a claim that dispatch and equipment share one revision |
| `supersedes` | A later item replaces an earlier one | A 2026 APAC limit item supersedes the 2025 APAC limit item for current lookup. Historical `rule_at` still uses `valid_time`. |
| `governs` | A decision or archive row governs a rule | `decision.fd08.canonical_archive` governs `rule.recipe_release.limit` |
| `evidenced_by` | A count or file supports a statement | `decision.bp1.recipe_mismatch` evidenced_by `data.join.recipe_mismatch` |
| `depends_on` | A program reads a file or table | `code.legacy_policy.js_allow` depends_on `data.contract.decision_policies_archive` |
| `maps_to` | A local term maps to a canonical term | `term.cases.region` maps_to `term.sales_region` |
| `tested_by` | A test or rule-card case locks a fact | `rule.recipe_release.limit` tested_by `test.rule.recipe_release.emea_2023` |

**Verified Fact.** Phase 4 ADR `adr-knowledge-graph-edges-table.md` used `tested_by` in its worked example. Adding it here is an engineering choice so Half B does not invent a ninth ad-hoc type later.

Do not use a catch-all type. `cross_references.relationship` already uses `relates_to`. That weak type stays in the operational store.

---

## SQLite columns Half B will write

Half B `build.py` creates these columns. No extra column.

### `items`

`id`, `kind`, `statement`, `source_path`, `source_lines`, `source_sha256`, `source_locator`, `valid_from`, `valid_to`, `recorded_at`, `claim`, `trust`, `authority`, `owner`, `lake_version`, `item_status`, `policy_status`, `honesty`, `supersedes`, `reviewer`, `reviewed_at`.

### `edges`

`from_id`, `type`, `to_id`. Unique on the three columns together.

### `terms`

`term_id`, `canonical_name`, `definition`, `local_system`, `local_name`, `maps_to_term`, `claim`, `authority`, `source_path`, `policy_status`.

Semantic-layer YAML in `context-lake/semantic-layer/` is the source of `terms`. See `mapping-design.md`.

### FTS5

Index `items.statement` and `items.id`. Name the virtual table `items_fts`.

### `generated/manifest.json`

`lake_version`, `built_at`, `item_count`, `edge_count`, `term_count`, `sqlite_sha256`, `source_register_sha256`, `correlation_id`.

Runtime opens the SQLite file read-only. Only `build.py` writes it.

---

## Authority on rules

| Label | When to set it | What Application B does |
|---|---|---|
| `policy_archive` | The value is in the archive JSON or in `policy_register`, and the interval is valid and unique | Use the value |
| `sme` | BO-05, BO-06a, or BO-07 supplies the meaning | Use the meaning |
| `unresolved` | Silent, overlapping, invalid interval, unsigned PROPOSED number, or two scopes disagree | Return `HOLD_FOR_REVIEW`. Do not guess. |

A `business_rule` with `authority: unresolved` still has test cases. Those cases expect `HOLD_FOR_REVIEW`.

---

## Required coverage before lake version 1.0.0

Half B must produce at least one `accepted` item in each of the seven kinds.

Half B must produce one `decision` item per catalogue row BP1 to BP8.

Half B must produce the rule cards listed in `rule-card-design.md`.

Half B must produce the mapping terms listed in `mapping-design.md`.

Missing any of those fails the build-time gate.

---

## Required item ids (locked for Half B)

Half B creates these ids. Extra ids are allowed. These are not optional.

### Rules and maps

`rule.recipe_release.limit` and one child per archive version (`rule.recipe_release.limit.vYYYY.region` for each of the 15 rows). `rule.recipe_release.no_match`. `rule.policy.overlap_or_invalid`. `rule.fab_rule.family`. `rule.recipe_release.limit.impl.js`. `rule.recipe_release.limit.impl.js_default`. `rule.urgent.amount.impl.python`. `rule.priority.closed.impl.python`. `rule.urgent.severity.impl.python`. `rule.open_closed.operational`. `rule.open_closed.finance_audit`. `rule.region.site_canonical`. `rule.region.specificity`. `rule.region.disagreement`. `rule.threshold.silent`. `rule.month_end.blank.impl.java`. `rule.month_end.float.impl.java`. `rule.open_flag.impl.night_batch`. `rule.night_batch.join_multiply`. `rule.feed.replay_duplicate`. `rule.recipe.mismatch_show_both`. `rule.clock.event_vs_arrival`. `rule.untrusted_text.block`. `rule.threshold.never_999999`. `rule.threshold.demo_50000`. `rule.hold.person_only`.

`map.site.IN-BLR`. `map.site.JP-KN`. `map.site.US-TX`. `map.site.BR-SP`. `map.site.DE-BY`. `map.site.GB-ENG`.

### Code, architecture, dependency

`code.legacy_logic.priority`. `code.legacy_policy.js_allow`. `code.reconcile_legacy.java_total`. `code.shift_reconciliation.night_batch`. `code.partner_feeds.reconcile`. `arch.listener.legacy_8080`. `arch.listener.gateway_8090`. `arch.listener.lake_rest_8091`. `arch.listener.lake_mcp_8092`. `arch.compose.inherited`. `arch.lake.yaml_sqlite`. `arch.graph.edges_table`. `dep.js_reads_archive`. `dep.night_batch_reads_enterprise`.

### Data

`data.contract.decision_policies_archive`. `data.join.recipe_mismatch`. `data.missing.lot_genealogy`. `data.missing.case_lot_id`. `data.clock.event_vs_arrival_partner`. `data.clock.event_vs_arrival_evidence`. `data.feed.replay`. `data.policy_register.overlap`. `data.policy_register.invalid_interval`. `data.task.unassigned`. `data.org.tenant_country_pairing`. `data.injection.partner_feeds`. `data.injection.bundled_events`. `data.injection.emails`. `data.injection.source_documents`. `data.injection.html`. `data.injection.evidence_payloads`.

### Domain and terms (also in semantic-layer YAML)

`domain.profile.states`. `domain.profile.parts`. `domain.profile.policies`. `domain.profile.systems`. `domain.object.lot`. `term.open_operational`. `term.closed_operational`. `term.closed_finance`. `term.closed_audit`. `term.recipe_revision_dispatch`. `term.recipe_revision_equipment`. `term.recipe_revision_change`. `term.recipe_release_limit`. `term.recipe_mismatch`. `term.lot_genealogy`. `term.sales_region`. `term.country_code`. `term.site_code`.

### Decisions

`decision.fd08.canonical_archive`. `decision.fd06.two_apps`. `decision.fd22.lake_version_policy`. `decision.bo05.recipe_authority`. `decision.bo06a.open_closed`. `decision.bo06b.three_closures`. `decision.bo07.site_canonical`. `decision.bo08.silent_threshold`. `decision.bp1.recipe_mismatch`. `decision.bp2.replay`. `decision.bp3.two_clocks`. `decision.bp4.four_programs`. `decision.bp5.open_closed_words`. `decision.bp6.region_overlap`. `decision.bp7.untrusted_text`. `decision.bp8.auth_and_owner`. `decision.inc_2025_014`. `decision.historic.2025_replay_rollback`.

A test item id pattern `test.rule.*` is allowed for `tested_by` edges. Half B names those when it writes cards.

---

## What a statement may contain

A statement is one fact in plain speech. It may name a count that a harvest query produced, with honesty REAL.

A statement may quote untrusted language only when `trust` is `untrusted_text`, and only inside quotation marks, and only to identify a locator. Retrieval then returns that quote inside a data envelope. See `provenance-policy.md`.

A statement must not tell a model to approve, ignore, or release.

A statement must not paste a full `wafer_lots` or `cases` row.

---

## What this file does not do

This file does not write YAML items. It does not write JSON Schema files. It does not write `build.py`. It does not start Half B.
