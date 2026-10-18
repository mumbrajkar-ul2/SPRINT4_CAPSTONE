# Phase 7 — Transform the repo

> Spine units: 14, 15, 16 | Guidelines 10, 27 | Decision gate: FD-12

Build phase. Two halves. Half A is the transformation plan and the characterization-test plan. Half B strangles the workflows and validates against the baseline. The coordinator spawns an executor for Half A, then for Half B after the reviewer returns HALF_A_ACCEPTED. This is the first phase that changes application behaviour.

## Inputs

- Phase 1 rule implementations `docs/07-repo-assessment/` and the four rule sources
- Phase 6 specs `docs/12-specs/`
- Phase 0 baseline `docs/04-baseline-kpis/`
- `Decision_Tracker.md` (section 6 row for Phase 7)

## Prompt

```text
# Phase 7 — Transform the repo

## Objective
Plan the transformation, then strangle the high-value workflows behind characterization tests, then validate the transformed repo against the baseline.

## Scope
Analyse and change across feed intake, reconciliation, and rule evaluation in the legacy app. Exclude: changing behaviour before a test locks it; new features.

## Sub-stages
- 14 Transformation plan. `docs/14-transformation/`: `transformation-backlog.md`, `migration-roadmap.md`, `cutover-plan.md`, `rollback-strategy.md`, `transformation-gates.md`.
- 15 Transform. `docs/15-modernization/`: `transformation-log.md`, `changed-components.md`, `behavior-preservation-evidence.md`, `approved-behavior-changes.md`, `test-execution-log.md`. Plus `tests/characterization/` and the transformed services.
- 16 Validate. `docs/16-repo-validation/`: `repo-quality-gate.md`, `regression-results.md`, `behavior-difference-report.md`, `validation-signoff.md`.

## Required analysis (Half A)
1. The current behaviour of each target workflow (feed intake, reconciliation, rule evaluation), captured as a characterization-test plan.
2. The parity target against the Phase 0 baseline, with the tolerance named.
3. The strangle order and the cutover and rollback plan.
4. The shadow-run comparison design.
5. The risk that a behaviour change slips through, and the gate that catches it.
For every change: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response for Half A. Wait for HALF_A_ACCEPTED.

## Required work (Half B, after acceptance)
1. Write the characterization tests under `tests/characterization/` that lock current behaviour before any change.
2. Strangle the workflows in the order feed intake, reconciliation, rule evaluation. Each change follows its test.
3. Run the characterization suite and the shadow comparison. Record before-and-after in `test-execution-log.md` and `behavior-difference-report.md`.
4. Explain every behaviour difference against the Phase 7 baseline; mark each as preserved or an approved change.

## Evidence rules
Every transform is preceded by a characterization test. Classify claims as Verified Fact, Inference, Assumption, or Unknown. Cite test names and shadow-run results. Test output is REAL.

## Constraints and guardrails
Do not change a workflow before a test locks its current behaviour. Do not break baseline parity. Do not read Business-Owner policy values into code; route undefined cases to review. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Strangle order (FD-12 default) | Feed intake, then reconciliation, then rule evaluation |
| Parity source | The Phase 0 baseline KPI numbers |
| Rule for undefined policy | Route the case to HOLD_FOR_REVIEW; never read a Business-Owner value into code |
| First behaviour-change phase | Phase 7; Phases 0 to 6 changed no application behaviour |

## Decision gate (before you start)
FD-12 characterization-test approach and strangle order — Team-Force; default order is feed intake, reconciliation, rule evaluation. No Business Owner decision required.

## Required artifacts
The three folders above, plus `tests/characterization/`. Standard header on the docs.

## Completion gate
Half A PASS when the plan, the parity target, the strangle order, and the characterization-test plan are specified. Half B PASS when characterization parity holds for every transformed path and every behaviour difference is explained. BLOCKED if parity fails.

## Required final response (after each half)
Return the seven items.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/14-transformation/*` (Half A) | Header. Transformation backlog, roadmap, cutover, rollback, gates. The strangle order named. |
| `tests/characterization/*` (Half B) | Passing tests that lock current behaviour before each change. |
| `docs/15-modernization/test-execution-log.md` (Half B) | Header. Before-and-after test output. Each change preceded by its test. |
| `docs/16-repo-validation/behavior-difference-report.md` (Half B) | Header. Every behaviour difference against the Phase 7 baseline, each marked preserved or an approved change. |

## Done test

Run the characterization suite; all tests pass. Run a shadow comparison on each transformed path; results match the Phase 0 baseline within the stated tolerance. Open `behavior-difference-report.md`; every difference is explained.
