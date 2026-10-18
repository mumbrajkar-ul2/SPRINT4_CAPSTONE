# Phase 2 — AI-versus-no-AI qualification

> Spine unit: 8 | Guideline 24 | Decision gate: FD-04, FD-05, BO-03

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test before Phase 3 starts.

## Inputs

- Phase 1 conflict catalogue `docs/05-current-state/conflict-catalogue.md`
- the repo data (for the ML null test on the `engineering_hold` column in `wafer_lots`, `data/legacy.sqlite3`)
- the 0C envelope in `docs/00-preflight/ai-economics/`
- `Execution_Plan.md` section 5
- `Decision_Tracker.md` (section 6 row for Phase 2; section 5.1 for BO-03)

## Prompt

```text
# Phase 2 — AI-versus-no-AI qualification

## Objective
Decide, per capability, whether to use GenAI, deterministic code, or neither. Run the machine-learning null test on the `engineering_hold` column in `wafer_lots` (`data/legacy.sqlite3`) and show it does no better than guessing the most common answer. Reconcile the result with the 0C economics envelope.

## Scope
Analyse across each candidate capability: triage, conflict explanation, natural-language query, agentic planning, rule evaluation, reconciliation, intake de-duplication. Exclude: building any model or feature.

## Sub-stages
- 8 AI-versus-no-AI. `docs/08-ai-qualification/`: `intervention-options.md`, `ai-vs-no-ai-matrix.md`, `deterministic-vs-ai-boundaries.md`, `minimum-intelligence-assessment.md`, `minimum-agency-assessment.md`, `economics-baseline-reconciliation.md`, `qualification-decision.md`. Sub-gate: each capability is labelled GenAI, deterministic, or ML-rejected with a reason; the ML null-test result is recorded; the 0C envelope is reconciled and irrelevant AI cost assumptions are retired.

## Required analysis
Evaluate, per capability: the business risk of a wrong answer; the input variety; whether the task repeats deterministically or needs language understanding. Plus the ML null test accuracy versus the majority baseline, and the text-variety counts that justify GenAI. For every capability: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
Report the ML test as a number against the majority baseline. Classify each label as Verified Fact, Inference, Assumption, or Unknown. Cite the data used.

## Constraints and guardrails
Do not build a production model; the ML test is a one-off check. Do not claim AI value without the text-variety evidence. If a capability is unclear, label it Unknown and route the decision to review. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| ML null test | On the `engineering_hold` column in `wafer_lots` (`data/legacy.sqlite3`); accuracy must not beat the majority-class baseline |
| AI risk boundary (SME view for BO-03) | AI explains and proposes; a person approves every record-changing action |
| Honesty labels | REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL |
| 0C envelope | Lives in `docs/00-preflight/ai-economics/`; reconcile here and retire irrelevant AI cost assumptions |

## Decision gate (before you start)
FD-04 and FD-05 are Team-Force engineering calls; the SME advises. Decide them here with evidence. BO-03 risk appetite is the Business Owner's — if PENDING, pause and show the SME recommendation (AI explains and proposes; a person approves every record-changing action).

## Required artifacts
The `docs/08-ai-qualification/` folder, with the standard header on each file.

## Completion gate
Complete only when the sub-gate passes: every capability labelled with a reason, the ML result recorded, the 0C reconciliation done, and BO-03 decided or deferred.

## Required final response
Return the seven items.

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `ai-vs-no-ai-matrix.md` | Header. Every capability labelled GenAI, deterministic, or ML-rejected, each with a reason. |
| `minimum-intelligence-assessment.md` | Header. The ML null-test accuracy against the majority baseline. Text-variety counts that justify any GenAI label. |
| `minimum-agency-assessment.md` | Header. Where agency is needed and where it is not. A person approves every record-changing action. |
| `economics-baseline-reconciliation.md` | Header. A reference to the 0C envelope. The retired AI cost assumptions named. |
| `qualification-decision.md` | Header. The per-capability decision. BO-03 recorded as decided or deferred with the SME recommendation shown. |

## Done test

Re-run the ML null test on the `engineering_hold` column in `wafer_lots` (`data/legacy.sqlite3`); its accuracy does not beat the majority-class baseline. Every capability in `ai-vs-no-ai-matrix.md` has a label and a reason. `economics-baseline-reconciliation.md` names the 0C envelope.
