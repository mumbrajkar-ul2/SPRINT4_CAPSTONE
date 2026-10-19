# Phase 8 — Implementation PRD and delivery foundations

> Spine units: 17, 18 | Guidelines 5, 13 | Decision gate: FD-13

Build phase. Two halves. Half A is the implementation PRD and the delivery plan. Half B stands up the platform (identity, CI/CD, observability, compose). The coordinator spawns an executor for Half A, then for Half B after the reviewer returns HALF_A_ACCEPTED.

## Inputs

- Phase 4 ADRs `docs/10-architecture/adrs/` (ports, compose)
- Phase 6 specs `docs/12-specs/`
- Phase 3 Initial PRD `docs/09-initial-prd/`
- `Execution_Plan.md` section 10
- `Decision_Tracker.md` (section 6 row for Phase 8)

## Prompt

```text
# Phase 8 — Implementation PRD and delivery foundations

## Objective
Finalise the implementation PRD, plan the delivery increments, and stand up the delivery platform: identity, CI/CD, observability, and the data seams. Keep everything laptop-runnable with one command.

## Scope
Analyse and build across the implementation PRD, the delivery plan, identity and auth scaffolding, CI/CD config, observability, the Docker Compose topology, and the data seams. Exclude: app features.

## Sub-stages
- 17 Implementation PRD. `docs/17-implementation-prd/`: `implementation-prd.md`, `prd-change-log.md`, `finalized-nfrs.md`, `release-boundaries.md`, `implementation-baseline-signoff.md`.
- 18 Delivery planning and foundations. `docs/18-delivery/`: `delivery-backlog.md`, `definition-of-done.md`, `acceptance-test-plan.md`, `evaluation-rubric.md`, `evidence-checklist.md`. Plus the CI config and the compose files.

## Required analysis (Half A)
1. The Initial PRD reconciled with repo findings; every invalidated assumption recorded.
2. The identity and auth approach that closes the no-auth gap (BP8).
3. The CI/CD steps and the observability signals.
4. The compose topology and the fixed ports (8080, 8090, 8091, 8092, plus the app UIs); the replay-mode wiring (`MODEL_MODE=replay`).
5. The Definition of Done and the acceptance-test plan.
For every element: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response for Half A. Wait for HALF_A_ACCEPTED.

## Required work (Half B, after acceptance)
1. Write the CI config and the compose files for the full stack on the fixed ports.
2. Add identity and auth scaffolding that closes BP8.
3. Wire observability so each service emits telemetry.
4. Wire replay mode so the stack runs with no network.
5. Bring the stack up with one command and confirm every service is healthy. Record the result.

## Evidence rules
Cite config files, compose files, and CI definitions. Classify claims as Verified Fact, Inference, Assumption, or Unknown. The health-check output is REAL.

## Constraints and guardrails
Do not build app features here. Do not hard-code secrets; use environment variables and a documented local default. Keep the whole stack runnable with one `docker compose up`. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Fixed ports | 8080 legacy, 8090 gateway, 8091 lake REST, 8092 lake MCP, plus the app UIs |
| Offline mode | `MODEL_MODE=replay`; the stack runs with no network |
| One-command run | `docker compose up` brings up the whole stack |
| Gap to close | BP8: no API auth; add identity scaffolding |
| Secrets | Environment variables with a documented local default; never hard-coded |
| Front-end image | This phase leaves `Dockerfile.platform` as a Python image. Phase 17 may add Node to that file and build the React screens. A later Node install is in scope for Phase 17. The passed Python-only image stays the Phase 8 record. |

## Decision gate (before you start)
FD-13 platform stack — Team-Force engineering; the SME advises. No Business Owner decision required.

## Required artifacts
The `docs/17-implementation-prd/` and `docs/18-delivery/` folders, plus CI and compose files. Standard header on the docs.

## Completion gate
Half A PASS when the implementation PRD, the delivery plan, and the Definition of Done are specified. Half B PASS when the platform deploys from one command, emits telemetry, and replay mode starts with no network. BLOCKED if the stack does not come up.

## Required final response (after each half)
Return the seven items.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/17-implementation-prd/*` (Half A) | Header. The Initial PRD reconciled with repo findings. Every invalidated assumption recorded. |
| `docs/18-delivery/definition-of-done.md` (Half A) | Header. The Definition of Done and the acceptance-test plan. |
| compose and CI files (Half B) | The full stack on the fixed ports. One-command bring-up. Replay-mode wiring. Identity scaffolding for BP8. |
| `docs/18-delivery/evidence-checklist.md` (Half B) | Header. The health-check result per service. |

## Done test

Run `docker compose up` (or ask Team-Force to); every service is healthy on its port. Start the stack in replay mode with no network; it comes up. The reviewer marks this NEEDS_HUMAN if the sandbox blocks the container build.
