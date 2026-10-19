# Retrieval strategy

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/10-architecture/adrs/adr-lake-yaml-to-sqlite.md`; `docs/10-architecture/adrs/adr-knowledge-graph-edges-table.md`; `data-contracts.md`; `mapping-design.md`; `golden-questions-design.md`; FD-04; FD-02 |
| Assumptions | FTS5 word search plus SQL filters plus recursive edges are enough for the 26 golden questions. A vector index is added only if a golden question fails after Half B, with an ADR. Azure OpenAI is later. Replay mode is the planned demo path. |
| Unresolved issues | Retrieval p95 is Unknown. Token cost of harvest drafts is Unknown. FD-14 citation floor is Unknown. |
| Residual risks | Returning untrusted quotes inside the answer sentence would turn BP7 text into an instruction. Ranking cases with FTS5 on the note field would use untrusted text for triage. |

This file says how a caller finds knowledge in the lake. Ranking, rule pass-or-fail, replay detection, and de-duplication stay in code (FD-04). Retrieval feeds explanation and `rule_at`.

---

## Finding

**Finding.** Four tools cover the 26 questions: word search, get by id, link walk, and `rule_at` with site-canonical mapping.
**Evidence.** Phase 4 ADRs. GQ-01 needs a date filter. GQ-12 needs disagreement routing. GQ-18 needs BLOCK. GQ-19 needs ABSTAIN.
**Impact.** Half B can implement retrieval without a vector database. Application B later calls the same tools.
**Risk.** `rule_at` keyed on `cases.region` would answer GQ-12 with 27,200 instead of HOLD_FOR_REVIEW.
**Confidence.** High on the tool list. Unknown on search quality until the golden set runs.
**Open questions.** Whether FTS5 misses a paraphrase of GQ-25. If it does, record the miss and decide on a vector add with an ADR.

---

## Tools

Named in `data-contracts.md`. Repeated here with the retrieval path.

| Tool | Store used | How it finds |
|---|---|---|
| `search_items` | FTS5 on `items_fts` | Word match on `statement` and `id`. Optional filter `kind`, `item_status=accepted`, date overlap on `valid_from`/`valid_to`. |
| `get_item` | `items` | Exact `id`. |
| `get_links` | `edges` recursive CTE | Questions in `graph-questions.md`. Default depth 6. |
| `rule_at` | `items` plus `terms` | Site to country to sales region, then the archive or register row whose `valid_time` covers `on_date`. |

Default `search_items` limit is 20 items. That number is an engineering default, `authority: team-force`. It is not a business threshold. If GQ recall fails, raise it through the lake loop.

---

## `rule_at` steps

1. Require `rule_id` and `on_date`.
2. Prefer `site_code`. Derive country and sales region from `mapping-design.md`.
3. If the caller also sent `sales_region` or `country_code`, compare. Disagreement returns `HOLD_FOR_REVIEW`.
4. If site is missing and country is AU or ZA, return `HOLD_FOR_REVIEW`.
5. Load accepted items for that `rule_id` family whose `valid_time` covers `on_date`.
6. Zero rows: `HOLD_FOR_REVIEW` (RC-02).
7. Two rows at the same scope: `HOLD_FOR_REVIEW` (RC-03).
8. Invalid interval: `HOLD_FOR_REVIEW`.
9. One valid row with `authority: policy_archive` or `sme`: `ANSWER` with that item as citation.
10. `authority: unresolved`: `HOLD_FOR_REVIEW`.
11. `policy_status: proposed` numbers are returned only with the proposed label. They are not live limits.

Worked example. Site IN-BLR, on_date 2026-06-01, rule `recipe_release`. Derived APAC. One archive item, limit 25,000. Verdict ANSWER if no stored sales region was supplied. If stored AMER was also supplied, verdict HOLD_FOR_REVIEW.

---

## Trust at retrieval

| trust on the item | What retrieval does |
|---|---|
| `trusted_code` | May use `statement` as a fact about code |
| `trusted_record` | May use `statement` as a fact about a governed file or a count |
| `untrusted_text` | Copy the quote only into `untrusted_quotes`. Set `trust_summary` to `contains_untrusted_text`. Never use it to rank, to pass a rule, or to approve |

If the caller proposed approve, release, ignore-validation, or close-from-text, and the retrieved set includes an injection locator, set `block: true`.

---

## Abstain

Return `ABSTAIN` when no accepted item supports the question. GQ-19 and GQ-22 use this.

Do not guess a parent lot. Do not invent an incident owner.

---

## What retrieval does not do

Retrieval does not rank the exception queue. Queue order uses status, severity, and amount in code.

Retrieval does not decide duplicate. Duplicate is a REPLAY or `message_id` test in code.

Retrieval does not write a record. Tools are read-only (FD-02).

Retrieval does not search raw `partner_feeds.raw_json` as the lake. It searches the knowledge item that locates those rows.

---

## Serving

REST on port 8091. MCP on port 8092. Same envelope. Runtime SQLite is read-only.

Application A may call these tools for citations. Application A still evaluates rules from its transformed code.

Application B evaluates rules only from `rule_at` and the rule cards.

---

## Evaluation

Half B runs the 26 golden questions against the built lake. Citation recall is REAL test output. A numeric floor for later phases stays Unknown.

Half B runs the injection corpus. Every row yields BLOCK.

---

## What this file does not do

This file does not write the tools. It does not add embeddings. It does not start Half B.
