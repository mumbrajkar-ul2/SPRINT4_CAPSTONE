# Implementation PRD

| Field | Value |
|---|---|
| Stage | Phase 8 / 17 Implementation PRD. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. UNSIGNED. BO-04 and other Business Owner rows stay PROPOSED. |
| Evidence sources | `docs/09-initial-prd/`; `docs/12-specs/`; `docs/10-architecture/adrs/adr-ports-and-compose.md`; `docs/10-architecture/security-architecture.md`; `docs/10-architecture/component-model.md`; `docs/13-traceability/coverage-gap-register.md`; `Execution_Plan.md` sections 4 and 10; `Decision_Tracker.md` FD-13, BO-02, BO-03, BO-04, BO-06b, BO-08; inherited `compose.yaml`; inherited `.github/workflows/verify.yml`; `app/server.py` via Phase 1 assessment |
| Assumptions | BO-02, BO-03, and BO-04 working answers hold and stay PROPOSED. Company job titles stay unmapped. Headline KPI values stay Unknown. Numeric SLO percents stay Unknown. |
| Unresolved issues | FD-13 stays DEFERRED until the coordinator records HALF_A_ACCEPTED. FD-14, FD-15, FD-16, FD-17, FD-18, FD-19, FD-21, and FD-23 stay later. INC-2025-014 follow-up owner stays Unknown. Signer names stay Unknown. |
| Residual risks | Treating this unsigned file as a signed gate would hide the deferred Business Owner signatures. Writing 50,000 or 999,999 as live policy would treat a PROPOSED row as code. Adding a ninth business problem would grow past BO-04. |

This file is the implementation product requirements document. It takes the Initial PRD and reconciles it with what the repository now holds. It names the platform that Phase 8 Half B will stand up. It does not write compose files, CI files, or application feature code.

---

## FD-13 recommended answer

**Authority:** team-force. **Status in the tracker:** DEFERRED until the coordinator records HALF_A_ACCEPTED.

**Recommended text.** The platform stack is Docker Compose at the capstone root, GitHub Actions at the capstone root, three request headers plus one environment variable for identity, structured JSON logs on stdout, and a `GET /health` route on every listener. One `docker compose up` starts seven named containers. The host ports are 8080 legacy, 8090 source gateway, 8091 lake REST, 8092 lake MCP, 8100 Application A, and 8110 Application B. Application A and Application B each serve their React screens from the same FastAPI process that serves `/api`. `MODEL_MODE=replay` plays back a file named by the SHA-256 hash of the prompt. The stack does not call the public network. There is no third offline mode. Identity scaffolding reads `FABPULSE_API_KEY` from the environment. The documented local default is `local-demo-only`. That value is written in `.env.example`. It is not written in application source. Application A and Application B require `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role` on every case read and every record-changing write. A missing or wrong set returns HTTP 401 with `error_class: missing_identity`. Health routes stay open. Ports 8080 and 8090 stay without an identity check so the current-system baseline remains visible. Lake REST and lake MCP require `X-Api-Key` on every route except health. CI runs tests, lake gates, `docker compose config`, and the identity 401 check. CI does not run `python -m app.generate --reset`. CI does not call a live model. Observability is JSON lines on stdout with `service`, `event`, `level`, and `correlation_id`. No extra identity server, metrics server, graph server, or policy container is added in Phase 8. Numeric latency, availability, recovery, and quality percents stay Unknown.

**Label.** Inference from the Phase 8 prompt, `Execution_Plan.md` section 10, `adr-ports-and-compose.md`, `docs/12-specs/error-handling-spec.md` EH-01, and the inherited compose and CI files. The numeric cells are Unknown.

After HALF_A_ACCEPTED, the coordinator may mark FD-13 DECIDED with this answer.

---

## Finding

**Finding.** The Initial PRD still names the right product. The repository now holds a locked four-port map, Phase 6 contracts, a generated lake at version 1.0.0, and 70 characterization tests. Identity format, Application A host port, and Application B host port were still Unknown. This file names those three items as engineering decisions.
**Evidence.** `docs/09-initial-prd/initial-prd.md`. `adr-ports-and-compose.md`. `docs/12-specs/api-contracts.md`. `docs/16-repo-validation/validation-signoff.md`. `Decision_Tracker.md` FD-13.
**Impact.** Half B can write compose, CI, identity scaffolding, lake listeners, and health stubs without inventing a product feature.
**Risk.** Copying the 8080 HTTP 200-without-identity path onto Application A would leave BP8 open.
**Confidence.** High on the product boundary and the four locked ports. High on the named host ports and header names as team-force decisions. Unknown on live compose on this laptop.
**Open questions.** Reviewer verdict. Coordinator record of FD-13. Live health output (Half B).

---

## What the Initial PRD still requires

**Verified Fact.** `docs/09-initial-prd/initial-prd.md`. BO-04 working answer.

The product is still two applications that run the same fab-exception workflow on business problems BP1 to BP8.

Application A reads rules from its rebuilt program. Application B reads rules only from the Context Lake. The Context Lake is the stored, versioned set of rules, evidence, and decisions.

Both applications run demo scenarios 7 to 11 with the same inputs. Scenario 12 is the Application B lineage view. Scenario 13 names each difference and traces it to a lake item.

A person approves every record-changing action. **Verified Fact** of the BO-03 working answer, still PROPOSED.

AI explains and proposes. Ranking, rule pass-or-fail, reconciliation, and intake de-duplication stay in code. Conflict explanation, natural-language answers, and draft plans may use a language model. Predicting `engineering_hold` stays rejected. **Verified Fact.** FD-04. FD-05. Majority and leave-one-out logistic regression are both 117/125. Honesty: REAL.

The 40-minute path in `Execution_Plan.md` section 10 remains the working demo flow. FD-21 still freezes that path in Phase 15.

No ninth business problem is added. No cycle-time target is set. No aged-backlog cutoff is set. No dollar benefit is claimed.

Worked example. 91 of 125 process steps have a `recipe_version` that differs from the joined tool `recipe_rev`. Honesty: REAL. Both applications must show both revisions. A Process Engineer at RT-03 approves a hold or a release. Phase 8 does not build that screen. Phase 8 only makes the later screen reachable on a named port with an identity.

---

## Repo findings that change the implementation plan

These are facts found after the Initial PRD. They do not add product features.

| Finding | Evidence | Label | What this PRD does with it |
|---|---|---|---|
| Inherited Compose starts three services: `legacy`, `source-gateway`, and `bridge` | Inherited `compose.yaml` | Verified Fact | Half B writes a new capstone-root Compose that keeps those three and adds lake and app listeners |
| Inherited host binds are 8080 and 8090 | Inherited `compose.yaml`. `environments/dev.env.example` | Verified Fact | Those two stays. 8091, 8092, 8100, and 8110 are added |
| Inherited CI runs `python -m app.generate --reset` then `python -m app.baseline` | Inherited `.github/workflows/verify.yml` | Verified Fact | Capstone CI omits `--reset`. A reset can replace the frozen packaged store |
| The current GET API has no identity check | Phase 1 `repo-assessment.md`. Characterization CT-35 | Verified Fact | 8080 stays open as the baseline. Application A and Application B reject a case read with no identity |
| Lake REST and lake MCP are not in inherited Compose | Phase 0 `high-level-architecture.md` | Verified Fact | Half B adds listeners on 8091 and 8092 |
| Lake version 1.0.0 exists with 148 items | Phase 6 `system-spec.md` | Verified Fact | Lake listeners read that generated file. They do not write it |
| Phase 7 recorded 70 characterization tests OK and two matching baseline runs | `docs/16-repo-validation/validation-signoff.md` | Verified Fact | Capstone CI reruns those tests. It does not treat Unknown headline KPIs as a fail |
| Application A and Application B folders do not exist yet | Workspace glob of `apps/` | Verified Fact | Half B writes health and identity stubs only. Feature routes stay for Phase 9 and Phase 11 |
| Identity header format was Unknown | `api-contracts.md`. EH-01. GAP-02 | Verified Fact of the gap | This file names the three headers and the environment variable |
| Application host ports were Unknown | `adr-ports-and-compose.md`. GAP-03 | Verified Fact of the gap | This file names 8100 and 8110 |

Worked example. Inherited CI runs `python -m app.generate --count 6000 --seed 4552 --reset`. That command can replace `data/legacy.sqlite3`. Capstone CI keeps the packaged file and runs the characterization suite on a copy.

---

## Invalidated assumptions

Every Initial PRD assumption that later files or this design change is listed here. Assumptions that still hold sit in the next section.

| ID | Earlier statement | Where it sat | What is true now | Label |
|---|---|---|---|---|
| IA-01 | Ports 8080, 8090, 8091, and 8092 stay later-phase facts | `initial-prd.md` Assumptions. `nfrs.md`. `non-goals.md` | Those four ports are locked. FD-06. `adr-ports-and-compose.md` | Verified Fact |
| IA-02 | Identity design stays later | `mvp-scope.md` Unresolved. FR-08. NFR identity row | Scaffolding is named in this file. Full role-permission threat model stays Phase 12 (FD-18) | Inference for the split. Verified Fact that FD-18 stays PENDING |
| IA-03 | Application A and Application B host ports stay Unknown | Ports ADR. `system-spec.md`. `api-contracts.md`. AC-MVP | Application A is 8100. Application B is 8110. Authority: team-force. ED-P8A-01 | Inference of the numbers. Verified Fact that the ADR left them open |
| IA-04 | Identity token or header format stays Unknown | `api-contracts.md`. EH-01. GAP-02 | Headers are `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role`. Authority: team-force. ED-P8A-02 | Inference of the names. Verified Fact of the 401 mapping |
| IA-05 | FD-07 lake item schema is later | FR-15. `target-architecture.md` | FD-07 DECIDED. Schema in `docs/11-data-context/knowledge-model.md` | Verified Fact |
| IA-06 | FD-09 stored region map is later | FR-06 | FD-09 DECIDED. Site code is canonical. 84 of 125 packaged cases disagree with the derived region and route to HOLD_FOR_REVIEW. Honesty: REAL | Verified Fact |
| IA-07 | FD-10 golden questions are later | FR-11 | FD-10 DECIDED. 26 golden questions | Verified Fact |
| IA-08 | FD-11 stays pending for contracts and SLOs | `nfrs.md` Unresolved | FD-11 DECIDED. HTTP and MCP contracts exist. Numeric percents stay Unknown | Verified Fact |
| IA-09 | FD-22 lake version policy is later | `target-architecture.md` Unresolved. `architecture-decision-summary.md` | FD-22 DECIDED. Lake version starts at 1.0.0 | Verified Fact |
| IA-10 | Lake item schema is later, so lineage cannot name a file | FR-15 Open questions | Lineage reads lake items already specified. Phase 8 still does not build the lineage screen | Verified Fact |
| IA-11 | Offline replay stays an assumption until Phase 15 | `nfrs.md` Operability | Half B wires `MODEL_MODE=replay` and the hash-of-prompt files. FD-21 still freezes the demo path in Phase 15 | Inference for the wiring date. Verified Fact that FD-21 stays PENDING |
| IA-12 | No Context Lake listener exists, and that is the whole picture | Phase 0 current-state note, carried as a later-phase fact in the Initial PRD | The lake file exists. Half B adds the 8091 and 8092 listeners | Verified Fact |

Worked example for IA-03. The ports ADR said Phase 8 assigns Application A and Application B. This file assigns 8100 and 8110. The speaker opens `http://127.0.0.1:8100` for Application A and `http://127.0.0.1:8110` for Application B.

---

## Assumptions that still hold

| Statement | Status | Label |
|---|---|---|
| BO-02, BO-03, and BO-04 working answers hold | PROPOSED. Accepted 2026-10-18. Not signed DECIDED | Verified Fact |
| Company job titles that match RT-01 to RT-06 stay Unknown | Still Unknown | Unknown |
| Exception cycle time stays Unknown | Still Unknown | Unknown |
| Aged backlog cutoff stays Unknown | Still Unknown | Unknown |
| Availability percent, API p95, retrieval p95, recovery time, recovery point, groundedness percent, citation percent, and abstention percent stay Unknown | Still Unknown. Inherited 99.5 percent is not adopted | Unknown |
| BO-06b keeps operational, finance, and audit closure as three states | PROPOSED | Verified Fact of the working answer |
| BO-08 silent threshold routes to HOLD_FOR_REVIEW. Demo 50,000 stays PROPOSED. Never use 999,999 as live policy | PROPOSED | Verified Fact of the working answer |
| INC-2025-014 follow-up owner stays empty until a person at RT-06 supplies a name | Unknown | Unknown |
| FD-14, FD-15, FD-16, FD-17, FD-18, FD-19, FD-21, FD-23 stay later | PENDING | Verified Fact |
| Packaged counts cited in the Initial PRD stay REAL | 125 cases, 89 not CLOSED, 2 urgent, 67 REPLAY, 91 recipe mismatches, 695 unassigned tasks | Verified Fact |

---

## Functional requirements disposition

Each Initial PRD requirement stays in force. Phase 8 implements none of the scenario screens.

| Requirement | Disposition | Phase that builds the feature | Phase 8 platform need |
|---|---|---|---|
| FR-01 Recipe mismatch | Unchanged | 9 and 11 | Port and identity so the later screen can require an actor |
| FR-02 Replay duplicate | Unchanged | 9 and 11 | Same |
| FR-03 Two clocks | Unchanged | 9 and 11 | Same |
| FR-04 Governed rule evaluation | Unchanged. Application B still reads only the lake | 9, 11, and lake listeners in 8 | 8091 and 8092 serve lake items |
| FR-05 Open and closed | Unchanged. REVIEW and HOLD stay open | 9 and 11 | None beyond the later apps |
| FR-06 Policy overlap | Unchanged. Wait for RT-04 | 9 and 11 | Same |
| FR-07 Untrusted text | Unchanged | 9, 11, and 12 | Replay and logs must not treat feed text as an order |
| FR-08 Identity, owner, recovery | Scaffolding in Phase 8. Owner assign and recovery screen stay later | 8 (identity), 9 and 11 (status and owner) | Headers, 401, documented key |
| FR-09 Queue ranking | Unchanged. Code on stored fields | 9 and 11 | None |
| FR-10 Cited explanation | Unchanged. Percent floor Unknown | 9 | Replay cache for saved sentences |
| FR-11 Cited natural-language answer | Unchanged. 26 golden questions already named | 9 | Replay cache |
| FR-12 Draft plan then wait | Unchanged. Recursion limit later (FD-15) | 10 | Replay cache. Checkpoint path later |
| FR-13 Person on every write | Unchanged. BO-03 stays PROPOSED | 10 | Identity headers on `POST /api/approvals` when that route is built |
| FR-14 Same-scenario run | Unchanged. Harness later (FD-17) | 11 | Two independent host ports |
| FR-15 Rule lineage | Unchanged. Application B only | 11 | Lake read on 8091 |

Worked example. FR-08 says a reader of a case has an identity. Phase 8 Half B returns 401 when Application A is called with no headers. Phase 9 still has to show the recipe fields on that case.

---

## Identity and auth approach (BP8)

**Finding.** The current GET API on 8080 returns cases with no actor. Application A and Application B must reject that path. Phase 8 adds scaffolding only.
**Evidence.** Catalogue BP8. CT-35. EH-01. API shared rules. GAP-02.
**Impact.** Minutes 0 to 8 can still show the open baseline on 8080. Minutes 13 to 25 show Application A only after an actor is sent.
**Risk.** Hard-coding the shared key in source would ignore the secrets rule. Adding Keycloak or a cloud login would need a public network.
**Confidence.** High on the gap and the 401 mapping. High on the header names as a team-force choice.
**Open questions.** FD-18 role-permission threat model. Company titles. How a real company would issue actor ids.

### What a request carries

Engineering decision ED-P8A-02, authority: team-force.

| Header | What it holds | Required on |
|---|---|---|
| `X-Api-Key` | The shared key from `FABPULSE_API_KEY` | Application A and Application B case reads and writes. Lake REST and lake MCP except health |
| `X-Actor-Id` | The person id for this request | Application A and Application B case reads and writes |
| `X-Actor-Role` | One of `RT-01`, `RT-02`, `RT-03`, `RT-04`, `RT-05`, `RT-06` | Application A and Application B case reads and writes |

Health routes do not require these headers.

A case read or write on Application A or Application B with a missing header, an empty header, or a key that does not match `FABPULSE_API_KEY` returns HTTP 401. The body uses `error_class: missing_identity`. No case body is returned. **Verified Fact** of the EH-01 mapping.

`POST /api/approvals` is a later feature. When Phase 10 builds it, `actor_id` must differ from `proposed_by`. A match returns HTTP 403 with `error_class: forbidden_role`. **Verified Fact.** BO-09. EH-02. Phase 8 does not build that route.

### Secret handling

Engineering decision ED-P8A-02 continued, authority: team-force.

| Item | Value |
|---|---|
| Environment variable | `FABPULSE_API_KEY` |
| Documented local default | `local-demo-only` |
| Where the default is written | `.env.example` at the capstone root. Compose may substitute that default when the variable is unset |
| Where the default is not written | Application source files. CI logs. The implementation PRD body as if it were a production secret |

The default is a local laptop value. It is not a company production key. Half B must not paste a different secret into source.

Worked example. Application A receives `GET /api/identity-check` with no headers. It returns 401 and `missing_identity`. The same route with `X-Api-Key: local-demo-only`, `X-Actor-Id: demo-rt01-1`, and `X-Actor-Role: RT-01` returns 200 and echoes the actor. It does not return a case body. Case bodies stay Phase 9.

### What stays ungated

Engineering decision ED-P8A-03, authority: team-force.

Port 8080 stays without an identity check. Characterization CT-35 records `GET /api/cases` as HTTP 200 with no identity header. That record is the current system. Application A does not replace port 8080.

Port 8090 stays without an identity check. Scenario 11 uses the inherited failure modes `timeout`, `schema`, and `rate_limit` as the outage fixture.

### Lake listeners

Engineering decision ED-P8A-04, authority: team-force.

Ports 8091 and 8092 require `X-Api-Key` on every route except health. They do not require actor headers. The lake is a read store. Actor duties apply on the application write path.

A lake write method stays rejected. POST, PUT, PATCH, or DELETE on 8091 returns 405 with `error_class: lake_write_rejected`. **Verified Fact.** `api-contracts.md`.

---

## Compose topology and ports

**Finding.** Section 10 requires one Compose command for the legacy API, the source gateway, lake REST, lake MCP, and both app UIs.
**Evidence.** `Execution_Plan.md` section 10. `adr-ports-and-compose.md`. Inherited `compose.yaml`.
**Impact.** Half B writes `compose.yaml` at the capstone root. The inherited workshop file stays as the three-service baseline.
**Risk.** Binding lake REST and lake MCP both to 8000 would clash. Replacing 8080 with Application A would hide the 0-to-8-minute current system.
**Confidence.** High on the six host ports. Unknown on live Docker on this laptop.
**Open questions.** Whether the Half B machine can run Compose. The reviewer marks NEEDS_HUMAN if the sandbox blocks the build.

### Host port map

Engineering decision ED-P8A-01, authority: team-force.

| Host port | Listener | Role in the demo | Identity |
|---|---|---|---|
| 8080 | Legacy API | Current-system baseline. Minutes 0 to 8 | None. Current behaviour |
| 8090 | Source gateway | Simulated upstream. Scenario 11 fixture | None. Inherited |
| 8091 | Lake REST | Screens read lake items | `X-Api-Key` except health |
| 8092 | Lake MCP | Agents read the same lake as tools. MCP is the Model Context Protocol | `X-Api-Key` except health |
| 8100 | Application A | FastAPI serves `/api` and the React screens | Three headers on case reads and writes |
| 8110 | Application B | FastAPI serves `/api` and the React screens, including the later lineage view | Three headers on case reads and writes |

Why 8100 and 8110. The locked set already uses 8080, 8090, 8091, and 8092. 8000 is the common FastAPI and MCP sample default, and two listeners would clash on it. 3000 is a common other-app default on a laptop. 8100 and 8110 sit in the same 81xx block, ten apart, so the speaker can remember two round numbers. FastAPI serves the React build from the same process so the demo has six host ports, matching the ADR count of two app UI listeners plus the four locked listeners.

Worked example. The speaker says: current system 8080, gateway 8090, lake 8091 and 8092, Application A 8100, Application B 8110.

### Containers Half B must name

Engineering decision ED-P8A-05, authority: team-force.

| Compose service | Container name | Host port | What Half B starts |
|---|---|---|---|
| `legacy` | `fabpulse-legacy` | 8080 | Inherited image and `/health` |
| `source-gateway` | `fabpulse-source-gateway` | 8090 | Inherited image and `/health` |
| `bridge` | `fabpulse-bridge` | none | Inherited one-shot seed. `restart: "no"` |
| `lake-rest` | `fabpulse-lake-rest` | 8091 | New listener on `context-lake.sqlite3`. Read only |
| `lake-mcp` | `fabpulse-lake-mcp` | 8092 | New MCP tools on the same file. Read only |
| `app-a` | `fabpulse-app-a` | 8100 | Health, identity probe, JSON logs. No scenario screens |
| `app-b` | `fabpulse-app-b` | 8110 | Same stub shape. No lineage screen yet |

The Compose network is internal. Containers talk to each other by service name. No container needs a public-network call when `MODEL_MODE=replay`.

`GET /health` on 8080, 8090, 8091, 8092, 8100, and 8110 returns HTTP 200 with `{ "ok": true }` when that listener is up.

The inherited bridge can write inbox rows on the named volume. Half B must point operational writes at a compose volume or a copy. The packaged `data/legacy.sqlite3` hash in `sources/register.yaml` must still match after the unit.

Seed the bundled lake file already generated as version 1.0.0. Half B does not rebuild the lake unless a test says the pin is missing.

---

## Replay-mode wiring

**Finding.** Section 10 already names the offline design. Half B wires that design. It does not invent a third mode.
**Evidence.** `Execution_Plan.md` section 10. Phase 8 locked fact `MODEL_MODE=replay`.
**Impact.** The laptop demo can start with the public network off. The audience is told when replay is on.
**Risk.** Inventing an Ollama path or a guessed model sentence would go past section 10.
**Confidence.** High on the rule. Unknown on how many saved files Phase 9 will add.
**Open questions.** Saved-file count stays Unknown until rehearsal writes them.

Engineering decision ED-P8A-08, authority: team-force.

| Item | Value |
|---|---|
| Environment variable | `MODEL_MODE` |
| Compose default | `replay` |
| Saved file directory | `operations/model-replay/` |
| File name | SHA-256 hex digest of the exact prompt bytes |
| File body | The saved model response from rehearsal |
| Missing file in replay | Structured error. No public-network call. No invented sentence |
| Live model | Phase 9, when a human supplies the API key. Not a Phase 8 Done test |

In rehearsal, each model response is saved under that hash. In replay, that saved response plays back. **Verified Fact.** `Execution_Plan.md` section 10.

Phase 8 Half B creates the directory, the environment wiring, and a small lookup helper. It does not fill a complete rehearsal cache. Phase 9 writes files when the human runs a live prompt.

A Done test that needs a live model, a running stack, or a network call pauses as `NEEDS_HUMAN`. Replay is a product feature. It is not a substitute for that human step. **Verified Fact.** `Execution_Plan.md` section 11.

---

## CI/CD steps

**Finding.** Inherited CI tests the workshop package and can reset generated data. Capstone CI must protect the freeze and the new listeners.
**Evidence.** Inherited `.github/workflows/verify.yml`. Phase 1 generate-reset gap. Phase 7 characterization suite.
**Impact.** Every push at the capstone root runs a safe check. Workshop `--reset` stays inside the inherited workflow only.
**Risk.** Running `--reset` on the packaged store would void the Phase 0 and Phase 7 signoff.
**Confidence.** High on the omitted reset. Unknown on GitHub runner availability in the sandbox.
**Open questions.** Whether Half B can run Actions locally with `act`, or only `docker compose config` plus pytest.

Engineering decision ED-P8A-06, authority: team-force.

Capstone workflow path: `.github/workflows/verify.yml` at the capstone root. Trigger: push and pull_request.

| Step | What it does |
|---|---|
| Checkout | Reads the capstone tree |
| Python 3.12 | Matches the inherited workflow |
| Characterization tests | Rerun the Phase 7 suite on a copy. Packaged hashes must still match `sources/register.yaml` |
| Lake tests | Rerun `context-lake` gates and golden-question checks already in that tree |
| Identity scaffolding test | Application A and Application B identity probe without headers returns 401. With the three headers it returns 200 |
| Replay lookup test | A known prompt hash returns the saved file. A missing hash returns the structured error and does not open a network socket |
| Compose config | `docker compose config` on the capstone file. Checks that 8080, 8090, 8091, 8092, 8100, and 8110 are published |
| Omitted | `python -m app.generate --reset`. Live Azure or OpenAI calls. App feature scenario tests |

The inherited workshop workflow is left in place as a record of the current package. Capstone CI does not invoke it.

---

## Observability signals

**Finding.** Each service must emit telemetry so a later reliability phase can measure. This phase does not set a latency percent.
**Evidence.** Phase 8 prompt. `docs/09-initial-prd/nfrs.md`. FD-11 numeric cells Unknown. FD-19 later.
**Impact.** Half B can prove a service is up from logs and `/health` without inventing a p95.
**Risk.** Adding Prometheus or a cloud exporter would add a service the laptop demo does not need and would call a network.
**Confidence.** High on stdout logs and health. Unknown on later numeric floors.
**Open questions.** FD-19 alert thresholds. FD-23 audit columns.

Engineering decision ED-P8A-07, authority: team-force.

Each of the six listeners writes one JSON object per line to stdout.

| Field | What it holds |
|---|---|
| `timestamp` | ISO-8601 time of the line |
| `service` | `legacy`, `source-gateway`, `lake-rest`, `lake-mcp`, `app-a`, or `app-b` |
| `level` | `info`, `warn`, or `error` |
| `event` | A short name such as `health_ok`, `identity_missing`, `replay_hit`, `replay_miss` |
| `correlation_id` | Present when the request sent one. Minting rules stay FD-23 |
| `actor_id` | Present on Application A and Application B when the header was accepted |
| `path` | The HTTP path or the MCP tool name |
| `status` | HTTP status when the event is a request |
| `duration_ms` | Elapsed milliseconds for that request. This is a measured log field. It is not a target |

`GET /health` on each host port is the liveness signal. Compose healthchecks call that path.

No extra collector container is added in Phase 8. Compose already shows stdout. Phase 13 may add more signals under FD-19.

Audit-chain rows are still one row per agent step and per human approval. The column list stays Phase 10 (FD-23). JSON request logs are not that audit chain.

---

## Data seams

Lake YAML in Git remains the source of truth. `build.py` writes `context-lake/generated/context-lake.sqlite3`. Lake REST and lake MCP open that file read-only.

Application A may read the lake for citations. Application A still evaluates pass or fail from transformed code.

Application B reads rules only from the lake.

Application A does not call Application B at run time. Application B does not call Application A at run time.

The operational store remains the packaged SQLite used by the legacy API and later by Application A writes that a person approved. Phase 8 does not add a new operational database.

---

## What this file does not do

This file does not write `compose.yaml`. It does not write CI YAML. It does not write application feature code. It does not start Half B. It does not sign BO-02, BO-03, BO-04, BO-06b, BO-08, BO-10, BO-11, BO-12, or BO-13. It does not invent a cycle-time number, an aged-backlog cutoff, an availability percent, or a dollar benefit. It does not mark FD-13 DECIDED. It does not update `Decision_Tracker.md` or `STATUS.md`.
