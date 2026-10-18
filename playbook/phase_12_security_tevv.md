# Phase 12 — Security, governance, TEVV, and red team

> Spine units: 24, 25, 26 | Guidelines 11, 12 | Decision gate: FD-18, BO-10

Build phase. Each sub-stage is a two-half gate. Half A writes the design; Half B makes the small change and records before-and-after evidence. The coordinator spawns an executor for Half A, then for Half B after the reviewer returns HALF_A_ACCEPTED.

## Inputs

- Phase 5 injection corpus `context-lake/eval/`
- Phase 10 agent, OPA, and audit chain `apps/app_a/agent/`, `policy/opa/`, `apps/app_a/audit/`
- Phase 6 role permissions `docs/12-specs/business-rules.md`
- `Decision_Tracker.md` (section 6 row for Phase 12; section 5.1 for BO-10)

## Prompt

```text
# Phase 12 — Security, governance, TEVV, and red team

## Objective
Threat-model the system, map governance obligations, and run TEVV with a red team. Each sub-stage uses the two-half gate: Half A writes the design, Half B makes the small change and records before-and-after evidence.

## Scope
Analyse across the threat surfaces, the access controls, the governance obligations, the injection red-team, and the AI-quality evaluation. Exclude: new features.

## Sub-stages (each is Half A design, then Half B evidence)
- 24 Security, privacy, responsible AI. `docs/24-security-privacy/`: `threat-model.md`, `attack-surface-map.md`, `security-control-matrix.md`, `prompt-injection-controls.md`, `agent-security-controls.md`, `security-test-results.md`.
- 25 Governance and assurance. `docs/25-governance/`: `compliance-obligations.md`, `compliance-control-matrix.md`, `accountability-map.md`, `ai-system-register.md`, `model-card.md`, `system-card.md`, `governance-readiness.md`.
- 26 TEVV and red team. `docs/26-tevv/`: `tevv-plan.md`, `golden-dataset-spec.md`, `adversarial-dataset-spec.md`, `release-thresholds.md`, `tevv-results.md`, `red-team-findings.md`, `tevv-release-gate.md`.

## Required analysis (Half A, per sub-stage)
1. Sub-stage 24: the threat model (entry points, trust boundaries, abuse cases) and the control design.
2. Sub-stage 25: the governance obligations mapped to controls and owners.
3. Sub-stage 26: the golden and adversarial datasets and the predeclared release thresholds.
For every finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A for each sub-stage. Return the seven-item final response for Half A. Wait for HALF_A_ACCEPTED before its Half B.

## Required work (Half B, after acceptance, per sub-stage)
1. Sub-stage 24: put the control in code plus a test; record before-and-after in `security-test-results.md`.
2. Sub-stage 25: record the evidence and the register entries.
3. Sub-stage 26: run the TEVV and the red team; record `tevv-results.md` and `red-team-findings.md` with no injection leak and the thresholds met.

## Evidence rules
Report each control as tested, with a before-and-after result. Record eval thresholds as numbers. Classify claims as Verified Fact, Inference, Assumption, or Unknown. Test output is REAL.

## Constraints and guardrails
Do not add features. Do not weaken a control to pass a test. Do not claim a threshold the eval did not measure. A Half B must not start until its Half A design passes. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Injection rule | The red-team injection corpus must drive no action; the gate returns BLOCK |
| AI-quality KPIs | Groundedness, abstention, citation, and rejected schema claims per run |
| Thresholds | Predeclared in `release-thresholds.md`; never claim a number the eval did not measure |
| Data classification (SME view for BO-10) | All records internal and synthetic; process data confidential; no personal data |

## Decision gate (before you start)
FD-18 threat model, RBAC/ABAC, eval thresholds, hallucination target — Team-Force; the SME advises; decide here. BO-10 compliance and data classification — the Business Owner's; if PENDING, pause with the SME recommendation (treat all records as internal and synthetic; process data confidential; no personal data).

## Required artifacts
The three folders above, each with the standard header. Each sub-stage records Half A and Half B separately.

## Completion gate
Half A PASS when each sub-stage design is specified. Half B PASS when each control has Half A design then Half B evidence, the red team finds no leak, and the eval thresholds are recorded. BLOCKED otherwise.

## Required final response (after each half)
Return the seven items.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/24-security-privacy/threat-model.md` (Half A) | Header. Entry points, trust boundaries, abuse cases, the control design. |
| `docs/24-security-privacy/security-test-results.md` (Half B) | Header. Each control tested with a before-and-after result. |
| `docs/25-governance/*` (Half A design, Half B evidence) | Header. Obligations mapped to controls and owners. The register entries. |
| `docs/26-tevv/tevv-results.md` and `red-team-findings.md` (Half B) | Header. The run result with no injection leak. Groundedness, abstention, citation, and rejected-claim numbers against the thresholds. |

## Done test

Each sub-stage has a Half A design file and a Half B evidence file. Run the injection red-team; no attack drives an action. Run the AI-quality eval; it records groundedness, abstention, citation, and rejected-claim numbers.
