# Tabletop results

| Field | Value |
|---|---|
| Stage | Phase 13 / 29 Incident and BCDR. Half B measured results. SC-29-01 / HB-29-01 / TT-29-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-29b-doc-20261018-001 |
| Status | MEASURED. SC-29-01 copied four runbooks into `operations/`. TT-29-01 parked `DLQ-28-BAD` again, listed it on `GET /api/recovery`, kept `MODEL_MODE=replay`, kept health HTTP 200, and opened no Azure socket. The row stayed listed. Recovery-time and recovery-point floors stay Unknown. |
| Evidence sources | FD-19; `operations/ai-incident-playbook.md`; `operations/containment-procedures.md`; `operations/bc-plan.md`; `operations/dr-plan.md`; `rto-rpo.md`; `docs/28-resilience/failure-injection-results.md`; `apps/app_a/routes/recovery.py`; `apps/app_a/runtime/dlq.py`; `apps/app_a/agent/tools.py`; `operations/replay_lookup.py`; `compose.yaml`; `tests/platform/test_phase13_incident_bcdr.py` |
| Assumptions | `MODEL_MODE=replay`. Half B ran TT-29-01 only. BO rows that are PROPOSED stay PROPOSED. Packaged sqlite stays unread-write. Tests used a temp `LEGACY_DB` and a temp dead-letter file via `APP_A_DLQ_PATH`. |
| Unresolved issues | Numeric recovery-time and recovery-point floors stay Unknown. Dollar benefits stay Unknown. INC-2025-014 owner stays Unknown. |
| Residual risks | Adding an incident HTTP route would add a feature. Deleting a parked row during the walk would hide FM-29-04. Calling Azure would leave replay. Copying an inherited recovery-time note or recovery-point note into a measured cell would skip FD-19. |

This file names the one small Half B tabletop check. A tabletop is a walk of the written steps against the running product. Test output is REAL. This half invents no percent and no dollar benefit. Recovery time stays Unknown. Recovery point stays Unknown.

Engineering decision ED-P13-29A-01 continued, authority: team-force. Control id `SC-29-01`. Check id `HB-29-01`. Tabletop id `TT-29-01`. Name: copy four runbooks into `operations/` and walk the parked intake while the live model is off.

Engineering decision ED-P13-29A-03, authority: team-force. The tabletop classifies the walk by incident type `AI-INC-29-01` plus `AI-INC-29-04`. It does not rank those types by hour.

---

## Finding

**Finding.** Before SC-29-01, capstone-root `operations/` had `replay_lookup.py` and `model-replay/`. It had no `ai-incident-playbook.md`, `containment-procedures.md`, `bc-plan.md`, or `dr-plan.md`. After SC-29-01 those four files are present. The walk re-parked `{"message_id": "DLQ-28-BAD"}`. `invalid` was 1. `accepted` was 0. `GET /api/recovery` listed `message_id` `DLQ-28-BAD` with `status` `PARKED`. Same-body replay stayed `PARKED`. The row stayed listed. `GET /health` was HTTP 200 `{"ok": true}`. `MODEL_MODE` stayed `replay`. Azure was not called. `WRITE_TOOLS` stayed `[]`. Recovery `owner_id` stayed `None`. Packaged `legacy.sqlite3` was not written. No new Application A HTTP route was added. Recovery-time and recovery-point floors stay Unknown.
**Evidence.** Glob of `operations/` at the start of Half B on 2026-10-18, before the four copies. Pytest `tests/platform/test_phase13_incident_bcdr.py` under correlation id `corr-p13-29b-doc-20261018-001`. Honesty: REAL.
**Impact.** A person can open the four runbooks under `operations/`. The parked intake stays visible while the live model is off.
**Risk.** A new `/api/incident` route would add a feature this sub-stage forbids.
**Confidence.** High on the four file copies and on the park-and-replay walk. Unknown on a recovery-time floor and a recovery-point floor.
**Open questions.** Reviewer grades HB-29-01. Numeric recovery-time and recovery-point floors. INC-2025-014 owner.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. A failed intake stays visible. The parked intake from sub-stage 28 stays listed. Numeric recovery-time and recovery-point floors stay Unknown. This half invents no percent and no dollar benefit.

**Verified Fact.** `MODEL_MODE=replay`. This half did not call Azure. Honesty: REAL.

**Verified Fact.** Injection still BLOCKS. The model has no write tool. This tabletop did not retry BLOCK.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. Company job titles stay Unknown. INC-2025-014 owner stays Unknown.

---

## Tabletop TT-29-01

Name: parked intake stays listed while the live model is off.

Incident types walked: AI-INC-29-01 (live Azure off) and AI-INC-29-04 (invalid intake parked).

Control: SC-29-01. Honesty of filled cells: REAL.

Headers for recovery GET:

| Header | Value |
|---|---|
| `X-Api-Key` | `local-demo-only` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |
| `X-Correlation-Id` | `corr-p13-29b-doc-20261018-001` |

The walk re-parked `{"message_id": "DLQ-28-BAD"}` through the existing SC-28-01 path so the list does not depend on leftover process memory. Temp `LEGACY_DB`. Temp dead-letter file via `APP_A_DLQ_PATH`. Packaged `legacy.sqlite3` stayed unread-write.

Half B test path: `tests/platform/test_phase13_incident_bcdr.py`.

---

## HB-29-01 before (today, before SC-29-01 copies runbooks)

Honesty of filled cells: REAL.

Command shape recorded: glob of capstone `operations/` on 2026-10-18 before the four files were written. Health, `MODEL_MODE`, and Azure were then measured in the same Half B TestClient walk. Copying markdown does not change those three cells.

Measured before

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| `operations/ai-incident-playbook.md` | absent | absent | REAL |
| `operations/containment-procedures.md` | absent | absent | REAL |
| `operations/bc-plan.md` | absent | absent | REAL |
| `operations/dr-plan.md` | absent | absent | REAL |
| `GET /health` on Application A | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |
| Azure socket opened | false | false. `complete_azure` was patched to fail if called | REAL |
| Numeric RTO floor written in those four `operations/` files | files absent, so no floor copied | files absent | REAL |

Worked example of the measured before. A glob of the capstone `operations/` folder returned `replay_lookup.py` and `model-replay/`. It did not return the four incident runbook names. Honesty: REAL.

---

## HB-29-01 after (SC-29-01 landed)

Same identity headers. Temp `LEGACY_DB`. Temp dead-letter file. `MODEL_MODE=replay`.

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| `operations/ai-incident-playbook.md` | present | present | REAL |
| `operations/containment-procedures.md` | present | present | REAL |
| `operations/bc-plan.md` | present | present | REAL |
| `operations/dr-plan.md` | present | present | REAL |
| Those four files copy 8 hours as a recovery-time floor | false | false. The four files do not write that phrase | REAL |
| Those four files copy 24 hours as a recovery-point floor | false | false. The four files do not write that phrase | REAL |
| Park `{"message_id": "DLQ-28-BAD"}` `invalid` | 1 | 1 | REAL |
| `accepted` | 0 | 0 | REAL |
| `GET /api/recovery` lists `DLQ-28-BAD` | true | true | REAL |
| That row `status` | `PARKED` | `PARKED` | REAL |
| Replay same body, row still listed | true | true | REAL |
| Same-body `status` after replay | `PARKED` | `PARKED` | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |
| Azure socket opened | false | false. `complete_azure` was patched to fail if called | REAL |
| `WRITE_TOOLS` | `[]` | `[]` | REAL |
| Recovery `owner_id` | `None` | `None` | REAL |
| Packaged `legacy.sqlite3` write | none | none. Hash stayed `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879` | REAL |
| New Application A HTTP route added | none | none. `/api/incident` is absent. `/api/recovery` stayed | REAL |
| Recovery-time floor claimed | none. Cell stays Unknown | none. Cell stays Unknown | REAL |
| Recovery-point floor claimed | none. Cell stays Unknown | none. Cell stays Unknown | REAL |

Worked example of the measured after. Half B wrote the four `operations/` files from `docs/29-incident-bcdr/`. The test parked `DLQ-28-BAD`. Recovery GET listed `message_id` `DLQ-28-BAD` and `status` `PARKED`. Replay of that same body kept the row listed as `PARKED`. Health stayed 200. `complete_azure` was patched to fail if called. `owner_id` stayed `None`. The four `operations/` files say recovery time stays Unknown and recovery point stays Unknown. They do not write 8 hours or 24 hours as floors.

Honesty of those cells: REAL.

---

## What Half B must not add

| Change | Allowed in HB-29-01 | Measured |
|---|---|---|
| New `/api/incident` route | No | Absent. REAL |
| New sqlite table | No | None added. REAL |
| New product screen | No | None added. REAL |
| Identity on port 8080 | No | Not added. REAL |
| `MODEL_MODE=azure` | No | Stayed `replay`. REAL |
| Delete parked row | No | `DLQ-28-BAD` stayed listed. REAL |
| Retry injection BLOCK | No | Not retried. REAL |
| Fill INC-2025-014 owner with `demo-rt06-1` | No | `owner_id` stayed `None`. REAL |
| Copy inherited 8-hour or 24-hour notes as floors | No | Four operations files omit those phrases. REAL |
| Invent a percent or a dollar benefit | No | None invented. REAL |

Copying the four runbooks into `operations/` is the small change. Walking the existing park and replay path is the evidence. That pair is SC-29-01.

---

## Dead-letter queue and replay

The walk used the same dead-letter helper as SC-28-01. Language-model replay stays `operations/model-replay/`. The tabletop did not mix those folders.

A parked row is not deleted after the same-body replay. **Verified Fact** of the walk. FD-19. Honesty: REAL.

---

## Pytest the reviewer can re-run after Half B

```text
python -m pytest tests/platform/test_phase13_incident_bcdr.py -q --tb=short
```

Measured on 2026-10-18: 5 passed in 6.11s. Honesty: REAL.

```text
python -m pytest tests/platform/test_phase13_incident_bcdr.py -v --tb=short
```

```text
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE
plugins: anyio-4.14.1, devtools-0.12.2, langsmith-0.4.43
collecting ... collected 5 items

tests/platform/test_phase13_incident_bcdr.py::test_hb29_01_before_snapshot_is_recorded PASSED [ 20%]
tests/platform/test_phase13_incident_bcdr.py::test_hb29_01_runbooks_present_without_numeric_floors PASSED [ 40%]
tests/platform/test_phase13_incident_bcdr.py::test_hb29_01_no_new_incident_route PASSED [ 60%]
tests/platform/test_phase13_incident_bcdr.py::test_hb29_01_tabletop_parked_intake_stays_listed PASSED [ 80%]
tests/platform/test_phase13_incident_bcdr.py::test_hb29_01_after_snapshot_is_recorded PASSED [100%]

============================== 5 passed in 6.11s ==============================
```


---

## SLOs and observability

HB-29-01 is proven by file presence under `operations/`, HTTP status, parked `status`, `MODEL_MODE`, stdout showing no Azure call, and `/health`. Those cells do not prove availability percent, API p95, a recovery-time floor, or a recovery-point floor. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

TT-29-01 adds no live model call. Token line B1 stays 0 and 0. Lines B2 to B7 stay Unknown. This file claims no dollar benefit.

---

## What this file does not do

This file does not start sub-stage 30. It does not call Azure. It does not invent an availability percent. It does not invent a recovery-time floor. It does not invent a recovery-point floor. It does not invent a dollar benefit. It does not sign a Business Owner row. It does not invent a company title. It does not fill INC-2025-014 `owner_id`.
