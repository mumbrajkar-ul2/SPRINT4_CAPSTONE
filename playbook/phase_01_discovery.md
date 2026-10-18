# Phase 1 — Discovery and deep brownfield

> Spine units: 5, 6, 7 | Guideline 27 | Decision gate: FD-03

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test before Phase 2 starts.

## Inputs

- the repo code, data, docs, and contracts (attach `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`)
- `contracts/decision-policies-archive.json` and the four rule sources
- Phase 0 artifacts in `docs/00-preflight/`, `docs/03-problem-value/`, `docs/04-baseline-kpis/`
- `Execution_Plan.md` section 3
- `Decision_Tracker.md` (section 6 stage-entry row for Phase 1)

## Prompt

```text
# Phase 1 — Discovery and deep brownfield

## Objective
Map the current process, find the root causes, and assess the repo in depth. Build the conflict catalogue BP1 to BP8 with one reproducible query per conflict. Each sub-stage writes to its own spine folder.

## Scope
Analyse across the application code and API, the four rule sources, the two SQLite databases, the bundled lake tier, the docs, and `contracts/decision-policies-archive.json`. Exclude: any change to code or data.

## Sub-stages
- 5 Current process and landscape. `docs/05-current-state/`: `current-process-map.md`, `system-landscape.md`, `integration-landscape.md`, `brownfield-inventory.md`, `process-bottlenecks.md`, `conflict-catalogue.md` (BP1 to BP8, each with a query and its result). Sub-gate: the end-to-end process is mapped and every conflict has a reproducible query.
- 6 Root cause. `docs/06-root-cause/`: `root-cause-tree.md`, `five-whys.md`, `evidence-confidence-matrix.md`, `confirmed-root-causes.md`. Sub-gate: each cause carries supporting evidence and a confidence; correlation is not labelled causation.
- 7 Deep repo assessment. `docs/07-repo-assessment/`: `repo-assessment.md`, `dependency-map.md`, `technical-debt-register.md`, `critical-workflow-inventory.md`, `baseline-behaviour.md`, `characterization-test-plan.md`. Sub-gate: critical workflows are named; a characterization plan exists where coverage is thin.

## Required analysis
Evaluate: the data relationships and keys across all tables in the two legacy databases (19 in `data/legacy.sqlite3`, 12 in `data/enterprise_legacy.sqlite3`); the temporal fields and where they are confused; the trust labels on text; the four rule implementations and how they disagree; the conflict catalogue BP1 to BP8. For every conflict: finding, evidence (a query), impact, risk, confidence, open questions.

## Evidence rules
Every conflict has a reproducible query with its result. Classify each statement as Verified Fact, Inference, Assumption, or Unknown. Cite file paths, tables, and row counts.

## Constraints and guardrails
Do not change code or data. Do not fix any defect; only catalogue it. Do not generalise from one row; give counts. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Four rule sources that disagree | Python `app/legacy_logic.py`; JavaScript `legacy_js/legacy_policy.js`; Java `legacy_java/ReconcileLegacy.java`; night batch `legacy_batch/shift_reconciliation.py` |
| Legacy deviations | Python 50,000 cutoff; JS limit times 1.05 and 999,999 default; Java float totals drop blank rows; night batch treats REVIEW as open |
| Canonical rule source | `contracts/decision-policies-archive.json` and the `policy_register` table in `data/enterprise_legacy.sqlite3` |
| Business problems | BP1 recipe mismatch (91 of 125 steps); BP2 REPLAY inflation; BP3 time confusion; BP4 four disagreeing rule implementations; BP5 open/closed across sites; BP6 three region vocabularies; BP7 untrusted approve/ignore text; BP8 no API auth, INC-2025-014 unknown owner |
| "Open"/"closed" (SME BO-06a) | Open while any disposition or engineering action is pending, including REVIEW and HOLD; closed only when a final disposition is recorded and no engineering action is pending |

## Decision gate (before you start)
FD-03 baseline KPI set must be settled from Phase 0. No Business Owner decision is required here.

## Required artifacts
The three folders above, each artifact with the standard header.

## Completion gate
Complete only when every sub-gate passes and every conflict BP1 to BP8 has a reproducible query and result.

## Required final response
Return the seven items: status; findings; risks; assumptions and unknowns; artifacts; blocking issues; next action.

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/05-current-state/conflict-catalogue.md` | Header. One row per business problem BP1 to BP8. Each row has a query and its result count. No row says "should" or "fix". |
| `docs/05-current-state/*` (rest) | Header. Current-process map, system landscape, integration landscape, brownfield inventory, process bottlenecks. |
| `docs/06-root-cause/*` | Header. Root-cause tree, five-whys, evidence-confidence matrix, confirmed causes. Each cause has evidence and a confidence. Correlation not called causation. |
| `docs/07-repo-assessment/*` | Header. Repo assessment, dependency map, tech-debt register, critical-workflow inventory, baseline behaviour, a characterization-test plan where coverage is thin. |

## Done test

Open `conflict-catalogue.md`. Pick any row. Its query runs against the repo database and returns the stated count. No row proposes a change. All eight business problems BP1 to BP8 appear.
