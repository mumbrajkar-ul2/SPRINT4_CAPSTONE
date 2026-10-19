# AI-disabled mode

| Field | Value |
|---|---|
| Stage | Phase 13 / 28 Reliability and resilience. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-28a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No mode change in this half. |
| Evidence sources | FD-19; FD-13; FD-04; `compose.yaml`; `.env.example`; `operations/replay_lookup.py`; `apps/app_a/intelligence/generate.py`; `apps/app_b/intelligence/generate.py`; `docs/19-intelligence/model-configuration.md`; `docs/00-preflight/ai-economics/provisional-token-budget.md` |
| Assumptions | Compose still sets `MODEL_MODE=replay` on Application A, Application B, lake REST, and lake MCP. Azure variables stay unset for this half. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Azure endpoint, deployment name, and API version stay Unknown. Live token cost stays Unknown. |
| Residual risks | Setting `MODEL_MODE=azure` on the laptop would call the public network. Inventing a sentence on a miss would hide the miss. |

This file names what keeps running when the live model is off. The live model is Azure OpenAI. Off means `MODEL_MODE=replay` and no Azure socket.

---

## Finding

**Finding.** Compose already defaults `MODEL_MODE` to `replay`. Application A and Application B already read `operations/model-replay/{sha256}`. A miss returns `replay_miss` and abstains. Ranking, intake de-duplication, rule evaluation, and reconciliation stay deterministic code. Health, identity, recovery GET, OPA, and the approval pause stay up. The model still has no write tool.
**Evidence.** `compose.yaml` `MODEL_MODE: ${MODEL_MODE:-replay}`. `lookup()` in `operations/replay_lookup.py`. FD-04. FD-13. FD-19. `WRITE_TOOLS = []`.
**Impact.** Half B leaves this mode as built. HB-28-01 runs under replay.
**Risk.** Calling Azure when a replay file is missing would open a public-network socket on the laptop demo.
**Confidence.** High on the current mode wiring. Unknown on a live Azure duration.
**Open questions.** HALF_A_ACCEPTED. Azure variable values.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. The system keeps running with the model off.

**Verified Fact.** FD-13. Modes `replay` and `azure`. No third offline mode. Ollama is not a product mode.

**Verified Fact.** FD-04. Triage ranking, rule evaluation, reconciliation, and intake de-duplication are deterministic. Conflict explanation, natural-language query, and agentic planning are GenAI. Those GenAI paths use replay files or abstain.

**Verified Fact.** Injection still BLOCKS. The model has no write tool.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

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
| Gateway probe and recovery GET | Visible timeout, schema, throttle | No |
| Natural-language query | Replay file or abstain | Replay file only. Live Azure off |
| Conflict explanation | Replay file or abstain | Replay file only |
| Agent `plan_draft` | Replay file or abstain | Replay file only |

Worked example. `MODEL_MODE=replay`. Azure variables unset. `POST /api/query` with a freeze-set hash that has a file returns the PRECOMPUTED sentence after `check_claim`. Honesty of that sentence: PRECOMPUTED. Honesty of HTTP and citations: REAL when the test runs.

Worked example. Same mode. Hash has no file. Body is `error_class: replay_miss` and `verdict: ABSTAIN`. `complete_azure` is not imported onto the network path. The process stays up. `/health` stays 200.

---

## How to set the mode

| Setting | Value for this sub-stage |
|---|---|
| Process environment | `MODEL_MODE=replay` |
| Compose | `${MODEL_MODE:-replay}` on `app-a`, `app-b`, `lake-rest`, `lake-mcp` |
| `.env.example` | `MODEL_MODE=replay` |
| Azure variables | Unset. Values stay Unknown. Not committed |

A person who later wants Azure sets `MODEL_MODE=azure` and supplies the four Azure variables. That step stays NEEDS_HUMAN. This half does not do it.

---

## Dead-letter queue and replay

Language-model replay and intake park are different stores.

| Store | Path | What a miss or invalid does |
|---|---|---|
| Model replay | `operations/model-replay/{sha256}` | `replay_miss`. Abstain. No Azure |
| Intake dead-letter | `apps/app_a/runtime/dlq.sqlite3` after SC-28-01 | Row stays visible. Replay re-runs `intake_apply` |

The model does not write either store. Application A code writes the dead-letter file. Rehearsal code may write a replay file when mode is `azure`. This half does not write a new replay sentence.

---

## Runbook — keep the laptop on replay

1. Confirm `MODEL_MODE` is `replay` in the process. Compose default already is.
2. Confirm Azure variables are unset for the demo.
3. `GET /health` on 8100 returns HTTP 200.
4. A query with a saved hash returns the PRECOMPUTED body.
5. A query with no saved hash returns `replay_miss` and abstains.
6. Do not set `MODEL_MODE=azure` because a hash has no file. Keep replay. The miss stays `replay_miss`.

A copy of this runbook into `operations/` belongs to sub-stage 29.

---

## SLOs and observability

| Signal | What it proves | What it does not prove |
|---|---|---|
| JSON `model_mode=replay` | This request used replay | An availability percent |
| `error_class: replay_miss` | The hash had no file | A citation percent floor |
| Token line B1 0 and 0 | Envelope assumption for replay | Measured Azure cost |

Numeric latency stays Unknown. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

**Verified Fact** of the envelope row. Line B1 is 0 prompt tokens and 0 completion tokens when replay is used as designed. Honesty of that row: Assumption until Phase 15 proves replay. Lines B2 to B7 stay Unknown.

This half claims no dollar benefit for leaving Azure off. BO-11 working answer stays PROPOSED.

---

## Exact Half B check

HB-28-01 runs with `MODEL_MODE=replay`. The test must not call Azure. The test must not open a public-network socket for a model.

---

## What this file does not do

This file does not set `MODEL_MODE=azure`. It does not start Half B. It does not invent a third mode. It does not sign a Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
