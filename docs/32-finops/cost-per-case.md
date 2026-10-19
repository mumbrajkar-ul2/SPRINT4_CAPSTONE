# Cost per case

| Field | Value |
|---|---|
| Stage | Phase 13 / 32 FinOps and token efficiency. Half B measured results. SC-32-01 / HB-32-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-32b-doc-20261018-001 |
| Status | MEASURED. One shown Application A replay query wrote `prompt_tokens=0` and `completion_tokens=0`. Dollars per case stay Unknown. 4982.61 and 0.603 stay SIMULATED. BO-11 stays PROPOSED. |
| Evidence sources | FD-19; BO-11; `docs/00-preflight/ai-economics/preliminary-finops-baseline.md`; `docs/00-preflight/ai-economics/workload-assumptions.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/08-ai-qualification/economics-baseline-reconciliation.md`; `app/baseline.py` output cited in 0C; `apps/app_a/intelligence/generate.py`; `tests/platform/test_phase13_finops.py`; `baseline-vs-actual-token-analysis.md` |
| Assumptions | `MODEL_MODE=replay`. One case may have zero or more query, explain, or draft turns. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | Dollars per case stay Unknown. Live Azure tokens per case stay Unknown. Exception cycle time stays Unknown. Aged backlog stays Unknown. |
| Residual risks | Dividing 4982.61 by 125 would invent a dollar per case from a synthetic amount. Writing 0 dollars because replay used 0 tokens would invent an invoice. |

This file names how this stack will count cost for one packaged case. A case is one row in the 125-record packaged set. The model cost of a case is the sum of prompt tokens and completion tokens on that case's language turns. Under replay those two counts are 0 on the shown Application A query. Dollar cost per case stays Unknown because no invoice exists.

Engineering decision ED-P13-32A-05, authority: team-force. Cost per case in dollars stays Unknown. Replay live tokens on a shown Application A query stay 0 after HB-32-01. Deterministic cores add 0 model tokens.

---

## Finding

**Finding.** `python -m app.baseline` emitted 125 records, `mean_amount` 4982.61, and `hours_per_case` 0.603. Those two money-shaped fields are synthetic. Honesty: SIMULATED. They are not model cost. After HB-32-01, one Application A replay query wrote `prompt_tokens=0` and `completion_tokens=0`. Honesty: REAL for that path. Dollars per case stay Unknown.
**Evidence.** `preliminary-finops-baseline.md`. `workload-assumptions.md`. `generate.py`. `tests/platform/test_phase13_finops.py`. Phase 2 retired rows R-P2-03 to R-P2-06. FD-19. BO-11.
**Impact.** The shown query meters as 0 and 0. This page still leaves dollars per case Unknown.
**Risk.** Multiplying 0.603 hours by a wage would invent a labor dollar.
**Confidence.** High on the packaged 125, the synthetic labels, and the measured zeros. Unknown on dollars per case.
**Open questions.** Who later records a unit price. Company signer.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric cost floors stay Unknown. This half invents no dollar benefit.

**Verified Fact** of BO-11 working answer. Claim no monetary benefit. The row stays PROPOSED.

**Verified Fact.** Packaged volume from `app/baseline.py` on 2026-10-18: 125 records, 89 open, 2 urgent, 6 sites. Honesty: REAL for those counts.

**Verified Fact** of the same tool output. `mean_amount` 4982.61 and `hours_per_case` 0.603. Honesty: SIMULATED.

---

## What a case costs on this laptop

| Cost bucket | How it is counted | Amount now | Honesty | Label |
|---|---|---|---|---|
| Live model tokens on a replay query | Sum of `prompt_tokens` and `completion_tokens` after Half B | Measured 0 and 0 on the shown query | REAL for that path | Verified Fact of HB-32-01 |
| Live model tokens on Azure | Same fields from a live usage object | Unknown | Unknown | Unknown |
| Synthetic case amount | Mean of `cases.amount` | 4982.61 | SIMULATED | Verified Fact of tool output |
| Synthetic labor | `operating_costs.labor_hours / total_cases` | 0.603 hours | SIMULATED | Verified Fact of tool output |
| Dollars per case | Tokens times a unit price | Unknown | Unknown | Unknown |
| Delivery-agent tokens | Cursor coordinator, executor, reviewer | Unknown | Assumption A-W1 keeps them off this meter | Assumption |
| Cloud platform | Invoice | Unknown | Unknown | Unknown |

Worked example. Case `REPLAY-000000000` is one packaged row. Half B posted `POST /api/query` with question `Which port does the Context Lake REST listener use?`. The stdout line holds `prompt_tokens=0` and `completion_tokens=0`. The model-token sum for that turn is 0. Honesty: REAL. The dollar cost of that turn stays Unknown. The 4982.61 mean amount stays on the synthetic row. It is not the cost of that query.

Worked example. Ranking that case with `priority()` uses status, severity, and amount. That function adds 0 model tokens. Phase 2 retired the triage token line as R-P2-06.

---

## How the later sum is built

Engineering decision ED-P13-32A-04, authority: team-force.

| Step | What is added | What is left out |
|---|---|---|
| 1 | Each Application A query, explain, or draft turn that ran for the case | Health GET. Identity miss. Lake write reject |
| 2 | Each agent `plan_draft` that called `generate()` | OPA verdict. Human approval wait |
| 3 | Prompt tokens plus completion tokens on those turns | Cursor delivery tokens |
| 4 | Under replay, write 0 and 0 | A guessed Azure usage |

The roll-up key is `case_id` when the request sent one. A query with an empty `case_id` still meters the turn. It does not invent a case row.

Half B wrote the two fields on one query. Half B did not build a per-case report screen.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-32-06 | 4982.61 is divided by 125 and labeled cost per case | A dollar with two decimals | Keep 4982.61 as the synthetic mean amount. Leave dollars per case Unknown |
| FM-32-07 | 0.603 hours is multiplied by a wage | A labor dollar | Leave labor as 0.603 hours SIMULATED |
| FM-32-08 | Deterministic ranking is given a token line | A model cost on triage | Keep R-P2-06 retired |
| FM-32-09 | Cursor chat tokens are added to the case | A large token total | Keep A-W1. Delivery tokens stay off the case meter |

Dead-letter parking stays on invalid intake. A case with no query turn has no token line. That empty meter is not a parked message.

---

## Dead-letter queue and replay

A parked intake on a case does not call the model. Replay of that parked row stays in `dlq.py`. Language-model replay stays `MODEL_MODE=replay`. Both paths add 0 live model tokens on this laptop.

---

## Runbook — read cost for one case

1. Take one packaged `case_id`.
2. List the query, explain, and draft turns that used that id.
3. After Half B, read `prompt_tokens` and `completion_tokens` on those stdout lines.
4. Sum those integers. Under replay the shown turn is 0.
5. Leave dollars Unknown.
6. Leave 4982.61 and 0.603 on the synthetic rows.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| 125 records | 0C workload page | Packaged volume | A cost floor |
| `prompt_tokens` after Half B | stdout | The shown turn wrote 0 | Dollars per case |
| `hours_per_case` 0.603 | 0C FinOps baseline | The tool emitted that field | Saved labor |

No cost-per-case percent or dollar floor is set. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

Line B1 is the demo replay path. It is measured as 0 and 0 for the shown query. Honesty: REAL for that path. Cost per resolved scenario stays Unknown in dollars. See `cost-per-outcome.md`. This half claims no dollar benefit. BO-11 stays PROPOSED.

---

## The one small Half B check

See `cost-guardrails.md` SC-32-01 and HB-32-01. Half B metered one Application A replay-hit query as 0 and 0. Honesty: REAL. Half B did not compute a dollar per case. Measured cells live in `baseline-vs-actual-token-analysis.md`.

---

## What this file does not do

This file named cost per case. Half B wrote the two zeros on one query. This file does not start sub-stage 33. It does not invent a wage. It does not invent a dollar per case. It does not sign BO-11. It does not update a tracker.
