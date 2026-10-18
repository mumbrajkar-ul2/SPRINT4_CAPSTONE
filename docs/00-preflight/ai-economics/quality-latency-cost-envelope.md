# Quality, latency, and cost envelope

| Field | Value |
|---|---|
| Stage | Phase 0 / 0C AI-economics envelope |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL. Reconcile at Phase 2 and Phase 13 |
| Evidence sources | `Execution_Plan.md` section 9; `Project_Intent.md` sections 13 and 14; `docs/operations-service-levels.md`; `app/baseline.py` output; no live server timing |
| Assumptions | Historical SLO numbers in the inherited runbook are planning notes, not this envelope |
| Unresolved issues | Quality thresholds, latency percentiles, and unit prices are Unknown |
| Residual risks | Copying 99.5% availability from `docs/operations-service-levels.md` into this envelope would present an unmeasured number as a target |

This envelope names the three axes Phase 2 and Phase 13 must fill. It does not invent a threshold.

## Quality

**Verified Fact.** FD-03 freezes the AI quality family. Measures in `Execution_Plan.md` section 9 are groundedness, citation, abstention, and rejected schema claims. Honesty label: REAL when those tests run.

**Unknown.** Release thresholds for groundedness, citation, abstention, and hallucination. FD-14 and FD-18 are PENDING.

**Verified Fact.** BO-03 working answer. A model may explain and propose. It may not write a record without a person.

Provisional quality envelope:

| Axis | Floor in force now | Target | Label |
|---|---|---|---|
| Citation on a consequential answer | Must cite a lake item or abstain (later app rule in `Execution_Plan.md` Phase 9) | Unknown numeric percent | Assumption of the later rule. Not measured |
| Abstention on overlap or silence | HOLD_FOR_REVIEW (FD-08 / BO-08 working answers) | Unknown | Working policy, not a scored KPI |
| Hallucination | Unknown | Unknown | Unknown |
| Expert agreement | Unknown | Unknown | Decision quality is PRECOMPUTED later |

## Latency

**Verified Fact.** This unit did not start `python -m app.server` or the gateway. No request time was measured.

**Verified Fact.** `docs/operations-service-levels.md` records older planning notes: 99.5% scheduled-hour availability, overnight reconciliation before 06:00, partner feed accepted within 4 hours, recovery time 8 hours, recovery point 24 hours. That file says these are historical working targets, not measured guarantees.

Provisional latency envelope:

| Axis | Measured now | Target | Label |
|---|---|---|---|
| Legacy API p95 | Unknown | Unknown | Unknown |
| Lake REST p95 (8091) | Service does not exist yet | Unknown | Unknown |
| Retrieval p95 | Service does not exist yet | Unknown | Unknown |
| Agent completion time | Service does not exist yet | Unknown | Unknown |
| Approval wait | No app yet | Unknown | Unknown |

Do not copy the 4-hour or 8-hour historical notes as this project's SLO.

## Cost

**Verified Fact.** `app/baseline.py` emitted `hours_per_case` 0.603 and `mean_amount` 4982.61 on both runs. Those are synthetic operating-cost and case-amount fields. Honesty: SIMULATED. They are not model cost.

**Unknown.** Tokens. Unknown. Dollars per 1,000 tokens. Unknown. Cost per resolved scenario. Unknown.

Provisional cost envelope:

| Axis | Measured now | Target | Honesty | Label |
|---|---|---|---|---|
| Labor hours per case (legacy field) | 0.603 | None invented | SIMULATED | Verified Fact of the tool output |
| Mean case amount (legacy field) | 4982.61 | None invented | SIMULATED | Verified Fact of the tool output |
| Inference cost | Unknown | None invented | Unknown | Unknown |
| Storage and laptop compute | Unknown | None invented | Unknown | Unknown |
| Cost per resolved scenario | Unknown | None invented | REAL later if measured | Unknown |
| ROI | Unknown | None invented | EDUCATIONAL later | Unknown. BO-11 forbids a monetary benefit claim |

## Reconciliation

Phase 2 drops quality and cost lines for capabilities it rejects. Phase 13 writes measured latency and token cost. Until then every empty numeric cell stays Unknown.
