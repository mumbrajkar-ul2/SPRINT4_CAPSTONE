# Resilience architecture

| Field | Value |
|---|---|
| Stage | Phase 13 / 28 Reliability and resilience. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-28a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No resilience code in this half. |
| Evidence sources | FD-19; FD-13; FD-14; FD-15; `apps/app_a/routes/recovery.py`; `apps/app_a/rules/adapter.py`; `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/app/gateway_bridge.py`; `operations/replay_lookup.py`; `apps/app_a/agent/tools.py`; `docs/12-specs/error-handling-spec.md`; `docs/21-integration/failure-semantics.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/27-hardening/runtime-hardening.md` |
| Assumptions | `MODEL_MODE=replay`. One `docker compose up` still starts the seven named containers. Host ports stay 8080, 8090, 8091, 8092, 8100, 8110. BO rows that are PROPOSED stay PROPOSED. Packaged sqlite files stay `mode=ro`. |
| Unresolved issues | Numeric latency, availability, recovery-time, recovery-point, and retry-count floors stay Unknown. Dollar benefits stay Unknown. Measured HB-28-01 cells stay Unknown until Half B. Company job titles stay Unknown. INC-2025-014 owner stays Unknown. |
| Residual risks | Auto-retry of an OPA BLOCK would run an injection write. Deleting a parked intake row would hide the failure. Calling Azure on a replay miss would open a public-network socket during the laptop demo. |

This file names how Application A stays up when a probe fails, when intake rejects a message, and when the live model is off. The one Half B control is SC-28-01. That control parks a failed intake and replays it. This half does not add a product screen. This half does not add a message bus.

Engineering decision ED-P13-28A-01, authority: team-force. One extra attempt after the first `upstream_timeout` or `upstream_rate_limit` on the source-gateway probe. Constant name `UPSTREAM_RETRY_COUNT`. Value `1`. Total attempts `2`. This integer is an engineering default. It is not Business Owner policy. It is not a quality floor. The retry-count floor stays Unknown.

Engineering decision ED-P13-28A-02, authority: team-force. Control id `SC-28-01`. Check id `HB-28-01`. Dead-letter store path `apps/app_a/runtime/dlq.sqlite3`. Tests may point that path at a temp file.

Engineering decision ED-P13-28A-03, authority: team-force. Failure ids `FM-28-01` to `FM-28-10`. Injection ids `FI-28-01` to `FI-28-08`.

---

## Finding

**Finding.** Application A already shows a gateway timeout, schema miss, and throttle on `GET /api/recovery`. The probe may return HTTP 503. The recovery GET stays HTTP 200. `retry_shown` is true. The process does not retry the probe. `intake_apply` counts a bad message as `invalid` and does not store it. The person sees a count and does not see the parked body. When the live model is off, `MODEL_MODE=replay` reads `operations/model-replay/{sha256}`. A miss returns `replay_miss` and abstains. Injection still returns HTTP 409 `blocked`. `WRITE_TOOLS` is `[]`. Half B parks one invalid intake row, keeps it visible, and replays it. A completed payload on replay is accepted on a temp store. Numeric floors stay Unknown.
**Evidence.** `probe_gateway` in `apps/app_a/routes/recovery.py` uses `timeout=3` and calls once. `intake_apply` in `gateway_bridge.py` increments `invalid` and continues. Characterization `test_apply_rejects_missing_required_fields` uses `{"message_id": "bad"}` and expects `invalid` 1, `accepted` 0. FD-19. `WRITE_TOOLS = []` in `apps/app_a/agent/tools.py`.
**Impact.** Half B edits the recovery module and adds a small dead-letter helper. One pytest file records before and after.
**Risk.** Retrying BLOCK, or parking an injection approve as if it were a later EXECUTE, would skip FD-10.
**Confidence.** High on the current probe and intake counts. Unknown on measured park and replay rows until Half B.
**Open questions.** HALF_A_ACCEPTED. Measured HB-28-01 cells.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. A failed intake stays visible to the person. Numeric latency, availability, recovery-time, recovery-point, retry-count, and cost floors stay Unknown until a measured run. This half invents no percent and no dollar benefit. The engineering retry default in ED-P13-28A-01 is not a floor.

**Verified Fact.** FD-13. Compose default `MODEL_MODE=replay`. Replay files live under `operations/model-replay/`. There is no third offline mode.

**Verified Fact.** FD-14. A consequential answer cites a lake item id or abstains. Percent floors stay Unknown.

**Verified Fact.** FD-15. `WRITE_TOOLS` is empty. Recursion limit 12. Step budget 8. Max tool calls 8. Max gather visits 3. Checkpoint file `apps/app_a/runtime/checkpoints.sqlite3`.

**Verified Fact.** FD-04. Intake de-duplication is deterministic code. The model does not decide accept or invalid.

**Verified Fact** of BO-01 through BO-13 that are PROPOSED. Those rows stay PROPOSED. This half invents no signer name. BO-03 working answer still sends every record-changing write through a person.

**Verified Fact.** Injection still BLOCKS. HTTP 409. `error_class: blocked`. The model has no write tool.

---

## What is already running

**Verified Fact.**

| Piece | What it does today | Label |
|---|---|---|
| `GET /api/recovery` | Returns `status_visible`, `error_class`, `retry_shown`. Identity required. HTTP 200 | Verified Fact of `recovery.py` |
| `GET /api/recovery/probe?mode=timeout` | Calls the source gateway or the local fixture. HTTP 503. `error_class: upstream_timeout` | Verified Fact |
| `GET /api/recovery/probe?mode=schema` | HTTP 503. `error_class: upstream_schema` | Verified Fact |
| `GET /api/recovery/probe?mode=rate_limit` | HTTP 503. `error_class: upstream_rate_limit` | Verified Fact |
| `GET /api/recovery/probe?mode=normal` | HTTP 200. `error_class: none` | Verified Fact |
| Gateway client timeout | 3 seconds on `urlopen` | Verified Fact of the current code. Client timeout, not an SLO |
| Lake retrieve HTTP timeout | 5 seconds | Verified Fact of `retrieve.py`. Client timeout, not an SLO |
| OPA `eval` timeout | 15 seconds | Verified Fact of `opa_client.py`. Client timeout, not an SLO |
| Azure complete timeout | 30 seconds | Verified Fact of `azure_client.py`. This half does not call Azure |
| `intake_apply` | Counts `accepted`, `duplicates`, `invalid`, `received`. Writes accepted rows to `gateway_inbox` with `message_id` as the primary key | Verified Fact |
| Model replay | Reads a file named by SHA-256 of the prompt. Miss returns `replay_miss`. Opens no public-network socket | Verified Fact |
| Agent tools | Six read names. `WRITE_TOOLS` is `[]` | Verified Fact |
| `/health` | HTTP 200 `{"ok": true}` when the process is up | Verified Fact |

Worked example. `GET /api/recovery/probe?mode=timeout` with headers `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` returns HTTP 503. `retry_shown` is true. `GET /api/recovery` on the next call still returns HTTP 200 and repeats the visible status. The first failure stays in `_LAST`. The probe ran once.

Worked example. `intake_apply([{"message_id": "bad"}])` returns `received` 1, `invalid` 1, `accepted` 0. The body is not in `gateway_inbox`. The person who only sees those four counts cannot open the parked payload.

---

## Layers

| Layer | What fails | What Application A does | Recovery |
|---|---|---|---|
| Process | Named container exits | Compose health marks unhealthy after five failed probes | Start that service again. Restart seconds stay Unknown |
| Identity | Missing headers or missing process key | HTTP 401 or, after sub-stage 27, HTTP 503 `missing_server_key` on `/api`. `/health` stays 200 | Send headers. Or set `FABPULSE_API_KEY` |
| Source gateway | Timeout, schema, or throttle | Probe HTTP 503. Recovery GET HTTP 200. After the extra attempt in ED-P13-28A-01, a still-failing timeout or throttle sets the circuit flag | `mode=normal` probe. Schema is not retried |
| Intake | Missing fields or unknown lot | Count `invalid`. After SC-28-01, write one dead-letter row and keep it on GET `/api/recovery` | Replay the parked id. Completed fields on a temp store can accept. Packaged `legacy.sqlite3` stays unread-write |
| Lake | Listener down or empty accepted set | Query abstains. HTTP 200 `verdict: ABSTAIN` | Start lake REST. Or use in-process `lake_runtime` |
| Model | Live Azure off, or replay miss | `MODEL_MODE=replay`. Miss abstains. No Azure socket | Keep replay. Add a PRECOMPUTED file only in a later rehearsal |
| Policy | Injection write-from-text | OPA BLOCK. HTTP 409. No park-to-execute path | Leave the case unchanged |
| Graph | Recursion 12 or step budget 8 | HOLD_FOR_REVIEW. Draft stays a draft | Person at the mapped RT role resumes |

---

## Dead-letter store

Dead-letter store. Application A writes one SQLite row for an intake message that `intake_apply` counted as invalid.

**Verified Fact** of the need. FD-19. **Inference** of the file path, authority: team-force.

| Field | Value |
|---|---|
| Path | `apps/app_a/runtime/dlq.sqlite3` |
| Writer | Application A code. The model has no tool for this file |
| Packaged `legacy.sqlite3` | Stays `mode=ro`. Half B does not insert into packaged `gateway_inbox` |
| Tests | Temp file. Temp `LEGACY_DB` copied from the packaged store, same pattern as characterization `TempLegacyMixin` |
| Visibility | `GET /api/recovery` includes `parked_intakes`. Each row stays after replay |
| Replay | `POST /api/recovery/dlq/replay` with identity headers and `parked_id`. Re-runs `intake_apply` on that body |

A row is kept after a successful replay. Status becomes `REPLAYED`. The original failure stays visible. Half B does not delete the row.

Identity misses, OPA BLOCK rows, and replay misses are not parked in this file. Those results return on the same request.

---

## Circuit flag

Circuit. That is a process flag on Application A.

After both probe attempts return `upstream_timeout` or `upstream_rate_limit`, Application A skips the next call to port 8090 and returns `error_class: circuit_open`. `GET /api/recovery` stays HTTP 200. The skipped call and the earlier failures stay in the body.

A `mode=normal` probe is the trial. HTTP 200 clears the flag. A still-failing trial leaves the flag set.

Schema mismatch does not set the flag. Injection BLOCK does not set the flag. Replay miss does not set the flag.

Half B does not have to wire this flag to pass HB-28-01. Measured circuit cells stay Unknown until a later check. The flag is named so Half B does not invent a second retry count.

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery | Numeric floor |
|---|---|---|---|---|
| FM-28-01 | Intake missing required fields | After SC-28-01: parked row on `GET /api/recovery`, `invalid` 1, `accepted` 0 | Replay. Same body stays `PARKED`. Completed body on a temp store can become `REPLAYED` | None invented |
| FM-28-02 | Intake unknown lot | Parked row. `business_key` visible | Replay after the lot exists in the temp store, or leave `PARKED` | None invented |
| FM-28-03 | Gateway timeout | Probe HTTP 503. Recovery GET HTTP 200. `retry_shown` true | One extra attempt. Then `mode=normal` | Retry floor Unknown. Default extra attempts = 1 |
| FM-28-04 | Gateway schema | Probe HTTP 503. No extra attempt | Fix the body. Retry is visible. Circuit flag stays clear | None invented |
| FM-28-05 | Gateway throttle | Probe HTTP 503. One extra attempt | `mode=normal` | Same default of 1 |
| FM-28-06 | Live model off | Replay file or `replay_miss` abstain | Keep `MODEL_MODE=replay` | Token line B1 stays 0 and 0 in the envelope |
| FM-28-07 | Replay miss | `error_class: replay_miss`. `verdict: ABSTAIN` | Do not call Azure. Add a saved file only in a later rehearsal | None invented |
| FM-28-08 | Injection approve, release, ignore-validation, or close-from-text | HTTP 409 `blocked`. Case unchanged | Leave the record. Do not retry. Do not park as EXECUTE | None invented |
| FM-28-09 | Graph budget exhausted | HTTP 409 `wait_for_person` | Person at the mapped RT role. Checkpoint file keeps the wait | Recursion 12 and step 8 stay engineering defaults from FD-15 |
| FM-28-10 | Named container exits | Compose unhealthy after five failed probes | `docker compose up` for that service | Restart seconds Unknown |

Worked example for FM-28-01. Payload `{"message_id": "DLQ-28-BAD"}` is missing `business_key`, `system`, `event_type`, and `occurred_at`. Today `intake_apply` returns `invalid` 1. After SC-28-01 the same payload is one parked row. `GET /api/recovery` lists `message_id` `DLQ-28-BAD` and `status` `PARKED`. Replay of that same body still returns `invalid` 1. The row stays `PARKED`. The person can still read it.

Worked example for recovery. The test copies packaged `legacy.sqlite3` to a temp file. It parks a payload that has `message_id` `DLQ-28-OK`, `business_key` equal to the first `lot_id` in that temp file, `system` `mes`, `event_type` `lot_started`, and no `occurred_at`. Replay then sends the same keys plus `occurred_at` `2025-02-02T03:00:00Z`. `intake_apply` returns `accepted` 1. Parked status becomes `REPLAYED`. Packaged `legacy.sqlite3` is not opened for write.

---

## Runbook — park, replay, and bring a probe back

1. `GET /health` on 8100. HTTP 200 means the process is up.
2. `GET /api/recovery` with the three identity headers. Read `error_class`, `retry_shown`, and `parked_intakes`.
3. If `error_class` is `timeout` or `upstream_timeout`, the source gateway did not answer in 3 seconds. The extra attempt may already have run. Send `GET /api/recovery/probe?mode=normal` when the fixture should pass.
4. If `error_class` is `schema`, do not expect an extra attempt. The body did not match. Retry stays visible.
5. If `parked_intakes` has a `PARKED` row, open that row. Replay with `POST /api/recovery/dlq/replay` and the `parked_id`.
6. If replay still reports `invalid`, the body is still missing a field or the lot is unknown. Leave the row `PARKED`.
7. If `error_class` is `blocked`, stop. Do not replay that action as a write.
8. If `error_class` is `replay_miss`, keep `MODEL_MODE=replay`. Do not set `azure` on the laptop demo.

A copy of this runbook into `operations/` belongs to sub-stage 29.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| `/health` HTTP 200 | Application A | The process accepted a GET | An availability percent |
| Probe HTTP 503 | `/api/recovery/probe` | That one upstream mode failed | API p95 |
| `retry_shown` true | Recovery body | The person can see retry | A retry-count floor |
| JSON `event=intake_parked` after Half B | stdout | SC-28-01 wrote a row | A cost saving |
| JSON `event=intake_replayed` after Half B | stdout | Replay ran | An SLO |
| `duration_ms` | stdout | Time for that one request | API p95 |

Availability, API p95, retrieval p95, recovery time, and recovery point stay Unknown. **Verified Fact.** FD-19. The 0C envelope left those cells Unknown. This half leaves them Unknown.

Do not copy the inherited 99.5 percent availability note. Do not copy the inherited 8-hour recovery note.

---

## Cost and the 0C envelope

SC-28-01 adds no live model call. Token line B1 in `docs/00-preflight/ai-economics/provisional-token-budget.md` stays 0 prompt tokens and 0 completion tokens when `MODEL_MODE=replay`. Lines B2 to B7 stay Unknown.

Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED legacy fields. This half claims no dollar benefit. **Verified Fact.** FD-19. BO-11 working answer stays PROPOSED.

---

## The one small control Half B puts in code

Engineering decision ED-P13-28A-02 continued, authority: team-force.

Control id **SC-28-01**. Name: park a failed intake and replay it.

Today `intake_apply` increments `invalid` and continues. The payload is not stored.

After Half B:

1. `apps/app_a/runtime/dlq.py` opens `apps/app_a/runtime/dlq.sqlite3` (or a temp path in tests). Table `parked_intake` holds `parked_id`, `message_id`, `payload_json`, `reason`, `status`, `correlation_id`, `parked_at`, `replayed_at`.
2. Application A wraps `intake_dedupe` / `intake_apply` so each invalid event writes one row with `status` `PARKED`. Accepted and duplicate events do not write this table.
3. `GET /api/recovery` adds `parked_intakes` as a list of those rows. Identity stays required. HTTP stays 200.
4. `POST /api/recovery/dlq/replay` requires the three identity headers. Body has `parked_id`. Optional `payload` replaces the stored JSON when the test supplies completed fields. Re-runs `intake_apply` against the test `LEGACY_DB`. Same body still invalid keeps `PARKED`. `accepted` 1 sets `REPLAYED` and `replayed_at`. The row stays in the list.
5. Packaged `legacy.sqlite3` stays `mode=ro`. Half B uses a temp copy for accept.
6. `WRITE_TOOLS` stays `[]`. Injection BLOCK stays HTTP 409. Half B does not park BLOCK as a later write.
7. `/health` stays HTTP 200.

Application B recovery stays as built in this sub-stage. Port 8080 and port 8090 stay ungated.

---

## Exact Half B check HB-28-01

Test path Half B writes: `tests/platform/test_phase13_resilience.py`.

Headers for the probe:

| Header | Value |
|---|---|
| `X-Api-Key` | `local-demo-only` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |

Honesty of today's before cells and of Half B after cells: REAL when the test runs. This Half A file leaves measured cells Unknown.

### Before (today's `intake_apply` and `GET /api/recovery`)

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| `intake_apply([{"message_id": "DLQ-28-BAD"}])` `invalid` | 1 | Unknown until Half B | Unknown |
| `accepted` | 0 | Unknown until Half B | Unknown |
| `GET /api/recovery` `parked_intakes` | Absent or `[]` | Unknown until Half B | Unknown |
| `GET /health` | 200 `{"ok": true}` | Unknown until Half B | Unknown |

### After (SC-28-01 landed)

Same identity headers. Temp `LEGACY_DB`. Temp dead-letter file.

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| Park `{"message_id": "DLQ-28-BAD"}` `invalid` | 1 | Unknown until Half B | Unknown |
| `accepted` | 0 | Unknown until Half B | Unknown |
| `parked_intakes` length | 1 | Unknown until Half B | Unknown |
| That row `message_id` | `DLQ-28-BAD` | Unknown until Half B | Unknown |
| That row `status` | `PARKED` | Unknown until Half B | Unknown |
| Replay same body `status` | `PARKED` | Unknown until Half B | Unknown |
| Replay completed payload `accepted` | 1 | Unknown until Half B | Unknown |
| Completed row `status` | `REPLAYED` | Unknown until Half B | Unknown |
| Row still listed on GET | true | Unknown until Half B | Unknown |
| `GET /health` | 200 `{"ok": true}` | Unknown until Half B | Unknown |
| Packaged `legacy.sqlite3` write | none | Unknown until Half B | Unknown |
| `WRITE_TOOLS` | `[]` | Unknown until Half B | Unknown |

Full measured table belongs in `failure-injection-results.md` after Half B.

---

## What this file does not do

This file does not write SC-28-01. It does not start Half B. It does not write sub-stages 29 to 33. It does not call Azure. It does not invent an availability percent. It does not invent a dollar benefit. It does not sign a Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
