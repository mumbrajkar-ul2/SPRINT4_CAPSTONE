# Paper rehearsal

| Field | Value |
|---|---|
| Stage | Phase 15 / 42 Executive defence. Paper rehearsal |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE as a timed walk of the script. No audience. Live Compose NEEDS_HUMAN |
| Evidence sources | `docs/42-executive/demo-day-script.md`; `Execution_Plan.md` section 10; `operations/model-replay/`; FD-21 |
| Assumptions | A paper rehearsal is a timed read of the spoken blocks. It is not a room with judges |
| Unresolved issues | Live six-port health today Unknown |
| Residual risks | Calling this walk a watched rehearsal. Inventing a Compose pass |

This page records the timed walk of `demo-day-script.md` on 2026-10-18. No audience watched it. `docker compose up` was not run.

---

## Finding

**Finding.** The seven spoken blocks take 39 minutes. The sum is under 40. Injection BLOCK and the pid 29320 restart both appear in the script. Replay files exist on disk. A live offline run of the six listeners is NEEDS_HUMAN and is not marked passed.
**Evidence.** Minute table below. 77 replay files besides README. Script blocks 6 and 7.
**Impact.** FD-21 paper length is met. The Done-test live Compose step waits for a person.
**Risk.** A later note that says the room saw this walk.
**Confidence.** High on the paper sum. Unknown on live health.
**Open questions.** Who runs P1 in the script's pre-show list.

---

## Timed walk

Walker: executor agent, correlation id `corr-p15-doc-20261018-001`.

Date: 2026-10-18.

Audience: none.

| Clock | Block | Minutes | Walked on paper | Live stack used |
|---|---|---|---|---|
| 0:00 to 7:00 | Problem and baseline | 7 | Yes | No |
| 7:00 to 12:00 | Architecture and model boundary | 5 | Yes | No |
| 12:00 to 24:00 | Application A scenarios 7 to 11 | 12 | Yes | No. Clicks NEEDS_HUMAN |
| 24:00 to 31:00 | Application B and rule trace | 7 | Yes | No. Clicks NEEDS_HUMAN |
| 31:00 to 35:00 | Scorecard | 4 | Yes | No. File read |
| 35:00 to 38:00 | Injection BLOCK and pid 29320 restart | 3 | Yes. Cited prior REAL | No new POST. No new kill |
| 38:00 to 39:00 | Five lessons | 1 | Yes | No |

Minute total: **39**.

Section 10 content order: kept. First block shortened by one minute so the sum stays under 40.

---

## Must-appear checks

| Required item | In the script? | How it was walked |
|---|---|---|
| Injection that yields BLOCK | Yes. Block 6 | Read Phase 12 HTTP 409 on `REPLAY-000000000` |
| Approval that survives a restart | Yes. Block 6 | Read Phase 10 kill of pid 29320 and `corr-p10b-kill-20261018-001` on `PS000000016` |
| `MODEL_MODE=replay` | Yes. Locked facts and Block 3 | Stated. 77 replay files counted on disk |
| Four or five lessons | Yes. Five lessons | Read titles in Block 7 |
| Every number labelled | Yes | REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL |

---

## Offline replay check this unit did run

| Check | Result | Label |
|---|---|---|
| Compose default text is `MODEL_MODE: ${MODEL_MODE:-replay}` | Present in `compose.yaml` | Verified Fact |
| Replay folder file count besides README | 77 | REAL |
| Replay README says a miss returns `replay_miss` and opens no public-network socket | Present | Verified Fact |
| Azure variables set by this unit | No | Verified Fact |

---

## Offline live run this unit did not run

| Check | Result |
|---|---|
| `docker compose up --build` | NEEDS_HUMAN. Not run. No pass invented |
| Health GET on 8100 and 8110 | NEEDS_HUMAN. Not run |
| Live `POST /api/agent/run` for BLOCK | NEEDS_HUMAN. Prior REAL cited instead |
| Live process kill | Not run. Prior REAL cited instead |

---

## Sign-off block

| Field | Value |
|---|---|
| Rehearsal witness | None |
| Signature | Not signed |
| Status | UNSIGNED |
| Minute total | 39 |

This file does not invent a witness. The paper walk is recorded. A room rehearsal is not claimed.
