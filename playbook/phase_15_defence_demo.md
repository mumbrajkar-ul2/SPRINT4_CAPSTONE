# Phase 15 — Target operating model, handover, and executive defence

> Spine units: 37, 38, 39, 40, 41, 42 | Guidelines 15, 16, 17, 19, 20, 22, 25, 28 | Decision gate: FD-21, BO-12

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test before Phase 16 starts.

## Inputs

- Phase 14 scorecard `docs/model-comparison/scorecard.md`
- `Execution_Plan.md` section 10 (demo design, the 40-minute flow)
- all prior phase records in `docs/_playbook-log.md` and the phase folders
- `Decision_Tracker.md` (section 6 row for Phase 15; section 5.1 for BO-12)

## Prompt

```text
# Phase 15 — Target operating model, handover, and executive defence

## Objective
Define the target operating model, hand over, set the drift and scale plans, define retirement, and build the executive defence. Write the 40-minute flow, apply Birlasoft branding, draft four or five lessons, and rehearse in replay mode so the demo runs offline. Build the deck on a neutral placeholder until the official Birlasoft assets arrive, then restyle.

## Scope
Analyse and build across the operating model, the handover, the drift and scale plans, retirement, the 40-minute flow, the deck, the lessons, and the offline rehearsal. Exclude: last-minute feature work.

## Sub-stages
- 37 Target operating model. `docs/37-operating-model/`: `target-operating-model.md`, `raci.md`, `decision-rights.md`, `operating-contract-closure.md`. Sub-gate: steady-state ownership assigned; the provisional contract from 0B is closed.
- 38 Handover. `docs/38-handover/`: `handover-index.md`, `operator-exercises.md`, `handover-acceptance-signoff.md`. Sub-gate: an operator can deploy, observe, and recover the solution.
- 39 Drift and continuous improvement. `docs/39-continuous-improvement/`: `drift-framework.md`, `change-trigger-thresholds.md`, `controlled-change-process.md`. Sub-gate: drift thresholds and a controlled-change process exist.
- 40 Scale and roadmap. `docs/40-scale/`: `reusable-components.md`, `pattern-catalog.md`, `90-day-roadmap.md`. Sub-gate: only evidenced assets are marked reusable.
- 41 Retirement. `docs/41-retirement/`: `retirement-criteria.md`, `dependency-clearance.md`, `decommission-checklist.md`. Sub-gate: safe retirement criteria exist.
- 42 Executive defence. `docs/42-executive/`: `executive-narrative.md`, `problem-to-value-story.md`, `lessons-learned.md`, `demo-day-script.md`, `executive-evidence-index.md`. Plus `docs/demo/`. Sub-gate: a timed rehearsal under 40 minutes; an offline replay run passes; four or five lessons drafted; every material claim maps to evidence.

## Required analysis
Evaluate: the 40-minute flow against the time blocks in `Execution_Plan.md` section 10; the problem-to-solution-to-impact story; the business-and-technical balance; the offline run in replay mode; the lessons. For every element: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
Every demo claim carries an honesty label. Every lesson cites a phase or a result. Classify claims as Verified Fact, Inference, Assumption, or Unknown.

## Constraints and guardrails
Do not add features. Do not show an unlabelled number. Do not depend on the network during the demo; use replay mode. Do not ship final Birlasoft branding before the official assets arrive. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Demo length | Under 40 minutes; time blocks in `Execution_Plan.md` section 10 |
| Offline run | `MODEL_MODE=replay`; the demo runs with no network |
| Must appear in the flow | An injection record that yields BLOCK; a restart mid-approval that keeps state |
| Branding (SME view for BO-12) | Build on the neutral placeholder; restyle when Birlasoft assets arrive; label every claim |

## Decision gate (before you start)
FD-21 demo flow, replay mode, lessons — Team-Force; the SME advises; decide here. BO-12 Birlasoft assets and final-claim sign-off — the Business Owner's; if PENDING, pause with the SME recommendation (build on the neutral placeholder; restyle when assets arrive; label every claim).

## Required artifacts
The six folders above, plus `docs/demo/`. Standard header on the docs.

## Completion gate
Complete only when every sub-gate passes: the timed rehearsal is under 40 minutes, the offline run passes, and the lessons are drafted. The final branded deck waits on BO-12; the placeholder deck passes this gate with BO-12 noted as pending.

## Required final response
Return the seven items.

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/37-operating-model/*` | Header. Target operating model, RACI, decision rights, the 0B provisional contract closed. |
| `docs/38-handover/*` | Header. A handover index and operator exercises that let an operator deploy, observe, and recover. |
| `docs/42-executive/demo-day-script.md` | Header. The 40-minute flow against section 10. The injection BLOCK and the restart mid-approval both in the script. Every claim labelled. |
| `docs/demo/*` | The deck on a neutral placeholder. BO-12 noted as pending. |

## Done test

Run the demo in replay mode with no network; it completes. Time the rehearsal; it is under 40 minutes. The injection BLOCK and the restart-mid-approval both appear in `demo-day-script.md`.
