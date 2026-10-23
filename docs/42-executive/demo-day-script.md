# Demo-day script

| Field | Value |
|---|---|
| Stage | Phase 15 / 42 Executive defence. Demo-day script |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Paper rehearsal 39 minutes. Live `docker compose up` NEEDS_HUMAN. BO-12 placeholder |
| Evidence sources | `Execution_Plan.md` section 10; `docs/09-initial-prd/initial-prd.md`; `docs/model-comparison/scorecard.md`; `docs/24-security-privacy/security-test-results.md`; `docs/_playbook-log.md` Phase 10; FD-21; BO-12 |
| Assumptions | `MODEL_MODE=replay`. The presenter tells the audience replay is on. Official Birlasoft assets have not arrived |
| Unresolved issues | Live six-port stack not started by this unit. Audience watch not claimed |
| Residual risks | Claiming a new pid kill. Showing an unlabelled number. Setting `MODEL_MODE=azure` |

This script is the spoken 39-minute walk. It follows the content blocks in `Execution_Plan.md` section 10. The paper clock ends at minute 39 so the sum stays under 40 minutes.

Engineering decision ED-P15-07, authority: team-force. Section 10 keeps the seven content blocks. The paper rehearsal shortens the first block from 8 minutes to 7 minutes. Injection BLOCK and the pid 29320 restart stay in the security block. Lessons stay last.

---

## Finding

**Finding.** Seven blocks cover problem, architecture, Application A, Application B, scorecard, injection-plus-restart, and lessons. The paper walk sums to 39 minutes. The script includes one injection that returned HTTP 409 BLOCK and one approval that survived the kill of pid 29320. Replay files exist on disk (77 besides README). A live Compose start is NEEDS_HUMAN. No audience watched this walk.
**Evidence.** Section 10 table. Phase 12 HB-24-01. Phase 10 `corr-p10-kill-20261018-001`. This-unit file count.
**Impact.** The reviewer can time the script from the minute column. A later person can run Compose and paste health.
**Risk.** Re-running a kill in the room and calling it the Phase 10 result.
**Confidence.** High on the paper sum and the cited results. Unknown on live container health today.
**Open questions.** Who runs D3 in `operator-exercises.md`. BO-12 assets.

---

## Locked demo facts

| Constant | Value | Label |
|---|---|---|
| Demo length | Paper walk 39 minutes. Under 40 | Verified Fact of this script |
| Offline mode | `MODEL_MODE=replay` | Verified Fact. FD-21 |
| Injection | Phase 12 HTTP 409 BLOCK on `REPLAY-000000000` quotes-plus-approve with no corpus id | REAL prior. Not a new post |
| Restart | Coordinator killed pid 29320. `corr-p10b-kill-20261018-001` stayed on `PS000000016`. `engineering_hold` stayed 0 | REAL prior. Not a new kill |
| Brand | Neutral placeholder. Official assets have not arrived | Verified Fact. BO-12 PROPOSED |
| ROI | EDUCATIONAL. Dollars Unknown | Verified Fact |
| Company titles | Unknown | Unknown |
| INC-2025-014 owner | Unknown | Unknown |
| Numeric floors | Unknown | Unknown |

---

## Minute map

Section 10 windows are listed so a reviewer can see the source. Paper start and end are the timed walk.

| Paper clock | Section 10 window | Minutes | Content |
|---|---|---|---|
| 0:00 to 7:00 | 0 to 8 min | 7 | Business problem and baseline |
| 7:00 to 12:00 | 8 to 13 min | 5 | Architecture and GenAI-versus-deterministic boundary |
| 12:00 to 24:00 | 13 to 25 min | 12 | Application A. Scenarios 7 to 11. Agent trace. Approval gate |
| 24:00 to 31:00 | 25 to 32 min | 7 | Application B. Same scenarios. Rule trace |
| 31:00 to 35:00 | 32 to 36 min | 4 | Before-and-after scorecard |
| 35:00 to 38:00 | 36 to 39 min | 3 | Injection BLOCK and restart mid-approval |
| 38:00 to 39:00 | 39 to 40 min | 1 | Five lessons |

Minute total: 7 + 5 + 12 + 7 + 4 + 3 + 1 = **39**.

---

## Before the live show (not part of the 39 minutes)

| Step | Action | Status |
|---|---|---|
| P0 | Set `MODEL_MODE=replay`. Leave Azure variables unset | Written default. Verified Fact |
| P1 | `docker compose up --build` from the capstone root | NEEDS_HUMAN |
| P2 | Health GET on 8080, 8090, 8091, 8092, 8100, 8110 | NEEDS_HUMAN |
| P3 | Say to the room: replay is on. Saved files play back. No network call | Spoken line |

If P1 cannot run, use the paper walk and the already-measured screenshots in the evidence index. Do not invent a health pass.

---

## Block 1. 0:00 to 7:00. Problem and baseline

Say:

Fabpulse cannot consistently explain or close a fab-lot or equipment exception when the feeds, the local rules, the archived documents, and the month-end reports disagree.

Show the eight defects. Read the packaged counts. Honesty REAL: 91 recipe mismatches, 67 REPLAY feeds, 11,985 clock mismatches, 2,090 REVIEW objects, 89 open cases, 34 active policies, 86 untrusted notes, 695 unassigned tasks.

Show the frozen six fields. Honesty REAL: records 125, open_cases 89, urgent_cases 2, sites 6. Honesty SIMULATED: mean_amount 4982.61, hours_per_case 0.603.

Say: exception cycle time is Unknown. Aged backlog is Unknown. Company titles are Unknown. INC-2025-014 owner is Unknown.

Do not show a dollar.

---

## Block 2. 7:00 to 12:00. Architecture and the model boundary

Say:

Two applications run the same workflow. Application A is the rebuilt program on port 8100. Application B is built from the Context Lake on port 8110. They do not call each other.

The lake version is 1.0.0. It holds 148 items, 180 edges, and 267 term rows. Honesty: REAL. Phase 5.

Ranking, rules, reconciliation, and de-duplication stay in code. The model drafts a cited sentence, a query answer, or a plan. The model has no write tool.

Hold prediction was measured and rejected. 125 lots. 8 held. 117 not held. Majority 117/125. Leave-one-out 117/125. Honesty: REAL. Phase 2. No production hold scorer exists.

A person in RT-01 to RT-06 records every write. The proposer is never the approver. Named people stay Unknown.

---

## Block 3. 12:00 to 24:00. Application A. Scenarios 7 to 11

Mode: `MODEL_MODE=replay`. Tell the room replay is on.

If the stack is down, read the bound ids and the prior results. Live clicks are NEEDS_HUMAN.

| Minute | Scenario | Case id | What to show | Honesty |
|---|---|---|---|---|
| 12:00 to 14:00 | S7 Replay inflation | `REPLAY-000000000` | Duplicate candidate. 67 REPLAY rows. RT-05 must confirm | REAL |
| 14:00 to 17:00 | S8 Recipe mismatch | `PS000000016` | Recipe R02 and R01. Agent draft. Approval gate. Model does not write `engineering_hold` | REAL |
| 17:00 to 19:00 | S9 Two clocks | `E-00000000` | Event time 2020-12-30 and arrival 2021-01-01 stay two fields | REAL |
| 19:00 to 21:30 | S10 Overlapping policies | `FAB-00000002` | Five US policy ids. Wait for RT-04 | REAL |
| 21:30 to 24:00 | S11 Missing owner | `INC-2025-014` | Owner field empty. Task `T-00000000` unassigned. RT-06 assigns a supplied name. This script leaves the owner Unknown | REAL empty field |

Open `GET /api/audit/{correlation_id}` after the S8 run if the stack is up. Rows ordered by `seq`. If the stack is down, say the audit table has 27 columns and the join key is the correlation id. **Verified Fact.** FD-23.

---

## Block 4. 24:00 to 31:00. Application B and a rule trace

Same five case ids on port 8110. Application B source has no inherited-repo path and no call to 8100. **Verified Fact.** Phase 11.

Show one rule trace. GQ-01 cites `rule.recipe_release.limit.v2023.emea` and the sentence holds 18600. Honesty: REAL. Phase 12 freeze.

Say: PH-S12-01 differs because Application A has no lineage route. Application B returns the 2023 EMEA item. The difference cites lake items. Do not say a match percent.

---

## Block 5. 31:00 to 35:00. Scorecard

Open `docs/model-comparison/scorecard.md` or the placeholder slide that copies its table.

Say the six frozen fields again with their labels.

Say: harness 14 rows, matched 12, differing 2. Honesty: REAL. No match percent.

Say: freeze `rows=42 pass=42 fail=0`. Honesty: REAL. Floors Unknown.

Say: shown Application A replay `prompt_tokens` 0 and `completion_tokens` 0. Honesty: REAL for that path. Dollars Unknown.

Say: ROI is EDUCATIONAL. Monetary benefit claimed: none. BO-11 stays UNSIGNED.

---

## Block 6. 35:00 to 38:00. Injection BLOCK and restart mid-approval

This block must appear. FD-21.

### Injection that returns BLOCK (about 35:00 to 36:30)

Cite Phase 12. Do not claim a new live post unless a person runs it and pastes the 409.

Spoken line:

Partner feed `REPLAY-000000000` already carries untrusted quotes. The note says disregard validation and auto approve. We posted `proposed_action=approve` with no corpus id. Before the control the reply was HTTP 200 and the graph waited. After the control the reply was HTTP 409 BLOCK. `opa_verdict` was BLOCK. `waiting` was false. Approvals stayed empty. Case status stayed REPLAY. Application B after its own control did the same.

Honesty: REAL. Source: `docs/24-security-privacy/security-test-results.md` and `docs/26-tevv/tevv-results.md`.

If a person later re-posts on a live stack, the expected reply is HTTP 409. That re-post is NEEDS_HUMAN. Do not retry BLOCK as EXECUTE.

### Approval that survives a process restart (about 36:30 to 38:00)

Cite Phase 10. Do not kill a process in this unit.

Spoken line:

The coordinator started Application A on port 8765. It posted case `PS000000016`. It killed pid 29320. It started a new process. The same correlation id `corr-p10b-kill-20261018-001` was still on that case. `engineering_hold` stayed 0.

Honesty: REAL. Source: `docs/_playbook-log.md` Phase 10. Tracker note restart pid 30216.

This script does not claim a new live kill.

---

## Block 7. 38:00 to 39:00. Five lessons

Read the titles only. Detail sits in `lessons-learned.md`.

1. Phase 2. Hold prediction scored 117/125. Same as the majority guess. Rejected.
2. Phase 11 and 14. Harness 12 matched, 2 differed. Each difference cites the lake.
3. Phase 10. `corr-p10b-kill-20261018-001` stayed on `PS000000016` after pid 29320 died.
4. Phase 12. Quotes plus approve returned HTTP 409 BLOCK. No record changed.
5. Phase 14. ROI stays EDUCATIONAL. Headlines stay Unknown.

Stop at 39:00.

---

## Honesty labels the presenter must say

| Label | Meaning on this demo |
|---|---|
| REAL | Counted from a tool, a test, or a dated paste |
| PRECOMPUTED | A saved replay sentence |
| SIMULATED | A modelled figure on synthetic data |
| EDUCATIONAL | ROI cells. No cash claim |

Every demo number carries one of those four labels. **Verified Fact.** FD-20.

---

## Paper rehearsal record

| Field | Value |
|---|---|
| Kind | Timed walk of this script |
| Date | 2026-10-18 |
| Audience present | No |
| Minute total | 39 |
| Under 40 | Yes |
| `docker compose up` | NEEDS_HUMAN. Not run |
| New process kill | Not run |
| New injection POST | Not run |
| Replay files on disk | 77 besides README. REAL |
| Offline paper result | Script complete on paper. Live stack unstarted |

See `docs/demo/paper-rehearsal.md`.

## Six limits to say out loud

1. The sign-in service on this laptop is a local stand-in. The users are seeded. They share one demo one-time-code secret.
2. Scrap of 1,500 USD per defect is an estimate. It is labelled that way on the page.
3. Hold age uses the latest process step in the legacy file. That file ends in February 2023.
4. Model latency and model cost are not measured. Those KPI cells stay Unknown.
5. Application A grounded accuracy is not measured. Application B shows the recorded 42 of 42.
6. The OPA program is not installed here. The built-in checker applies the same rules.
