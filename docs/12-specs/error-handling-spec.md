# Error-handling specification

| Field | Value |
|---|---|
| Stage | Phase 6 / 12 Spec-driven design |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. FD-11 recommended. HTTP mapping is an engineering decision. Numeric retry budgets stay Unknown. |
| Evidence sources | `docs/09-initial-prd/functional-requirements.md`; `docs/10-architecture/adrs/adr-opa-gates.md`; `docs/11-data-context/data-contracts.md`; lake items listed per family. Confirmed in `context-lake.sqlite3` on 2026-10-18. |
| Assumptions | OPA three verdicts stay EXECUTE, HOLD_FOR_REVIEW, BLOCK. Lake envelope verdicts stay ANSWER, ABSTAIN, HOLD_FOR_REVIEW, plus `block: true`. BO-03 working answer still sends every record-changing write through a person. |
| Unresolved issues | Identity token format stays Unknown. Retry count and backoff milliseconds stay Unknown (FD-19). Audit column list stays Unknown (FD-23). OPA rule bodies stay Unknown (FD-16). |
| Residual risks | Mapping HOLD_FOR_REVIEW to HTTP 200 without a wait flag would look like a completed write. Mapping BLOCK to a silent 200 would hide the injection stop. Inventing a retry-count number would invent an SLO. |

This file names how errors, waits, and stops are returned. It maps domain verdicts to HTTP for Application A, Application B, and the lake. It does not invent a latency target.

Engineering decision ED-P6-05, authority: team-force. HTTP status mapping in the table below. Domain verdict strings stay as already locked.

---

## Finding

**Finding.** Five error families cover this product: identity, not-found, validation, wait-for-person, and stop. Lake reads add abstain. Recovery adds a user-visible retry class without a numeric budget.
**Evidence.** `decision.bp8.auth_and_owner`, `rule.hold.person_only`, `rule.untrusted_text.block`, `rule.threshold.silent`, `term.outage`, `arch.listener.legacy_8080`.
**Impact.** Clients can tell a completed write from a wait from a block. Scenario 11 can show a status without claiming an 8-hour recovery.
**Risk.** Copying the 8080 HTTP 200-without-identity behaviour onto Application A would leave BP8 open.
**Confidence.** High on the families. Unknown on retry counts and token format.
**Open questions.** FD-13 identity format. FD-16 Rego. FD-19 retry budget.

---

## Domain verdicts (already locked)

These strings are the product language. HTTP is a wrapper around them.

| Source | Verdict | What the application does | Lake item |
|---|---|---|---|
| OPA | EXECUTE | The next code step may run. A record-changing action still waits on the person | `rule.hold.person_only` |
| OPA | HOLD_FOR_REVIEW | The case waits for RT-01 to RT-06 | `term.approval` |
| OPA | BLOCK | The action stops. The case is unchanged | `rule.untrusted_text.block` |
| Lake envelope | ANSWER | Items support the question | `arch.lake.yaml_sqlite` |
| Lake envelope | ABSTAIN | No accepted item supports the question | `data.missing.lot_genealogy` (worked case: parent lot) |
| Lake envelope | HOLD_FOR_REVIEW | Unresolved authority, overlap, silence, or mapping disagreement | `rule.threshold.silent`, `rule.policy.overlap_or_invalid`, `rule.region.disagreement` |
| Lake envelope | `block: true` | Injection path. Approve, release, ignore-validation, or close-from-text stops | `rule.untrusted_text.block` |

Worked example. A partner note says auto approve. OPA returns BLOCK. Envelope `block` is true. HTTP mapping below returns 409 with `error_class: blocked`. No approval resource is offered.

Worked example. Archive silent on urgent cutoff. Envelope verdict is HOLD_FOR_REVIEW. HTTP mapping returns 409 with `error_class: wait_for_person`. Live policy does not insert 50,000. Lake item `rule.threshold.silent`. BO-08 stays PROPOSED.

---

## HTTP mapping for Application A, Application B, and lake REST

**Verified Fact** of the need. **Inference** of the status numbers, authority: team-force.

Every error body includes: `ok: false`, `error_class`, `message` in plain speech, `correlation_id` when one exists, `waiting_role` when waiting, `lake_item_ids` cited.

| error_class | HTTP | When | Lake item |
|---|---|---|---|
| `missing_identity` | 401 | Application A or Application B case read or write with no actor | `decision.bp8.auth_and_owner` |
| `forbidden_role` | 403 | Actor role does not match the action type, or actor equals proposer | `term.approval` |
| `not_found` | 404 | Unknown case id, unknown lake item id, unknown correlation id | `arch.lake.yaml_sqlite` |
| `invalid_request` | 400 | Missing required field, extra property, eighth `kind`, unknown `action_type` | item schema extra-properties false |
| `wait_for_person` | 409 | HOLD_FOR_REVIEW. Record unchanged | `rule.hold.person_only` |
| `blocked` | 409 | OPA BLOCK or envelope `block: true`. Record unchanged | `rule.untrusted_text.block` |
| `abstain` | 200 | Lake or query has no supporting item. `verdict: ABSTAIN`. This is a successful empty answer, not a crash | `data.missing.lot_genealogy` |
| `upstream_timeout` | 503 | Gateway failure mode `timeout`. Recovery status is visible | `arch.listener.gateway_8090`, `term.outage` |
| `upstream_schema` | 503 | Gateway failure mode `schema` | `arch.listener.gateway_8090` |
| `upstream_rate_limit` | 503 | Gateway failure mode `rate_limit` | `arch.listener.gateway_8090` |
| `lake_write_rejected` | 405 | POST, PUT, PATCH, or DELETE on port 8091 | `arch.lake.yaml_sqlite` |

409 is used for wait and block so a client does not treat the write as stored. 200 with `verdict: ABSTAIN` is used when the read worked and the knowledge is missing.

Health routes stay 200 when the listener is up. They do not require identity.

The inherited 8080 API today returns 200 on `GET /api/cases` with no identity. Characterization check CT-35 records that fact. Application A and Application B do not copy that behaviour.

---

## EH-01 Identity missing

| Field | Value |
|---|---|
| Finding | The current GET API on 8080 has no identity check. Application A and Application B require an identity on case read and write. |
| Evidence | `arch.listener.legacy_8080`, `decision.bp8.auth_and_owner` |
| Impact | Anyone who can reach 8080 can read cases today. The new apps reject that path. |
| Risk | Inventing a token format here would skip FD-13. |
| Confidence | High on the gap. Unknown on the format. |
| Open questions | Header name, cookie, or bearer token. Owner: Team-Force at FD-13. |
| Behaviour | `error_class: missing_identity`. HTTP 401. No case body. |

---

## EH-02 Separation of duties

| Field | Value |
|---|---|
| Finding | The proposer of an action is never its approver. |
| Evidence | BO-09. `term.approval` |
| Impact | `POST /api/approvals` with `actor_id == proposed_by` is rejected. |
| Risk | One login used for draft and approve would skip Group C. |
| Confidence | High |
| Open questions | Company titles Unknown. |
| Behaviour | `error_class: forbidden_role`. HTTP 403. Record unchanged. |

---

## EH-03 Role mismatch

| Field | Value |
|---|---|
| Finding | Each action type has one SME role. |
| Evidence | Group C. `rule.recipe.mismatch_show_both`, `rule.feed.replay_duplicate`, `rule.policy.overlap_or_invalid`, `decision.inc_2025_014` |
| Impact | RT-05 cannot record a recipe hold. RT-03 cannot drop a replay. |
| Risk | A generic admin role would skip the map. This spec does not add an admin role. |
| Confidence | High |
| Open questions | Title confirmation. |
| Behaviour | `error_class: forbidden_role`. HTTP 403. |

---

## EH-04 Wait for person

| Field | Value |
|---|---|
| Finding | Overlap, silence, unsigned policy, and model-proposed writes wait. |
| Evidence | `rule.policy.overlap_or_invalid`, `rule.threshold.silent`, `rule.open_closed.finance_audit`, `rule.hold.person_only` |
| Impact | The client sees `waiting_role` and a correlation id. LangGraph `interrupt()` holds the graph. |
| Risk | Treating 409 as a retry-until-success loop would spam the person. |
| Confidence | High |
| Open questions | Recursion-limit number (FD-15). |
| Behaviour | `error_class: wait_for_person`. HTTP 409. Event EV-07 and then EV-08 interrupt. |

BO-06b and BO-08 stay PROPOSED. Those waits use this family. They do not compile a number into the error body as a decided limit.

---

## EH-05 Injection stop

| Field | Value |
|---|---|
| Finding | 86 partner feeds, 150 bundled events, 3 emails, and 22 source documents carry approve-or-ignore text. Honesty: REAL. The path returns BLOCK. |
| Evidence | `rule.untrusted_text.block`, `data.injection.partner_feeds`, `decision.bp7.untrusted_text` |
| Impact | Minutes 36 to 39. No approval is offered. |
| Risk | Returning 200 with a draft approve button would leak the instruction into a write. |
| Confidence | High |
| Open questions | None for the 86 count. |
| Behaviour | `error_class: blocked`. HTTP 409. Envelope `block: true`. Event EV-12. |

---

## EH-06 Abstain

| Field | Value |
|---|---|
| Finding | If retrieval returns nothing, the model abstains. Parent-lot questions abstain because the column does not exist. INC-2025-014 owner questions abstain until a person assigns one. |
| Evidence | `data.missing.lot_genealogy`, `decision.inc_2025_014` |
| Impact | FR-10 and FR-11 stay honest. |
| Risk | Inventing a parent lot or an incident owner would hide Unknown. |
| Confidence | High |
| Open questions | Citation percent floor (FD-14). |
| Behaviour | HTTP 200. `verdict: ABSTAIN`. Empty sentence allowed. Citations may name the missing-data item. |

---

## EH-07 Upstream recovery

| Field | Value |
|---|---|
| Finding | Scenario 11 shows retry and a user-visible status after an outage or schema mismatch. |
| Evidence | `term.outage`, `arch.listener.gateway_8090`, `decision.bp8.auth_and_owner` |
| Impact | `GET /api/recovery` stays readable. HTTP 503 on the failing call. |
| Risk | Copying an 8-hour recovery-time target would invent an SLO. |
| Confidence | High on the need. Unknown on retry count. |
| Open questions | Retry count, backoff, DLQ design (FD-19). |
| Behaviour | `error_class` one of `upstream_timeout`, `upstream_schema`, `upstream_rate_limit`. HTTP 503. Event EV-11. Retry count is Unknown. |

---

## EH-08 Lake write rejected

| Field | Value |
|---|---|
| Finding | Only `build.py` writes `context-lake.sqlite3`. |
| Evidence | `arch.lake.yaml_sqlite`, `decision.fd22.lake_version_policy` |
| Impact | A POST to 8091 does not change items. |
| Risk | A convenience write API would skip Git review. |
| Confidence | High |
| Open questions | None |
| Behaviour | `error_class: lake_write_rejected`. HTTP 405. |

---

## EH-09 Validation

| Field | Value |
|---|---|
| Finding | JSON Schema extra properties are false. Closed enums reject unknown values. |
| Evidence | `arch.lake.yaml_sqlite`. Item and envelope schemas. |
| Impact | An eighth `kind` or a ninth link type fails. |
| Risk | A lenient parser would let `parent_lot_id` through. |
| Confidence | High |
| Open questions | None |
| Behaviour | `error_class: invalid_request`. HTTP 400. |

---

## EH-10 Baseline 8080 does not use these mappings

| Field | Value |
|---|---|
| Finding | Port 8080 stays the current system. It has no identity check. |
| Evidence | `arch.listener.legacy_8080` |
| Impact | Demo minutes 0 to 8 still show the current API. Minutes 13 to 25 show Application A with identity. |
| Risk | Calling 8080 a secured API would hide BP8. |
| Confidence | High |
| Open questions | None for the current handler |
| Behaviour | CT-35 remains the characterization of today. It is not the Application A contract. |

---

## What this file does not do

This file does not invent a retry-count number, a backoff millisecond, or an availability percent. It does not write OPA Rego. It does not design the identity token. It does not start Phase 7.
