# Problem statement

| Field | Value |
|---|---|
| Stage | Phase 0 / 3 Frame problem and value |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE. Technology-neutral |
| Evidence sources | `Project_Intent.md` sections 3 and 6; `Execution_Plan.md` section 3; `docs/business-context.md`; `docs/correspondence/operations-vs-risk-2024.md`; `docs/historic-decisions.md`; `operations/incidents/INC-2025-014.md`; `domain-profile.json` |
| Assumptions | The fictional company and the packaged records stand in for the operating problem |
| Unresolved issues | Cycle time and aged backlog are named headlines. Their current values are Unknown because the baseline tools do not emit them |
| Residual risks | Rewriting this problem as an AI-need statement would skip the evidence |

This statement names the business problem. It does not name a product, a model, or a cloud service.

## The problem

Fabpulse cannot consistently explain or close a fab-lot or equipment exception when the feeds, the local rules, the archived documents, and the month-end reports disagree.

People then spend more time reconciling. Queues grow. Two teams can report a different open-or-closed count for the same week. A disputed outage can sit with no owner.

## What operators feel

**Verified Fact.** `docs/business-context.md`. Operations leadership reports rising exception-handling effort and inconsistent information between external feeds and the core system.

**Verified Fact.** `docs/correspondence/operations-vs-risk-2024.md`. Operations wants cases closed within 48 hours. Compliance refuses automatic closures without evidence. Finance has not agreed what counts as a successfully resolved case. This was never written into the shared policy repository.

**Verified Fact.** `operations/incidents/INC-2025-014.md`. On 2025-11-18 a partner feed was delayed. The queue was retried twice. Downstream totals diverged. Staff used a spreadsheet at 04:00 UTC. Root cause was disputed. Follow-up owner unknown.

**Verified Fact.** `docs/historic-decisions.md`. In 2025 a replayed partner delivery inflated the exception queue and a rollout was rolled back.

## The eight defects the work must show

**Verified Fact.** `Execution_Plan.md` section 3.

1. A recipe revision on a process step does not match the tool recipe.
2. A replayed delivery creates extra queue work.
3. Event time, arrival time, and effective date are mixed.
4. Four local rule programs disagree.
5. Open and closed mean different things in different places.
6. Region words and policies overlap.
7. Untrusted text tells a reader to approve or ignore.
8. There is no access control, ownership is disputed, and recovery is manual.

## Value the business wants

**Verified Fact.** `Project_Intent.md` section 3.2. Faster and safer resolution. Explainable evidence. Interfaces that stay up. Comparable cost definitions. Audit evidence. Feeds that can be replayed without silent duplicates. Recipe, metrology, tool, and lot facts that can be trusted for a decision.

**Verified Fact.** BO-02 working answer. The two headline business measures are exception cycle time and aged backlog. No target percent is set.

## What this statement does not say

It does not say the fix is a model. It does not say the fix is a rewrite. It does not say a dollar will be saved. Phase 2 decides where a model helps. Later phases decide the design.
