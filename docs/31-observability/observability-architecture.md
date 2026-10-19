# Observability architecture

| Field | Value |
|---|---|
| Stage | Phase 13 / 31 Observability and service levels. Half B evidence. SC-31-01 / HB-31-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-31b-doc-20261018-001 |
| Status | MEASURED. SC-31-01 emits `event=replay_miss` from Application A `POST /api/query`. HB-31-01 before and after are REAL. Numeric floors stay Unknown. |
| Evidence sources | FD-19; FD-11; FD-13; FD-23; `apps/shared/jsonlog.py`; `apps/app_a/server.py`; `apps/app_a/routes/query.py`; `apps/app_b/server.py`; `context-lake/rest_server.py`; `context-lake/mcp_server.py`; `apps/app_a/runtime/dlq.py`; `apps/app_a/audit/store.py`; `tests/platform/test_logs.py`; `tests/platform/test_phase13_observability.py`; `telemetry-results.md`; `docs/12-specs/system-spec.md`; `docs/17-implementation-prd/finalized-nfrs.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `compose.yaml` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. One `docker compose up` still starts the seven named containers. Host ports stay 8080, 8090, 8091, 8092, 8100, 8110. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Numeric latency, availability, error-budget, and recovery floors stay Unknown. Company job titles stay Unknown. INC-2025-014 owner stays Unknown. Application B miss line stays unbuilt. |
| Residual risks | Adding a metrics product would add a collector this stack does not run. Copying an inherited availability note as a floor would skip FD-19. Writing the API key onto stdout would leak the shared secret. Treating one `duration_ms` as API p95 would invent a target. |

This file names how a person sees what the laptop stack did. Observability here is JSON lines on stdout plus the audit table. The one Half B check is HB-31-01. That check writes one `replay_miss` line and records before and after. Measured cells live in `telemetry-results.md`. This half adds no product screen. This half adds no metrics product. This half adds no cloud exporter.

Engineering decision ED-P13-31A-01, authority: team-force. Control id `SC-31-01`. Check id `HB-31-01`. Half B emits one JSON line `event=replay_miss` from Application A `POST /api/query` when `generate()` returns `error_class` `replay_miss`. The process stays on `MODEL_MODE=replay`. Azure stays uncalled.

Engineering decision ED-P13-31A-02, authority: team-force. Two stores hold facts. Store 1 is stdout JSON from `apps/shared/jsonlog.py`. Store 2 is table `audit_chain` in `apps/app_a/audit/audit_chain.sqlite3`. The request log records the HTTP call. The audit row records the graph step or the human approval.

Engineering decision ED-P13-31A-05, authority: team-force. Failure ids `FM-31-01` to `FM-31-08`. Stdout event ids `LOG-31-01` to `LOG-31-12`.

Engineering decision ED-P13-31A-07, authority: team-force. The person reads container stdout with `docker compose logs` or a pytest capture. Half B adds no extra container.

---

## Finding

**Finding.** Application A, Application B, lake REST, and lake MCP already write one JSON object per request to stdout. Required fields are `service`, `event`, and `correlation_id`. `jsonlog.emit` also writes `timestamp`, `level`, `actor_id`, `path`, `status`, and `duration_ms`. Named events already on disk are `health_ok`, `request_ok`, `identity_missing`, `server_key_missing`, `forbidden_role`, `lake_write_rejected`, `intake_parked`, and `intake_replayed`. `test_at_log_json_identity_missing` already proves `service=app-a` and `event=identity_missing` with the API key absent. `replay_lookup.lookup` already returns `event=replay_miss` in a Python dict. `generate()` returns `error_class=replay_miss` and does not call `emit`. `POST /api/query` therefore has a request line and no `replay_miss` line. Ports 8080 and 8090 write their own server text. They do not call `jsonlog.emit`. Numeric floors stay Unknown.
**Evidence.** `apps/shared/jsonlog.py` `emit`. Middleware in `apps/app_a/server.py` and `apps/app_b/server.py`. `identity_reject` event names. `dlq.py` park and replay emits. `tests/platform/test_logs.py`. `operations/replay_lookup.py` miss dict. `apps/app_a/intelligence/generate.py` return without `emit`. `apps/app_a/routes/query.py`. FD-19. FD-11.
**Impact.** Half B adds one `emit` on the Application A query path and one pytest that records before and after. Half B adds no HTTP route and no metrics product.
**Risk.** Emitting a field named `token` would drop that field. `jsonlog.FORBIDDEN_KEYS` includes `token`. A later token count must use `prompt_tokens` and `completion_tokens`.
**Confidence.** High on the current emit list and the measured `replay_miss` line. Unknown on availability percent.
**Open questions.** Reviewer grades HB-31-01. Whether Application B query later emits the same miss line.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. A failed intake stays visible. Numeric latency, availability, error-budget, recovery-time, recovery-point, retry-count, and cost floors stay Unknown. This half invents no percent and no dollar benefit.

**Verified Fact.** FD-11. HTTP, MCP, event records, and error families are specified in `docs/12-specs/`. Numeric latency, availability percent, recovery time, recovery point, API p95, retrieval p95, groundedness percent, citation percent, and abstention percent stay Unknown.

**Verified Fact.** FD-13. JSON logs are one object per line on stdout with `service`, `event`, and `correlation_id`. Compose default `MODEL_MODE=replay`. Host ports stay 8080, 8090, 8091, 8092, 8100, 8110.

**Verified Fact.** FD-23. Table `audit_chain` holds one row per agent step and one row per human approval. `GET /api/audit/{correlation_id}` returns that list in `seq` order.

**Verified Fact** of BO-01 through BO-13 that are PROPOSED. Those rows stay PROPOSED. This half invents no signer name.

---

## What is already running

**Verified Fact.**

| Piece | What it does today | Label |
|---|---|---|
| `apps/shared/jsonlog.py` | Writes one JSON object per line to stdout. Drops forbidden secret field names | Verified Fact |
| Application A middleware | Emits `identity_missing`, `server_key_missing`, `forbidden_role`, `health_ok`, `request_ok` | Verified Fact of `server.py` |
| Application B middleware | Same event names with `service=app-b` | Verified Fact |
| Lake REST middleware | Same identity and request events with `service=lake-rest`, plus `lake_write_rejected` on write methods | Verified Fact |
| Lake MCP middleware | Same pattern with `service=lake-mcp` | Verified Fact |
| Dead-letter helper | Emits `intake_parked` and `intake_replayed` | Verified Fact of `dlq.py` |
| `GET /health` on 8100 | HTTP 200 `{"ok": true}` and a `health_ok` line | Verified Fact |
| `GET /api/audit/{correlation_id}` | Returns `audit_chain` rows in `seq` order. Identity required | Verified Fact |
| `GET /api/recovery` | Lists `parked_intakes`. Identity required | Verified Fact of HB-28-01 |
| Replay lookup | Returns a Python dict with `event=replay_miss` or `event=replay_hit`. Writes no stdout line | Verified Fact of `replay_lookup.py` |
| Port 8080 and port 8090 | Listen without `jsonlog.emit` | Verified Fact of those servers |

Worked example. `GET /api/identity-check` on 8100 with no headers writes one stdout line. `service` is `app-a`. `event` is `identity_missing`. `status` is 401. The line has no `api_key` field. Honesty: REAL in `test_logs.py`.

Worked example. `generate("zz-no-replay-hash-question-about-port-8091-unique")` returns `verdict` `ABSTAIN`. When retrieve found an item, `error_class` is `replay_miss`. Stdout from `generate()` has no `emit` call. Honesty: REAL in `test_app_a_grounding.py` for the return body. The missing stdout line is a Verified Fact of `generate.py` and `query.py`.

---

## Two stores

| Store | Path or stream | What it holds | How a person reads it |
|---|---|---|---|
| Request and control logs | Process stdout | One JSON object per emit. Join key `correlation_id` | `docker compose logs app-a` or pytest `capsys` |
| Audit chain | `apps/app_a/audit/audit_chain.sqlite3` | One row per agent step and per human approval | `GET /api/audit/{correlation_id}` |

Worked example. Header `X-Correlation-Id: corr-p13-31a-doc-20261018-001` on `POST /api/query` puts that string on the `request_ok` line. The same header on an agent run is `thread_id` in `audit_chain`. The person greps stdout for that string, then GETs the audit route with the same string.

A request log proves the HTTP call ran. An audit row proves a graph step or a human approval ran. SLO-B10 already said request logs are not that audit row. **Verified Fact.** `finalized-nfrs.md` SLO-B10.

---

## Who writes JSON lines

| `service` value | Process | Host port | Uses `jsonlog.emit` |
|---|---|---|---|
| `app-a` | `fabpulse-app-a` | 8100 | Yes |
| `app-b` | `fabpulse-app-b` | 8110 | Yes |
| `lake-rest` | `fabpulse-lake-rest` | 8091 | Yes |
| `lake-mcp` | `fabpulse-lake-mcp` | 8092 | Yes |
| (none from this helper) | `fabpulse-legacy` | 8080 | No |
| (none from this helper) | `fabpulse-source-gateway` | 8090 | No |
| (none from this helper) | `fabpulse-bridge` | none published | No |

Worked example. Compose health for `app-a` calls `http://127.0.0.1:8100/health`. The process writes `event=health_ok`. Compose marks the container healthy after that HTTP 200. Seconds to healthy stay Unknown. **Verified Fact.** FD-19.

---

## Stdout event catalogue

Engineering decision ED-P13-31A-05 continued, authority: team-force.

| Id | `event` | When it is written today | After Half B |
|---|---|---|---|
| LOG-31-01 | `health_ok` | `GET /health` on a gated listener | Unchanged |
| LOG-31-02 | `request_ok` | Any other completed request on a gated listener | Unchanged |
| LOG-31-03 | `identity_missing` | Missing or wrong caller headers. HTTP 401 | Unchanged |
| LOG-31-04 | `server_key_missing` | Process has no `FABPULSE_API_KEY`. HTTP 503 | Unchanged |
| LOG-31-05 | `forbidden_role` | Role outside RT-01 to RT-06, or role mismatch. HTTP 403 | Unchanged |
| LOG-31-06 | `lake_write_rejected` | Write method on 8091 or 8092. HTTP 405 | Unchanged |
| LOG-31-07 | `intake_parked` | Invalid intake written to the dead-letter file | Unchanged |
| LOG-31-08 | `intake_replayed` | Dead-letter replay ran | Unchanged |
| LOG-31-09 | `replay_miss` | Python dict only in `replay_lookup` | Also one stdout line from Application A query |
| LOG-31-10 | `replay_hit` | Python dict only in `replay_lookup` | Stays a dict in this sub-stage |
| LOG-31-11 | `replay_required` | `generate()` when `MODEL_MODE` is not `replay` or `azure` | Stays in the HTTP body in this sub-stage |
| LOG-31-12 | (reserved) | No Azure live line in this half | Half B does not call Azure |

Worked example for LOG-31-09 after Half B. `POST /api/query` with question `What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file` and header `X-Correlation-Id: corr-p13-31b-doc-20261018-001`. Retrieve finds that lake item id. Replay has no file for that prompt hash. HTTP 200. `verdict` is `ABSTAIN`. `error_class` is `replay_miss`. Stdout includes `{"service":"app-a","event":"replay_miss","correlation_id":"corr-p13-31b-doc-20261018-001","model_mode":"replay"}`. Honesty: REAL in `telemetry-results.md`.

---

## Required fields on every emit

**Verified Fact** of `jsonlog.emit`.

| Field | What it holds |
|---|---|
| `timestamp` | UTC time the line was written |
| `service` | `app-a`, `app-b`, `lake-rest`, or `lake-mcp` |
| `level` | `info` or `warn` |
| `event` | One name from the catalogue |
| `correlation_id` | Header `X-Correlation-Id`, or null when the header is empty |
| `actor_id` | Header `X-Actor-Id` on a gated path. Null on `/health` |
| `path` | Request path |
| `status` | HTTP status when the emit is from middleware |
| `duration_ms` | Milliseconds for that one request |

`duration_ms` is a measured field on that line when the line is captured. It is not API p95. **Verified Fact.** FD-19. FD-11.

Forbidden field names stay out: `api_key`, `x-api-key`, `x_api_key`, `fabpulse_api_key`, `authorization`, `password`, `secret`, `token`. **Verified Fact.** `FORBIDDEN_KEYS`.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-31-01 | A gated listener writes no JSON line | Compose still has HTTP. Grep finds no `{` line | Restart that named container. Confirm `health_ok` |
| FM-31-02 | Replay miss has no stdout line | HTTP body has `error_class=replay_miss`. Stdout has `request_ok` only | SC-31-01 adds the `replay_miss` line |
| FM-31-03 | A secret field name reaches `emit` | `jsonlog` drops that field | Keep using `FORBIDDEN_KEYS`. Rotate the key using the 27 secrets runbook |
| FM-31-04 | Person treats one `duration_ms` as a floor | One number on one line | Leave API p95 Unknown |
| FM-31-05 | Person copies an inherited availability note into a target | A percent appears in a later file | Leave availability Unknown. See `slo-sla-definitions.md` |
| FM-31-06 | Person sets `MODEL_MODE=azure` because logs are quiet | A public-network socket can open | Keep `MODEL_MODE=replay`. See `operational-runbook.md` |
| FM-31-07 | Agent ran and `GET /api/audit/{id}` is empty | Stdout may still show `request_ok` | Re-run the agent with a minted correlation id. Do not invent the missing step |
| FM-31-08 | Person deletes a parked row to tidy the list | Failed intake disappears | Leave the row. FD-19 keeps it visible |

Dead-letter parking and replay stay as built in sub-stage 28. This half does not change `dlq.py`.

---

## SLOs and observability

Behavioural service needs SLO-B1 to SLO-B10 stay in force as written in `system-spec.md`. Numeric cells SLO-N1 to SLO-N8 stay Unknown. See `slo-sla-definitions.md`.

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| `GET /health` HTTP 200 | Application A, B, lake REST, lake MCP | That process accepted a GET | An availability percent |
| `event=health_ok` | stdout | The health request wrote a line | A recovery-time floor |
| `event=identity_missing` | stdout | The identity miss was logged | An error-budget percent |
| `event=intake_parked` | stdout | SC-28-01 wrote a row | A cost saving |
| `duration_ms` | stdout | Time for that one request | API p95 |
| `GET /api/audit/{id}` rows | audit sqlite | SLO-B10 for that id | A latency floor |
| `event=replay_miss` after Half B | stdout | The miss is visible without Azure | A citation percent |

Do not copy the inherited availability note as a floor. **Verified Fact.** FD-19. FD-11. The 0C envelope left those cells Unknown.

---

## Cost and the 0C envelope

SC-31-01 adds no live model call. Token line B1 in `docs/00-preflight/ai-economics/provisional-token-budget.md` stays 0 prompt tokens and 0 completion tokens when `MODEL_MODE=replay`. Lines B2 to B7 stay Unknown.

Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED legacy fields. This half claims no dollar benefit. **Verified Fact.** FD-19. BO-11 working answer stays PROPOSED.

---

## The one small control Half B puts in code

Engineering decision ED-P13-31A-01 continued, authority: team-force.

Control id **SC-31-01**. Name: write a `replay_miss` JSON line on Application A query.

Before SC-31-01, `POST /api/query` called `generate()`. A miss returned HTTP 200 with `verdict` `ABSTAIN` and `error_class` `replay_miss`. Middleware then emitted `request_ok`. No line had `event=replay_miss`. Honesty: REAL in `telemetry-results.md`.

After Half B:

1. `apps/app_a/routes/query.py` calls `emit` when `result.get("error_class") == "replay_miss"`.
2. The line uses `service=app-a`, `event=replay_miss`, `level=info`, `path=/api/query`, `status=200`.
3. `correlation_id` is the `X-Correlation-Id` header, or null when that header is empty.
4. Extra fields are `model_mode` from the process, `error_class=replay_miss`, and `prompt_hash` from the result when present.
5. `MODEL_MODE` stays `replay`. Azure variables stay unset. Half B does not call Azure.
6. Application B query stays as built in this sub-stage.
7. Half B adds no metrics product and no extra container.
8. `/health` stays HTTP 200.

Check id **HB-31-01**. One pytest file `tests/platform/test_phase13_observability.py`.

| Row | What the test does | Honesty after Half B |
|---|---|---|
| Before | Same `POST /api/query` with a retrieve hit and no replay file. Capture stdout. Assert no line has `event=replay_miss` | REAL. `request_ok` present. `replay_miss` absent |
| After | Same POST. Assert one JSON line has `service=app-a`, `event=replay_miss`, and the supplied `correlation_id` | REAL. One line. Id `corr-p13-31b-doc-20261018-001` |
| After, mode | Assert `model_mode` is `replay` | REAL. `replay` |
| After, network | Socket create stays forbidden during the POST | REAL. `create_connection` patched. `socket.socket` forbidden inside `generate()` |
| After, health | `GET /health` still HTTP 200 | REAL. 200 `{"ok": true}` |
| After, cited | GQ-23 cited answer is not labeled `replay_miss` | REAL. `verdict` `ANSWER`. `error_class` null. No miss line |

Worked example for the before row. Question `What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file`. Header `X-Correlation-Id: corr-p13-31b-doc-20261018-001`. Retrieve finds that item id. Replay has no file. HTTP 200. `error_class` is `replay_miss`. Stdout lines include `request_ok` and omit `replay_miss`. Honesty: REAL.

Half B may copy `operational-runbook.md` into `operations/operational-runbook.md`. That copy places the same text under `operations/`.

---

## What this file does not do

This file named the design. Half B wrote the emit and recorded HB-31-01 in `telemetry-results.md`. This file does not write sub-stage 32 or 33. It does not update a tracker. It does not invent a percent. It does not add a metrics product.
