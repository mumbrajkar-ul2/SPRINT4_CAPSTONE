# Solution scenarios

| Field | Value |
|---|---|
| Stage | Phase 0 / 0C AI-economics envelope |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL. Reconcile at Phase 2 and Phase 13 |
| Evidence sources | `Execution_Plan.md` sections 8 and 10; `Project_Intent.md` sections 10 and 15; `Decision_Tracker.md` BO-03 |
| Assumptions | Phase 2 will confirm which of these scenarios keep a model and which stay deterministic |
| Unresolved issues | Token and latency numbers per scenario are Unknown |
| Residual risks | Counting every scenario as a GenAI cost before Phase 2 will overstate the envelope |

This page names the work paths the envelope must cover. It does not choose the Phase 2 qualification result.

## Scenario set the demo must run

**Verified Fact.** `Project_Intent.md` section 15.2 and `Execution_Plan.md` section 8.

| ID | What the user sees | Linked problem | AI role in the intent | Deterministic core |
|---|---|---|---|---|
| S7 | A replayed MESDispatch delivery is detected and explained | BP2 | Explain the duplicate evidence | Duplicate and replay rules |
| S8 | Recipe revision differs. The case routes for approval | BP1 | Show the two revisions and the time they apply | Recipe authority and approval |
| S9 | A late metrology event is shown with event time and arrival time kept apart | BP3 | Explain the two clocks | Temporal fields |
| S10 | Overlapping policies. The system abstains and asks for approval | BP6 | Name the overlap. Do not pick a silent winner | Policy lookup and HOLD_FOR_REVIEW |
| S11 | Upstream outage or schema mismatch. Retry and a visible status | BP8 | Summarize the failure | Retry, health, user-visible status |
| S12 | A rule is traced from document and code to a test | BP4 | Retrieve the four implementations | Rule cards and tests |
| S13 | Both apps run S7 to S11. Each difference traces to a lake item | BP4, BP5 | Help show the missing lake item | Parity harness |

## Candidate AI tasks from the intent

**Verified Fact.** `Project_Intent.md` section 10.1 lists these as justified opportunities. Phase 2 still has to accept or reject each one.

- Summarize a case or lot timeline with citations and conflict flags.
- Explain why sources disagree.
- Assist discovery across code, tests, schemas, and incidents.
- Draft plans, tests, and handoffs for a person to review.
- Propose term mappings for governed approval.

**Verified Fact.** `Project_Intent.md` section 10.2 keeps authorization, state changes, KPI math, and final reconciliation deterministic.

**Verified Fact.** BO-03 working answer. AI explains and proposes. A person approves every record-changing action.

## Cost-bearing modes

| Mode | When | Live model calls | Label |
|---|---|---|---|
| Delivery agents | Phases 0 to 16 in Cursor | Yes, on the builder and reviewer models | Assumption that those tokens are delivery cost |
| Rehearsal record | Before demo day | Yes, once per prompt hash | Assumption. Count Unknown |
| Demo replay | 40-minute defence | No, if `MODEL_MODE=replay` holds | Assumption A-W2 |
| Evaluation | Phase 12 and Phase 14 | Yes, unless replay is reused | Assumption. Count Unknown |
| Offline laptop with no key | Any time replay files exist | No | Assumption |

## Reconciliation note

Phase 2 retires any scenario that fails the AI-versus-no-AI test. Phase 13 replaces every Unknown token and price cell that can then be measured. Until those phases run, this page carries no unit price and no token total.
