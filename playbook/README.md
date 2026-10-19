# Playbook — autonomous execution of the Sprint 4 capstone

This folder turns `Execution_Plan.md` into prompts a Cursor agent can run.

Three agents run the capstone. A coordinator runs the show, an executor builds the work, and a separate reviewer checks it. They run on different models, so no agent grades its own work, and the builder is not the checker.

- Coordinator — Grok 4.7 (`grok-4.7-high-fast`). It settles the decisions, spawns the executor to build each unit, spawns the reviewer to check it, applies fixes, and advances the run. It writes no artifact itself.
- Executor — Grok 4.6 (`cursor-grok-4.6-high-fast`). A fresh agent the coordinator launches with the Task tool to build one unit of work. It reads the inputs on disk, writes the artifacts, and returns the seven-item response.
- Reviewer — Composer 2.5 (`composer-2.5-fast`). A fresh agent the coordinator launches with the Task tool. It reads the files on disk, checks them against the Expected output, runs the Done test, and returns a verdict. It is never a resume of the executor.

A unit of work is one document phase, or one half of a build phase, or one half of a hardening sub-stage. The coordinator spawns one executor to build each unit and one reviewer to check it. Where a person must act, the coordinator stops and shows a pause card.

## Files

| File | Role |
|---|---|
| `00_coordinator.md` | The orchestrator prompt. You paste this once. It drives the whole run. |
| `executor.md` | The executor prompt. The coordinator hands this to a fresh Grok 4.6 agent to build each unit. |
| `reviewer.md` | The reviewer prompt. The coordinator hands this to a fresh Composer 2.5 agent at every gate. |
| `EXECUTION_ARCHITECTURE.md` | How the run works: the three agents, the per-phase loop, and the human pause points, with mermaid diagrams. |
| `phase_00_*.md` to `phase_16_*.md` | One prompt per phase (0 to 16). The coordinator opens these in order. |
| `STATUS.md` | The progress board. One row per sub-stage, 48 rows (the 46 spine units plus 11R and 20p). It shows Half A, Half B, the reviewer verdict, the gate, and the date. |

The glossary lives one level up. `PROJECT_ACRONYMS.md` at the workspace root explains every short code in plain speech.

## Trackers

Two files follow the run.

- `playbook/STATUS.md` tells you where the run is. Each sub-stage has a row. The coordinator sets the row to "in progress" when the phase starts, writes `HALF_A_ACCEPTED` when the reviewer accepts Half A, and stamps the gate and the date when the stage is accepted. "Blocked or paused" lists anything the run is waiting on.
- `PROJECT_ACRONYMS.md` tells you what a short code means. It is seeded with the codes already in the plan and the tracker. The coordinator adds a row in "New terms by phase" each time a phase introduces a new short code.

The coordinator updates both files at every gate.

Each phase prompt holds one or more spine sub-stages. A sub-stage is one spine unit (for example stage 24 security). It writes to its own `docs/NN-*/` folder and has its own sub-gate. The phase gate passes only when every sub-gate passes. The full map from spine unit to phase to folder is section 7 of `Execution_Plan.md`.

## The four sections in every phase prompt

Every `phase_NN_*.md` has the same shape, matching the Sprint 3 playbook.

- Inputs: the exact files to attach for that phase.
- Prompt: one fenced block you paste whole. It carries the Prompt Anatomy parts plus a Locked facts table so the agent reads the repo facts and SME rulings and does not re-derive them.
- Expected output: a table with one row per artifact and a "Must contain" column.
- Done test: one concrete check the reviewer runs.

## Half A and Half B

- Document phases (0, 1, 2, 3, 4, 6, 14, 15, 16) write documents and change no app behaviour. They have no Half A/B split. The reviewer checks the output in `STAGE` mode before the next phase.
- Build phases (5, 7, 8, 9, 10, 11, 12, 13, 17, 18) split into Half A (analysis and design) and Half B (code and tests). Half A ends with "STOP after Half A. Wait for HALF_A_ACCEPTED." The reviewer checks Half A in `HALF_A` mode. Half B starts only after the reviewer accepts. After Half B the reviewer checks again in `STAGE` mode. Phase 17 and Phase 18 sit outside the 46 spine units.

## How to run

All new deliverables are written at the capstone root: `docs/`, `apps/`, `context-lake/`, `policy/`, `sources/`, `operations/`, and the full-stack `compose` file. Only the Phase 7 transform edits files inside `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`.

1. Open a new Cursor agent chat on Grok 4.7.
2. Attach `Execution_Plan.md`, `Decision_Tracker.md`, `Project_Intent.md`, and this folder.
3. Paste the contents of `00_coordinator.md`.
4. The coordinator reads `playbook/STATUS.md` first. When every Phase 0 to 16 gate is `PASS` and the Phase 17 gate is not `PASS`, it opens `playbook/phase_17_demo_ready.md` only. When the Phase 17 gate is `PASS` and the Phase 18 gate is not `PASS`, it opens `playbook/phase_18_remaining_deviations.md` only. When any Phase 0 to 16 gate is not `PASS`, it stops and names that row. A fresh unfinished spine still starts at Phase 0. For each unit it settles the decisions, spawns a Grok 4.6 executor with `executor.md` to build the artifacts, then spawns a Composer 2.5 reviewer with `reviewer.md` to check the Expected output and run the Done test. It pauses when it needs Team-Force or the Business Owner, or when the reviewer returns a block. You answer, then tell it to continue.

## The loop the coordinator runs

For each phase, in order. A fresh spine runs from Phase 0 to Phase 16. A spine whose Phase 0 to 16 gates are already `PASS` runs Phase 17, then Phase 18:

1. Read the phase prompt file.
2. Open `Decision_Tracker.md` section 6 and find the phase row. List every decision the phase needs that is still `PENDING`.
3. Decide the gate:
   - A `PENDING` row owned by the SME: the coordinator decides it now as the SME, records the answer in `Decision_Tracker.md`, and continues.
   - A `PENDING` row owned by Team-Force that needs no human hand (an engineering or method choice): the coordinator decides it, records `authority: team-force`, and continues.
   - A `PENDING` row owned by Team-Force that needs a human hand (keys, a local service, a manual confirmation): pause with a pause card.
   - A Business Owner row that is `PROPOSED` and accepted in section 5.2: proceed on that answer. Do not pause. Do not write a policy value behind it into code.
   - A `PENDING` row owned by the Business Owner (the owner rejected the PROPOSED answer, or none was proposed): pause with a pause card, and show the SME recommendation from section 5.1 beside it.
4. Spawn the executor to build the unit. On a build phase, spawn it in `HALF_A` mode first; it writes the design and stops. On a document phase, spawn it in `DOCUMENT` mode. Every artifact lands in its own `docs/NN-*/` folder. For Phase 5, the executor runs the review loop in the Half B unit and sets the lake version.
5. Launch the reviewer. On a build phase after Half A, the reviewer runs in `HALF_A` mode; the Half B executor runs only on `HALF_A_ACCEPTED`. On a document phase, and after Half B, the reviewer runs in `STAGE` mode and runs the Done test.
6. Act on the verdict: `ACCEPTED` advances; `CONDITIONAL` applies the named fixes or prints a pause card for a Done test that needs a person; `BLOCKED` prints a pause card and does not start the next phase.
7. On acceptance, write a short phase record and move to the next phase.

## Pause card format

When the agent stops, it prints this card and waits.

```
PAUSE — <phase number and name>
Reason: <decision needed | human action needed | gate failed>
Who must act: <Team-Force | Business Owner>
What is needed: <the exact decision or task>
SME recommendation: <present for every Business Owner decision; mandatory>
Decision Tracker row: <ID, for example BO-04>
What I will do when you reply: <the next concrete step>
```

The agent does not guess past a pause. It waits for the reply, records the answer in `Decision_Tracker.md`, then continues.

## Rules that bind every phase

These come from `Execution_Plan.md` section 11, `playbook/executor.md`, and `playbook/reviewer.md`.

- Each phase prompt has the four sections (Inputs, Prompt, Expected output, Done test), the eight Prompt Anatomy parts inside the Prompt, and the Prompt Template header on every artifact.
- The coordinator orchestrates; a fresh Grok 4.6 executor builds each unit; a fresh Composer 2.5 reviewer is the gate, accepting Half A then the finished stage. No agent grades its own work, and the builder is not the checker.
- Every claim carries one label: Verified Fact, Inference, Assumption, or Unknown.
- Every material finding states six things: the finding, the evidence, the impact, the risk, the confidence, and the open questions.
- No invented thresholds. A proposed number is marked PROPOSED and names the owner.
- A deferred business-policy decision never becomes a silent value in code. The affected cases route to HOLD_FOR_REVIEW.
- Every Business Owner decision is shown with its SME recommendation.
- Each sub-stage saves to its own spine `docs/NN-*/` folder from section 7 of `Execution_Plan.md`.
- Each hardening sub-stage in Phases 12 and 13 does Half A design, then Half B with before-and-after evidence.
- The Context Lake carries a version and changes through the Phase 5 review loop.
- Every agent step and every human approval writes an audit-chain row keyed by a correlation id.
- Phases 0 to 6 change no application behaviour.
- Each phase ends with the seven-item final response and a gate: PASS, CONDITIONAL PASS, or BLOCKED. A BLOCKED phase stops the next phase.
- Append every chat turn to `transcript/chat_transcript.md`.
