# ADR: two applications

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | ACCEPTED. Documents FD-06. Does not change the lock. |
| Evidence sources | `Execution_Plan.md` sections 4, 8, 10; `Project_Intent.md` section 8; `docs/09-initial-prd/initial-prd.md`; `docs/09-initial-prd/mvp-scope.md`; `Decision_Tracker.md` FD-06 |
| Assumptions | Trainer confirmation on 2026-10-17 still holds: Application B is a full fab-exception app driven only by the Context Lake. |
| Unresolved issues | Application A and Application B host ports stay Unknown. Internal module layout stays later. |
| Residual risks | Building Application B as a dashboard on Application A would fail Intent 8.1 independence. Measuring the two apps on different scenarios would fail guideline 14. |

This ADR records the locked choice to run two FastAPI and React applications. Application A is built from its own transformed code. Application B is built from the Context Lake. Both run the same scenarios and are measured on the same KPI families.

---

## Decision

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 8.

Build two independently running applications.

- Application A is the AI-transformed operational application. It takes its rules from its own transformed code.
- Application B is the Context Lake ported application. It takes its rules only from the lake.
- Both expose a FastAPI HTTP API and a React screen.
- Both run without calling the other at run time.
- Both run scenarios 7 to 11 with the same inputs. Scenario 13 compares them. Each difference traces to a lake item.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected |
|---|---|---|
| One application | One modern app plus a lake used only as a document store | Guideline 4 asks for two functional applications. A working second app is what tests the lake |
| Two applications, both from transformed code | Two copies of the rebuilt program | Application B would not prove what the lake holds. FR-14 would have no miss to trace |
| Application B as a screen on Application A | Application B calls Application A at run time | Intent 8.1: each app must work without the other. A down Application A would hide an unfinished Application B |
| Streamlit as the demo UI | Faster to sketch. Looks like an internal tool | Guideline 5 asks for a professional application. `Execution_Plan.md` section 4 locks FastAPI and React |
| Three or more user applications | Extra product surface | BO-04 working answer holds scope to both apps, the AI limits, the eight problems, and the demo flow. This file does not sign BO-04 |

Worked example. If Application B were a screen on Application A, every Application B result would be Application A's result. A missing lake item would stay hidden. Scenario 13 would always match.

---

## Why this wins for a laptop demo

**Verified Fact.** `Execution_Plan.md` section 10. Minutes 13 to 25 show Application A. Minutes 25 to 32 show Application B. Minutes 32 to 36 show the comparison.

Two processes on one Compose network fit a laptop. The audience sees the same five cases twice. The second run is the lake test.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Shared hidden state between the two apps | Independence rule in Intent 8.1. No run-time call from one app to the other |
| Duplicate feature work | Shared lake reads and shared contracts are allowed. Each application still keeps its own rule source |
| Application B scope creep | MVP: same workflow plus the context view (F-15). No ninth business problem |

---

## Cost and token or runtime impact

Each scenario runs twice. Token use for explanation and planning can double if both apps call the model live.

**Assumption.** Demo replay (`MODEL_MODE=replay`) plays saved responses. Live tokens in that mode stay Unknown until measured. Phase 0C left those cells Unknown.

Runtime cost is two FastAPI processes and two React screens on one laptop. No extra cloud service is required for the two-app split itself.

Honesty: token numbers are Unknown. Packaged case count 125 is REAL.

---

## Portability lesson

A second application built only from governed knowledge tests whether the knowledge is complete. A second copy of the same code does not.

Sprint 3 used a second model on a semantic layer. Sprint 4 needs rule logic, dependencies, architecture decisions, and evidence as well. `Project_Intent.md` section 8.2.

---

## Finding

**Finding.** Two independently running FastAPI and React applications, built from different rule sources and measured the same, is the locked application shape.
**Evidence.** `Execution_Plan.md` section 4. `Project_Intent.md` section 8. FD-06.
**Impact.** Phase 9 builds Application A. Phase 11 builds Application B. Phase 14 scores both.
**Risk.** Calling one app from the other at run time would hide a missing lake item.
**Confidence.** High.
**Open questions.** Host ports for the two apps. Phase 8 compose assigns them.

---

## What this ADR does not do

This ADR does not assign Application A or Application B ports. It does not write code. It does not sign BO-04.
