# FinOps model

| Field | Value |
|---|---|
| Stage | Phase 13 / 32 FinOps and token efficiency. Half B measured results. SC-32-01 / HB-32-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-32b-doc-20261018-001 |
| Status | MEASURED. Bucket 1 on the shown Application A replay query is 0 and 0. Honesty: REAL for that path. B2 to B7 stay Unknown. BO-11 stays PROPOSED. 4982.61 and 0.603 stay SIMULATED. |
| Evidence sources | FD-19; FD-02; FD-04; BO-11; `docs/00-preflight/ai-economics/provisional-token-budget.md`; `docs/00-preflight/ai-economics/preliminary-finops-baseline.md`; `docs/00-preflight/ai-economics/workload-assumptions.md`; `docs/08-ai-qualification/economics-baseline-reconciliation.md`; `Execution_Plan.md` sections 9 and 10; `docs/31-observability/ai-telemetry-spec.md`; `apps/shared/jsonlog.py`; `tests/platform/test_phase13_finops.py`; `baseline-vs-actual-token-analysis.md` |
| Assumptions | `MODEL_MODE=replay`. This model meters Application A query first. Application B stays as built. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | Unit price stays Unknown. Lines B2 to B7 stay Unknown. Numeric cost floors stay Unknown. |
| Residual risks | Building a cost screen would add a feature. Mixing delivery tokens with case tokens would break A-W1. Signing an ROI number here would skip Phase 14 and BO-11. |

This file names the cost model the other five pages use. FinOps here is the token and cost record for the laptop stack. The model has four buckets, one meter, one honesty rule, and one Half B write. It invents no unit price. Half B wrote bucket 1 as 0 and 0 on the shown Application A replay query.

Engineering decision ED-P13-32A-04, authority: team-force. Four buckets. Bucket 1 is live model tokens. Bucket 2 is synthetic legacy labor and amount. Bucket 3 is delivery-agent tokens. Bucket 4 is laptop and cloud compute. This sub-stage meters bucket 1 on the Application A replay path only.

Engineering decision ED-P13-32A-08, authority: team-force. Company titles and the signer stay Unknown. BO-11 stays PROPOSED. No dollar benefit is written.

---

## Finding

**Finding.** The 0C envelope already named the token lines, the synthetic money fields, and the honesty labels. Phase 2 kept three GenAI capabilities and retired four code capabilities. Application A logs JSON lines on stdout. `jsonlog.emit` drops a field named `token`. After HB-32-01 a replay hit writes `event=replay_tokens` with `prompt_tokens=0` and `completion_tokens=0`. A replay miss adds those two fields to `event=replay_miss`. B1 is REAL for that shown path. Dollars stay Unknown.
**Evidence.** Five 0C files. Phase 2 reconciliation. `query.py` after SC-32-01. `tests/platform/test_phase13_finops.py`. `FORBIDDEN_KEYS`. FD-19. BO-11. Honesty: REAL for the two zeros.
**Impact.** Later Phase 14 may use those zeros as the replay actual. Dollars stay Unknown.
**Risk.** A later author who treats this model as a signed finance system would invent a company process.
**Confidence.** High on the four buckets and the measured replay zeros. Unknown on unit price.
**Open questions.** Who later records an invoice. Application B meter.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric cost floors stay Unknown. Replay is the path when the live model is off.

**Verified Fact.** FD-04. Only conflict explanation, natural-language query, and agentic planning carry a GenAI token line.

**Verified Fact.** FD-02. The model has no write tool.

**Verified Fact** of BO-11 working answer. ROI is EDUCATIONAL. Claim no monetary benefit. The row stays PROPOSED.

**Verified Fact.** `Execution_Plan.md` section 9. Cost honesty is REAL when tokens and spend are measured.

---

## Four buckets

| Bucket | What it holds | How it is filled on this laptop | Honesty |
|---|---|---|---|
| 1. Live model tokens | Prompt tokens and completion tokens on query, explain, draft, and agent draft | Measured 0 and 0 on the shown Application A query | REAL for that replay path |
| 2. Synthetic legacy fields | `mean_amount` 4982.61 and `hours_per_case` 0.603 | Already emitted by `app/baseline.py` | SIMULATED |
| 3. Delivery-agent tokens | Coordinator, executor, and reviewer in Cursor | Off the case meter. Count Unknown | Assumption A-W1 |
| 4. Laptop and cloud compute | Host CPU, Docker images, a later cloud bill | Unknown | Unknown |

Worked example. One Application A query under replay wrote bucket 1 as 0 and 0. Honesty: REAL. Bucket 2 still shows 4982.61 as the synthetic mean amount. Honesty: SIMULATED. Those two figures sit in different buckets. They are not added together.

---

## Meter

| Rule | Value | Authority |
|---|---|---|
| Field names | `prompt_tokens`, `completion_tokens` | team-force, ED-P13-32A-02 |
| Forbidden field name | `token` | `FORBIDDEN_KEYS`. Verified Fact |
| Unit of a write | One Application A `POST /api/query` that called `generate()` | team-force, ED-P13-32A-01 |
| Replay value | 0 and 0 | FD-19. REAL after HB-32-01 for the shown path |
| Azure value | Unknown | Unknown |
| Join key | `correlation_id` on the stdout line. `case_id` when the request sent one | FD-13 event record |
| Event on a hit | `replay_tokens` | team-force, ED-P13-32A-01 |
| Event on a miss | Existing `replay_miss` plus the two fields | team-force, ED-P13-32A-01 |

A token is one piece of text the language model reads or writes. Prompt tokens are the pieces sent in. Completion tokens are the pieces written out.

Half B does not add a metrics product. The person reads container stdout or a pytest capture. **Verified Fact** of the Phase 31 store rule.

---

## Honesty and ownership

| Claim type | Who owns it | Status on this laptop |
|---|---|---|
| Replay token pair 0 and 0 | Team-Force engineering | REAL after HB-32-01 for the shown path |
| Numeric cost floor | Team-Force may not invent one. FD-19 | Unknown |
| Unit price | A recorded invoice or a recorded list price | Unknown |
| ROI and monetary benefit | Business Owner on BO-11 | PROPOSED. EDUCATIONAL later. No benefit written here |
| Company title and signer | Business Owner | Unknown |
| Headline business KPIs | BO-02 | PROPOSED. Cycle time and aged backlog stay Unknown |

Worked example. Half B may write `prompt_tokens=0`. Half B may not write "this saved 12 dollars." The second sentence is a benefit claim. BO-11 leaves that claim unsigned.

---

## How later pages roll numbers up

| Page | Roll-up | What stays Unknown |
|---|---|---|
| `baseline-vs-actual-token-analysis.md` | B1 actual 0 and 0 from the shown replay query | B2 to B7. Total. Dollars |
| `cost-per-case.md` | Sum of bucket 1 turns for one `case_id` | Dollars per case |
| `cost-per-outcome.md` | Bucket 1 turns on one of S7 to S13 | Dollars per scenario. ROI |
| `token-leakage-analysis.md` | Extra or hidden bucket 1 spend | Live Azure leak size |
| `cost-guardrails.md` | The one write and the stop rules | A dollar cutoff |

Phase 14 compares after-intervention cost with this envelope. Honesty on that later cost is REAL only when tokens and spend are measured. Spend stays unmeasured in this half.

---

## Failure modes and recovery

| Id | What failed | What the person sees | Recovery |
|---|---|---|---|
| FM-32-02 | A public price is copied into bucket 1 | A dollar total | Leave unit price Unknown |
| FM-32-06 | Bucket 2 is added to bucket 1 | 4982.61 next to 0 tokens | Keep the buckets apart |
| FM-32-09 | Bucket 3 is added to a case | Cursor tokens on B1 | Keep A-W1 |
| FM-32-11 | Bucket 1 zeros are called a saving | A benefit sentence | Write the zeros. Leave dollars Unknown |

Dead-letter parking stays on invalid intake. The cost model does not park a quiet meter. Half B writes the two fields so the meter is visible.

---

## Dead-letter queue and replay

Replay files in `operations/model-replay/` are the model path. Dead-letter rows in `apps/app_a/runtime/dlq.sqlite3` are the intake path. The model path is the only path this meter writes. Both paths stay at 0 live model tokens on this laptop.

---

## Runbook — apply this model

1. Classify the number into one of the four buckets.
2. If it is bucket 1 and mode is replay, read 0 and 0 from stdout after HB-32-01.
3. If it is bucket 2, keep the SIMULATED label.
4. If it is bucket 3 or 4, leave the cell Unknown unless a later measured run exists.
5. If the sentence claims a monetary benefit, stop. BO-11 stays PROPOSED.

---

## SLOs and observability

This model sets no cost SLO. Phase 31 left API p95, availability, and error budget Unknown. This half leaves those cells Unknown. The proof for bucket 1 is the stdout pair `prompt_tokens` and `completion_tokens`.

---

## Cost and the 0C envelope

This model is the Phase 13 read of the five 0C files plus the Phase 2 reconciliation. It does not edit those files. Line B1 is the only cell Half B labelled REAL, and only for the shown replay path. This half claims no dollar benefit. BO-11 stays PROPOSED.

---

## The one small Half B check

See `cost-guardrails.md` SC-32-01 and HB-32-01. Half B implemented the meter write. Measured cells live in `baseline-vs-actual-token-analysis.md`. Half B did not add a cost screen. Half B did not add a second bucket.

---

## What this file does not do

This file named the four buckets. Half B wrote the meter. This file does not start sub-stage 33. It does not call Azure. It does not invent a unit price. It does not sign BO-11. It does not update a tracker.
