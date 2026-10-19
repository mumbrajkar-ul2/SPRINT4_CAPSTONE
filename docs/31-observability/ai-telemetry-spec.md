# AI telemetry specification

| Field | Value |
|---|---|
| Stage | Phase 13 / 31 Observability and service levels. Half B evidence. SC-31-01 / HB-31-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-31b-doc-20261018-001 |
| Status | MEASURED. SC-31-01 emits `event=replay_miss` from Application A query. HB-31-01 cells are REAL. Token lines B2 to B7 stay Unknown. |
| Evidence sources | FD-19; FD-11; FD-13; FD-14; FD-18; `apps/app_a/intelligence/generate.py`; `apps/app_b/intelligence/generate.py`; `operations/replay_lookup.py`; `apps/app_a/routes/query.py`; `apps/app_a/intelligence/azure_client.py`; `docs/00-preflight/ai-economics/provisional-token-budget.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `tests/platform/test_replay.py`; `tests/platform/test_app_a_grounding.py` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. Replay files live under `operations/model-replay/`. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Live Azure token counts stay Unknown. Retrieval p95 stays Unknown. Citation percent and groundedness percent stay Unknown. Application B miss line stays unbuilt. |
| Residual risks | Calling Azure on a miss would open a public-network socket. Emitting a field named `token` would drop that field. Copying a citation percent from a freeze score would invent a floor. |

This file names what a language-model call records. The three in-use AI paths are natural-language query, conflict explanation, and agent draft. Replay is the path on this laptop. Half B writes one stdout line when replay misses on Application A query.

Engineering decision ED-P13-31A-01 applies here. Control `SC-31-01` emits `event=replay_miss` from `POST /api/query` on Application A.

Engineering decision ED-P13-31A-08, authority: team-force. AI stdout extra fields are `model_mode`, `error_class`, `prompt_hash`, `prompt_id`, and `verdict` when those values exist. Prompt and completion counts, when written later, use names `prompt_tokens` and `completion_tokens`. On replay those two counts are 0. Half B writes `model_mode`, `error_class`, and `prompt_hash` only.

---

## Finding

**Finding.** `generate()` already returns `model_mode`, `error_class`, `prompt_hash`, `prompt_id`, `semver`, `retrieved_item_ids`, `verdict`, `citations`, and `lake_version`. Replay reads `operations/model-replay/{sha256}`. A miss returns `error_class=replay_miss` and `verdict=ABSTAIN`. `lookup()` already puts `event=replay_miss` in its dict. That dict is not written to stdout. Token line B1 stays 0 and 0 under replay. Live Azure stays uncalled in this half.
**Evidence.** `generate.py` return dict. `replay_lookup.py` miss dict. `test_at_replay_miss_stays_local`. `provisional-token-budget.md` line B1. FD-13. FD-19.
**Impact.** Half B adds one `emit` on the Application A query path. Application B `generate()` stays as built.
**Risk.** Setting `MODEL_MODE=azure` to fill a token line would open a public-network socket.
**Confidence.** High on the current return fields and the measured `replay_miss` stdout line. Unknown on live Azure token counts.
**Open questions.** Reviewer grades HB-31-01. Application B miss line.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric latency, availability, error-budget, and recovery floors stay Unknown. This half invents no percent and no dollar benefit.

**Verified Fact.** FD-13. Compose default `MODEL_MODE=replay`. There is no third offline mode.

**Verified Fact.** FD-14 and FD-18. A consequential answer cites a lake item id or abstains. Injection returns BLOCK. Numeric quality percents stay Unknown.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED.

---

## Paths that use the model

| Path | Route or graph | Prompt id | What replay does |
|---|---|---|---|
| Natural-language query | `POST /api/query` with `job=query` | `P-NL-QUERY` | Read the file named by the prompt hash |
| Conflict explanation | `POST /api/query` with `job=explain` | `P-EXPLAIN-CONFLICT` | Same lookup |
| Draft plan | `POST /api/query` with `job=draft` | `P-DRAFT-PLAN` | Same lookup |
| Agent draft | Graph `app_a_investigate` node `plan_draft` | Same generate helper | Same lookup |

Worked example. Question `Which port does the Context Lake REST listener use?` with prompt `P-NL-QUERY` has a saved replay file after fixtures are written. `lookup` returns `ok` true and `event=replay_hit`. Honesty: REAL in `test_replay.py` for the fixture prompt. The query sentence from that fixture is PRECOMPUTED.

Worked example. Question `zz-no-replay-hash-question-about-port-8091-unique` returns `verdict` `ABSTAIN`. When retrieve found an item, `error_class` is `replay_miss`. Honesty: REAL in `test_app_a_grounding.py`.

---

## Fields the HTTP body already returns

**Verified Fact** of `apps/app_a/routes/query.py`.

| Field | What it holds | Honesty |
|---|---|---|
| `sentence` | Answer text, or empty on abstain | PRECOMPUTED on a replay hit. Empty on a miss |
| `citations` | Lake item ids | REAL ids from retrieve |
| `verdict` | `ANSWER`, `ABSTAIN`, or a hold or block path | REAL from `ground()` |
| `block` | True when injection locators plus a write action | REAL |
| `error_class` | `replay_miss`, `replay_required`, `azure_call_failed`, or null | REAL on this laptop under replay |
| `prompt_id` | `P-NL-QUERY`, `P-EXPLAIN-CONFLICT`, or `P-DRAFT-PLAN` | REAL |
| `semver` | Prompt version string | REAL |
| `prompt_hash` | SHA-256 of the canonical prompt | REAL |
| `retrieved_item_ids` | Ids retrieve accepted | REAL |
| `lake_version` | Pinned lake version | REAL |
| `model_mode` | From `MODEL_MODE`, default `replay` | REAL on the generate return. HTTP body today omits this key |
| `correlation_id` | `X-Correlation-Id` or null | REAL of the header copy in `query.py` |
| `grounded` | True when citations support the sentence | REAL of the ground check |
| `reject_reason` | Why a claim was dropped | REAL when present |

`model_mode` sits on the `generate()` return today. `POST /api/query` does not copy that key into the JSON body. Half B leaves the HTTP body as built. The new stdout line carries `model_mode`.

---

## Stdout line Half B adds

| Field | Value on a miss |
|---|---|
| `service` | `app-a` |
| `event` | `replay_miss` |
| `level` | `info` |
| `path` | `/api/query` |
| `status` | 200 |
| `correlation_id` | Header value, or null |
| `model_mode` | `replay` |
| `error_class` | `replay_miss` |
| `prompt_hash` | Hash from `generate()` when present |

HTTP stays 200 with `verdict` `ABSTAIN`. A miss is a successful empty answer. **Verified Fact.** `error-handling-spec.md` `abstain` mapping.

Azure is not called. **Verified Fact** of the Half B constraint.

---

## Token counts

| Line | Prompt tokens | Completion tokens | Honesty | Label |
|---|---|---|---|---|
| B1 laptop demo, replay on | 0 | 0 | REAL if replay is used as designed | Assumption A-W2 until a later measured rehearsal |
| B2 to B7 | Unknown | Unknown | Unknown | Unknown |

Worked example. HB-31-01 keeps `MODEL_MODE=replay`. The miss path reads no completion. Prompt tokens stay 0. Completion tokens stay 0. Half B does not write those two fields on the line. A later FinOps sub-stage may add them.

`jsonlog.emit` drops a field whose name is `token`. Use `prompt_tokens` and `completion_tokens` if a later half writes counts. **Verified Fact.** `FORBIDDEN_KEYS`.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-31-02 | Replay miss has no stdout line | HTTP `error_class=replay_miss`. Stdout `request_ok` only | SC-31-01 |
| AI-empty-retrieve | Retrieve found no item | `generate()` abstains before lookup. `error_class` may be null | Leave that path. It is an abstain, not a miss file |
| AI-replay-hit | Saved file exists | HTTP sentence from that file | Keep the file. Label the sentence PRECOMPUTED |
| AI-azure-off | Live model is off | Replay file or miss abstain. Process stays up | Keep `MODEL_MODE=replay` |
| AI-azure-tempt | Person wants a live token number | No invoice exists | Leave B2 to B7 Unknown. Do not set `azure` on this laptop |

Dead-letter parking stays on invalid intake. A replay miss is not parked in `dlq.sqlite3`. The miss returns on the same request.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| `error_class=replay_miss` on HTTP | Query body | Generate abstained without Azure | A citation percent |
| `event=replay_miss` after Half B | stdout | The miss is grep-able | Retrieval p95 |
| `model_mode=replay` on that line | stdout | The process used replay | An availability percent |
| Replay fixture body | `operations/model-replay/` | A hit is PRECOMPUTED | A live Azure pass |
| Token line B1 | 0C envelope | Replay adds no live token | A dollar benefit |

Citation percent, groundedness percent, and abstention percent stay Unknown. **Verified Fact.** FD-14. FD-18. FD-11.

---

## Cost and the 0C envelope

This half adds no live model call. Line B1 stays 0 and 0. Lines B2 to B7 stay Unknown. Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED. This half claims no dollar benefit. **Verified Fact.** FD-19. BO-11 working answer stays PROPOSED.

---

## Half B check

See `observability-architecture.md` SC-31-01 and HB-31-01. Measured cells are in `telemetry-results.md`. Before: query miss has no `event=replay_miss` stdout line. Honesty: REAL. After: one line with `service=app-a`, `event=replay_miss`, `model_mode=replay`, and `correlation_id` `corr-p13-31b-doc-20261018-001`. Honesty: REAL. A cited GQ-23 answer is not labeled `replay_miss`.

---

## What this file does not do

This file named the AI fields. Half B wrote the miss line. This file does not call Azure. It does not invent a token count. It does not invent a citation percent.
