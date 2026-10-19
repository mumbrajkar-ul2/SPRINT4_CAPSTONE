# Close paths for DEV-010 through DEV-020

| Field | Value |
|---|---|
| Stage | Phase 18 / Remaining deviations. Half A. |
| Date / version | 2026-10-19, v1.0 |
| Author / agent | Executor agent (Grok 4.7), correlation id corr-p18a-doc-20261019-001 |
| Status | DESIGN. Half B builds each row after this file. |
| Evidence sources | `Deviations_From_Original_Execution_Plan.md`; `playbook/phase_18_remaining_deviations.md`; FD-26 |
| Assumptions | Phase 17 has built the React pages and the session overlay before these rows close. |
| Unresolved issues | A federated identity provider, a company vault, and a company image-signing service stay unnamed. |
| Residual risks | A process kill on a live port stays NEEDS_HUMAN when Compose is not already up. The checkpoint file is the proof Half B can run without that live kill. |

The Application B kill uses correlation id `corr-p18-kill-20261019-001`. It does not reuse `corr-p10b-kill-20261018-001`.

## DEV-010

Copy the pause pattern into Application B. Tools read the lake. `interrupt()` stores the pause in `apps/app_b/runtime/checkpoints.sqlite3`. Resume requires a different person from `proposed_by`.

Done test. A run pauses, the checkpoint file exists, and a resume with the same person as `proposed_by` is refused.

## DEV-011

Start that pause, drop the in-memory graph, open the same checkpoint file again, and read `corr-p18-kill-20261019-001`. A live `taskkill` of the Application B process stays NEEDS_HUMAN when Compose is not up.

Done test. After the graph is rebuilt from the checkpoint file, the waiting approval and `corr-p18-kill-20261019-001` are still on the case.

## DEV-012

Add three read-only jobs beside investigation: change-impact analyst, evidence-pack assembler, and operational handoff. Each job has a tool list, one waiting role, and one audit row. The model has no write tool.

Done test. Each job returns its tool list, its waiting role, and one audit row.

## DEV-013

A case read with no `X-Api-Key` fails. A case read with the demo key and a role succeeds. The React page shows that rejection in words. A federated identity provider stays unnamed.

Done test. The anonymous call fails. The keyed call succeeds.

## DEV-014

Run `.github/workflows/verify.yml` once, or the same steps locally when GitHub is not available, and save the log under this folder. A failed test fails the job. Do not add a second CI product.

Done test. `docs/44-remaining-deviations/verify-log.txt` exists and a failed check is a failed job.

## DEV-015

One scenario click writes one JSON log line that contains the correlation id. Do not add a new metrics product.

Done test. That line is present for one scenario click.

## DEV-016

Record the image digest from the Phase 17 image build, and read the demo API key from a gitignored file path. A company signing service and a company vault stay unnamed.

Done test. `docs/44-remaining-deviations/image-digest.md` names the digest and the gitignored path. The company services stay unnamed.

## DEV-017

Add one definition each for lot, wafer, tool, chamber, recipe revision, metrology sample, engineering change, replay, and approval when a term is missing. Metric rows show population, event time, ingestion time, window, exclusions, status, unit, and owner. A cell with no signed owner stays Unknown and still shows the field name. Rebuild through the review loop and raise the version. Phase 17's pin stays the record of that phase.

Done test. Each term has one definition. The metric field list is visible. Unknown stays Unknown.

## DEV-018

Answer five questions from the `edges` table: lots on a recipe revision, tools and metrology for an excursion, the policy in force at event time, the documents and code for that policy, and the changes that affect a workflow. Each answer cites an edge. New links are statements with a locator.

Done test. The five answers each cite an edge.

## DEV-019

A button receives one message from port 8090 and places it on the session queue. The queue count rises by 1. The message id on the page matches the gateway body. This is separate from the DEV-003 replay of ref `C00001646`. The packaged store is unchanged.

Done test. The queue count rises by 1 and the message id matches.

## DEV-020

The same injection post runs on port 8100 and port 8110. Both return BLOCK. Case status and approvals stay as they were. The React page has one Injection button. The OPA rules already used for this block stay as they are.

Done test. Both posts return BLOCK. Case status and approvals stay as they were.
