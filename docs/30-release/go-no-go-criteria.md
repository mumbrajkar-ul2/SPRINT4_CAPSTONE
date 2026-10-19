# Go and no-go criteria

| Field | Value |
|---|---|
| Stage | Phase 13 / 30 Release and rollback. Half B measured results. SC-30-01 / HB-30-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-30b-doc-20261018-001 |
| Status | MEASURED. HB-30-01 recorded GNG-30-01 to GNG-30-10. Live recreate is NEEDS_HUMAN. No signer invented. Numeric floors stay Unknown. |
| Evidence sources | FD-19; FD-13; FD-18; `compose.yaml`; `.github/workflows/verify.yml`; `docs/29-incident-bcdr/dr-plan.md`; `docs/28-resilience/failure-injection-results.md`; `docs/26-tevv/tevv-release-gate.md`; `docs/18-delivery/definition-of-done.md`; `Decision_Tracker.md` BO rows |
| Assumptions | `MODEL_MODE=replay`. Half B records HB-30-01. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Numeric recovery-time, recovery-point, availability, and dollar floors stay Unknown. Company production go-live sign-off stays Unknown. |
| Residual risks | Treating `/health` 200 as an availability floor would skip FD-19. Filling a Business Owner cell with a demo name would invent a signer. |

This file names when the laptop release may proceed and when it stops. Go means the listed checks passed. No-go means at least one listed stop is true.

Engineering decision ED-P13-30A-05, authority: team-force. Go ids `GNG-30-01` to `GNG-30-10`. These are engineering checks for this laptop stack. They are not a Business Owner production certificate.

---

## Finding

**Finding.** Phase 8 already named platform Done as six healthy listeners, identity on the gated ports, replay with no public-network model call, and CI without `generate --reset`. Phase 12 already named the TEVV gate as injection BLOCK plus cite-or-abstain. Sub-stage 28 already proved park and replay of `DLQ-28-BAD`. Sub-stage 29 already copied four runbooks and walked that parked row under replay. This sub-stage adds three host sqlite binds and a recreate that still lists a parked row. Numeric floors stay Unknown. BO rows stay PROPOSED. A go here is the engineering list below. It is not a signed company launch.
**Evidence.** `definition-of-done.md` Phase 8 platform table. `tevv-release-gate.md`. HB-28-01. HB-29-01. FD-19. `Decision_Tracker.md` BO status PROPOSED.
**Impact.** Half B records GNG cells as REAL for the checks it runs. Empty numeric floor cells stay Unknown.
**Risk.** Copying an inherited 99.5 percent availability note into a go cell would skip FD-19.
**Confidence.** High on the current test commands. Unknown on a company signer.
**Open questions.** HALF_A_ACCEPTED. Human Docker recreate if the sandbox blocks it.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric latency, availability, recovery-time, recovery-point, retry-count, and cost floors stay Unknown. Do not invent a percent or a dollar benefit.

**Verified Fact.** FD-13. `MODEL_MODE=replay`. Ports 8080 and 8090 stay ungated.

**Verified Fact.** FD-18. Injection returns BLOCK and drives no action. Every scored AI answer cites a lake item or abstains. Numeric percent floors stay Unknown.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. This half invents no signer.

---

## Go list

Every row must be true before the person treats HB-30-01 as a pass. Honesty of Half B measured cells: REAL when the test runs.

| Id | Check | Pass when | Label |
|---|---|---|---|
| GNG-30-01 | Replay | `MODEL_MODE=replay`. Azure variables unset | REAL. `replay`. Azure not called |
| GNG-30-02 | Health | `GET /health` on 8100 returns HTTP 200 `{"ok": true}` | REAL in-process. HTTP 200 `{"ok": true}`. Live 8100 after recreate stays NEEDS_HUMAN |
| GNG-30-03 | Parked intake | Host dead-letter file still lists `DLQ-30-ROLL` as `PARKED` after the new process opens it | REAL. Reopen of the same host file listed `PARKED` |
| GNG-30-04 | Binds | `compose.yaml` `app-a` volumes name the three host sqlite files | REAL. Three binds present |
| GNG-30-05 | Ungated ports | 8080 and 8090 still have no identity env. Mapping lines still present | REAL. No `FABPULSE_API_KEY` on `legacy` or `source-gateway` |
| GNG-30-06 | Packaged sqlite | Packaged `legacy.sqlite3` was not opened for write | REAL. Hash unchanged |
| GNG-30-07 | CI shape | `verify.yml` still has `MODEL_MODE: replay`, omits `generate --reset`, omits a live model call | REAL. Rechecked in HB-30-01 |
| GNG-30-08 | Platform tests | `python -m pytest tests/platform -q` passes on the Half B tree | REAL. HB-30-01 file 9 passed. Full suite 1 failed, 136 passed, 4 skipped. The fail is `test_no_app_b_feature_handlers` on Application B `apps/app_b/routes/queue.py`. This half did not edit Application B |
| GNG-30-09 | Failed intake visible | Replay of a still-invalid body leaves the row listed | REAL. Same-body replay of `DLQ-30-ROLL` stayed `PARKED` |
| GNG-30-10 | No new product route | Half B added no login server and no new Application A HTTP path | REAL. No `login` service. `/login` absent |

Worked example. Half B pytest parks `{"message_id": "DLQ-30-ROLL"}`. It closes the sqlite connection. It opens the same host file again. `status` is still `PARKED`. `GET /health` is 200. `MODEL_MODE` is `replay`. GNG-30-01, GNG-30-02, and GNG-30-03 pass for that run. Recovery-time seconds stay Unknown.

---

## No-go list

Stop the release when any row is true.

| Id | Stop when | What the person does |
|---|---|---|
| NG-30-01 | `MODEL_MODE` is `azure` on the laptop | Set `replay`. Unset Azure. Restart |
| NG-30-02 | `/health` on 8100 is not 200 after recreate | Follow `rollback-plan.md` |
| NG-30-03 | Parked list is empty because the bind was omitted and the in-container file dropped | Restore the host copy. Add the binds. Do not invent a row |
| NG-30-04 | Identity was added to 8080 or 8090 | Remove that wrap. Leave those ports ungated |
| NG-30-05 | Packaged `legacy.sqlite3` was written | Stop. Restore the packaged file from git. Confirm the hash |
| NG-30-06 | A parked row was deleted to make the list look clean | Stop. FD-19 requires the failure to stay visible |
| NG-30-07 | A go cell was filled with 8 hours, 24 hours, or 99.5 percent as a floor | Clear that cell. Leave it Unknown |
| NG-30-08 | A Business Owner row was marked signed by a demo actor | Leave the row PROPOSED |

Worked example for NG-30-07. The inherited file `docs/operations-service-levels.md` still records older planning notes of 8 hours, 24 hours, and 99.5 percent. Those notes stay historical. A go cell that copies them as this product's floor is a no-go.

---

## Failure modes and recovery

| Id | Failure | Linked stop | Recovery |
|---|---|---|---|
| FM-30-01 | Recreate dropped in-container sqlite | NG-30-03 | Host copy plus SC-30-01 binds |
| FM-30-02 | Health fail after compose change | NG-30-02 | Git restore of `compose.yaml`. Recreate |
| FM-30-03 | Azure mode on laptop | NG-30-01 | Set replay |
| FM-30-07 | Identity on 8080 | NG-30-04 | Remove the wrap |

Numeric floors stay Unknown.

---

## Dead-letter queue and replay

GNG-30-03 and GNG-30-09 are the park checks. A go requires the parked row to stay listed. A no-go is a deleted row or a hidden empty list.

---

## Runbook — read go or no-go

1. Run the Half B pytest file `tests/platform/test_phase13_release.py`.
2. Read GNG-30-01 to GNG-30-10. Every pass cell must match the table.
3. If any NG row is true, stop. Use `rollback-plan.md`.
4. Leave BO rows PROPOSED.
5. Leave recovery-time and recovery-point cells Unknown.

---

## SLOs and observability

Go cells that are HTTP 200, `PARKED`, and `MODEL_MODE=replay` prove those events. They do not prove availability percent, API p95, or a recovery-time floor. **Verified Fact.** FD-19.

Sub-stage 31 writes SLO files. This file does not fill those files.

---

## Cost and the 0C envelope

A go under replay adds no live model token. Token line B1 stays 0 and 0. Lines B2 to B7 stay Unknown. A dollar benefit in a go cell is a no-go. **Verified Fact.** FD-19. BO-11 working answer stays PROPOSED.

---

## Exact Half B check

HB-30-01 recorded GNG-30-01 to GNG-30-10 for the checks it ran. Live `docker compose up -d --force-recreate app-a` is `NEEDS_HUMAN`. File checks on `compose.yaml` ran. In-process health ran. Host-file reopen ran.

---

## What this file does not do

This file names the engineering go list. It leaves Business Owner rows PROPOSED. It invents no signer and no percent floor. It does not start sub-stage 31.
