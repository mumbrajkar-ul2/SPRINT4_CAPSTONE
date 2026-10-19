# Acceptance test plan

| Field | Value |
|---|---|
| Stage | Phase 8 / 18 Delivery planning. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Tests are named. Test code is Half B. |
| Evidence sources | `docs/18-delivery/definition-of-done.md`; `docs/12-specs/error-handling-spec.md`; `docs/12-specs/api-contracts.md`; `docs/13-traceability/test-to-evidence-map.md`; `Execution_Plan.md` section 10 |
| Assumptions | Half B writes the tests after HALF_A_ACCEPTED. Scenario tests AT-S7 to AT-S13 stay Phase 9 and Phase 11. |
| Unresolved issues | Live HTTP on the six ports stays Unknown until Half B or a human starts compose. |
| Residual risks | Treating CT-35 (8080 without identity returns 200) as a fail would hide that it records current behaviour. |

This file names the acceptance tests for the Phase 8 platform. It does not write the test modules. It does not invent a latency target.

---

## Finding

**Finding.** Eleven platform tests cover health, identity, lake read-only, replay, compose ports, CI omissions, logs, and the freeze. Scenario tests stay later.
**Evidence.** EH-01. API-L-01. GAP-02. GAP-03. Planned AT-ID and AT-HEALTH in `docs/13-traceability/`.
**Impact.** Half B has a closed test list.
**Risk.** Adding AT-S8 here would pull Application A features into Phase 8.
**Confidence.** High on the names. Unknown on live ports.
**Open questions.** Whether Half B starts listeners inside pytest or only through compose.

---

## Shared rules

- Label every demo number REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.
- Health-check output is REAL.
- Do not assert a p95, an availability percent, or a cycle-time target.
- Do not expect 8080 to return 401. CT-35 already records 200 without identity.
- Use a copy of packaged SQLite when a test might write.
- Use `FABPULSE_API_KEY` from the environment. Default for local tests is `local-demo-only`.

---

## Platform tests

### AT-HEALTH-8080 Legacy health

| Field | Value |
|---|---|
| Route | `GET http://127.0.0.1:8080/health` |
| Pass when | HTTP 200 |
| Fail when | Listener down |
| Finding | Inherited compose already healthchecks this path |
| Evidence | Inherited `compose.yaml` |
| Impact | Minutes 0 to 8 still have a current system |
| Risk | Replacing 8080 with Application A |
| Confidence | High on the path. Unknown until started |
| Open questions | Live run |
| Honesty | REAL when executed |

### AT-HEALTH-8090 Gateway health

| Field | Value |
|---|---|
| Route | `GET http://127.0.0.1:8090/health` |
| Pass when | HTTP 200 |
| Fail when | Listener down |
| Finding | Inherited compose already healthchecks this path |
| Evidence | Inherited `compose.yaml` |
| Impact | Scenario 11 later still has a fixture |
| Risk | Adding identity and breaking the inherited client |
| Confidence | High on the path |
| Open questions | Live run |
| Honesty | REAL when executed |

### AT-HEALTH-8091 Lake REST health

| Field | Value |
|---|---|
| Route | `GET http://127.0.0.1:8091/health` |
| Pass when | HTTP 200 and body includes `{ "ok": true }`. No API key required |
| Fail when | Listener down, or health requires a key |
| Finding | API-L-01 |
| Evidence | `api-contracts.md` |
| Impact | Compose can mark the lake healthy |
| Risk | Putting items in the health body |
| Confidence | High |
| Open questions | Live run |
| Honesty | REAL when executed |

### AT-HEALTH-8092 Lake MCP ready

| Field | Value |
|---|---|
| Route | Documented ready check on 8092. Prefer `GET /health` if the SDK allows a sibling HTTP port. Otherwise a tools-list call that does not need a model |
| Pass when | The listener accepts a connection and lists the four read tools |
| Fail when | No listener, or a write tool is listed |
| Finding | API-M |
| Evidence | `api-contracts.md` |
| Impact | Later agents have a port |
| Risk | Skipping a ready check because MCP is not HTTP |
| Confidence | Medium on the exact ready URL |
| Open questions | Ready URL Half B records |
| Honesty | REAL when executed |

### AT-HEALTH-8100 Application A health

| Field | Value |
|---|---|
| Route | `GET http://127.0.0.1:8100/health` |
| Pass when | HTTP 200 and `{ "ok": true }`. No identity required |
| Fail when | Listener down, or health requires headers |
| Finding | API-Q-01. GAP-03 |
| Evidence | `api-contracts.md`. ED-P8A-01 |
| Impact | Speaker URL for Application A is known |
| Risk | Serving a case list from health |
| Confidence | High |
| Open questions | Live run |
| Honesty | REAL when executed |

### AT-HEALTH-8110 Application B health

| Field | Value |
|---|---|
| Route | `GET http://127.0.0.1:8110/health` |
| Pass when | HTTP 200 and `{ "ok": true }`. No identity required |
| Fail when | Listener down, or health requires headers |
| Finding | API-Q-01. GAP-03 |
| Evidence | `api-contracts.md`. ED-P8A-01 |
| Impact | Speaker URL for Application B is known |
| Risk | Serving lineage from health |
| Confidence | High |
| Open questions | Live run |
| Honesty | REAL when executed |

### AT-ID-A Application A missing identity

| Field | Value |
|---|---|
| Route | `GET http://127.0.0.1:8100/api/identity-check` with no headers |
| Pass when | HTTP 401. `error_class: missing_identity`. No case body |
| Fail when | HTTP 200, or a case list |
| Finding | EH-01. Planned AT-ID |
| Evidence | `error-handling-spec.md`. `test-to-evidence-map.md` |
| Impact | BP8 scaffolding is visible |
| Risk | Copying CT-35 onto Application A |
| Confidence | High |
| Open questions | None for the status code |
| Honesty | REAL when executed |

Worked example. The same path on 8080 is 200 today. That is CT-35. Application A on 8100 must be 401.

### AT-ID-B Application B missing identity

| Field | Value |
|---|---|
| Route | `GET http://127.0.0.1:8110/api/identity-check` with no headers |
| Pass when | HTTP 401. `error_class: missing_identity` |
| Fail when | HTTP 200 |
| Finding | EH-01 |
| Evidence | Same as AT-ID-A |
| Impact | Both apps close the no-auth gap |
| Risk | Only gating Application A |
| Confidence | High |
| Open questions | None |
| Honesty | REAL when executed |

### AT-ID-HIT Accepted identity

| Field | Value |
|---|---|
| Route | `GET /api/identity-check` on 8100 and 8110 with `X-Api-Key`, `X-Actor-Id: demo-rt01-1`, `X-Actor-Role: RT-01` |
| Pass when | HTTP 200. Body echoes actor id and role. No case fields |
| Fail when | 401 with the documented default key, or a recipe or queue payload |
| Finding | ED-P8A-02 |
| Evidence | `implementation-prd.md` |
| Impact | Later screens can send the same headers |
| Risk | Using INC-2025-014 as the demo actor |
| Confidence | High |
| Open questions | None for the demo actor id. It is a scaffold label, not an incident owner |
| Honesty | REAL when executed |

### AT-ID-KEY Wrong key

| Field | Value |
|---|---|
| Route | Identity probe with `X-Api-Key: wrong`, plus actor headers |
| Pass when | HTTP 401. `error_class: missing_identity` |
| Fail when | HTTP 200 |
| Finding | Secrets rule |
| Evidence | Phase 8 locked facts |
| Impact | A guessed key does not pass |
| Risk | Returning 403 with a different body that names the expected key |
| Confidence | High |
| Open questions | None |
| Honesty | REAL when executed |

### AT-LAKE-RO Lake write rejected

| Field | Value |
|---|---|
| Route | `POST http://127.0.0.1:8091/v1/items` with the API key |
| Pass when | HTTP 405. `error_class: lake_write_rejected` |
| Fail when | An item is written |
| Finding | API-L write methods absent |
| Evidence | `api-contracts.md` |
| Impact | YAML in Git stays the source of truth |
| Risk | A convenience POST |
| Confidence | High |
| Open questions | None |
| Honesty | REAL when executed |

### AT-LAKE-KEY Lake read without key

| Field | Value |
|---|---|
| Route | `GET http://127.0.0.1:8091/v1/version` with no key |
| Pass when | HTTP 401 |
| Fail when | Version body with no key |
| Finding | ED-P8A-04 |
| Evidence | `implementation-prd.md` |
| Impact | Anonymous lake reads stop |
| Risk | Gating health the same way |
| Confidence | High |
| Open questions | None |
| Honesty | REAL when executed |

### AT-REPLAY-HIT Saved prompt plays back

| Field | Value |
|---|---|
| Setup | One file in `operations/model-replay/` named by the SHA-256 hex of a fixture prompt |
| Pass when | Lookup in `MODEL_MODE=replay` returns that file body |
| Fail when | A network call is attempted, or a new sentence is invented |
| Finding | Section 10 |
| Evidence | `Execution_Plan.md` section 10 |
| Impact | Offline demo path exists |
| Risk | A third fallback mode |
| Confidence | High |
| Open questions | Fixture prompt wording |
| Honesty | REAL when executed. The fixture sentence is PRECOMPUTED |

### AT-REPLAY-MISS Missing hash stays local

| Field | Value |
|---|---|
| Setup | `MODEL_MODE=replay`. Prompt whose hash has no file |
| Pass when | Structured error. No public-network socket to a model host |
| Fail when | An outbound model call starts, or a guessed sentence is returned |
| Finding | Phase 8 locked fact. Section 10 |
| Evidence | Coordinator locked facts for this unit |
| Impact | Offline run does not hang on a missing cache |
| Risk | Silent empty string treated as a model answer |
| Confidence | High |
| Open questions | Exact error_class string. Half B may use `replay_miss` |
| Honesty | REAL when executed |

### AT-COMPOSE-PORTS Published map

| Field | Value |
|---|---|
| Command | `docker compose config` at the capstone root |
| Pass when | Published host ports include 8080, 8090, 8091, 8092, 8100, and 8110 |
| Fail when | Application A shares 8080, or a lake listener uses 8000 |
| Finding | Ports ADR plus ED-P8A-01 |
| Evidence | `adr-ports-and-compose.md` |
| Impact | Speaker URLs stay stable |
| Risk | OS-assigned ports |
| Confidence | High |
| Open questions | None |
| Honesty | REAL when executed |

### AT-CI-SAFE Workflow omissions

| Field | Value |
|---|---|
| File | Capstone `.github/workflows/verify.yml` |
| Pass when | The file has no `app.generate --reset` step and no live model invocation |
| Fail when | Either step is present |
| Finding | Inherited workflow reset gap |
| Evidence | Workshop `verify.yml`. Phase 1 assessment |
| Impact | Freeze stays intact |
| Risk | Copying the inherited file wholesale |
| Confidence | High |
| Open questions | None |
| Honesty | REAL when the file is read |

### AT-LOG-JSON New listeners log JSON

| Field | Value |
|---|---|
| Setup | Identity probe without headers on 8100 |
| Pass when | Stdout contains a JSON object with `service`, `event`, and `level`. `event` is `identity_missing` or the same fact in the chosen event name |
| Fail when | No line, or a line that prints the API key |
| Finding | ED-P8A-07 |
| Evidence | `implementation-prd.md` |
| Impact | Compose logs diagnose a 401 |
| Risk | Logging `X-Api-Key` |
| Confidence | High |
| Open questions | Exact event string |
| Honesty | REAL when executed |

### AT-FREEZE Packaged hashes

| Field | Value |
|---|---|
| Command | Hash check against `sources/register.yaml` after tests |
| Pass when | Packaged files still match |
| Fail when | A test wrote `data/legacy.sqlite3` |
| Finding | Phase 7 signoff residual risk |
| Evidence | `validation-signoff.md` |
| Impact | Baseline remains the Phase 0 freeze |
| Risk | Compose volume pointed at the packaged file |
| Confidence | High |
| Open questions | Volume layout Half B chooses |
| Honesty | REAL when executed |

---

## Tests this plan does not include

| Test | Why it waits |
|---|---|
| AT-S7 to AT-S13 | App features. Phases 9 and 11 |
| AT-PERSON approval gate | Phase 10 |
| AT-RESTART mid-approval | Phase 10. SqliteSaver |
| Injection BLOCK minutes 36 to 39 | Phase 10 and Phase 12. Lake injection tests already exist and stay green |
| Numeric p95 | No target |
| CT-35 as a fail | It records current 8080 behaviour |

---

## What this file does not do

This file does not write pytest modules. It does not start compose. It does not sign a Business Owner row.
