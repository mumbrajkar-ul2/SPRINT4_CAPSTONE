# Fallback matrix

| Field | Value |
|---|---|
| Stage | Phase 13 / 28 Reliability and resilience. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-28a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No fallback code in this half. |
| Evidence sources | FD-19; FD-13; FD-14; FD-15; FD-04; `operations/replay_lookup.py`; `apps/app_a/intelligence/generate.py`; `apps/app_a/agent/opa_client.py`; `apps/app_a/routes/recovery.py`; `docs/19-intelligence/model-configuration.md`; `docs/21-integration/failure-semantics.md` |
| Assumptions | `MODEL_MODE=replay`. There is no third offline mode. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Live Azure fallback behaviour stays Unknown. Measured HB-28-01 cells stay Unknown. |
| Residual risks | Calling Azure after a replay miss would open a public-network socket. Returning HOLD_FOR_REVIEW after OPA BLOCK would offer an approval on injection. |

This file names, for each failure, the next step Application A already takes or will take after SC-28-01. Each next step stays inside the current product. This half adds no second model vendor.

---

## Finding

**Finding.** Six next steps already exist: replay files, abstain, visible recovery, local OPA evaluate, checkpoint resume, and HTTP 409 BLOCK. SC-28-01 adds park-and-replay for invalid intake. Azure stays a later live path. Ollama is not a product mode.
**Evidence.** FD-13. FD-19. `replay_lookup.py`. `local_evaluate` in `opa_client.py`. SqliteSaver path. OPA three verdicts. `WRITE_TOOLS` is `[]`.
**Impact.** Half B implements park-and-replay only. Other rows stay as built.
**Risk.** Naming Ollama as a backup would add a third mode.
**Confidence.** High on the existing paths. Unknown on measured park rows.
**Open questions.** HALF_A_ACCEPTED.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. A failed intake stays visible.

**Verified Fact.** FD-13. Modes are `replay` and `azure`. Compose default is `replay`. No third offline mode.

**Verified Fact.** Injection still BLOCKS. The model has no write tool.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

---

## Matrix

| Trigger | Next step | HTTP / body | Writes a record | Label |
|---|---|---|---|---|
| Live Azure off, `MODEL_MODE=replay`, file present | Read `operations/model-replay/{sha256}` | 200 with the saved sentence after `check_claim` | No, unless a person later approves | Verified Fact |
| Replay file missing | Abstain. `error_class: replay_miss`. Do not call Azure | 200 `verdict: ABSTAIN` on the query path | No | Verified Fact |
| `MODEL_MODE` is neither `replay` nor `azure` | `error_class: replay_required`. Abstain | 200 abstain | No | Verified Fact of `generate.py` |
| Azure variables missing while mode is `azure` | `error_class: missing_model_config`. Abstain | 200 abstain | No | Verified Fact of `azure_client.py`. This half does not set that mode |
| Lake REST down | In-process `lake_runtime` when the retrieve helper has no `LAKE_REST_URL`. If HTTP lake was required and timed out, abstain | 200 `verdict: ABSTAIN` | No | Verified Fact of retrieve |
| Empty accepted lake set | Abstain | 200 `verdict: ABSTAIN` | No | Verified Fact. FD-14 |
| Gateway timeout or throttle | Visible retry. One extra attempt. Probe 503. Recovery GET 200 | 503 on probe | No | Verified Fact plus ED-P13-28A-01 |
| Gateway schema | Visible retry. No extra attempt. Probe 503 | 503 on probe | No | Verified Fact |
| Circuit flag set | Skip 8090. `error_class: circuit_open`. Recovery GET 200 | 200 on GET recovery | No | Inference, authority: team-force. Unwired in HB-28-01 |
| Invalid intake | After SC-28-01, park the payload. GET recovery lists it | 200 on GET recovery with `parked_intakes` | No packaged write. Temp store only in tests | Inference of the park path, authority: team-force |
| Duplicate `message_id` | Count `duplicates`. Inbox primary key holds | Same apply result | No second insert | Verified Fact |
| OPA binary missing | `local_evaluate` with the same named rules | Verdict string EXECUTE, HOLD_FOR_REVIEW, or BLOCK | No | Verified Fact |
| OPA eval timeout or non-zero exit | `local_evaluate` | Same three verdicts | No | Inference, authority: team-force. Binary timeout already 15 seconds |
| Injection write-from-text | BLOCK. HTTP 409. No next model. No park-to-execute | 409 `error_class: blocked` | No | Verified Fact |
| Record-changing action with a person | HOLD_FOR_REVIEW. `interrupt()`. Checkpoint file keeps the wait | 409 `wait_for_person` | No until the mapped RT role posts approval | Verified Fact. BO-03 stays PROPOSED |
| Graph recursion 12 or step 8 | HOLD_FOR_REVIEW. Draft stays a draft | 409 | No | Verified Fact. FD-15 |
| Process restart during wait | SqliteSaver reloads `thread_id` | GET case still shows `waiting_role` | No extra write from the model | Verified Fact |
| Identity miss | 401 or 503 `missing_server_key`. Same request | 401 or 503 | No | Verified Fact of sub-stage 27 |
| Lake write HTTP | 405 `lake_write_rejected` | 405 | No | Verified Fact |

Worked example. `MODEL_MODE=replay`. Prompt hash has no file. `generate()` returns `error_class: replay_miss` and `verdict: ABSTAIN`. `complete_azure` is not called. Honesty of a later live Azure row: Unknown.

Worked example. Partner note says auto approve. `proposed_action=approve`. OPA returns BLOCK. HTTP 409. `WRITE_TOOLS` is `[]`. The next step is stop. There is no replay of that action as EXECUTE.

Worked example. Intake `{"message_id": "DLQ-28-BAD"}`. After SC-28-01 the next step is a parked row. Replay of the same body stays `PARKED`. Replay of completed fields on a temp store can become `REPLAYED`. Packaged `legacy.sqlite3` stays unread-write.

---

## Stay with these actions

| Trigger | What Application A does | Limit |
|---|---|---|
| Replay miss | Abstain with `replay_miss` | Modes stay `replay` or later `azure`. No Ollama product mode |
| OPA BLOCK | Return HTTP 409 once | No second attempt |
| Parked intake | Keep the row listed after replay | Half B does not delete the row |
| Recovery time | Leave the cell Unknown | Do not copy the inherited 8-hour note |
| Replay mode | Token line B1 stays 0 prompt tokens and 0 completion tokens | No live Azure tokens |

---

## Dead-letter queue and replay

Park is the next step for invalid intake only. Language-model replay stays `MODEL_MODE=replay`. Those two stores are different folders. Dead-letter file: `apps/app_a/runtime/dlq.sqlite3`. Model replay folder: `operations/model-replay/`.

---

## Runbook — pick the next step

1. Read `error_class` on the HTTP body and `event` on stdout.
2. `replay_miss` → keep replay. Do not set `azure` on the laptop.
3. `upstream_timeout` or `rate_limit` → read `attempt_count`. Send `mode=normal` when the fixture should pass.
4. `blocked` → stop. Do not replay as a write.
5. Parked `PARKED` → replay the `parked_id`. Leave it listed.
6. `wait_for_person` → mapped RT role posts approval.

A copy of this runbook into `operations/` belongs to sub-stage 29.

---

## SLOs and observability

Each next step is proven by `error_class` and HTTP status. Numeric SLO cells stay Unknown. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

Replay and abstain add 0 live tokens. Park and replay of intake add 0 live tokens. This half claims no dollar benefit. Token lines B2 to B7 stay Unknown.

---

## Exact Half B check

HB-28-01 in `resilience-architecture.md`. One park-and-replay path. This matrix does not add a second check.

---

## What this file does not do

This file does not add a vendor. It does not start Half B. It does not call Azure. It does not sign a Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
