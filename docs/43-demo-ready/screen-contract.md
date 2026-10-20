# Screen contract

| Field | Value |
|---|---|
| Stage | Phase 17 / Live demo and React screens. Half A. |
| Date / version | 2026-10-19, v1.5 |
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
5. Audit rows. This band appears when the click returned a correlation id or at least one audit row. On the recipe page of Application B the Phase 10 chain `corr-p10b-doc-20261018-001` stays on this band even when the current click has no id.

JSON from the API stays behind a closed Details section. The person does not have to open it to finish the click.

## Scenario tabs

The seven scenarios are tabs: Replay, Recipe, Clocks, Policy, Outage, Rule trace, and Compare. Each tab shows the scenario name and the case under it. Replay shows C00001646. Recipe shows L00000016. Clocks shows E-00000000. Policy shows FAB-00000002. Outage shows INC-2025-014. Rule trace shows Recipe rule path. Compare shows Both apps.

The open tab uses the class `scenario-current`. A tab change clears the latest-action line, the model sentence, the cited items, the audit rows, and the Compare reading. The stored case status stays. A dropped delivery still reads dropped when Replay is opened again. A tab change does not clear the session overlay.

Rule trace is present on Application A and tells the person the lineage route is on Application B only. That is one of the two known differences.

**Start this shift again** sits in the header. It clears the session overlay. It does not change the packaged sqlite files.

The situation sentence names the case. Example: Partner feed REPLAY-000000000 is a second delivery of C00001646.

## Buttons

| Button | Who may use it | What the page does |
|---|---|---|
| Review this delivery | Any signed-in demo role | Raises the work-queue count by 1 and explains the duplicate. The evidence table shows ingest `2022-04-25T19:09` and `2022-04-25T20:09`. The result names the answer source. |
| Drop this duplicate | RT-05 Operations Analyst | Returns the queue count to the start value. The evidence row This delivery changes to dropped. The packaged store stays at 67 `REPLAY` rows. Another role sees “Confirm drop waits for RT-05.” and the evidence row stays put. |
| Explain this mismatch | Any signed-in demo role | Explains lot `L00000016` on tool `T0000013`. Dispatch is `R02`. The tool is `R01`. The result names the answer source. |
| Hold | RT-03 Process Engineer | The button stays clickable. A successful hold changes the evidence row to recorded by that actor id. Another role, or the same person as `proposed_by`, sees the refusal on the latest-action line and the evidence row stays “not recorded”. |
| Place this event on the timeline | Any signed-in demo role | Places `E-00000000` at event time `2020-12-30`. Arrival time `2021-01-01` is a second mark. |
| Ask which policy applies | Any signed-in demo role | Abstains. Four US policies are in force on `2024-06-01`. |
| Record my decision | RT-04 Policy Owner | Records keep-wait. |
| Check the upstream link | Any signed-in demo role | Shows attempt count 2 against port 8090. |
| Check the message shape | Any signed-in demo role | Shows attempt count 1. The sentence matches that count. |
| Set this intake aside | Any signed-in demo role | Lists the parked row. |
| Bring the parked intake back | Any signed-in demo role | Leaves the row listed as `REPLAYED`. |
| Record the owner | RT-06 Operations Lead | Types the owner of `INC-2025-014`. Any other role sees the refusal sentence. |
| Show where this rule came from | Any signed-in demo role on Application B | Shows the five existing steps. Application A says the trace is on Application B. |
| Compare this case | Any signed-in demo role | The browser reads both apps. The servers do not call each other. |

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

The five bands sit on one sheet under the open tab. The page canvas is `#e8eef2`. The sheet is `#fbfcfd`. Body text is `#1c2833`. The header is `#143044` with an amber line `#c9842a`. The open tab mark and the primary action are teal `#0e7c66`. A refusal line is `#fdecea` with a red bar. These colors are neutral. They are not copied from a company website. Official Birlasoft assets are still not in hand.

The header shows the app name, the port, the model mode, the role, the actor id, and Start this shift again. The words Role picker stay on the page. The model mode is `azure` or `replay`. The page does not show a key.

The open scenario stays highlighted. The situation sentence names the case. Example: Partner feed REPLAY-000000000 is a second delivery of C00001646. A switch to another tab returns the result lines to Ready and leaves the previous model sentence off that page.

The evidence table is wide enough to read the ingest times, the recipe rows, and the policy dates.

The first button of the open scenario is the primary button. The other buttons that scenario already requires stay on the same panel. Review this delivery and Drop this duplicate both stay. Hold stays clickable. A line under Drop, Hold, Record my decision, and Record the owner names the role that can record that action. The outage page has an owner box.

Access and untrusted text stays in a second row: Open the case with no identity, Try to approve from the feed note, and Take the next gateway message.

The result panel shows the latest-action line on every tab. While the call is in flight it names the work. A refusal stays on that line and names the current role. A success names the new count or status. The model sentence, the answer source, and the cited item ids appear under that line only after Review this delivery or Explain this mismatch returns them. The answer source is Azure OpenAI, a replay file, or a lake statement. Application B does not label an answer as Azure OpenAI. Clocks, Policy, Outage, Rule trace, and Compare do not print those three lines. JSON stays behind Details.

Application B uses the same layout. Rule trace stays an ordered list on Application B only. Application A still has no lineage route.

`Dockerfile.platform` installs Node and runs `npm install` and `npm run build` in both folders. FastAPI serves `dist/index.html` and `dist/assets`. A folder that is only `index.html`, `assets/app.js`, and `assets/styles.css` fails Half B.

Application B does not import Application A rule functions. Sharing this screen file list does not share rule code.
