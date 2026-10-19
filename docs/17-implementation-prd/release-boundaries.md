# Release boundaries

| Field | Value |
|---|---|
| Stage | Phase 8 / 17 Implementation PRD. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. BO rows that are PROPOSED stay PROPOSED. |
| Evidence sources | `docs/09-initial-prd/mvp-scope.md`; `docs/09-initial-prd/non-goals.md`; `Execution_Plan.md` sections 5 and 10; `docs/17-implementation-prd/implementation-prd.md`; FD-13, FD-14 through FD-23 |
| Assumptions | Later phases still implement the same MVP. They do not add a ninth business problem. Phase 8 builds platform only. |
| Unresolved issues | FD-21 later freezes the 40-minute path. App feature completion stays Phases 9 to 11. |
| Residual risks | Treating a healthy `/health` route as a finished Application A would hide that scenarios 7 to 11 are still unbuilt. |

This file names what Phase 8 releases and what waits. MVP remains the smallest product that names both applications, the AI limits, the eight business problems, and the 40-minute demo flow.

---

## Finding

**Finding.** Phase 8 Half B releases a runnable platform baseline. Application features, agent pause, OPA rule bodies, and the two-app harness stay later.
**Evidence.** `Execution_Plan.md` Phase 8 scope. Phase 8 exclude list: app features. `mvp-scope.md`.
**Impact.** Half B has a closed list. A reviewer can fail extra screens or extra servers.
**Risk.** Adding Keycloak, Prometheus, or scenario 8 in this phase would grow past the boundary.
**Confidence.** High
**Open questions.** Live Compose on the Half B machine.

---

## Phase 8 increment (this release)

Half B may write only these things.

| Item | What the user or operator can finish | Bound |
|---|---|---|
| Capstone Compose | `docker compose up` starts the six host ports | Ports 8080, 8090, 8091, 8092, 8100, 8110 |
| Health | Each host port answers `GET /health` | `{ "ok": true }` |
| Identity scaffolding | Application A and Application B reject a case-path or identity-probe call with no headers | HTTP 401, `missing_identity` |
| Documented key | `.env.example` names `FABPULSE_API_KEY=local-demo-only` | Not hard-coded in source |
| Lake REST | Port 8091 serves the Phase 6 read routes from the generated lake file | Read only. Key required except health |
| Lake MCP | Port 8092 serves the four locked tools | Read only. Key required except health |
| Replay wiring | `MODEL_MODE=replay` reads `operations/model-replay/` | Hash-of-prompt files only |
| JSON logs | Each listener writes one JSON object per line to stdout | Fields in `finalized-nfrs.md` |
| Capstone CI | Tests, lake gates, compose config, identity 401, replay miss | No `generate --reset`. No live model |
| App stubs | `apps/app_a/` and `apps/app_b/` serve health and the identity probe | No queue, case, approval, query, or lineage feature |

Worked example. After Phase 8, `http://127.0.0.1:8100/health` is 200. `http://127.0.0.1:8100/api/identity-check` without headers is 401. `http://127.0.0.1:8100/api/queue` is not a finished ranking screen.

---

## Later increments that still serve the same MVP

These are how later phases build the MVP. They are not extra product features.

| Later work | Why it still sits inside BP1 to BP8 |
|---|---|
| Phase 9 Application A | Scenarios 7 to 11, citations, role screens. FD-14 quality floors stay Unknown until measured |
| Phase 10 agents, human pause, OPA, audit chain | Approval gate, restart mid-approval, correlation-id rows. FD-15, FD-16, FD-23 |
| Phase 11 Application B and parity harness | Same scenarios from the lake, scenario 12, scenario 13. FD-17 |
| Phase 12 identity hardening and threat model | Full role-permission design. FD-18. BO-10 still PROPOSED |
| Phase 13 recovery and operability | Scenario 11 depth, measured reliability. FD-19. Percents stay Unknown until measured |
| Phase 14 scorecard | Eight KPI families. No invented dollar benefit. BO-11 still PROPOSED |
| Phase 15 rehearsal | Freeze the 40-minute path (FD-21). Replay already wired |
| Phase 16 as-built baseline | Requirement dispositions. BO-13 still PROPOSED |

Ports 8080, 8090, 8091, 8092, 8100, and 8110 are platform facts for that build. They are not extra MVP features.

---

## Out of this release

| Item | Why it stays out | Label |
|---|---|---|
| Scenario screens 7 to 13 | Phase 8 exclude: app features | Verified Fact of the phase prompt |
| Language-model ranking, pass-or-fail, reconcile, or duplicate mark | FD-04 | Verified Fact |
| Model write of a case, hold, or feed status | BO-03 working answer | Verified Fact of the working answer |
| Production `engineering_hold` predictor | FD-05 | Verified Fact |
| OPA container or Rego bodies | FD-16 PENDING. Phase 10 | Verified Fact |
| Audit column list | FD-23 PENDING. Phase 10 | Verified Fact |
| Keycloak, Auth0, or another login server | Needs a public network or an extra container the stack lock omits | Inference. ED-P8A-02 |
| Prometheus, Grafana, or a cloud exporter | Extra container. Offline replay forbids a public-network exporter | Inference. ED-P8A-07 |
| Ollama or a third offline model path | Section 10 names hash-of-prompt replay only | Verified Fact of section 10 |
| `python -m app.generate --reset` in capstone CI | Would replace the freeze | Verified Fact of the Phase 1 gap |
| Invented cycle-time target or aged-backlog cutoff | BO-02. Both values Unknown | Unknown |
| Monetary benefit claim | BO-11 | Verified Fact of the working answer |
| Workshop 500k and stress 2M lake tiers | Not packaged | Verified Fact |
| Official Birlasoft brand files | Not in hand. BO-12 | Verified Fact of the working answer |
| Named company job titles | Unmapped | Unknown |
| Signed BO-04 | This folder stays UNSIGNED | Verified Fact |
| Numeric SLO percents | No governed source | Unknown |

---

## MVP acceptance stays later

The MVP is accepted for demo use when all of these are true. Numeric KPI targets are not in this list. Phase 8 alone does not finish this list.

1. Application A runs scenarios 7 to 11 with an approval gate.
2. Application B runs the same scenarios from the Context Lake and shows scenario 12.
3. Scenario 13 names matches and traces each difference to a lake item.
4. Each of BP1 to BP8 has a visible handling on that path.
5. A person approves every record-changing action.
6. The 40-minute path in Execution_Plan section 10 can be rehearsed.
7. Every demo number carries an honesty label.
8. BO-04 remains recorded as PROPOSED until the owner signs.

Phase 8 acceptance is the shorter platform list in `docs/18-delivery/definition-of-done.md`.

---

## What this file does not do

This file does not add scope beyond the eight business problems. It does not write compose or CI files. It does not sign BO-04.
