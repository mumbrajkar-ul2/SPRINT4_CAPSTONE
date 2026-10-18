# Phase 3 — Initial PRD and product intent

> Spine unit: 9 | Guidelines 4, 16, 21 | Decision gate: BO-02, BO-03, BO-04

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test before Phase 4 starts.

## Inputs

- Phase 1 `docs/05-current-state/conflict-catalogue.md` and Phase 2 `docs/08-ai-qualification/`
- `Project_Intent.md`
- `Execution_Plan.md` sections 3, 4, 8
- `Decision_Tracker.md` (section 6 row for Phase 3; section 5.1 for BO-04)

## Prompt

```text
# Phase 3 — Initial PRD and product intent

## Objective
Write the initial PRD for both applications. Name the users, the workflows, the AI limits, the scope, the exclusions, and the demo flow. Tie every feature to a business problem BP1 to BP8.

## Scope
Analyse across both apps, the shared Context Lake, the user roles, and the 40-minute demo flow. Exclude: implementation detail; code.

## Sub-stages
- 9 Initial PRD. `docs/09-initial-prd/`: `initial-prd.md`, `capability-map.md`, `functional-requirements.md`, `nfrs.md`, `mvp-scope.md`, `non-goals.md`, `initial-prd-traceability.md`. Sub-gate: the PRD names both apps and the demo flow; every feature traces to a business problem; BO-04 is signed or deferred.

## Required analysis
Evaluate: the user roles and the outcome each needs; the workflows both apps run; the AI limits from Phase 2 and BO-03; the acceptance criteria per workflow; the demo flow mapped to scenarios 7 to 13. For every requirement: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
Each requirement cites Phase 1 or 2. Classify as Verified Fact, Inference, Assumption, or Unknown. No unsupported scope.

## Constraints and guardrails
Do not add scope beyond the eight business problems. Do not specify code. Do not promise AI autonomy; a person approves every record-changing action. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Two apps | App A takes rules from its own transformed code; App B takes rules only from the Context Lake |
| AI limit | AI explains and proposes; a person approves every record-changing action |
| Scope | The eight business problems BP1 to BP8; demo scenarios 7 to 13 map to them |
| Demo | A 40-minute flow; see `Execution_Plan.md` section 10 |

## Decision gate (before you start)
BO-02 and BO-03 carry forward from Phases 0 and 2. BO-04 PRD sign-off is the Business Owner's and closes this phase. Pause for it with the SME recommendation (approve once the PRD names both apps, the AI limits, the eight problems, and the demo flow, and nothing beyond).

## Required artifacts
The `docs/09-initial-prd/` folder, standard header on each file.

## Completion gate
Complete only when the sub-gate passes: the PRD names both apps and the demo flow, every feature traces to a BP, and BO-04 is signed or explicitly deferred.

## Required final response
Return the seven items.

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `initial-prd.md` | Header. Both apps named. The AI limits. The 40-minute demo flow. The eight business problems in scope. |
| `functional-requirements.md` | Header. One requirement per feature, each tracing to a BP1 to BP8. |
| `non-goals.md` | Header. What is out of scope. No scope beyond the eight problems. |
| `initial-prd-traceability.md` | Header. A map from every feature to a business problem and to a Phase 1 or Phase 2 finding. BO-04 recorded as signed or deferred with the SME recommendation shown. |

## Done test

Open `initial-prd-traceability.md`. Every feature row maps to a business problem BP1 to BP8. `initial-prd.md` names App A, App B, and the 40-minute flow. No requirement adds scope beyond the eight problems.
