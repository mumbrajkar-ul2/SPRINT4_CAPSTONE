# Handover index

| Field | Value |
|---|---|
| Stage | Phase 15 / 38 Handover |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE for this unit. Index only. Live Compose start stays NEEDS_HUMAN |
| Evidence sources | `compose.yaml`; `operations/operational-runbook.md`; `operations/ai-incident-playbook.md`; `operations/containment-procedures.md`; `operations/bc-plan.md`; `operations/dr-plan.md`; `docs/30-release/deployment-strategy.md`; `docs/30-release/rollback-plan.md`; `docs/30-release/go-no-go-criteria.md`; `.env.example`; FD-13; FD-19 |
| Assumptions | The operator works from the capstone root `c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE`. `MODEL_MODE=replay` |
| Unresolved issues | Company on-call title Unknown. INC-2025-014 owner Unknown. Measured recreate seconds Unknown |
| Residual risks | Starting Compose in this unit and inventing a health pass. Setting `MODEL_MODE=azure` |

This index points an operator at the files that already exist. It does not add a feature. It does not start Docker.

---

## Finding

**Finding.** Deploy, observe, and recover already have files on disk. Deploy is Compose from the capstone root. Observe is `operations/operational-runbook.md` plus `GET /api/audit/{correlation_id}`. Recover is the four incident files plus `GET /api/recovery`. A live `docker compose up` is NEEDS_HUMAN.
**Evidence.** Phase 8 Team-Force paste of port 8080 and 8090 health. Phase 13 runbooks. GNG-30-01 to GNG-30-10. This unit did not start Compose.
**Impact.** An operator can follow one index to those files.
**Risk.** Claiming the six listeners are up on this laptop today without a new paste.
**Confidence.** High on the file list. Unknown on current container state.
**Open questions.** Who runs the first live `docker compose up` after handover. INC-2025-014 owner.

---

## What the operator receives

| Item | Path | What it does |
|---|---|---|
| Full stack | `compose.yaml` | Starts legacy 8080, source gateway 8090, lake REST 8091, lake MCP 8092, Application A 8100, Application B 8110 |
| Local key default | `.env.example` | Shows `FABPULSE_API_KEY=local-demo-only` |
| Replay files | `operations/model-replay/` | 77 saved files besides `README.md`. Honesty: REAL count on 2026-10-18 |
| Log walk | `operations/operational-runbook.md` | Six walks: process up, identity miss, replay miss, parked intake, agent trace, injection BLOCK |
| AI incident | `operations/ai-incident-playbook.md` | Parked intake, replay miss, injection, recovery GET |
| Containment | `operations/containment-procedures.md` | Keep replay. Do not retry BLOCK. Do not delete a parked row |
| Continuity | `operations/bc-plan.md` | What stays up when the live model is off |
| Restore | `operations/dr-plan.md` | Restore steps. Recovery-time floor Unknown |
| Deploy | `docs/30-release/deployment-strategy.md` | Recreate a named Compose service |
| Rollback | `docs/30-release/rollback-plan.md` | Git restore plus Compose. Host sqlite binds on Application A |
| Go list | `docs/30-release/go-no-go-criteria.md` | GNG-30-01 to GNG-30-10 |
| Operating model | `docs/37-operating-model/` | Roles and rights |
| Operator drills | `docs/38-handover/operator-exercises.md` | Deploy, observe, recover exercises |
| Sign-off | `docs/38-handover/handover-acceptance-signoff.md` | UNSIGNED |

---

## Ports the operator must know

**Verified Fact.** FD-13.

| Host port | Service | Identity on `/api` |
|---|---|---|
| 8080 | Legacy | None. Port stays ungated |
| 8090 | Source gateway | None. Port stays ungated |
| 8091 | Lake REST | `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` |
| 8092 | Lake MCP | Same three headers |
| 8100 | Application A | Same three headers |
| 8110 | Application B | Same three headers |

Worked example. Phase 8 Team-Force pasted port 8080 `{"status": "ok", "service": "fabpulse-legacy"}` and port 8090 `{"status": "ok", "service": "source-gateway", "domain": "High Tech"}`. Honesty: REAL for that paste on 2026-10-18. This unit did not repeat that paste.

---

## Host files Application A keeps across a recreate

**Verified Fact.** Phase 13 SC-30-01.

- `apps/app_a/runtime/dlq.sqlite3`
- `apps/app_a/runtime/checkpoints.sqlite3`
- `apps/app_a/audit/audit_chain.sqlite3`

A later recreate of `app-a` still opens those host files. Measured recreate seconds stay Unknown. A live recreate is NEEDS_HUMAN.

---

## What this index does not hand over

- A named on-call person.
- Official Birlasoft brand assets. BO-12 stays PROPOSED.
- A signed production certificate.
- An Azure key.
- A live stack that this unit started.
