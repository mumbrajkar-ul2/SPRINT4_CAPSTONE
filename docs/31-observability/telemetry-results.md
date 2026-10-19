# Telemetry results

| Field | Value |
|---|---|
| Stage | Phase 13 / 31 Observability and service levels. Half B measured results. SC-31-01 / HB-31-01. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-31b-doc-20261018-001 |
| Status | MEASURED. SC-31-01 writes one JSON stdout line `event=replay_miss` from Application A `POST /api/query` when `generate()` returns `error_class` `replay_miss`. HB-31-01 before and after are REAL. A cited answer stays unlabeled as `replay_miss`. Numeric floors stay Unknown. |
| Evidence sources | FD-19; FD-13; FD-11; `observability-architecture.md`; `ai-telemetry-spec.md`; `apps/app_a/routes/query.py`; `apps/shared/jsonlog.py`; `apps/app_a/intelligence/generate.py`; `tests/platform/test_phase13_observability.py` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. Half B ran HB-31-01 only. Application B query stays as built. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | API p95, retrieval p95, agent completion, availability percent, recovery time, recovery point, error-budget count, and token cost stay Unknown. Company signer stays Unknown. INC-2025-014 owner stays Unknown. Application B miss line stays unbuilt. |
| Residual risks | Treating one `duration_ms` as API p95 would invent SLO-N1. Setting `MODEL_MODE=azure` to fill a token line would open a public-network socket. Adding a metrics product would add a collector this stack does not run. |

This file records the Half B before-and-after run for control SC-31-01. Test output is REAL. This half invents no percent and no latency floor.

Engineering decision ED-P13-31A-01 continued, authority: team-force. Control id `SC-31-01`. Check id `HB-31-01`.

Engineering decision ED-P13-31B-01, authority: team-force. `apps/app_a/routes/query.py` calls `emit` only when `result.get("error_class") == "replay_miss"`. A cited answer with `error_class` null writes no `replay_miss` line.

---

## Finding

**Finding.** Before SC-31-01, `POST /api/query` with question `What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file` and header `X-Correlation-Id: corr-p13-31b-doc-20261018-001` returned HTTP 200, `verdict` `ABSTAIN`, `error_class` `replay_miss`. Retrieve found `arch.listener.lake_rest_8091`. Stdout had `event=request_ok` for that id. No line had `event=replay_miss`. After SC-31-01 the same POST still returns HTTP 200 and `error_class` `replay_miss`. Stdout now has one line with `service=app-a`, `event=replay_miss`, `model_mode=replay`, and `correlation_id` `corr-p13-31b-doc-20261018-001`. The cited GQ-23 answer `Which port does the Context Lake REST listener use?` returned HTTP 200, `verdict` `ANSWER`, `error_class` null, citation `arch.listener.lake_rest_8091`. That POST wrote no `replay_miss` line. `GET /health` stayed HTTP 200 `{"ok": true}`. `MODEL_MODE` stayed `replay`. Azure was not called. Socket create stayed forbidden during the POST. Numeric floors stay Unknown.
**Evidence.** Live before probe on 2026-10-18 before the emit landed. Live after pytest `tests/platform/test_phase13_observability.py`. Correlation id `corr-p13-31b-doc-20261018-001`. Honesty: REAL.
**Impact.** A person can grep stdout for `event=replay_miss` without calling Azure.
**Risk.** A later author who copies one `duration_ms` into SLO-N1 would invent a floor.
**Confidence.** High on the measured miss line and the cited-answer negative case. Unknown on availability percent.
**Open questions.** Reviewer grades HB-31-01. Whether Application B query later emits the same miss line. Who may later set SLO-N4.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric latency, availability, error-budget, and recovery floors stay Unknown. This half invents no percent and no dollar benefit.

**Verified Fact.** FD-13. JSON logs are one object per line on stdout with `service`, `event`, and `correlation_id`. Compose default `MODEL_MODE=replay`.

**Verified Fact.** FD-11. Numeric API p95, retrieval p95, citation percent, and availability percent stay Unknown.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

---

## Exact Half B check HB-31-01

Test path: `tests/platform/test_phase13_observability.py`.

Headers:

| Header | Value |
|---|---|
| `X-Api-Key` | `local-demo-only` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |
| `X-Correlation-Id` | `corr-p13-31b-doc-20261018-001` on the miss POST. `corr-p13-31b-cite-001` on the cited POST |

Control: SC-31-01. Honesty of filled cells: REAL.

---

## HB-31-01 before

Honesty of filled cells: REAL.

Command shape recorded: in-process `TestClient` `POST /api/query` on 2026-10-18, before `query.py` called `emit` for `replay_miss`. Question `What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file`. Header `X-Correlation-Id: corr-p13-31b-doc-20261018-001`. `MODEL_MODE=replay`.

Measured before

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| HTTP status | 200 | 200 | REAL |
| `verdict` | `ABSTAIN` | `ABSTAIN` | REAL |
| `error_class` on the HTTP body | `replay_miss` | `replay_miss` | REAL |
| Retrieve item | `arch.listener.lake_rest_8091` present | present in `retrieved_item_ids` | REAL |
| Sentence | empty | empty | REAL |
| Stdout `event=request_ok` for that id | present | present. `service=app-a`, `path=/api/query`, `status=200` | REAL |
| Stdout `event=replay_miss` | absent | absent. no line has `event=replay_miss` | REAL |
| `model_mode` on stdout | absent | absent on the `request_ok` line | REAL |
| Cited GQ-23 `verdict` | `ANSWER` | `ANSWER` | REAL |
| Cited GQ-23 `error_class` | null | null | REAL |
| Cited GQ-23 citations | `arch.listener.lake_rest_8091` | `arch.listener.lake_rest_8091` | REAL |
| Cited GQ-23 stdout `replay_miss` | absent | absent | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |

Worked example of the measured before. Stdout lines were `health_ok`, then `request_ok` for the miss id, then `request_ok` for the cited id. Those three lines omit `replay_miss`.

---

## HB-31-01 after

Same miss POST. Same identity headers. `MODEL_MODE=replay`. In-process `TestClient`. Socket create patched to fail. `complete_azure` patched to fail.

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| HTTP status | 200 | 200 | REAL |
| `verdict` | `ABSTAIN` | `ABSTAIN` | REAL |
| `error_class` on the HTTP body | `replay_miss` | `replay_miss` | REAL |
| HTTP body `model_mode` key | absent. Body stays as built | absent | REAL |
| Stdout `event=replay_miss` count | 1 | 1 | REAL |
| That line `service` | `app-a` | `app-a` | REAL |
| That line `event` | `replay_miss` | `replay_miss` | REAL |
| That line `model_mode` | `replay` | `replay` | REAL |
| That line `correlation_id` | `corr-p13-31b-doc-20261018-001` | `corr-p13-31b-doc-20261018-001` | REAL |
| That line `error_class` | `replay_miss` | `replay_miss` | REAL |
| That line `path` | `/api/query` | `/api/query` | REAL |
| That line `status` | 200 | 200 | REAL |
| That line `prompt_hash` | present | `be25183a6c82ce22c9e2331b682f5658357f02d5b641450322fe4d8a7f982cec` | REAL |
| Stdout `event=request_ok` | still present | present | REAL |
| Cited GQ-23 `verdict` | `ANSWER` | `ANSWER` | REAL |
| Cited GQ-23 `error_class` | not `replay_miss` | null | REAL |
| Cited GQ-23 citations | `arch.listener.lake_rest_8091` | `arch.listener.lake_rest_8091` | REAL |
| Cited GQ-23 sentence | present. PRECOMPUTED | `The Context Lake REST listener uses port 8091.` PRECOMPUTED | REAL for the HTTP fields. PRECOMPUTED for the sentence text |
| Cited GQ-23 stdout `replay_miss` | none | none | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |
| Azure socket | none | none. `complete_azure` and `socket.create_connection` were patched to fail. `socket.socket` was forbidden only inside `generate()` so TestClient could open its event loop | REAL |
| `WRITE_TOOLS` | `[]` | `[]` | REAL |
| Metrics product added | none | none | REAL |
| API p95 claimed | none. SLO-N1 stays Unknown | none. SLO-N1 stays Unknown | REAL |
| Availability percent claimed | none. SLO-N4 stays Unknown | none. SLO-N4 stays Unknown | REAL |
| Error-budget count claimed | none. SLO-N7 stays Unknown | none. SLO-N7 stays Unknown | REAL |

Worked example of the measured after. The miss POST wrote one JSON line `{"service":"app-a","event":"replay_miss","correlation_id":"corr-p13-31b-doc-20261018-001","model_mode":"replay"}`. Middleware still wrote `request_ok`. The cited GQ-23 POST wrote `request_ok` only.

Honesty of those cells: REAL. Numeric floors stay Unknown.

---

## SLOs this line supports

| Id | What the measured line supports | What it does not prove |
|---|---|---|
| SLO-B4 | The miss stayed an abstain. The cited answer kept its lake item id | A citation percent |
| SLO-B9 | Identity headers were present. The miss POST ran | An error-budget percent |
| LOG-31-09 | The miss is grep-able on stdout | Retrieval p95 |
| SLO-N1 to SLO-N8 | No supporting numeric series exists | Any floor |

---

## Cost and the 0C envelope

SC-31-01 adds no live model call. Token line B1 stays 0 prompt tokens and 0 completion tokens when `MODEL_MODE=replay`. Lines B2 to B7 stay Unknown. This half claims no dollar benefit. **Verified Fact.** FD-19.

---

## Commands

```text
python -m pytest tests/platform/test_phase13_observability.py -q --tb=short
```

```text
python -m pytest tests/platform/test_phase13_observability.py -v --tb=short
```

---

## What this file does not do

This file does not start sub-stage 32. It does not add Prometheus, Grafana, or a cloud exporter. It does not call Azure. It does not invent a percent or a latency floor. It does not update a tracker.
