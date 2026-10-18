# Approval-authority map

| Field | Value |
|---|---|
| Stage | Phase 0 / 2 Stakeholders |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL |
| Evidence sources | `Decision_Tracker.md` sections 5 and 7; BO-03, BO-09; `docs/00-preflight/operating-contract/provisional-human-approval-rules.md`; `Project_Intent.md` section 10.3 |
| Assumptions | BO-03 working answer holds: a person approves every record-changing action |
| Unresolved issues | Company titles Unknown. Named approvers Unknown |
| Residual risks | Coding an approval to a made-up user would invent an owner |

## Delivery approvals

| Artifact or action | Authority | Sign-off state today |
|---|---|---|
| Team charter | Business Owner (BO-01) | Accepted. Document unsigned |
| KPI baseline sheet | Business Owner (BO-02) | Accepted. Document unsigned |
| Phase unit output | Reviewer (FD-24) | Not this agent's job |
| Engineering ADR | Team-Force | Later phases |
| Industry-fact rule card | FDE SME | Later phases |
| Company-liability policy number | Business Owner | PROPOSED rows never written into code |
| Live model key | Human | Not used in Phase 0 |

## Live-case approvals (future apps)

| Action | Approver role | Cannot approve | Gap |
|---|---|---|---|
| Record-changing action proposed by an agent | Shift Lead or Process Engineer (Approver) | The proposing agent. The proposer of an action is never its approver (BO-09) | Person Unknown |
| Recipe-mismatch case | Process Engineer | Operations Analyst acting alone | Person Unknown |
| Overlapping-policy pick | Policy Owner | The model | Person Unknown |
| Drop a replay duplicate | Operations Analyst | An unattended job | Person Unknown |
| HOLD_FOR_REVIEW disposition | Fab Exception Reviewer | The model | Person Unknown |
| Assign missing incident owner | Operations Lead | No current person. INC-2025-014 owner is Unknown | Person Unknown |

## Authority that is not approval

**Verified Fact.** Numeric KPI calculation, schema validation, and duplicate detection stay deterministic (`Project_Intent.md` section 10.2). Those paths do not wait on a person once the rule is governed.

**Verified Fact.** OPA later returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK (`Execution_Plan.md` section 4). That gate is Team-Force design (FD-16, PENDING). This page does not design it.

## Gaps

Unresolved owners are G-01, G-02, and G-03. They stay gaps.
