# Access-control implementation

| Field | Value |
|---|---|
| Stage | Phase 9 / 20 Application and services. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p9a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `Decision_Tracker.md` FD-13, BO-09, Group C; `docs/12-specs/business-rules.md`; `docs/12-specs/error-handling-spec.md` EH-01 to EH-03; `docs/17-implementation-prd/implementation-prd.md` identity section; `apps/shared/identity.py` |
| Assumptions | `FABPULSE_API_KEY` local default remains `local-demo-only` in `.env.example`. Company job titles stay Unknown. Full threat model stays Phase 12 (FD-18). |
| Unresolved issues | How a real company issues actor ids stays Unknown. Named people stay Unknown. INC-2025-014 owner stays Unknown until RT-06. |
| Residual risks | Copying the 8080 HTTP 200-without-identity path onto 8100 would leave BP8 open. Allowing the model to send approval headers would skip BO-09. |

This file names how Application A on port 8100 checks identity and role for scenarios 7 to 11. Phase 8 already rejects a missing key. Half B adds role matching on writes.

Engineering decision ED-P9A-07, authority: team-force. Role enum, read versus write checks, and demo actors.

---

## Finding

**Finding.** Phase 8 checks that three headers exist and that `X-Api-Key` matches `FABPULSE_API_KEY`. It does not check that `X-Actor-Role` is one of RT-01 to RT-06, and it does not match role to action type. Half B must add those checks on Application A feature routes.
**Evidence.** `apps/shared/identity.py` `check_app_identity`. EH-01, EH-02, EH-03. Group C.
**Impact.** Scenario 8 rejects RT-05 on a recipe hold. Scenario 7 rejects RT-03 on a replay drop.
**Risk.** A generic admin role would skip the map. This design does not add an admin role.
**Confidence.** High on the SME map. Unknown on company titles.
**Open questions.** FD-18 threat model. Company title confirmation.

---

## Headers (already decided)

**Verified Fact.** FD-13. ED-P8A-02.

| Header | Holds | Required on |
|---|---|---|
| `X-Api-Key` | Shared key from `FABPULSE_API_KEY` | Every `/api` route except `/health` |
| `X-Actor-Id` | Person id for this request | Same |
| `X-Actor-Role` | `RT-01` to `RT-06` | Same |

Optional `X-Correlation-Id` joins audit rows. Minting rules stay Phase 10. If the header is missing, Application A mints a request-scoped id for logs. That minting format is an engineering default. The FD-23 column list stays later.

Health stays open. Static UI GET stays open. Port 8080 stays ungated as the baseline. Port 8090 stays ungated as the fixture.

Lake REST needs `X-Api-Key` only. Application A supplies that key when it retrieves citations. Actor duties apply on Application A writes, not on the lake read.

---

## Closed role list

Engineering decision ED-P9A-07, authority: team-force.

`X-Actor-Role` must be exactly one of `RT-01`, `RT-02`, `RT-03`, `RT-04`, `RT-05`, `RT-06`. Any other string is HTTP 401 or 403 with `error_class: missing_identity` if empty, or `error_class: forbidden_role` if present and unknown.

Phase 8 today accepts any non-empty role string. Half B tightens this on Application A.

---

## Reads versus writes

| Action | Who may call | Fail |
|---|---|---|
| `GET /api/queue` | Any of RT-01 to RT-06 with a valid key | 401 if headers missing |
| `GET /api/cases/{id}` | Any of RT-01 to RT-06 | 401. No case body |
| `POST /api/query` | Any of RT-01 to RT-06 | 401. Query is a read of knowledge, not a record write |
| `GET /api/recovery` | Any of RT-01 to RT-06 | 401 |
| `POST /api/approvals` | Only the role mapped to `action_type` | 403 `forbidden_role` |
| Model calling `POST /api/approvals` | Nobody. No write tool | Rejected before HTTP if a tool is attempted. If a request arrives with `X-Actor-Role` set to a model string, 403 |

Worked example. `POST /api/query` with RT-01 can ask GQ-01. That is a read. It does not change a case.

---

## Write map (Group C)

**Verified Fact.** `business-rules.md`. Lake items in the last column.

| `action_type` | Allowed `X-Actor-Role` | Forbidden | Lake item |
|---|---|---|---|
| `dispose` | RT-01 | Model. Same person as `proposed_by` | `term.approval` |
| `approve_agent` | RT-02 | Proposing agent. Same person as `proposed_by` | `rule.hold.person_only` |
| `recipe_hold_or_release` | RT-03 | RT-05 acting alone. Model | `rule.recipe.mismatch_show_both` |
| `policy_pick` | RT-04 | Model | `rule.policy.overlap_or_invalid` |
| `replay_confirm` | RT-05 | Unattended job. Model | `rule.feed.replay_duplicate` |
| `assign_owner` | RT-06 | Invented name. Model | `decision.inc_2025_014` |

`actor_id` must differ from `proposed_by`. BO-09. HTTP 403 `forbidden_role` on a match. Record unchanged.

When `block` is true, Application A does not offer the approval control. HTTP 409 `error_class: blocked` if a write is still attempted.

When the case waits, a wrong-role write is 403. A right-role write still records EV-09.

---

## Exception mapping Half B implements

**Verified Fact** of EH families. Host is 8100.

| Case | HTTP | `error_class` | User-visible |
|---|---|---|---|
| Missing or wrong key, missing actor, missing role | 401 | `missing_identity` | No case body |
| Unknown role string, role/action mismatch, actor equals proposer | 403 | `forbidden_role` | Record unchanged |
| HOLD_FOR_REVIEW on a write | 409 | `wait_for_person` | `waiting_role` set |
| Injection stop | 409 | `blocked` | Quote in `untrusted_quotes`. No approve button |
| Query abstain | 200 | none, `verdict: ABSTAIN` | Abstain banner |
| Gateway timeout, schema, rate_limit | 503 on the failing upstream call. Recovery GET stays 200 | `upstream_timeout`, `upstream_schema`, `upstream_rate_limit` | Retry status |
| Replay miss | 200 query with abstain | log `replay_miss` | No guessed sentence |

Worked example. `GET /api/cases/CASE-1` on 8100 with no headers is HTTP 401 `missing_identity`. Honesty of that Phase 8 probe: REAL. Feature case bodies still wait for Half B.

---

## Demo actors

These are laptop identities. They are not company staff. Company titles stay Unknown.

| `X-Actor-Id` | `X-Actor-Role` | Scenario write they may record |
|---|---|---|
| `demo-rt01-1` | RT-01 | dispose |
| `demo-rt02-1` | RT-02 | approve_agent (Phase 10 write; Phase 9 draft only) |
| `demo-rt03-1` | RT-03 | Scenario 8 hold or release |
| `demo-rt04-1` | RT-04 | Scenario 10 policy pick |
| `demo-rt05-1` | RT-05 | Scenario 7 replay confirm |
| `demo-rt06-1` | RT-06 | Scenario 11 owner assign |

The role picker must not put the same actor id into `proposed_by` and `actor_id` on one approval. Use `demo-rt02-1` as a typical `proposed_by` for a draft, and a different demo actor as the approver.

---

## Untrusted text and identity

Harvested notes do not grant a role. A feed that says auto approve does not become RT-01. Identity stays the three headers. The note stays `untrusted_quotes`.

---

## What this file does not do

This file does not add Keycloak. It does not sign company titles. It does not start Half B. Threat model remains FD-18.
