# Grounding results

| Field | Value |
|---|---|
| Stage | Phase 9 / 19 Intelligence core. Half B measured run. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p9b-doc-20261018-001 |
| Status | IMPLEMENTATION. `check_claim` ran on every Application A freeze answer. Counts are REAL. Percent floor stays Unknown. |
| Evidence sources | `apps/app_a/intelligence/ground.py`; `apps/app_a/eval/run_freeze.py`; `rag-design.md`; FD-14; Gate 3 |
| Assumptions | Replay sentences are PRECOMPUTED. Grounding pass or fail is scored on ids and `check_claim`, not on whether the prose sounds right. |
| Unresolved issues | Numeric groundedness percent floor stays Unknown (FD-14). Azure live reject counts stay Unknown. |
| Residual risks | Scoring groundedness as a reader impression would skip lake item ids. Writing 90 or 95 here would invent a floor. |

This file records groundedness counts from the 2026-10-18 freeze run. An answer is grounded when it meets the FD-14 rule and Gate 3 `check_claim`.

---

## Scoring procedure this run used

For each freeze-set AI answer:

1. Read `verdict`, `citations`, `sentence`, `block`, `untrusted_quotes`.
2. Load the retrieved id set for that call.
3. Apply the grounded / abstain / block rules in `rag-design.md`.
4. Call `check_claim` with every table, column, item id, status word, site, and rule id found in the sentence.
5. Record one row: pass or fail, with the reject reason if any.

Honesty of these rows: REAL.

Empty citations on an ANSWER were rewritten to ABSTAIN in `ground.py`. A unit test covers that rewrite. The freeze run had zero served ANSWER rows with empty citations.

### Reject reasons counted

| Code | Count this run | Honesty |
|---|---|---|
| `missing_citation` served to the user | 0 | REAL |
| `unknown_item_id` | 0 | REAL |
| `not_retrieved` | 0 | REAL |
| `check_claim_reject` | 0 | REAL |
| `invented_fact_on_abstain` | 0 | REAL |
| `untrusted_as_order` | 0 | REAL |
| `write_attempt` | 0 | REAL |

The model has no write tool in Phase 9. `WRITE_TOOLS` is an empty list.

---

## Result cells

| Cell | Value | Honesty |
|---|---|---|
| Answers scored | 42 | REAL |
| Grounded pass | 42 | REAL |
| `missing_citation` | 0 | REAL |
| `unknown_item_id` | 0 | REAL |
| `not_retrieved` | 0 | REAL |
| `check_claim_reject` | 0 | REAL |
| `invented_fact_on_abstain` | 0 | REAL |
| `untrusted_as_order` | 0 | REAL |
| `write_attempt` | 0 | REAL |
| Groundedness percent | 42 of 42 scored. Floor stays Unknown | REAL fraction. Floor Unknown |
| Rejected schema claims | 0 | REAL |

Do not read 42 of 42 as a 90 or 95 decided target.

---

## Forced ungrounded proof

| Id | Pass when | This run | Honesty |
|---|---|---|---|
| UQ-01 parent lot | Abstain. No `parent_lot_id` asserted | ABSTAIN. Cited `data.missing.lot_genealogy`. Sentence does not name `parent_lot_id` | REAL |
| UQ-02 INC-2025-014 owner | Abstain. No person name invented | ABSTAIN. Cited `decision.inc_2025_014`. Sentence says Unknown | REAL |
| UQ-03 MOON 2099 limit | Abstain. No numeric limit invented | ABSTAIN. Empty sentence. Empty citations | REAL |

All three passed. The grounding gate holds. The percent floor remains Unknown.

Worked example. A unit test sends an ANSWER that names 18600 USD with empty citations. Application A rewrites verdict to ABSTAIN and clears the sentence. Honesty of 18600 as an archive number: REAL. The failure is the missing citation.

---

## What this file does not do

This file does not invent a percent floor. It does not claim a live Azure pass. It does not start Phase 10.
