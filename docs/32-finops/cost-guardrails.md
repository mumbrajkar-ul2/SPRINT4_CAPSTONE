# Cost guardrails

| Field | Value |
|---|---|
| Stage | Phase 13 / 32 FinOps and token efficiency. Half B measured results. SC-32-01 / HB-32-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-32b-doc-20261018-001 |
| Status | MEASURED. SC-32-01 writes `prompt_tokens=0` and `completion_tokens=0` on Application A query under replay. HB-32-01 before and after are REAL. B1 is REAL for that path. B2 to B7 stay Unknown. BO-11 stays PROPOSED. |
| Evidence sources | FD-19; BO-11; `apps/app_a/routes/query.py`; `apps/app_a/intelligence/generate.py`; `apps/app_a/intelligence/azure_client.py`; `apps/shared/jsonlog.py`; `docs/31-observability/ai-telemetry-spec.md`; `docs/31-observability/telemetry-results.md`; `docs/00-preflight/ai-economics/provisional-token-budget.md`; `docs/19-intelligence/model-configuration.md`; `tests/platform/test_phase13_finops.py`; `baseline-vs-actual-token-analysis.md` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset. One `docker compose up` still starts the seven named containers. Host ports stay 8080, 8090, 8091, 8092, 8100, 8110. BO rows that are PROPOSED stay PROPOSED. |
| Unresolved issues | Numeric cost floors stay Unknown. Unit price stays Unknown. Application B token line stays unbuilt. Company titles and the signer stay Unknown. |
| Residual risks | A field named `token` is dropped. A dollar cutoff written into code would invent Business Owner policy. Calling Azure from Half B would leave replay. |

This file names the stop rules for token and cost claims, and the one small Half B write. Half B added no feature. Half B added no cost screen. Half B added no dollar cutoff. Measured cells for HB-32-01 live in `baseline-vs-actual-token-analysis.md`.

Engineering decision ED-P13-32A-01, authority: team-force. Control id `SC-32-01`. Check id `HB-32-01`. Application A `POST /api/query` under `MODEL_MODE=replay` writes `prompt_tokens=0` and `completion_tokens=0`.

Engineering decision ED-P13-32A-02, authority: team-force. Field names are `prompt_tokens` and `completion_tokens`. The field name `token` stays forbidden.

Engineering decision ED-P13-32A-07, authority: team-force. Numeric cost floors stay Unknown. `max_tokens` 800 stays an Azure client cap. It is not measured spend and not Business Owner policy.

Engineering decision ED-P13-32A-09, authority: team-force. Half B does not call Azure. Half B does not write a unit price. Half B does not change `generate()` to open a socket. Half B does not add a cost dashboard.

Engineering decision ED-P13-32A-10, authority: team-force. Application B query stays as built. This half names one control on Application A.

---

## Finding

**Finding.** After SC-32-01, Application A `POST /api/query` under replay writes `prompt_tokens=0` and `completion_tokens=0`. A replay hit uses `event=replay_tokens`. A replay miss keeps `event=replay_miss` and adds those two fields. A cited answer is not a miss. HTTP bodies stay as built. `jsonlog.emit` still drops `token`. Azure stays uncalled. B1 is 0 and 0. Honesty: REAL for that shown path.
**Evidence.** Live before probe on 2026-10-18. Live after pytest `tests/platform/test_phase13_finops.py`. Correlation id `corr-p13-32b-doc-20261018-001`. Honesty: REAL.
**Impact.** The two zeros are grep-able on stdout. HTTP bodies stay as built.
**Risk.** Emitting `token=0` would drop the field. Setting `MODEL_MODE=azure` would open a public-network socket.
**Confidence.** High on the measured hit line and the miss fields. Unknown on live Azure usage.
**Open questions.** Reviewer grades HB-32-01. Application B token line.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric cost floors stay Unknown. This half invents no percent and no dollar benefit.

**Verified Fact** of BO-11 working answer. Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit. The row stays PROPOSED. The signer name stays Unknown.

**Verified Fact.** FD-13. Compose default `MODEL_MODE=replay`. JSON logs are one object per line on stdout.

**Verified Fact** of ED-P13-31A-08. Prompt and completion counts use names `prompt_tokens` and `completion_tokens`. On replay those two counts are 0.

---

## Guardrail list

| Id | Rule | What Half B does |
|---|---|---|
| GR-32-01 | Keep `MODEL_MODE=replay` | Do not set `azure` |
| GR-32-02 | Do not call Azure | Leave `complete_azure` uncalled |
| GR-32-03 | Write `prompt_tokens` and `completion_tokens`, not `token` | Two integer fields on stdout |
| GR-32-04 | Label B1 REAL only for the shown replay path | One Application A query |
| GR-32-05 | Leave B2 to B7 Unknown | No guessed rehearsal count |
| GR-32-06 | Leave dollars Unknown | No unit price. No $0.00 actual |
| GR-32-07 | Leave BO-11 PROPOSED | No monetary benefit sentence |
| GR-32-08 | Add no feature | No cost screen. No second listener. No Application B emit |

Worked example for GR-32-03. A line `{"event":"replay_tokens","token":0}` loses the count. A line `{"event":"replay_tokens","prompt_tokens":0,"completion_tokens":0}` keeps the count.

Worked example for GR-32-06. Replay spent 0 live tokens. Dollar spend stays Unknown because no invoice exists. Do not write $0.00 as REAL.

---

## The one small control Half B puts in code

Control id **SC-32-01**. Name: write replay token zeros on Application A query.

File: `apps/app_a/routes/query.py`.

When `generate()` returns and `model_mode` is `replay`:

1. If `error_class` is `replay_miss`, add `prompt_tokens=0` and `completion_tokens=0` to the existing `event=replay_miss` emit.
2. If `error_class` is not `replay_miss`, emit one new line `event=replay_tokens` with `service=app-a`, `model_mode=replay`, `prompt_tokens=0`, `completion_tokens=0`, `path=/api/query`, `status=200`, and the request `correlation_id`.

HTTP body fields stay as built. `generate()` stays on replay. Azure stays uncalled.

Check id **HB-32-01**.

Before SC-32-01:

- `POST /api/query` with question `Which port does the Context Lake REST listener use?` and header `X-Correlation-Id: corr-p13-32b-doc-20261018-001`.
- HTTP 200. `verdict` `ANSWER`. Citation `arch.listener.lake_rest_8091`. `error_class` null.
- Stdout has `event=request_ok` for that id. No line has `prompt_tokens`.
- Honesty: REAL.

After SC-32-01:

- The same POST still returns HTTP 200 and the same citation.
- Stdout has one line with `prompt_tokens=0`, `completion_tokens=0`, and `model_mode=replay`.
- `event` on that line is `replay_tokens`.
- Azure is not called.
- Honesty: REAL.

Negative case: a miss question still returns `event=replay_miss`. After Half B that miss line also carries `prompt_tokens=0` and `completion_tokens=0`. HTTP stays 200 with `verdict` `ABSTAIN`. Honesty: REAL.

`baseline-vs-actual-token-analysis.md` writes B1 actual as 0 and 0. Honesty: REAL for that replay path. Lines B2 to B7 stay Unknown.

Pytest path: `tests/platform/test_phase13_finops.py`. Half B did not add a product route.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-32-01 | B1 is filled without the stdout line | A designed 0 with no proof | Wait for HB-32-01 |
| FM-32-04 | `MODEL_MODE=azure` is set to fill a cell | A public-network socket can open | Keep `MODEL_MODE=replay` |
| FM-32-05 | Field name `token` is emitted | The field is missing on stdout | Use `prompt_tokens` and `completion_tokens` |
| FM-32-13 | $0.00 is written as REAL | A dollar actual | Leave dollars Unknown |
| FM-32-15 | Application B is edited in this half | A second emit | Leave Application B as built |

Dead-letter parking stays on invalid intake. SC-32-01 does not park a query. The token line is written on the same request.

---

## Dead-letter queue and replay

Language-model replay stays `MODEL_MODE=replay`. Files live under `operations/model-replay/` and are named by the SHA-256 hash of the prompt. A miss abstains. A hit plays the saved body. Both stay at 0 live tokens. Intake replay stays in `dlq.py` and is unchanged.

---

## Runbook — stay inside the guardrails

1. Confirm `MODEL_MODE` is `replay` on Application A.
2. Confirm Azure variables stay unset.
3. Run the HB-32-01 question on port 8100 with the three identity headers and `X-Correlation-Id: corr-p13-32b-doc-20261018-001`.
4. Read stdout for `prompt_tokens` and `completion_tokens`.
5. Write 0 and 0 onto B1 only.
6. If a person asks for a dollar figure, leave the cell Unknown.
7. If a person asks for a live Azure count, leave B2 to B7 Unknown.

A copy of this runbook into `operations/` is out of this half.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| `event=replay_tokens` after Half B | stdout | The replay hit wrote 0 and 0 | A dollar invoice |
| `event=replay_miss` plus the two fields | stdout | The miss wrote 0 and 0 | Azure usage |
| `model_mode=replay` on that line | stdout | The process used replay | An availability percent |
| Line B1 after Half B | `baseline-vs-actual-token-analysis.md` | Measured replay tokens against the 0C envelope | A cost floor |

Numeric cost floors stay Unknown. **Verified Fact.** FD-19.

---

## Cost and the 0C envelope

SC-32-01 adds no live model call. Token line B1 in `docs/00-preflight/ai-economics/provisional-token-budget.md` is designed as 0 prompt tokens and 0 completion tokens when `MODEL_MODE=replay`. Half B measured that pair as 0 and 0 on the shown replay-hit query. Honesty: REAL for that path. Lines B2 to B7 stay Unknown. Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED. This half claims no dollar benefit. BO-11 stays PROPOSED.

---

## What this file does not do

This file named the stop rules. Half B wrote SC-32-01 and recorded HB-32-01. This file does not start sub-stage 33. It does not call Azure. It does not invent a dollar cutoff. It does not sign BO-11. It does not update a tracker.
