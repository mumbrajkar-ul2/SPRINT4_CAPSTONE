# Jobs to be done

| Field | Value |
|---|---|
| Stage | Phase 0 / 3 Frame problem and value |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `docs/business-context.md`; `Project_Intent.md` sections 3, 10, and 15; `Execution_Plan.md` sections 3 and 8; `Decision_Tracker.md` section 7 |
| Assumptions | These jobs are current-state work plus the demo jobs the brief already named |
| Unresolved issues | Time-on-task for each job is Unknown. The baseline tools do not emit it |
| Residual risks | Turning every job into a model task before Phase 2 would ignore the deterministic jobs |

Each job says who acts, what they are trying to finish, and what "done" means. No product name is required.

## Current-state jobs

| ID | Actor | Job | Done when | Evidence |
|---|---|---|---|---|
| J1 | External source / partner | Send a lot, recipe, metrology, or yield message | The message has arrived with its source time | `docs/business-context.md` step 1 |
| J2 | Integration | Reconcile or import the message | The case or feed row exists. A replay is visible | `docs/business-context.md` step 2; BP2 |
| J3 | Operations user | Prioritize the queue | The next case to touch is chosen | `docs/business-context.md` step 3 |
| J4 | Reviewer or engineer | Record a decision | Status, owner, and note sit on the case | `docs/business-context.md` step 4 |
| J5 | Finance and operations | Review monthly measures | A count and a cost for the month exist | `docs/business-context.md` step 5 |
| J6 | On-call staff | Recover from an outage or a late feed | Totals agree or the dispute has an owner | INC-2025-014 |

## Decision jobs the defects force

| ID | Actor | Job | Done when | Linked problem |
|---|---|---|---|---|
| J7 | Process engineer | See both recipe revisions and their times | The mismatch is visible and routed | BP1 |
| J8 | Operations analyst | Tell a replay from a new delivery | The duplicate is marked and confirmed | BP2 |
| J9 | Reviewer | Keep event time and arrival time apart | Both times are shown | BP3 |
| J10 | Policy owner | Handle overlapping or silent rules | The case waits for a person | BP4, BP6 |
| J11 | Any reader | Treat feed text as data | An "approve" note does not close the case | BP7 |
| J12 | Operations lead | Assign an owner when none exists | A name is recorded | BP8 |

## Demo jobs already required

**Verified Fact.** `Project_Intent.md` section 15.2. The live defence must show J7 to J12 as scenarios 7 to 13 on both future applications.

## Jobs that stay human

**Verified Fact.** BO-03 working answer and `Project_Intent.md` section 10.2. A record-changing action is a human job. Numeric KPI math is a deterministic job. Those jobs are not assigned to a model on this page.

## Unknowns

Time to finish J1 to J12 on the packaged data is Unknown. Exception cycle time is Unknown. Aged backlog age threshold is Unknown. Do not invent those numbers.
