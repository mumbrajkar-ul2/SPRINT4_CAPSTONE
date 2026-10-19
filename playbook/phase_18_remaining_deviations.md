# Phase 18 — Remaining deviations

> Outside the 46 spine units. Decision gate: FD-26. Closes DEV-010 through DEV-020.

Build phase. Two halves. Half A writes one close path and one Done test per row in `docs/44-remaining-deviations/` and stops. Half B builds those closes. The coordinator opens this file only when the Phase 17 gate is PASS. It does not open Phase 0. It does not change a Phase 0 to 16 PASS cell.

## Inputs

- `playbook/STATUS.md` with the Phase 17 gate PASS
- `Deviations_From_Original_Execution_Plan.md` rows DEV-010 through DEV-020
- `playbook/phase_17_demo_ready.md` and `docs/43-demo-ready/`
- `apps/app_a/agent/graph.py` as the pause pattern to copy
- `apps/app_b/` after the React screens exist
- `.github/workflows/verify.yml`
- `Decision_Tracker.md` FD-26
- The Context Lake, for the term list and the edge answers

## Prompt

```text
# Phase 18 — Remaining deviations

## Objective
Close DEV-010 through DEV-020. Each row closes only when its correction check passes.

## Scope
`docs/44-remaining-deviations/`, the Application B pause and restart, three read-only jobs, the rejected anonymous call, one pipeline log, one correlation-id log line, the image digest and a gitignored secrets file, the term list, five edge answers, one successful gateway delivery, and injection BLOCK on both ports. Exclude: a federated identity provider, a company vault, a company image-signing service, a second CI product, and a new metrics product. No such company service was named.

## Sub-stages
- Remaining deviations. `docs/44-remaining-deviations/`.

## Required analysis (Half A)
Write one close path and one Done test for DEV-010 through DEV-020. Name the new correlation id for the Application B kill. Do not reuse `corr-p10b-kill-20261018-001`.
Name the three unnamed external services on the DEV-013 and DEV-016 rows. A missing federated provider, a missing company vault, or a missing company image-signing service does not fail the phase.
STOP after Half A. Return the seven-item final response for Half A. Wait for HALF_A_ACCEPTED.

## Required work (Half B, after acceptance)
1. DEV-010. Copy the pause pattern from `apps/app_a/agent/graph.py` into Application B. Tools read the lake. `interrupt()` stores the pause in `apps/app_b/runtime/checkpoints.sqlite3`. Resume requires a different person from `proposed_by`.
2. DEV-011. Start that pause, kill the Application B process, start it again, and read the same new correlation id.
3. DEV-012. Add three read-only jobs beside investigation: change-impact analyst, evidence-pack assembler, and operational handoff. Each job has a tool list, one waiting role, and one audit row. The model still has no write tool.
4. DEV-013. A case read with no `X-Api-Key` fails. A case read with the demo key and a role succeeds. The React page shows that rejection in words.
5. DEV-014. Run `.github/workflows/verify.yml` once, or the same steps locally when GitHub is not available, and save the log under `docs/44-remaining-deviations/`. A failed test fails the job.
6. DEV-015. One scenario click writes one JSON log line that contains the correlation id.
7. DEV-016. Record the image digest from the Phase 17 image build, and read the demo API key from a gitignored file path.
8. DEV-017. Add lake term items for lot, wafer, tool, chamber, recipe revision, metrology sample, engineering change, replay, and approval, each with one definition. Metric rows show population, event time, ingestion time, window, exclusions, status, unit, and owner. A cell with no signed owner stays Unknown and still shows the field name. Rebuild the lake through the review loop and raise the version. Phase 17's pin stays the record of that phase.
9. DEV-018. Answer the five relationship questions from the `edges` table. Each answer cites an edge. Add lake links where the current edges cannot answer. Those links are statements with a locator, not raw data rows.
10. DEV-019. A button receives one message from port 8090 and places it on the session queue. The queue count rises by 1. The message id on the page matches the gateway body. This is separate from the DEV-003 session replay of ref `C00001646`. The packaged store is unchanged.
11. DEV-020. The same injection post runs on port 8100 and port 8110. Both return BLOCK. Case status and approvals stay as they were. The React page has one Injection button that shows that result. The OPA rules already used for this block stay as they are.

## Evidence rules
Each close cites the file or the response that decided it. Classify claims as Verified Fact, Inference, Assumption, or Unknown. Do not invent a provider name, a vault product, a signing product, a KPI floor, or a dollar benefit.

## Constraints and guardrails
Application B still does not import Application A rule functions and still does not open the packaged sqlite files for a rule decision. `reconcile()` stays off the packaged store. The model still has no write tool. Do not change a Phase 0 to 16 PASS cell. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Start rule | Phase 17 gate is PASS before this phase opens. |
| Pause store | `apps/app_b/runtime/checkpoints.sqlite3` |
| Kill id | A new correlation id for Phase 18. Do not reuse `corr-p10b-kill-20261018-001`. |
| Identity | Demo headers stay. A missing `X-Api-Key` fails the case read. No federated provider. |
| Secrets | Gitignored file path. No company vault. |
| Image | Digest recorded. No company signing service. |
| Telemetry | One JSON log line with the correlation id. |
| Gateway delivery | One successful message on the session queue. Packaged store unchanged. |
| Injection | BLOCK on port 8100 and port 8110. No record change. |

## Decision gate (before you start)
FD-26 is DECIDED. Phase 18 does not add a federated identity provider, a company vault, or a company image-signing service.

## Required artifacts
`docs/44-remaining-deviations/` in Half A. The eleven closes in Half B. Standard header on the docs.

## Completion gate
Half A PASS when each of DEV-010 through DEV-020 has a close path and a Done test in `docs/44-remaining-deviations/`. Half B PASS when each correction check passes and the deviations file marks those rows CLOSED. BLOCKED otherwise.

## Required final response (after each half)
Return the seven items.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/44-remaining-deviations/close-paths.md` (Half A) | Header. One close path and one Done test for DEV-010 through DEV-020. The new kill correlation id. The three unnamed external services. |
| Application B agent (Half B) | `interrupt()` pause, checkpoint file, resume by a different person, and the three read-only jobs. |
| `docs/44-remaining-deviations/verify-log.txt` (Half B) | The pipeline log, or the same steps run locally. |
| `docs/44-remaining-deviations/image-digest.md` (Half B) | The image digest and the gitignored secrets path. Company services stay unnamed. |
| Lake terms and edge answers (Half B) | Nine term definitions, metric fields or Unknown, and five answers that each cite an edge. |
| React pages (Half B) | The anonymous rejection in words, the gateway-delivery button, and the Injection button. |

## Done test

Fail the handoff when Phase 17 is not PASS, or when the first phase file is anything other than `playbook/phase_18_remaining_deviations.md`, or when a Phase 0 to 16 gate cell changed.

The phase passes when each correction check for DEV-010 through DEV-020 passes and `Deviations_From_Original_Execution_Plan.md` marks those rows CLOSED.

A missing federated provider, a missing company vault, or a missing company image-signing service does not fail the phase. Those three stay named as unnamed external services on the DEV-013 and DEV-016 rows.

The click-through on a running stack stays `NEEDS_HUMAN` when Compose is not already up.
