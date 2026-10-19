# Baseline versus actual token analysis

| Field | Value |
|---|---|
| Stage | Phase 13 / 32 FinOps and token efficiency. Half B measured results. SC-32-01 / HB-32-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-32b-doc-20261018-001 |
| Status | MEASURED. SC-32-01 writes `prompt_tokens=0` and `completion_tokens=0` from Application A `POST /api/query` under `MODEL_MODE=replay`. A replay hit uses `event=replay_tokens`. A replay miss adds those two fields to `event=replay_miss`. B1 is REAL for that shown replay path. B2 to B7 stay Unknown. BO-11 stays PROPOSED. `mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. |
| Evidence sources | FD-19; BO-11; `docs/00-preflight/ai-economics/provisional-token-budget.md`; `docs/00-preflight/ai-economics/preliminary-finops-baseline.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/00-preflight/ai-economics/workload-assumptions.md`; `docs/08-ai-qualification/economics-baseline-reconciliation.md`; `docs/31-observability/ai-telemetry-spec.md`; `apps/app_a/routes/query.py`; `apps/app_a/intelligence/generate.py`; `apps/shared/jsonlog.py`; `tests/platform/test_phase13_finops.py` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. Half B ran HB-32-01 only. Application B query stays as built. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | Lines B2 to B7 stay Unknown. Live Azure prompt and completion counts stay Unknown. Dollars per 1,000 tokens stay Unknown. Application B token line stays unbuilt. Unit price stays Unknown. |
| Residual risks | Writing a guessed thousand-token figure as actual spend would invent a budget. Copying 4982.61 as a customer saving would break BO-11. Setting `MODEL_MODE=azure` to fill a cell would open a public-network socket. |

This file compares the Phase 0C token envelope with the token counts this laptop can show. FinOps here is the cost and token record for the stack. The 0C envelope lives in `docs/00-preflight/ai-economics/`. Half B recorded the replay path as 0 prompt tokens and 0 completion tokens. That pair is REAL only for the replay path Half B showed. Numeric cost floors stay Unknown. This half claims no dollar benefit.

Engineering decision ED-P13-32A-01 continued, authority: team-force. Control id `SC-32-01`. Check id `HB-32-01`. Application A `POST /api/query` under `MODEL_MODE=replay` writes `prompt_tokens=0` and `completion_tokens=0`.

Engineering decision ED-P13-32A-03 continued, authority: team-force. Line B1 is REAL for the shown replay-hit path. Lines B2 to B7 stay Unknown.

Engineering decision ED-P13-32B-01, authority: team-force. `query.py` emits `event=replay_tokens` when `generate()` returns under replay and `error_class` is not `replay_miss`. A miss keeps `event=replay_miss` and adds the two zero fields. The HTTP body stays without those fields. The field name `token` is not written.

---

## Finding

**Finding.** Before SC-32-01, `POST /api/query` with question `Which port does the Context Lake REST listener use?` and header `X-Correlation-Id: corr-p13-32b-doc-20261018-001` returned HTTP 200, `verdict` `ANSWER`, citation `arch.listener.lake_rest_8091`, `error_class` null. Stdout had `event=request_ok` for that id. No line has `prompt_tokens`. After SC-32-01 the same POST still returns HTTP 200 and the same citation. Stdout now has one line with `service=app-a`, `event=replay_tokens`, `model_mode=replay`, `prompt_tokens=0`, `completion_tokens=0`, and that correlation id. A miss question still returns `event=replay_miss`. That miss line now also carries `prompt_tokens=0` and `completion_tokens=0`. A cited answer is not a miss. `GET /health` stayed HTTP 200 `{"ok": true}`. `MODEL_MODE` stayed `replay`. Azure was not called. B1 actual is 0 and 0. Honesty: REAL for that replay path. B2 to B7 stay Unknown. `mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. They are not model cost. BO-11 stays PROPOSED.
**Evidence.** Live before probe on 2026-10-18 before the two fields landed. Live after pytest `tests/platform/test_phase13_finops.py`. Correlation id `corr-p13-32b-doc-20261018-001`. Honesty: REAL.
**Impact.** A person can grep stdout for `prompt_tokens` and `completion_tokens` on the Application A replay path without calling Azure.
**Risk.** Treating the two zeros as a signed invoice would invent a dollar actual.
**Confidence.** High on the measured replay-hit line and the miss fields. Unknown on live Azure counts.
**Open questions.** Reviewer grades HB-32-01. Who later records a rehearsal invoice for B2. Application B meter.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric latency, availability, recovery, retry, and cost floors stay Unknown. This half invents no percent and no dollar benefit.

**Verified Fact** of BO-11 working answer. Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit. The row stays PROPOSED. The signer name stays Unknown.

**Verified Fact.** `Execution_Plan.md` section 9. Cost honesty is REAL when tokens and spend are measured. ROI honesty is EDUCATIONAL.

**Verified Fact** of Compose default `MODEL_MODE=replay`. Azure endpoint, deployment name, and API version stay Unknown.

---

## The 0C baseline this page reconciles

**Verified Fact** of `docs/00-preflight/ai-economics/provisional-token-budget.md`.

| Line | Purpose | 0C prompt tokens | 0C completion tokens | 0C honesty | Half B actual | Half B honesty |
|---|---|---|---|---|---|---|
| B1 | Laptop demo, replay on | 0 | 0 | REAL if replay is used as designed | 0 and 0 on the shown Application A query. stdout `event=replay_tokens` | REAL for that replay path |
| B2 | Rehearsal record of the 40-minute path | Unknown | Unknown | Unknown | Unknown | Unknown |
| B3 | Evaluation of S7 to S13 on Application A | Unknown | Unknown | Unknown | Unknown | Unknown |
| B4 | Evaluation of S7 to S13 on Application B | Unknown | Unknown | Unknown | Unknown | Unknown |
| B5 | Retrieval / embedding for the lake | Unknown | Unknown | Unknown | No embedding client on disk | Embedding invoice stays Unknown |
| B6 | Delivery agents for later phases | Unknown | Unknown | Unknown | Cursor build tokens stay off the case meter | Assumption A-W1 |
| B7 | Contingency | Unknown | Unknown | Unknown | Unknown | Unknown |
| **Total** | **Sum of measured lines** | **Unknown** | **Unknown** | **Unknown** | **Unknown** | **Unknown** |

Worked example for B1. Question `Which port does the Context Lake REST listener use?` has a saved replay file. The Context Lake is the SQLite knowledge store on port 8091. `generate()` reads that file. Azure stays uncalled. Half B wrote `prompt_tokens=0` and `completion_tokens=0` on stdout with `event=replay_tokens`. Honesty: REAL for that replay path.

Worked example for B5. Lake search uses SQLite word search named FTS5. No embedding client sits under `apps/` or `context-lake/`. No embedding tokens were sent. An embedding invoice cell still stays Unknown because no embedding bill exists.

Worked example for the total. B1 is 0 and 0. B2 to B7 stay Unknown. The sum of a measured 0 with six Unknown lines stays Unknown.

---

## What Phase 2 already retired

**Verified Fact** of `economics-baseline-reconciliation.md`.

| Retired id | What is not a model-token line |
|---|---|
| R-P2-01 | The deterministic core of S7 to S13 (replay mark, recipe compare, clock split, policy lookup, retry status) |
| R-P2-02 | Machine-learning inference for `engineering_hold` |
| R-P2-03 | Rule evaluation |
| R-P2-04 | Reconciliation |
| R-P2-05 | Intake de-duplication |
| R-P2-06 | Triage ranking |
| R-P2-07 | Agent-completion time for those four code jobs |
| R-P2-08 | Every candidate language task from the intent counted as live spend |

Worked example. Scenario 7 still marks 67 REPLAY rows in code. That mark has no model token line. A later explanation of those 67 rows is a GenAI turn. Under replay that explanation is designed as 0 live tokens. Under Azure the count stays Unknown.

---

## What already exists on the query path

**Verified Fact** of `query.py` and `generate.py` after SC-32-01.

| Signal | What it holds now | Token fields |
|---|---|---|
| HTTP body on a replay hit | Sentence from the saved file. `error_class` null | None. Body stays as built |
| HTTP body on a replay miss | `verdict` `ABSTAIN`. `error_class` `replay_miss` | None. Body stays as built |
| stdout `event=replay_tokens` | `service=app-a`, `model_mode=replay`, `prompt_hash` | `prompt_tokens=0`, `completion_tokens=0` |
| stdout `event=replay_miss` | `service=app-a`, `model_mode=replay`, `prompt_hash` | `prompt_tokens=0`, `completion_tokens=0` |
| stdout `event=replay_hit` | Python dict only in `replay_lookup` | None |
| `generate()` return | `model_mode`, `error_class`, `prompt_hash` | None |
| Azure usage object | `complete_azure` returns `body` only | None. Azure uncalled under replay |

A token is one piece of text the language model reads or writes. Prompt tokens are the pieces sent in. Completion tokens are the pieces written out.

`jsonlog.emit` drops a field whose name is `token`. Half B used `prompt_tokens` and `completion_tokens`. **Verified Fact.** `FORBIDDEN_KEYS`. ED-P13-31A-08. ED-P13-32A-02.

---

## Exact Half B check HB-32-01

Test path: `tests/platform/test_phase13_finops.py`.

Headers:

| Header | Value |
|---|---|
| `X-Api-Key` | `local-demo-only` |
| `X-Actor-Id` | `demo-rt01-1` |
| `X-Actor-Role` | `RT-01` |
| `X-Correlation-Id` | `corr-p13-32b-doc-20261018-001` on the hit POST. `corr-p13-32b-miss-001` on the miss POST |

Control: SC-32-01. Honesty of filled cells: REAL.

---

## HB-32-01 before

Honesty of filled cells: REAL.

Command shape recorded: in-process `TestClient` `POST /api/query` on 2026-10-18, before `query.py` wrote `prompt_tokens`. Question `Which port does the Context Lake REST listener use?`. Header `X-Correlation-Id: corr-p13-32b-doc-20261018-001`. `MODEL_MODE=replay`.

Measured before

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| HTTP status | 200 | 200 | REAL |
| `verdict` | `ANSWER` | `ANSWER` | REAL |
| `error_class` on the HTTP body | null | null | REAL |
| Citations | `arch.listener.lake_rest_8091` | `arch.listener.lake_rest_8091` | REAL |
| Sentence | present. PRECOMPUTED | `The Context Lake REST listener uses port 8091.` PRECOMPUTED | REAL for the HTTP fields. PRECOMPUTED for the sentence text |
| Stdout `event=request_ok` for that id | present | present. `service=app-a`, `path=/api/query`, `status=200` | REAL |
| Stdout `prompt_tokens` | absent | absent. no line has `prompt_tokens` | REAL |
| Stdout `completion_tokens` | absent | absent | REAL |
| Stdout `event=replay_tokens` | absent | absent | REAL |
| Stdout `event=replay_miss` on the cited answer | absent | absent | REAL |
| HTTP body `prompt_tokens` | absent | absent | REAL |
| Miss POST `event=replay_miss` | present from SC-31-01 | present. `model_mode=replay`. no `prompt_tokens` | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |

Worked example of the measured before. Stdout lines were `health_ok`, then `request_ok` for the cited id. Those lines omit `prompt_tokens`. The miss POST already wrote `event=replay_miss` from SC-31-01. That miss line also omitted `prompt_tokens`.

---

## HB-32-01 after

Same hit POST. Same identity headers. `MODEL_MODE=replay`. In-process `TestClient`. Socket create patched to fail. `complete_azure` patched to fail.

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| HTTP status | 200 | 200 | REAL |
| `verdict` | `ANSWER` | `ANSWER` | REAL |
| `error_class` on the HTTP body | null | null | REAL |
| Citations | `arch.listener.lake_rest_8091` | `arch.listener.lake_rest_8091` | REAL |
| Sentence | present. PRECOMPUTED | `The Context Lake REST listener uses port 8091.` PRECOMPUTED | REAL for the HTTP fields. PRECOMPUTED for the sentence text |
| HTTP body `prompt_tokens` | absent. Body stays as built | absent | REAL |
| HTTP body `model_mode` key | absent. Body stays as built | absent | REAL |
| Stdout `event=replay_tokens` count | 1 | 1 | REAL |
| That line `service` | `app-a` | `app-a` | REAL |
| That line `event` | `replay_tokens` | `replay_tokens` | REAL |
| That line `model_mode` | `replay` | `replay` | REAL |
| That line `correlation_id` | `corr-p13-32b-doc-20261018-001` | `corr-p13-32b-doc-20261018-001` | REAL |
| That line `path` | `/api/query` | `/api/query` | REAL |
| That line `status` | 200 | 200 | REAL |
| That line `prompt_tokens` | 0 | 0 | REAL |
| That line `completion_tokens` | 0 | 0 | REAL |
| That line `prompt_hash` | present | `a654c447418e2cd460be9a032c4cb185921572abbc9cf42bbd961a50a7d12719` | REAL |
| That line field named `token` | absent | absent | REAL |
| Stdout `event=request_ok` | still present | present | REAL |
| Cited-answer stdout `replay_miss` | none | none | REAL |
| Miss POST HTTP `verdict` | `ABSTAIN` | `ABSTAIN` | REAL |
| Miss POST `error_class` | `replay_miss` | `replay_miss` | REAL |
| Miss stdout `event=replay_miss` | 1 line with the two fields | 1. `prompt_tokens=0`, `completion_tokens=0`, `correlation_id` `corr-p13-32b-miss-001`, `prompt_hash` `be25183a6c82ce22c9e2331b682f5658357f02d5b641450322fe4d8a7f982cec` | REAL |
| Miss stdout `event=replay_tokens` | none | none | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| `MODEL_MODE` | `replay` | `replay` | REAL |
| Azure socket | none | none. `complete_azure` and `socket.create_connection` were patched to fail. `socket.socket` was forbidden only inside `generate()` so TestClient could open its event loop | REAL |
| `WRITE_TOOLS` | `[]` | `[]` | REAL |
| B1 actual | 0 and 0 | 0 and 0 | REAL for that replay path |
| B2 to B7 | Unknown | Unknown | Unknown |
| Unit price | Unknown | Unknown | Unknown |
| Dollars | Unknown | Unknown | Unknown |
| `mean_amount` 4982.61 | SIMULATED. Not model cost | SIMULATED. Not model cost | SIMULATED |
| `hours_per_case` 0.603 | SIMULATED. Not model cost | SIMULATED. Not model cost | SIMULATED |
| BO-11 | PROPOSED | PROPOSED | PROPOSED |

Worked example of the measured after. The hit POST wrote one JSON line `{"service":"app-a","event":"replay_tokens","correlation_id":"corr-p13-32b-doc-20261018-001","model_mode":"replay","prompt_tokens":0,"completion_tokens":0}`. Middleware still wrote `request_ok`. The miss POST wrote `event=replay_miss` with the same two zero fields. The cited answer wrote no `replay_miss` line.

Honesty of those cells: REAL. Numeric cost floors stay Unknown.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-32-01 | B1 is filled with a guessed 1,000 tokens | A number with no stdout line | B1 is 0 and 0 from the `replay_tokens` line |
| FM-32-02 | B2 to B7 are filled from a public price list | A dollar total | Leave those lines Unknown. Do not copy a list price |
| FM-32-03 | 4982.61 is copied as actual model spend | A money figure next to B1 | Keep 4982.61 on the synthetic case-amount row. Honesty: SIMULATED |
| FM-32-04 | `MODEL_MODE` is set to `azure` to fill B3 | A public-network socket can open | Keep `MODEL_MODE=replay`. Leave B3 Unknown |
| FM-32-05 | Field name `token` is emitted | `jsonlog` drops the field | Use `prompt_tokens` and `completion_tokens` |

Dead-letter parking stays on invalid intake in `apps/app_a/runtime/dlq.sqlite3`. A missing token field is not parked there. The next query is a new meter write.

---

## Dead-letter queue and replay

Language-model replay stays `MODEL_MODE=replay`. A miss returns `replay_miss` and abstains. That miss spends 0 live tokens on this laptop. **Verified Fact** of `generate.py` and the measured miss line.

Intake replay is a different path. It replays a parked bad message. It does not call Azure. It adds no model token line.

---

## Runbook — read the B1 actual

1. Confirm `MODEL_MODE` is `replay` on Application A.
2. `POST /api/query` with a saved replay-hit question. The Half B question is `Which port does the Context Lake REST listener use?`.
3. Grep stdout for `prompt_tokens` and `completion_tokens`.
4. Line B1 of this page is 0 and 0. Honesty: REAL for that replay path.
5. Leave B2 to B7 Unknown.
6. Leave dollars Unknown. No invoice sits in this repo.

A copy of this runbook into `operations/` is out of this half.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| Line B1 designed 0 and 0 | 0C envelope | Replay adds no live token by design | A dollar invoice |
| `event=replay_tokens` after Half B | stdout | The replay hit wrote 0 and 0 | Azure usage |
| `event=replay_miss` plus the two fields | stdout | The miss wrote 0 and 0 | A cost floor |
| Synthetic 0.603 hours | 0C FinOps baseline | The legacy tool emitted that field | Model cost |

Numeric cost floors stay Unknown. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

This half adds no live model call. Line B1 actual is 0 prompt tokens and 0 completion tokens for the shown replay-hit query. Honesty: REAL for that path. Lines B2 to B7 stay Unknown. Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED. This half claims no dollar benefit. **Verified Fact.** FD-19. BO-11 stays PROPOSED.

---

## Commands

```text
python -m pytest tests/platform/test_phase13_finops.py -q --tb=short
```

```text
python -m pytest tests/platform/test_phase13_finops.py -v --tb=short
```

Measured result. Honesty: REAL.

```text
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE
plugins: anyio-4.14.1, devtools-0.12.2, langsmith-0.4.43
collecting ... collected 5 items

tests/platform/test_phase13_finops.py::test_hb32_01_before_replay_hit_has_no_prompt_tokens SKIPPED [ 20%]
tests/platform/test_phase13_finops.py::test_hb32_01_before_snapshot_is_recorded PASSED [ 40%]
tests/platform/test_phase13_finops.py::test_hb32_01_after_replay_hit_emits_replay_tokens PASSED [ 60%]
tests/platform/test_phase13_finops.py::test_hb32_01_after_replay_miss_adds_token_fields PASSED [ 80%]
tests/platform/test_phase13_finops.py::test_hb32_01_cited_answer_is_not_replay_miss PASSED [100%]

======================== 4 passed, 1 skipped in 7.27s =========================
```

---

## What this file does not do

This file named the B1 actual. Half B wrote the two zero fields and recorded HB-32-01. This file does not start sub-stage 33. It does not call Azure. It does not invent a token total. It does not invent a dollar actual. It does not sign BO-11. It does not update a tracker.
