# Stop conditions

| Field | Value |
|---|---|
| Stage | Phase 0 / 0B Provisional operating contract |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL |
| Evidence sources | `Execution_Plan.md` section 11; `Decision_Tracker.md` sections 2, 3, and 6; `playbook/executor.md`; FD-02; `PRELOADED_DATA.md` |
| Assumptions | A stop here means the coordinator holds the next unit. It does not mean the inherited repo is deleted. |
| Unresolved issues | No on-call person is named for a live stop after the apps exist. That owner is Unknown. |
| Residual risks | A builder who continues after a stop will write files the reviewer never accepted. |

These stop rules are PROVISIONAL.

## Stops that hold the delivery

**Verified Fact.** `Execution_Plan.md` section 11 and `Decision_Tracker.md` section 2.

1. A phase ends BLOCKED. The next phase does not start.
2. A PENDING decision in the stage-entry checklist has no accepted default. The phase does not start.
3. The Business Owner rejects a PROPOSED answer. The run pauses.
4. The SME cannot propose an answer for a Business Owner row. The run pauses.
5. The reviewer does not accept the unit. The next unit does not start.
6. A Done test needs a credential or a running service. The run marks `NEEDS_HUMAN` and waits.
7. A policy value is missing. The executor does not invent it. The case routes to HOLD_FOR_REVIEW. The coordinator is asked.

## Stops that protect the inherited repo

**Verified Fact.** FD-01, FD-02, and the Phase 0 unit rules.

1. Any request to edit a file inside `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` before Phase 7. Stop.
2. Any request to run the app in write mode in Phases 0 to 6. Stop. That includes `generate --reset`, `partner_feeds --reconcile`, and `gateway_bridge`.
3. Any request to give the model a write tool. Stop. FD-02 forbids it.
4. Any request to invent a KPI target, a dollar benefit, or an owner name. Stop. Record Unknown or PROPOSED with a named role, not a made-up person.
5. Any request to present an Assumption as a Verified Fact. Stop and relabel.

## Stops inside a live case (later)

**Verified Fact.** BO-03 working answer and `Project_Intent.md` section 10.3.

1. An action would change a record and no human has approved it. The app must not write.
2. An injection or untrusted instruction is detected. The later OPA path returns BLOCK.
3. Two policy scopes disagree. The case routes to review.
4. The governed source is silent on a threshold. The case routes to review (BO-08 working answer).

**Unknown.** The named person who will take a live production-style stop once the demo apps run. The run-time roles exist as titles. The people do not.

## Phase 0 application of these rules

**Verified Fact.** This unit did not start Phase 1. It did not edit the inherited tree. It did not run write-mode commands. BO-01 and BO-02 are accepted PROPOSED rows, so they do not pause this unit. The unsigned charter is a condition, not a stop.
