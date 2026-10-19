# Runtime hardening

| Field | Value |
|---|---|
| Stage | Phase 13 / 27 Hardening. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-27a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No hardening code in this half. |
| Evidence sources | FD-13; FD-19; `compose.yaml`; `Dockerfile.platform`; `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/Dockerfile`; `apps/app_a/server.py`; `apps/app_b/server.py`; `apps/shared/jsonlog.py`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md` |
| Assumptions | One `docker compose up` still starts the seven named containers. Host ports stay 8080, 8090, 8091, 8092, 8100, 8110. `MODEL_MODE=replay`. |
| Unresolved issues | Restart-count floor stays Unknown. Recovery-time and recovery-point stay Unknown. Container user stays root in this sub-stage. |
| Residual risks | `Dockerfile.platform` has no `USER` line. The default user of `python:3.12-slim` is root. A later bind of 8080 or 8090 beyond the laptop would expose the fixture and the baseline case list. |

This file names how the laptop stack stays up, how a dead listener is brought back, and which runtime change this half defers. The one Half B control is SC-27-01 on the four gated listeners. This half does not add `USER` to the image.

---

## Finding

**Finding.** Seven named Compose services already publish six host ports and run a `/health` probe. Application A, Application B, lake REST, and lake MCP already disable FastAPI `/docs`. Health returns `{"ok": true}` and stays open. `Dockerfile.platform` copies the platform tree and runs as the image default user. Half B does not change the image user. Half B changes only the missing-key `/api` response.
**Evidence.** `compose.yaml` services `legacy`, `source-gateway`, `bridge`, `lake-rest`, `lake-mcp`, `app-a`, `app-b`. `Dockerfile.platform` has no `USER`. FastAPI `docs_url=None` in `apps/app_a/server.py` and `apps/app_b/server.py`.
**Impact.** Operators keep using `/health` and Compose healthchecks. HB-27-01 keeps health at 200. Compose still marks the process up when the key is missing.
**Risk.** Failing `/health` when the key is missing would stop Compose from marking `app-a` healthy even though the process is up.
**Confidence.** High on the Compose map. Unknown on restart time.
**Open questions.** HALF_A_ACCEPTED. Measured restart seconds. A later non-root user change.

---

## Locked facts this design applies

**Verified Fact.** FD-13. Docker Compose at the capstone root. Host ports 8080, 8090, 8091, 8092, 8100, 8110. JSON logs on stdout. No extra identity, metrics, graph, or policy container in Phase 8. This half adds no extra container.

**Verified Fact.** FD-19. Recovery-time and recovery-point stay Unknown. Replay is the path when the live model is off.

---

## What is running

**Verified Fact.** `compose.yaml`.

| Service | Container name | Host port | Health probe |
|---|---|---|---|
| `legacy` | `fabpulse-legacy` | 8080 | `GET http://127.0.0.1:8080/health` |
| `source-gateway` | `fabpulse-source-gateway` | 8090 | `GET http://127.0.0.1:8090/health` |
| `bridge` | `fabpulse-bridge` | none | `restart: "no"` after one pass |
| `lake-rest` | `fabpulse-lake-rest` | 8091 | `GET http://127.0.0.1:8091/health` |
| `lake-mcp` | `fabpulse-lake-mcp` | 8092 | `GET http://127.0.0.1:8092/health` |
| `app-a` | `fabpulse-app-a` | 8100 | `GET http://127.0.0.1:8100/health` |
| `app-b` | `fabpulse-app-b` | 8110 | `GET http://127.0.0.1:8110/health` |

Healthcheck interval is 10 seconds. Timeout is 4 seconds. Retries are 5. Start period is 20 seconds on the inherited listeners and 15 seconds on the platform listeners. Those numbers are Compose engineering defaults. Recovery-time stays Unknown. **Verified Fact** of the file. **Assumption** that they stay for this half.

Port 8080 and port 8090 stay ungated. **Verified Fact.** Compose comment and CT-35. A later wrap, if release work needs one, is named for sub-stage 30. This half does not add that wrap. This half does not add a login server.

---

## Image and process user

**Verified Fact.** `Dockerfile.platform` starts `FROM python:3.12-slim`. It has no `USER` line.

**Verified Fact.** The inherited workshop `Dockerfile` also has no `USER` line.

Control SC-27-07 records that FastAPI docs stay closed and health stays a small JSON object. Half B leaves those as built.

Control for a non-root image user stays deferred. Adding `USER` would be a second change. This half names one control: SC-27-01.

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery | Numeric floor |
|---|---|---|---|---|
| FM-27-01 | Process key missing | After Half B: `/api` HTTP 503 `missing_server_key`. `/health` HTTP 200 | Set `FABPULSE_API_KEY`. Restart the four gated listeners | None invented |
| FM-27-06 | Live model is off | Query abstains or uses a replay file | Keep `MODEL_MODE=replay`. Read `operations/model-replay/{sha256}` | Token line B1 stays 0 and 0 in the envelope |
| FM-27-07 | A named container exits | Compose health turns unhealthy after five failed probes | `docker compose up` for that service. `bridge` is one-shot and stays `restart: "no"` | Restart seconds Unknown |
| Listener bind fail | Port already taken | Process does not start | Free the host port. Start again | Unknown |

Worked example for FM-27-07. `app-a` dies. Compose marks it unhealthy after the probe fails five times at a 10-second interval, after the 15-second start period. The person starts that service again. The number of seconds until `/health` returns 200 stays Unknown until a measured run. Do not write 8 hours from the inherited runbook as this product's recovery time.

SqliteSaver file `apps/app_a/runtime/checkpoints.sqlite3` keeps an approval wait across a process restart. **Verified Fact.** FD-15. Audit file `apps/app_a/audit/audit_chain.sqlite3` keeps the trace. Retention days stay Unknown.

---

## Dead-letter queue and replay

Runtime restart does not park an identity miss. The next request is a new check.

Language-model replay stays `MODEL_MODE=replay`. **Verified Fact.** FD-19.

A bad intake message parked and replayed is sub-stage 28.

---

## Runbook — bring a listener back

1. `GET /health` on the host port. HTTP 200 means the process is up.
2. If health fails, read Compose logs for that container name.
3. If `/health` is 200 and `/api` is 503 `missing_server_key`, set `FABPULSE_API_KEY` and restart the four gated listeners.
4. If `/health` is 200 and `/api` is 401 `missing_identity`, send the three headers.
5. If the container is gone, start that service with Compose.
6. For Application A during an approval wait, the checkpoint file keeps the wait. The person resumes at the mapped RT role.

A copy of this runbook into `operations/` belongs to sub-stage 29.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| `/health` HTTP 200 | Each listener | The process accepted a GET | An availability percent |
| Compose healthcheck | `compose.yaml` | Five failed probes mark the service unhealthy | A recovery-time target |
| JSON `duration_ms` | stdout | Time for that one request | API p95 |
| JSON `event=server_key_missing` after Half B | stdout | SC-27-01 fired | A cost saving |

Availability, API p95, retrieval p95, recovery time, and recovery point stay Unknown. **Verified Fact.** FD-19. The 0C envelope left those cells Unknown. This half leaves them Unknown.

---

## Cost and the 0C envelope

A health GET adds no model token. A restart adds no model token. Token lines B2 to B7 stay Unknown. This half claims no dollar benefit for keeping health open.

---

## Exact Half B check HB-27-01

The same check as `identity-rbac-hardening.md`.

Runtime assertion on both before and after: `GET /health` on Application A returns HTTP 200 `{"ok": true}` while `FABPULSE_API_KEY` is unset. Compose healthchecks stay valid. Half B does not fail health to signal a missing key.

Half B does not add `USER` to `Dockerfile.platform`. Half B does not change port 8080 or port 8090.

---

## What this file does not do

This file does not write SC-27-01. It does not start Half B. It does not add a non-root user. It does not add a login server. It does not invent a recovery-time number. It does not sign a Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
