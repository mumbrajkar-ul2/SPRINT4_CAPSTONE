# Evaluation rubric

| Field | Value |
|---|---|
| Stage | Phase 8 / 18 Delivery planning. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. The reviewer grades. This file does not grade Half A. |
| Evidence sources | `playbook/executor.md`; `playbook/phase_08_foundations.md`; `playbook/reviewer.md` if present; `docs/18-delivery/definition-of-done.md`; `docs/18-delivery/acceptance-test-plan.md` |
| Assumptions | The reviewer is a fresh Composer 2.5 agent. The builder does not grade this unit. |
| Unresolved issues | Reviewer verdict for this unit is Unknown until that agent reads the files. |
| Residual risks | The builder filling PASS on the reviewer line would hide the two-agent rule. |

This file tells the reviewer how to grade Phase 8 Half A and, later, Half B. It does not assign the verdict for this unit.

---

## Finding

**Finding.** Half A is graded on design completeness, reconciliation, labelled claims, and the stop boundary. Half B is graded on one-command health, identity 401, replay, logs, and the absence of app features.
**Evidence.** Phase 8 completion gate. Executor rules.
**Impact.** A later reviewer has the same list the executor used.
**Risk.** Scoring invented SLO percents.
**Confidence.** High on the criteria. Unknown on the verdict.
**Open questions.** Reviewer verdict.

---

## Verdict words

| Verdict | When to use it |
|---|---|
| HALF_A_ACCEPTED | Every Half A criterion below is met |
| HALF_A_REJECTED | A required design file is missing, an assumption is unrecorded, a BO row was marked DECIDED, or code was written |
| STAGE_ACCEPTED | Half B also meets the platform Done list |
| NEEDS_HUMAN | The Done test needs Docker, a running stack, or a credential the sandbox blocks |
| BLOCKED | A required listener cannot be named or a locked fact was violated |

The executor may write an own-read of PASS, CONDITIONAL PASS, or BLOCKED. That line is not the reviewer grade.

---

## Half A criteria

Score each row yes or no. HALF_A_ACCEPTED needs yes on every row.

| ID | Criterion | Yes when |
|---|---|---|
| R-A1 | Five implementation PRD files exist | Paths in `docs/17-implementation-prd/` match the phase prompt |
| R-A2 | Five delivery files exist | Paths in `docs/18-delivery/` match the phase prompt |
| R-A3 | Eight-field header | Every file has stage, date and version, author or agent, status, evidence sources, assumptions, unresolved issues, residual risks |
| R-A4 | Claims labelled | Material statements carry Verified Fact, Inference, Assumption, or Unknown |
| R-A5 | Demo numbers labelled | Packaged counts used as evidence carry REAL |
| R-A6 | Reconciliation | The implementation PRD compares the Initial PRD with repo findings |
| R-A7 | Invalidated assumptions | IA-01 to IA-12 are recorded, or an equivalent complete list |
| R-A8 | App host ports named | Application A and Application B ports are present and are not 8080, 8090, 8091, or 8092 |
| R-A9 | Identity named | Headers, environment variable, and documented local default are present. No secret is hard-coded as production source |
| R-A10 | FD-13 recommended | A copyable stack paragraph is present, authority: team-force |
| R-A11 | Replay bounded | Design uses hash-of-prompt files from section 10. No third offline mode |
| R-A12 | SLO percents empty | Availability, p95, groundedness, citation, abstention, cycle time, and aged backlog stay Unknown |
| R-A13 | BO rows unchanged | PROPOSED rows stay PROPOSED. Signoff is UNSIGNED |
| R-A14 | No Half B artifacts | No new compose file, no new CI file, no app feature code |
| R-A15 | Plain speech | Sentences state the fact. Product words are explained |
| R-A16 | Six-field findings | Required analysis rows include finding, evidence, impact, risk, confidence, open questions |
| R-A17 | Stop | The unit does not start Half B |

Worked example. If Application A is placed on 8080, R-A8 is no. If BO-04 is marked DECIDED, R-A13 is no.

---

## Half B criteria (after HALF_A_ACCEPTED)

Score each row yes or no. STAGE_ACCEPTED needs yes on every row, or NEEDS_HUMAN plus a human paste-back that then satisfies the row.

| ID | Criterion | Yes when |
|---|---|---|
| R-B1 | One command | `docker compose up` from the capstone root |
| R-B2 | Six health rows | 8080, 8090, 8091, 8092, 8100, 8110 are healthy. Honesty REAL |
| R-B3 | Identity 401 | AT-ID-A and AT-ID-B pass |
| R-B4 | Identity 200 | AT-ID-HIT passes and returns no case feature body |
| R-B5 | Secret | Key comes from the environment. Default documented. Not in source |
| R-B6 | Lake read-only | AT-LAKE-RO passes |
| R-B7 | Replay | AT-REPLAY-HIT and AT-REPLAY-MISS pass |
| R-B8 | Logs | AT-LOG-JSON passes. Key is not logged |
| R-B9 | CI | AT-CI-SAFE passes |
| R-B10 | Freeze | AT-FREEZE passes |
| R-B11 | No app features | DB-15 passes |
| R-B12 | Evidence sheet | Result cells filled with REAL or NEEDS_HUMAN |

---

## Automatic no

Any one of these makes the half a reject.

| Event | Half |
|---|---|
| A ninth business problem added | A or B |
| A numeric SLO invented | A or B |
| A Business Owner PROPOSED row marked DECIDED by the executor | A or B |
| INC-2025-014 owner invented | A or B |
| 50,000 or 999,999 written as live policy | B |
| `generate --reset` in capstone CI | B |
| Public-network model call in `MODEL_MODE=replay` | B |
| Compose or CI written in Half A | A |

---

## What this file does not do

This file does not grade the current unit. It does not launch the reviewer. It does not update `STATUS.md`.
