# Cost per outcome

| Field | Value |
|---|---|
| Stage | Phase 13 / 32 FinOps and token efficiency. Half B measured results. SC-32-01 / HB-32-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-32b-doc-20261018-001 |
| Status | MEASURED. One shown replay language turn wrote 0 and 0 live tokens. Dollars per outcome stay Unknown. ROI stays for Phase 14. BO-11 stays PROPOSED. |
| Evidence sources | FD-19; BO-02; BO-11; `docs/00-preflight/ai-economics/solution-scenarios.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/00-preflight/ai-economics/provisional-token-budget.md`; `docs/08-ai-qualification/qualification-decision.md`; `docs/08-ai-qualification/economics-baseline-reconciliation.md`; `Execution_Plan.md` section 9; `tests/platform/test_phase13_finops.py`; `baseline-vs-actual-token-analysis.md` |
| Assumptions | An outcome on this page is one finished demo scenario S7 to S13. Headline business KPIs stay exception cycle time and aged backlog under BO-02. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | Dollars per resolved scenario stay Unknown. Exception cycle time stays Unknown. Aged backlog stays Unknown. Live Azure tokens per scenario stay Unknown. |
| Residual risks | Calling 0 live tokens a verified saving would invent a Phase 14 benefit. Filling cost per resolved scenario with a public list price would invent a floor. |

This file names cost for one finished demo scenario. The 0C envelope calls that number cost per resolved scenario. The deterministic core of each scenario uses code. The language turn, when the scenario asks for an explanation, a natural-language answer, or a draft, uses `generate()`. Under replay that language turn is 0 live tokens on the shown query. Dollar cost per outcome stays Unknown. ROI stays EDUCATIONAL and waits for Phase 14.

Engineering decision ED-P13-32A-05 continued, authority: team-force. Cost per outcome in dollars stays Unknown. Replay live tokens on a shown language turn stay 0 after HB-32-01.

---

## Finding

**Finding.** Scenarios S7 to S13 still run. Phase 2 labelled triage, rule evaluation, reconciliation, and intake de-duplication as deterministic. It labelled conflict explanation, natural-language query, and agentic planning as GenAI. The 0C cost axis for cost per resolved scenario is Unknown. ROI honesty is EDUCATIONAL. BO-11 forbids a monetary benefit claim. After HB-32-01, replay line B1 is 0 and 0 on the shown query. Honesty: REAL for that path. No measured outcome-dollar cell exists.
**Evidence.** `solution-scenarios.md`. `qualification-decision.md` FD-04. `quality-latency-cost-envelope.md` cost table. `Execution_Plan.md` section 9. `tests/platform/test_phase13_finops.py`. BO-11. FD-19.
**Impact.** Half B proved 0 live tokens on one replay query. This page still leaves dollars per outcome Unknown.
**Risk.** Writing a Phase 14 ROI number in this half would skip BO-11 sign-off.
**Confidence.** High on the scenario list, the retired deterministic lines, and the measured zeros. Unknown on dollars per outcome.
**Open questions.** Phase 14 owner for the EDUCATIONAL ROI sheet. Company signer.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric cost floors stay Unknown. This half invents no dollar benefit.

**Verified Fact** of BO-11 working answer. Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit. The row stays PROPOSED.

**Verified Fact** of BO-02 working answer. Exception cycle time and aged backlog are the two headline business KPIs. Both measured values stay Unknown. The row stays PROPOSED.

**Verified Fact.** FD-04. Conflict explanation, natural-language query, and agentic planning are the three GenAI capabilities that still carry a token line.

---

## Outcomes this page covers

**Verified Fact** of `solution-scenarios.md` and Phase 2.

| Id | What finishes | Deterministic core | Language turn if asked | Model tokens under replay |
|---|---|---|---|---|
| S7 | Replayed MESDispatch delivery is marked and explained | Duplicate and replay rules. 67 REPLAY rows | Explain the duplicate evidence | Designed 0 live tokens |
| S8 | Recipe revision differs and routes for approval | Recipe compare | Show the two revisions | Designed 0 live tokens |
| S9 | Late metrology keeps event time and arrival time apart | Two clocks | Explain the two clocks | Designed 0 live tokens |
| S10 | Overlapping policies abstain | Policy lookup and HOLD_FOR_REVIEW | Name the overlap | Designed 0 live tokens |
| S11 | Upstream outage or schema mismatch stays visible | Retry and status | Summarize the failure | Designed 0 live tokens |
| S12 | A rule is traced from document and code to a test | Rule cards and tests | Retrieve the four implementations | Designed 0 live tokens |
| S13 | Both apps run S7 to S11. A difference cites a lake item | Parity harness | Help show the missing lake item | Designed 0 live tokens |

Worked example. Scenario 7 marks 67 REPLAY rows in code. That mark adds 0 model tokens. An explanation of those 67 rows under `MODEL_MODE=replay` is designed as 0 prompt tokens and 0 completion tokens. The dollar cost of finishing S7 stays Unknown.

Worked example. Headline KPI exception cycle time is still Unknown. This page does not write a cycle-time saving. BO-02 stays PROPOSED.

---

## How cost per outcome is computed later

| Input | Source | Status |
|---|---|---|
| Live tokens on the language turns of that scenario | `prompt_tokens` and `completion_tokens` after Half B | Measured 0 and 0 on the shown replay query. Honesty: REAL |
| Unit price | Invoice or a recorded list price | Unknown |
| Dollars per outcome | Tokens times unit price | Unknown |
| Avoided effort | Phase 14 ROI sheet | EDUCATIONAL later. Not written here |
| ROI | Avoided effort minus cost | EDUCATIONAL later. BO-11 |

Phase 14 writes `docs/36-benefits/`. This half does not open that folder.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-32-10 | S7's 67-row mark is priced as a model turn | A token line on the deterministic core | Keep R-P2-01. The mark stays 0 model tokens |
| FM-32-11 | 0 live tokens is written as a verified saving | A benefit sentence | Write 0 tokens. Leave dollars Unknown. Leave ROI to Phase 14 |
| FM-32-12 | Exception cycle time is invented so an outcome has a number | A hours figure | Leave cycle time Unknown |
| FM-32-13 | A public Azure price is multiplied by 0 and shown as $0.00 | A dollar actual | Leave the price Unknown. Do not write $0.00 as REAL |

Dead-letter parking stays on invalid intake. A scenario that parks a bad message still finishes the visible failure. That park adds 0 model tokens.

---

## Dead-letter queue and replay

S11 can show a parked intake and a replay of that row. Those steps are intake handling. Language-model replay stays `MODEL_MODE=replay`. Both stay at 0 live model tokens on this laptop.

---

## Runbook — read cost for one scenario

1. Name the scenario id, for example S7.
2. Separate the code core from the language turn.
3. After Half B, read `prompt_tokens` and `completion_tokens` on the language turn if it ran under replay.
4. The shown replay turn is 0 and 0. Honesty: REAL.
5. Leave dollars per outcome Unknown.
6. Leave ROI for Phase 14 with honesty EDUCATIONAL.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| S7 to S13 still in the envelope | 0C solution-scenarios page | The demo set | A dollar per scenario |
| B1 designed 0 and 0 | 0C token budget | Replay adds no live token by design | A signed ROI |
| Headline KPIs | BO-02 working answer | Which business numbers count later | A measured cycle time |

No outcome-cost floor is set. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

The 0C cell "Cost per resolved scenario" stays Unknown in dollars. Honesty later is REAL only when tokens and spend are measured. Spend is unmeasured. Token line B1 is the only cell Half B labelled REAL, and only for the replay path it showed. This half claims no dollar benefit. BO-11 stays PROPOSED.

---

## The one small Half B check

See `cost-guardrails.md` SC-32-01 and HB-32-01. Half B did not write an ROI number. Half B did not open `docs/36-benefits/`. Measured cells live in `baseline-vs-actual-token-analysis.md`.

---

## What this file does not do

This file named cost per outcome. Half B wrote 0 live tokens on one replay query. This file does not start sub-stage 33. It does not invent a cycle-time saving. It does not invent a dollar per outcome. It does not sign BO-11. It does not update a tracker.
