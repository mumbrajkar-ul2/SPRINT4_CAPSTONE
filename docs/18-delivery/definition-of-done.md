# Definition of Done

| Field | Value |
|---|---|
| Stage | Phase 8 / 18 Delivery planning. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Numeric SLO percents are not Done criteria. |
| Evidence sources | `playbook/phase_08_foundations.md`; `docs/17-implementation-prd/release-boundaries.md`; `docs/17-implementation-prd/finalized-nfrs.md`; `docs/12-specs/error-handling-spec.md`; `Execution_Plan.md` section 10 |
| Assumptions | Half A Done is design completeness. Half B Done is a running platform. Product MVP Done stays later. |
| Unresolved issues | Live Compose may be NEEDS_HUMAN. Headline KPIs stay Unknown. BO-04 stays PROPOSED. |
| Residual risks | Counting a 200 on `/health` as Application A complete would hide unbuilt scenarios. |

This file names when Half A is done, when the Phase 8 platform is done, and when the later product MVP is done. The three lists stay separate.

---

## Finding

**Finding.** Phase 8 Half A is done when the implementation PRD, the delivery plan, and this Definition of Done exist. Phase 8 Half B is done when one command starts six healthy listeners, identity scaffolding returns 401 without headers, JSON logs appear, and replay starts with no public-network model call.
**Evidence.** Phase 8 completion gate. Section 10. EH-01.
**Impact.** The reviewer can grade each half against a closed list.
**Risk.** Adding an availability percent to this list would invent an SLO.
**Confidence.** High on the lists. Unknown on live Docker.
**Open questions.** Human run of `docker compose up`.

---

## Half A Done (this unit)

Half A is done when all of these are true.

1. `docs/17-implementation-prd/` holds the five named files.
2. `docs/18-delivery/` holds the five named files.
3. The Initial PRD is reconciled with repo findings.
4. Every invalidated assumption is recorded as IA-01 to IA-12.
5. Application A host port and Application B host port are named.
6. Identity headers and `FABPULSE_API_KEY` are named.
7. FD-13 has a recommended stack the coordinator can copy.
8. Business Owner rows that are PROPOSED stay PROPOSED.
9. The implementation baseline signoff stays UNSIGNED.
10. No compose file, CI file, or application feature code was written in this unit.
11. No numeric SLO percent was invented.

This unit claims those design items. The reviewer makes the real call.

---

## Phase 8 platform Done (Half B)

The platform is done when all of these are true. Honesty of the health output is REAL.

| Check | Pass when |
|---|---|
| One command | `docker compose up` starts the stack from the capstone root |
| Port 8080 | `GET /health` is 200 |
| Port 8090 | `GET /health` is 200 |
| Port 8091 | `GET /health` is 200 |
| Port 8092 | Lake MCP ready check is 200, or the documented equivalent is 200 |
| Port 8100 | `GET /health` is 200 |
| Port 8110 | `GET /health` is 200 |
| Identity miss | `GET /api/identity-check` on 8100 and on 8110 without headers is 401 and `error_class: missing_identity` |
| Identity hit | The same path with `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role` is 200 |
| Secret | Application source has no key literal. `.env.example` documents `local-demo-only` |
| Lake write | A POST to 8091 is 405 |
| Replay | `MODEL_MODE=replay`. A missing hash does not open a public-network model call |
| Logs | `app-a`, `app-b`, `lake-rest`, and `lake-mcp` emit JSON lines |
| CI | Capstone workflow omits `generate --reset` and omits a live model call |
| No app features | Stubs have no queue, case, approval, query, recovery, or lineage feature |
| Packaged freeze | `sources/register.yaml` hashes still match |
| Evidence sheet | `evidence-checklist.md` holds the REAL health rows or a NEEDS_HUMAN note |

If the sandbox blocks the container build, the reviewer marks NEEDS_HUMAN. The human runs the command and pastes the result. **Verified Fact.** `Execution_Plan.md` section 11.

Worked example. Half B starts compose. `curl http://127.0.0.1:8100/health` prints `{"ok": true}`. That line is REAL. It does not mean scenario 8 is built.

---

## Product MVP Done (later phases)

This list is copied from `mvp-scope.md` so it is not lost. Phase 8 does not claim it.

1. Application A runs scenarios 7 to 11 with an approval gate.
2. Application B runs the same scenarios from the Context Lake and shows scenario 12.
3. Scenario 13 names matches and traces each difference to a lake item.
4. Each of BP1 to BP8 has a visible handling on that path.
5. A person approves every record-changing action.
6. The 40-minute path in Execution_Plan section 10 can be rehearsed.
7. Every demo number carries an honesty label.
8. BO-04 remains recorded as PROPOSED until the owner signs.

Numeric KPI targets are not in this list.

---

## What is never a Done criterion in Phase 8

| Item | Why |
|---|---|
| API p95 below a number | Unknown. No governed source |
| Availability 99.5 percent | Inherited note, not adopted |
| Groundedness percent | FD-14 later |
| Exception cycle time improved | Unknown baseline |
| Dollar benefit | BO-11 forbids the claim |
| Signed BO-04 | Stays PROPOSED |
| INC-2025-014 owner filled | Unknown until RT-06 |

---

## What this file does not do

This file does not write tests. It does not run compose. It does not sign a Business Owner row.
