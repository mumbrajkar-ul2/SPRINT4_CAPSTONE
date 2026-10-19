# Phase 16 — Final As-Built PRD

> Spine unit: FINAL | Guidelines 14, 18, 28 | Decision gate: BO-13

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test. This is the final phase.

## Inputs

- `docs/09-initial-prd/`, `docs/17-implementation-prd/`, `docs/12-specs/`
- `docs/10-architecture/adrs/`, `docs/26-tevv/`, `docs/34-after-kpis/`
- `docs/model-comparison/scorecard.md`
- `Decision_Tracker.md` (section 6 row for Phase 16; section 5.1 for BO-13)

## Prompt

```text
# Phase 16 — Final As-Built PRD

## Objective
Build the authoritative as-built product baseline: what was actually delivered, validated, and accepted. Reconcile the Initial PRD (Phase 3), the Implementation PRD (Phase 8), the specs, the ADRs, the TEVV evidence, and the production KPIs. Classify every original requirement.

## Scope
Analyse across every original requirement, the as-built architecture, and the residual risk. Exclude: new features; copying earlier PRDs unchanged.

## Sub-stages
- FINAL Authoritative as-built PRD. `docs/final-prd/`: `final-as-built-prd.md`, `requirement-disposition-matrix.md`, `as-built-architecture.md`, `final-acceptance-evidence-map.md`, `known-limitations.md`, `residual-risk-register.md`, `final-product-baseline-signoff.md`. Sub-gate: every original requirement is classified Delivered, Changed, Deferred, Rejected, or Superseded, each with a rationale and evidence; the as-built architecture matches what runs; BO-13 is signed or deferred.

## Required analysis
Evaluate: the disposition of every requirement against the evidence; the as-built architecture versus the Phase 4 target; the acceptance evidence per capability; the known limitations and residual risks. For every disposition: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
Each disposition maps to lifecycle evidence (a spec, a test, a KPI, an ADR). Classify claims as Verified Fact, Inference, Assumption, or Unknown. Do not mark a requirement Delivered without acceptance evidence.

## Constraints and guardrails
Do not copy the Initial or Implementation PRD unchanged. Do not add new scope. Do not mark a requirement Delivered without evidence; if evidence is missing, mark it Unknown and route to the Business Owner. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Disposition set | Delivered, Changed, Deferred, Rejected, Superseded; each with a rationale and evidence |
| Delivered needs evidence | No requirement is Delivered without acceptance evidence (a spec, a test, a KPI, an ADR) |
| As-built architecture | Must match the services that actually run |
| Screen sentence | The as-built screen sentence matches the files under `apps/app_a/ui/` and `apps/app_b/ui/`. Write "React" only when those folders contain a React app. When they contain `index.html` and `assets/app.js`, write that fact and mark the section 4 React row as a deviation. |
| BO-13 (SME view) | Sign once every requirement is classified with evidence and the known limitations are listed |

## Decision gate (before you start)
BO-13 final as-built baseline sign-off — the Business Owner's; if PENDING, pause with the SME recommendation (sign once every requirement is classified with evidence and the known limitations are listed). Until signed, the baseline is marked unsigned but the phase may complete under the default.

## Required artifacts
The `docs/final-prd/` folder, each file with the standard header.

## Completion gate
Complete only when the sub-gate passes: every requirement is classified with a rationale and evidence, the as-built architecture is recorded, and BO-13 is signed or deferred under its default.

## Required final response
Return the seven items, plus a handover summary and the open items (for example BO-06b, BO-12, or BO-13 if still pending).

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `requirement-disposition-matrix.md` | Header. Every requirement from the Initial and Implementation PRD classified Delivered, Changed, Deferred, Rejected, or Superseded, each with a rationale and evidence link. |
| `as-built-architecture.md` | Header. The architecture that actually runs, compared to the Phase 4 target. |
| `final-acceptance-evidence-map.md` | Header. Each Delivered requirement linked to acceptance evidence. |
| `known-limitations.md` and `residual-risk-register.md` | Header. The limitations and residual risks. |
| `final-product-baseline-signoff.md` | Header. BO-13 recorded as signed or deferred with the SME recommendation shown. |

## Done test

The requirement-disposition matrix covers every requirement in the Initial PRD and the Implementation PRD. Each Delivered requirement links to acceptance evidence. The as-built architecture matches the running services.

Screen sentence check:

1. Read `apps/app_a/ui/` and `apps/app_b/ui/`.
2. Search `docs/final-prd/as-built-architecture.md` and `docs/final-prd/final-as-built-prd.md` for the word React.
3. Fail the stage when those docs say the running screens are React and the UI folders have no `react` dependency and no JSX or TSX source.

The Phase 16 PASS row stays the record of the first run. Do not re-accept Phase 16 from this added check. After Phase 17 Half B, those docs may keep the word React because the UI folders then contain a React app. A sentence that still disagrees is corrected in `docs/43-demo-ready/` and names the old sentence.
