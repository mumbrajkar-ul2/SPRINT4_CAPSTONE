# Operator exercises

| Field | Value |
|---|---|
| Stage | Phase 15 / 38 Handover. Operator exercises |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE as written drills. Live Compose and live HTTP stay NEEDS_HUMAN |
| Evidence sources | `operations/operational-runbook.md`; `docs/30-release/deployment-strategy.md`; `docs/30-release/rollback-plan.md`; `docs/23-human-control/audit-chain.md`; `docs/24-security-privacy/security-test-results.md`; `docs/_playbook-log.md` Phase 10 kill; FD-13; FD-19; FD-21; CON-29-01 |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. The operator has Docker on the laptop when a live step is later run |
| Unresolved issues | Docker state on this laptop today is Unknown to this unit. Recovery seconds Unknown |
| Residual risks | Inventing a health 200. Claiming a new process kill. Setting `MODEL_MODE=azure` |

These three exercises let an operator deploy, observe, and recover. Each live command that needs a running stack is marked NEEDS_HUMAN. This unit did not start Compose. This unit did not kill a process.

---

## Finding

**Finding.** The operator can deploy from one Compose file, observe from logs and audit, and recover a parked intake or a replay miss. Injection BLOCK is left unchanged. A mid-approval restart is already measured as the Phase 10 kill of pid 29320. This unit cites that result. It does not run a new kill.
**Evidence.** Phase 8 health paste. Phase 10 `corr-p10b-kill-20261018-001` on `PS000000016`. Phase 12 HTTP 409 BLOCK. Phase 13 walks 1 to 6.
**Impact.** Handover has a drill list. Live pass cells stay empty until a person runs them.
**Risk.** Filling a live pass from an older paste without saying the date.
**Confidence.** High on the written steps. Unknown on today's containers.
**Open questions.** Who runs the first live drill. INC-2025-014 owner.

---

## Exercise 1. Deploy

Goal. The six listeners that stay up after `bridge` exits are healthy. `MODEL_MODE` is `replay`.

| Step | Action | Expected | Live status |
|---|---|---|---|
| D1 | From the capstone root, read `compose.yaml` and `.env.example` | Ports 8080, 8090, 8091, 8092, 8100, 8110. Key default `local-demo-only` | Paper. Files on disk. Verified Fact |
| D2 | Confirm process environment will use `MODEL_MODE=replay` | Compose default `${MODEL_MODE:-replay}` | Paper. Verified Fact of `compose.yaml` |
| D3 | `docker compose up --build` | Six health probes start. `bridge` exits after one pass | NEEDS_HUMAN |
| D4 | `GET http://127.0.0.1:8100/health` and `GET http://127.0.0.1:8110/health` | HTTP 200 `{"ok": true}` | NEEDS_HUMAN |
| D5 | `GET http://127.0.0.1:8080/health` | Prior paste was `{"status": "ok", "service": "fabpulse-legacy"}` | NEEDS_HUMAN for a new GET. Prior REAL on 2026-10-18 |

Worked example. Phase 8 Team-Force pasted 8080 and 8090 health on 2026-10-18. That paste is prior REAL. It is not this unit's live pass.

If D3 cannot run, stop. Do not invent a pass.

---

## Exercise 2. Observe

Goal. The operator can join a request to a log line and an audit row by correlation id.

Identity headers for gated `/api` calls:

| Header | Value in drills |
|---|---|
| `X-Api-Key` | `local-demo-only` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |
| `X-Correlation-Id` | A string the operator chooses, for example `corr-p15-observe-001` |

| Step | Action | Expected | Live status |
|---|---|---|---|
| O1 | `GET /api/identity-check` on 8100 with no headers | HTTP 401. `error_class` is `missing_identity` | NEEDS_HUMAN. Prior REAL in `test_logs.py` |
| O2 | `GET /api/audit/{correlation_id}` after an agent run | `rows` ordered by `seq`. Columns include `step_name`, `opa_verdict`, `decision` | NEEDS_HUMAN. Design is FD-23 |
| O3 | `docker compose logs --no-color app-a` and search the correlation id | JSON lines with `service`, `event`, `correlation_id` | NEEDS_HUMAN |
| O4 | Paper read of Walk 3 in `operations/operational-runbook.md` | A replay miss writes `event=replay_miss`. Prior measured header `corr-p13-31b-doc-20261018-001` | Paper. Prior REAL |

Worked example. Empty header on `GET /health` writes `correlation_id` null and still writes `event=health_ok`. Honesty: REAL in the Phase 13 runbook.

---

## Exercise 3. Recover

Goal. The operator can list a parked intake, leave an injection BLOCK unchanged, and cite the already-measured restart.

| Step | Action | Expected | Live status |
|---|---|---|---|
| R1 | `GET /api/recovery` on 8100 with identity headers | `parked_intakes` listed. Leave every row | NEEDS_HUMAN. Prior REAL `DLQ-28-BAD` stayed PARKED |
| R2 | Paper read of Phase 12 HB-24-01 after | `POST /api/agent/run` on `REPLAY-000000000` with `proposed_action=approve` and no corpus id returned HTTP 409 BLOCK. Case unchanged | Paper. Prior REAL. Do not retry BLOCK |
| R3 | Paper read of Phase 10 coordinator kill | pid 29320 killed. New process on port 8765. Case `PS000000016` still carried `corr-p10b-kill-20261018-001`. `engineering_hold` stayed 0 | Paper. Prior REAL. This unit does not kill a process |
| R4 | If health on 8100 fails after a code change | Restore the previous git tree. Recreate `app-a`. Host sqlite files stay | NEEDS_HUMAN. Seconds Unknown |

Worked example for R2. Before SC-24-01 the same POST returned HTTP 200 and waited. After SC-24-01 it returned HTTP 409, `opa_verdict=BLOCK`, `waiting` false, empty approvals. Honesty: REAL in `docs/24-security-privacy/security-test-results.md`.

Worked example for R3. The coordinator recorded `corr-p10-kill-20261018-001`. Restart pid was 30216. This unit cites those numbers. It does not claim a new live kill.

---

## What the operator must not do

- Set `MODEL_MODE=azure` on this laptop for a drill.
- Delete a parked intake row.
- Retry an injection BLOCK as EXECUTE.
- Fill INC-2025-014 `owner_id` with a made-up name.
- Publish a match percent from the 12 matched and 2 differing harness rows.
