# Deviations from the original execution plan

| Field | Value |
|---|---|
| Date | 2026-10-19 |
| Status | CLOSED on 2026-10-19. Phase 17 closed DEV-001 through DEV-009. Phase 18 closed DEV-010 through DEV-020. Phase 0 to 16 PASS cells were not changed. |
| Evidence | `Execution_Plan.md` section 4, section 8, and section 10; `Project_Intent.md` sections 9, 10, 12, 13, 15.1, and 15.2; `docs/10-architecture/adrs/adr-two-applications.md`; `playbook/STATUS.md`; `playbook/00_coordinator.md`; `playbook/phase_05_context_lake.md`; `playbook/phase_08_foundations.md`; `playbook/phase_09_app_a.md`; `playbook/phase_10_agents_hitl.md`; `playbook/phase_11_app_b.md`; `playbook/phase_12_security_tevv.md`; `playbook/phase_13_hardening.md`; `playbook/phase_15_defence_demo.md`; `playbook/phase_16_final_asbuilt_prd.md`; `playbook/executor.md`; `playbook/reviewer.md`; `Dockerfile.platform`; `apps/app_a/ui/`; `apps/app_b/ui/`; the Phase 17 plan |
| Scope | The screen library, the live demo motions in section 15.1 and section 15.2, and the prompt gaps that Phase 17 does not close. The server tools that section 4 names stayed in the build. |

This file records the misses that the first playbook run left open. Every row has a tracking number. A later check marks a row CLOSED only when the correction check passes. Phases 0 to 16 stay PASS in `playbook/STATUS.md`. Closing a row here does not reopen those gates.

The locked screen is React. The pages that run are plain HTML, CSS, and browser JavaScript. No later decision records that swap. This file keeps the locked name, React, until a new ADR replaces it.

The close path for DEV-001 through DEV-009 is the Phase 17 plan. Step 1 writes the standing prompt text and does not spawn an executor. A new coordinator chat then starts at `playbook/phase_17_demo_ready.md`. It does not open Phase 0. It does not re-run Phase 8, 9, 11, or 16. Phase 17 Half B is the stage that installs React and builds the scenario clicks. DEV-010 through DEV-020 stay open after that phase. They need their own prompt text and their own Done test before a later phase can close them.

A playbook correction has to change the prompt, the inputs, the expected output, and the validation test together. A single added sentence that says "use React" leaves the same gap.

---

## What stayed on the lock

`Execution_Plan.md` section 4 locks these server tools. The running code uses them.

| Lock | Where it runs |
|---|---|
| FastAPI and Uvicorn | Application A on port 8100. Application B on port 8110. Lake REST on 8091. Lake MCP on 8092. |
| LangGraph `interrupt()` and a SQLite checkpoint | `apps/app_a/agent/graph.py`. Checkpoint file `apps/app_a/runtime/checkpoints.sqlite3`. |
| OPA verdicts EXECUTE, HOLD_FOR_REVIEW, BLOCK | `policy/opa/`. Python applies the same named rules when the OPA binary is absent. |
| YAML in Git, built into one SQLite file | `context-lake/build.py` writes `context-lake.sqlite3`. |
| Docker Compose | `compose.yaml` names seven containers. |
| Replay as the laptop model path | `MODEL_MODE=replay` in `compose.yaml`. |

The screen row of that same lock did not land in the files.

| Lock | Files on disk |
|---|---|
| React screens, served by the same FastAPI process | `apps/app_a/ui/index.html`, `apps/app_a/ui/assets/app.js`, `apps/app_a/ui/assets/styles.css`. Application B has the same three files under `apps/app_b/ui/`. |

Worked example. Open `apps/app_a/ui/assets/app.js`. The queue button calls `document.getElementById` and `fetch`. The folder has no `package.json`, no JSX file, and no React runtime. A search of `apps/` for `react` and `ReactDOM` returns no matches.

`Dockerfile.platform` starts from `python:3.12-slim` and installs `requirements-platform.txt`. That image has no Node install and no front-end build step.

`adr-two-applications.md` rejects Streamlit as the demo UI. The pages that shipped are static HTML served by FastAPI. The build used neither React nor Streamlit.

---

## How the lock dropped out of the build order

Each step below is a place the React sentence stopped being an order. A correction that fixes only the last step still lets the next run skip the screen library.

1. **The architecture sentence stays in section 4 and in the ADR.** `Execution_Plan.md` section 4 opens with "Two FastAPI and React applications." `adr-two-applications.md` repeats that sentence and rejects Streamlit because Guideline 5 asks for a professional application and because section 4 already locks FastAPI and React. Phase 4 is told not to change those fixed choices.

2. **The phase that builds the screen uses different words.** Phase 9 in `Execution_Plan.md` and in `playbook/phase_09_app_a.md` asks for a role-based UI: queue, case, query, recovery, and approval. Guideline 5 is mapped to Phase 9 as "Enterprise-grade UI/UX." The phase prompt turns that into those screens. The locked-facts table, the artifact list, and the Done test do not name React, `npm`, or Vite.

3. **The spawn message points at the scenario list.** The Phase 9 Half A order told the executor to read `playbook/executor.md`, `playbook/phase_09_app_a.md`, and the plain-speech rule. It told the executor to read `Execution_Plan.md` section 8 for the scenario mapping. It did not name section 4 or `adr-two-applications.md`. The locked facts in that message cover grounding, rule source, write tools, scenarios, replay, and the three identity headers. They do not name the screen library.

4. **The executor is told to stop at the unit boundary.** `playbook/executor.md` says build the unit and stop. A React app needs a Node project and a change to `Dockerfile.platform`. Phase 8 had already closed that image as Python only, and Phase 8 says "Do not build app features here." Those steps sit outside the Phase 9 artifact list.

5. **Half A still wrote the word React, and left the layout open.** `docs/20-application/application-component-map.md` says Half B builds React views. The same file lists "React folder layout details inside `apps/app_a/ui/`" as an open question. Half A wrote no UI code.

6. **Half B wrote HTML and recorded no new decision.** The Half B note says the work followed the earlier design decisions and added no new decision. The files are `index.html`, `styles.css`, and `app.js`. FastAPI serves them with `StaticFiles` and `FileResponse`.

7. **The reviewer grades the Done test, and the Done test does not open the page.** `playbook/reviewer.md` says check the Expected output and the Done test, and do not add scope. The Phase 9 reviewer re-ran `python apps/app_a/eval/run_freeze.py` and `python -m pytest tests/platform -q`. Those checks cover citations, abstain, and role headers. They do not look for React. A reviewer who fails the stage for a missing React app is adding a check the Done test does not name. The current reviewer rules call that extra scope.

8. **Later stages copied the page and kept the old name.** Phase 11 built Application B in the same HTML shape. Phase 16 docs still say "React screens," including `docs/final-prd/as-built-architecture.md` and `docs/final-prd/final-as-built-prd.md`. The Phase 16 Done test says the as-built architecture matches the running services. That test did not compare the word React to `index.html`.

---

## What a one-line prompt fix leaves in place

Adding "use React" to `playbook/phase_09_app_a.md` alone leaves these holes:

- The coordinator can still omit section 4 and the ADR from the read list.
- The executor can still treat a Node build and a Docker change as outside the unit.
- Phase 8 can still close a Python-only image with no statement about who may add the front-end build.
- The reviewer can still accept the stage, because `playbook/reviewer.md` forbids a check that the Done test does not name.
- Phase 11 can still copy the HTML page.
- Phase 16 can still write "React screens" over HTML files.

The blocks below close those holes. Each block has the prompt text to add, the inputs to hand over, the output to require, and the check that fails the stage.

---

## Coordinator spawn, for every build phase after Phase 4

This block changes the message the coordinator sends. It applies to Phase 8 through Phase 16. The measured miss is Phase 9. The same message shape can drop any other section 4 tool on a later run.

### Prompt text to add

Add this paragraph to the coordinator template, after the phase id and before the phase-specific locked facts:

```text
Read Execution_Plan.md section 4 and every ADR under docs/10-architecture/adrs/ before you write files. Those choices stay locked. Copy each tool named there into the locked-facts list you hand to the executor, including the screen library: React, served by the same FastAPI process. If a file you are about to write would use a different tool, stop. Record an engineering decision and name the ADR that would have to change. Do not ship the other tool and leave the ADR unchanged.
```

### Inputs the coordinator must hand over

- `Execution_Plan.md` section 4.
- `docs/10-architecture/adrs/adr-two-applications.md` on any phase that builds or describes a screen.
- The phase prompt.
- A locked-facts block that repeats the screen sentence: "Screens are React. FastAPI on the same port serves the built files."

The Phase 9 spawn that ran pointed at section 8 for scenarios. Keep that pointer. Add section 4 and the ADR beside it. Section 8 does not name the screen library.

### Output the stage must produce

The spawn message itself is the output of this correction. A later reader can see the screen library in the locked-facts block of the executor prompt, in the same list as grounding and ports.

### Validation

Read the spawn message before the executor starts. Fail the handoff when the read list lacks `Execution_Plan.md` section 4 or `adr-two-applications.md` on a screen phase. Fail the handoff when the locked-facts block has no screen-library line.

Worked example. The Phase 9 Half A message that ran listed FD-14, FD-04, the rule source, write tools, scenarios, replay, and the three headers. A corrected message still lists those rows, and it adds one row: screens are React.

---

## `playbook/executor.md`

### Prompt text to add

Add this rule under "Rules that bind you":

```text
A locked tool in Execution_Plan.md section 4 is part of this unit when this unit builds that layer. The screen layer is React. If the files for that layer would use HTML, Streamlit, or another library, stop before you write them. Return BLOCKED, name the lock, and name the ADR a person would have to change. Do not write the other library and report that you added no decision.
```

### Inputs the coordinator must hand over

The same section 4 extract and the ADR path from the coordinator block. The executor already receives the phase prompt. That prompt must contain the screen row, or this rule has nothing to enforce.

### Output the stage must produce

Either the React files named in the phase output, or a BLOCKED response that names `adr-two-applications.md`. A folder of `index.html`, `styles.css`, and `app.js` with a note that says "no new decision" fails this rule.

### Validation

On a screen phase, open the executor's final response. Fail the unit when the UI path contains only static HTML and the response says no engineering decision was added.

---

## `playbook/phase_08_foundations.md`

Phase 8 builds the image and then closes. Phase 9 is told not to wander into platform work. The React build has no owner.

`Dockerfile.platform` is `FROM python:3.12-slim`. It runs `pip install -r requirements-platform.txt`. It copies `apps/` and starts Uvicorn. It does not install Node.

### Prompt text to add

Add one locked fact. Pick one of the two sentences and delete the other when you edit the playbook. This deviations file does not pick for you. Both sentences keep React as the screen.

```text
Front-end build, choice A: This phase installs Node in Dockerfile.platform and builds the React screens for Application A and Application B. The image serves the built files from FastAPI.

Front-end build, choice B: This phase leaves Dockerfile.platform as a Python image. Phase 9 is allowed to add the Node build to that image when it adds the React screens. Phase 9 records that image change as an engineering decision. Phase 8 does not treat a later Node install as out of scope.
```

Add the chosen sentence to the Phase 8 locked-facts table and to the Half B constraints.

### Inputs the coordinator must hand over

- `Execution_Plan.md` section 4, so the image work can see the React sentence.
- `Dockerfile.platform` and `compose.yaml`.
- The chosen front-end sentence from the prompt block above.

### Output the stage must produce

Choice A produces a `Dockerfile.platform` that installs Node and runs the React build, plus a compose service that serves the built files on ports 8100 and 8110.

Choice B produces a written sentence in `docs/18-delivery/` that names Phase 9 as the phase that may edit `Dockerfile.platform` for the React build. The current image can stay Python-only in Phase 8.

### Validation

Choice A. Open `Dockerfile.platform`. Fail the stage when the file has no Node install and no React build command.

Choice B. Open the Phase 8 delivery doc and `playbook/phase_09_app_a.md`. Fail the pair when Phase 8 says the image is finished and Phase 9 says it must not change the image, while the screen lock is still React.

The run that already finished took neither choice. The image stayed Python-only, and Phase 9 wrote HTML inside `apps/app_a/ui/`.

---

## `playbook/phase_09_app_a.md`

This is the phase that wrote the screens.

### Prompt text to add

Add this row to the locked-facts table:

```text
| Screen library | React. FastAPI on port 8100 serves the built files from the same process. Plain HTML, CSS, and browser JavaScript do not meet this row. Streamlit does not meet this row. |
```

Add this sentence to Required work, item 3:

```text
Build the React screens under apps/app_a/ui/. The source uses React. The FastAPI process serves the built files. A page of index.html plus assets/app.js fails this item.
```

### Inputs the coordinator must hand over

- `Execution_Plan.md` section 4.
- `docs/10-architecture/adrs/adr-two-applications.md`.
- `docs/20-application/application-component-map.md` after Half A. Half B must close the open question "React folder layout," and the answer must be a React tree.
- `Dockerfile.platform`, plus the Phase 8 choice about who may add Node.

Keep the current inputs: the lake, the specs, the transformed services, the Phase 8 platform, and the decision tracker.

### Output the stage must produce

Replace the Expected output cell for `apps/app_a/` with:

```text
apps/app_a/ holds the intelligence core and a React app under apps/app_a/ui/. The React source is in the repo. FastAPI serves the built files on port 8100. The role picker sets X-Api-Key, X-Actor-Id, and X-Actor-Role. Queue, case, query, recovery, and approval call /api.
```

Half A must name the React folder layout. An open question that says "React folder layout details stay later" fails Half A, because Half B then has no layout to build.

### Validation

Add this to the Done test, beside the current scenario and abstain checks:

```text
Screen library check for Application A:
1. apps/app_a/ui/package.json lists the react dependency.
2. At least one source file under apps/app_a/ui/ is JSX or TSX.
3. The served page is the output of that React build.
Fail the stage when apps/app_a/ui/ contains only index.html, assets/app.js, and assets/styles.css.
Fail the stage when a search of apps/app_a/ui/ finds no react dependency.
```

The current files fail that check. `apps/app_a/ui/assets/app.js` calls `document.getElementById` and `fetch`.

Keep the existing Done test. Scenarios 7 to 11 still run. An ungrounded query still abstains. The screen check is an added row.

---

## `playbook/reviewer.md`

The rule that says "do not add scope" stays. It is the reason a careful reviewer accepted HTML. The fix is to put the screen library in the Done test, so a miss is a failed test.

### Prompt text to add

Add this sentence under "On the Done test":

```text
Run every row of the phase Done test, including a screen-library row when the phase has one. A missing React app on a phase whose Done test requires React is a FAIL. Do not treat that miss as extra scope. Do not invent a screen check for a phase whose Done test has no screen row.
```

Leave this sentence in place: "You check the work against its Expected output and Done test, not against a better design you would have written."

### Inputs the coordinator must hand over

The phase Done test, including the screen-library row when the phase is Phase 9, Phase 11, or Phase 16. The reviewer already receives the Expected output table and the locked facts. Those three inputs must agree on the word React.

### Output the stage must produce

The REVIEW block names the screen check as its own row, with PASS or FAIL and the file that decided it.

Worked example. A Phase 9 REVIEW block includes a row: "Screen library FAIL. `apps/app_a/ui/package.json` is absent. `apps/app_a/ui/assets/app.js` uses `document.getElementById`." The verdict is STAGE_BLOCKED. The freeze set can still be 42 of 42. That count does not pass the screen row.

### Validation

Read the REVIEW block. Fail the review when a screen phase's Done test has a React row and the REVIEW block has no screen line. Fail the review when the screen line says PASS and the UI folder has no React source.

---

## `playbook/phase_11_app_b.md`

Application B copied the HTML page. The phase prompt asks for "the App B UI" and a lineage view. It does not name React.

### Prompt text to add

Add this row to the locked-facts table:

```text
| Screen library | The same React library as Application A. FastAPI on port 8110 serves the built files. The lineage view is a React view. Rules still come only from the lake. |
```

### Inputs the coordinator must hand over

- `adr-two-applications.md`.
- The Application A React tree under `apps/app_a/ui/`, as the screen pattern to follow.
- The lake, the specs, and the parity harness inputs the phase already names.

Application B still must not import Application A rule functions and must not read the legacy repo to decide pass or fail. The screen library and the rule source are separate. Sharing the React pattern does not share the rule code.

### Output the stage must produce

`apps/app_b/ui/` is a React app. The lineage view shows the correlation id. FastAPI on port 8110 serves the built files. The parity harness still traces each difference to a lake item.

### Validation

Use the Phase 9 screen check against `apps/app_b/ui/`. Fail the stage when that folder is only `index.html`, `assets/app.js`, and `assets/styles.css`.

Keep the current Done test. Application B still runs with Application A stopped. The parity harness still traces each difference to a lake item. A search of Application B build inputs still finds no legacy-repo path.

---

## Phase 16 as-built docs

`playbook/phase_16_final_asbuilt_prd.md` says the as-built architecture must match the services that run. The Done test says the same. The files that passed still call the pages React screens.

These sentences are the mismatch:

- `docs/final-prd/as-built-architecture.md` describes ports 8100 and 8110 as "API and React screens."
- `docs/final-prd/final-as-built-prd.md` says FastAPI serves the React screens.
- `docs/20-application/application-component-map.md` says Half B builds React views.
- `docs/17-implementation-prd/implementation-prd.md` says FastAPI serves the React screens.
- `docs/model-comparison/app-b-from-lake.md` and `docs/model-comparison/app-b-lineage.md` say React screens.

The pages on disk are `apps/app_a/ui/index.html` and `apps/app_b/ui/index.html`.

### Prompt text to add

Add this row to the Phase 16 locked-facts table:

```text
| Screen sentence | The as-built screen sentence matches the files under apps/app_a/ui/ and apps/app_b/ui/. Write "React" only when those folders contain a React app. When they contain index.html and assets/app.js, write that fact and mark the section 4 React row as a deviation. |
```

### Inputs the coordinator must hand over

- `Execution_Plan.md` section 4.
- `adr-two-applications.md`.
- `apps/app_a/ui/` and `apps/app_b/ui/`.
- The as-built files named above.

The phase already reads the ADRs. The added input is the UI folders, so the architecture sentence is checked against files.

### Output the stage must produce

`docs/final-prd/as-built-architecture.md` names the screen files that exist. When those files are HTML, the comparison to Phase 4 says the React row was not built, and it points at this deviations file. A table cell that says "React screens" while the folder is HTML fails the phase.

### Validation

Add this to the Phase 16 Done test:

```text
Screen sentence check:
1. Read apps/app_a/ui/index.html and apps/app_b/ui/index.html.
2. Search docs/final-prd/as-built-architecture.md and docs/final-prd/final-as-built-prd.md for the word React.
3. Fail the stage when those docs say the running screens are React and the UI folders have no react dependency and no JSX or TSX source.
```

The current docs fail that check.

---

## Tracking index

Each row stays OPEN until the correction check passes. DEV-001 through DEV-009 are owned by Phase 17. DEV-010 through DEV-020 are owned by Phase 18. The first-run PASS cells in `playbook/STATUS.md` stay as they are.

| Tracking | Miss | Close path | Correction check | Status |
|---|---|---|---|---|
| DEV-001 | Section 4 locks React. The pages are HTML, CSS, and `app.js`. | Step 1 writes the seven prompt checks below. Phase 17 Half B installs Node and builds the React screens. | `apps/app_a/ui/package.json` and `apps/app_b/ui/package.json` list `react`. Each folder has a JSX or TSX file. `Dockerfile.platform` installs Node and runs the build. FastAPI on 8100 and 8110 serves that build. | CLOSED |
| DEV-002 | Section 15.1, minutes 13 to 25, asks for live intake and replay, conflict detection, exception investigation, human approval, and audit evidence. | Phase 17 React pages show five bands and call `POST /api/agent/run` and `GET /api/audit/{correlation_id}`. | A person can complete those five motions on the page without reading a JSON dump. | CLOSED |
| DEV-003 | B1. A replayed MESDispatch delivery inflates the queue and the screen explains the duplicate evidence. | Phase 17 session action **Receive the replayed MESDispatch** on ref `C00001646`. | The work-queue count rises by 1. The table shows ingest `2022-04-25T19:09` and `2022-04-25T20:09`. RT-05 **Confirm drop** returns the count. The packaged store stays at 67 `REPLAY` rows. | CLOSED |
| DEV-004 | B2. Recipe revisions differ, with the time each fact was true, and the case routes for approval. | Phase 17 shows the step, the tool, and `ECN0000001` on `PS000000016`. | The page shows R02 at `2023-01-05T16:00`, tool R01 with no effective date, and the approved change effective `2023-01-01T07:00`. **Investigate** shows `HOLD_FOR_REVIEW`. The hold button stays disabled until RT-03 is a different person from `proposed_by`. | CLOSED |
| DEV-005 | B3. A late or backfilled event changes the case timeline. Event time stays separate from arrival time. | Phase 17 **Apply the backfilled event** for `E-00000000`. | The row appears at event time `2020-12-30`. The arrival mark stays `2021-01-01`. The page says metrology samples have no clock. | CLOSED |
| DEV-006 | B4. Overlapping policies are identified, the app abstains, and a named person approves. | Phase 17 shows `valid_from` and `valid_to` and the date `2024-06-01`. | Four policies are in force on that date. **Check the overlap** abstains. RT-04 records keep-wait or a named policy id. | CLOSED |
| DEV-007 | B5. An outage or schema mismatch shows retry, a dead-letter row, recovery, and a status a user can read. | Phase 17 recovery on both apps, with `SOURCE_GATEWAY_URL` set to port 8090. | Timeout shows attempt count 2. Schema shows attempt count 1, and the sentence matches that count. A parked intake stays listed after replay as `REPLAYED`. | CLOSED |
| DEV-008 | B6. The lake traces one rule from historical decision and code to specification, test, and transformed implementation. | Phase 17 lineage view on Application B, five ordered steps. The `implements` link is added from `rule.recipe_release.limit.v2023.emea` to the transformed evaluator. | The page shows those five steps in order. The Phase 10 chain `corr-p10b-doc-20261018-001` is on the recipe audit band. | CLOSED |
| DEV-009 | B7. Both apps run scenarios 7 to 11. Matches are shown. Each difference traces to a lake item. | Phase 17 compare page in the browser. The servers do not call each other. | The page lists the match rows from the clicks above. The two differences stay: Application A has no lineage route, and the 50,000 label is `proposed` on Application B only. | CLOSED |
| DEV-010 | Section 4 says agents run in LangGraph and the approval pause uses `interrupt()`. Application B has no such pause. | Phase 18 copies the pause pattern into Application B. Tools read the lake. `interrupt()` stores the pause in `apps/app_b/runtime/checkpoints.sqlite3`. Resume requires a different person from `proposed_by`. Phase 17 calls the existing `POST /api/agent/run` and does not add that pause. | Application B pauses with `interrupt()`, stores the pause, and resumes only for a different person. | CLOSED |
| DEV-011 | A restart mid-approval is required on Application A only. Guideline 17 asks for that approval path on both apps. | Phase 18 starts the Application B pause, kills that process, starts it again, and reads the same correlation id. The id is new for Phase 18. It does not reuse `corr-p10b-kill-20261018-001`. The Phase 10 Done test stays the Application A kill. | After the Application B process is killed and started again, the waiting approval and its correlation id are still on the case. | CLOSED |
| DEV-012 | `Project_Intent.md` section 10.3 names five agent workflows. The playbook builds one investigation graph. | Phase 18 adds the change-impact analyst, the evidence-pack assembler, and the operational handoff beside investigation. Each job has a tool list, one waiting role, and one audit row. The model still has no write tool. | Each of those three workflows has a read-only tool list, a person who must approve, and one audit row. | CLOSED |
| DEV-013 | Section 12.1 asks for federated identity and a rejected anonymous call. Phase 8 and Phase 13 can pass on a healthy stack and an identity document. | Phase 18 rejects a case read that has no `X-Api-Key` and shows that rejection on the React page. A federated identity provider stays out of this phase. No provider was named. | A case read with no `X-Api-Key` fails. A case read with the demo key and a role succeeds. | CLOSED |
| DEV-014 | Phase 8 names CI files. The Done test does not run a pipeline. Section 13 asks for a gated release. | Phase 18 runs `.github/workflows/verify.yml` once, or the same steps locally when GitHub is not available, and saves the log under `docs/44-remaining-deviations/`. A failed test fails the job. | The pipeline log exists, and a failed check stops the run. | CLOSED |
| DEV-015 | Phase 13 says telemetry is live. The Done test checks a recovering failure, a dead-letter replay, and the token note. | Phase 18 writes one JSON log line from one scenario click. That line contains the correlation id. It does not add a new metrics product. | One JSON log line from one scenario click contains the correlation id. | CLOSED |
| DEV-016 | Sections 12.1 and 13 ask for a scan that blocks release, a signed image, and a secret vault. Phase 13 asks for two documents. | Phase 18 records the image digest from the Phase 17 image build and reads the demo API key from a gitignored file path. A company signing service and a company vault stay unnamed. | The image digest from the Phase 17 image build is recorded, and the demo API key is read from a gitignored file path. A company signing service and a company vault stay unnamed. | CLOSED |
| DEV-017 | Section 9.2 names the entities and the metric fields the semantic layer must define. Phase 5 checks the build, the golden questions, and version 1.0.0. | Phase 18 checks one lake term for lot, wafer, tool, chamber, recipe revision, metrology sample, engineering change, replay, and approval. Those nine terms are already in the pinned lake at version 1.0.0. Metric rows show the field list. A cell with no signed owner stays Unknown and still shows the field name. The version stays 1.0.0. Compiling new statements changes the item ids search returns, and the saved replies then miss. Phase 17's pin stays that same hash. | Each of those terms has one definition. A metric row names population, event time, ingestion time, window, exclusions, status, unit, and owner, or the cell stays Unknown with that field list visible. | CLOSED |
| DEV-018 | Section 9.3 asks five relationship questions. Phase 5 says the graph tests pass and does not name the five questions. | Phase 18 answers the five questions from the `edges` table. Each answer cites an edge. New links are statements with a locator. Phase 17 walks one rule. | The five answers each cite an edge: lots on a recipe revision, tools and metrology for an excursion, the policy at event time, the documents and code for that policy, and the changes that affect a workflow. | CLOSED |
| DEV-019 | Phase 10 integrates the systems of record. Its Done test never posts a message from port 8090 into the queue. | Phase 18 adds a button that receives one message from port 8090 and places it on the session queue. This is separate from the DEV-003 session replay of ref `C00001646`. The packaged store stays unchanged. | The queue count rises by 1 after a successful gateway delivery, and the message id on the page matches the gateway body. | CLOSED |
| DEV-020 | Phase 12 says no injection drives an action. The Done test does not name port 8110. | Phase 18 posts the same injection on port 8100 and port 8110. The React page has one Injection button that shows BLOCK on both. The OPA rules already used for this block stay as they are. | Both posts return BLOCK. Case status and approvals stay as they were. | CLOSED |

Worked example for a later check. DEV-003 is CLOSED when the React page for Replay shows the queue count go from its start value to that value plus 1, then back after RT-05 confirms, and `partner_feeds` still has 67 rows with status `REPLAY`.

Worked example for a row Phase 17 leaves open. DEV-010 stays OPEN when Application B's investigate call returns a verdict and Application B still has no `interrupt()` pause and no checkpoint file.

---

## How Phase 17 closes DEV-001

The seven blocks above stay the text that must land in the prompts. They are step 1 of the Phase 17 plan. An editing session writes them before the coordinator starts. That session does not re-grade Phase 8, 9, 11, or 16.

The image owner is fixed here, because the deviations text above left two choices. Phase 8's Python-only `Dockerfile.platform` stays the record of that phase. Phase 17 Half B installs Node in that file and builds the React screens. Phase 9 is not reopened to do it. `playbook/phase_08_foundations.md` gains one forward pointer that says Phase 17 may add Node.

| Tracking | Prompt that receives the text | What the later check reads | Status |
|---|---|---|---|
| DEV-001-C1 | `playbook/00_coordinator.md` spawn paragraph | The Phase 17 handoff lists section 4, `adr-two-applications.md`, and the sentence "Screens are React." The first phase file opened is `playbook/phase_17_demo_ready.md`. | CLOSED |
| DEV-001-C2 | `playbook/executor.md` | The rule is present. A screen unit of only static HTML would return BLOCKED and name the ADR. | CLOSED |
| DEV-001-C3 | `playbook/phase_08_foundations.md` | The forward pointer names Phase 17 as the owner of the Node install. The Phase 8 PASS row is unchanged. | CLOSED |
| DEV-001-C4 | `playbook/phase_09_app_a.md` | The locked-fact row and the Done-test screen check are present. The Phase 9 PASS row is unchanged. The files that satisfy the check are built in Phase 17. | CLOSED |
| DEV-001-C5 | `playbook/reviewer.md` | A missing React app on a phase whose Done test requires React is a FAIL, and it is not extra scope. | CLOSED |
| DEV-001-C6 | `playbook/phase_11_app_b.md` | The same React check is on `apps/app_b/ui/`. Rules still come only from the lake. The Phase 11 PASS row is unchanged. | CLOSED |
| DEV-001-C7 | `playbook/phase_16_final_asbuilt_prd.md` | The screen sentence check is present. The Phase 16 PASS row is unchanged. After Half B, the as-built docs may keep the word React because the UI folders contain a React app. A sentence that still disagrees is corrected in `docs/43-demo-ready/` and names the old sentence. | CLOSED |

DEV-001 is CLOSED only when DEV-001-C1 through DEV-001-C7 are CLOSED and the DEV-001 correction check in the index passes.

The coordinator start check sits on DEV-001-C1. Fail that check when the first phase file is anything other than `playbook/phase_17_demo_ready.md`, or when a Phase 0 to 16 gate cell changed.

---

## Order to apply the corrections

Apply them in this order. A later block depends on the earlier one. This order does not re-run a PASS phase.

1. Step 1, editing session. Write DEV-001-C1 through DEV-001-C7 into the standing prompts. Add Phase 17 to `Execution_Plan.md`. Add FD-26. Add one Phase 17 row to `playbook/STATUS.md`. Leave every Phase 0 to 16 PASS cell as it is.
2. Write `playbook/phase_17_demo_ready.md`.
3. New coordinator chat. It reads `playbook/STATUS.md` and opens Phase 17 only.
4. Phase 17 Half A. Write `docs/43-demo-ready/` with the bands, the buttons, the roles, the lake items, and the React folder layout. Stop for acceptance.
5. Phase 17 Half B. Install Node. Build the React screens. Build the session, the lake statements, and the clicks for DEV-002 through DEV-009.
6. Run the correction check on DEV-001 through DEV-009. Mark a row CLOSED only when that check passes. Leave DEV-010 through DEV-020 OPEN until Phase 18. Phase 17 does not close them.
7. After the Phase 17 gate is PASS, write `playbook/phase_18_remaining_deviations.md` if step 1 has not already written it.
8. The coordinator opens Phase 18 only. It does not open Phase 0.
9. Phase 18 Half A. Write `docs/44-remaining-deviations/` with one close path and one Done test for DEV-010 through DEV-020. Stop for acceptance.
10. Phase 18 Half B. Build those eleven closes. Mark a row CLOSED only when its correction check passes.

---

## What this file does not do

This file does not edit the playbook. This file does not add a React app. This file does not replace React with HTML in the ADR. This file does not clear a PASS row in `playbook/STATUS.md`. This file does not claim that FastAPI, LangGraph, OPA, SQLite, or Compose drifted. The screen row is DEV-001. The demo rows are DEV-002 through DEV-009. Phase 17 closes those rows. Phase 18 closes DEV-010 through DEV-020.
