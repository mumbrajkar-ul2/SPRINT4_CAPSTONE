# Provisional operating contract

| Field | Value |
|---|---|
| Stage | Phase 0 / 0B Provisional operating contract |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL. Unsigned. BO-01 accepted 2026-10-18 and not signed DECIDED |
| Evidence sources | `Decision_Tracker.md` sections 1, 4, 5, 5.1, 5.2, 6, and 7; `Execution_Plan.md` sections 4, 5, and 11; `Project_Intent.md` sections 3 and 12 |
| Assumptions | The Business Owner accepted the draft charter rights on 2026-10-18. That acceptance is the working answer until the owner signs the document. |
| Unresolved issues | The named person who will sign this contract is Unknown. Company job titles that match the SME role map are unconfirmed. |
| Residual risks | A later phase could treat this working answer as a signed policy. The status on this page stays PROVISIONAL until the owner signs. |

This contract is the working agreement for how the capstone is run. It is not signed.

## Parties and rights

**Verified Fact.** `Decision_Tracker.md` section 1 and the BO-01 working answer split rights this way.

| Party | What this party decides | Status |
|---|---|---|
| Team-Force | Engineering and method. Schema, pipelines, tests, platform, agent design | Working. FD-01, FD-02, FD-03 are DECIDED |
| FDE SME (Semiconductor) | Industry fact. System of record under SEMI-style process traceability. Site and region hierarchy. Standard exception-handling roles. Operational meaning of fab status words | Working. BO-05, BO-06a, BO-07, BO-09 are DECIDED |
| Business Owner | Company liability. Charter, which KPIs count, risk appetite, compliance, ROI, finance and audit meaning of a status | Working answers accepted 2026-10-18. Rows stay PROPOSED until the owner signs |
| Run-time roles | One live case. Dispose, approve, hold, block, confirm a replay, assign a follow-up owner | Roles named in `Decision_Tracker.md` section 7. No live app yet |

**Verified Fact.** Industry expertise does not transfer company liability. The SME sets what is true of the industry. The Business Owner sets what is true of this company.

## Working answers already accepted

**Verified Fact.** On 2026-10-18 the Business Owner accepted every row on the section 5.2 sheet. The run does not pause at an accepted PROPOSED row. A policy number behind a PROPOSED row is never written into code. Affected cases route to HOLD_FOR_REVIEW.

Phase 0 working answers:

- BO-01. Adopt this draft charter with the rights above. The charter document stays unsigned.
- BO-02. Exception cycle time and aged backlog are the two headline business KPIs. The other six families are supporting measures.

## How work is built and checked

**Verified Fact.** `Execution_Plan.md` section 11 and FD-24 / FD-25.

- The coordinator (Grok 4.7) orchestrates and settles decisions. It writes no artifact.
- A fresh executor (Grok 4.6) builds one unit.
- A fresh reviewer (Composer 2.5) checks the files on disk. The builder is not the checker.
- The reviewer never signs a Business Owner row.
- Phases 0 to 6 change no application behaviour.
- New files are written at the capstone root. Only Phase 7 edits files inside the inherited repo.

## Safety boundary

**Verified Fact.** FD-02. All data is local and synthetic. The model gets read-only tools only.

**Verified Fact.** `Project_Intent.md` section 10.2. Authorization, state transitions, numeric KPIs, and final reconciliation stay deterministic. AI-generated text does not become a source-of-record fact.

## Reconciliation

This contract is reconciled with `docs/02-stakeholders/decision-rights-map.md` and `docs/02-stakeholders/operating-contract-confirmations.md`. Those files use the same rights and the same PROVISIONAL status.

## What remains open

**Unknown.** Named signer of this document.

**Unknown.** Company job titles for Fab Exception Reviewer, Shift Lead, Process Engineer, Policy Owner, Operations Analyst, and Operations Lead.

Flag those gaps. Do not invent names.
