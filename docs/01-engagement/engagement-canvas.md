# Engagement canvas

| Field | Value |
|---|---|
| Stage | Phase 0 / 1 Engage and qualify |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE for orientation. Charter still unsigned |
| Evidence sources | `Project_Intent.md` sections 1, 3, and 8; `Execution_Plan.md` sections 2, 3, and 4; `Decision_Tracker.md`; `docs/business-context.md`; `domain.json`; baseline tool runs |
| Assumptions | The fictional customer is Fabpulse Group. All people and company records are synthetic |
| Unresolved issues | Named Business Owner signer Unknown. Company job titles Unknown. Birlasoft brand assets not in hand |
| Residual risks | The assignment is a training capstone. Treating it as a live fab engagement would over-claim |

## Why this engagement exists

**Verified Fact.** `docs/business-context.md` and `Project_Intent.md` section 3.1. Fabpulse Group is a fictional multi-region semiconductor organization. The operating concern is rising effort and inconsistency in fab-lot and equipment-exception handling.

**Verified Fact.** `domain.json` names the workflow "Fab lot and equipment exception tracking" and the owner label "Fab operations".

**Verified Fact.** `Project_Intent.md` section 1. The repository is a production-shaped legacy simulator. It is not the target architecture. It does not contain a finished AI solution.

## Who is served

| Stakeholder | Primary concern | Source | Label |
|---|---|---|---|
| Fab operations lead | Throughput, handling time, case quality | `Project_Intent.md` 3.2, `docs/business-context.md` | Verified Fact |
| Enterprise application owner | Uptime, interfaces, release process | same | Verified Fact |
| Finance partner | Case cost and avoidable rework | same | Verified Fact |
| Risk and security partner | Authorization, retention, audit evidence | same | Verified Fact |
| Integration lead | Delivery semantics and reconciliation | same | Verified Fact |
| Domain quality and engineering | Recipe, metrology, tool and lot correctness | `Project_Intent.md` 3.2 | Verified Fact |
| Team-Force | Engineering delivery of this capstone | `Decision_Tracker.md` | Verified Fact |
| FDE SME (Semiconductor) | Industry fact | `Decision_Tracker.md` | Verified Fact |
| Business Owner | Company liability | `Decision_Tracker.md` | Verified Fact |

## What success looks like for this engagement

**Verified Fact.** `Project_Intent.md` section 17.4 and `Execution_Plan.md` section 2.

- Two independently useful applications run the same fab-exception workflow.
- The eight defects BP1 to BP8 are shown with evidence.
- The eight KPI families are compared with honesty labels.
- The Context Lake holds versioned, evidence-backed items.
- Agents are bounded and a person approves record-changing actions.
- The live defence fits 40 minutes plus 10 minutes of questions.

**Verified Fact.** BO-02 working answer. The two headline business KPIs are exception cycle time and aged backlog. No target percent is set.

## What this engagement will not do

**Verified Fact.**

- Change the inherited repo in Phases 0 to 6.
- Use real production data or write tools for the model (FD-02).
- Invent a KPI target or a dollar benefit.
- Sign the charter or the KPI sheet in this unit (BO-01 and BO-02 stay unsigned).

## Constraints

**Verified Fact.** Local laptop. Python 3.10+. Packaged 125-case database. Ports 8080, 8090 now. Ports 8091 and 8092 later. Replay mode for the offline demo.

## Qualification pointer

See `engagement-go-no-go.md`. The call on 2026-10-18 is Conditional Go.
