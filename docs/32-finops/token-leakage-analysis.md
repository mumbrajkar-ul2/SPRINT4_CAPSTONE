# Token leakage analysis

| Field | Value |
|---|---|
| Stage | Phase 13 / 32 FinOps and token efficiency. Half B measured results. SC-32-01 / HB-32-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-32b-doc-20261018-001 |
| Status | MEASURED. Replay hit and miss stdout lines now carry `prompt_tokens=0` and `completion_tokens=0`. Field name `token` stays absent. Live Azure leak size stays Unknown. BO-11 stays PROPOSED. |
| Evidence sources | FD-02; FD-13; FD-15; FD-19; `apps/app_a/intelligence/generate.py`; `apps/app_a/intelligence/azure_client.py`; `apps/app_a/agent/budget.py`; `apps/shared/jsonlog.py`; `docs/22-agentic-engineering/agent-budget-policy.md`; `docs/19-intelligence/model-configuration.md`; `docs/08-ai-qualification/economics-baseline-reconciliation.md`; `docs/31-observability/ai-telemetry-spec.md`; `tests/platform/test_phase13_finops.py`; `baseline-vs-actual-token-analysis.md` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. Agent step budget stays 8 model-or-tool nodes. Maximum completion tokens on the Azure client stay 800. BO-11 stays PROPOSED. |
| Unresolved issues | Live Azure leakage size stays Unknown. Rehearsal token count stays Unknown. Application B token line stays unbuilt. |
| Residual risks | A silent Azure call on a replay miss would spend live tokens during the laptop demo. A field named `token` would vanish from stdout. Counting Cursor delivery tokens as case spend would inflate the meter. |

This file names how extra tokens could be spent, or how a real spend could hide. A leak here is extra model text, a hidden meter, or a cost line that Phase 2 already retired. Under replay the shown Application A path spends 0 live tokens. Half B wrote that pair so a miss or a hit is visible.

Engineering decision ED-P13-32A-06, authority: team-force. Leak ids `L-32-01` to `L-32-10`. Failure ids `FM-32-01` to `FM-32-16` across this folder.

---

## Finding

**Finding.** `generate()` on `MODEL_MODE=replay` returns `replay_miss` when the saved file is absent. It does not call `complete_azure`. `WRITE_TOOLS` is empty. After HB-32-01 the hit line is `event=replay_tokens` with `prompt_tokens=0` and `completion_tokens=0`. The miss line is `event=replay_miss` with the same two fields. No stdout field named `token` was written. Live Azure leak size stays Unknown.
**Evidence.** `generate.py` replay branch. `query.py` after SC-32-01. `tests/platform/test_phase13_finops.py`. `jsonlog.py` `FORBIDDEN_KEYS`. FD-02. FD-19. Honesty: REAL for the two zeros.
**Impact.** The replay zeros are grep-able. Half B did not add a retry into Azure.
**Risk.** Setting `MODEL_MODE=azure` to measure leakage would open a public-network socket.
**Confidence.** High on the measured miss path and the forbidden field name. Unknown on live Azure extra tokens.
**Open questions.** Measured Azure usage later. Application B meter.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric cost floors stay Unknown.

**Verified Fact.** FD-02. The model gets read-only tools only. There is no write-tool token path.

**Verified Fact.** FD-13. Compose default `MODEL_MODE=replay`. There is no third offline mode.

**Verified Fact.** FD-15 engineering defaults. Recursion limit 12. Step budget 8. Maximum tool invocations 8. Those integers are not quality floors.

**Verified Fact** of BO-11 working answer. Claim no monetary benefit. The row stays PROPOSED.

---

## Leak catalogue

| Id | What can leak or hide | What the code does today | Live tokens on this laptop | Label |
|---|---|---|---|---|
| L-32-01 | Replay miss falls through to Azure | `generate()` returns `replay_miss` and abstains | 0. Azure uncalled | Verified Fact |
| L-32-02 | Agent uses up to 8 model nodes on a live run | Same `generate()` helper. Budget 8 | 0 under replay. Unknown under Azure | Verified Fact of the cap. Unknown on Azure |
| L-32-03 | Azure is retried after a timeout | `complete_azure` is one call. Upstream retry 1 is for gateway timeout, not the model | Azure uncalled | Verified Fact of this laptop |
| L-32-04 | Prompt includes unused retrieved items | Retrieve can return several lake ids. Live extra prompt tokens Unknown | 0 under replay | Assumption on live size |
| L-32-05 | Field named `token` is logged | `FORBIDDEN_KEYS` drops it | Meter would hide | Verified Fact |
| L-32-06 | Cursor delivery tokens are added to a case | 0C assumption A-W1 keeps them separate | Off the case meter | Assumption A-W1 |
| L-32-07 | Deterministic S7 to S13 cores are priced as model work | Phase 2 retired R-P2-01 | 0 model tokens | Verified Fact |
| L-32-08 | Client cap 800 is treated as spend | `max_tokens` 800 in `azure_client.py` | Uncalled. Cap is not usage | Verified Fact of the file |
| L-32-09 | Embedding API for lake search | FTS5 word search. No embedding client | 0 embedding tokens sent | Verified Fact of the tree |
| L-32-10 | Rehearsal tokens are guessed into B2 | No invoice | Unknown | Unknown |

Worked example for L-32-01. Question `What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file` already returns `error_class` `replay_miss`. Honesty: REAL in `telemetry-results.md`. The replay branch of `generate()` does not call `complete_azure`. Extra live tokens on that miss are 0.

Worked example for L-32-08. A later Azure call may send `max_tokens` 800. That number is the cap the client asks for. The usage object, when one exists, is the spend. No usage object exists on this laptop. Do not write 800 as the B3 actual.

Worked example for L-32-02. Graph `app_a_investigate` may visit `plan_draft` more than once inside the step budget of 8. Under replay each visit reads a file or misses. Live tokens stay 0. Under Azure the sum stays Unknown.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-32-14 | Someone sets `MODEL_MODE=azure` after a miss to "fill the cache" | A public-network socket can open | Keep `MODEL_MODE=replay`. Leave B2 Unknown |
| FM-32-15 | Someone emits `token=0` | The field is dropped | Use `prompt_tokens` and `completion_tokens` |
| FM-32-16 | Someone adds Cursor tokens to B1 | B1 is no longer the replay path | Keep B1 as the laptop demo replay line |

Dead-letter parking stays on invalid intake. A replay miss is a successful empty answer. It is not parked in `dlq.sqlite3`. Parking it would hide the miss from the token meter.

---

## Dead-letter queue and replay

Intake park and intake replay add 0 model tokens. Language-model replay stays the SHA-256 file in `operations/model-replay/`. A miss stays on the same HTTP request. Half B writes 0 and 0 on that request so the miss is metered.

---

## Runbook — check for a leak on this laptop

1. Confirm `MODEL_MODE` is `replay`.
2. Confirm Azure variables stay unset.
3. POST a replay miss and a replay hit on Application A query.
4. After Half B, both lines show `prompt_tokens=0` and `completion_tokens=0`. Honesty: REAL.
5. Confirm stdout has no field named `token`.
6. Confirm no `complete_azure` socket ran.
7. Leave L-32-02 through L-32-04 live sizes Unknown.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| `error_class=replay_miss` | HTTP and stdout | The miss did not call Azure | Azure usage |
| `prompt_tokens` after Half B | stdout | The replay path wrote 0. Honesty: REAL | A leakage percent |
| `STEP_BUDGET` 8 | `budget.py` | The agent stops at 8 nodes | Live tokens inside that cap |
| Empty `WRITE_TOOLS` | `tools.py` | No write-tool token path | A dollar saving |

No leakage percent floor is set. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

Leaks L-32-01, L-32-07, and L-32-09 add 0 live model tokens on this laptop. Line B1 is measured 0 and 0 for the shown replay path. Honesty: REAL. Line B2 stays Unknown so rehearsal is not guessed. This half claims no dollar benefit from avoided Azure calls. BO-11 stays PROPOSED.

---

## The one small Half B check

See `cost-guardrails.md` SC-32-01 and HB-32-01. The check wrote the two zero fields so L-32-05 cannot hide the replay meter. Half B did not add an Azure retry. Half B did not add embeddings. Measured cells live in `baseline-vs-actual-token-analysis.md`.

---

## What this file does not do

This file named the leak catalogue. Half B wrote the two zero fields. This file does not start sub-stage 33. It does not call Azure. It does not invent a leakage percent. It does not invent a dollar saving. It does not update a tracker.
