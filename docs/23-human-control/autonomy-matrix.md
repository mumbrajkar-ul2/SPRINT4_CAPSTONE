# Autonomy matrix

| Field | Value |
|---|---|
| Stage | Phase 10 / 23 Human control and audit chain. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/08-ai-qualification/minimum-agency-assessment.md`; `docs/12-specs/business-rules.md`; `docs/20-application/deterministic-ai-boundary.md`; BO-03; BO-09 |
| Assumptions | BO-03 stays PROPOSED. The working answer is used. Company titles stay Unknown. |
| Unresolved issues | Named people stay Unknown. INC-2025-014 owner stays Unknown. |
| Residual risks | Moving a write cell into the agent column would apply an unsigned bound as if it were signed code. |

This file names who may act on each job. The agent may draft. A person records every record-changing action.

---

## Finding

**Finding.** The agent has autonomy only for read-only explanation and a stored draft. Every write sits with RT-01 to RT-06. Injection has no approver.
**Evidence.** BO-03 working answer. Group C. FD-04. FD-05 rejects a hold predictor.
**Impact.** OPA and the graph edges follow this matrix.
**Risk.** An EXECUTE path that writes `engineering_hold` would skip RT-03.
**Confidence.** High on the SME roles. Unknown on company titles.
**Open questions.** BO-03 signer. Company titles.

---

## Matrix

| Job | Agent may | Code may | Person who records a write | OPA on a write proposal |
|---|---|---|---|---|
| Queue rank | None | `priority()` | None. Ranking does not write | Not called |
| Archive limit lookup | Read `rule_at` for a citation | `evaluate_live_policy` | None for the lookup. Silence waits | OPA-R-02 when no row |
| Explain a conflict | Draft a cited sentence | `check_claim` | None | EXECUTE when read-only |
| Draft a plan | Draft `draft_plan` | Store the text | None for the draft | EXECUTE when `record_change` is false |
| Recipe hold or release | Name both revisions. Propose a wait | Show the join | RT-03 | HOLD_FOR_REVIEW |
| Replay drop | Name the REPLAY mark. Propose a wait | Mark candidate | RT-05 | HOLD_FOR_REVIEW |
| Policy pick | Name the overlapping ids. Propose a wait | Flag overlap | RT-04 | HOLD_FOR_REVIEW |
| Keep wait on overlap | Propose keep-wait | Keep `waiting_role=RT-04` | RT-04 | HOLD_FOR_REVIEW |
| Assign follow-up owner | Say the owner is empty | Keep `owner_id` empty | RT-06 | HOLD_FOR_REVIEW. BLOCK if the model supplies a name |
| Dispose a review case | Propose a wait | Keep the wait | RT-01 | HOLD_FOR_REVIEW |
| Approve an agent draft that would write | Propose only | Pause | RT-02 | HOLD_FOR_REVIEW |
| Approve or release from harvested text | None | Copy quotes. Mark blocked | None offered | BLOCK |
| Predict `engineering_hold` | None. ML-rejected | None | RT-03 already owns hold | Not called |

Worked example. Scenario 8. The agent names R02 and R01. Honesty: REAL on that fixture. RT-03 records hold. The agent does not update the overlay.

Worked example. IC-04 proposes release from a source document. OPA-R-01 returns BLOCK. No RT role is offered a release button for that text.

---

## Proposer and approver

**Verified Fact.** BO-09.

`proposed_by` on a model draft is `model_draft`. The person who starts `POST /api/agent/run` is `actor_id` on the start event. That person may be the later approver only when `proposed_by` is `model_draft` and the actor is a matching RT role. If a person typed the proposal and that same person posts the approval, `check_write_action` rejects the write.

Half B treats a human-typed proposal as `proposed_by=<that actor_id>`. A model draft stays `proposed_by=model_draft`.

---

## What this file does not do

This file does not invent a company title. It does not sign BO-03.
