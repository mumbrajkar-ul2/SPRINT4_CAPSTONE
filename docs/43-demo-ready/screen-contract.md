# Screen contract

| Field | Value |
|---|---|
| Stage | Phase 17 / Live demo and React screens. Half A. |
| Date / version | 2026-10-20, v1.6 |
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

1. Situation. One sentence that says which scenario is open and which case is on screen. That sentence is the page title.
2. Evidence. The table for this object only. Rows have a label and a value. The values come from the lake statements in `lake-statements.md`.
3. Actions. The primary button for this page, then any decision that follows it. A short role line sits under each restricted action.
4. Result. The latest-action line, then the model sentence, the answer source, and the cited item ids only when those lines are filled.
5. Audit. This band appears when the click returned a correlation id or at least one audit row. On the recipe page of Application B the Phase 10 chain `corr-p10b-doc-20261018-001` stays on this band even when the current click has no id.

JSON from the API stays behind a closed Details section. The person does not have to open it to finish the click.

## Scenario tabs

The seven scenarios are tabs: Replay, Recipe, Clocks, Policy, Outage, Rule trace, and Compare. Each tab shows the scenario name and the case under it. Replay shows C00001646. Recipe shows L00000016. Clocks shows E-00000000. Policy shows FAB-00000002. Outage shows INC-2025-014. Rule trace shows Recipe rule path. Compare shows Both apps.

The strip is `role="tablist"`. Each tab is `role="tab"` with `aria-selected`. The open tab also has `aria-current="page"` and the class `scenario-current`. Arrow keys move across the strip. The open page’s primary button is a real button, so a keyboard user can reach it and activate it.

A tab change clears the latest-action line, the model sentence, the cited items, the audit rows, and the Compare reading. The stored case status stays. A dropped delivery still reads dropped when Replay is opened again. A tab change leaves the session overlay in place.

The page remembers which tab was open when the click started. If the person is on a different tab when the answer returns, the page leaves that answer off the latest-action line, the explanation, the audit rows, and the Compare reading. The check in source is `viewRef.current !== started`. The clear-on-switch function is `openScenario`.

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

The page background is light gray `#F2F2F2`. A solid red bar, `#ED1C24`, 16px wide, runs the full height of the viewport on the left. Content starts to the right of that bar.

The header is a white bar. Text is charcoal `#231F20`. From left to right the header shows: the Birlasoft word, the application name, the location as the port, the role picker, the actor id, and the runtime mode. Start this shift again is a quiet text action in `#666666`. The words Role picker stay on the page. The runtime mode is `azure` or `replay`, on a short pill of red tint `#FDEBEC`. The page leaves the key off the screen.

The right side of the header draws the cover motif once: two open arcs, no fill. The outer arc is an 8px stroke of `#ED1C24`. The inner arc is a 2px stroke of `#231F20`. No label, control, or logo crosses either stroke. The work sheet does not repeat the arcs.

The repo has no master artwork file. The header shows the word Birlasoft in Calibri, charcoal, semibold. That word is a text label. The clear space around it is at least the height of the “b”, and the slot is at least 76px wide. The logo image appears only when the master artwork file is in the repo. The header shows Birlasoft only. The parent lock-up is for a brief that asks for the CKA Birla Group.

The tab strip sits on the gray canvas, directly under the header, in one row about 40px tall. Tabs stay on one line. A narrow window scrolls the strip sideways. An inactive tab has no box and no fill. Its text is `#666666`, 14px, weight 400, Calibri. The second line under the name is the case id, also `#666666`. The open tab uses the white sheet, weight 600, charcoal text, and a 3px top line in `#ED1C24`. Its bottom edge meets the sheet.

The five bands sit on one white sheet under the open tab. The sheet has one border, `#E0E0E0`, and a soft shadow on the gray page. There is no gap between the open tab and the situation band. Inside the sheet the order is Situation, Evidence, Actions, Result, and Audit when Audit is filled. The situation sentence is 24px bold charcoal. Body text is 16px regular charcoal. Labels are 13px `#666666`. A small purple index `#72007D` marks the band number. Purple stays off the latest-action line, off page fills, and off buttons.

The open scenario stays marked. The situation sentence names the case. Example: Partner feed REPLAY-000000000 is a second delivery of C00001646. A switch to another tab returns the result line to Ready and leaves the previous model sentence off that page.

The evidence table is wide enough to read the ingest times, the recipe rows, and the policy dates. On a narrow window the table scrolls sideways. The red bar stays 16px.

The first button of the open scenario is the one primary button: filled `#ED1C24`, white text, at least 16px Calibri semibold. The other buttons that scenario already requires stay on the same band: charcoal text, white fill, hairline border. Review this delivery and Drop this duplicate both stay. Hold stays clickable. A line under Drop, Hold, Record my decision, and Record the owner names the role that can record that action. The outage page has an owner box. Drop, Hold, Record my decision, and Record the owner keep the quiet button. Red is the page’s main job, which is the first button.

Access and untrusted text stays below the sheet, in `#666666`, smaller type, with no red fill: Open the case with no identity, Try to approve from the feed note, and Take the next gateway message.

The result band shows the latest-action line on every tab. While the call is in flight the line names the work, uses gold tint `#FCF3DE`, and has a 4px gold bar `#EFBC4A`. A success uses that same gold line and names the new count or status. A refusal or a failure stays on the white page, with a charcoal left bar and charcoal text. The sentence starts with Refused or Failed, and a refusal names the current role. The model sentence, the answer source, and the cited item ids appear under that line only after Review this delivery or Explain this mismatch returns them. The answer source is Azure OpenAI, a replay file, or a lake statement. Both apps use those same three labels. Clocks, Policy, Outage, Rule trace, and Compare leave those three lines off the page. JSON stays behind Details.

Every run of text uses Calibri. Headings are bold or semibold. Body is regular. The face stays Calibri.

## Birlasoft tokens

| Token | Value | Use |
|---|---|---|
| Red | `#ED1C24` | Left page bar, open-tab mark, primary button |
| Charcoal | `#231F20` | Titles, body text, table text, lines, refusal bar |
| Purple | `#72007D` | Band index only |
| Gold | `#EFBC4A` | 4px left bar on the in-flight and success line |
| White | `#FFFFFF` | Header, work sheet, table body, logo background |
| Light gray | `#F2F2F2` | Page around the sheet |
| Red tint | `#FDEBEC` | Pill behind the runtime mode |
| Gold tint | `#FCF3DE` | Background of the in-flight and success line |
| Secondary text | `#666666` | Tab second lines, role hints, secondary checks, session reset |
| Hairline | `#E0E0E0` | The one border around the sheet, and quiet button borders |
| Primary text | `#FFFFFF` | Text on the red primary button |

Application B uses the same layout. Rule trace stays an ordered list on Application B only. Application A still has no lineage route.

`Dockerfile.platform` installs Node and runs `npm install` and `npm run build` in both folders. FastAPI serves `dist/index.html` and `dist/assets`. A folder that is only `index.html`, `assets/app.js`, and `assets/styles.css` fails Half B. A source save leaves the running container on the previous bundle until the image is rebuilt.

Application B keeps its own rule code. Sharing this screen file list leaves the rule code in each app.
