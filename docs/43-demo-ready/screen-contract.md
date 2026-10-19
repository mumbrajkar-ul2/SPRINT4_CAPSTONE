# Screen contract

| Field | Value |
|---|---|
| Stage | Phase 17 / Live demo and React screens. Half A. |
| Date / version | 2026-10-19, v1.1 |
| Author / agent | Executor agent (Grok 4.7), correlation id corr-p17a-doc-20261019-001 |
| Status | DESIGN. Half B builds only this layout. |
| Evidence sources | `Execution_Plan.md` section 4; `docs/10-architecture/adrs/adr-two-applications.md`; `Deviations_From_Original_Execution_Plan.md` DEV-001 through DEV-009; FD-26 |
| Assumptions | FastAPI on port 8100 serves Application A. FastAPI on port 8110 serves Application B. The two servers do not call each other. |
| Unresolved issues | A live click-through on Compose stays NEEDS_HUMAN until the stack is already up. |
| Residual risks | A page that prints only JSON would leave DEV-002 open. |

This file names the bands, the buttons, the roles, and the React folder layout. Half B builds this layout. It does not leave the folder layout open.

## Finding

**Finding.** Both apps use the same five bands and the same scenario bar. Application B adds the rule trace. Application A has no lineage route.
**Evidence.** `adr-two-applications.md` locks React served by FastAPI. DEV-002 through DEV-009 name the clicks.
**Impact.** Half B replaces `index.html`, `assets/app.js`, and `assets/styles.css` as the served page.
**Risk.** Serving the Vite source `index.html` without a build would show an empty page.
**Confidence.** High. The layout below is the Half B file list.
**Open questions.** None for the folder layout.

## Five bands

Every scenario page shows these five bands, in this order.

1. Situation. One sentence that says which scenario is open and which app is on screen.
2. Evidence table. Rows with a label and a value. The values come from the lake statements in `lake-statements.md`.
3. One action. One primary button for the scenario.
4. Result. The count, the verdict, or the timeline after the action.
5. Audit rows. The correlation id for that action. On the recipe page the Phase 10 chain `corr-p10b-doc-20261018-001` stays on this band for Application B.

JSON from the API stays behind a closed Details section. The person does not have to open it to finish the click.

## Scenario bar

The bar has seven buttons: Replay, Recipe, Clocks, Policy, Outage, Rule trace, and Compare.

Rule trace is present on Application A and tells the person the lineage route is on Application B only. That is one of the two known differences.

**Start the demo again** clears the session overlay. It does not change the packaged sqlite files.

## Buttons

| Button | Who may use it | What the page does |
|---|---|---|
| Receive the replayed MESDispatch | Any signed-in demo role | Raises the work-queue count by 1. The evidence table shows ingest `2022-04-25T19:09` and `2022-04-25T20:09`. |
| Confirm drop | RT-05 Operations Analyst | Returns the queue count to the start value. The packaged store stays at 67 `REPLAY` rows. |
| Investigate | Any signed-in demo role | Calls `POST /api/agent/run` for `PS000000016`. The result shows `HOLD_FOR_REVIEW`. |
| Hold | RT-03 Process Engineer | Stays disabled until RT-03 is a different person from `proposed_by`. |
| Apply the backfilled event | Any signed-in demo role | Places `E-00000000` at event time `2020-12-30`. Arrival time `2021-01-01` is a second mark. |
| Check the overlap | Any signed-in demo role | Abstains. Four US policies are in force on `2024-06-01`. |
| Record policy decision | RT-04 Policy Owner | Records keep-wait or a named policy id. |
| Probe timeout | Any signed-in demo role | Shows attempt count 2 against port 8090. |
| Probe schema | Any signed-in demo role | Shows attempt count 1. The sentence matches that count. |
| Park a bad intake | Any signed-in demo role | Lists the parked row. |
| Replay the parked intake | Any signed-in demo role | Leaves the row listed as `REPLAYED`. |
| Compare | Any signed-in demo role | The browser calls port 8100 and port 8110. |

## Roles

The role picker sends `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role`.

- RT-01 Fab Exception Reviewer
- RT-02 Shift Lead or Process Engineer
- RT-03 Process Engineer. Recipe hold. Must differ from `proposed_by`.
- RT-04 Policy Owner. Keep-wait or a named policy id.
- RT-05 Operations Analyst. Confirm drop.
- RT-06 Operations Lead. The owner of `INC-2025-014` stays empty unless this person types one on the outage page.

## React folder layout

Half B creates this tree under `apps/app_a/ui/` and the same tree under `apps/app_b/ui/`.

- `package.json` lists the `react` dependency.
- `vite.config.js` writes the build to `dist/`.
- `index.html` is the Vite entry.
- `src/main.jsx` starts the page.
- `src/App.jsx` is the five bands and the scenario bar.
- `src/api.js` calls `/api` on the same port.
- `public/assets/styles.css` is the presenter stylesheet. FastAPI serves it at `/assets/styles.css`.

## Presenter layout

The five bands are separate panels on a light page with dark text. The header is dark. The panels are white. One primary button is blue. These colors are neutral. They are not copied from a company website. Official Birlasoft assets are still not in hand.

The header shows the app name, the port, the role, and the actor id. The words Role picker stay on the page.

The open scenario stays highlighted. The situation sentence names that scenario and the app. Example: Application A on port 8100. Replay is open.

The evidence table is wide enough to read the ingest times, the recipe rows, and the policy dates.

The first button of the open scenario is the primary button. The other buttons that scenario already requires stay on the same panel. Receive the replayed MESDispatch and Confirm drop both stay. Hold stays disabled until RT-03 is a different person from `proposed_by`.

Later checks stay in a second row: Read a case with no key, Injection, and Receive one gateway message.

The result panel shows one sentence after a click, such as the work-queue count. JSON stays behind Details.

Application B uses the same layout. Rule trace stays an ordered list on Application B only. Application A still has no lineage route.

`Dockerfile.platform` installs Node and runs `npm install` and `npm run build` in both folders. FastAPI serves `dist/index.html` and `dist/assets`. A folder that is only `index.html`, `assets/app.js`, and `assets/styles.css` fails Half B.

Application B does not import Application A rule functions. Sharing this screen file list does not share rule code.
