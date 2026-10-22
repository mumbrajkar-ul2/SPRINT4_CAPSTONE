# Context Lake architecture

| Field | Value |
|---|---|
| Stage | Architecture note for the built Context Lake. Written after Phase 5. |
| Date / version | 2026-10-21, v1.0 |
| Author / agent | Cursor Grok 4.7 |
| Status | Describes the lake that is on disk at version 1.0.0. Does not change that lake. |
| Evidence sources | `context-lake/build.py`; `context-lake/lake_runtime.py`; `context-lake/rest_server.py`; `context-lake/mcp_server.py`; `context-lake/harvest/`; `context-lake/schemas/`; `context-lake/generated/manifest.json`; `context-lake/generated/app-b-pin.json`; `docs/10-architecture/adrs/adr-lake-yaml-to-sqlite.md`; `docs/11-data-context/knowledge-model.md`; `docs/11-data-context/contract-gates.md`; `apps/app_a/intelligence/retrieve.py`; `apps/app_b/rules/resolver.py` |
| Assumptions | The counts below are the 1.0.0 build recorded in `manifest.json`: 148 items, 180 edges, 267 term rows. The pin hash is the hash in `app-b-pin.json`. |
| Unresolved issues | A later change to an accepted item id still has to go through the review loop and an ADR. This note does not start that loop. |
| Residual risks | Editing `context-lake.sqlite3` by hand would make the file disagree with the YAML in Git and with the pin. |

The Context Lake stores facts about the fab estate. A fact is one rule, one term, one code behavior, one data relationship, one dependency, or one recorded decision. Version 1.0.0 is the copy the apps read.

People and harvest scripts write YAML in Git. `build.py` checks that YAML and writes one SQLite file. The apps open that file read-only. The picture for this page is [context_lake_architecture.drawio](context_lake_architecture.drawio).

The picture has six bands, top to bottom.

1. Authoring. The YAML, the rule cards, the word list, the eval files, and the review notes.
2. Contracts. The JSON schemas and the five gates that reject a bad fact.
3. Build. `build.py`, the only program that writes the SQLite file.
4. Generated store. The SQLite file, its four tables, the build receipt, and the pin.
5. Read path. The read helper and the two listeners, ports 8091 and 8092.
6. Readers. Application A cites the lake. Application B takes its rules from the lake.

Arrows in the picture go from the harvest scripts and the YAML down to `build.py`, from `build.py` down to the SQLite file, from that file to the two listeners, and from the listeners to the two readers. A separate arrow on the right runs from the rule-card files to Application B. Those cards stay YAML. They are not rows in the SQLite file. A second arrow on the right runs from the pin to Application B, because Application B checks that hash before it uses the lake.

---

## Layer 1 — Authoring

This layer is the source people review in Git. `build.py` reads it. The apps do not edit it at run time.

### Harvest scripts

Folder: `context-lake/harvest/`.

`run_harvest.py` calls the four writers in order. It prints how many items, cards, and terms it wrote. It does not copy operational lot rows.

| Script | What it writes |
|---|---|
| `generate_items.py` | One YAML fact per file under `context-lake/items/`. Sources are the policy archive, the schema counts, the four legacy programs, and the locked decisions. |
| `generate_cards.py` | The 25 rule-card files under `context-lake/items/rules/`. |
| `generate_terms.py` | The word-list YAML under `context-lake/semantic-layer/`. |
| `generate_eval.py` | `context-lake/eval/golden-questions.yaml` and `context-lake/eval/injection-corpus.yaml`. |
| `common.py` | Shared paths, the seven kind folders, the source-register hash, and the site map. |

Worked example. `common.py` maps site `IN-BLR` to country `IN` and sales region `APAC`. The item writer and the term writer both use that same map.

### YAML facts

Folder: `context-lake/items/`. One fact per file. The file name matches the item id.

Each file has an id, a kind, a statement, a source path and SHA-256, a claim, a trust label, an owner, a lake version, an item status, a policy status, an honesty label, and a list of links. A business rule also has an authority: `policy_archive`, `sme`, or `unresolved`.

`kind` is one of seven values. The folder name matches the kind.

| Kind | Folder | One file states |
|---|---|---|
| `business_rule` | `items/rules/` | One governed test, or one recorded deviation from it. |
| `domain_knowledge` | `items/domain/` | One fab or workflow fact, such as what OPEN means. |
| `architecture` | `items/architecture/` | One boundary, listener, or store placement. |
| `code_intelligence` | `items/code/` | One function, constant, or module behavior. |
| `data_relationship` | `items/data/` | One schema, key, count, clock, or missing join. |
| `dependency` | `items/dependencies/` | One "this program reads that file or table" fact. |
| `decision` | `items/decisions/` | One recorded choice or conflict. Catalogue rows BP1 through BP8 each have one. |

Item status is `accepted`, `draft`, or `superseded`. Search returns accepted items. One draft file sits in `items/_drafts/data.draft.business_context.yaml`. An accepted file in that folder fails the build.

The 1.0.0 database holds 148 of these facts, including that draft. Rule cards are not part of the 148.

### Rule cards

Files: `context-lake/items/rules/*.card.yaml`. There are 25.

A card is the decision table for one business rule. It names the inputs, the authority, the test cases, and the observed legacy implementations. `build.py` checks that every required card is present. It does not insert the card into SQLite.

Application B loads these files itself and applies the table by card id. A card with authority `unresolved` must send the case to `HOLD_FOR_REVIEW`. The build fails if that route is missing.

### Semantic layer

Folder: `context-lake/semantic-layer/`.

YAML files define the words. Markdown files explain the same words in plain sentences. `status.md` says REVIEW and HOLD count as open, and that finance closed and audit closed stay separate. `region.md` and `recipe.md` explain the region map and the recipe words.

`build.py` reads the YAML and writes the `terms` table. The 1.0.0 build has 267 term rows, because one word can have several local names.

The six site maps are both items and terms: `IN-BLR`, `JP-KN`, `US-TX`, `BR-SP`, `DE-BY`, and `GB-ENG`.

### Eval files

Folder: `context-lake/eval/`.

`golden-questions.yaml` holds 26 questions the lake must answer with a citation. `injection-corpus.yaml` holds text that must come back as a block, not as an order to approve or release a hold.

These files test the lake. They are not rows in the SQLite file. A few injection notes are also stored as facts with ids `data.injection.*` and trust `untrusted_text`. Those facts are quoted back as data.

### Review notes

Folder: `context-lake/review/`.

| File | What it records |
|---|---|
| `lake-review.md` | The review round. Each of the seven kinds has at least one accepted item. |
| `lake-fixes.md` | The numbered fixes from that round, with the text before and after. |
| `lake-version.md` | The lake version, set to 1.0.0. |

A later change runs this loop again. Adding items with the same meaning raises the patch number. Changing the meaning of an id raises the minor number and needs an ADR. Removing an accepted id raises the major number.

---

## Layer 2 — Contracts

This layer says what a legal fact looks like, and what the build and the reads must reject.

### JSON schemas

Folder: `context-lake/schemas/`. Each schema sets `additionalProperties: false`. An extra field fails validation.

| Schema | What it checks |
|---|---|
| `item.schema.json` | One fact. Kind is the seven-value list. A business rule must have `authority`. |
| `link.schema.json` | One link. `type` plus `to`. |
| `rule-card.schema.json` | One rule card. Decision table, tests, and authority are required. |
| `term.schema.json` | One word. Canonical name, definition, and local names. |
| `read-envelope.schema.json` | The packet a read returns: items, citations, trust summary, verdict, and block flag. |

### enums.generated.json

File: `context-lake/schemas/enums.generated.json`.

`build.py` writes this file. Nobody edits it by hand. It lists the closed values: the seven kinds, the claim labels, the trust labels, the authority labels, the status words, the site codes, the country codes, the sales regions, the table names, the column names, and every item id.

`check_claim` in `lake_runtime.py` looks names up in this file. A claim that names `wafer_lots.parent_lot_id` is rejected, because that column is absent.

### The five gates

The gates are specified in `docs/11-data-context/contract-gates.md`. `build.py` enforces write-time and build-time. `check_claim` enforces model-output. The read envelope enforces read-time. `app-b-pin.json` is the artifact the Application B build gate checks. Tests under `context-lake/tests/` rerun these checks: `test_schema.py`, `test_gates.py`, `test_graph.py`, `test_golden.py`, `test_injection.py`, and `test_parity.py`.

| Gate | When it runs | What a reject does |
|---|---|---|
| Write-time | A YAML fact, term, or card is added or changed. | The file stays out of the accepted set. `build.py` does not copy it into SQLite. |
| Build-time | Every `build.py` run. | `build.py` exits with an error. It does not leave a new receipt. |
| Model-output | A draft or an agent answer names a table, column, id, status word, site, or rule. | The draft stays in `_drafts/`, or the answer verdict is `ABSTAIN`. |
| Read-time | Each call on port 8091 or port 8092. | A bad request is rejected. A normal miss returns `ABSTAIN`. Untrusted text is listed in `untrusted_quotes`. |
| Application B build | Before Application B uses a lake build. | Application B refuses to start when the SQLite hash disagrees with the pin. |

Write-time rejects an extra field, a kind outside the seven, a link type outside the eight, a business rule with no authority, a raw lot id in the statement, and instruction words such as "approve" inside a trusted statement.

Build-time rejects a duplicate id, a link to a missing id, a source hash that disagrees with `sources/register.yaml`, a missing kind, a missing BP1–BP8 decision, a missing rule card, and a missing site map.

Read-time opens the SQLite file with `mode=ro`. A write on the listener is rejected. `rule_at` that finds silence, overlap, an invalid interval, or a site and region that disagree returns `HOLD_FOR_REVIEW`. That return is a successful read.

---

## Layer 3 — Build

### build.py

File: `context-lake/build.py`.

This is the only writer of `context-lake/generated/context-lake.sqlite3`. It reads item YAML, skips `*.card.yaml` for the database insert, checks those cards, reads the semantic-layer YAML, and then writes the file.

Before it writes, it checks all of the following.

- The JSON schemas pass.
- The file name matches the item id.
- Inherited source hashes match `sources/register.yaml`.
- A locator names a column that exists.
- Each of the seven kinds has an accepted item.
- Each of `decision.bp1` through `decision.bp8` exists.
- Each of the 25 required rule cards exists.
- Each of the six site maps exists as an item and as a term.
- Every link target exists.
- The statement does not look like a raw lot id (`L000000` plus two digits).
- A canonical decision table does not use 999,999 as a live limit.
- The Python 50,000 cutoff is not marked `decided`.

It then creates the tables, fills them, builds the full-text index, and writes `enums.generated.json`, `manifest.json`, and `app-b-pin.json`. If the full-text index is empty while items exist, the build fails.

---

## Layer 4 — Generated store

This layer is what the apps open. Git YAML remains the source. If the SQLite file disagrees with the YAML, fix the YAML and run `build.py` again, or record an ADR.

### context-lake.sqlite3

File: `context-lake/generated/context-lake.sqlite3`.

One SQLite file. Version 1.0.0. The hash in the pin is `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`.

### items

One row per YAML fact. Columns are the fact fields: id, kind, statement, source path, source lines, source hash, locator, valid-from, valid-to, recorded date, claim, trust, authority, owner, lake version, item status, policy status, honesty, supersedes, reviewer, and reviewed date.

`valid_from` and `valid_to` are the dates the fact applied in the business. `recorded_at` is the date the lake learned it.

### edges

The knowledge graph is this table. Columns are `from_id`, `type`, and `to_id`. The three together are unique. The 1.0.0 build has 180 rows. `get_links` walks them and stops at depth 6.

Each row comes from a `links` entry on a fact. Eight types are allowed.

| Type | Meaning |
|---|---|
| `implements` | Code carries out a rule. |
| `conflicts_with` | Two facts disagree. |
| `supersedes` | A later fact replaces an earlier one. |
| `governs` | A decision or archive row governs a rule. |
| `evidenced_by` | A count or a file supports a statement. |
| `depends_on` | A program reads a file or a table. |
| `maps_to` | A local term maps to a canonical term. |
| `tested_by` | A test or a card case locks a fact. |

### terms

One row per local name of a canonical word. Columns are term id, canonical name, definition, local system, local name, maps-to term, claim, authority, source path, and policy status. The 1.0.0 build has 267 rows.

### items_fts

A full-text index on item id and statement. `search_items` matches words here, then joins back to `items`, and keeps accepted rows. The default limit is 20.

### manifest.json

File: `context-lake/generated/manifest.json`.

The build receipt. It records lake version `1.0.0`, the build time, item count 148, edge count 180, term count 267, the SQLite hash, the source-register hash, and the correlation id.

### app-b-pin.json

File: `context-lake/generated/app-b-pin.json`.

The pin Application B must match. It records lake version `1.0.0`, the SQLite hash, the enum-file hash, and the list of canonical rule-card ids. `apps/app_b/rules/resolver.py` hashes the SQLite file at start. If the hash disagrees, Application B stops.

---

## Layer 5 — Read path

Reads go through `lake_runtime.py`. The two listeners call that helper. They do not open a second database.

### lake_runtime.py

File: `context-lake/lake_runtime.py`.

It opens the SQLite file with `mode=ro`. It loads `enums.generated.json`. It checks every returned packet against `read-envelope.schema.json`.

Four reads:

| Read | What it returns |
|---|---|
| `search_items` | Accepted facts whose statement matches the words. Optional kind filter. Default limit 20. |
| `get_item` | One fact by id. A missing id or a hidden draft returns verdict `ABSTAIN`. |
| `get_links` | Links from that id, walked up to depth 6. |
| `rule_at` | The rule that applied on a date, for a site, a country, or a sales region. |

A packet lists the items, the edges, the citation ids, a trust summary, any untrusted quotes, a verdict, and a block flag. Trust `untrusted_text` is copied into `untrusted_quotes`.

`check_claim` is the model-output gate. It rejects an unknown table, column, item id, status word, site, country, or sales region.

### Lake REST

File: `context-lake/rest_server.py`. Port 8091.

| Route | Read |
|---|---|
| `GET /health` | Ready check. |
| `GET /v1/version` | Version, hash, and item count from the manifest. |
| `GET /v1/items` | `search_items`. |
| `GET /v1/items/{item_id}` | `get_item`. Unknown id returns 404. |
| `GET /v1/items/{item_id}/links` | `get_links`. |
| `GET /v1/rules/at` | `rule_at`. |

A write to this listener is rejected.

### Lake MCP

File: `context-lake/mcp_server.py`. Port 8092.

The same four reads are tools: `search_items`, `get_item`, `get_links`, and `rule_at`. `GET /health` and `GET /v1/tools` list them. `POST /v1/tools/{tool_name}` runs one tool. A tool name outside those four is rejected. A write that would change items is rejected.

---

## Layer 6 — Readers

These two apps are outside the lake folder. They are the programs that open it. They do not call each other.

### Application A

Code: `apps/app_a/intelligence/retrieve.py`. The agent tools in `apps/app_a/agent/tools.py` call the same four reads.

Application A uses the lake for citations. Pass or fail stays in Application A's own transformed code. By default the retrieve path calls `lake_runtime` in process. If `LAKE_REST_URL` is set, it calls port 8091 instead.

### Application B

Code: `apps/app_b/rules/resolver.py`.

Application B takes its rules from the lake. It checks `app-b-pin.json` against the SQLite hash. It loads the rule-card YAML from `context-lake/items/rules/`. It calls `lake_runtime` for items, links, search, and `rule_at`. It does not import the four legacy rule programs.

---

## Worked example

The 2023 EMEA recipe-release limit shows every layer on one fact.

The governed archive says the limit is 18,600 USD from 2023-01-01 through 2023-12-31. The harvest script writes that as YAML item `rule.recipe_release.limit.v2023.emea` under `context-lake/items/rules/`. Kind is `business_rule`. Authority is `policy_archive`. The source path is the archive JSON. The source hash is the hash in the register.

`item.schema.json` accepts that shape. Write-time passes because the authority is present and the statement is one limit, not a lot row.

`build.py` inserts one row in `items` with `valid_from` 2023-01-01 and `valid_to` 2023-12-31. The matching rule card `rule.recipe_release.limit.card.yaml` stays on disk. It is not that row.

A `rule_at` call for that rule id, on date 2023-07-01, with sales region EMEA, returns that row. The same call on 2026-07-01 returns the 2026 EMEA row, 26,100 USD, because that row's dates cover 2026. The 2023 row is still in the file for a historical question.

Application A can cite the item id. Application B applies the card and the dated row. If the opened SQLite hash differs from the pin, Application B does not answer.
