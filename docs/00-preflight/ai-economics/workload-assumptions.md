# Workload assumptions

| Field | Value |
|---|---|
| Stage | Phase 0 / 0C AI-economics envelope |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL. Reconcile at Phase 2 and Phase 13 |
| Evidence sources | `Execution_Plan.md` header, section 4, section 8, and section 10; `Project_Intent.md` sections 14 and 15; `PRELOADED_DATA.md`; `app/baseline.py` output 2026-10-18; `app/workshop_check.py` output 2026-10-18 |
| Assumptions | Every numeric token or dollar figure that is not measured is Assumption or Unknown. None is a Verified Fact |
| Unresolved issues | Tokens per case, model unit price, and live API latency are Unknown |
| Residual risks | A later FinOps page could copy these working assumptions as measured cost |

This page states the workload this envelope covers. Reconcile it at Phase 2 (AI versus no-AI) and Phase 13 (FinOps).

## Measured operational volume

These numbers came from the baseline tools. Honesty label follows `Execution_Plan.md` section 9 where a family applies.

| Measure | Run 1 | Run 2 | Diff | Honesty | Label |
|---|---:|---:|---|---|---|
| Case records | 125 | 125 | Match | REAL | Verified Fact from `python -m app.baseline` |
| Open cases (`status != CLOSED`) | 89 | 89 | Match | REAL for the Python status test | Verified Fact from `app/baseline.py` |
| Urgent cases | 2 | 2 | Match | REAL for the Python priority test | Verified Fact |
| Mean amount | 4982.61 | 4982.61 | Match | SIMULATED synthetic money | Verified Fact of the tool output. Not a customer dollar |
| Sites | 6 | 6 | Match | REAL | Verified Fact |
| Hours per case | 0.603 | 0.603 | Match | SIMULATED labor on synthetic costs | Verified Fact of the tool output |
| Partner feeds | 8,567 | 8,567 | Match | REAL row count | Verified Fact from `python -m app.workshop_check` |
| Policy exceptions | 224 | 224 | Match | REAL row count | Verified Fact |
| Upstream outages | 72 | 72 | Match | REAL row count | Verified Fact |

**Verified Fact.** `PRELOADED_DATA.md` says this is the packaged default. It is not the README generator target of 6,000 cases.

## Work this envelope must cover later

**Assumption A-W1.** Delivery work uses Cursor agents on this laptop. Coordinator, executor, and reviewer tokens are delivery cost, not run-time case cost.

**Assumption A-W2.** The live demo uses `MODEL_MODE=replay` (`Execution_Plan.md` section 10). Replay plays saved responses. Live model tokens during a replayed 40-minute demo are 0.

**Assumption A-W3.** Rehearsal before replay records one response per prompt hash. That recording uses live tokens once. The count is Unknown.

**Assumption A-W4.** Evaluation later runs the seven demo scenarios in `Project_Intent.md` section 15.2 on both applications. Scenario count is 7 shared scenarios plus the rule-trace and both-apps compare. Token use per scenario is Unknown.

**Assumption A-W5.** Azure OpenAI is the primary live model path (`Execution_Plan.md` header). Unit prices are Unknown until a bill or a list price is recorded at Phase 13.

**Assumption A-W6.** The model receives read-only tools only (FD-02). There is no write-tool token path.

## What the current tools do not measure

| Needed later | Current tool field | Status |
|---|---|---|
| Exception cycle time | Not in `app/baseline.py` | Unknown |
| Aged backlog | Not in `app/baseline.py` | Unknown |
| Tokens per case | None | Unknown |
| Retrieval tokens | None | Unknown |
| Agent step tokens | None | Unknown |
| API p95 latency | Server was not started | Unknown |
| Model unit price | No invoice | Unknown |

Do not fill those cells with invented numbers.
