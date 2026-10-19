# Release plan

| Field | Value |
|---|---|
| Stage | Phase 13 / 30 Release and rollback. Half B measured results. SC-30-01 / HB-30-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-30b-doc-20261018-001 |
| Status | MEASURED. SC-30-01 added three `app-a` sqlite binds. HB-30-01 before and after are REAL. Live recreate is NEEDS_HUMAN. Recovery-time stays Unknown. |
| Evidence sources | FD-19; FD-13; FD-15; FD-18; `compose.yaml`; `.github/workflows/verify.yml`; `Dockerfile.platform`; `docs/29-incident-bcdr/dr-plan.md`; `docs/27-hardening/runtime-hardening.md`; `apps/app_a/runtime/dlq.py`; `.gitignore`; `docs/00-preflight/ai-economics/provisional-token-budget.md` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. One `docker compose up` from the capstone root still starts the seven named containers. BO rows that are PROPOSED stay PROPOSED. Half B stays on this laptop Compose set. |
| Unresolved issues | Numeric recovery-time, recovery-point, availability, and dollar floors stay Unknown. Company production sign-off stays Unknown. A container registry URL stays unused. |
| Residual risks | Checking out the previous `compose.yaml` would remove the three binds. Copying an inherited 8-hour recovery note as a floor would skip FD-19. Adding a login server would add a feature. |

This file names how a person ships a change on this laptop stack. A release here is a git tree plus `docker compose up`. It is not a second cloud region.

Engineering decision ED-P13-30A-01, authority: team-force. Control `SC-30-01`. Check `HB-30-01`. After Half B, `app-a` bind-mounts three host files: `apps/app_a/runtime/dlq.sqlite3`, `apps/app_a/runtime/checkpoints.sqlite3`, and `apps/app_a/audit/audit_chain.sqlite3`. Those files then survive a container recreate. That is an engineering default. It is not a recovery-time number.

Engineering decision ED-P13-30A-02, authority: team-force. Host ports 8080 and 8090 stay ungated. This sub-stage adds no login server.

---

## Finding

**Finding.** The laptop stack starts from `compose.yaml`. CI in `.github/workflows/verify.yml` runs characterization tests, lake pytest, platform pytest, and `docker compose config`. Application A bind-mounts only `./operations/model-replay` as read-only today. The dead-letter file default path is `apps/app_a/runtime/dlq.sqlite3`. The checkpoint file is `apps/app_a/runtime/checkpoints.sqlite3`. The audit file is `apps/app_a/audit/audit_chain.sqlite3`. Those three sqlite files are omitted from the `app-a` volume list. Recreating `fabpulse-app-a` drops the in-container copies unless the person copied the host files in. `.gitignore` already leaves those sqlite files off git. Half B adds the three host bind mounts and proves one parked row still lists after a recreate. Ports 8080 and 8090 stay without identity.
**Evidence.** `compose.yaml` `app-a` `volumes`. `dlq.py` `DEFAULT_DLQ_PATH`. FD-15 checkpoint path. `apps/app_a/audit/store.py` `DEFAULT_AUDIT_PATH`. `.gitignore` lines 8 and 9. `verify.yml`. `docs/29-incident-bcdr/dr-plan.md` RS-29-03 to RS-29-05. ED-P13-27A-02 left a wrap of 8080 and 8090 for this sub-stage.
**Impact.** Half B edits `compose.yaml` only for those three binds, plus a pytest that records before and after. Half B adds no HTTP route and no login server.
**Risk.** A missing host file at compose start can make Docker create a directory on that path. Half B creates the three host files as files before `docker compose up`.
**Confidence.** High on the current volume list and the default sqlite paths. Unknown on measured recreate seconds.
**Open questions.** HALF_A_ACCEPTED. Measured recreate seconds. Whether Application B audit sqlite later gets the same bind.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric recovery-time, recovery-point, availability, retry-count, and cost floors stay Unknown. Replay is the path when the live model is off. A failed intake stays visible. This half invents no percent and no dollar benefit.

**Verified Fact.** FD-13. Docker Compose at the capstone root. Host ports 8080, 8090, 8091, 8092, 8100, 8110. `MODEL_MODE=replay`. Identity stays `FABPULSE_API_KEY` plus three headers on the four gated listeners.

**Verified Fact.** FD-15. Checkpoint file `apps/app_a/runtime/checkpoints.sqlite3`. `WRITE_TOOLS` is empty.

**Verified Fact.** Ports 8080 and 8090 stay ungated. Compose comment. CT-35. ED-P13-27A-02 named a later wrap for this sub-stage. This sub-stage leaves those ports open.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. This half invents no signer.

---

## What a release is on this product

| Step | What the person does | What it proves |
|---|---|---|
| 1. Tree | The git checkout at the capstone root holds the files to run | Which code is on disk |
| 2. Checks | `.github/workflows/verify.yml` jobs, or the same commands locally | Characterization, lake tests, platform tests, compose config |
| 3. Mode | `MODEL_MODE=replay`. Azure variables unset | No live model socket |
| 4. Host files | Three sqlite files exist as files on the host before compose start | Docker bind stays a file, not a directory |
| 5. Start | `docker compose up` from the capstone root | Seven named containers start |
| 6. Probe | `GET /health` on 8100 returns HTTP 200. Repeat 8110, 8091, 8092, 8080, 8090 as needed | That process accepted a GET |
| 7. Park list | `GET /api/recovery` with the three identity headers lists parked rows from the host dead-letter file | Failed intake stays visible |

Worked example. The person is in `c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE`. Compose default already sets `MODEL_MODE` to `replay`. After SC-30-01 the `app-a` volume list names the three host sqlite files. `GET /health` on 8100 returns `{"ok": true}`. Seconds until that 200 stay Unknown.

The version of a release is the git commit on that tree. This half names no container registry and no production tag scheme.

---

## What survives a container recreate

| Id | File | Survives `app-a` recreate today | Survives after SC-30-01 |
|---|---|---|---|
| RS-29-01 | Host `operations/model-replay/` | Yes. Already bind-mounted read-only | Yes |
| RS-29-02 | Packaged `legacy.sqlite3` | Yes. Image copy, `mode=ro` | Yes |
| RS-29-03 | `apps/app_a/runtime/dlq.sqlite3` | Host pytest file stays. In-container default drops | Yes. Host bind |
| RS-29-04 | `apps/app_a/runtime/checkpoints.sqlite3` | Same as RS-29-03 | Yes. Host bind |
| RS-29-05 | `apps/app_a/audit/audit_chain.sqlite3` | Same as RS-29-03 | Yes. Host bind |
| RS-29-06 | Process list in `compose.yaml` | Recreate with `docker compose up` | Same |
| Memory | `_LAST` recovery status and the circuit flag | Drop on process exit | Still drop |

Worked example for RS-29-03 after Half B. Host path `./apps/app_a/runtime/dlq.sqlite3` is the same file the container opens at `/opt/platform/apps/app_a/runtime/dlq.sqlite3`. Recreating `fabpulse-app-a` still opens that host file. A parked `message_id` `DLQ-30-ROLL` stays listed.

Application B audit file `apps/app_b/audit/audit_chain.sqlite3` stays a process file in this sub-stage. Recreating `app-b` drops the in-container copy unless the person copied the host file. Half B does not add that bind.

Named volume `legacy_data` already keeps `/var/lib/legacy` across recreate of `legacy` and `bridge`. **Verified Fact** of `compose.yaml`.

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery | Numeric floor |
|---|---|---|---|---|
| FM-30-01 | Recreate `app-a` with today's volume list | New process opens an empty default dead-letter file. Parked list is empty | Point the process at a host copy, or park again. After SC-30-01 the host bind keeps the file | Recovery point Unknown |
| FM-30-02 | Compose change fails health | `/health` is not 200 | Restore previous `compose.yaml` from git. `docker compose up` that tree | Restart seconds Unknown |
| FM-30-03 | `MODEL_MODE=azure` on the laptop | Public-network model call | Set `MODEL_MODE=replay`. Leave Azure unset. Restart the four platform listeners | Token line B1 stays 0 and 0 under replay |
| FM-30-07 | Identity wrap added to 8080 | CT-35 would change | Leave 8080 and 8090 ungated | None invented |

---

## Dead-letter queue and replay

Release does not delete parked rows. After SC-30-01 the host dead-letter file is the file the new process opens. `GET /api/recovery` lists those rows. Same-body replay of `DLQ-28-BAD` still stays `PARKED`. Language-model replay files already sit on the host bind `operations/model-replay/`.

If Half B ran before the bind, a recreate with today's compose would show an empty list. That empty list stays visible. Do not invent a row.

---

## Runbook — ship one laptop change

1. Confirm `MODEL_MODE=replay` in Compose. Leave Azure unset.
2. Create the three host sqlite files as files if they are missing.
3. Run the checks in `verify.yml`, or the same local pytest and `docker compose config`.
4. `docker compose up` from the capstone root, or `docker compose up -d --force-recreate app-a` when only Application A changed.
5. `GET /health` on 8100. HTTP 200 means Application A accepted the probe.
6. `GET /api/recovery` with the three identity headers. Read `parked_intakes`.
7. `GET /health` on 8080 and 8090 with no identity header. HTTP 200 means those listeners stayed ungated.
8. If health fails, follow `docs/30-release/rollback-plan.md`.

A copy of this order into `operations/` may wait until Half B. This half writes `docs/30-release/` only.

---

## SLOs and observability

| Signal | What it proves | What it does not prove |
|---|---|---|
| `/health` HTTP 200 after start | That process accepted a GET | A recovery-time floor |
| `parked_intakes` after recreate | Which dead-letter file this process opened | A recovery-point floor |
| Compose volume lines for the three sqlite files | SC-30-01 landed | An availability percent |
| CI `MODEL_MODE: replay` | The workflow stayed on replay | A dollar saving |

Recovery time stays Unknown. Recovery point stays Unknown. Availability stays Unknown. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

A Compose recreate adds no live model token. Token line B1 stays 0 prompt tokens and 0 completion tokens under replay. Lines B2 to B7 stay Unknown. This half claims no dollar benefit for a release.

Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED legacy fields. BO-11 working answer stays PROPOSED.

---

## Exact Half B check HB-30-01

Control id **SC-30-01**. Name: bind the three Application A sqlite files to the host.

Test path Half B writes: `tests/platform/test_phase13_release.py`.

Half B also creates the three host files as files before any Compose recreate that uses the new binds.

Honesty of Half B after cells: REAL. Full measured table is also in `backup-validation.md`.

### Before (today's `compose.yaml`)

Honesty of filled cells: REAL.

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| `app-a` volumes includes `./operations/model-replay` read-only | true | true | REAL |
| `app-a` volumes includes `dlq.sqlite3` | false | false | REAL |
| `app-a` volumes includes `checkpoints.sqlite3` | false | false | REAL |
| `app-a` volumes includes `audit_chain.sqlite3` | false | false | REAL |
| Ports 8080 and 8090 mapping lines | present, no identity on those services | present, no `FABPULSE_API_KEY` on `legacy` or `source-gateway` | REAL |
| `MODEL_MODE` default on `app-a` | `replay` | `replay` | REAL |

### After (SC-30-01 landed)

Honesty of filled cells: REAL.

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| `app-a` volume for host `dlq.sqlite3` | present | present | REAL |
| `app-a` volume for host `checkpoints.sqlite3` | present | present | REAL |
| `app-a` volume for host `audit_chain.sqlite3` | present | present | REAL |
| Park `{"message_id": "DLQ-30-ROLL"}` then reopen the same host file | row `status` `PARKED` still listed | `PARKED` | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` in-process | REAL |
| 8080 and 8090 stay ungated | compose still has no identity env on `legacy` and `source-gateway` | no `FABPULSE_API_KEY` on those services | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |
| Packaged `legacy.sqlite3` write | none | none. Hash unchanged | REAL |
| Azure socket | none | none | REAL |
| Live `docker compose up -d --force-recreate app-a` | optional | NEEDS_HUMAN | REAL |
| Recovery-time floor claimed | none. Cell stays Unknown | none. Cell stays Unknown | REAL |

If Docker is present, Half B may also `docker compose up -d --force-recreate app-a` and read `GET /api/recovery` on 8100. Half B did not run that recreate. The pytest file check plus a new sqlite connection to the same host path prove the bind design. The live recreate row is `NEEDS_HUMAN`.

Full measured table is in `docs/30-release/backup-validation.md`. Honesty: REAL.

---

## What this file does not do

This file names the laptop release order and the three host binds. Ports 8080 and 8090 stay ungated. It copies no inherited recovery-time note into a floor. It signs no Business Owner row. It does not start sub-stage 31.
