# Decision-rights map

| Field | Value |
|---|---|
| Stage | Phase 0 / 2 Stakeholders |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL. Reconciled with 0B |
| Evidence sources | `docs/00-preflight/operating-contract/provisional-operating-contract.md`; `docs/00-preflight/operating-contract/open-governance-decisions.md`; `Decision_Tracker.md` sections 1, 4, 5, and 7 |
| Assumptions | The 0B contract text is the source this map must match |
| Unresolved issues | Same owner gaps as 0B. Named signer Unknown |
| Residual risks | A later file that restates these rights with a new owner would drift from the tracker |

This map is reconciled with the 0B provisional operating contract. The rights are the same. The status is the same: PROVISIONAL.

## Rights matrix

| Decision class | Example | Owner | Status now | 0B file that states it |
|---|---|---|---|---|
| Engineering / method | KPI family set, lake schema, ports | Team-Force | FD-01, FD-02, FD-03 DECIDED. Later FD rows wait | `provisional-operating-contract.md` |
| Industry fact | Operational open/closed, site key, standard roles, recipe authority | FDE SME | BO-05, BO-06a, BO-07, BO-09 DECIDED | same |
| Company liability | Charter, headline KPIs, finance/audit closed, ROI, brand | Business Owner | Accepted PROPOSED. Artifacts unsigned | same |
| Live case | One disposition, one approval, one replay confirm | Run-time role | Roles named. People Unknown | `provisional-human-approval-rules.md` |
| Team-Force output accept | Half or finished stage | Reviewer agent | FD-24 DECIDED | `provisional-operating-contract.md` |
| Policy value missing | Silent threshold | No one invents it. Case routes to review | BO-08 working answer | `provisional-human-approval-rules.md` |

## Reconciliation check against 0B

| 0B statement | This map | Result |
|---|---|---|
| Team-Force owns engineering | Same | Match |
| SME owns industry fact | Same | Match |
| Business Owner owns liability | Same | Match |
| Run-time roles own one live case | Same | Match |
| Charter unsigned / PROVISIONAL | Same | Match |
| Unresolved owners flagged, not invented | Same. See gaps below | Match |

## Gaps carried from 0B

| Gap | Owner missing | Do not invent |
|---|---|---|
| G-01 | Named signer of BO-01 and BO-02 | A person's name |
| G-02 | Company job titles for the six run-time roles | A local title |
| G-03 | INC-2025-014 follow-up owner | A person's name |
| G-04 | Person who may reset the packaged database | A person's name |
| G-05 | Person who supplies Birlasoft assets | A person's name |

## What this map forbids

A Team-Force agent does not sign a Business Owner row. A Business Owner does not pick the lake schema. The SME does not take company finance liability. A run-time role does not change the governed policy.
