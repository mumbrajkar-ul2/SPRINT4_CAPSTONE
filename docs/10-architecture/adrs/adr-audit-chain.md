# ADR: audit chain

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | ACCEPTED for the locked idea. Row schema OPEN for Phase 10 (FD-23 PENDING). |
| Evidence sources | `Execution_Plan.md` section 4, Phase 10, and section 11; `docs/09-initial-prd/nfrs.md`; `Decision_Tracker.md` FD-06, FD-23 |
| Assumptions | Sprint 3 S05-14 is the named practice being reused: a correlation-id audit chain. The default in the tracker holds until Phase 10 designs the schema. |
| Unresolved issues | FD-23 PENDING for Phase 10: the correlation-id row schema and the read-by-correlation-id path. Column names, file path, and table name stay Unknown. |
| Residual risks | Inventing the column list in this ADR would skip FD-23. Logging only to stdout would fail the end-to-end read. |

This ADR records the locked audit-chain idea. It does not invent the row schema.

---

## Decision (locked idea)

**Verified Fact.** `Execution_Plan.md` section 4. `Decision_Tracker.md` FD-23 default.

- Every agent step writes one audit row.
- Every human approval writes one audit row.
- Each row carries a correlation id.
- A read by that correlation id returns the full trace for one case.

This is the Sprint 3 S05-14 practice.

**Verified Fact.** FD-23 status is PENDING. Phase is 10. This unit records the idea. It does not design the columns.

---

## What stays open for Phase 10

The following are Unknown in this ADR. Phase 10 Half A designs them under FD-23.

| Open item | Why it stays open |
|---|---|
| Column list | FD-23 is the schema decision |
| Table or file name | Phase 10 output path is `apps/app_a/audit/`. The inner schema is not named here |
| How the correlation id is minted | Not in `Execution_Plan.md` section 4 |
| Retention and redaction | Phase 12 and Phase 13 concerns |
| Whether Application B writes to the same store | Inference: the same idea applies. The file layout is later |

This ADR does not fill those cells.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected |
|---|---|---|
| Application log lines only | Print steps to stdout or a rotating log | Lines mix across cases. A read by one id is not guaranteed. Rotation can drop the demo trace |
| One row per case | A single summary at the end | The steps inside the case, and the human approval as its own row, would be missing |
| Distributed tracing with no correlation-id key on the audit row | Spans in a viewer | Section 4 requires the id on the audit row and a read that returns the full trace |
| Invent the column list in Phase 4 | Freeze schema now | FD-23 is a Phase 10 decision. The coordinator's instruction is to mark the schema open |
| No audit chain | Rely on the UI screenshot | Guideline 18 and Intent 11.3 need a stored trace a reader can open. A screenshot of the UI does not return the step list |
| Model-written audit text as the only record | A paragraph from the language model | The chain must be one row per step written by the application, not a summary the model can omit |

Worked example. Minutes 13 to 25 run an investigation. The plan step writes a row. Each read-only tool call writes a row. OPA writes a row. `interrupt()` wait writes a row. RT-02 approval writes a row. One correlation id ties those rows. A later read returns that list in order.

The example names the events. It does not name columns.

---

## Why this wins for a laptop demo

Minutes 36 to 39 restart a waiting approval. The audience then needs to see that the same case is still the same case. A correlation id on every row is the join key.

Scenario 13 differences also need a traceable id on Application B's lineage view. `Execution_Plan.md` Phase 11 sub-gate: the lineage view shows the correlation id.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Schema invented here | Status line: schema OPEN for Phase 10 |
| Missing rows on BLOCK | Phase 10 sub-gate: every agent step and approval writes a row |
| PII in the chain | Records are synthetic (FD-02). Redaction design still later |
| Two apps, two id formats | Phase 10 design must pick one id scheme. Not picked here |

---

## Cost and token or runtime impact

Writing one local row per step is disk I/O. It adds no model tokens.

Asking the model to summarise the trace would add tokens and could drop a step. That option is rejected.

Honesty: row counts per case are Unknown until Phase 10 measures them.

---

## Portability lesson

Give every agent step and every human approval one correlation id. Offer a read that returns the whole list. Log lines without that id leave the steps of one case mixed with other cases.

Leave the column list to the phase that builds the writer. Freezing columns in the architecture phase forces a rewrite when the agent graph is designed.

---

## Finding

**Finding.** The locked idea is one audit row per agent step and per human approval, keyed by a correlation id, with a full-trace read. The row schema is open for Phase 10.
**Evidence.** `Execution_Plan.md` section 4. FD-23 PENDING.
**Impact.** Phase 10 Half A designs the schema. Phase 10 Half B writes `apps/app_a/audit/`.
**Risk.** A Phase 4 column list would skip FD-23.
**Confidence.** High on the idea. Unknown on the schema.
**Open questions.** FD-23 schema. Id minting. Application B store layout.

---

## What this ADR does not do

This ADR does not invent the row schema. It does not write audit code. It does not start Phase 10. It does not sign a Business Owner row.
