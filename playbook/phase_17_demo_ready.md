# Phase 17 — Live demo and React screens

> Outside the 46 spine units. Decision gate: FD-26. Closes DEV-001 through DEV-009.

Build phase. Two halves. Half A writes the screen contract in `docs/43-demo-ready/` and stops. Half B installs Node, builds the React screens, and builds the seven click paths. The coordinator opens this file only when every Phase 0 to 16 gate is PASS. It does not open Phase 0. It does not spawn the Phase 8, 9, 11, or 16 executors.

## Inputs

- `Execution_Plan.md` section 4, section 10, and section 11
- `docs/10-architecture/adrs/adr-two-applications.md`
- `Deviations_From_Original_Execution_Plan.md` rows DEV-001 through DEV-009
- `Decision_Tracker.md` FD-26
- `playbook/STATUS.md` (Phase 0 to 16 gates are PASS; do not change those cells)
- `Dockerfile.platform`, `compose.yaml`
- `apps/app_a/`, `apps/app_b/`
- The packaged sqlite files, read only. Do not run `reconcile()` on them.

## Prompt

```text
# Phase 17 — Live demo and React screens

## Objective
Install React and build the live clicks a person uses for scenarios 7 to 13. Close DEV-001 through DEV-009 when each correction check passes. Leave DEV-010 through DEV-020 open.

## Scope
`docs/43-demo-ready/`, both UI folders, the session overlay, the recovery counts, and the lake statements those clicks read. Exclude: reopening Phase 0 to 16; editing files under `docs/42-executive/`; running `reconcile()` on the packaged store; the Application B LangGraph pause; the three extra agent jobs; a rejected anonymous call as the close for DEV-013; a pipeline run; a correlation-id log line as the close for DEV-015; an image digest; the term list; the five edge answers; a successful gateway delivery as the close for DEV-019; the injection button.

## Sub-stages
- Live demo and React screens. `docs/43-demo-ready/`.

## Required analysis (Half A)
Name every band, button, role, lake item, and the React folder layout. An open question that leaves the layout for later fails Half A.
Name what stays unchanged: the packaged sqlite hash, no `reconcile()` on that store, replay mode, the empty write-tool list, Application B does not open the inherited files, and the owner of `INC-2025-014` stays empty.
STOP after Half A. Return the seven-item final response for Half A. Wait for HALF_A_ACCEPTED.

## Required work (Half B, after acceptance)
1. Replace the static pages. `apps/app_a/ui/` and `apps/app_b/ui/` are React source. `package.json` lists `react`. At least one file is JSX or TSX. `Dockerfile.platform` installs Node and runs the build. FastAPI on ports 8100 and 8110 serves the built files.
2. Use the same five bands on both apps: situation, evidence table, one action, result, and audit rows for the correlation id. The scenario bar is Replay, Recipe, Clocks, Policy, Outage, Rule trace, and Compare. Start the demo again clears the session. JSON stays behind a closed Details section. The role picker still sends `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role`.
   The presenter layout is part of this step. A header shows the app name, the port, the role, and the actor id. The open scenario stays highlighted. The five bands are separate panels, in order. The situation sentence names the open scenario and the app. The evidence table is wide enough to read the ingest times, the recipe rows, and the policy dates. The first button of the open scenario is the primary button. The other buttons that scenario already requires stay on that panel. Receive and Confirm drop both stay. Hold stays disabled until RT-03 is a different person from `proposed_by`. Later checks stay in a second row: Read a case with no key, Injection, and Receive one gateway message. The result panel shows one sentence after a click, such as the work-queue count. Application B uses the same layout. Rule trace stays a React list on Application B only. Colors stay neutral. Do not copy a company website stylesheet, logo, or image.
3. Add a session store per app. It holds the received replay, the applied backfill, the approval, the parked intake, and the last probe. Confirming a drop changes the session row only.
4. Add lake statements, then a version bump and an ADR. New items are statements with a locator. They are not copies of raw rows. Application B reads these items. Application A may also read the packaged columns, and the values must match.
5. Build the seven click paths in the Done test.

## Evidence rules
Every screen fact cites a lake item or a packaged column. Classify claims as Verified Fact, Inference, Assumption, or Unknown. A session count is REAL for the session and does not change the packaged store.

## Constraints and guardrails
Do not clear a Phase 0 to 16 PASS cell. Do not replace React with HTML in the ADR. Do not run `reconcile()` on the packaged store. Application B still does not call Application A. The owner of `INC-2025-014` stays empty unless a person at RT-06 types one during the outage page. The model has no write tool. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| Screen library | React. FastAPI on the same port serves the built files. |
| Node owner | Phase 17 edits `Dockerfile.platform`. Phase 8's Python-only image stays the record of that phase. |
| Session | Overlay only. Packaged sqlite stays read-only. |
| Replay pair | Ref `C00001646`. `FEED-000000000` ingested `2022-04-25T19:09`. `REPLAY-000000000` ingested `2022-04-25T20:09`. Same source time `2022-04-25T19:39`. Packaged store stays at 67 `REPLAY` rows. |
| Recipe rows | Step `PS000000016`, etch, `2023-01-05T16:00` to `2023-01-05T23:00`, dispatch R02, tool `T0000013` recipe R01, no tool effective date. Change `ECN0000001`, etch, R01 to R02, effective `2023-01-01T07:00`, `APPROVED`. |
| Clocks | Event `E-00000000`. Event time `2020-12-30`. Arrival time `2021-01-01`. Kind `tool_alarm`. Metrology samples have no clock. |
| Policy date | Five US policies. On `2024-06-01`, four are in force. |
| Rule link | `implements` from `rule.recipe_release.limit.v2023.emea` to the transformed `evaluate_live_policy` code item. |
| Known differences | Application A has no lineage route. The 50,000 label is `proposed` on Application B only. |
| Write tools | Empty. `MODEL_MODE=replay`. |

## Decision gate (before you start)
FD-26 is DECIDED, authority: team-force. No Business Owner decision is required. Do not invent an identity provider, a company vault, a signing service, a KPI floor, or a dollar benefit.

## Required artifacts
`docs/43-demo-ready/` in Half A. React source, the Node image step, the session routes, and the lake statements in Half B. Standard header on the docs.

## Completion gate
Half A PASS when the contract names every band, button, role, lake item, and the React folder layout. Half B PASS when both UI folders have a `react` dependency and JSX or TSX source, the image builds those apps, FastAPI serves the built files, and the seven click paths change the session counts in the Done test. BLOCKED otherwise.

## Required final response (after each half)
Return the seven items.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/43-demo-ready/screen-contract.md` (Half A) | Header. Five bands, the scenario bar, every button, every role, and the React folder layout. |
| `docs/43-demo-ready/lake-statements.md` (Half A) | Header. The replay pair, the recipe rows, the clocks, the policy date, and the `implements` link. Each item is a statement with a locator. |
| `docs/43-demo-ready/unchanged.md` (Half A) | Header. Packaged sqlite hash, no `reconcile()`, replay mode, empty write-tool list, Application B does not open the inherited files, owner of `INC-2025-014` stays empty. |
| `apps/app_a/ui/` and `apps/app_b/ui/` (Half B) | `package.json` lists `react`. At least one JSX or TSX file. FastAPI serves the build. The presenter layout has a header, a highlighted scenario, five panels, one primary button, a later-checks row, and a result sentence. `public/assets/styles.css` sets a light page and dark text. |
| `Dockerfile.platform` (Half B) | Installs Node and runs the React build. |
| Session and recovery routes (Half B) | The seven click paths below. |

## Done test

Fail the handoff when the coordinator's first phase file is anything other than `playbook/phase_17_demo_ready.md`. Fail the handoff when a Phase 0 to 16 gate cell changed.

Half A passes when `docs/43-demo-ready/` names every band, button, role, lake item, and the React folder layout, and names what stays unchanged.

Half B passes when both UI folders have a `react` dependency and JSX or TSX source, `Dockerfile.platform` installs Node and builds those apps, and FastAPI serves the built files. A test loads each scenario page and checks the evidence table. The session actions change the counts below. The as-built docs do not say React while the UI folders lack a React source file.

The presenter layout also passes only when both apps show a header with the app name, the port, the role, and the actor id; the open scenario stays highlighted; the five bands are separate panels; the situation sentence names the open scenario and the app; the first button of the open scenario is the primary button; the later checks sit in a second row; and the result panel shows one sentence after a click. A page of unstyled default controls fails this check.

Click path:

1. Replay. Receive the replayed MESDispatch raises the work-queue count by 1. RT-05 Confirm drop returns that count. Evidence shows ingest `2022-04-25T19:09` and `2022-04-25T20:09`. The packaged store stays at 67 `REPLAY` rows.
2. Recipe. The page shows R02 at `2023-01-05T16:00`, tool R01 with no effective date, and `ECN0000001` effective `2023-01-01T07:00`. Investigate calls `POST /api/agent/run`, shows `HOLD_FOR_REVIEW`, and keeps the hold button disabled until RT-03 is a different person from `proposed_by`.
3. Clocks. Apply the backfilled event places `E-00000000` at event time `2020-12-30`, with arrival time `2021-01-01` as a second mark. The page says metrology samples have no clock.
4. Policy. Four policies are in force on `2024-06-01`. Check the overlap abstains. RT-04 records keep-wait or a named policy id.
5. Outage. Both apps. Timeout shows attempt count 2 against port 8090. Schema shows attempt count 1, and the sentence matches that count. Park a bad intake lists the row. Replay the parked intake leaves it listed as `REPLAYED`. Compose sets `SOURCE_GATEWAY_URL` for both apps. Application B gains the same recovery fields as Application A.
6. Rule trace. Application B only. Five ordered steps: historical decision, earlier code `code.legacy_policy.js_allow`, specification `data.contract.decision_policies_archive`, test `test.rule.recipe_release.emea_2023`, transformed implementation. The Phase 10 chain `corr-p10b-doc-20261018-001` stays on the recipe audit band.
7. Compare. A browser page calls 8100 and 8110. The servers do not call each other. Match rows come from the clicks above. The two known differences stay.

A person then clicks the seven paths once on the running stack. That click-through stays `NEEDS_HUMAN` if Compose is not already up. The reviewer does not invent a health pass.

Mark DEV-001 through DEV-009 CLOSED only when each correction check in `Deviations_From_Original_Execution_Plan.md` passes. Leave DEV-010 through DEV-020 OPEN.
