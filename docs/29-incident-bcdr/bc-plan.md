# Business continuity plan

| Field | Value |
|---|---|
| Stage | Phase 13 / 29 Incident and BCDR. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-29a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No continuity code in this half. |
| Evidence sources | FD-19; FD-13; FD-04; FD-15; `docs/28-resilience/ai-disabled-mode.md`; `docs/28-resilience/fallback-matrix.md`; `compose.yaml`; `.env.example`; `operations/replay_lookup.py`; `apps/app_a/intelligence/generate.py`; `docs/00-preflight/ai-economics/provisional-token-budget.md` |
| Assumptions | Compose still sets `MODEL_MODE=replay` on Application A, Application B, lake REST, and lake MCP. Azure variables stay unset for this half. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Azure endpoint, deployment name, and API version stay Unknown. Live token cost stays Unknown. Numeric continuity minutes stay Unknown. |
| Residual risks | Setting `MODEL_MODE=azure` on the laptop would call the public network. Inventing a sentence on a miss would hide the miss. Treating continuity as an 8-hour recovery floor would skip FD-19. |

This file names what keeps running while the live model is off, while an intake is parked, and while a named container is down. Continuity here is the work that still completes on this laptop. A signed company continuity certificate is a later artifact. This half does not write that certificate.

---

## Finding

**Finding.** Ranking, intake de-duplication, rule evaluation, reconciliation, health, identity, recovery GET, OPA, the approval pause, and the audit chain already run with the live model off. Natural-language query, conflict explanation, and agent `plan_draft` read a replay file or abstain. SC-28-01 park and replay already run without a live model. Half B leaves those paths as built and walks them in TT-29-01.
**Evidence.** `compose.yaml` `MODEL_MODE: ${MODEL_MODE:-replay}`. `lookup()` in `operations/replay_lookup.py`. FD-04. FD-13. FD-19. `WRITE_TOOLS = []`. HB-28-01 REAL.
**Impact.** Half B copies this plan into `operations/bc-plan.md`. No new workload is added.
**Risk.** Calling Azure when a replay file is missing would open a public-network socket on the laptop demo.
**Confidence.** High on the current mode wiring. Unknown on a live Azure duration.
**Open questions.** HALF_A_ACCEPTED. Azure variable values.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. The system keeps running with the model off. A failed intake stays visible. The parked intake from sub-stage 28 stays listed.

**Verified Fact.** FD-13. Modes `replay` and `azure`. No third offline mode. Ollama is not a product mode.

**Verified Fact.** FD-04. Triage ranking, rule evaluation, reconciliation, and intake de-duplication are deterministic. Conflict explanation, natural-language query, and agentic planning are GenAI. Those GenAI paths use replay files or abstain.

**Verified Fact.** Injection still BLOCKS. The model has no write tool.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. BO-03 working answer still sends every record-changing write through a person.

---

## What stays up with the live model off

| Piece | What it does | Needs a live model |
|---|---|---|
| `GET /health` on 8080, 8090, 8091, 8092, 8100, 8110 | Process probe | No |
| Identity on 8100, 8110, 8091, 8092 | Three headers plus process key | No |
| Queue, case GET, ranking | `priority()` in transformed code | No |
| Intake de-duplication | `intake_apply` | No |
| SC-28-01 park and replay | Dead-letter file plus `intake_apply` | No |
| Reconciliation | `reconcile_feeds` on a temp store in tests. Packaged partner feeds stay unread-write | No |
| Live policy archive match | `evaluate_live_policy` | No |
| Lake REST and lake MCP reads | Cite lake 1.0.0 | No |
| OPA | EXECUTE, HOLD_FOR_REVIEW, BLOCK | No |
| Approval `interrupt()` and `Command(resume=...)` | Person at RT-01 to RT-06 | No |
| Audit chain | One row per finished node | No |
| Gateway probe and recovery GET | Visible timeout, schema, throttle, parked list | No |
| Natural-language query | Replay file or abstain | Replay file only. Live Azure off |
| Conflict explanation | Replay file or abstain | Replay file only |
| Agent `plan_draft` | Replay file or abstain | Replay file only |

Worked example. `MODEL_MODE=replay`. Azure variables unset. A person still opens `GET /api/recovery` and reads `parked_intakes`. Row `message_id` `DLQ-28-BAD` stays `PARKED` after same-body replay. Honesty of that park path: REAL in HB-28-01.

Worked example. Same mode. Prompt hash has no file. Body is `error_class: replay_miss` and `verdict: ABSTAIN`. The process stays up. `/health` stays 200. Continuity here is the abstain plus the rest of the table. Azure stays unset.

---

## Order of work while a piece is down

1. Confirm `/health` on the listeners the person still needs. HTTP 200 means that process is up.
2. Confirm `MODEL_MODE=replay`. Leave Azure unset on the laptop.
3. Keep ranking, intake, rules, and park-and-replay in use. Those paths do not wait on Azure.
4. For a GenAI question, use a saved replay file. If the file is missing, accept the abstain.
5. For a record-changing action, the mapped RT role still posts approval. BO-03 stays PROPOSED.
6. For INC-2025-014, `owner_id` stays `None` until RT-06 supplies an owner at run time. This half invents no name.

Minutes that this order takes stay Unknown. This table is the order. It is not a recovery-time floor.

---

## Continuity when intake is parked

The person still sees the failure. `GET /api/recovery` lists the row. Replay re-runs `intake_apply`. Same body stays `PARKED`. Completed fields on a temp store can become `REPLAYED`. The row stays listed either way.

Packaged `legacy.sqlite3` stays unread-write. Continuity tests use a temp copy, same pattern as HB-28-01.

---

## Continuity when one named container exits

The other healthy listeners stay up. Compose marks the dead service unhealthy after five failed probes at a 10-second interval, after the 15-second start period. The person starts that one service. Seconds until `/health` returns 200 stay Unknown. **Verified Fact** of the Compose probe shape. **Unknown** of the measured restart seconds.

`bridge` is one-shot and stays `restart: "no"`. Starting `bridge` again is a later operator choice. This half does not change that Compose key.

---

## Dead-letter queue and replay

Continuity for a bad intake is the parked row plus replay. Continuity for a missing model file is abstain. Those two stores stay separate. Dead-letter file: `apps/app_a/runtime/dlq.sqlite3`. Model replay folder: `operations/model-replay/`.

A copy of this plan into `operations/bc-plan.md` is Half B SC-29-01.

---

## SLOs and observability

| Signal | What it proves | What it does not prove |
|---|---|---|
| JSON `model_mode=replay` | This request used replay | An availability percent |
| `error_class: replay_miss` | The hash had no file | A citation percent floor |
| `parked_intakes` length ≥ 1 | The failed intake is visible | A continuity-minute floor |
| Token line B1 0 and 0 | Envelope assumption for replay | Measured Azure cost |

Numeric latency stays Unknown. Recovery time stays Unknown. Recovery point stays Unknown. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

**Verified Fact** of the envelope row. Line B1 is 0 prompt tokens and 0 completion tokens when replay is used as designed. Honesty of that row: Assumption until Phase 15 proves replay. Lines B2 to B7 stay Unknown.

This half claims no dollar benefit for leaving Azure off. BO-11 working answer stays PROPOSED.

---

## Exact Half B check

HB-29-01 runs with `MODEL_MODE=replay`. The walk must not call Azure. The walk must not open a public-network socket for a model. Continuity evidence is health 200 plus the parked intake still listed.

---

## What this file does not do

This file does not set `MODEL_MODE=azure`. It does not start Half B. It does not invent a third mode. It does not invent a continuity-minute floor. It does not sign a Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
