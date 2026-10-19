# ROI model

| Field | Value |
|---|---|
| Stage | Phase 14 / 36 ROI and benefits |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | EDUCATIONAL. UNSIGNED. BO-11 stays PROPOSED. |
| Evidence sources | `Execution_Plan.md` section 9; BO-11; `Decision_Tracker.md` section 5.1 BO-11 row; `docs/00-preflight/ai-economics/workload-assumptions.md`; `docs/08-ai-qualification/economics-baseline-reconciliation.md`; `docs/32-finops/cost-per-outcome.md`; `docs/32-finops/baseline-vs-actual-token-analysis.md`; `verified-benefits.md` |
| Assumptions | Listed in the assumption table below. Every ROI number on this page is EDUCATIONAL. |
| Unresolved issues | Avoided effort Unknown. Dollar cost Unknown. Unit price Unknown. Wage Unknown. Cycle time Unknown. Aged backlog Unknown. Signer name Unknown. |
| Residual risks | Filling the formula with 0.603 times a guessed wage. Presenting 0 replay tokens as a monetary benefit. Inventing a signer. |

This file is the ROI model. ROI here means avoided effort minus cost, as in `Execution_Plan.md` section 9. Honesty for this family is EDUCATIONAL. A SIMULATED or EDUCATIONAL number is a modelled figure on synthetic data. This page claims no monetary benefit.

Engineering decision ED-P14-03, authority: team-force. The formula stays avoided effort minus cost. Avoided effort stays Unknown. Dollar cost stays Unknown. No wage and no list price are invented. All filled teaching cells are EDUCATIONAL.

---

## Finding

**Finding.** The educational formula is avoided effort minus cost. Avoided effort stays Unknown because exception cycle time and aged backlog stay Unknown and no wage is recorded. Dollar cost stays Unknown because unit price is unnamed. Shown replay tokens are prompt_tokens 0 and completion_tokens 0, honesty REAL for that path, and still yield Unknown dollars. hours_per_case 0.603 and mean_amount 4982.61 stay SIMULATED. BO-11 stays PROPOSED.
**Evidence.** Section 9. BO-11 working answer. Phase 0 baseline. Phase 13 HB-32-01. This-unit baseline JSON.
**Impact.** The model is a teaching formula. BO-11 stays UNSIGNED. Dollar cells stay Unknown.
**Risk.** A later deck copying an EDUCATIONAL cell without the label.
**Confidence.** High on the empty dollar cells and the listed assumptions. Unknown on a later invoice.
**Open questions.** Who signs BO-11. Which invoice records a unit price.

---

## SME recommendation (mandatory to show)

**Verified Fact.** `Decision_Tracker.md` section 5.1 for BO-11.

Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit.

Why: The data is synthetic. An EDUCATIONAL label keeps the claim honest and defensible to judges.

**Verified Fact.** Section 5.2 Accept on 2026-10-18. The owner accepted that working answer. The row stays PROPOSED until the owner signs the artifact. This file is UNSIGNED.

---

## Formula

ROI = avoided effort minus cost.

| Term | Meaning on this stack | Value now | Honesty |
|---|---|---|---|
| Avoided effort | Shorter exception cycle time or fewer aged cases, converted with a recorded wage or delay cost | Unknown | EDUCATIONAL when later modelled |
| Cost | Model tokens times unit price, plus other recorded run cost | Unknown dollars | Tokens 0 and 0 REAL on the shown replay path. Dollars Unknown |
| ROI | Avoided effort minus cost | Unknown dollars | EDUCATIONAL |

Worked example. Shown replay tokens are 0 and 0. Honesty: REAL for that path. Unit price is unnamed. 0 times an unnamed price is Unknown dollars. Subtracting Unknown cost from Unknown avoided effort stays Unknown. The teaching label on that Unknown ROI cell is EDUCATIONAL.

---

## Assumption table

Every ROI cell on this page depends on these assumptions. Honesty of each modelled money cell: EDUCATIONAL.

| Id | Assumption | Status | Label |
|---|---|---|---|
| A-R1 | Population is the packaged 125 cases | Measured. records 125 | REAL count. EDUCATIONAL if used inside ROI |
| A-R2 | Python open volume stays 89 | Measured | REAL for `status != CLOSED` |
| A-R3 | Headline cycle time stays unmeasured | Unknown | Unknown |
| A-R4 | Aged backlog stays unmeasured | Unknown | Unknown |
| A-R5 | hours_per_case 0.603 is synthetic labor | Measured tool output | SIMULATED |
| A-R6 | mean_amount 4982.61 is synthetic money | Measured tool output | SIMULATED |
| A-R7 | No wage is on disk | Unknown | Unknown |
| A-R8 | `MODEL_MODE=replay` for the demo path | Measured | REAL |
| A-R9 | Shown Application A replay query uses 0 prompt tokens and 0 completion tokens | Measured | REAL for that path |
| A-R10 | Lines B2 to B7 stay Unknown | Unknown | Unknown |
| A-R11 | Azure unit price is unnamed | Unknown | Unknown |
| A-R12 | Delivery-agent tokens stay off the case meter (A-W1) | Assumption | Assumption |
| A-R13 | Deterministic cores add 0 model tokens (R-P2-03 to R-P2-06) | Phase 2 | Verified Fact of the labels |
| A-R14 | This page claims no monetary benefit | BO-11 working answer | Verified Fact of the working answer |
| A-R15 | Signer name stays Unknown | Unknown | Unknown |

Worked example for A-R5 and A-R7. The tool prints hours_per_case 0.603. Honesty: SIMULATED. A wage cell is empty. This model does not write 0.603 times 125 times a wage.

Worked example for A-R9 and A-R11. Replay wrote zeros. Honesty: REAL for that path. A dollars-per-1,000-tokens cell is empty. Cost in dollars stays Unknown.

---

## What enters cost

| Bucket | After value | Honesty | Enters ROI dollars? |
|---|---|---|---|
| Shown replay prompt_tokens | 0 | REAL for that path | Not until a unit price exists |
| Shown replay completion_tokens | 0 | REAL for that path | Not until a unit price exists |
| Live Azure tokens | Unknown | Unknown | No |
| hours_per_case | 0.603 | SIMULATED | No. Not a wage bill |
| mean_amount | 4982.61 | SIMULATED | No. Not customer savings |
| Cloud invoice | Unknown | Unknown | No |
| Delivery Cursor tokens | Unknown | Assumption A-W1 keeps them off the case meter | No |

---

## What enters avoided effort

| Candidate | After value | Honesty | Enters ROI dollars? |
|---|---|---|---|
| Exception cycle time cut | Unknown | Unknown | No |
| Aged backlog cut | Unknown | Unknown | No |
| open_cases cut | 89 minus 89 = 0 | REAL for the Python field | No. Delta 0 leaves avoided effort Unknown |
| Freeze 42 of 42 | 42 of 42 | REAL. Floor Unknown | No. That integer stays in AI quality |
| Harness 12 matched | 12 | REAL | No |

---

## Locked teaching result

| Cell | Value | Honesty |
|---|---|---|
| Avoided effort | Unknown | EDUCATIONAL |
| Cost | Unknown | EDUCATIONAL |
| ROI | Unknown | EDUCATIONAL |
| Monetary benefit claimed | None | Verified Fact of this page |

**Verified Fact.** FD-20. ROI honesty is EDUCATIONAL.

This file does not set a target percent. This file does not sign BO-11.
