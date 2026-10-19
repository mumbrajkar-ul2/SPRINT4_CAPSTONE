# Operational runbook for logs and service levels

| Field | Value |
|---|---|
| Stage | Phase 13 / 31 Observability and service levels. Half B evidence. SC-31-01 / HB-31-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-31b-doc-20261018-001 |
| Status | MEASURED. Walk 3 now finds `event=replay_miss`. A copy sits at `operations/operational-runbook.md`. Numeric floors stay Unknown. |
| Evidence sources | FD-19; FD-13; FD-15; `observability-architecture.md`; `ai-telemetry-spec.md`; `agent-telemetry-spec.md`; `slo-sla-definitions.md`; `error-budget-policy.md`; `operations/ai-incident-playbook.md`; `operations/containment-procedures.md`; `compose.yaml`; `apps/shared/jsonlog.py`; `apps/app_a/routes/query.py`; `apps/app_a/routes/recovery.py` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. The person can run `docker compose logs` from the capstone root. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Company on-call title stays Unknown. INC-2025-014 owner stays Unknown. |
| Residual risks | Setting `MODEL_MODE=azure` to get a louder log would open a public-network socket. Deleting a parked row would hide a failure. Adding a metrics product would add a collector this stack does not run. |

This file names how a person reads logs on this laptop stack and how that person walks a miss. Continuity and disaster steps stay in `operations/ai-incident-playbook.md`, `operations/containment-procedures.md`, `operations/bc-plan.md`, and `operations/dr-plan.md`. This file adds the log walk.

Engineering decision ED-P13-31A-06, authority: team-force. Half B may copy this file to `operations/operational-runbook.md`. That copy is a file placement. The one coded check stays HB-31-01.

---

## Finding

**Finding.** Four incident runbooks already sit in `operations/`. A person already lists parked intake on `GET /api/recovery` and reads the agent trace on `GET /api/audit/{correlation_id}`. Gated listeners already write JSON lines on stdout. Half B added the `replay_miss` line and copied this walk into `operations/operational-runbook.md`.
**Evidence.** Glob of `operations/*.md` at the capstone root. HB-28-01. HB-29-01. `jsonlog.emit`. `apps/app_a/routes/query.py` emit on miss. FD-19. `telemetry-results.md`.
**Impact.** A person greps `event=replay_miss` on Application A query. Half B adds no new HTTP route.
**Risk.** Filling `owner_id` for INC-2025-014 with a demo actor would invent a person.
**Confidence.** High on the current routes and the measured `replay_miss` line. Unknown on availability percent.
**Open questions.** Reviewer grades HB-31-01. INC-2025-014 owner.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. A failed intake stays visible. Numeric latency, availability, error-budget, and recovery floors stay Unknown.

**Verified Fact.** FD-13. Compose default `MODEL_MODE=replay`. JSON logs on stdout with `service`, `event`, and `correlation_id`.

**Verified Fact.** Containment default CON-29-01. Keep `MODEL_MODE=replay`. Do not set `azure` on the laptop. Do not delete a parked intake row. Do not retry an injection BLOCK.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. This half invents no signer.

---

## Before the person starts

| Check | Command or read | Expected |
|---|---|---|
| Mode | Process environment `MODEL_MODE` | `replay` |
| Health | `GET http://127.0.0.1:8100/health` | HTTP 200 `{"ok": true}` |
| Identity | Three headers on `/api` | `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` |
| Correlation | Header on the walk | A string the person chose, for example `corr-p13-31-walk-001` |

Worked example. From `c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE` the person runs `docker compose logs --no-color app-a`. Lines that start with `{` are JSON objects. The person searches that text for `"correlation_id":"corr-p13-31-walk-001"`.

Ports 8080 and 8090 stay without `jsonlog.emit`. The person reads those containers for their own server text. **Verified Fact.**

---

## Walk 1. Process up

1. `GET /health` on 8100, 8110, 8091, and 8092.
2. Each GET returns HTTP 200 `{"ok": true}`.
3. Grep that service stdout for `event=health_ok`.

Recovery if a GET fails: start that named Compose service again. Seconds until 200 stay Unknown. See `operations/dr-plan.md`.

This walk does not fill SLO-N4. **Verified Fact.** FD-19.

---

## Walk 2. Identity miss

1. `GET /api/identity-check` on 8100 with no headers.
2. HTTP 401. Body `error_class` is `missing_identity`.
3. Grep stdout for `event=identity_missing` and `service=app-a`.
4. Confirm the line has no `api_key` field and no `local-demo-only` string.

Recovery: send the three headers. If the process has no `FABPULSE_API_KEY`, HTTP 503 and `event=server_key_missing`. Set the variable from `.env.example`. See `docs/27-hardening/secrets-hardening.md`.

Honesty on the 401 line: REAL in `test_logs.py`.

---

## Walk 3. Replay miss

1. Keep `MODEL_MODE=replay`. Azure variables unset.
2. `POST /api/query` on 8100 with the three identity headers and `X-Correlation-Id: corr-p13-31-walk-001`.
3. Body question `What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file`.
4. HTTP 200. `verdict` is `ABSTAIN`. `error_class` is `replay_miss` when retrieve found that item.
5. Grep stdout for that correlation id. The person sees `request_ok`. After HB-31-01 the person also sees `event=replay_miss` with `model_mode=replay`.

Measured HB-31-01 used header `X-Correlation-Id: corr-p13-31b-doc-20261018-001`. Before SC-31-01, step 5 found `request_ok` only. After SC-31-01, step 5 also found one `replay_miss` line. Honesty: REAL in `telemetry-results.md`. A cited answer such as GQ-23 is not labeled `replay_miss`.

Recovery: keep replay. Add a PRECOMPUTED file only in a later rehearsal. Do not set `MODEL_MODE=azure` on this laptop. **Verified Fact.** CON-29-01.

---

## Walk 4. Parked intake

1. `GET /api/recovery` with identity headers.
2. Read `parked_intakes`.
3. Grep stdout for `event=intake_parked` and `event=intake_replayed`.
4. Leave every row in the list.

Worked example. `message_id` `DLQ-28-BAD` stayed `PARKED` after replay. Honesty: REAL in `failure-injection-results.md`.

Recovery: `POST /api/recovery/dlq/replay` with `parked_id`. The row stays listed. See `operations/ai-incident-playbook.md`.

---

## Walk 5. Agent trace

1. Take the correlation id from the agent POST header, or from a minted `corr-app-a-` value in the response.
2. `GET /api/audit/{correlation_id}` with identity headers.
3. Read `rows` in `seq` order. Check `step_name`, `opa_verdict`, and `decision`.
4. Grep stdout for the same id. Expect `request_ok` on the agent path.

Recovery if `rows` is empty: the graph wrote nothing for that id. Re-run with a known header. Do not invent a step. See `agent-telemetry-spec.md`.

---

## Walk 6. Injection BLOCK

1. POST a query or agent body that carries approve-or-ignore text and a write action.
2. HTTP 409. `error_class` is `blocked`.
3. Audit row `event_type` `EV-12` when the agent path ran.
4. Leave the case unchanged.

Recovery: do not retry BLOCK. **Verified Fact.** CON-29-01. SLO-B3.

---

## Join key

| Source | Field | Example |
|---|---|---|
| Request header | `X-Correlation-Id` | `corr-p13-31-walk-001` |
| Stdout JSON | `correlation_id` | Same string, or null when the header was empty |
| Audit table | `correlation_id` and `thread_id` | Same string on an agent run |
| Dead-letter row | `correlation_id` | String stored at park time |

Worked example. Empty header on `GET /health` writes `correlation_id` null. The person still sees `event=health_ok` and `service=app-a`.

---

## Failure modes and recovery

| Id | What failed | First action |
|---|---|---|
| FM-31-01 | No JSON line from a gated listener | Restart that Compose service. Repeat Walk 1 |
| FM-31-02 | Replay miss has no stdout line | Confirm SC-31-01 is present. Grep `event=replay_miss`. Use the HTTP `error_class` if the line is still missing |
| FM-31-03 | Secret text on stdout | Rotate `FABPULSE_API_KEY`. See the 27 secrets runbook |
| FM-31-06 | Temptation to set `azure` | Keep `replay`. See CON-29-01 |
| FM-31-07 | Empty audit GET | Re-run with a known id |
| FM-31-08 | Urge to delete a parked row | Leave the row |

---

## SLOs and observability

This runbook proves one request or one listed row. It does not fill SLO-N1 to SLO-N8. **Verified Fact.** FD-19. FD-11.

| Walk | Behaviour it supports |
|---|---|
| Walk 1 | Process up for that GET |
| Walk 2 | SLO-B9 |
| Walk 3 | SLO-B4 on the miss path |
| Walk 4 | FD-19 intake visibility |
| Walk 5 | SLO-B10 |
| Walk 6 | SLO-B3 |

---

## Cost and the 0C envelope

These walks stay on replay. Token line B1 stays 0 and 0. This file claims no dollar benefit. **Verified Fact.** FD-19.

---

## Half B check

HB-31-01 is Walk 3 after the emit lands. Before: step 5 found `request_ok` only. After: step 5 also finds `event=replay_miss`. Honesty: REAL. Half B copied this file to `operations/operational-runbook.md`.

---

## What this file does not do

This file names the log walk. Half B wrote the miss line and copied this walk to `operations/`. It does not add a metrics product. It does not invent a percent. It does not name a person for INC-2025-014.
