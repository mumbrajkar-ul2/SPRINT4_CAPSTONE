# Delivery backlog

| Field | Value |
|---|---|
| Stage | Phase 8 / 18 Delivery planning. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Documents only. No compose, CI, or app code written. |
| Evidence sources | `docs/17-implementation-prd/implementation-prd.md`; `docs/17-implementation-prd/release-boundaries.md`; `Execution_Plan.md` sections 5 and 10; inherited `compose.yaml`; inherited `.github/workflows/verify.yml` |
| Assumptions | Half B runs after HALF_A_ACCEPTED. Half B writes only the Phase 8 increment. Later phase rows stay PLANNED. |
| Unresolved issues | Live Docker on the Half B machine stays Unknown. GitHub runner availability stays Unknown. BO-06b and BO-08 stay PROPOSED. |
| Residual risks | Writing app feature screens in Half B would break the Phase 8 exclude list. Running `generate --reset` would void the freeze. |

This file lists the delivery increments. Phase 8 Half B items are specified in full. Later phase items are named so the coordinator can see the order. They are not started here.

---

## Finding

**Finding.** Fifteen Half B items stand up compose, lake listeners, identity stubs, replay wiring, logs, and CI. Later increments stay with Phases 9 to 16.
**Evidence.** Phase 8 scope. `release-boundaries.md`. ED-P8A-01 through ED-P8A-08.
**Impact.** Half B can open this list and write files without inventing a product feature.
**Risk.** Starting Application A scenario 8 in this list would hide that Phase 9 owns that work.
**Confidence.** High on the Phase 8 list. Unknown on live Compose.
**Open questions.** Whether the sandbox can build container images.

---

## How to read an item

Each Phase 8 item is one Half B job. Status in this file is PLANNED. Half B records the result in `docs/18-delivery/evidence-checklist.md` after acceptance.

Honesty on packaged counts cited from earlier phases stays REAL.

Shared rules for every item:

- Do not hard-code `FABPULSE_API_KEY` in source.
- Do not invent a numeric SLO percent.
- Do not write 50,000 or 999,999 as live policy.
- Do not assign an INC-2025-014 owner.
- Do not call a public network when `MODEL_MODE=replay`.
- Do not edit `Decision_Tracker.md` or `STATUS.md`.

---

## Phase 8 Half B — platform increment

### DB-01 Capstone Compose file

| Field | Value |
|---|---|
| Files Half B writes | `compose.yaml` at the capstone root. `.env.example` |
| Finding | Inherited Compose starts only `legacy`, `source-gateway`, and `bridge` |
| Evidence | Inherited `compose.yaml` |
| Impact | One `docker compose up` can start the six host ports |
| Risk | Editing the inherited workshop Compose in place would mix the baseline file with the full stack |
| Confidence | High |
| Open questions | Live Docker |
| Pass when | `docker compose config` shows 8080, 8090, 8091, 8092, 8100, and 8110. Services use the container names in ED-P8A-05 |

Worked example. The capstone file publishes `"8100:8100"` for `app-a`. It does not publish Application A on 8080.

### DB-02 Environment defaults

| Field | Value |
|---|---|
| Files Half B writes | `.env.example` |
| Finding | Inherited `environments/dev.env.example` names HOST, PORT, SOURCE_PORT, LOG_LEVEL only |
| Evidence | That file |
| Impact | A new clone can start without inventing a key |
| Risk | Putting the key in a `.py` file |
| Confidence | High |
| Open questions | None for the variable name |
| Pass when | `.env.example` lists `FABPULSE_API_KEY=local-demo-only`, `MODEL_MODE=replay`, and the six host ports. Application source has no key literal |

### DB-03 Lake REST listener

| Field | Value |
|---|---|
| Files Half B writes | Lake REST server under `context-lake/` serving port 8091 |
| Finding | The generated lake file exists. No REST process exists |
| Evidence | `context-lake/generated/manifest.json`. Phase 0 architecture note |
| Impact | Screens and later Application B can read items |
| Risk | A write route on 8091 would skip `build.py` |
| Confidence | High on the contract. Unknown on Half B runtime libraries |
| Open questions | Process language. FastAPI is the locked app stack. The lake listener may use the same |
| Pass when | `GET /health` is 200. `GET /v1/version` returns lake 1.0.0 when the key is present. Write methods return 405. Missing key on a read returns 401 |

### DB-04 Lake MCP listener

| Field | Value |
|---|---|
| Files Half B writes | Lake MCP server on port 8092 |
| Finding | Four tools are already named |
| Evidence | `docs/12-specs/api-contracts.md` API-M |
| Impact | Later agents read the same lake |
| Risk | A write tool would break FD-02 |
| Confidence | High on the four names |
| Open questions | MCP SDK pin |
| Pass when | Tools `search_items`, `get_item`, `get_links`, and `rule_at` are listed. Write tools are absent. Health or an equivalent ready check is 200 |

### DB-05 Application A stub

| Field | Value |
|---|---|
| Files Half B writes | `apps/app_a/` health and identity probe |
| Finding | `apps/` does not exist |
| Evidence | Workspace glob |
| Impact | Port 8100 can go healthy. Identity 401 can be tested |
| Risk | Implementing `/api/queue` ranking would be an app feature |
| Confidence | High |
| Open questions | None for the probe path |
| Pass when | `GET /health` is 200. `GET /api/identity-check` without headers is 401. The same path with the three headers is 200 and echoes `actor_id` and `actor_role`. No scenario body is returned |

### DB-06 Application B stub

| Field | Value |
|---|---|
| Files Half B writes | `apps/app_b/` health and identity probe |
| Finding | Application B is a later phase |
| Evidence | `Execution_Plan.md` Phase 11 |
| Impact | Port 8110 can go healthy on the same command |
| Risk | Building lineage in this stub |
| Confidence | High |
| Open questions | None for the probe path |
| Pass when | Same checks as DB-05 on port 8110. No `/api/lineage` feature body |

### DB-07 Identity middleware

| Field | Value |
|---|---|
| Files Half B writes | Shared header check used by both stubs and the lake listeners |
| Finding | EH-01 already maps missing identity to 401 |
| Evidence | `error-handling-spec.md` |
| Impact | One check, two apps |
| Risk | Hard-coded key |
| Confidence | High |
| Open questions | Shared package path. Default `apps/shared/identity.py` unless Half B has a better local module |
| Pass when | Missing header, empty header, and wrong key each return 401 with `error_class: missing_identity`. Health stays 200 without headers |

### DB-08 Replay lookup helper

| Field | Value |
|---|---|
| Files Half B writes | `operations/model-replay/` directory. Lookup helper. One sample file for the unit test |
| Finding | Section 10 already names hash-of-prompt replay |
| Evidence | `Execution_Plan.md` section 10 |
| Impact | Later Phase 9 calls this helper |
| Risk | Inventing a third mode |
| Confidence | High |
| Open questions | Sample prompt text for the unit test |
| Pass when | A known hash returns the saved file. A missing hash returns a structured error and does not open a public-network socket. `MODEL_MODE=replay` is the compose default |

### DB-09 JSON logs

| Field | Value |
|---|---|
| Files Half B writes | Logging helper used by new listeners. Inherited 8080 and 8090 keep their current logs if a wrap is too large. New listeners must emit JSON |
| Finding | Inherited services log as they do today |
| Evidence | Inherited server files |
| Impact | New services are diagnosable from `docker compose logs` |
| Risk | Adding a metrics container |
| Confidence | High on new listeners. Unknown on wrapping inherited servers without behaviour change |
| Open questions | Whether inherited 8080 and 8090 stay on their current text logs for this increment |
| Pass when | `app-a`, `app-b`, `lake-rest`, and `lake-mcp` each emit a JSON line for `health_ok` and for `identity_missing` |

### DB-10 Capstone CI

| Field | Value |
|---|---|
| Files Half B writes | `.github/workflows/verify.yml` at the capstone root |
| Finding | Inherited CI runs `generate --reset` |
| Evidence | Workshop `.github/workflows/verify.yml` |
| Impact | Pushes check the freeze and the new contracts |
| Risk | Calling the inherited workflow from the capstone workflow |
| Confidence | High |
| Open questions | Whether Actions can start Docker in the sandbox |
| Pass when | The workflow runs characterization tests on a copy, lake tests, identity 401 tests, replay miss test, and `docker compose config`. It does not run `generate --reset`. It does not call a live model |

### DB-11 Characterization rerun in CI

| Field | Value |
|---|---|
| Files Half B writes | CI step only. No new characterization module required unless a path break is found |
| Finding | Phase 7 recorded 70 tests OK |
| Evidence | `docs/16-repo-validation/validation-signoff.md` |
| Impact | Platform work does not silently break the freeze |
| Risk | Running tests against the packaged file instead of a copy |
| Confidence | High |
| Open questions | None for the six-field target |
| Pass when | Characterization suite is green on a copy. Packaged hashes match `sources/register.yaml` |

### DB-12 One-command bring-up

| Field | Value |
|---|---|
| Files Half B writes | None beyond DB-01. This item is the live run |
| Finding | Section 10 requires one command |
| Evidence | `Execution_Plan.md` section 10 |
| Impact | The Done test can be run |
| Risk | Sandbox blocks Docker. Reviewer then marks NEEDS_HUMAN |
| Confidence | Unknown until run |
| Open questions | Human paste-back if the sandbox blocks |
| Pass when | `docker compose up` reports healthy on 8080, 8090, 8091, 8092, 8100, and 8110. Honesty of that output: REAL |

### DB-13 Replay with no public network

| Field | Value |
|---|---|
| Files Half B writes | Compose environment `MODEL_MODE=replay`. Optional compose note that outbound internet is unused |
| Finding | Locked fact: the stack runs with no network |
| Evidence | Phase 8 locked facts. Section 10 |
| Impact | Venue demo can start with the laptop offline |
| Risk | A hidden download in a build step |
| Confidence | Medium until proven |
| Open questions | Whether image builds need a network once and then run offline |
| Pass when | With `MODEL_MODE=replay`, a replay miss does not attempt a public-network model call. Health still returns 200 |

### DB-14 Evidence sheet

| Field | Value |
|---|---|
| Files Half B writes | Fills result cells in `docs/18-delivery/evidence-checklist.md` |
| Finding | This Half A file leaves those cells unrun |
| Evidence | This folder |
| Impact | Reviewer can see REAL health output |
| Risk | Pasting a simulated 200 as REAL |
| Confidence | High on the rule |
| Open questions | Live output |
| Pass when | Each listener row has a REAL health result or a NEEDS_HUMAN note |

### DB-15 No app features

| Field | Value |
|---|---|
| Files Half B writes | None. This is a negative check |
| Finding | Phase 8 exclude list is app features |
| Evidence | `playbook/phase_08_foundations.md` |
| Impact | Phase 9 still owns scenarios 7 to 11 |
| Risk | A helpful queue screen |
| Confidence | High |
| Open questions | None |
| Pass when | `apps/app_a/` and `apps/app_b/` contain no ranking, approval, query, recovery, or lineage feature handler |

---

## Later increments (not this unit)

Status for every row below is PLANNED. Half B does not start them.

| ID | Phase | What it delivers | Owner decision still open |
|---|---|---|---|
| DB-L09 | 9 | Application A scenarios 7 to 11. Prompt registry. Retrieval | FD-14 Unknown floors |
| DB-L10 | 10 | LangGraph pause, OPA verdicts, audit rows | FD-15, FD-16, FD-23 |
| DB-L11 | 11 | Application B from the lake. Parity harness | FD-17 |
| DB-L12 | 12 | Threat model. Identity hardening | FD-18. BO-10 PROPOSED |
| DB-L13 | 13 | Recovery depth. Measured reliability | FD-19. Percents stay Unknown until measured |
| DB-L14 | 14 | Scorecard. ROI labels EDUCATIONAL | BO-11 PROPOSED |
| DB-L15 | 15 | 40-minute freeze. Brand restyle when assets arrive | FD-21. BO-12 PROPOSED |
| DB-L16 | 16 | As-built baseline | BO-13 PROPOSED |

---

## What this file does not do

This file does not write compose, CI, or application code. It does not start Half B. It does not sign a Business Owner row.
