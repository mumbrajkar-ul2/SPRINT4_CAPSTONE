# Schema specifications

| Field | Value |
|---|---|
| Stage | Phase 6 / 12 Spec-driven design |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. Lake schemas already exist. This file binds them to the APIs and names operational payloads. Audit columns stay later. |
| Evidence sources | `docs/11-data-context/knowledge-model.md`; `docs/11-data-context/data-contracts.md`; `context-lake/schemas/*.json`; `docs/09-initial-prd/functional-requirements.md`; lake items listed per schema. Confirmed in `context-lake.sqlite3` on 2026-10-18. |
| Assumptions | Semantic layer stays: Markdown explains, YAML defines, JSON Schema validates with `additionalProperties` false, tests protect, generated output serves. Half B already wrote the six schema files. |
| Unresolved issues | Audit row columns stay Unknown (FD-23). Money type for Java float totals stays unresolved (`rule.month_end.float.impl.java`). Default page size stays Unknown. Identity token schema stays Unknown (FD-13). |
| Residual risks | Adding `parent_lot_id` would claim genealogy the tables do not have. Lake item `data.missing.lot_genealogy`. Marking 50,000 `decided` in a schema enum would sign BO-08 in code. |

This file names the schemas the contracts use. The lake item, link, rule-card, term, enum, and read-envelope schemas already sit under `context-lake/schemas/`. This unit does not change those files.

---

## Finding

**Finding.** Six lake JSON Schemas plus the operational case, queue, approval, recovery, query, and lineage payloads are enough for Phase 6. The audit column list stays open.
**Evidence.** `arch.lake.yaml_sqlite`. Files `item.schema.json`, `link.schema.json`, `rule-card.schema.json`, `term.schema.json`, `enums.generated.json`, `read-envelope.schema.json`.
**Impact.** Application B binds to these schemas. Application A uses the same read envelope when it cites the lake.
**Risk.** Editing `enums.generated.json` by hand would let a fake column through the model-output gate.
**Confidence.** High on the lake files. Unknown on audit columns and money type.
**Open questions.** FD-23. Java money type. Identity token schema.

---

## SCH-01 Lake item

**Verified Fact.** `arch.lake.yaml_sqlite`. `docs/11-data-context/knowledge-model.md`. File `context-lake/schemas/item.schema.json`.

| Rule | Value |
|---|---|
| Extra properties | false |
| `kind` | Closed list of seven: `business_rule`, `domain_knowledge`, `architecture`, `code_intelligence`, `data_relationship`, `dependency`, `decision` |
| `id` | Pattern already in the schema. Unique |
| `item_status` | `accepted`, `draft`, `superseded` |
| `claim` | `verified_fact`, `inference`, `assumption`, `unknown` |
| `honesty` | `REAL`, `PRECOMPUTED`, `SIMULATED`, `EDUCATIONAL`, `n/a` |

Lake 1.0.0 holds 148 items, of which `data.draft.business_context` is draft. Application B uses `accepted` items as current. Honesty on 148: REAL.

A `business_rule` item requires `authority`: `policy_archive`, `sme`, or `unresolved`.

Worked example. Id `rule.recipe_release.limit.v2023.emea` is `kind: business_rule`, `authority: policy_archive`, honesty REAL for 18,600 USD.

---

## SCH-02 Lake link / edge

**Verified Fact.** `arch.graph.edges_table`. File `context-lake/schemas/link.schema.json`.

| Rule | Value |
|---|---|
| Extra properties | false |
| `type` | Closed list of eight: `conflicts_with`, `depends_on`, `evidenced_by`, `governs`, `implements`, `maps_to`, `supersedes`, `tested_by` |
| `to` | An item id that exists |

Lake 1.0.0 holds 180 edges. Honesty: REAL. API-L-05 returns these rows.

---

## SCH-03 Rule card

**Verified Fact.** File `context-lake/schemas/rule-card.schema.json`. Cards live as lake items under `kind: business_rule`.

Minimum card fields: `id`, `kind`, `inputs`, `decision_table`, `authority`, `owner`, `policy_status`, `tests`, `observed_implementations`.

`then.route` is one of `ALLOW`, `DENY`, `URGENT`, `QUEUE`, `ARCHIVE`, `HOLD_FOR_REVIEW`, `BLOCK`, `OPEN`, `CLOSED_OPERATIONAL`.

A card with `authority: unresolved` includes a `no_match` or `overlap` row that expects `route: HOLD_FOR_REVIEW`.

A card must not place 999,999 in `decision_table` as a canonical limit. Lake item `rule.threshold.never_999999`.

A card may record 50,000 only on the Python deviation, with `policy_status: proposed`. Lake items `rule.urgent.amount.impl.python`, `rule.threshold.demo_50000`. BO-08 stays PROPOSED.

---

## SCH-04 Term

**Verified Fact.** File `context-lake/schemas/term.schema.json`. Lake 1.0.0 holds 267 term rows. Honesty: REAL.

Required: `term_id`, `canonical_name`, `definition`, `local_names`, `authority`, `policy_status`, `claim`.

Operational terms this spec uses:

| term_id | What it names | Lake item also in `items` |
|---|---|---|
| `open_operational` | REVIEW and HOLD stay open | `term.open_operational` |
| `closed_operational` | Final disposition and no pending engineering action | `term.closed_operational` |
| `closed_finance` | Finance booked. Separate from operational closed | `term.closed_finance` |
| `closed_audit` | Audit closed. Separate from operational closed | `term.closed_audit` |
| `replay` | `processing_status` that marks a duplicate candidate | `term.replay` |
| `duplicate` | Status `reconcile()` writes for a REPLAY feed | `term.duplicate` |
| `approval` | A person action | `term.approval` |
| `outage` | One row in `upstream_outages` | `term.outage` |
| `case` | One exception case | `term.case` |

BO-06b stays PROPOSED. `closed_finance` and `closed_audit` are not merged into `closed_operational`. Lake item `rule.open_closed.finance_audit`.

---

## SCH-05 Read envelope

**Verified Fact.** File `context-lake/schemas/read-envelope.schema.json`. Extra properties false.

| Field | Type | Allowed values |
|---|---|---|
| `ok` | boolean | true or false |
| `lake_version` | string | Semver. Current pin 1.0.0 |
| `items` | array | Item objects, or empty |
| `edges` | array | Edge objects, or empty |
| `citations` | array of string | Item ids |
| `trust_summary` | string | `trusted` or `contains_untrusted_text` |
| `untrusted_quotes` | array of string | Possibly empty |
| `verdict` | string | `ANSWER`, `ABSTAIN`, `HOLD_FOR_REVIEW` |
| `block` | boolean | true on the injection stop path |

Optional pagination fields `limit` and `offset` may appear on the HTTP request. They are not required on the envelope itself. Phase 5 allowed Phase 6 to add pagination. This spec does not remove envelope fields.

`untrusted_quotes` holds strings copied from items whose `trust` is `untrusted_text`. Those strings do not sit in an instruction field. Lake item `rule.untrusted_text.block`.

---

## SCH-06 Operational case payload

**Inference** from FR-01, FR-03, FR-05, FR-07, FR-08. Authority: team-force (ED-P6-02). Extra properties that the later JSON Schema will reject stay out of this list.

| Field | Required | What it holds | Lake item |
|---|---|---|---|
| `case_id` | yes | Case identifier | `term.case` |
| `status` | yes | Stored status word | `decision.bp5.open_closed_words` |
| `open_operational` | yes | true when REVIEW, HOLD, or other pending action | `rule.open_closed.operational` |
| `severity` | yes | Stored severity | `code.legacy_logic.priority` |
| `amount` | yes | Stored amount | `code.legacy_logic.priority` |
| `recipe_version` | when present on the join | Dispatch revision | `rule.recipe.mismatch_show_both` |
| `recipe_rev` | when present on the join | Equipment revision | `rule.recipe.mismatch_show_both` |
| `event_time` | when evidence exists | Event clock | `rule.clock.event_vs_arrival` |
| `arrival_time` | when evidence exists | Arrival clock | `rule.clock.event_vs_arrival` |
| `untrusted_quotes` | yes, may be empty | Flagged strings | `rule.untrusted_text.block` |
| `waiting_role` | when waiting | `RT-01` to `RT-06` | `term.approval` |
| `owner_id` | no | Empty allowed. Unknown stays empty | `decision.inc_2025_014` |
| `finance_closed` | no | Separate flag. PROPOSED | `rule.open_closed.finance_audit` |
| `audit_closed` | no | Separate flag. PROPOSED | `rule.open_closed.finance_audit` |
| `draft_plan` | no | Model text. Not a write | `rule.hold.person_only` |
| `citations` | when a model sentence is present | Lake item ids | `arch.lake.yaml_sqlite` |

`parent_lot_id` is absent. Lake item `data.missing.lot_genealogy`. A query for the parent lot abstains.

---

## SCH-07 Approval payload

**Inference** from FR-13 and Group C. Authority: team-force (ED-P6-03).

| Field | Required | Allowed values |
|---|---|---|
| `case_id` | yes | String |
| `action_type` | yes | `dispose`, `approve_agent`, `recipe_hold_or_release`, `policy_pick`, `replay_confirm`, `assign_owner` |
| `decision` | yes | `approve`, `hold`, `block`, `drop_duplicate`, `keep_duplicate`, `keep_wait`, `assign` |
| `actor_role` | yes | `RT-01` to `RT-06` |
| `actor_id` | yes | Person. Format Unknown until FD-13 |
| `proposed_by` | yes | Must differ from `actor_id` |
| `correlation_id` | yes | String. Minting later |
| `owner_id` | when assign | Person supplied at RT-06 |
| `policy_id` | when policy pick and not keep-wait | A policy id |
| `hold_value` | when recipe hold or release | Hold or release |

The later JSON Schema sets `additionalProperties: false`.

---

## SCH-08 Recovery payload

**Inference** from FR-08 and Scenario 11. Authority: team-force.

| Field | Required | Allowed values | Lake item |
|---|---|---|---|
| `status_visible` | yes | User-visible retry or mismatch text | `term.outage` |
| `error_class` | yes | `timeout`, `schema`, `rate_limit`, `none` | `arch.listener.gateway_8090` |
| `owner_id` | no | Empty allowed | `decision.inc_2025_014` |
| `correlation_id` | yes | String | locked audit idea |

No recovery-time number sits on this payload.

---

## SCH-09 Query response payload

**Inference** from FR-10 and FR-11. Authority: team-force.

| Field | Required | Allowed values |
|---|---|---|
| `sentence` | yes | Cited text, or empty when abstain |
| `citations` | yes | Lake item ids or stored-row locators |
| `verdict` | yes | `ANSWER`, `ABSTAIN`, `HOLD_FOR_REVIEW` |
| `block` | yes | boolean |
| `untrusted_quotes` | yes | array, may be empty |

Percent floors stay off this schema. FD-14 and FD-18 remain later.

---

## What stays out of schema in this unit

| Item | Why |
|---|---|
| Audit column list | FD-23 PENDING |
| Identity token fields | FD-13 PENDING |
| `parent_lot_id` | Column does not exist. `data.missing.lot_genealogy` |
| Canonical 999,999 | `rule.threshold.never_999999` |
| Canonical 50,000 as decided | BO-08 PROPOSED. `rule.threshold.demo_50000` |
| Money binary type | `rule.month_end.float.impl.java` records the Java float deviation. Canonical money type is Unknown |
| Application A / Application B host port | Unknown |

---

## What this file does not do

This file does not edit `context-lake/schemas/`. It does not invent audit columns. It does not sign BO-06b or BO-08. It does not start Phase 7.
