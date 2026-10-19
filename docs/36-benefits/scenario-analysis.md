# Scenario analysis

| Field | Value |
|---|---|
| Stage | Phase 14 / 36 ROI and benefits |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | EDUCATIONAL. Three teaching scenarios. No monetary benefit. BO-11 stays PROPOSED. |
| Evidence sources | `roi-model.md`; `docs/00-preflight/ai-economics/provisional-token-budget.md`; `docs/32-finops/baseline-vs-actual-token-analysis.md`; `docs/32-finops/cost-per-outcome.md`; this-unit pytest; BO-11; FD-19 |
| Assumptions | Scenario R is the laptop replay path already measured. Scenario A is a later live Azure path. Scenario L is a labor teaching path that still has no wage. |
| Unresolved issues | Azure tokens Unknown. Unit price Unknown. Wage Unknown. Cycle time Unknown. |
| Residual risks | Presenting Scenario L hours as booked labor recovery. Presenting Scenario R zeros as an invoice. |

This file runs the educational ROI formula on three named scenarios. Every ROI cell is EDUCATIONAL. This page claims no monetary benefit.

---

## Finding

**Finding.** Scenario R (replay demo) has measured prompt_tokens 0 and completion_tokens 0, honesty REAL for that path, and Unknown dollars. Scenario A (live Azure) has Unknown tokens and Unknown dollars. Scenario L (synthetic labor) keeps hours_per_case 0.603 SIMULATED and wage Unknown, so labor dollars stay Unknown. All three ROI results are Unknown dollars labelled EDUCATIONAL. Headlines stay Unknown in every scenario.
**Evidence.** HB-32-01. This-unit harness `event=replay_tokens` lines. 0C lines B1 to B7. Frozen hours_per_case 0.603.
**Impact.** A reader can see three ways the formula stays empty of money.
**Risk.** Filling Scenario L with a public wage.
**Confidence.** High on Scenario R token zeros. Unknown on Scenario A and on any wage.
**Open questions.** Rehearsal invoice for B2. Unit price. Wage source. BO-11 signer.

---

## Shared locks across scenarios

| Lock | Value | Honesty |
|---|---|---|
| records | 125 | REAL |
| open_cases | 89 | REAL for `status != CLOSED` |
| Exception cycle time | Unknown | Unknown |
| Aged backlog | Unknown | Unknown |
| mean_amount | 4982.61 | SIMULATED |
| hours_per_case | 0.603 | SIMULATED |
| Parity | 14 rows, matched 12, differed 2 | REAL |
| ROI label | EDUCATIONAL | FD-20 |

---

## Scenario R — laptop replay

What it is. Compose default `MODEL_MODE=replay`. Saved answers play back. Azure stays uncalled on this path.

| Cell | Value | Honesty |
|---|---|---|
| prompt_tokens on the shown Application A query | 0 | REAL for that path |
| completion_tokens on that query | 0 | REAL for that path |
| 0C line B1 | 0 and 0 | REAL if replay is used as designed. Measured 0 and 0 |
| Lines B2 to B7 | Unknown | Unknown |
| Unit price | Unknown | Unknown |
| Cost dollars | Unknown | EDUCATIONAL |
| Avoided effort | Unknown | EDUCATIONAL |
| ROI | Unknown | EDUCATIONAL |

Worked example. Phase 13 question `Which port does the Context Lake REST listener use?` wrote `event=replay_tokens`, `prompt_tokens=0`, `completion_tokens=0`. This unit's harness also wrote those zeros on `/api/query` with `model_mode=replay`. Honesty: REAL for the replay path. Dollar cost stays Unknown.

---

## Scenario A — live Azure later

What it is. A person sets `MODEL_MODE=azure` and supplies endpoint, deployment, and key. That step is NEEDS_HUMAN. This unit did not call Azure.

| Cell | Value | Honesty |
|---|---|---|
| prompt_tokens | Unknown | Unknown |
| completion_tokens | Unknown | Unknown |
| Unit price | Unknown | Unknown |
| Cost dollars | Unknown | EDUCATIONAL |
| Avoided effort | Unknown | EDUCATIONAL |
| ROI | Unknown | EDUCATIONAL |

Worked example. 0C lines B2, B3, and B4 are rehearsal and eval token lines. They stayed Unknown in Phase 13. They stay Unknown here. This scenario does not copy a public list price.

---

## Scenario L — synthetic labor teaching path

What it is. A teaching reader looks at hours_per_case 0.603 and asks whether labor dollars can fill avoided effort. The wage is unnamed. The hours are synthetic.

| Cell | Value | Honesty |
|---|---|---|
| hours_per_case | 0.603 | SIMULATED |
| records | 125 | REAL |
| Wage | Unknown | Unknown |
| Labor dollars | Unknown | EDUCATIONAL |
| Cycle-time cut | Unknown | Unknown |
| Avoided effort | Unknown | EDUCATIONAL |
| ROI | Unknown | EDUCATIONAL |

Worked example. The tool prints 0.603. Honesty: SIMULATED. The wage cell is empty. This scenario does not write 0.603 times 125 times a wage. The product would be an invented bill.

---

## Scenario compare

| Cell | Scenario R | Scenario A | Scenario L | Honesty of ROI |
|---|---|---|---|---|
| Live tokens | 0 and 0 on the shown path | Unknown | Not the labor path | REAL zeros only on R replay |
| Dollars | Unknown | Unknown | Unknown | EDUCATIONAL |
| Headlines | Unknown | Unknown | Unknown | Unknown |
| Monetary benefit claimed | None | None | None | Verified Fact of this page |

**Verified Fact** of BO-11. Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit.
