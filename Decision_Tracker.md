# Decision Tracker — Sprint 4 Fabpulse Capstone

| Field | Value |
|---|---|
| Stage | Method layer. Runs beside `Execution_Plan.md`. |
| Date / version | 2026-10-18, v1.7 |
| Author | Mangesh (FDE, Team-Force), drafted with Cursor |
| Status | ACTIVE |
| Purpose | One list of every decision the project must make. It says who decides, at which phase, and what happens if the decision is still open. |
| Linked files | `Execution_Plan.md` (the 17 phases, 0 to 16), `Project_Intent.md` (the brief). |

## 1. What this file is

This file lists every decision the project depends on. It splits the decisions into three groups.

- Group A: decisions the FDE team (Team-Force) makes. These are engineering and method choices.
- Group B: decisions the Business Owner makes. These are policy and business-meaning choices.
- Group C: decisions made at run time, inside the live application, by a named role.

Each decision has an owner, the phase where it should be settled, a status, and a default that holds until it is settled.

### Owner roles

| Owner | Who | Decides |
|---|---|---|
| Team-Force | The FDE team. | Engineering and method choices: schema, pipelines, tests, platform, agent design. |
| FDE SME (Semiconductor) | The designated fab-industry expert. Team-Force has no in-house SME, so this role fills that gap. | Industry facts and standard practice: the system of record under SEMI-style process traceability, site and region hierarchy, the standard exception-handling roles, the operational meaning of fab status terms. |
| Business Owner | The customer's accountable owner. | Company-specific choices with liability: the charter, which KPIs count, risk appetite, compliance duties, ROI assumptions, and the finance or audit consequences of a status. |

The SME and the Business Owner draw a clear line. The SME decides what is true of the industry. The Business Owner decides what is true of this company. Industry expertise does not transfer company liability. So where a term has an industry-standard operational meaning but also drives money or audit, the SME sets the operational meaning and the Business Owner confirms the money and audit consequence.

## 2. How each phase uses this file

Before a phase starts, open this file and read the stage-entry checklist in section 6.

- List every decision that the phase needs and that is still `PENDING`.
- Ask the owner for each one. Record the answer, change the status to `DECIDED`, and note the date and the source.
- If a blocking decision stays open, the phase does not start. It waits, or it runs under the stated default and the decision is marked `DEFERRED` with that default in force.
- A `DEFERRED` business-policy decision never becomes a silent value in code. The affected cases route to HOLD_FOR_REVIEW until the owner decides.
- Every Business Owner decision must be shown with the SME recommendation beside it. This is mandatory. The owner does not sign a Group B row until the matching SME recommendation in section 5.1 is in front of them. The stage-entry step displays both together.
- Before the run starts, the SME pre-fills every Business Owner row with its recommended answer, marked PROPOSED, and the owner reviews them all once in the section 5.2 sheet. After that one review, a PROPOSED row does not pause the run; the PROPOSED answer holds until the owner signs it DECIDED. A policy value behind a PROPOSED row is still never written into code; the affected cases route to HOLD_FOR_REVIEW. The run pauses for a Business Owner row only if the owner rejects a PROPOSED answer or the SME cannot propose one.

## 3. Status legend

| Status | Meaning |
|---|---|
| DECIDED | The owner gave the answer. The row names the date and the source. |
| PENDING | No answer yet. The phase that needs it must ask before it starts. |
| DEFERRED | No answer yet, but the phase may run under the stated default. The default holds until the owner decides. |
| PROPOSED | The SME filled in a recommended answer for a Business Owner row. It is not signed. The Business Owner reviews all PROPOSED rows once, before the run, in the section 5.2 sheet. Until the owner signs, the PROPOSED answer holds and the run does not pause at that row. A policy value behind a PROPOSED row is never written into code; the affected cases still route to HOLD_FOR_REVIEW. |

## 4. Group A — FDE team (Team-Force) decisions

These are engineering and method choices. Team-Force owns them. Each one becomes an ADR or a documented method note.

| ID | Decision | Phase | Status | Default until decided |
|---|---|---|---|---|
| FD-01 | The inherited repo is the only system under change. | 0 | DECIDED | — |
| FD-02 | Safety boundary: all data is local and synthetic; the model gets read-only tools only. | 0 | DECIDED | — |
| FD-03 | The baseline KPI set to reproduce and freeze. | 0 | PENDING | Use the KPIs named in `Project_Intent.md` section 9. |
| FD-04 | Per capability, use GenAI, deterministic code, or neither. | 2 | PENDING | Deterministic code, until the AI-qualification note is written. |
| FD-05 | Accept or reject machine learning, from the null test on the `engineering_hold` column in `wafer_lots` (`data/legacy.sqlite3`). | 2 | PENDING | Reject ML. |
| FD-06 | The locked architecture: two apps, YAML built into one SQLite file, an `edges` table instead of a graph server, LangGraph `interrupt()`, OPA gates, fixed ports, App B reads only the lake. | 4 | DECIDED | — (ADRs still to be written) |
| FD-07 | The lake item schema and the five contract gates. | 5 | PENDING | — (phase 5 cannot start without it) |
| FD-08 | Which rule source is canonical and which legacy variants are deviations. | 5 | DECIDED | Governed, effective-dated archive is canonical; four legacy variants are deviations with parity tests. |
| FD-09 | The cross-system mapping design for region, status, and recipe. | 5 | PENDING | — |
| FD-10 | The golden-question set and the injection-test corpus. | 5 | PENDING | — |
| FD-11 | API and event contracts, error semantics, and SLOs. | 6 | PENDING | — |
| FD-12 | The characterization-test approach and the strangle order. | 7 | PENDING | Feed intake first, then reconciliation, then rule evaluation. |
| FD-13 | The platform stack: identity, CI/CD, observability, and compose. | 8 | PENDING | — |
| FD-14 | App A groundedness and abstention thresholds. | 9 | PENDING | — |
| FD-15 | Agent bounds: the tool allow-list, the recursion limit, and the checkpoint store. | 10 | PENDING | — |
| FD-16 | The OPA policy rules that return EXECUTE, HOLD_FOR_REVIEW, or BLOCK. | 10 | PENDING | — |
| FD-17 | The parity-harness design for the two-app comparison. | 11 | PENDING | — |
| FD-18 | The threat model, RBAC/ABAC design, eval thresholds, and the hallucination KPI target. | 12 | PENDING | — |
| FD-19 | Reliability, DLQ and replay, BCDR, SLOs, and FinOps design. | 13 | PENDING | — |
| FD-20 | The honesty label on each KPI. | 14 | DECIDED | Labels set in `Execution_Plan.md` section 9; confirm at phase 14. |
| FD-21 | The 40-minute demo flow, the replay mode, and the lessons learned. | 15 | PENDING | — |
| FD-22 | The Context Lake review-loop and version policy: how the review, fix, and revision loop runs and how the version is raised. | 5 | PENDING | One review round before Phase 6; the version starts at 1.0.0; a later change goes through the loop and raises the version with an ADR. |
| FD-23 | The audit-chain design: the correlation-id row schema and the read-by-correlation-id path. | 10 | PENDING | One audit row per agent step and per human approval, keyed by a correlation id, with a read that returns the full trace for one case. |
| FD-24 | Who accepts Team-Force output before the run advances. | all | DECIDED | A separate reviewer agent accepts for Team-Force. It runs on Composer 2.5 (`composer-2.5-fast`), reads the files on disk, and is a fresh agent, never a resume of the builder. It accepts Half A before Half B on the build phases (5, 7, 8, 9, 10, 11, 12, 13), and it accepts the finished stage on every phase by checking the Expected output and running the Done test. It never signs a Group B row. An unresolvable block, a Business Owner row, or a Done test that needs a credential or a running service escalates to a human. See `playbook/reviewer.md`. |
| FD-25 | Who builds the phase output. | all | DECIDED | A separate executor agent builds each unit of work. It runs on Grok 4.6 (`cursor-grok-4.6-high-fast`), reads the inputs on disk, and is a fresh agent per unit. The coordinator runs on Grok 4.7 (`grok-4.7-high-fast`). One unit is a document phase, one half of a build phase, or one half of a hardening sub-stage. The coordinator orchestrates and settles the SME and Business Owner decisions before spawning the executor; it writes no artifact itself. The executor may make an engineering design decision the build requires, marks it `authority: team-force`, and returns it for the coordinator to log. It does not set a Business Owner or SME policy value; an unresolved policy value routes to HOLD_FOR_REVIEW. The executor is not the reviewer, so the builder never checks its own work. See `playbook/executor.md`. |

## 5. Group B — Business Owner decisions

These are policy and business-meaning choices. The owner column says who decides each one. Rows owned by the SME are now settled using fab-industry standard practice. Rows owned by the Business Owner still need a company sign-off, because they carry company liability.

| ID | Decision | Phase | Owner | Status | Answer or default |
|---|---|---|---|---|---|
| BO-01 | Sign off the charter, the stakeholder list, and the decision rights. | 0 | Business Owner | PROPOSED | Proceed on the draft charter; mark it unsigned. |
| BO-02 | Which business KPIs count as success. | 0 | Business Owner | PROPOSED | Use the KPI families in `Project_Intent.md` section 9. |
| BO-03 | How much risk is acceptable for places where AI may act. | 2 | Business Owner | PROPOSED | AI explains and proposes; a person approves every action. |
| BO-04 | Sign off the initial PRD: users, workflows, AI limits, and the demo flow. | 3 | Business Owner | PROPOSED | PROPOSED (SME): approve the initial PRD once it names both apps, the AI limits, the eight business problems, and the demo flow, and nothing beyond. See 5.1 and 5.2. |
| BO-05 | The authority for the `recipe_release` limit. | 5 | FDE SME | DECIDED | In a fab, process and recipe change control is the system of record under SEMI-style traceability. The governed, effective-dated archive (`contracts/decision-policies-archive.json` and `policy_register`) is canonical. The four legacy variants are deviations. |
| BO-06a | The operational meaning of "open" and "closed" for a fab exception case. | 5 | FDE SME | DECIDED | A case is "open" while any disposition or engineering action is still pending, including REVIEW and HOLD states. A case is "closed" only when a final disposition is recorded and no engineering action is pending. This makes the night batch wrong to treat REVIEW as closed-equivalent. |
| BO-06b | Whether operational "closed" also means finance-booked and audit-closed, or those differ. | 5 | Business Owner | PROPOSED | Keep the three meanings separate in the semantic layer. A case that is operationally closed but not finance or audit closed routes to review. No single coded value. |
| BO-07 | The canonical region vocabulary: APAC/EMEA/AMER, country codes, or site codes. | 5 | FDE SME | DECIDED | The site code is the canonical key. Country and region are derived attributes mapped from the site. A policy binds at the most specific scope and inherits upward. Where two scopes disagree, the case routes to review. |
| BO-08 | Confirm any threshold that the governed source does not contain. | 5 | Business Owner | PROPOSED | The SME may suggest an industry-typical value, but it stays PROPOSED and is not used live until the owner confirms, because the exact number is company risk appetite. |
| BO-09 | Role permissions: who may approve, hold, or block each action type. | 6 | FDE SME | DECIDED | The SME sets the standard fab exception-handling roles and separation of duties (see Group C). The proposer of an action is never its approver. The company confirms its own job titles match this map. |
| BO-10 | Compliance obligations and data classification. | 12 | Business Owner | PROPOSED | Treat all records as internal and synthetic. |
| BO-11 | Sign off the ROI assumptions. | 14 | Business Owner | PROPOSED | Label ROI numbers EDUCATIONAL; no claimed benefit. |
| BO-12 | Provide the Birlasoft brand assets and sign off the final claims. | 15 | Business Owner | PROPOSED | Use the neutral placeholder deck. |
| BO-13 | Sign off the final as-built baseline: the requirement dispositions and the known limitations. | 16 | Business Owner | PROPOSED | Proceed on the as-built PRD and mark it unsigned until the owner signs. |

### 5.1 SME recommendation to the Business Owner (mandatory to show)

The Business Owner must see this recommendation before signing each row above. The SME writes it from fab-industry practice. The recommendation is advice; the sign-off stays with the owner.

| ID | SME recommendation | Why |
|---|---|---|
| BO-01 | Adopt the draft charter as written, with the decision rights in this tracker: Team-Force owns engineering, the SME owns industry fact, the Business Owner owns liability, run-time roles own single cases. | A clear split now prevents the four-way rule drift the project exists to end. |
| BO-02 | Make exception cycle time and aged backlog the two headline business KPIs. Keep the other six families as engineering and AI-quality measures. | These two track the backlog and the delay the fab feels. The rest are supporting evidence. |
| BO-03 | AI explains and proposes. A person approves every action that changes a record. No autonomous writes. | A wrong auto-action in a fab can scrap material. Human approval caps that risk at review, not loss. |
| BO-04 | Approve the initial PRD once it names both apps, the AI limits, the eight business problems, and the demo flow, and nothing beyond them. | Scope held to the evidenced defects keeps the build demoable on the laptop and honest. |
| BO-06b | Keep operational, finance, and audit closure as three separate states. Operational closure does not auto-book finance or close the audit. A case moves to finance-closed only on a recorded finance action. | This is the audit-safe choice. It prevents a backlog number from silently booking revenue. |
| BO-08 | Do not invent a number where the governed source is silent. Route the case to review. If a value is needed for the demo, use the most conservative legacy value, the Python 50,000 cutoff, marked PROPOSED. Never use the 999,999 default. | The 999,999 default passes almost everything and hides risk. The conservative value fails safe. |
| BO-10 | For the capstone, treat all records as internal and synthetic. Apply the standard fab template: process data is confidential, and there is no personal data. | Sets a safe handling baseline without waiting on a formal classification. |
| BO-11 | Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit. | The data is synthetic. An EDUCATIONAL label keeps the claim honest and defensible to judges. |
| BO-12 | Build the deck on the neutral placeholder until the official Birlasoft assets arrive, then restyle. Give every claim an honesty label. | Branding should not block rehearsal. Labels keep the final claims defensible. |
| BO-13 | Sign the as-built baseline once every requirement is classified Delivered, Changed, Deferred, Rejected, or Superseded with evidence, and the known limitations are listed. | A signed as-built baseline is what operations, audit, and future change rely on. An unsigned one leaves ownership unclear. |

### 5.2 One-time Business Owner review sheet

Review this sheet once, before the run. Each row carries the SME's PROPOSED answer. Mark each row Accept or Reject. An accepted row holds as the working answer and the run does not pause at it; sign it DECIDED when you are ready. A rejected row becomes a pause point: the coordinator stops at that phase and waits for your answer.

| ID | Phase | The PROPOSED answer the SME recommends | Your call (Accept / Reject) |
|---|---|---|---|
| BO-01 | 0 | Adopt the draft charter with the decision rights in this tracker: Team-Force owns engineering, the SME owns industry fact, the Business Owner owns liability, run-time roles own single cases. | |
| BO-02 | 0 | Make exception cycle time and aged backlog the two headline business KPIs; keep the other six families as supporting measures. | |
| BO-03 | 2 | AI explains and proposes; a person approves every record-changing action; no autonomous writes. | |
| BO-04 | 3 | Approve the initial PRD once it names both apps, the AI limits, the eight business problems, and the demo flow, and nothing beyond. | |
| BO-06b | 5 | Keep operational, finance, and audit closure as three separate states; operational closure does not book finance or close audit; a mismatch routes to review. | |
| BO-08 | 5 | Do not invent a number where the governed source is silent; route the case to review; if a demo value is needed, use the Python 50,000 cutoff marked PROPOSED, never 999,999. | |
| BO-10 | 12 | Treat all records as internal and synthetic; process data confidential; no personal data. | |
| BO-11 | 14 | Label every ROI number EDUCATIONAL; state each assumption; claim no monetary benefit. | |
| BO-12 | 15 | Build the deck on the neutral placeholder until the Birlasoft assets arrive, then restyle; label every claim. | |
| BO-13 | 16 | Sign the as-built baseline once every requirement is classified with evidence and the known limitations are listed. | |

## 6. Stage-entry checklist

Before a phase starts, confirm these decisions. A `PENDING` entry in this list is a blocker unless the row's default is accepted and the entry is set to `DEFERRED`.

| Phase | Must be settled before start | Owner |
|---|---|---|
| 0 Frame and baseline | FD-01, FD-02, FD-03, BO-01, BO-02 | Team-Force, Business Owner |
| 1 Discovery | FD-03 | Team-Force |
| 2 AI vs no-AI | FD-04, FD-05, BO-03 | Team-Force, SME, Business Owner |
| 3 Initial PRD | BO-02, BO-03, BO-04 | Business Owner |
| 4 Architecture + ADRs | FD-06 | Team-Force |
| 5 Context Lake core | FD-07, FD-08, FD-09, FD-10, FD-22, BO-05, BO-06a, BO-06b, BO-07, BO-08 | Team-Force, SME, Business Owner |
| 6 Specs + contracts | FD-11, BO-09 | Team-Force, SME |
| 7 Transform repo | FD-12 | Team-Force |
| 8 Foundations | FD-13 | Team-Force |
| 9 App A | FD-14 | Team-Force |
| 10 Agents + HITL + audit chain | FD-15, FD-16, FD-23, BO-09 | Team-Force, SME, Business Owner |
| 11 App B from lake | FD-17 | Team-Force |
| 12 Security + governance + TEVV | FD-18, BO-10 | Team-Force, Business Owner |
| 13 Production hardening | FD-19 | Team-Force |
| 14 Compare + ROI | FD-20, BO-11 | Team-Force, Business Owner |
| 15 TOM + defence | FD-21, BO-12 | Team-Force, Business Owner |
| 16 Final As-Built PRD | BO-13 | Business Owner |

## 7. Group C — Live application and workflow decisions

These decisions happen at run time, after the apps are built. A person in a named role makes each one inside the app. The app does not decide these on its own; it presents the case and records who chose.

These are not policy changes. The policy is fixed in the lake. Each row below is one person applying that policy to one case. Changing the policy itself follows Group B and a new governed, versioned record.

| ID | Run-time decision | Role | Where it happens |
|---|---|---|---|
| RT-01 | Dispose a case that routed to HOLD_FOR_REVIEW. | Fab Exception Reviewer | App A and App B review queue |
| RT-02 | Approve, hold, or block an agent-proposed action at the gate. | Shift Lead or Process Engineer (Approver) | App A approval gate |
| RT-03 | Approve a recipe-mismatch case (scenario 8). | Process Engineer | App A triage |
| RT-04 | For an overlapping-policy case, accept the abstain or pick a policy (scenario 10). | Policy Owner | App A review |
| RT-05 | Confirm a replay duplicate before it is dropped (scenario 7). | Operations Analyst | App A intake |
| RT-06 | Assign the follow-up owner for an incident with no owner (BP8, INC-2025-014). | Operations Lead | App A exception handling |

A note on roles. The SME set these role names as the standard fab exception-handling map under BO-09. The Business Owner's remaining task is only to confirm the company's own job titles match this map, not to design it.

## 8. Change log

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-17 | First issue. 21 FDE decisions, 12 Business Owner decisions, 6 run-time role decisions, and the stage-entry checklist. |
| v1.1 | 2026-10-17 | Added the FDE SME (Semiconductor) owner role. The SME now decides industry-fact rows: BO-05 (recipe authority), BO-06a (operational meaning of open/closed), BO-07 (site as canonical key), BO-09 (standard roles). Split BO-06 into BO-06a (SME, operational) and BO-06b (Business Owner, finance and audit). Company-liability rows stay with the Business Owner. |
| v1.2 | 2026-10-17 | Added section 5.1: a mandatory SME recommendation for every Business Owner decision. The owner must see the recommendation before signing. The stage-entry step shows both together. |
| v1.3 | 2026-10-17 | Spine-alignment rehaul. Added FD-22 (Context Lake review loop and version policy, Phase 5), FD-23 (audit-chain design, Phase 10), and BO-13 (final as-built baseline sign-off, Phase 16, with its 5.1 recommendation). Added the Phase 16 stage-entry row and updated the Phase 5 and 10 rows. |
| v1.4 | 2026-10-17 | Added FD-24: a separate reviewer agent accepts Team-Force output. It runs on GPT 5.6-Sol as a fresh agent, accepts Half A before Half B on the build phases, and accepts the finished stage on every phase by checking the Expected output and running the Done test. It never signs a Business Owner row; an unresolvable block or a test that needs a person escalates to a human. Matches the two-agent playbook and `Execution_Plan.md` v1.7. |
| v1.6 | 2026-10-18 | Added FD-25: a separate executor agent builds each unit of work. It runs on Claude Sonnet 5.5 as a fresh agent per unit; the coordinator orchestrates and settles decisions but writes no artifact; the executor is not the reviewer. Matches the three-agent playbook and `Execution_Plan.md` v2.0. |
| v1.7 | 2026-10-18 | Changed the run models. FD-24 now names Composer 2.5 (`composer-2.5-fast`) as the reviewer. FD-25 now names Grok 4.6 (`cursor-grok-4.6-high-fast`) as the executor. The coordinator runs on Grok 4.7 (`grok-4.7-high-fast`). |
| v1.5 | 2026-10-17 | Added the PROPOSED status and section 5.2, a one-time Business Owner review sheet. The SME pre-filled every Business Owner row (BO-01, BO-02, BO-03, BO-04, BO-06b, BO-08, BO-10, BO-11, BO-12, BO-13) with its recommended answer, marked PROPOSED, so the owner reviews them once before the run. After that review an accepted PROPOSED row does not pause the run; a rejected row stays a pause point. A policy value behind a PROPOSED row is still never written into code. Updated the coordinator pause rules to match. |
