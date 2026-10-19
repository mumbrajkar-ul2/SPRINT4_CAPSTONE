# Retrieval pipeline

| Field | Value |
|---|---|
| Stage | Phase 9 / 19 Intelligence core. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p9a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/11-data-context/retrieval-strategy.md`; `docs/12-specs/api-contracts.md` API-L-03 to API-L-06; `docs/11-data-context/contract-gates.md`; `context-lake/eval/golden-questions.yaml`; FD-04; FD-14 |
| Assumptions | Lake REST on 8091 already serves the four read routes. Application A on 8100 calls that listener with `X-Api-Key`. FTS5 word search plus SQL filters plus recursive edges remain the search method. A vector index waits on a failed golden question plus an ADR. |
| Unresolved issues | Retrieval p95 stays Unknown. Default `search_items` limit 20 is the Phase 5 engineering default. Whether FTS5 misses a paraphrase of GQ-25 stays Unknown until Half B runs the freeze set. |
| Residual risks | Using lake `rule_at` as Application A's pass-or-fail result would take rules from the lake. Ranking cases with FTS5 on the note field would use untrusted text for triage. |

This file names how Application A finds lake items for citations. Application A still evaluates rules from its transformed code. The lake is the citation and retrieval store.

Engineering decision ED-P9A-03, authority: team-force. The Application A retrieval steps and the cite-then-generate order below.

---

## Finding

**Finding.** Application A retrieval is a code pipeline of four lake reads, a trust filter, `check_claim`, and then the model. The model does not search. The model does not decide pass or fail.
**Evidence.** Retrieval strategy four tools. FD-04. API-L-03 to API-L-06. Gate 3 `check_claim`.
**Impact.** Half B can implement `apps/app_a/intelligence/retrieve.py` against port 8091 without a vector database.
**Risk.** Calling `rule_at` and then skipping `evaluate_live_policy` would make Application A a second copy of Application B.
**Confidence.** High on the tool list. Unknown on FTS5 recall until the freeze set runs.
**Open questions.** Paraphrase miss rate. Retrieval p95.

---

## Rule-source split at retrieval time

**Verified Fact.** `decision.fd06.two_apps`. Phase 9 locked fact.

| Question | Where Application A gets the answer |
|---|---|
| Is this feed a duplicate candidate? | Transformed `reconcile_feeds` / REPLAY test |
| What is the queue order? | Transformed `priority()` |
| What live `recipe_release` limit applies, or must we wait? | Transformed `evaluate_live_policy` |
| Which lake item ids may the model cite? | Lake REST on 8091 |

Worked example. GQ-02 asks the 2026 APAC limit. Application A pass-or-fail still comes from `evaluate_live_policy('APAC', 2026)`, which returned limit 25,000 USD in Phase 7. Honesty: REAL. Retrieval still loads `rule.recipe_release.limit.v2026.apac` so the sentence can cite that id.

If the lake is down, ranking and live-policy evaluation still run. The explanation and query paths abstain.

---

## Steps

Half B implements these steps in order. Do not generate before retrieve. Do not skip `check_claim`.

1. Read identity headers. Reject missing identity with HTTP 401. See `access-control-implementation.md`.
2. Treat the user question and every harvested note as data.
3. If the job is ranking, duplicate, or pass-or-fail, run transformed code and stop. Do not call the model.
4. If the job is explanation, query, or draft plan, call lake REST.
5. Filter to `item_status: accepted` unless the caller asked for a named draft, which Phase 9 does not.
6. Copy `trust: untrusted_text` strings only into `untrusted_quotes`.
7. If the implied action is approve, release, ignore-validation, or close-from-text, and an injection locator is present, set `block: true` and do not offer a write.
8. If no accepted item supports the question, set `verdict: ABSTAIN` and skip the model, or call the model only to format the abstain that cites a missing-data item.
9. Build the canonical prompt from the versioned file plus retrieved ids.
10. Obtain a model response from replay or, later, Azure.
11. Run `check_claim` on claimed tables, columns, item ids, status words, and rule ids.
12. If `check_claim` rejects, replace the answer with `verdict: ABSTAIN`.
13. Return SCH-09.

Worked example. A query "which column stores the parent lot" retrieves `data.missing.lot_genealogy`. Step 8 sets ABSTAIN. `check_claim` would also reject `wafer_lots.parent_lot_id`. The user sees an abstain, not a guessed parent.

---

## Lake calls Application A may make

**Verified Fact.** API-L-03 to API-L-06. Identity on the lake is `X-Api-Key` except health (ED-P8A-04).

| Tool | Path | What Application A uses it for |
|---|---|---|
| `search_items` | `GET /v1/items?q=&kind=&on_date=` | Word match for GQ and case explanation |
| `get_item` | `GET /v1/items/{id}` | Confirm one citation id exists |
| `get_links` | `GET /v1/items/{id}/links` | Related evidence. Lineage view stays Application B |
| `rule_at` | `GET /v1/rules/at` | Citation for the archive row that matches a date and site. Not the Application A pass-or-fail result |

Default `search_items` limit is 20. **Verified Fact** of the Phase 5 engineering default. It is not a business threshold.

Application A does not POST to 8091. A lake write is `error_class: lake_write_rejected`, HTTP 405.

---

## Per-scenario retrieval targets

These ids are the citation targets Half B must retrieve for scenarios 7 to 11. Expected verdicts follow the golden-question file and the acceptance criteria.

| Scenario | Retrieval must return at least | Expected model verdict on the happy path |
|---|---|---|
| 7 Replay | `rule.feed.replay_duplicate`, `data.feed.replay` | ANSWER. Drop still waits for RT-05 |
| 8 Recipe mismatch | `rule.recipe.mismatch_show_both`, `data.join.recipe_mismatch` | ANSWER. Hold still waits for RT-03 |
| 9 Two clocks | `rule.clock.event_vs_arrival`, `data.clock.event_vs_arrival_evidence` | ANSWER for the two fields. A signed cut-off question is HOLD_FOR_REVIEW |
| 10 Policy overlap | `rule.policy.overlap_or_invalid`, `data.policy_register.overlap` | HOLD_FOR_REVIEW. Model does not pick the policy |
| 11 Outage or missing owner | `term.outage` or `decision.inc_2025_014` | ANSWER for retry status. ABSTAIN for the INC-2025-014 owner until a person assigns one |

Ungrounded control: GQ-19 and GQ-22 must abstain. A question with no lake hit must abstain.

---

## Trust and injection

**Verified Fact.** `rule.untrusted_text.block`. Retrieval strategy trust table.

| Item trust | Pipeline action |
|---|---|
| `trusted_code` | May use `statement` as a fact about code |
| `trusted_record` | May use `statement` as a fact about a governed file or a count |
| `untrusted_text` | Quote only in `untrusted_quotes`. Never rank. Never pass a rule. Never approve |

86 partner feeds carry auto-approve or disregard-validation language. Honesty: REAL. Those strings stay data.

---

## What retrieval does not do

Retrieval does not rank the queue.

Retrieval does not mark a duplicate.

Retrieval does not write `engineering_hold`.

Retrieval does not replace `evaluate_live_policy`.

Retrieval does not search raw `partner_feeds.raw_json` as the lake. It searches the knowledge item that locates those rows.

---

## What this file does not do

This file does not write `retrieve.py`. It does not add embeddings. It does not start Half B.
