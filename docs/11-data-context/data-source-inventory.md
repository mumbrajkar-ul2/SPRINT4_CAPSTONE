# Data source inventory

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No lake YAML, `build.py`, tests, or SQLite written in this unit. |
| Evidence sources | `docs/05-current-state/conflict-catalogue.md`; `docs/05-current-state/system-landscape.md`; `docs/05-current-state/brownfield-inventory.md`; `sources/register.yaml`; `contracts/decision-policies-archive.json` under the inherited tree; the four rule files; `domain-profile.json`; `domain.json`; `Decision_Tracker.md` FD-08, BO-05, BO-06a, BO-07; `Execution_Plan.md` section 5; read-only SQLite URI `mode=ro` on 2026-10-18 |
| Assumptions | Harvest in Half B reads the packaged tree. It does not run `python -m app.generate --reset`. The SHA-256 list in `sources/register.yaml` (1,590 files, captured 2026-10-18) is the source freeze Half B hashes against. |
| Unresolved issues | `00-Best Practices/Semantic_Layer_capture.pdf` was not present on disk in this unit. INC-2025-014 follow-up owner stays Unknown. Workshop 500k and stress 2M lake tiers are absent from this archive. |
| Residual risks | A harvest that copies a `wafer_lots` row into an item would break the Phase 5 exclude. A harvest that treats feed notes as instructions would break BP7. |

This file lists every source Half B may harvest. The lake stores knowledge about the estate. Raw operational rows stay in `legacy.sqlite3` and `enterprise_legacy.sqlite3`.

Each source row says what kind of lake item it fills. Kind names match `knowledge-model.md`.

---

## How to read this inventory

**Verified Fact.** The inherited tree lives at `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`. Phase 0 hashed 1,590 files into `sources/register.yaml`.

**Verified Fact.** FD-08. Canonical business-rule numbers come from `contracts/decision-policies-archive.json` and the `policy_register` table. The four local programs are deviations.

Harvest writes YAML facts. Harvest does not copy lot yields, case notes, or feed JSON into the lake as rows.

Honesty on packaged counts in this file is REAL.

---

## Finding

**Finding.** Twelve source groups cover the seven guideline-3 content kinds. No group is a copy of the 125 lot rows.
**Evidence.** Catalogue BP1 to BP8. System landscape table counts. File paths in the brownfield inventory. Read-only queries on 2026-10-18.
**Impact.** Half B can assign one harvest script per group without inventing a source.
**Risk.** Treating `organizations.tenant` as a region map would encode a generator pairing that puts Brazil under `TENANT-APAC`.
**Confidence.** High on the source list. Unknown on live unittest count.
**Open questions.** Who reviews model-drafted document items. Named person is Unknown.

---

## Source groups

### S1 Governed policy archive

| Field | Value |
|---|---|
| Path | `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/contracts/decision-policies-archive.json` |
| What it holds | 15 `historical_versions` of rule `recipe_release`. Regions APAC, EMEA, AMER. Years 2022 through 2026. Currency USD. |
| 2026 limits | APAC 25,000. EMEA 26,100. AMER 27,200. Honesty: REAL. |
| Fills kind | `business_rule` |
| Required item ids | `rule.recipe_release.limit` plus one child id per version, for example `rule.recipe_release.limit.v2026.apac` |
| Claim label | `verified_fact` |
| Trust | `trusted_record` |
| Authority | `policy_archive` |
| Do not harvest | The JavaScript 1.05 reading of this file. That reading is S3. |

Worked example. The 2023 EMEA row has `effective_from` 2023-01-01, `effective_to` 2023-12-31, `limit` 18600. Half B writes that as one item. Golden question GQ-01 expects 18,600 from that item.

### S2 Policy register table

| Field | Value |
|---|---|
| Path | `data/enterprise_legacy.sqlite3` table `policy_register` |
| What it holds | 40 rows. Columns `policy_id`, `region` (country code), `policy_code`, `active`, `valid_from`, `valid_to`, `threshold`, `owner_team`. |
| Active rows | 34. Honesty: REAL. Per country 4 or 5 active rows. |
| Fills kind | `business_rule` (register family `FAB-RULE-0` to `FAB-RULE-4`) and `data_relationship` (overlap and invalid interval) |
| Required item ids | `rule.fab_rule.family`, `data.policy_register.overlap`, `data.policy_register.invalid_interval` |
| Claim label | `verified_fact` for schema, counts, and the invalid interval. |
| Trust | `trusted_record` |
| Authority | `policy_archive` for the stored threshold. `unresolved` when two active rows overlap on one country, or when `valid_from` is after `valid_to`. |

Worked example. `POL-0039` has `valid_from` 2025-01-01 and `valid_to` 2024-12-31, `active` 1. The interval is empty. Half B records that row as a self-contradiction and routes a match to `HOLD_FOR_REVIEW`. Half B does not copy all 40 rows into the lake.

`FAB-RULE-0` through `FAB-RULE-4` are a different rule family from `recipe_release`. A register threshold is not a `recipe_release` limit.

### S3 Four local rule programs

| Program | Path | Deviation to record | Fills kind |
|---|---|---|---|
| Python priority | `app/legacy_logic.py` | Urgent when severity is CRITICAL or `amount > 50000`. CLOSED returns `archive`. | `code_intelligence` plus a deviation card under `business_rule` |
| JavaScript allow | `legacy_js/legacy_policy.js` | Allows amount up to archive limit times 1.05. Missing year or region returns 999999. | same |
| Java totals | `legacy_java/ReconcileLegacy.java` | Sums `amount_text` as float. A blank or unreadable cell is skipped with no report. Packaged blanks: 10. Honesty: REAL. | same |
| Night batch | `legacy_batch/shift_reconciliation.py` | Flags HOLD and REVIEW, and flags `value > threshold` after a join on country code to every active register row. Default `LIMIT 500` applies to joined rows. | same |

**Verified Fact.** BO-06a. The night-batch file flags REVIEW. Its comment says it treats REVIEW as open. That matches the operational meaning. The remaining night-batch deviations are the join that multiplies one object into several flagged rows, and the `LIMIT 500` on joined rows.

Required item ids: `code.legacy_logic.priority`, `code.legacy_policy.js_allow`, `code.reconcile_legacy.java_total`, `code.shift_reconciliation.night_batch`, plus deviation cards `rule.recipe_release.limit.impl.js`, `rule.urgent.amount.impl.python`, `rule.month_end.total.impl.java`, `rule.open_flag.impl.night_batch`.

Trust: `trusted_code`. Authority on deviation cards: `unresolved` for any number the archive does not state. The Python 50,000 cutoff is PROPOSED for demo only (BO-08). Never 999,999 as a live policy number.

### S4 Domain profile and domain JSON

| Path | Fills kind | What to extract |
|---|---|---|
| `domain-profile.json` | `domain_knowledge` | Units LOT, WAFER, TOOL. States QUEUED, PROCESSING, HOLD, ENGINEERING_REVIEW, RELEASED. Kinds RECIPE_CHANGE, METROLOGY_RESULT, YIELD_EXCURSION. Parts ETCH, LITHO, DEPOSITION, CMP. Policies `spc_hold`, `ec_effective_date`, `tool_qualification`, `lot_genealogy`. Systems MESDispatch and PLM-Metrology. |
| `domain.json` | `domain_knowledge` | Object is production lot. Partition is chamber. Metric is `scrap_cost` in USD. |

Required item ids: `domain.profile.states`, `domain.profile.parts`, `domain.profile.policies`, `domain.profile.systems`, `domain.object.lot`.

`lot_genealogy` is a named policy string in the profile. No `parent_lot_id` column exists on `wafer_lots`. Half B records that gap as Unknown. It does not invent a parent link.

### S5 Inherited docs that state practice and history

| Path | Fills kind |
|---|---|
| `docs/domain-assurance.md` | `domain_knowledge`. `recipe_release` needs authorized human review. SEMI-style process traceability is background. The file says this is a synthetic training environment. |
| `docs/source-systems-and-constraints.md` | `domain_knowledge` and `architecture`. MESDispatch and PLM-Metrology. Schema revisions 1.0, 1.1, 2.0, unsupported. Three clocks: source, ingest, revision. |
| `docs/service-boundaries.md` | `architecture`. Night batch reads the enterprise SQLite file directly. JavaScript applies a distinct reading. |
| `docs/decisions/ADR-archived-007.md` | `decision` and `architecture`. Nightly file exchange accepted 2022. Diagram still shows an obsolete endpoint. |
| `docs/historic-decisions.md` | `decision`. Five year sentences, 2022 through 2026. 2025 rollback after a replayed partner delivery. |
| `docs/correspondence/operations-vs-risk-2024.md` | `decision`. Operations wants close within 48 hours. Compliance refuses automatic closures without evidence. Finance has not agreed what counts as resolved. |
| `docs/data-dictionary.md` | `data_relationship`. `fab_tools` and `wafer_lots` column lists. |
| `docs/operations-service-levels.md` | `domain_knowledge`. Historical working targets, not measured guarantees. 48-hour close is correspondence, not a signed cutoff. |
| `operations/incidents/INC-2025-014.md` | `decision`. Owner unknown. Manual spreadsheet at 04:00 UTC on 2025-11-18. |
| `docs/business-context.md`, `docs/interface-notes.md`, remaining inherited `docs/` | Harvest metadata and one statement per file. Model may draft. A person reviews before `item_status: accepted`. |

Claim on reviewed prose: `inference` until a person accepts. Then `verified_fact` of the file text, still `inference` for any gloss.

### S6 Operational SQLite `legacy.sqlite3`

19 tables. Harvest schema, keys, counts, and value lists. Do not copy the 125 lot rows.

| Table | Rows | Knowledge to extract | Kind |
|---|---:|---|---|
| `cases` | 125 | Columns. Status words OPEN, UNDER_REVIEW, CLOSED, ESCALATED, REOPENED. Six site codes. Three sales regions. Site and region assigned independently (see `mapping-design.md`). | `data_relationship` |
| `fab_tools` | 30 | `recipe_rev`. `chamber` holds a site code. | `data_relationship` |
| `process_steps` | 125 | `recipe_version`. Join to `fab_tools` on `tool_id`. 91 mismatches. Honesty: REAL. | `data_relationship` |
| `wafer_lots` | 125 | `engineering_hold`. No `parent_lot_id`. No `lot_id` on `cases`. | `data_relationship` |
| `metrology` | 125 | `measured`, `spec_low`, `spec_high`. Join to lots on `lot_id`. | `data_relationship` |
| `engineering_changes` | 30 | `from_rev`, `to_rev`, `effective_at`, `approval_state`. | `data_relationship` |
| `partner_feeds` | 8,567 | `source_ts` and `ingest_ts`. 67 REPLAY. 86 notes with auto-approve language. | `data_relationship` plus injection locators |
| `vendor_file_rows` | 2,400 | 10 blank `amount_text`. Honesty: REAL. | `data_relationship` |
| `events` | 145 | `recorded_at`. Types CASE_CREATED 125, STATUS_REVIEWED 20. | `data_relationship` |
| remaining 10 tables | as catalogued | Column lists, keys, counts | `data_relationship` |

Required item ids include `data.join.recipe_mismatch`, `data.missing.lot_genealogy`, `data.missing.case_lot_id`, `data.clock.event_vs_arrival_partner`, `data.feed.replay`.

### S7 Enterprise SQLite `enterprise_legacy.sqlite3`

12 tables. Same harvest rule: schema, keys, counts. No object-row copy.

| Fact | Count | Honesty | Kind |
|---|---:|---|---|
| `operational_objects` | 12,500 | REAL | `data_relationship` |
| status REVIEW | 2,090 | REAL | `data_relationship` |
| status HOLD | 2,083 | REAL | `data_relationship` |
| `evidence_events` arrival differs from event_time | 11,985 of 12,500 | REAL | `data_relationship` |
| `workflow_tasks` with `assigned_to` empty | 695 | REAL | `data_relationship` |
| `organizations` tenant and country pairing | 96 orgs. `TENANT-APAC` holds IN and BR. `TENANT-SOUTH` holds AU and JP. | REAL | `data_relationship` |
| `cross_references.relationship` | `relates_to`, `supersedes`, `same_source` | REAL | `data_relationship`. Lake `edges` uses a tighter type list. Do not copy `relates_to` as the lake default. |

Required item ids: `data.clock.event_vs_arrival_evidence`, `data.task.unassigned`, `data.org.tenant_country_pairing`.

### S8 Integration contracts and HTTP pieces

| Path | Fills kind |
|---|---|
| `integration/source-gateway.json` | `architecture`, `dependency` |
| `integration/source-contract-v1.json` | `architecture` |
| `app/server.py` | `code_intelligence`. Port 8080. No identity check. |
| `services/source_gateway/server.py` | `code_intelligence`. Port 8090. Returns `occurred_at` and `published_at`. |
| `compose.yaml` | `architecture`, `dependency`. Services legacy, source-gateway, bridge. |
| `app/partner_feeds.py` `reconcile()` | `code_intelligence`. REPLAY becomes DUPLICATE. |
| `app/gateway_bridge.py` | `code_intelligence`. Duplicate `message_id` is a primary-key error. |

Required item ids: `arch.listener.legacy_8080`, `arch.listener.gateway_8090`, `arch.compose.inherited`, `code.partner_feeds.reconcile`, `dep.js_reads_archive`.

### S9 Tests

Seven modules under `tests/`. Fills `code_intelligence` and `dependency` (`tested_by` edges). Record what each module checks and what it skips, from `docs/05-current-state/brownfield-inventory.md`. Do not run `unittest` in Half B harvest if a test writes the packaged database.

### S10 Documents, archive mail, bundled lake events

| Store | Count | Injection subset | Kind |
|---|---:|---:|---|
| `data/documents/source_documents.jsonl` | 1,200 | 22 bodies with ignore-or-release language | Profile as `data_relationship`. Injection locators in `injection-corpus-design.md`. Text is `untrusted_text`. |
| `data/archive_documents/*.eml` | 210 | 3 with approve-or-ignore language | same |
| `data/archive_documents/*.html` | 210 | 2 extra with the same language | same |
| Bundled lake events JSONL | 100,000 | 150 with `source_claim` approve language | Profile schema versions and defect counts. Do not copy 100,000 events. |

A model may draft a one-line summary of document metadata (kind, site, language, status). The body stays untrusted data. `item_status` stays `draft` until a person accepts.

### S11 Capstone decisions already locked

These live at the capstone root. They fill `decision` items so Application B can cite them.

| Source | Item id |
|---|---|
| FD-08 | `decision.fd08.canonical_archive` |
| BO-05 | `decision.bo05.recipe_authority` |
| BO-06a | `decision.bo06a.open_closed` |
| BO-07 | `decision.bo07.site_canonical` |
| FD-22 | `decision.fd22.lake_version_policy` |
| FD-06 architecture ADRs | `decision.fd06.two_apps`, `arch.lake.yaml_sqlite`, `arch.graph.edges_table` |
| BO-06b PROPOSED | `decision.bo06b.three_closures` with `policy_status: proposed` and `authority: unresolved` |
| BO-08 PROPOSED | `decision.bo08.silent_threshold` with `policy_status: proposed` and `authority: unresolved` |

Do not write a PROPOSED number as a decided limit.

### S12 Source register

`sources/register.yaml` is the hash freeze. Half B harvest records the SHA-256 of each harvested file against that register. A mismatch fails the build-time gate.

The register itself is not copied into `items/`. Its hash goes in `generated/manifest.json`.

---

## Sources that stay out of the lake as rows

| Store | Why it stays out | Label |
|---|---|---|
| 125 `wafer_lots` rows | Phase 5 exclude. Knowledge about the table is in. The yield numbers stay in SQLite. | Verified Fact of the exclude |
| 12,500 `operational_objects` rows | Same | Verified Fact |
| 8,567 feed JSON bodies | Profile and injection locators only | Verified Fact |
| 50,000 bundled CSV transactions | Profile counts and schema versions only | Verified Fact |
| Workshop 500k and stress 2M tiers | Not in this archive | Verified Fact |

---

## Harvest method per source type

| Source type | Method in Half B | Claim |
|---|---|---|
| SQLite schema and counts | Script. `PRAGMA table_info`. `SELECT COUNT`. Distinct value lists. URI `mode=ro`. | `verified_fact` |
| JSON archive and domain files | Script parse. One item per version or term. | `verified_fact` |
| Python | `ast` parse for functions, constants, imports. | `verified_fact` |
| Java and JavaScript | Hand extract with line numbers. Files are short. | `verified_fact` |
| Markdown docs, ADR, incident | Model may draft. Person reviews. | `inference` until accepted |
| Document bodies and feed notes | Metadata script. Body stored only as untrusted locator, never as an instruction. | `untrusted_text` |

Each harvest run records script version, date, and, if a model drafted text, model name and prompt version. **Assumption.** A named reviewer exists before a draft item is accepted. The name is Unknown in this unit.

---

## What this file does not do

This file does not write harvest scripts. It does not write YAML items. It does not copy a row. It does not start Half B.
