# Graph questions

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/10-architecture/adrs/adr-knowledge-graph-edges-table.md`; `Project_Intent.md` section 9.3; FR-15; `knowledge-model.md` link types; catalogue BP1 to BP8 |
| Assumptions | Recursive SQL on the `edges` table answers these questions. A graph database is not used. Live case status stays in the operational store. The graph holds knowledge about rules, code, terms, and decisions. |
| Unresolved issues | Edge counts are Unknown until Half B. Recursion depth default is specified here as 6. FD-15 may cap agent walks later. |
| Residual risks | Walking `relates_to` from `cross_references` would copy a weak operational type into the lake. Drawing lot parent links would claim genealogy the tables do not have. |

This file lists the questions Half B recursive queries must answer. Each question names the start item, the link types, and the expected kind of result. Half B writes one test per question.

---

## Finding

**Finding.** Twelve graph questions cover lineage, impact, mapping, tests, and the four-implementation trace. They stay inside knowledge items.
**Evidence.** Phase 4 ADR worked example for scenario 12. FR-15. Eight link types in `knowledge-model.md`.
**Impact.** Half B can write CTEs without inventing a question. Application B scenario 12 uses GQ-G01.
**Risk.** Starting a walk on a live `object_id` would mix operational state into the graph.
**Confidence.** High on the question list. Unknown on edge count.
**Open questions.** Whether depth 6 is enough after harvest. If a golden question fails at depth 6, raise depth through the lake loop, do not add Neo4j.

---

## Store

**Verified Fact.** Edges table columns: `from_id`, `type`, `to_id`. Unique on the three together.

Default walk: recursive CTE, `depth <= 6`, types taken from the question. Cycles stop when a visited `(from_id, type, to_id)` repeats.

---

## Questions the CTEs must answer

### GQ-G01 Which programs implement this rule, and which test locks it?

Start: `rule.recipe_release.limit`.

Walk: `implements` (incoming), `tested_by` (outgoing), `conflicts_with` (outgoing).

Expect: four implementation items (Python, JavaScript, Java, night batch) plus at least one test item. This is scenario 12.

### GQ-G02 Which decision made the archive canonical?

Start: `rule.recipe_release.limit`.

Walk: `governs` (incoming).

Expect: `decision.fd08.canonical_archive` and `decision.bo05.recipe_authority`.

### GQ-G03 What conflicts with the recipe-revision claim that dispatch and equipment agree?

Start: `data.join.recipe_mismatch`.

Walk: `conflicts_with`, `evidenced_by`.

Expect: the two column items `term.recipe_revision_dispatch` and `term.recipe_revision_equipment`, and the BP1 decision item. Count 91 of 125 is on the evidence item. Honesty: REAL.

### GQ-G04 What did this archive version supersede?

Start: `rule.recipe_release.limit.v2026.apac`.

Walk: `supersedes` (outgoing), repeated.

Expect: the 2025, 2024, 2023, and 2022 APAC limit items in that order. `rule_at` still uses `valid_time`, not this walk, to pick the row for a date.

### GQ-G05 What depends on the archive JSON file?

Start: `data.contract.decision_policies_archive`.

Walk: `depends_on` (incoming).

Expect: `code.legacy_policy.js_allow` at minimum. Python priority does not read the JSON. That absence is a fact on the Python code item.

### GQ-G06 How does each system read "open"?

Start: `term.open_operational`.

Walk: `maps_to` both ways.

Expect: local words REVIEW, HOLD, UNDER_REVIEW, OPEN, ESCALATED, REOPENED, QUEUED, PROCESSING, ENGINEERING_REVIEW. Night-batch flag item sits on this term through `implements` or `maps_to`.

### GQ-G07 If the 2026 APAC limit changes, what else is linked?

Start: `rule.recipe_release.limit.v2026.apac`.

Walk: `implements`, `tested_by`, `depends_on`, `governs`, `maps_to`, depth 3.

Expect: JS implementation, RC-01 tests, FD-08 decision, APAC sales-region term. This is impact, not a live write.

### GQ-G08 Site to country to sales region to archive family

Start: `map.site.IN-BLR`.

Walk: `maps_to`.

Expect: country IN, sales region APAC, then `rule.recipe_release.limit` as the family those terms serve. The walk does not pick 25,000 by itself. `rule_at` does that with `valid_time`.

### GQ-G09 Untrusted-text locators linked to the BLOCK rule

Start: `rule.untrusted_text.block`.

Walk: `evidenced_by`.

Expect: one evidence item per injection store in `injection-corpus-design.md` (feeds, bundled events, emails, source documents, HTML, evidence payload).

### GQ-G10 Missing genealogy

Start: `term.lot_genealogy`.

Walk: `conflicts_with`, `evidenced_by`.

Expect: `data.missing.lot_genealogy`. No edge to a parent-lot item. A test fails if such an edge appears.

### GQ-G11 Recovery decision with unknown owner

Start: `decision.inc_2025_014`.

Walk: `evidenced_by`.

Expect: the incident file item. Owner field `unknown`. No invented person node.

### GQ-G12 Night-batch join versus canonical overlap rule

Start: `rule.night_batch.join_multiply`.

Walk: `conflicts_with`, `implements`.

Expect: `rule.policy.overlap_or_invalid` (RC-03) on `conflicts_with`. The REVIEW-flag item `rule.open_flag.impl.night_batch` does not conflict with RC-09. That match is a `maps_to` or `implements` edge, not `conflicts_with`.

---

## Questions the graph must not answer

| Question | Why it stays out | Label |
|---|---|---|
| What is the live status of object FAB-00000012 | Operational store | Verified Fact of the ADR boundary |
| Which parent lot produced this lot | No parent column | Verified Fact |
| What is exception cycle time for case C00000001 | No close-time column | Unknown |
| Which company job title maps to RT-03 | Unmapped | Unknown |

---

## Half B tests

One pytest per GQ-G01 to GQ-G12. Each test runs the CTE and checks the expected ids. Test output is REAL.

---

## What this file does not do

This file does not write SQL. It does not create edges. It does not start Half B.
