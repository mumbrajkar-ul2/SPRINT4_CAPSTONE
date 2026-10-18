# Phase 13 — Production hardening

> Spine units: 27, 28, 29, 30, 31, 32, 33 | Guideline 13 | Decision gate: FD-19

Build phase. Each of the seven sub-stages is a two-half gate. Half A writes the design; Half B makes the small change and records before-and-after evidence. The coordinator spawns an executor for Half A, then for Half B after the reviewer returns HALF_A_ACCEPTED.

## Inputs

- Phase 8 platform (compose, CI, observability)
- Phase 10 agent and audit chain `apps/app_a/agent/`, `apps/app_a/audit/`
- Phase 12 controls `docs/24-security-privacy/`
- the 0C envelope `docs/00-preflight/ai-economics/`
- `Decision_Tracker.md` (section 6 row for Phase 13)

## Prompt

```text
# Phase 13 — Production hardening

## Objective
Harden the system across seven concerns. Each is its own sub-stage with the two-half gate: Half A writes the design, Half B makes the small change and records before-and-after evidence. Show that failures recover.

## Scope
Analyse and build across hardening, reliability, incident and BCDR, release, observability, FinOps, and vendor risk. Exclude: new features.

## Sub-stages (each is Half A design, then Half B evidence)
- 27 Hardening. `docs/27-hardening/`: `identity-rbac-hardening.md`, `secrets-hardening.md`, `runtime-hardening.md`, `dependency-hardening.md`, `sbom-summary.md`, `vulnerability-disposition.md`.
- 28 Reliability and resilience. `docs/28-resilience/`: `resilience-architecture.md`, `timeout-retry-policy.md`, `circuit-breaker-policy.md`, `fallback-matrix.md`, `ai-disabled-mode.md`, `failure-injection-results.md`.
- 29 Incident and BCDR. `docs/29-incident-bcdr/`: `ai-incident-playbook.md`, `containment-procedures.md`, `bc-plan.md`, `dr-plan.md`, `rto-rpo.md`, `tabletop-results.md`.
- 30 Release and rollback. `docs/30-release/`: `release-plan.md`, `deployment-strategy.md`, `feature-flag-plan.md`, `go-no-go-criteria.md`, `rollback-plan.md`, `backup-validation.md`.
- 31 Observability and SLOs. `docs/31-observability/`: `observability-architecture.md`, `ai-telemetry-spec.md`, `agent-telemetry-spec.md`, `slo-sla-definitions.md`, `error-budget-policy.md`, `operational-runbook.md`.
- 32 FinOps and token efficiency. `docs/32-finops/`: `baseline-vs-actual-token-analysis.md`, `cost-per-case.md`, `cost-per-outcome.md`, `token-leakage-analysis.md`, `finops-model.md`, `cost-guardrails.md`.
- 33 Vendor and concentration risk. `docs/33-vendor-risk/`: `vendor-inventory.md`, `concentration-risk-analysis.md`, `lock-in-analysis.md`, `portability-assessment.md`, `exit-plan.md`.
- Operational runbooks also live in `operations/`.

## Required analysis (Half A, per sub-stage)
For each concern: the failure modes and recovery; the DLQ and replay where relevant; the runbooks; the SLOs and the observability that proves them; the cost and token efficiency against the 0C envelope. For every element: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A for each sub-stage. Return the seven-item final response for Half A. Wait for HALF_A_ACCEPTED before its Half B.

## Required work (Half B, after acceptance, per sub-stage)
Make the small, reviewable change for the concern and record the before-and-after evidence. Sub-stage 28: a failure demo recovers. Sub-stage 30: a rollback is proven. Sub-stage 31: telemetry is live. Sub-stage 32: measured cost is compared against the 0C envelope. Park a bad message in the DLQ and replay it.

## Evidence rules
Show each failure demo recovering, as a before-and-after result. Classify claims as Verified Fact, Inference, Assumption, or Unknown. Test output is REAL.

## Constraints and guardrails
Do not add features. Do not hide a failure; show it and the recovery. Do not claim an SLO the telemetry does not support. A Half B must not start until its Half A design passes. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Failure rule | Show each failure and its recovery; never hide a failure |
| FinOps source | Reconcile measured cost against the 0C envelope in `docs/00-preflight/ai-economics/` |
| DLQ | Park a bad message and replay it; confirm correct handling |
| AI-disabled mode | The system keeps running with the model off |

## Decision gate (before you start)
FD-19 reliability, DLQ, BCDR, SLOs, FinOps design — Team-Force; the SME advises. No Business Owner decision required.

## Required artifacts
The seven folders above, plus `operations/`. Each sub-stage records Half A and Half B separately. Standard header on the docs.

## Completion gate
Half A PASS when each concern's design is specified. Half B PASS when each concern has Half A design then Half B evidence and every failure demo recovers. BLOCKED otherwise.

## Required final response (after each half)
Return the seven items.
```

## Expected output

| File | Must contain |
|---|---|
| each of the seven `docs/NN-*/` folders (Half A) | Header. The concern's design. |
| `docs/28-resilience/failure-injection-results.md` (Half B) | Header. A failure demo that recovers, with before-and-after evidence. |
| `docs/31-observability/*` (Half B) | Header. Live telemetry and the SLOs it supports. |
| `docs/32-finops/baseline-vs-actual-token-analysis.md` (Half B) | Header. Measured cost against the 0C envelope. |

## Done test

Each of the seven sub-stages has a Half A design and a Half B evidence record. Trigger each failure demo; it recovers. Park a bad message in the DLQ and replay it; it is handled correctly. `baseline-vs-actual-token-analysis.md` references the 0C envelope.
