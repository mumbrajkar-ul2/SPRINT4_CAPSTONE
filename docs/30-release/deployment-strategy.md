# Deployment strategy

| Field | Value |
|---|---|
| Stage | Phase 13 / 30 Release and rollback. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-30a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No compose edit in this half. |
| Evidence sources | FD-19; FD-13; `compose.yaml`; `Dockerfile.platform`; `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/Dockerfile`; `.github/workflows/verify.yml`; `docs/29-incident-bcdr/dr-plan.md`; `tests/platform/test_compose_ci.py` |
| Assumptions | `MODEL_MODE=replay`. The person deploys from the capstone root. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Measured recreate seconds stay Unknown. A container registry stays unused. A percent of traffic to a second Application A copy stays unused. This product runs one laptop set. |
| Residual risks | Binding a missing sqlite path as a file mount can create a directory. Rebuilding `legacy` writes a new image copy of packaged sqlite; the freeze hash still comes from the packaged file on disk, which stays unread-write in tests. |

This file names how the seven named containers are replaced. Deploy here means rebuild the image from the git tree and recreate the named Compose service.

Engineering decision ED-P13-30A-03, authority: team-force. Deploy is Compose recreate of named services. There is no second replica and no traffic split. Half B recreates `app-a` only for HB-30-01.

---

## Finding

**Finding.** Seven named services already live in one `compose.yaml`. Platform services build from `Dockerfile.platform` at the capstone root. `legacy`, `source-gateway`, and `bridge` build from the packaged workshop Dockerfile. There is no rolling set of extra copies. `bridge` runs once and stays `restart: "no"`. Health probes `/health` every 10 seconds, times out at 4 seconds, retries 5 times, and waits 15 seconds on the platform listeners. Those integers are probe settings. They are not a recovery-time floor. Half B adds three host file binds on `app-a` and recreates that one service.
**Evidence.** `compose.yaml` services and `healthcheck` keys. `Dockerfile.platform`. `test_compose_ci.py` required container names. FD-13.
**Impact.** Half B does not add a replica, a proxy, or a registry push.
**Risk.** Recreating all seven services at once would also bounce 8080 and 8090. HB-30-01 recreates `app-a` only.
**Confidence.** High on the current Compose map. Unknown on measured recreate seconds.
**Open questions.** HALF_A_ACCEPTED. Live `docker compose up --force-recreate app-a` if the sandbox allows it.

---

## Locked facts this design applies

**Verified Fact.** FD-13. One Compose file at the capstone root. Host ports 8080, 8090, 8091, 8092, 8100, 8110.

**Verified Fact.** FD-19. Numeric recovery-time and availability floors stay Unknown. Replay is the path when the live model is off.

**Verified Fact.** Ports 8080 and 8090 stay ungated. This file adds no identity env on `legacy` or `source-gateway`.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

---

## How each service is replaced

| Service | Image source | Host port | Recreate command | Extra volume today |
|---|---|---|---|---|
| `legacy` | Workshop Dockerfile | 8080 | `docker compose up -d --build --force-recreate legacy` | Named volume `legacy_data` |
| `source-gateway` | Workshop Dockerfile | 8090 | same pattern for `source-gateway` | none |
| `bridge` | Workshop Dockerfile | none | runs once. `restart: "no"` | `legacy_data` |
| `lake-rest` | `Dockerfile.platform` | 8091 | same pattern for `lake-rest` | `context-lake/generated` read-only |
| `lake-mcp` | `Dockerfile.platform` | 8092 | same pattern for `lake-mcp` | `context-lake/generated` read-only |
| `app-a` | `Dockerfile.platform` | 8100 | same pattern for `app-a` | `operations/model-replay` read-only. After SC-30-01 also the three sqlite files |
| `app-b` | `Dockerfile.platform` | 8110 | same pattern for `app-b` | `operations/model-replay` read-only |

Worked example. Application A code changed. The person creates the three host sqlite files if they are missing. The person runs `docker compose up -d --build --force-recreate app-a` from the capstone root. Compose rebuilds `Dockerfile.platform`. The new `fabpulse-app-a` still publishes 8100. After SC-30-01 it still opens the host dead-letter file.

Worked example. The person needs the full set. `docker compose up --build` from the capstone root starts all seven names. `bridge` exits after one pass. The other six keep their health probes.

This laptop runs one `fabpulse-app-a`. A percent of traffic to a second copy stays unused.

---

## Image and git

`Dockerfile.platform` copies `apps`, `context-lake`, `operations`, and selected workshop paths into `/opt/platform`. **Verified Fact** of that file.

A deploy uses the files in the current git checkout. Rollback of the image is checkout of the previous tree, then `docker compose up --build` for the service that changed. See `rollback-plan.md`.

CI does not push an image. `verify.yml` runs pytest and `docker compose config`. **Verified Fact** of that workflow.

---

## SC-30-01 volume lines Half B writes

On service `app-a`, after the existing replay bind, Half B adds these three lines:

```yaml
      - ./apps/app_a/runtime/dlq.sqlite3:/opt/platform/apps/app_a/runtime/dlq.sqlite3
      - ./apps/app_a/runtime/checkpoints.sqlite3:/opt/platform/apps/app_a/runtime/checkpoints.sqlite3
      - ./apps/app_a/audit/audit_chain.sqlite3:/opt/platform/apps/app_a/audit/audit_chain.sqlite3
```

Those binds are read-write. The process writes parked rows, checkpoint waits, and audit rows.

Before `docker compose up`, Half B creates each host path as a file if it is missing. A missing path would let Docker create a directory, and sqlite would fail to open that path as a database.

`.gitignore` already ignores `apps/app_a/runtime/*.sqlite3` and `apps/app_a/audit/audit_chain.sqlite3`. The files stay on the laptop. They are not the git version.

Container paths match `Path(__file__).resolve().parents[3]` in `dlq.py`, `checkpointer.py`, and `audit/store.py` when `WORKDIR` is `/opt/platform`. **Inference**, authority: team-force, from those files plus `Dockerfile.platform` `WORKDIR /opt/platform`.

Tests may keep using `APP_A_DLQ_PATH`, `APP_A_CHECKPOINT_PATH`, and `APP_A_AUDIT_PATH` on temp files. Pytest does not need the Compose bind.

---

## Failure modes and recovery

| Id | Failure | Recovery | Numeric floor |
|---|---|---|---|
| FM-30-01 | Recreate without the three binds | Host copy is the restore source. After SC-30-01 the bind is the running file | Recovery point Unknown |
| FM-30-04 | Host sqlite path missing, Docker created a directory | Stop the service. Remove that directory. Create a file. Start again | None invented |
| FM-30-05 | Named container exits | `docker compose up` for that service | Restart seconds Unknown |
| FM-27-07 continued | Health probe fails five times | Read logs. Fix the tree. Recreate | Probe settings stay 10s / 4s / 5 / 15s. Not a floor |

---

## Dead-letter queue and replay

Deploy of `app-a` after SC-30-01 keeps the host dead-letter file. Replay of a parked row uses `POST /api/recovery/dlq/replay` as built in SC-28-01. This deploy adds no new replay route.

Language-model replay files stay on `./operations/model-replay` read-only.

---

## Runbook — recreate Application A

1. Create `apps/app_a/runtime/dlq.sqlite3`, `apps/app_a/runtime/checkpoints.sqlite3`, and `apps/app_a/audit/audit_chain.sqlite3` as files if they are missing.
2. Confirm `MODEL_MODE=replay`. Leave Azure unset.
3. From the capstone root: `docker compose up -d --build --force-recreate app-a`.
4. `GET /health` on 8100. HTTP 200 means the new process accepted the probe.
5. `GET /api/recovery` with the three identity headers. Confirm parked rows from the host file.
6. Leave 8080 and 8090 unchanged.

---

## SLOs and observability

`/health` HTTP 200 after recreate proves the new process accepted a GET. Compose healthcheck integers prove the probe settings in the file. Neither cell is an availability percent. **Verified Fact.** FD-19.

JSON logs on stdout still carry `duration_ms` for that one request. API p95 stays Unknown.

---

## Cost and the 0C envelope

Rebuild and recreate add no live model token. Token line B1 stays 0 and 0 under replay. Lines B2 to B7 stay Unknown. This half claims no dollar benefit for a recreate.

---

## Exact Half B check

HB-30-01 in `release-plan.md`. Half B writes the three volume lines on `app-a` only. Half B does not add a replica. Half B does not wrap 8080 or 8090.

---

## What this file does not do

This file names Compose recreate as the deploy. It leaves `compose.yaml` unchanged in this half. It adds no replica and no registry. It starts no Half B.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
