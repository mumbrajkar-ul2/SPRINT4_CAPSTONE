# Five relationship answers

| Field | Value |
|---|---|
| Stage | Phase 18 / DEV-018. |
| Date / version | 2026-10-19, v1.0 |
| Author / agent | Executor agent (Grok 4.7), correlation id corr-p18b-doc-20261019-001 |
| Status | CLOSED from the `edges` table at lake version 1.0.0. |
| Evidence sources | `context-lake/generated/context-lake.sqlite3` table `edges` |
| Assumptions | An answer cites an edge that is in that table. |
| Unresolved issues | No edge has a lot id on one end and a recipe revision id on the other. |
| Residual risks | Treating two separate edges as one join would invent a relationship the table does not store. |

1. Lots on a recipe revision. `domain.object.lot` maps_to `term.lot`. `data.join.recipe_mismatch` conflicts_with `term.recipe_revision_dispatch`. Those are two edges. The table does not store one edge from a lot to a recipe revision.

2. Tools and metrology for an excursion. `rule.clock.event_vs_arrival` evidenced_by `data.clock.event_vs_arrival_evidence`. That edge is the tool-alarm clock evidence. `term.tool` and `term.metrology_sample` are definitions in the terms table. The edges table does not join those two terms to an excursion id.

3. The policy in force at event time. `rule.recipe_release.limit.v2023.emea` maps_to `term.sales_region`. The rule item names the window `2023-01-01` through `2023-12-31`.

4. The documents and code for that policy. `code.legacy_policy.js_allow` depends_on `data.contract.decision_policies_archive`. `code.legacy_policy.js_allow` implements `rule.recipe_release.limit`. `rule.recipe_release.limit.v2023.emea` is tested_by `test.rule.recipe_release.emea_2023`.

5. The changes that affect a workflow. `rule.recipe_release.limit.v2023.emea` supersedes `rule.recipe_release.limit.v2022.emea`.
