# Open governance decisions

| Field | Value |
|---|---|
| Stage | Phase 0 / 0B Provisional operating contract |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL |
| Evidence sources | `Decision_Tracker.md` sections 4, 5, 5.2, 6, and 7; `Execution_Plan.md` unresolved issues |
| Assumptions | An accepted PROPOSED row is a working answer. It is not a signed decision. |
| Unresolved issues | Every row in the open list below. Owners that are missing are flagged, not invented. |
| Residual risks | A later phase could copy a working answer into code. The tracker forbids that for policy numbers. |

This file lists governance items that are still open. Status values come from `Decision_Tracker.md`. They are not re-derived.

## Phase 0 decisions

| ID | Topic | Status | Working answer | Gap |
|---|---|---|---|---|
| FD-01 | Only the inherited repo is under change | DECIDED | That repo is the only system later phases may change | None |
| FD-02 | Local synthetic data. Read-only model tools | DECIDED | Safety boundary in force | None |
| FD-03 | Eight KPI families from `Execution_Plan.md` section 9 | DECIDED 2026-10-18, authority team-force | Families frozen. Numbers come from tools. No invented targets | None |
| BO-01 | Sign the charter, stakeholder list, and decision rights | PROPOSED. Accepted 2026-10-18 | Adopt the draft charter with the tracker rights | Document unsigned. Named signer Unknown |
| BO-02 | Which business KPIs count as success | PROPOSED. Accepted 2026-10-18 | Exception cycle time and aged backlog are the headlines. The other six families support them | Sheet unsigned. No target percent. Named signer Unknown |

## Later decisions that this contract must not settle

These rows are listed so Phase 0 does not fill them.

| ID | Phase | Owner | Status | Why Phase 0 leaves it |
|---|---|---|---|---|
| BO-03 | 2 | Business Owner | PROPOSED, accepted | AI risk appetite. Used as working context only |
| BO-04 | 3 | Business Owner | PROPOSED, accepted | Initial PRD sign-off |
| BO-06b | 5 | Business Owner | PROPOSED, accepted | Finance and audit meaning of closed |
| BO-08 | 5 | Business Owner | PROPOSED, accepted | Thresholds the governed source does not contain |
| BO-10 | 12 | Business Owner | PROPOSED, accepted | Compliance and classification |
| BO-11 | 14 | Business Owner | PROPOSED, accepted | ROI assumptions |
| BO-12 | 15 | Business Owner | PROPOSED, accepted | Brand assets and final claims |
| BO-13 | 16 | Business Owner | PROPOSED, accepted | As-built baseline |
| FD-04, FD-05 | 2 | Team-Force | PENDING | AI versus no-AI. Defaults exist |
| Many later FD rows | 4 to 15 | Team-Force | PENDING or DECIDED with ADRs still to write | Not a Phase 0 decision |

## Unresolved owners

These are gaps. No name is invented.

| Gap | What is missing | Evidence |
|---|---|---|
| G-01 | Named person who signs BO-01 and BO-02 artifacts | Tracker rows stay PROPOSED |
| G-02 | Company job titles for the six run-time roles | BO-09 is DECIDED for standard names. Company match is open |
| G-03 | Follow-up owner for INC-2025-014 | `operations/incidents/INC-2025-014.md` |
| G-04 | Named person who may run `generate --reset` on the working copy | No file names that person |
| G-05 | Named person who supplies Birlasoft brand assets | `Execution_Plan.md` unresolved issues; BO-12 |

## Material finding

**Finding.** Phase 0 can run on working answers. Two required Business Owner artifacts stay unsigned. Several owners are Unknown.
**Evidence.** `Decision_Tracker.md` section 5.2 and section 6 Phase 0 row.
**Impact.** Engagement is a Conditional Go, not a signed Go.
**Risk.** Treating BO-01 or BO-02 as DECIDED would hide the unsigned documents.
**Confidence.** High.
**Open questions.** G-01 through G-05.
