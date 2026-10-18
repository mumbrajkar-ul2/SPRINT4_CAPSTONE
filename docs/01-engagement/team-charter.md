# Team charter

| Field | Value |
|---|---|
| Stage | Phase 0 / 1 Engage and qualify |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | UNSIGNED / PROVISIONAL. BO-01 accepted 2026-10-18 and not signed DECIDED |
| Evidence sources | `Decision_Tracker.md` sections 1, 5.1, 5.2, and 7; BO-01; `Execution_Plan.md` section 11; FD-24; FD-25 |
| Assumptions | The accepted working answer is the text of this charter. The owner has not signed the document |
| Unresolved issues | Named signer Unknown. Company job titles for run-time roles unconfirmed |
| Residual risks | A later phase could treat this unsigned charter as a signed policy |

This charter is the draft BO-01 asked the Business Owner to adopt. The owner accepted the draft on 2026-10-18. The owner has not signed this file. Status stays UNSIGNED / PROVISIONAL.

## Purpose

Run the Sprint 4 Fabpulse capstone. Freeze the inherited baseline. Then discover, specify, and later build two independently useful applications over one Context Lake. Keep industry fact, company liability, and engineering in separate hands.

## Decision rights

Copied from `Decision_Tracker.md`. Not re-derived.

| Party | Decides | Does not decide |
|---|---|---|
| Team-Force | Engineering and method. Schema, pipelines, tests, platform, agent design. FD rows | Industry fact. Company liability. A live case disposition |
| FDE SME (Semiconductor) | Industry fact. System of record under SEMI-style process traceability. Site as canonical key. Standard roles. Operational open and closed | Company finance or audit meaning. Engineering stack |
| Business Owner | Company liability. This charter. Which KPIs count. Risk appetite. Compliance. ROI. Finance and audit consequence of a status | Engineering design. Industry-standard operational meaning |
| Run-time roles | One live case. See the table below | Policy change. That follows Group B and a new governed record |

**Verified Fact.** BO-01 SME recommendation. Adopt the draft charter with these rights. A clear split now prevents the four-way rule drift the project exists to end.

## How delivery roles work

**Verified Fact.** FD-25 and FD-24.

| Role | Model | Duty |
|---|---|---|
| Coordinator | Grok 4.7 | Orchestrates. Settles decisions it owns. Writes no artifact |
| Executor | Grok 4.6 | Builds one unit from the files on disk |
| Reviewer | Composer 2.5 | Accepts Team-Force output. Never signs a Group B row |
| Human | Named later | Supplies keys. Runs `NEEDS_HUMAN` tests. Signs Group B artifacts |

The builder is not the checker.

## Run-time roles (standard map)

**Verified Fact.** `Decision_Tracker.md` section 7 and BO-09.

| Role | Live decision |
|---|---|
| Fab Exception Reviewer | Dispose a HOLD_FOR_REVIEW case |
| Shift Lead or Process Engineer (Approver) | Approve, hold, or block an agent-proposed action |
| Process Engineer | Approve a recipe-mismatch case |
| Policy Owner | Accept an abstain or pick a policy on overlap |
| Operations Analyst | Confirm a replay duplicate |
| Operations Lead | Assign a follow-up owner when none exists |

The proposer of an action is never its approver.

**Unknown.** The company job titles that match these names. Flagged. Not invented.

## Working rules

1. Phases 0 to 6 change no application behaviour.
2. All data is local and synthetic. The model gets read-only tools only.
3. No invented threshold. A silent governed source routes the case to review.
4. Every claim is Verified Fact, Inference, Assumption, or Unknown.
5. Every demo number carries REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.
6. An accepted PROPOSED Business Owner row does not pause the run. The artifact stays unsigned until the owner signs.

## Sign-off block

| Field | Value |
|---|---|
| Business Owner name | Unknown |
| Signature | Not signed |
| Date signed | Not signed |
| Status | UNSIGNED / PROVISIONAL |
| Working acceptance | 2026-10-18, section 5.2 Accept on BO-01 |
