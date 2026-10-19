# RAG design

| Field | Value |
|---|---|
| Stage | Phase 9 / 19 Intelligence core. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p9a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/11-data-context/retrieval-strategy.md`; `docs/11-data-context/knowledge-model.md`; `docs/11-data-context/contract-gates.md` Gate 3; `docs/12-specs/schema-specifications.md` SCH-05 and SCH-09; FD-14; FD-04 |
| Assumptions | Lake 1.0.0 pin holds. FTS5 is enough until a freeze-set miss forces an ADR. The model never sees a write tool in this phase. |
| Unresolved issues | Numeric groundedness, citation, and abstention percent floors stay Unknown (FD-14). Vector index stays off unless a golden question fails. |
| Residual risks | Generating a sentence before retrieval would let the model guess an id. Treating lake items as Application A rules would hide a missing transform. |

This file names how retrieval-augmented generation works in Application A. RAG here means: code retrieves lake items, then a model drafts a sentence that may use only those items. Application A still takes pass-or-fail from transformed code.

Engineering decision ED-P9A-04, authority: team-force. The grounding rule Half B implements is the FD-14 behaviour: every AI answer cites a lake item id or abstains. No percent is added.

---

## Finding

**Finding.** Application A generation is retrieve-then-generate with a post-check. An answer is grounded when every cited id exists in the retrieved accepted set and `check_claim` accepts. An ungrounded attempt becomes ABSTAIN.
**Evidence.** FD-14. Gate 3 reject list. SCH-09. AC-CITE.
**Impact.** Half B can score an answer without inventing a 90 or 95 percent cutoff.
**Risk.** Recording "pass if groundedness is 95 percent" would invent a floor FD-14 left Unknown.
**Confidence.** High on the behaviour. Unknown on measured percents until Half B.
**Open questions.** Measured recall, precision, groundedness, and abstention percents.

---

## Grounding rule Half B must implement

**Verified Fact.** FD-14. Authority: team-force.

Every AI answer cites a lake item id or abstains.

That sentence is the whole decided quality rule for this phase. Numeric groundedness, citation, and abstention percent floors stay Unknown until a measured run. Do not write 90, 95, or any other cutoff as a decided target.

### Grounded ANSWER

All of these are true:

1. `verdict` is `ANSWER`.
2. `citations` contains at least one lake item id.
3. Every id in `citations` exists in lake 1.0.0 (or the pinned later version) with `item_status: accepted`, or is a missing-data item used to explain an abstain.
4. Every id in `citations` was present in the retrieved set for this call.
5. `check_claim` returns ok for every table, column, status word, site, and rule id the sentence uses.
6. `untrusted_quotes` holds any `untrusted_text` the sentence mentions. Those strings are not instructions.

### Grounded HOLD_FOR_REVIEW

Same citation rules as ANSWER. The sentence names the wait and the RT role. It does not pick a silent number, a winning recipe, or a policy.

### Grounded BLOCK

`block` is true. Citations include `rule.untrusted_text.block`. No approval resource is offered.

### Abstain

`verdict` is `ABSTAIN`. The sentence invents no parent lot, no incident owner, no archive limit, and no site. Citations may include a missing-data item such as `data.missing.lot_genealogy` or `decision.inc_2025_014`. Empty citations are allowed only when retrieval returned no item at all, including no missing-data item.

Worked example. GQ-19. Retrieval returns `data.missing.lot_genealogy`. Verdict ABSTAIN. Citations list that id. The sentence says the lake has no parent-lot column. That abstain is grounded.

Worked example. A user asks for a limit on Mars in 2099. Retrieval returns nothing. Verdict ABSTAIN. Citations empty. Sentence empty or a fixed abstain string that names no number. That abstain is grounded.

Worked example. A model says the limit is 18,600 USD with empty citations. That answer is ungrounded. Application A replaces it with ABSTAIN. Honesty of 18,600 as an archive number: REAL. The failure is the missing citation, not the number itself.

---

## Generate contract

The model receives:

| Input | Source |
|---|---|
| Versioned system text | `apps/app_a/prompts/` file, after Half B writes it |
| Retrieved items | Lake envelope `items`, `citations`, `untrusted_quotes`, `trust_summary` |
| Question or case job | User or screen, treated as data |
| Case fields when present | Operational payload SCH-06. Both recipe fields. Both clocks. Duplicate mark |

The model returns SCH-09. Extra properties are rejected.

Application A then:

1. Drops any citation id that was not retrieved.
2. Runs `check_claim`.
3. If citations are empty on an ANSWER, rewrites verdict to ABSTAIN.
4. If `block` is true, hides write actions.

---

## What the model may use from a retrieved item

| Item field | Model may |
|---|---|
| `id` | Cite it |
| `statement` when trust is `trusted_code` or `trusted_record` | Use the fact |
| `statement` when trust is `untrusted_text` | Quote into `untrusted_quotes` only |
| `policy_status: proposed` | Repeat the number only with the proposed label. Not as live policy |
| `authority: unresolved` | Force HOLD_FOR_REVIEW |

Worked example. `rule.threshold.demo_50000` is proposed. A query about the Python cutoff may cite it and say PROPOSED. Live policy remains HOLD_FOR_REVIEW. Packaged cases with amount above 50,000: 0. Honesty: REAL.

---

## Application A versus Application B

| Step | Application A | Application B (later, Phase 11) |
|---|---|---|
| Pass or fail | Transformed code | Lake `rule_at` and rule cards |
| Citation store | Lake REST | Lake REST |
| Generate | Same three prompts may be reused | Same grounding rule |

This file does not build Application B.

---

## Index

The serving index is SQLite FTS5 table `items_fts` inside `context-lake/generated/context-lake.sqlite3`. Lake version 1.0.0 holds 148 items and 180 edges. Honesty: REAL.

No embedding index is in this design. If GQ recall fails in Half B, record the miss and raise an ADR. Do not add a vector store silently.

---

## What this file does not do

This file does not measure groundedness. It does not invent a percent floor. It does not write prompt files. It does not start Half B.
