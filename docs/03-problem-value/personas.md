# Personas

| Field | Value |
|---|---|
| Stage | Phase 0 / 3 Frame problem and value |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `Project_Intent.md` section 3.2; `docs/business-context.md`; `Decision_Tracker.md` section 7; `docs/correspondence/operations-vs-risk-2024.md`; `operations/incidents/INC-2025-014.md` |
| Assumptions | Each persona is a role, not a named employee |
| Unresolved issues | Company job titles and named people are Unknown |
| Residual risks | Giving a persona a fictional first name would look like an invented owner |

These personas are roles. No personal name is assigned.

## P1 Fab operations lead

**Job.** Keep the exception queue moving and keep lot holds visible.

**Verified Fact.** `Project_Intent.md` section 3.2. Cares about throughput, handling time, and case quality.

**Pain.** Open and closed mean different things. A replay inflates the queue. A night report can disagree with the day report.

**Success signal.** Exception cycle time and aged backlog, once those measures exist. Values today: Unknown.

## P2 Exception reviewer

**Job.** Dispose one case. Read the lot, the tool, the recipe, and the evidence.

**Verified Fact.** Run-time role Fab Exception Reviewer (RT-01).

**Pain.** Four programs can mark the same case differently. Documents and feeds can tell the reader to approve.

**Success signal.** A disposition with evidence and a recorded actor.

**Gap.** Company title Unknown. Person Unknown.

## P3 Process engineer

**Job.** Judge a recipe mismatch and an engineering hold.

**Verified Fact.** Run-time role for RT-03. Domain quality and engineering in `Project_Intent.md` section 3.2.

**Pain.** `domain-profile.json` records that a recipe revision field differs between dispatch and equipment systems.

**Success signal.** The two revisions and their effective times are visible. The engineer approves or holds.

**Gap.** Person Unknown.

## P4 Integration lead

**Job.** Get partner and MES messages in without silent duplicates.

**Verified Fact.** `Project_Intent.md` section 3.2.

**Pain.** INC-2025-014. Delayed feed, retried queue, spreadsheet recovery, owner unknown.

**Success signal.** Replay is detected. A late event keeps its two clocks.

## P5 Finance partner

**Job.** Explain case cost and the month-end count.

**Verified Fact.** `Project_Intent.md` section 3.2 and the 2024 correspondence.

**Pain.** Finance and operations have not agreed the cut-off or what "resolved" means.

**Success signal.** Comparable definitions. No invented dollar benefit.

## P6 Risk and security partner

**Job.** Know who could see a case and who approved a change.

**Verified Fact.** `Project_Intent.md` section 3.2. `app/server.py` has no authentication.

**Pain.** Anyone who can reach the port can read cases. Approvals are not enforced in the current API.

**Success signal.** Identity, an audit row, and a human approval on a record change. Those are later work.

## P7 Enterprise application owner

**Job.** Keep the service runnable and recoverable.

**Verified Fact.** `Project_Intent.md` section 3.2.

**Pain.** Historical SLOs are unmeasured. Compose starts a write-capable bridge.

**Success signal.** A start command, a health check, and a rollback plan. Those are later work.

## What this file does not do

It does not invent a name, an age, or a quote that is not in the sources.
