# Stakeholder map

| Field | Value |
|---|---|
| Stage | Phase 0 / 2 Stakeholders |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE with owner gaps flagged |
| Evidence sources | `Project_Intent.md` section 3.2; `docs/business-context.md`; `Decision_Tracker.md` sections 1 and 7; `domain.json`; `operations/incidents/INC-2025-014.md` |
| Assumptions | The fictional company names in the inherited docs are synthetic |
| Unresolved issues | Named people are Unknown. Company job titles for run-time roles are unconfirmed. INC-2025-014 follow-up owner is Unknown |
| Residual risks | Mapping a role to a real employee name would invent an owner |

## Delivery stakeholders

| Stakeholder | Interest | Decision right | Named person | Label |
|---|---|---|---|---|
| Team-Force | Engineering delivery | Group A FD rows | Role only. No personal name in the tracker | Verified Fact of the role |
| FDE SME (Semiconductor) | Industry fact | BO-05, BO-06a, BO-07, BO-09 | Role only | Verified Fact of the role |
| Business Owner | Company liability | Group B rows | Unknown | Unknown person |
| Coordinator | Orchestrate the run | Does not write artifacts | Agent role | Verified Fact |
| Executor | Build one unit | May record a team-force engineering decision | This unit: Grok 4.6 | Verified Fact |
| Reviewer | Accept Team-Force output | Never signs Group B | Composer 2.5 later | Verified Fact |

## Operating stakeholders (fictional company)

**Verified Fact.** `Project_Intent.md` section 3.2 and `docs/business-context.md`.

| Stakeholder | Primary concern | Capstone outcome they care about | Named person |
|---|---|---|---|
| Fab operations lead | Throughput, handling time, case quality | Prioritized queues and explainable evidence | Unknown |
| Enterprise application owner | Uptime, interfaces, release process | Contracts, observability, rollback | Unknown |
| Finance partner | Case cost and avoidable rework | Comparable cost definitions | Unknown |
| Risk and security partner | Authorization, retention, audit | Identity, provenance, approvals | Unknown |
| Integration lead | Delivery semantics and reconciliation | Idempotency, replay, data contracts | Unknown |
| Domain quality and engineering | Recipe, metrology, tool and lot correctness | Canonical semantics and lineage | Unknown |

**Verified Fact.** `domain.json` owner label is "Fab operations". That is a field in a synthetic file. It is not a named person.

## Run-time roles

**Verified Fact.** `Decision_Tracker.md` section 7.

| Role | Live case duty | Company title confirmed | Named person |
|---|---|---|---|
| Fab Exception Reviewer | RT-01 | No. Gap | Unknown |
| Shift Lead or Process Engineer (Approver) | RT-02 | No. Gap | Unknown |
| Process Engineer | RT-03 | No. Gap | Unknown |
| Policy Owner | RT-04 | No. Gap | Unknown |
| Operations Analyst | RT-05 | No. Gap | Unknown |
| Operations Lead | RT-06 | No. Gap | Unknown |

## Incident gap

**Verified Fact.** `operations/incidents/INC-2025-014.md`. Follow-up owner unknown. Root cause disputed between application and integration teams.

That gap is G-03 in `open-governance-decisions.md`. RT-06 will assign an owner later, inside the app. This phase does not invent one.

## Material finding

**Finding.** Stakeholders are named as roles. People are not named. Several required owners are Unknown.
**Evidence.** Tables above. `Decision_Tracker.md`. INC-2025-014.
**Impact.** The map is complete enough to qualify. Approvals stay with roles, not invented names.
**Risk.** Filling a name to make the map look finished.
**Confidence.** High.
**Open questions.** Who signs BO-01 and BO-02. Who owns INC-2025-014. Which company titles match the SME map.
