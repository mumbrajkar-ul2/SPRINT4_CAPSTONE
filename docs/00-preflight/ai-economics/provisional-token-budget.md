# Provisional token budget

| Field | Value |
|---|---|
| Stage | Phase 0 / 0C AI-economics envelope |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL. Reconcile at Phase 2 and Phase 13 |
| Evidence sources | `Execution_Plan.md` sections 9, 10, and 13; `app/baseline.py` (no token fields); no model invoice |
| Assumptions | Replay demo live tokens are 0. Every other token cell is Unknown |
| Unresolved issues | No measured prompt token, completion token, or embedding token count exists |
| Residual risks | Filling this table with guessed thousands of tokens would create a false budget |

This budget is a placeholder envelope. It exists so Phase 2 and Phase 13 have a place to write measured numbers. It does not invent a token count.

## Budget table

| Line | Purpose | Prompt tokens | Completion tokens | Honesty | Label |
|---|---|---|---|---|---|
| B1 | Laptop demo, replay on | 0 | 0 | REAL if replay is used as designed | Assumption until replay is proven in Phase 15 |
| B2 | Rehearsal record of the 40-minute path | Unknown | Unknown | Unknown | Unknown |
| B3 | Evaluation of S7 to S13 on Application A | Unknown | Unknown | Unknown | Unknown |
| B4 | Evaluation of S7 to S13 on Application B | Unknown | Unknown | Unknown | Unknown |
| B5 | Retrieval / embedding for the lake | Unknown | Unknown | Unknown | Unknown |
| B6 | Delivery agents for later phases | Unknown | Unknown | Unknown | Unknown |
| B7 | Contingency | Unknown | Unknown | Unknown | Unknown |
| **Total** | **Sum of measured lines** | **Unknown** | **Unknown** | **Unknown** | **Unknown** |

## What is forbidden on this page

- A guessed 1,000-token-per-case figure presented as fact.
- A copied public list price presented as a Verified Fact.
- A dollar total derived from Unknown tokens.

## Guardrail

**Verified Fact.** FD-02. The model gets read-only tools only. This budget has no write-tool line.

**Verified Fact.** `app/baseline.py` does not emit tokens. The 2026-10-18 tool runs therefore cannot fill B2 to B7.

## Reconciliation

- Phase 2: drop lines that Phase 2 labels deterministic or ML-rejected.
- Phase 13: write measured tokens and cost per resolved scenario on the surviving lines.
- Phase 14: compare this envelope with the after-intervention cost family. Honesty label for cost is REAL only when the tokens were measured.
