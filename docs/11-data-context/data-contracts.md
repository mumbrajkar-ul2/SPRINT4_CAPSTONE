# Data contracts

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `knowledge-model.md` (this folder, written in the same unit); `docs/10-architecture/adrs/adr-lake-yaml-to-sqlite.md`; `docs/10-architecture/adrs/adr-app-b-reads-only-the-lake.md`; `Execution_Plan.md` section 5; locked semantic-layer format: Markdown explains, YAML defines, JSON Schema validates with `additionalProperties` false, tests protect, generated output serves |
| Assumptions | Phase 6 (FD-11) will write the full REST and event contracts. This file names the lake-side shapes Half B must validate. Port 8091 REST and port 8092 MCP exist as listeners later. Their JSON bodies still follow these item, edge, term, and envelope shapes. |
| Unresolved issues | Exact REST path list is Phase 6. OPA rule bodies are Phase 10 (FD-16). Identity on the lake API is Phase 8 and Phase 12. |
| Residual risks | Serving YAML files at run time would skip FTS5 and the hashable SQLite artifact. Letting a model add a property would reopen the schema. |

This file names the contracts Half B enforces. The five gates that reject a broken payload live in `contract-gates.md`.

---

## Finding

**Finding.** Four JSON Schemas and one generated enum file are the lake contract. Markdown explains. YAML defines. Schema validates. Tests protect. SQLite serves.
**Evidence.** Locked semantic-layer format. Phase 4 ADR for YAML-to-SQLite. `knowledge-model.md` field list.
**Impact.** Half B writes schemas under `context-lake/schemas/`. Application B later binds to those schemas.
**Risk.** Editing `enums.generated.json` by hand would let a fake column through the model-output gate.
**Confidence.** High on the file list. Unknown on REST path names until Phase 6.
**Open questions.** REST path list. MCP tool names stay with FD-15 in Phase 10, except the four lake-read tools named below as a minimum.

---

## Semantic-layer format

**Verified Fact.** `Execution_Plan.md` section 5 and Phase 4 ADR.

| Layer | File pattern in Half B | What it does |
|---|---|---|
| Explains | `context-lake/semantic-layer/*.md` | Plain-speech definition of a term |
| Defines | `context-lake/semantic-layer/*.yaml` | Canonical name, local names, maps |
| Validates | `context-lake/schemas/*.json` | `additionalProperties: false` |
| Protects | `context-lake/tests/` | Schema, parity, graph, injection |
| Serves | `context-lake/generated/context-lake.sqlite3` | `items`, `edges`, `terms`, FTS5 |

Worked example. Term `open_operational` is explained in Markdown, defined in YAML, validated by `term.schema.json`, locked by a test that a REVIEW object counts as open, and served as one `terms` row.

---

## Schema files Half B must write

| File | extra properties | Required contents |
|---|---|---|
| `schemas/item.schema.json` | false | Every field in `knowledge-model.md`. `kind` enum of seven. `business_rule` requires `authority`. |
| `schemas/link.schema.json` | false | `type` enum of eight. `to` is an item id string. |
| `schemas/rule-card.schema.json` | false | Shape in `rule-card-design.md`. |
| `schemas/term.schema.json` | false | Shape of a semantic-layer term in `mapping-design.md`. |
| `schemas/enums.generated.json` | false | Closed lists. Written by `build.py`. Not hand-edited. |
| `schemas/read-envelope.schema.json` | false | Read response: `item` or `term` payload, `citations`, `trust`, `untrusted_quotes` list. Unknown properties rejected. |

`untrusted_quotes` is a list of strings copied from items whose `trust` is `untrusted_text`. The envelope keeps those strings out of any instruction field.

---

## YAML item contract

One file per item. Path: `context-lake/items/<kind-folder>/<id>.yaml`.

Kind folders: `rules`, `domain`, `architecture`, `code`, `data`, `dependencies`, `decisions`.

`item_status: draft` files live under `context-lake/items/_drafts/` until a reviewer accepts them. Accepted files never stay in `_drafts/`.

Id must match the file stem. `rule.recipe_release.limit.v2023.emea.yaml` has `id: rule.recipe_release.limit.v2023.emea`.

---

## Rule-card contract

One file per business rule under `context-lake/items/rules/` with `kind: business_rule`, or a sibling `*.card.yaml` if Half B splits card from version rows.

Minimum card fields: `id`, `kind`, `inputs`, `decision_table`, `authority`, `owner`, `policy_status`, `tests`, `observed_implementations`.

See `rule-card-design.md` for the closed card list and the test cases.

A card with `authority: unresolved` must include a `no_match` or `overlap` row that expects `route: HOLD_FOR_REVIEW`.

A card must not place 999,999 in `decision_table` as a canonical limit.

A card may record 50,000 only on the Python deviation implementation, with `policy_status: proposed`.

---

## Term contract

Each canonical term has:

| Field | Required |
|---|---|
| `term_id` | yes |
| `canonical_name` | yes |
| `definition` | yes, one sentence |
| `local_names` | list of `{ system, field_or_word, meaning }` |
| `authority` | `policy_archive`, `sme`, `unresolved`, or `n/a` |
| `policy_status` | `decided`, `proposed`, `n/a` |
| `claim` | four-way label |

Minimum terms are listed in `mapping-design.md`. `Project_Intent.md` section 9.2 also names lot, wafer, tool, chamber, recipe revision, process step, metrology sample, excursion, engineering hold, engineering change, case, evidence, decision, policy, source message, replay, duplicate, outage, cost period, and approval. Half B writes all of those.

---

## Read envelope contract

Every REST or MCP read returns this shape. Phase 6 may add pagination fields. It may not remove these.

| Field | What it holds |
|---|---|
| `ok` | true or false |
| `lake_version` | from `lake-version.md` / manifest |
| `items` | list of item objects, or empty |
| `edges` | list of edge objects when the caller asked for links |
| `citations` | list of item ids used |
| `trust_summary` | `trusted` or `contains_untrusted_text` |
| `untrusted_quotes` | list, possibly empty |
| `verdict` | `ANSWER`, `ABSTAIN`, or `HOLD_FOR_REVIEW` for lookup tools |
| `block` | true when the injection path must stop an action |

`verdict: ABSTAIN` when no accepted item supports the question.

`verdict: HOLD_FOR_REVIEW` when the matched rule has `authority: unresolved` or when two scopes disagree.

`block: true` when the retrieved text is an injection locator and the proposed action is approve, release, ignore-validation, or close-from-text. See `injection-corpus-design.md`.

Write methods are absent from the lake API. A POST that would change `items` fails the read-time gate.

---

## Minimum lake tools (for Application B and agents)

These four names are the Half A contract. FD-15 may add more later. It may not remove these four.

| Tool | Input | Output |
|---|---|---|
| `search_items` | query string, optional `kind`, optional date | read envelope with FTS5 hits |
| `get_item` | `id` | one item in the envelope |
| `get_links` | `id`, optional `type`, optional depth | items plus edges from the recursive CTE |
| `rule_at` | `rule_id`, `on_date`, `site_code` (canonical). Optional `country_code`, optional `sales_region` | the valid rule row, or `HOLD_FOR_REVIEW` |

`rule_at` uses the mapping in `mapping-design.md`. Site code is the canonical key. If a supplied sales region disagrees with the region derived from the site, the tool returns `HOLD_FOR_REVIEW`.

---

## Hash and pin contract

`generated/manifest.json` holds `sqlite_sha256` and `lake_version`.

Application B (Phase 11) pins that pair. The App-B-build gate fails if the running file hash disagrees with the pin.

The YAML in Git is the source of truth. If SQLite disagrees, rebuild, or write an ADR and raise the version (FD-22).

---

## What this file does not do

This file does not write the schema JSON. It does not name every REST path. It does not write OPA. It does not start Half B.
