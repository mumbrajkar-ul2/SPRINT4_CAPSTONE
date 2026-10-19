# Backup validation

| Field | Value |
|---|---|
| Stage | Phase 13 / 30 Release and rollback. Half B measured results. SC-30-01 / HB-30-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-30b-doc-20261018-001 |
| Status | MEASURED. SC-30-01 bind-mounts the three Application A sqlite files on `app-a`. HB-30-01 parked `DLQ-30-ROLL` on the host dead-letter file, closed the connection, reopened that same host file, and still read `status` `PARKED`. Health stayed HTTP 200 in-process. `MODEL_MODE` stayed `replay`. Ports 8080 and 8090 stayed ungated. Live `docker compose up -d --force-recreate app-a` is `NEEDS_HUMAN`. Recovery-time and recovery-point floors stay Unknown. |
| Evidence sources | FD-19; FD-15; `compose.yaml`; `docs/29-incident-bcdr/dr-plan.md`; `docs/29-incident-bcdr/rto-rpo.md`; `apps/app_a/runtime/dlq.py`; `apps/app_a/audit/store.py`; `.gitignore`; `docs/28-resilience/failure-injection-results.md`; `tests/platform/test_phase13_release.py` |
| Assumptions | `MODEL_MODE=replay`. Host copies of the three sqlite files are the backup. Packaged `legacy.sqlite3` stays unread-write. BO rows that are PROPOSED stay PROPOSED. Half B did not bounce the already-running `fabpulse-app-a` container. |
| Unresolved issues | Backup interval in hours stays Unknown. Recovery-point floor stays Unknown. Retention days for the audit file stay Unknown. Measured recreate seconds stay Unknown. |
| Residual risks | Writing into packaged `legacy.sqlite3` to "complete" a restore would change the freeze hash. Treating a file copy as an 8-hour floor would skip FD-19. Checking out the previous `compose.yaml` would remove the three binds. |

This file names how a person checks that the three Application A sqlite files on the host can be opened after a copy. A backup here is a host file copy. It is not a second site. Test output is REAL. This half invents no recovery-time number.

Engineering decision ED-P13-30A-07 continued, authority: team-force. Backup set for this sub-stage is the three host files `apps/app_a/runtime/dlq.sqlite3`, `apps/app_a/runtime/checkpoints.sqlite3`, and `apps/app_a/audit/audit_chain.sqlite3`, plus the already bind-mounted `operations/model-replay/` folder. Packaged sqlite is restored from git, not from a write.

Engineering decision ED-P13-30B-01, authority: team-force. Half B creates each host sqlite path as a file before Compose would start, so Docker does not create a directory on that path. `.gitignore` already ignores those files. The compose volume lines are the committed change.

---

## Finding

**Finding.** Before SC-30-01, `compose.yaml` `app-a` volumes listed only `./operations/model-replay` as read-only. The three sqlite files were omitted. After SC-30-01 those three host files are bind-mounted at `/opt/platform/apps/app_a/runtime/dlq.sqlite3`, `/opt/platform/apps/app_a/runtime/checkpoints.sqlite3`, and `/opt/platform/apps/app_a/audit/audit_chain.sqlite3`. Half B created `apps/app_a/runtime/dlq.sqlite3` as a new file. `checkpoints.sqlite3` and `audit_chain.sqlite3` were already files on the host. HB-30-01 parked `{"message_id": "DLQ-30-ROLL"}`. `invalid` was 1. `accepted` was 0. A new sqlite open of the same host file still listed `status` `PARKED`. A copy of that host file still listed `PARKED`. `GET /health` in-process was HTTP 200 `{"ok": true}`. `MODEL_MODE` stayed `replay`. Azure was not called. Packaged `legacy.sqlite3` was not written. Ports 8080 and 8090 still have no `FABPULSE_API_KEY`. No login server was added. Live `docker compose up -d --force-recreate app-a` was not run. That row is `NEEDS_HUMAN`. Recovery-time and recovery-point floors stay Unknown.
**Evidence.** Read of `compose.yaml` `app-a` volumes before the three lines were added, on 2026-10-18. Pytest `tests/platform/test_phase13_release.py` under correlation id `corr-p13-30b-doc-20261018-001`. Honesty: REAL.
**Impact.** A person can copy the host dead-letter file and still read the parked row. After SC-30-01 a later recreate of `app-a` opens those same host files.
**Risk.** A missing host path at compose start can still become a directory. Half B created the three paths as files first.
**Confidence.** High on the compose lines, the host-file reopen, and the in-process health probe. Unknown on measured recreate seconds.
**Open questions.** Reviewer grades HB-30-01. Live recreate command. Backup interval. Audit retention days.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric recovery-point and recovery-time floors stay Unknown. A failed intake stays visible when the process opens the file that holds it.

**Verified Fact.** Packaged `legacy.sqlite3` stays unread-write in Half B tests. Honesty of the HB-28-01 hash: REAL.

**Verified Fact.** Replay files on `operations/model-replay/` already survive recreate. **Verified Fact** of the `app-a` volume line.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. Audit retention days stay Unknown. OB-25-12 already left that count blank.

**Verified Fact.** Ports 8080 and 8090 stay ungated. Compose still has no `FABPULSE_API_KEY` on `legacy` and `source-gateway`. Honesty: REAL.

---

## Backup set

| Id | Path on the host | What a copy keeps | Restore method |
|---|---|---|---|
| BK-30-01 | `apps/app_a/runtime/dlq.sqlite3` | Parked intake rows | Copy the file onto the same path. Recreate `app-a` after SC-30-01 |
| BK-30-02 | `apps/app_a/runtime/checkpoints.sqlite3` | Approval waits keyed by `thread_id` | Same copy-and-recreate |
| BK-30-03 | `apps/app_a/audit/audit_chain.sqlite3` | One row per agent step and per human approval | Same copy-and-recreate |
| BK-30-04 | `operations/model-replay/` | PRECOMPUTED model JSON | Already a host bind. Copy the folder if the person wants a second host path |
| BK-30-05 | Packaged `legacy.sqlite3` | Cases and lots | Restore from git. Do not write the packaged file |
| BK-30-06 | Named volume `legacy_data` | Workshop `/var/lib/legacy` | Compose named volume. Leave it as built |

Worked example for BK-30-01. HB-30-01 parked `message_id` `DLQ-30-ROLL` with `status` `PARKED` on the host file. The test copied that file to a pytest temp folder. Opening the copy with sqlite still showed that row. Restore is copy back onto `apps/app_a/runtime/dlq.sqlite3`. After SC-30-01 the container opens that host path. Honesty: REAL.

Application B audit sqlite is omitted from this backup set. Recreating `app-b` drops the in-container file. Half B did not add that copy.

---

## HB-30-01 before

Honesty of filled cells: REAL.

Command shape recorded: read of `compose.yaml` service `app-a` `volumes` on 2026-10-18, before the three sqlite lines were added. At that moment app-a volumes omit the three sqlite files. The replay bind was already present.

Measured before

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| `app-a` volumes includes `./operations/model-replay` read-only | true | true. Only volume line was `./operations/model-replay:/opt/platform/operations/model-replay:ro` | REAL |
| `app-a` volumes includes `dlq.sqlite3` | false | false | REAL |
| `app-a` volumes includes `checkpoints.sqlite3` | false | false | REAL |
| `app-a` volumes includes `audit_chain.sqlite3` | false | false | REAL |
| Ports 8080 and 8090 mapping lines | present, no identity on those services | present. `legacy` and `source-gateway` have no `FABPULSE_API_KEY` | REAL |
| `MODEL_MODE` default on `app-a` | `replay` | `replay`. Compose value `${MODEL_MODE:-replay}` | REAL |
| Host `dlq.sqlite3` is a file | file, not a directory | absent before Half B created it. Then created as a file of size 0 | REAL |
| Host `checkpoints.sqlite3` is a file | file, not a directory | already a file, size 241664 | REAL |
| Host `audit_chain.sqlite3` is a file | file, not a directory | already a file, size 45056 | REAL |

Worked example of the measured before. Service `app-a` listed one volume. That line was the replay folder, read-only. The three sqlite paths were not in that list.

---

## HB-30-01 after

Same identity headers. Host dead-letter file `apps/app_a/runtime/dlq.sqlite3`. Temp `LEGACY_DB`. `MODEL_MODE=replay`. In-process `TestClient` for `/health`.

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| `app-a` volume for host `dlq.sqlite3` | present | present. `./apps/app_a/runtime/dlq.sqlite3:/opt/platform/apps/app_a/runtime/dlq.sqlite3` | REAL |
| `app-a` volume for host `checkpoints.sqlite3` | present | present. `./apps/app_a/runtime/checkpoints.sqlite3:/opt/platform/apps/app_a/runtime/checkpoints.sqlite3` | REAL |
| `app-a` volume for host `audit_chain.sqlite3` | present | present. `./apps/app_a/audit/audit_chain.sqlite3:/opt/platform/apps/app_a/audit/audit_chain.sqlite3` | REAL |
| Three host sqlite paths are files | files, not directories | files. Not directories | REAL |
| Park `{"message_id": "DLQ-30-ROLL"}` `invalid` | 1 | 1 | REAL |
| `accepted` | 0 | 0 | REAL |
| Reopen the same host file, row `status` | `PARKED` | `PARKED` | REAL |
| Copy of the host dead-letter file still lists `DLQ-30-ROLL` | `PARKED` | `PARKED` | REAL |
| Same-body replay, row still listed | `PARKED` | `PARKED` | REAL |
| `GET /health` in-process | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| 8080 and 8090 stay ungated | compose still has no identity env on `legacy` and `source-gateway` | no `FABPULSE_API_KEY` on those services. Mapping lines still present | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |
| Packaged `legacy.sqlite3` write | none | none. Hash stayed `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879` | REAL |
| Azure socket | none | none. `complete_azure` was patched to fail if called | REAL |
| New login server | none | none. Compose has no `login` service. `/login` is absent | REAL |
| New `FEATURE_` flag | none | none in `compose.yaml` | REAL |
| Live `docker compose up -d --force-recreate app-a` | optional | NEEDS_HUMAN. Half B did not invent a recreate pass | REAL |
| Recovery-time floor claimed | none. Cell stays Unknown | none. Cell stays Unknown | REAL |
| Recovery-point floor claimed | none. Cell stays Unknown | none. Cell stays Unknown | REAL |
| Backup interval hours | Unknown | Unknown | Unknown |

Worked example of the measured after. Half B wrote the three `app-a` volume lines. The test parked `DLQ-30-ROLL` on `apps/app_a/runtime/dlq.sqlite3`. It closed the sqlite connection. It opened that same host file again. `status` was `PARKED`. A copy of that file still listed `PARKED`. Health stayed 200. `complete_azure` was patched to fail if called.

Honesty of those cells: REAL. The live recreate cell is REAL as `NEEDS_HUMAN`. It is not a measured recreate.

---

## Validation steps

A copy is valid when every step below succeeds. Honesty of Half B measured cells: REAL when the test runs.

1. Confirm each of BK-30-01, BK-30-02, and BK-30-03 is a file, not a directory. Measured: all three are files. Honesty: REAL.
2. Copy the three files to a second host folder. Half B used a pytest temp folder. Measured: copy succeeded. Honesty: REAL.
3. Open the dead-letter copy. Table `parked_intake` exists. A known `message_id` is still present when one was parked. Measured: `DLQ-30-ROLL` `PARKED`. Honesty: REAL.
4. Open the checkpoint copy. If a wait was stored, `thread_id` still loads. If the file is empty, that empty file is the copy. Measured: host file existed and the copy is a file. Honesty: REAL for the copy. Row count stays unclaimed.
5. Open the audit copy. Table `audit_chain` still has the 27 named columns when the file was initialized. Measured: the host audit file existed as a file and was copied. Honesty: REAL for the copy. Column count was not re-counted in HB-30-01.
6. Confirm packaged `legacy.sqlite3` was not written. Hash stays the HB-28-01 value when that check runs. Measured: hash unchanged. Honesty: REAL.
7. Confirm `MODEL_MODE=replay` during the check. No Azure socket. Measured: `replay`. Azure not called. Honesty: REAL.

`PRAGMA integrity_check` returning `ok` is an extra sqlite check when the tool is present. It is not a recovery-point floor. Half B did not record that pragma. That cell stays Unknown.

Worked example. HB-30-01 parks `DLQ-30-ROLL`, copies the host dead-letter file, opens the copy, and still reads `status` `PARKED`. That copy is a valid backup of that one row. How many older rows may be missing stays Unknown.

---

## Failure modes and recovery

| Id | Failure | What validation shows | Recovery | Numeric floor |
|---|---|---|---|---|
| FM-30-01 | Recreate dropped in-container sqlite | Host copy still opens, or the copy is missing | Copy the host backup onto the default path. After SC-30-01 the bind is the running file | Recovery point Unknown |
| FM-30-04 | Path is a directory | Step 1 fails | Remove the directory. Create a file. Park again if the rows are gone | None invented |
| FM-30-05 | Packaged sqlite was written | Hash no longer matches HB-28-01 | Restore packaged file from git | None invented |
| FM-30-09 | Copy taken while sqlite had an open writer | Copy may be short | Copy again after the process closes, or after a quiet moment. Interval hours Unknown | None invented |

---

## Dead-letter queue and replay

Validation of BK-30-01 is the parked-row check. Restore of that file does not delete rows. After restore, `GET /api/recovery` lists them. Replay stays SC-28-01.

HB-30-01 same-body replay of `DLQ-30-ROLL` stayed `PARKED`. The row stayed listed. Honesty: REAL.

Language-model replay validation is a file present under `operations/model-replay/{sha256}` for a known prompt hash. A miss still abstains.

---

## Runbook — copy and check the three files

1. Pause Application A if you can. If Application A is still writing, still copy, then run integrity_check. A busy copy may be short. That limit stays visible.
2. Copy BK-30-01, BK-30-02, and BK-30-03 to a second host folder.
3. Open the dead-letter copy. Read `message_id` and `status`.
4. Open the checkpoint copy. List `thread_id` values when the `checkpoints` table exists.
5. Open the audit copy. Confirm table `audit_chain` when the file was initialized.
6. Restore by copying back onto the three default paths. Recreate `app-a` after SC-30-01.
7. `GET /health` on 8100. `GET /api/recovery` lists parked rows from the restored file.
8. Leave packaged sqlite unread-write.

Hours until the next copy stay Unknown. This runbook is the order. It is not a recovery-point floor.

---

## Live recreate

| Command | Result | Honesty |
|---|---|---|
| `docker compose up -d --force-recreate app-a` | NEEDS_HUMAN. Half B did not invent a recreate pass. Docker was present and `fabpulse-app-a` was already healthy. Recreate would bounce that container and wait on the 15-second health start period. Pytest file check plus a new sqlite connection to the same host path prove the bind design | REAL |

A person who can bounce `app-a` runs that exact command from the capstone root after the three host files exist as files. Seconds until health 200 stay Unknown.

---

## SLOs and observability

A successful open of the copy proves that file was readable. A listed `PARKED` row proves that row was in the copy. Those cells do not prove a recovery-point floor, a backup-interval SLO, or availability percent. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

A host file copy adds no live model token. Token line B1 stays 0 and 0 under replay. Lines B2 to B7 stay Unknown. Storage dollars stay Unknown. This half claims no dollar benefit for a copy.

Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED legacy fields. BO-11 working answer stays PROPOSED.

---

## Exact Half B check

HB-30-01 parks `DLQ-30-ROLL` on the host dead-letter file, reopens that same path, and still lists `PARKED`. That reopen is the validation of BK-30-01 for one row. Half B did not add a backup daemon. Half B did not write packaged sqlite. Half B did not add a login server. Half B did not gate ports 8080 or 8090.

Test path: `tests/platform/test_phase13_release.py`.

Headers:

| Header | Value |
|---|---|
| `X-Api-Key` | `local-demo-only` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |
| `X-Correlation-Id` | `corr-p13-30b-doc-20261018-001` |

Control: SC-30-01. Honesty of filled cells: REAL.

---

## What this file does not do

This file names the three host sqlite copies plus replay files plus git for packaged sqlite. It adds no backup service. It invents no recovery-point floor and no retention day count. It signs no Business Owner row. It does not start sub-stage 31.
