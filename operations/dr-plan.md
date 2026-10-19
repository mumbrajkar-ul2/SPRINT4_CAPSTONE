# Disaster recovery plan

| Field | Value |
|---|---|
| Stage | Phase 13 / 29 Incident and BCDR. Half B operations copy. SC-29-01. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-29b-doc-20261018-001 |
| Status | OPERATIONS COPY. This file is the accepted design copied into `operations/`. No new Compose volume. Packaged sqlite stays unread-write. |
| Evidence sources | FD-19; FD-13; FD-15; `docs/29-incident-bcdr/dr-plan.md`; `compose.yaml`; `docs/27-hardening/runtime-hardening.md`; `docs/28-resilience/failure-injection-results.md`; `apps/app_a/runtime/dlq.py`; packaged `legacy.sqlite3` hash from Phase 0 / HB-28-01 |
| Assumptions | `MODEL_MODE=replay`. Packaged sqlite files stay `mode=ro`. BO rows that are PROPOSED stay PROPOSED. This product runs on the laptop Compose set. This file does not recreate production cloud regions. |
| Unresolved issues | Seconds until `/health` returns 200 after a stop stay Unknown. How much in-container sqlite is lost on recreate stays Unknown as a numeric recovery point. Company job titles stay Unknown. Recovery time stays Unknown. Recovery point stays Unknown. |
| Residual risks | Copying an inherited recovery-time note would present an unmeasured number as a floor. Writing into packaged `legacy.sqlite3` to "restore" would change the freeze hash. |

This file names how a person starts the laptop processes again after a stop. Restore here is Compose plus the files already on disk. This file does not name a second site.

Engineering decision ED-P13-29A-04, authority: team-force. Restore source ids `RS-29-01` to `RS-29-06`. Those ids name files and listeners. They do not set a recovery-time number. They do not set a recovery-point number.

---

## Finding

**Finding.** Compose health probes `/health` every 10 seconds, times out at 4 seconds, retries 5 times, and waits 15 seconds after start. Application A bind-mounts only `./operations/model-replay` as read-only. The dead-letter file default path is `apps/app_a/runtime/dlq.sqlite3`. The checkpoint file is `apps/app_a/runtime/checkpoints.sqlite3`. Those two sqlite files are not named in the `app-a` volume list. Recreating the `app-a` container without a host copy of those files drops the in-container copies. Packaged `legacy.sqlite3` stays `mode=ro`. HB-28-01 left its hash `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879`. In-memory `_LAST` recovery status is lost when the process exits. Numeric recovery-time and recovery-point floors stay Unknown.
**Evidence.** `compose.yaml` `app-a` `volumes` and `healthcheck`. `dlq.py` `DEFAULT_DLQ_PATH`. FD-15 checkpoint path. `failure-injection-results.md` packaged hash. `recovery.py` `_LAST`.
**Impact.** This copy records the restore order. TT-29-01 records health 200. This file does not add a new volume. This file does not write packaged sqlite.
**Risk.** Treating an inherited recovery-point note as this product's floor would skip FD-19.
**Confidence.** High on the Compose volume list and the packaged hash. Unknown on measured restart seconds.
**Open questions.** Measured restart seconds. Whether a later sub-stage 30 bind-mounts runtime sqlite.

---

## Locked facts this copy applies

**Verified Fact.** FD-19. Numeric recovery-time and recovery-point floors stay Unknown. Replay is the path when the live model is off. A failed intake stays visible. The parked intake from sub-stage 28 stays listed when the dead-letter file is the file the process opens.

**Verified Fact.** FD-13. Host ports 8080, 8090, 8091, 8092, 8100, 8110. `MODEL_MODE=replay`.

**Verified Fact.** Packaged `legacy.sqlite3` stays unread-write in Half B tests. Honesty of the HB-28-01 hash: REAL.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

---

## Restore sources

| Id | What it holds | Where it lives today | Survives `app-a` container recreate | Numeric recovery point |
|---|---|---|---|---|
| RS-29-01 | PRECOMPUTED model JSON | Host `operations/model-replay/`, bind-mounted read-only into `app-a` | Yes, the host folder stays | Unknown. Files are on the host |
| RS-29-02 | Packaged cases and lots | Packaged `legacy.sqlite3`, `mode=ro` | Yes, the packaged file stays | Unknown. Hash stayed `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879` in HB-28-01 |
| RS-29-03 | Parked intake rows | `apps/app_a/runtime/dlq.sqlite3` on the host for pytest. Inside the container when Compose writes the default path | Host pytest file stays. In-container file is dropped unless copied | Unknown |
| RS-29-04 | Approval wait | `apps/app_a/runtime/checkpoints.sqlite3` | Same as RS-29-03 | Unknown |
| RS-29-05 | Audit chain | `apps/app_a/audit/audit_chain.sqlite3` | Same as RS-29-03 | Unknown |
| RS-29-06 | Process list | `compose.yaml` seven named containers | Recreate with `docker compose up` | Restart seconds Unknown |

Worked example for RS-29-01. Compose line `./operations/model-replay:/opt/platform/operations/model-replay:ro` means the replay folder on the laptop is the same folder the container reads. Recreating `fabpulse-app-a` still reads those files.

Worked example for RS-29-03. HB-28-01 set `APP_A_DLQ_PATH` to a temp sqlite file on the host. That temp file stayed after the test process ended. A Compose `app-a` with no extra volume writes `apps/app_a/runtime/dlq.sqlite3` inside the image filesystem. Recreating that container starts with an empty default file unless the person copied the host file in. This file names that fact. This file does not add a volume.

In-memory `_LAST` is not a restore source. After a process exit the next `GET /api/recovery` shows `status_visible` `No upstream probe has run in this process yet.` until a new probe runs. Parked rows still come from the dead-letter file the process opens.

---

## Restore order

1. From the capstone root, start the named services with Compose. `docker compose up` for the service that exited, or for the full set if several exited.
2. Confirm `MODEL_MODE=replay` in the process environment. Compose default already is.
3. Confirm Azure variables are unset for the laptop demo.
4. `GET /health` on 8100. HTTP 200 means Application A accepted the probe. Repeat 8110, 8091, 8092, 8080, 8090 as needed.
5. `GET /api/recovery` with the three identity headers. Read `parked_intakes`. If the process opened the same dead-letter file as HB-28-01, `DLQ-28-BAD` stays listed. If Compose started with an empty in-container file, the list is empty until the person parks again. Either result stays visible. Do not hide an empty list by inventing a row.
6. Do not open packaged `legacy.sqlite3` for write. Do not change its hash to "complete" a restore.
7. If an approval wait was in progress and the checkpoint file is the same file, `thread_id` still loads. If the checkpoint file was dropped, the wait is gone. That loss stays visible as a missing wait. Seconds and bytes lost stay Unknown.
8. Do not write a recovery-time claim next to the new health 200. The number of seconds stays Unknown until a measured run.

This file is the operations copy of that order. Recovery time stays Unknown. Recovery point stays Unknown.

---

## Failure modes and recovery

| Id | Failure | Restore | Numeric floor |
|---|---|---|---|
| FM-29-05 | Named container exits | `docker compose up` for that service | Restart seconds Unknown |
| FM-29-08 | Process restart during wait | Reload `checkpoints.sqlite3` when that file is the same file | None invented |
| AI-INC-29-04 after recreate | Dead-letter file missing in the new container | Park again using SC-28-01, or point `APP_A_DLQ_PATH` at the host file | Recovery point Unknown |

---

## Dead-letter queue and replay

Restore does not delete parked rows. If the file survived, `GET /api/recovery` lists them. If the file did not survive, the person sees an empty list and parks again. Language-model replay files survive because they sit on the host bind mount.

---

## SLOs and observability

| Signal | What it proves | What it does not prove |
|---|---|---|
| `/health` HTTP 200 after Compose start | That process accepted a GET | A recovery-time floor |
| Packaged hash unchanged | Restore did not write packaged sqlite | A recovery-point floor |
| `parked_intakes` after start | Which dead-letter file this process opened | That every historical row still exists |

Recovery time stays Unknown. Recovery point stays Unknown. **Verified Fact.** FD-19. Do not copy an inherited recovery-time note. Do not copy an inherited recovery-point note.

---

## Cost and the 0C envelope

A Compose start adds no live model token. Token line B1 stays 0 and 0 under replay. Lines B2 to B7 stay Unknown. This file claims no dollar benefit for a restart.

---

## Exact Half B check

HB-29-01 records `GET /health` 200. It does not require a container kill. A process-level health GET is enough for the tabletop. Measured restart seconds after a Compose kill stay Unknown unless the reviewer later asks for that extra check. This file does not invent those seconds.

---

## What this file does not do

This file does not add a Compose volume. It does not start sub-stage 30. It does not write packaged sqlite. It does not invent a recovery-time floor. It does not invent a recovery-point floor. It does not sign a Business Owner row.
