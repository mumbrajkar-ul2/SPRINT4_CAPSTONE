# Phase 6 — Spec-driven design and traceability

> Spine units: 12, 13 | Guidelines 9, 18 | Decision gate: FD-11, BO-09

Document phase. No Half A/B split. The coordinator spawns an executor to write the output, then a fresh reviewer on Composer 2.5 checks it and runs the Done test before Phase 7 starts.

## Inputs

- Phase 5 lake items in `context-lake/` and `context-lake.sqlite3`
- Phase 3 PRD `docs/09-initial-prd/`
- Phase 4 ADRs `docs/10-architecture/adrs/`
- `Decision_Tracker.md` (section 6 row for Phase 6; Group C roles for BO-09)

## Prompt

```text
# Phase 6 — Spec-driven design and traceability

## Objective
Write the scenarios, the non-functional requirements, the API and event contracts, and the acceptance criteria. Build the bidirectional traceability from requirement to spec to test to evidence. Cite lake item ids.

## Scope
Analyse across the API and event contracts, the error semantics, the role permissions, and the SLOs for both apps, plus the traceability map. Exclude: code.

## Sub-stages
- 12 Spec-driven design. `docs/12-specs/`: `system-spec.md`, `api-contracts.md`, `event-contracts.md`, `schema-specifications.md`, `business-rules.md`, `error-handling-spec.md`, `acceptance-criteria.md`. Sub-gate: every spec traces to a lake item; no material ambiguity is left to implementation.
- 13 Traceability. `docs/13-traceability/`: `requirements-traceability-matrix.md`, `spec-to-test-map.md`, `test-to-evidence-map.md`, `coverage-gap-register.md`. Sub-gate: requirement to spec to test to evidence is mapped; no critical orphan requirement.

## Required analysis
Evaluate: the scenarios per workflow and business problem; the error semantics; the role permissions (who may approve, hold, or block each action type); the SLOs; the trace from each spec to a lake item id. For every spec: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
Each spec cites a lake item id. Classify as Verified Fact, Inference, Assumption, or Unknown.

## Constraints and guardrails
Do not write code. Do not specify a permission the Business Owner has not confirmed; mark it PROPOSED. Do not add an API the PRD does not justify. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Spec source | Every spec traces to a Context Lake item id that exists in `context-lake.sqlite3` |
| Role map (SME BO-09) | Standard fab roles; the proposer is never the approver; see Group C in `Decision_Tracker.md` |
| Permission not confirmed | Mark PROPOSED with a named owner; do not hard-code it |
| Semantic layer | Markdown explains, YAML defines, JSON Schema validates, tests protect, generated output serves |

## Decision gate (before you start)
FD-11 is Team-Force; the SME advises; decide here. BO-09 role-to-permission map is set by the SME (Group C in `Decision_Tracker.md`); record it with `authority: sme`. The Business Owner only confirms the company titles match; if that is pending, proceed on the SME map and note it.

## Required artifacts
The `docs/12-specs/` and `docs/13-traceability/` folders, each file with the standard header and lake item ids.

## Completion gate
Complete only when both sub-gates pass: every spec traces to a lake item, the role map is recorded, and the traceability has no critical orphan.

## Required final response
Return the seven items.

STOP. The reviewer checks this output and runs the Done test. Wait for STAGE_ACCEPTED.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/12-specs/*` | Header. System spec, API and event contracts, schemas, business rules, error-handling, acceptance criteria. Each spec cites a lake item id. |
| `business-rules.md` | Header. The role permissions with `authority: sme`. Any unconfirmed permission marked PROPOSED with an owner. |
| `docs/13-traceability/requirements-traceability-matrix.md` | Header. Requirement to spec to test to evidence, with no critical orphan requirement. |
| `coverage-gap-register.md` | Header. Any gap named, with the missing spec or test. |

## Done test

Pick any spec in `docs/12-specs/`; the lake item id it cites exists in `context-lake.sqlite3`. Open `requirements-traceability-matrix.md`; no critical requirement is an orphan.
