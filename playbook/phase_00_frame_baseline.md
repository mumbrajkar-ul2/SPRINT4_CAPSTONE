# Phase 0 — Frame, govern, and freeze the baseline

> Spine units: 0A, 0B, 0C, 1, 2, 3, 4 | Guidelines 1, 18, 23 | Decision gate: FD-01, FD-02, FD-03, BO-01, BO-02

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test before Phase 1 starts.

## Inputs

- the inherited repo `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` (attach the folder)
- `Project_Intent.md` (users, KPIs, scope)
- `Execution_Plan.md` sections 3, 4, 5, 7, 9
- `Decision_Tracker.md` (section 6 stage-entry row for Phase 0; section 5.1 for BO-01 and BO-02)

## Prompt

```text
# Phase 0 — Frame, govern, and freeze the baseline

## Objective
Orient on the estate, set a provisional operating contract and an economics envelope, qualify the engagement, frame the problem, and freeze the baseline KPIs. Build a source register with a SHA-256 hash for every file. Each sub-stage writes to its own spine folder and has its own sub-gate.

## Scope
Analyse across the whole repo, read only. Exclude: any code change; any app behaviour change.

## Sub-stages
Run these in order. Each has its own folder and sub-gate.
- 0A Pre-flight orientation. `docs/00-preflight/discovery/`: `repository-overview.md`, `system-landscape.md`, `technology-inventory.md`, `high-level-architecture.md`, `assumptions-unknowns.md`, `initial-risk-register.md`. Sub-gate: orientation is enough to qualify, with no transformation recommendations yet.
- 0B Provisional operating contract. `docs/00-preflight/operating-contract/`: `provisional-operating-contract.md`, `scope-boundaries.md`, `repository-write-boundaries.md`, `provisional-human-approval-rules.md`, `stop-conditions.md`, `open-governance-decisions.md`. Sub-gate: boundaries and decision rights recorded as PROVISIONAL; unresolved owners flagged, not invented.
- 0C AI-economics envelope. `docs/00-preflight/ai-economics/`: `workload-assumptions.md`, `solution-scenarios.md`, `provisional-token-budget.md`, `quality-latency-cost-envelope.md`, `preliminary-finops-baseline.md`. Sub-gate: a provisional cost, token, and latency envelope exists; it is marked for reconciliation at Phase 2 and Phase 13.
- 1 Engage and qualify. `docs/01-engagement/`: `engagement-canvas.md`, `team-charter.md`, `qualification-checklist.md`, `engagement-go-no-go.md`. Sub-gate: a Go, Conditional Go, or No-Go with evidence.
- 2 Stakeholders. `docs/02-stakeholders/`: `stakeholder-map.md`, `decision-rights-map.md`, `approval-authority-map.md`, `operating-contract-confirmations.md`. Sub-gate: decision rights reconciled with 0B; unresolved owners recorded as gaps.
- 3 Problem and value. `docs/03-problem-value/`: `problem-statement.md`, `personas.md`, `jobs-to-be-done.md`, `scope-exclusions.md`, `nfrs.md`, `success-criteria.md`. Sub-gate: a technology-neutral problem definition.
- 4 Baseline KPIs. `docs/04-baseline-kpis/`: `kpi-dictionary.md`, `baseline-kpi-sheet.md`, `measurement-methodology.md`, `kpi-baseline-signoff.md`. Plus `sources/register.yaml`. Sub-gate: the baseline reproduces twice with identical numbers; the definitions are frozen.

## Required analysis
Evaluate: who the users and stakeholders are; the current-state KPIs; the incident history and known disputes; the file inventory and its integrity; the decision rights across Team-Force, the SME, the Business Owner, and run-time roles. For every material finding: state the finding, the evidence, the impact, the risk, the confidence, and the open questions.

## Evidence rules
Classify each statement as Verified Fact, Inference, Assumption, or Unknown. Cite file paths, tables, configs, and logs. Do not present an assumption as a fact.

## Constraints and guardrails
Do not modify any file in the repo. Do not run the app in write mode. Do not invent KPI values; read them from the baseline tools. Do not invent owners; flag unresolved ones. If a KPI cannot be reproduced, record it as Unknown. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Repo under change | `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`, the only system changed |
| Ports | 8080 legacy, 8090 gateway, 8091 lake REST, 8092 lake MCP |
| Decision owners | Team-Force (engineering); FDE SME (industry fact); Business Owner (company liability); run-time roles (one live case) |
| Baseline rule | Read KPI values from the baseline tools; never invent one |
| Phase 0 changes | No application behaviour changes in Phases 0 to 6 |

## Decision gate (before you start)
Confirm in `Decision_Tracker.md`: FD-01 and FD-02 are DECIDED; FD-03 adopt the `Project_Intent.md` section 9 set as the default if PENDING; BO-01 and BO-02 are Business Owner calls — if PENDING, pause with a pause card and show the SME recommendations for BO-01 and BO-02.

## Required artifacts
The seven folders above, each artifact with the standard header: stage, date and version, author or agent, status, evidence sources, assumptions, unresolved issues, residual risks.

## Completion gate
Complete only when every sub-gate passes: the baseline reproduces twice, the register lists every file with a hash, the charter names the decision rights, and all artifacts have headers.

## Required final response
Return: 1) PASS / CONDITIONAL PASS / BLOCKED; 2) key findings; 3) major risks; 4) assumptions and unknowns; 5) artifacts created; 6) blocking issues; 7) recommended next action.

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/00-preflight/discovery/*` | Header. Repo overview, landscape, technology inventory, high-level architecture, assumptions and unknowns, initial risks. No transformation recommendation. |
| `docs/00-preflight/operating-contract/*` | Header. Scope, write boundaries, approval rules, stop conditions, open governance decisions, all marked PROVISIONAL. Unresolved owners flagged. |
| `docs/00-preflight/ai-economics/*` | Header. Workload assumptions, scenarios, a provisional token budget, a quality-latency-cost envelope, a preliminary FinOps baseline, marked for reconciliation at Phase 2 and 13. |
| `docs/01-engagement/*` | Header. Engagement canvas, team charter with decision rights, qualification checklist, a Go / Conditional Go / No-Go with evidence. |
| `docs/02-stakeholders/*` | Header. Stakeholder map, decision-rights map reconciled with 0B, approval authority, unresolved owners recorded as gaps. |
| `docs/03-problem-value/*` | Header. Technology-neutral problem statement, personas, jobs-to-be-done, exclusions, NFRs, success criteria. |
| `docs/04-baseline-kpis/*` plus `sources/register.yaml` | Header. KPI dictionary, baseline sheet, measurement method, sign-off. The register lists every repo file with a SHA-256 hash. |

## Done test

Re-run the baseline tool a second time and diff the numbers against the first run; they match. Count the hashes in `sources/register.yaml` and the repo files; the counts are equal. Open any artifact; its header has all eight fields.
