# Economics baseline reconciliation

| Field | Value |
|---|---|
| Stage | Phase 2 / 8 AI-versus-no-AI qualification |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p2-doc-20261018-001 |
| Status | COMPLETE. 0C envelope named. Retired cost assumptions named. |
| Evidence sources | `docs/00-preflight/ai-economics/workload-assumptions.md`; `docs/00-preflight/ai-economics/solution-scenarios.md`; `docs/00-preflight/ai-economics/provisional-token-budget.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/00-preflight/ai-economics/preliminary-finops-baseline.md`; `ai-vs-no-ai-matrix.md`; `minimum-intelligence-assessment.md`; BO-11 |
| Assumptions | Token, price, and latency cells that 0C left Unknown stay Unknown. This page does not fill them. |
| Unresolved issues | Prompt tokens, completion tokens, dollars per 1,000 tokens, API p95, and cost per resolved scenario stay Unknown. |
| Residual risks | A later FinOps page that puts a model cost on triage, rule evaluation, reconciliation, or de-duplication would restore a line this page retires. |

This page reconciles Phase 2 with the Phase 0C AI-economics envelope. It names that envelope. It names the cost assumptions that no longer apply. It does not invent a price, a token count, or a target percent.

## The 0C envelope

The envelope lives in `docs/00-preflight/ai-economics/`. Five files:

| File | What it holds | Status in 0C |
|---|---|---|
| `workload-assumptions.md` | Measured volumes (125 cases, 89 open, 2 urgent, 8,567 feeds) and assumptions A-W1 to A-W6 | PROVISIONAL. Reconcile at Phase 2 and Phase 13 |
| `solution-scenarios.md` | Demo jobs S7 to S13 and candidate AI tasks | PROVISIONAL |
| `provisional-token-budget.md` | Lines B1 to B7. Most cells Unknown. Replay line is 0 if replay is used | PROVISIONAL |
| `quality-latency-cost-envelope.md` | Quality, latency, and cost axes with Unknown targets | PROVISIONAL |
| `preliminary-finops-baseline.md` | Synthetic `mean_amount` 4982.61 and `hours_per_case` 0.603 | PROVISIONAL. Honesty: SIMULATED |

**Verified Fact.** Those five files tell Phase 2 to drop lines for capabilities that will not use a model, and to retire irrelevant AI cost assumptions.

## What stays in the envelope

These lines still apply because conflict explanation, natural-language query, and agentic planning are labelled GenAI.

| 0C item | Why it stays | Label |
|---|---|---|
| A-W1. Delivery-agent tokens | Coordinator, executor, and reviewer still run in Cursor. | Assumption |
| A-W2. Demo replay live tokens = 0 | `MODEL_MODE=replay` is still the planned demo mode. | Assumption |
| A-W3. Rehearsal record | GenAI prompts still have to be recorded once. The count stays Unknown. | Unknown |
| A-W5. Azure OpenAI as the later live path | Still the header assumption. Unit price stays Unknown. | Unknown |
| A-W6. Read-only tools only | FD-02 is DECIDED. | Verified Fact |
| B1. Laptop demo, replay on | Still 0 live tokens if replay is used as designed. | Assumption until Phase 15 |
| B2, B3, B4, B5, B6, B7 | Still Unknown. Scope is the three GenAI capabilities, not all seven. | Unknown |
| Citation and abstention quality axes | They apply to GenAI answers. Numeric floors stay Unknown. | Unknown |
| Synthetic labor 0.603 hours/case and mean amount 4982.61 | Still SIMULATED operating fields. They are not model cost. | Verified Fact of the tool output |

S7 to S13 still run. The deterministic core of each scenario (replay mark, recipe compare, two clocks, policy lookup, retry status) stays in code. The model is used when that scenario asks for an explanation, a natural-language answer, or a draft plan.

## Retired AI cost assumptions

Each row names the assumption, where it lived, and why it is retired.

| ID | Retired assumption | Where it lived | Why it is retired | Label |
|---|---|---|---|---|
| R-P2-01 | Every S7 to S13 turn is a model-cost turn | `solution-scenarios.md` residual risk; `workload-assumptions.md` A-W4 read as full-scenario tokens | Replay detect, recipe compare, clock split, policy lookup, and retry status are labelled deterministic. Model tokens apply only to explanation, query, and draft-plan turns. | Inference from the FD-04 labels. A-W4’s token count stays Unknown. |
| R-P2-02 | Production machine-learning inference or training cost for `engineering_hold` | Implied by carrying an ML line into Phase 13. 0C has no numbered ML line. | Null test 117/125 versus majority 117/125. Honesty: REAL. FD-05 recommendation: Reject ML. No production model. No ML token line. | Verified Fact |
| R-P2-03 | Token and inference-cost envelope for rule evaluation | A reading of B3/B4 and the quality envelope that puts a model on every capability | Rule pass-or-fail is deterministic. FD-08 already names the archive. | Verified Fact |
| R-P2-04 | Token and inference-cost envelope for reconciliation | Same reading of B3/B4 | `reconcile()` is written key, schema, REPLAY, and quantity tests. | Verified Fact |
| R-P2-05 | Token and inference-cost envelope for intake de-duplication | Same reading of B3/B4 | Duplicate is a `message_id` or REPLAY status test. | Verified Fact |
| R-P2-06 | Token and inference-cost envelope for triage ranking | Same reading of B3/B4; any hold-score latency line | `priority()` is four branches. The hold predictor did not beat 117 of 125. | Verified Fact |
| R-P2-07 | Agent-completion latency as a cost line for ranking, rules, reconcile, or de-duplication | `quality-latency-cost-envelope.md` agent completion row | Those four capabilities have no agent step. Agent completion stays Unknown and applies only to agentic planning. | Inference from the labels |
| R-P2-08 | Counting every candidate AI task in Intent 10.1 as a live cost before qualification | `solution-scenarios.md` warning | This phase accepted three language tasks and rejected ML and the four code tasks. | Verified Fact of this note |

Worked example. Scenario 7 still runs. Code marks the 67 REPLAY rows. That mark has no model token line. A later explanation of those 67 rows is a GenAI turn and stays on B3 or B4 as Unknown tokens.

## What Phase 13 must still measure

Phase 13 writes `docs/32-finops/` against the 0C pages and this reconciliation. Cells it may fill only when measured:

- Prompt and completion tokens for conflict explanation, natural-language query, and agentic planning.
- Rehearsal-record tokens (B2).
- Retrieval or embedding tokens (B5) if that path is built.
- Dollars from a bill or a recorded list price. A copied public price becomes a Verified Fact only after that source is recorded.
- API p95 after a server is started.

**Verified Fact.** BO-11 working answer. Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit.

**Verified Fact.** This page states no dollar benefit.

## What this file does not do

This file does not edit the five 0C documents. Those files stay as Phase 0 wrote them. This file is the Phase 2 reconciliation note. It does not invent a token total.
