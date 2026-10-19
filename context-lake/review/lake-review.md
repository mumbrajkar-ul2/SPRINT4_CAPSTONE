# Lake review — round 1

| Field | Value |
|---|---|
| Stage | Phase 5 / 11R Review, fix, and revision loop. Half B. |
| Date / version | 2026-10-18, v1.0.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5b-doc-20261018-001 |
| Status | REVIEW COMPLETE. One round. Fixes applied. Version set to 1.0.0. |
| Evidence sources | `context-lake/` after harvest and `build.py`; pytest on 2026-10-18; `docs/11-data-context/` Half A files; read-only SQLite counts |
| Assumptions | Harvested YAML that cites a source file may be accepted. A model-drafted sentence stays draft. This review is the 11R loop, not the coordinator reviewer gate. |
| Unresolved issues | Named reviewer for model-drafted items is Unknown. BO-06b and BO-08 stay PROPOSED. A language-model paraphrase of a golden question was not scored. |
| Residual risks | A later edit of YAML without `build.py` would leave SQLite stale. Serving a draft item as current would hide the draft flag. |

This file records the first review of the built lake. The lake stores facts about the estate. It does not copy lot rows or case rows.

---

## What was reviewed

148 YAML items. 25 rule cards. 38 semantic-layer terms. 26 golden questions. 7 injection rows. `generated/context-lake.sqlite3` with 148 items, 180 edges, and 267 term rows. FTS5 table `items_fts` is populated.

Honesty on those counts: REAL from `build.py` and pytest.

---

## Checks that passed

Every required item id from `knowledge-model.md` is present.

Each of the seven kinds has at least one accepted item.

BP1 through BP8 each have a decision item.

Each of the 25 cards has an `authority` label and tests.

Site maps `map.site.IN-BLR` through `map.site.GB-ENG` exist as items and as terms.

`rule_at` for EMEA on 2023-07-01 returns 18600 USD. `rule_at` for APAC on 2026-06-01 returns 25000 USD. Honesty: REAL.

Site IN-BLR with stored sales region AMER returns HOLD_FOR_REVIEW. Country AU with no site returns HOLD_FOR_REVIEW. Country ZA has the same wait.

Python 50000 is labelled proposed. 999999 is not a live policy number.

The draft item `data.draft.business_context` stays draft. `get_item` without a draft flag returns ABSTAIN.

All six injection stores plus the tiny set return `block: true`. No test writes `cases.status`, `wafer_lots.engineering_hold`, or `partner_feeds.processing_status`.

Graph walks GQ-G01 through GQ-G12 return the expected ids. There is no parent-lot edge.

Spot-check of statements: counts and schema facts only. No pasted `wafer_lots` row.

---

## Findings that needed a fix

See `lake-fixes.md` for before-and-after text.

1. The item id pattern in the schema used only lowercase letters. Locked ids such as `map.site.IN-BLR` use uppercase site codes.
2. The first write-time check treated the words approve and release as an order even when the sentence said BLOCK or "does not approve".
3. Card `rule.threshold.demo_50000` had `authority: unresolved` and no HOLD_FOR_REVIEW row. The card contract requires that row.
4. Injection row IC-06 had no measured count. Half A left that count Unknown.
5. `build.py` used `jsonschema.RefResolver`, which this Python install marks deprecated.
6. Two probe scripts sat under `harvest/`. They are not harvest outputs.

---

## What this review does not do

This review does not mark the model-drafted business-context item accepted. The reviewer name is Unknown.

This review does not sign BO-06b or BO-08.

This review does not score a language-model sentence. Golden-question tests check retrieval, citations, and verdict only.

This review does not start Phase 6.
