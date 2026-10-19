# Rollback plan

| Field | Value |
|---|---|
| Stage | Phase 13 / 30 Release and rollback. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-30a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No rollback code in this half. |
| Evidence sources | FD-19; FD-13; FD-15; `compose.yaml`; `docs/29-incident-bcdr/dr-plan.md`; `operations/dr-plan.md`; `apps/app_a/runtime/dlq.py`; `apps/app_a/routes/recovery.py`; `.gitignore` |
| Assumptions | `MODEL_MODE=replay`. Git history of `compose.yaml` is the previous file. BO rows that are PROPOSED stay PROPOSED. Half B proves one parked row on a host sqlite file after a new open. |
| Unresolved issues | Measured recreate seconds stay Unknown. Recovery-point row-count floor stays Unknown. Application B audit sqlite stays a process file. |
| Residual risks | Rolling back `compose.yaml` to today's file would remove the three binds and drop in-container sqlite on the next recreate. In-memory `_LAST` and the circuit flag always drop on process exit. |

This file names how a person puts the previous Compose tree back and keeps the three Application A sqlite files. Rollback here is git restore of the changed files plus `docker compose up` against the host sqlite files.

Engineering decision ED-P13-30A-06, authority: team-force. After SC-30-01, a container recreate of `app-a` keeps `dlq.sqlite3`, `checkpoints.sqlite3`, and `audit_chain.sqlite3` because those paths are host binds. Today, without those binds, those in-container files drop. The host copies are then the restore source.

---

## Finding

**Finding.** `docs/29-incident-bcdr/dr-plan.md` already names RS-29-03, RS-29-04, and RS-29-05 as process files inside `app-a`. Recreating that container without a host copy drops the in-container sqlite. Half B bind-mounts the three host files so a recreate keeps them. Rollback of a bad Compose edit is `git checkout -- compose.yaml` on the previous tree, then `docker compose up` for the service that failed. After SC-30-01 a rollback recreate still opens the same host sqlite files. `_LAST` and the circuit flag still drop because they live in memory. Ports 8080 and 8090 stay ungated.
**Evidence.** `dr-plan.md` restore table. `compose.yaml` `app-a` volumes today. FD-15. `recovery.py` `_LAST`. ED-P13-28A-04 circuit flag.
**Impact.** Half B proves the data side of rollback: a parked row on the host file is still listed after a new process opens that file. Code rollback stays git plus Compose.
**Risk.** Checking out today's `compose.yaml` after Half B would remove the binds. The next recreate would drop in-container sqlite again.
**Confidence.** High on today's volume list. Unknown on measured recreate seconds.
**Open questions.** HALF_A_ACCEPTED. Live `docker compose up -d --force-recreate app-a` if Docker is present.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric recovery-time and recovery-point floors stay Unknown. A failed intake stays visible. Replay is the path when the live model is off.

**Verified Fact.** FD-13. `MODEL_MODE=replay`. Host ports 8080 and 8090 stay ungated.

**Verified Fact.** Today `app-a` bind-mounts only `./operations/model-replay` as read-only. **Verified Fact** of `compose.yaml`.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

---

## Two parts of a rollback

| Part | What the person restores | How |
|---|---|---|
| Code | Previous `compose.yaml`, application files, and image build from that git tree | `git checkout` of the previous commit or of the named files. Then `docker compose up --build` for the service that changed |
| Sqlite files | Parked intake rows, checkpoint waits, audit rows | After SC-30-01 the host files are the running files. Before SC-30-01 copy the host files in, or park again |

Worked example after SC-30-01. Half B added the three binds. Health on 8100 fails. The person restores the previous application files from git, keeps the three volume lines, and recreates `app-a`. The host `dlq.sqlite3` still holds `DLQ-30-ROLL`. `GET /api/recovery` lists it. Seconds until health 200 stay Unknown.

Worked example today, before SC-30-01. The person recreates `app-a`. The new container opens an empty default `dlq.sqlite3`. `parked_intakes` is empty. The host pytest file from HB-28-01 still exists on disk if the test used `APP_A_DLQ_PATH`. That host file is the restore source. The person points `APP_A_DLQ_PATH` at it, or copies it onto the default path.

---

## What drops even after SC-30-01

| Item | Where it lives | After recreate |
|---|---|---|
| `_LAST` recovery status | Process memory | Dropped. Next `GET /api/recovery` shows no upstream probe until a new probe runs |
| Circuit flag | Process memory | Dropped. Next probe calls the gateway |
| Application B `audit_chain.sqlite3` | Process file inside `app-b` unless copied | Dropped on `app-b` recreate. Half B does not bind it |
| In-container sqlite without a bind | Image filesystem | Dropped |

Those drops stay visible. Do not hide an empty recovery probe by inventing a last status.

---

## Failure modes and recovery

| Id | Failure | Rollback | Numeric floor |
|---|---|---|---|
| FM-30-01 | Recreate dropped in-container sqlite | Use the host copy. After SC-30-01 the bind is the running file | Recovery point Unknown |
| FM-30-02 | Bad Compose edit, health not 200 | Restore previous `compose.yaml` from git. Recreate the service | Restart seconds Unknown |
| FM-30-04 | Docker created a directory on a sqlite path | Stop the service. Remove the directory. Create a file. Start again | None invented |
| FM-30-08 | Rollback checkout removed the three binds | Put the three volume lines back. Recreate `app-a` | None invented |
| FM-29-08 continued | Process restart during an approval wait | Reload `checkpoints.sqlite3` when that file is the same host file | None invented |

---

## Dead-letter queue and replay

Rollback does not delete parked rows. After SC-30-01 the new process opens the host dead-letter file. `GET /api/recovery` lists `PARKED` and `REPLAYED` rows that were already written. Same-body replay of an invalid payload stays `PARKED`. Language-model replay files already survive on `operations/model-replay/`.

If the bind was missing and the list is empty, leave the list empty. Park again using SC-28-01, or copy the host file onto the path the process opens.

---

## Runbook — roll back Application A

1. `GET /health` on 8100. If it is 200, read `GET /api/recovery` before you recreate, so you know whether parked rows are already on the host file.
2. Restore the previous git files for the bad change. Keep the three sqlite volume lines once SC-30-01 has landed.
3. Confirm the three host sqlite paths are files, not directories.
4. Confirm `MODEL_MODE=replay`. Leave Azure unset.
5. `docker compose up -d --build --force-recreate app-a`.
6. `GET /health` on 8100. HTTP 200 means the process accepted the probe.
7. `GET /api/recovery` with the three identity headers. Confirm parked rows. Confirm `owner_id` stays `None` until RT-06 supplies an owner. This half invents no name.
8. `GET /health` on 8080 and 8090 with no header. HTTP 200 means those ports stayed ungated.
9. Do not write packaged `legacy.sqlite3`. Do not write an 8-hour recovery claim next to the new health 200.

---

## SLOs and observability

| Signal | What it proves | What it does not prove |
|---|---|---|
| Health 200 after recreate | The rolled-back process accepted a GET | A recovery-time floor |
| Same `message_id` still `PARKED` | The host dead-letter file was the file this process opened | A recovery-point floor |
| Empty parked list | This process opened an empty file | That historical rows are gone from every host copy |

**Verified Fact.** FD-19. Do not copy the inherited 8-hour recovery note. Do not copy the inherited 24-hour recovery-point note.

---

## Cost and the 0C envelope

A rollback recreate adds no live model token. Token line B1 stays 0 and 0 under replay. Lines B2 to B7 stay Unknown. This half claims no dollar benefit for a rollback.

---

## Exact Half B check HB-30-01

Before: `compose.yaml` `app-a` volumes omit the three sqlite files. A recreate would drop in-container sqlite.

After: the three volume lines are present. Park `{"message_id": "DLQ-30-ROLL"}` on the host file. Close the connection. Open the same host file in a new connection, or recreate `app-a` if Docker is present. The row is still `PARKED`. `GET /health` is 200. `MODEL_MODE` is `replay`. 8080 and 8090 stay ungated.

That after row is the proven rollback of a container recreate against the host files. Git checkout of a bad application edit stays a documented step. Half B does not invent a second region.

---

## What this file does not do

This file names git plus Compose plus the three host sqlite files as rollback. It leaves `compose.yaml` unchanged in this half. It starts no Half B. It invents no recovery-time floor. It signs no Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
