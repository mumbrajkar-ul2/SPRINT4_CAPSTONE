# Application A component map

| Field | Value |
|---|---|
| Stage | Phase 9 / 20 Application and services. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p9a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No Application A feature code in this half. |
| Evidence sources | `docs/12-specs/api-contracts.md`; `docs/12-specs/schema-specifications.md`; `docs/10-architecture/component-model.md`; `docs/15-modernization/changed-components.md`; `apps/app_a/server.py`; FD-13; FD-04 |
| Assumptions | Port 8100 already serves health and the identity probe. FastAPI will serve the React screens from the same process. Application A does not call Application B. |
| Unresolved issues | Exact packaged `case_id` values for scenario fixtures stay for Half B to bind. Audit column list stays Phase 10 (FD-23). LangGraph checkpoint path stays Phase 10 (FD-15). Company job titles stay Unknown. |
| Residual risks | Importing lake items as the pass-or-fail engine would make Application A a copy of Application B. Serving the UI only after identity headers would block the first page load in a browser. |

This file names the Application A pieces Half B will build on port 8100. It names who talks to whom. It does not write those modules.

Engineering decision ED-P9A-06, authority: team-force. Module paths, static UI identity exception, and the transformed-code import path below.

---

## Finding

**Finding.** Application A is one FastAPI process on host port 8100. It already has health and identity scaffolding. Half B adds queue, case, query, recovery, person-approval, retrieval, and generation modules, plus screens that call those routes.
**Evidence.** `apps/app_a/server.py`. Compose publishes 8100. API-Q-01 to API-Q-07. Phase 8 stubs omit scenario screens.
**Impact.** Half B extends `apps/app_a/` without starting a second Application A port.
**Risk.** Putting ranking inside the generation module would send queue order through a model.
**Confidence.** High on the route list. Unknown on packaged fixture ids.
**Open questions.** Fixture `case_id` values. React folder layout details inside `apps/app_a/ui/`.

---

## Process and listeners

**Verified Fact.** FD-13. ED-P8A-01.

| Piece | Bind | What it does |
|---|---|---|
| Application A | Host 8100 | `/api` and the React screens |
| Lake REST | Host 8091 | Citations. Application A is a client with `X-Api-Key` |
| Source gateway | Host 8090 | Scenario 11 failure fixture. No identity on 8090 |
| Legacy API | Host 8080 | Baseline only. Application A does not replace it |
| Lake MCP | Host 8092 | Phase 10 agents. Phase 9 retrieval uses REST |

Application A does not listen on 8110. Application B is out of this phase.

---

## Half B module map

Engineering decision ED-P9A-06, authority: team-force.

Paths are under the capstone root. Half B may split a file. It may not drop a row's responsibility.

| Path | Responsibility |
|---|---|
| `apps/app_a/server.py` | FastAPI app. Mounts routes and static UI |
| `apps/shared/identity.py` | Existing header check. Half B adds role enum and role-to-action match |
| `apps/app_a/routes/queue.py` | `GET /api/queue`. Calls transformed `priority()`. No model |
| `apps/app_a/routes/cases.py` | `GET /api/cases/{id}`. SCH-06 body |
| `apps/app_a/routes/query.py` | `POST /api/query`. Retrieval then generation |
| `apps/app_a/routes/recovery.py` | `GET /api/recovery`. Gateway status |
| `apps/app_a/routes/approvals.py` | `POST /api/approvals`. Person only |
| `apps/app_a/rules/adapter.py` | Imports Phase 7 functions from the inherited tree |
| `apps/app_a/intelligence/retrieve.py` | Lake REST client |
| `apps/app_a/intelligence/generate.py` | Replay or later Azure. Canonical hash |
| `apps/app_a/intelligence/ground.py` | FD-14 rule plus `check_claim` |
| `apps/app_a/prompts/` | Versioned JSON from the registry. Written in Half B |
| `apps/app_a/ui/` | React screens served by FastAPI |

Worked example. `GET /api/queue` with headers `X-Api-Key`, `X-Actor-Id: demo-rt01-1`, `X-Actor-Role: RT-01` returns ordered summaries. Order comes from `priority()`. The generation module is not imported on that path.

---

## Transformed-code adapter

**Verified Fact.** Phase 7 changed components. Application A takes rules from its own transformed code.

Engineering decision ED-P9A-06 continued. The adapter imports these names from `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`:

| Function | File | Application A use |
|---|---|---|
| `priority` | `app/legacy_logic.py` | Queue ranking |
| `evaluate_live_policy` | `app/legacy_logic.py` | Archive match or HOLD_FOR_REVIEW |
| `intake_apply` | `app/gateway_bridge.py` | Intake accept / reject |
| `reconcile_feeds` | `app/partner_feeds.py` | Duplicate candidate from REPLAY and key tests |

The adapter does not import lake YAML as a rule table. The adapter does not copy JavaScript `1.05` or `999999` as live policy.

`GET /api/cases` on port 8080 still calls `priority()`. Application A on 8100 also calls `priority()` for ranking. Live-policy questions on 8100 call `evaluate_live_policy`.

Worked example. `evaluate_live_policy('APAC', 2026)` returned limit 25,000 USD in Phase 7. Honesty: REAL. Application A uses that function. It may still retrieve `rule.recipe_release.limit.v2026.apac` for the citation on a query.

---

## HTTP routes Half B implements

**Verified Fact** of the contracts. Host port is now 8100.

| Route | Identity | Model | Person write |
|---|---|---|---|
| `GET /health` | No | No | No |
| `GET /` and `GET /assets/*` | No. Page must load | No | No |
| `GET /api/identity-check` | Yes | No | No |
| `GET /api/queue` | Yes | No | No |
| `GET /api/cases/{id}` | Yes | Optional explanation field from generate | No |
| `POST /api/query` | Yes | Yes | No |
| `GET /api/recovery` | Yes | Optional cited status sentence | No |
| `POST /api/approvals` | Yes, role must match action | No. Person route only | Yes |
| `GET /api/audit/{correlation_id}` | Yes | No | No. Schema later; Half B may return a stub list of known event types without inventing FD-23 columns |

`GET /api/lineage/{item_id}` stays Application B.

Engineering decision ED-P9A-06: static UI GET paths stay open so the browser can load HTML and JavaScript. Every `/api` path except `/health` requires the three identity headers. The landing page offers a role picker that sets `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role` on later `/api` calls.

Documented demo actors (not company people):

| Actor id | Role |
|---|---|
| `demo-rt01-1` | RT-01 |
| `demo-rt02-1` | RT-02 |
| `demo-rt03-1` | RT-03 |
| `demo-rt04-1` | RT-04 |
| `demo-rt05-1` | RT-05 |
| `demo-rt06-1` | RT-06 |

Company job titles stay Unknown. These ids are laptop demo values.

---

## Screens (design only)

Half B builds these React views. This half does not write UI code.

| Screen | User finishes | Bound |
|---|---|---|
| Role picker | Chooses an RT role and demo actor | Headers on later calls |
| Queue | Sees the next cases in `priority()` order | No model rank. Untrusted notes not used to rank |
| Case detail | Sees both conflict values, citations, wait role | Model sentence optional |
| Query | Asks in words, sees SCH-09 | Abstain banner when verdict is ABSTAIN |
| Recovery | Sees retry and error class | No 8-hour claim |
| Approval | Records the matching action | Hidden when role mismatches or `block` is true |

Worked example. RT-05 opens a REPLAY case. The approval control offers `replay_confirm`. It does not offer `recipe_hold_or_release`.

---

## Events Application A writes

**Verified Fact.** Event contracts EV-01 to EV-12. Column list later (FD-23).

Phase 9 writes the event types the scenarios need, using the shared envelope fields already named. Full audit-chain schema stays Phase 10. Half B must still emit the type, `correlation_id`, `actor_id`, `actor_role`, `case_id`, `app: app_a`, and `lake_item_ids`.

Scenario mapping is in `application-readiness.md`.

---

## What this file does not do

This file does not write route handlers. It does not write React. It does not start Half B. It does not build Application B.
