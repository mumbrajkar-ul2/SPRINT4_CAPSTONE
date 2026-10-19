# Failure-injection results

| Field | Value |
|---|---|
| Stage | Phase 13 / 28 Reliability and resilience. Half B measured results. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-28b-doc-20261018-001 |
| Status | MEASURED. SC-28-01 parks one invalid intake in `apps/app_a/runtime/dlq.sqlite3` (tests use a temp path). `GET /api/recovery` lists it. A replay keeps the row visible. HB-28-01 before and after are REAL. |
| Evidence sources | FD-19; `resilience-architecture.md`; `timeout-retry-policy.md`; `apps/app_a/runtime/dlq.py`; `apps/app_a/rules/adapter.py`; `apps/app_a/routes/recovery.py`; `apps/app_a/agent/tools.py`; `tests/platform/test_phase13_resilience.py`; packaged `legacy.sqlite3` hash from Phase 0 |
| Assumptions | `MODEL_MODE=replay`. Half B ran HB-28-01 only. Other injection ids stay designed. BO rows that are PROPOSED stay PROPOSED. Packaged sqlite stays unread-write. |
| Unresolved issues | Numeric latency, availability, recovery-time, recovery-point, and retry-count floors stay Unknown. Dollar benefits stay Unknown. FI-28-03 to FI-28-06 stay Unknown. |
| Residual risks | Deleting a parked row after replay would hide FM-28-01. Retrying an injection BLOCK would run a write. Calling Azure on a replay miss would open a public-network socket. |

This file records the Half B before-and-after run for control SC-28-01. Test output is REAL. This half invents no percent and no dollar benefit.

Engineering decision ED-P13-28A-03 continued, authority: team-force. Injection ids `FI-28-01` to `FI-28-08`. Check id `HB-28-01` uses `FI-28-01` and `FI-28-02`.

Engineering decision ED-P13-28B-01, authority: team-force. Tests set `APP_A_DLQ_PATH` to a temp sqlite file. The running app default stays `apps/app_a/runtime/dlq.sqlite3`.

---

## Finding

**Finding.** Before SC-28-01, `intake_apply([{"message_id": "DLQ-28-BAD"}])` returned `invalid` 1 and `accepted` 0. `GET /api/recovery` had no `parked_intakes` key. Health was HTTP 200 `{"ok": true}`. JSON `event=intake_parked` was absent. After SC-28-01 the same bad payload is one parked row. `GET /api/recovery` lists `message_id` `DLQ-28-BAD` with `status` `PARKED`. Replay of that same body stays `PARKED`. A completed payload for `DLQ-28-OK` on a temp store returns `accepted` 1 and `status` `REPLAYED`. Both rows stay listed. Packaged `legacy.sqlite3` hash stayed `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879`. `WRITE_TOOLS` stayed `[]`. `MODEL_MODE` stayed `replay`. Azure was not called.
**Evidence.** Live before probe on 2026-10-18. Live after pytest `tests/platform/test_phase13_resilience.py`. Correlation id `corr-p13-28b-doc-20261018-001`. Honesty: REAL.
**Impact.** A person can open the parked body on recovery GET. A replay keeps the original failure visible.
**Risk.** The inherited `pull()` path still calls `intake_apply` directly. Application A parks through `intake_dedupe`.
**Confidence.** High on the measured park and replay rows. Unknown on availability percent.
**Open questions.** Reviewer grades HB-28-01. Percent floors stay Unknown.

---

## Locked facts this design applies

**Verified Fact.** FD-19. A failed intake stays visible. Replay is the path when the live model is off. Numeric floors stay Unknown. This half invents no percent and no dollar benefit.

**Verified Fact.** `MODEL_MODE=replay`. Azure was not called. Honesty: REAL.

**Verified Fact.** Injection still BLOCKS. The model has no write tool. This half did not retry BLOCK.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

**Verified Fact.** `UPSTREAM_RETRY_COUNT` is `1`. That integer is an engineering default for `upstream_timeout` and `upstream_rate_limit` only. It is not a retry-count floor.

---

## Injection catalogue

| Id | What Half B (or a later check) does | Expected handling | In HB-28-01 | Measured |
|---|---|---|---|---|
| FI-28-01 | Intake `{"message_id": "DLQ-28-BAD"}` on a temp store | `invalid` 1, `accepted` 0, one `PARKED` row listed on `GET /api/recovery` | Yes | REAL. `invalid` 1. `accepted` 0. Listed `PARKED` |
| FI-28-02 | Replay `DLQ-28-BAD` with the same body, then replay completed fields for `DLQ-28-OK` | Same body stays `PARKED`. Completed payload `accepted` 1, status `REPLAYED`, row still listed | Yes | REAL. Same body `PARKED`. Completed `accepted` 1, `REPLAYED`, still listed |
| FI-28-03 | `GET /api/recovery/probe?mode=timeout` then `mode=normal` | Probe 503 then probe 200. Recovery GET stays 200. Failure stays in `_LAST` until normal | No | Unknown |
| FI-28-04 | `mode=schema` | Probe 503. No extra attempt. Circuit flag stays clear | No | Unknown |
| FI-28-05 | `mode=rate_limit` | Probe 503. One extra attempt when that constant is wired | No | Unknown |
| FI-28-06 | Query whose prompt hash has no replay file | `replay_miss`. Abstain. No Azure socket | No | Unknown in this file. Phase 9 already has REAL miss behaviour |
| FI-28-07 | `POST /api/agent/run` with quotes plus `proposed_action=approve` | HTTP 409 `blocked`. No record write | No | REAL in Phase 12. Not re-run as HB-28-01 |
| FI-28-08 | Read `WRITE_TOOLS` | `[]` | Asserted after HB-28-01 | REAL. `[]` |

Worked example for FI-28-01. The test copied packaged `legacy.sqlite3` to a temp file and set `LEGACY_DB` to that copy. It pointed `APP_A_DLQ_PATH` at a temp sqlite file. It called `intake_dedupe([{"message_id": "DLQ-28-BAD"}])`. Measured `invalid` 1. Measured listed `message_id` `DLQ-28-BAD`. Measured `/health` 200. Honesty: REAL.

Worked example for FI-28-02 recovery. The first lot in the temp store is `L00000000`. The test parked `message_id` `DLQ-28-OK`, `business_key` `L00000000`, `system` `mes`, `event_type` `lot_started`, and no `occurred_at`. Replay added `occurred_at` `2025-02-02T03:00:00Z`. Measured `accepted` 1. Measured status `REPLAYED`. Measured packaged `legacy.sqlite3` hash unchanged. Honesty: REAL.

---

## Exact Half B check HB-28-01

Test path: `tests/platform/test_phase13_resilience.py`.

Headers:

| Header | Value |
|---|---|
| `X-Api-Key` | `local-demo-only` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |
| `X-Correlation-Id` | `corr-p13-28b-doc-20261018-001` |

Control: SC-28-01. Honesty of filled cells: REAL.

### HB-28-01 before (today's code, before SC-28-01)

Command shape recorded:

`python` probe with `LEGACY_DB` set to a temp copy of packaged `legacy.sqlite3`. Then `intake_dedupe([{"message_id": "DLQ-28-BAD"}])`. Then FastAPI `TestClient` `GET /api/recovery` and `GET /health`. Honesty: REAL.

Measured before

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| `intake_apply([{"message_id": "DLQ-28-BAD"}])` `invalid` | 1 | 1 | REAL |
| `accepted` | 0 | 0 | REAL |
| `GET /api/recovery` key `parked_intakes` | Absent or `[]` | Absent | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| JSON `event=intake_parked` | Absent | Absent | REAL |

Worked example. Recovery GET keys were `citations`, `correlation_id`, `error_class`, `ok`, `owner_id`, `retry_shown`, `sentence`, `status_visible`, `verdict`. There was no `parked_intakes` key. HTTP status was 200. Honesty: REAL.

Packaged hash before the probe: `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879`. Packaged hash after the probe: the same value. Honesty: REAL.

### HB-28-01 after (SC-28-01 landed)

Same identity headers. Temp `LEGACY_DB`. Temp dead-letter file. The dead-letter file holds parked intake rows.

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| Park `DLQ-28-BAD` `invalid` | 1 | 1 | REAL |
| Park `accepted` | 0 | 0 | REAL |
| `parked_intakes` length | at least 1 | 1 after the bad park, then 2 after the completed park | REAL |
| Row `message_id` | `DLQ-28-BAD` | `DLQ-28-BAD` | REAL |
| Row `status` after same-body replay | `PARKED` | `PARKED` | REAL |
| Completed `DLQ-28-OK` replay `accepted` | 1 | 1 | REAL |
| Completed row `status` | `REPLAYED` | `REPLAYED` | REAL |
| Completed row still on GET | true | true | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| JSON `event=intake_parked` | present | present | REAL |
| JSON `event=intake_replayed` | present on replay | present on replay | REAL |
| Packaged `legacy.sqlite3` write | none | none. Hash stayed `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879` | REAL |
| `WRITE_TOOLS` | `[]` | `[]` | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |
| Azure socket opened | false | false. `complete_azure` was patched to fail if called | REAL |

Worked example. After the bad park, recovery GET listed one row: `message_id` `DLQ-28-BAD`, `status` `PARKED`, `reason` `missing_required_fields`. `POST /api/recovery/dlq/replay` with that `parked_id` and no new payload returned `invalid` 1 and `status` `PARKED`. The row stayed in `parked_intakes`. Honesty: REAL.

Worked example. After the completed replay, recovery GET still listed `DLQ-28-BAD` as `PARKED` and `DLQ-28-OK` as `REPLAYED`. The temp store had one `gateway_inbox` row for `DLQ-28-OK`. Packaged `gateway_inbox` had zero rows for `DLQ-28-OK` and zero rows for `DLQ-28-BAD`. Honesty: REAL.

---

## Control cases Half B records, not extra features

| Call | Expected | Measured | Honesty |
|---|---|---|---|
| Replay of `DLQ-28-BAD` does not insert `gateway_inbox` on the temp store | `accepted` 0 | `accepted` 0. Inbox count for `DLQ-28-BAD` stayed 0 | REAL |
| Duplicate replay of already `REPLAYED` `DLQ-28-OK` | `duplicates` 1, no second inbox row | `duplicates` 1. Inbox count for `DLQ-28-OK` stayed 1 | REAL |
| `POST /api/agent/run` approve with untrusted quotes | HTTP 409 `blocked` | Unknown in this file. Phase 12 REAL on Application A. Not re-run | Unknown here |
| `GET /api/recovery` without identity | HTTP 401 `missing_identity` | HTTP 401 `missing_identity` | REAL |

`UPSTREAM_RETRY_COUNT` measured `1`. That value is an engineering default for timeout and throttle only. The retry-count floor stays Unknown. Honesty of the constant: REAL.

---

## Dead-letter queue and replay

The dead-letter store is `apps/app_a/runtime/dlq.sqlite3` in the running app. That file holds parked intake rows. Tests use a temp path through `APP_A_DLQ_PATH`. Language-model replay stays `operations/model-replay/`. This half did not mix those folders.

A parked row is not deleted after `REPLAYED`. **Verified Fact** of the run. FD-19. Honesty: REAL.

---

## Pytest the reviewer can re-run

```text
python -m pytest tests/platform/test_phase13_resilience.py -q --tb=short
```

Measured on 2026-10-18: 4 passed, 1 skipped. Honesty: REAL.

The before function is skipped after SC-28-01. The before snapshot stays in this file. The after function parks `DLQ-28-BAD`, lists it, replays the same body, parks `DLQ-28-OK`, replays completed fields, and checks that both rows stay listed.

---

## SLOs and observability

HB-28-01 is proven by HTTP status, `invalid` / `accepted` counts, parked `status`, stdout `event`, and `/health`. Those cells do not prove availability percent, API p95, or a retry-count floor. **Verified Fact.** FD-19.

Availability percent stays Unknown. API p95 stays Unknown. Retrieval p95 stays Unknown. Recovery time stays Unknown. Recovery point stays Unknown.

---

## Cost and the 0C envelope

FI-28-01 and FI-28-02 add no live model call. Token line B1 stays 0 and 0. Lines B2 to B7 stay Unknown. This file claims no dollar benefit.

---

## What this file does not do

This file does not start sub-stage 29. It does not copy a runbook into `operations/`. It does not call Azure. It does not delete a parked intake. It does not retry an injection BLOCK. It does not invent an availability percent. It does not invent a dollar benefit. It does not sign a Business Owner row.
