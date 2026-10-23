# Scenario demo scripts

These six scripts use the buttons on the current consoles. Each script can be read on its own.

Application A is http://127.0.0.1:8100. Application B is http://127.0.0.1:8110. Sign in as the person named in the step. There is no role picker. Sign in again if the one-time code is older than five minutes. The draft author stays `model_draft`.

Read the runtime pill before the first click. Compose starts these apps in replay when `MODEL_MODE` is unset. The containers checked on 20 October 2026 reported `azure`. If the pill says replay, the page reads a saved explanation and a hit shows "Answer source: a replay file." If the pill says azure, the page asks Azure OpenAI and a successful call shows "Answer source: Azure OpenAI." Read the answer-source line the page shows.

Before each script, click **Start this shift again** on the app you are about to use. The page keeps a shift record in memory. That click clears the shift record. It does not rewrite the packaged sqlite files.

A click changes what this page shows for this shift. Packaged replay rows stay 67. After the shift record is clear, Application A’s work-queue start count is 196. The result line prints the count. Read the number on that line. Application B’s queue count is separate. Do not expect 196 on Application B.

The role names on the picker are:

- RT-01 Fab Exception Reviewer
- RT-02 Shift Lead
- RT-03 Process Engineer
- RT-04 Policy Owner
- RT-05 Operations Analyst
- RT-06 Operations Lead

## 1. Replay

### Background business scenario

A fab receives messages about lots from partner systems and from tools. The same message can arrive a second time. Reference `C00001646` arrived at `2022-04-25T19:09`. Partner feed `REPLAY-000000000` is that same delivery again, at `2022-04-25T20:09`.

If both copies stay on the work queue, the shift counts one arrival twice. If the wrong copy is dropped, a real delivery leaves the queue. The page therefore names the role that may drop the copy before the drop is recorded.

The partner system sent the feed. RT-01 Fab Exception Reviewer reads the two times and puts the second delivery on the queue. RT-05 Operations Analyst confirms the drop. Any other role is refused.

Both applications have this tab. Do this script on Application A.

### Steps

| Step | Who | App | What they do | What the screen shows | What is stored |
|---|---|---|---|---|---|
| 1 | Presenter | Application A, port 8100 | Click **Start this shift again**. Open the Replay tab. | The situation sentence is "Partner feed REPLAY-000000000 is a second delivery of C00001646." Feed ingest is `2022-04-25T19:09`. Replay ingest is `2022-04-25T20:09`. Packaged REPLAY rows is 67. This delivery is `not on the queue`. The result line says Ready. | The shift record is clear. The packaged file still has 67 replay rows. |
| 2 | RT-01 Fab Exception Reviewer | Application A | Sign in as reviewer.tw. Click **Review this delivery**. | While the call runs, a replay pill says "Reading the saved explanation for the second delivery." An azure pill says "Asking Azure OpenAI to explain the second delivery." On success the result line says "The second delivery is on the work queue. Work-queue count is 197. Packaged replay count is 67." This delivery changes to `on the work queue`. Under the result line, the page shows the sentence, the answer source, and the cited item ids. Read those three lines from the screen. If the result starts with Failed, read that sentence. The delivery can still be on the queue, because the queue update runs before the explanation. | The shift record marks this delivery as on the queue. The work-queue count is the start count plus 1. The packaged row count stays 67. |
| 3 | RT-01 Fab Exception Reviewer | Application A | Stay on RT-01. Click **Drop this duplicate**. | The result line says "Refused. Confirm drop waits for RT-05. The current role is RT-01." This delivery stays `on the work queue`. | The shift record does not drop the delivery. |
| 4 | RT-05 Operations Analyst | Application A | Sign in as analyst.az. Click **Drop this duplicate**. | The result line says "RT-05 dropped the duplicate. The work-queue count returned to the start value. Work-queue count is 196. Packaged replay count is 67." This delivery changes to `dropped`. | The shift record marks the delivery dropped. The work-queue count returns to 196. The packaged row count stays 67. |

## 2. Recipe

### Background business scenario

A lot is sent to an etch tool with a recipe named by dispatch. The tool can still be running an older recipe. Lot `L00000016` on tool `T0000013` shows dispatch recipe `R02` at `2023-01-05T16:00`. The tool recipe is `R01`. Change `ECN0000001` moved the recipe from `R01` to `R02`. That change is approved and effective `2023-01-01T07:00`. The tool row has no effective date.

The mismatch matters because the lot may have run the recipe dispatch did not name. A person has to read both facts before anyone holds the lot.

RT-01 Fab Exception Reviewer asks for the explanation. The model drafts a sentence. The model has no write tool. RT-03 Process Engineer records the hold. The draft author is `model_draft`. The person who clicks Hold must be RT-03, and the actor id must be different from `model_draft`. The actor id `engineer.az` meets that rule.

Both applications have these two buttons. Do the clicks on Application A. Say that Application B has the same two buttons.

### Steps

| Step | Who | App | What they do | What the screen shows | What is stored |
|---|---|---|---|---|---|
| 1 | Presenter | Application A, port 8100 | Click **Start this shift again**. Open the Recipe tab. | The situation sentence is "Lot L00000016 on tool T0000013 shows dispatch recipe R02 and tool recipe R01." Dispatch is `R02` at `2023-01-05T16:00`. Tool recipe is `R01` on `T0000013`, with effective date none. Change is `ECN0000001` effective `2023-01-01T07:00` APPROVED. Hold is `not recorded`. | The Hold line on the page is clear. |
| 2 | RT-01 Fab Exception Reviewer | Application A | Sign in as reviewer.tw. Click **Explain this mismatch**. | While the call runs, a replay pill says "Reading the saved explanation for the recipe mismatch." An azure pill says "Asking Azure OpenAI to explain the recipe mismatch." On success the result line says "The mismatch is explained." The sentence says dispatch recipe `R02` and tool recipe `R01` disagree. It names change `ECN0000001`, effective `2023-01-01T07:00`, and the lot start `2023-01-05T16:00`. It says the tool row still says `R01` and has no effective date. The cited items include `rule.recipe.mismatch_show_both`. Read the answer source from the screen. Hold stays `not recorded`. | The sentence states why the two recipes disagree. It does not write a hold. |
| 3 | RT-01 Fab Exception Reviewer | Application A | Stay on RT-01. Click **Hold**. | The result line says "Refused. Hold waits for RT-03. The current role is RT-01." Hold stays `not recorded`. | No hold is written. |
| 4 | RT-03 Process Engineer | Application A | Sign in as engineer.az. Do this within five minutes of the one-time code. Click **Hold**. | The result line says "Hold recorded by engineer.az." Hold changes to `recorded by engineer.az`. If the Audit band appears, read the correlation id on that band. | The page shows the hold for this shift. The server keeps that approval in memory for case `PS000000016` until the process restarts. The packaged sqlite file is not rewritten. |

On Application B, the Recipe tab has the same two buttons and the same evidence rows. The Audit band on Application B also shows "Phase 10 chain corr-p10b-doc-20261018-001." That id is the earlier chain. It is already on the page.

## 3. Clocks

### Background business scenario

A tool alarm has two times. One time is when the event happened. The other time is when the message arrived. Those times can fall on different dates. Event `E-00000000` is a tool alarm. The event time is `2020-12-30`. The arrival time is `2021-01-01`. The metrology samples for this case have no clock.

If a reviewer folds both times into one cell, the shift cannot tell the day the tool alarmed from the day the message arrived. The page keeps the two times in two cells.

RT-01 Fab Exception Reviewer places the event on the timeline. No other role is required for this button.

Both applications have this tab. Do this script on Application A.

### Steps

| Step | Who | App | What they do | What the screen shows | What is stored |
|---|---|---|---|---|---|
| 1 | Presenter | Application A, port 8100 | Click **Start this shift again**. Open the Clocks tab. | The situation sentence is "Evidence E-00000000 has an event time and a later arrival time." Event is `E-00000000`. Event time is `not applied`. Arrival time is `2021-01-01`. Metrology is "Metrology samples have no clock." | The event time has not been placed for this shift. |
| 2 | RT-01 Fab Exception Reviewer | Application A | Sign in as reviewer.tw. Click **Place this event on the timeline**. | The result line says "Event E-00000000 is on the timeline at 2020-12-30. Arrival time 2021-01-01 stays a second mark." Event time changes to `2020-12-30`. Arrival time stays `2021-01-01`. Metrology stays "Metrology samples have no clock." | The shift record marks the event time as placed. The two times stay in two fields. The packaged file is not rewritten. |

## 4. Policy

### Background business scenario

A fab can have several US policy windows that cover the same date. Fab `FAB-00000002` is checked on `2024-06-01`. Four windows are in force on that date: `POL-0002` from `2023-01-01` to open, `POL-0010` from `2021-01-01` to open, `POL-0018` from `2024-01-01` to `2024-12-31`, and `POL-0026` from `2022-01-01` to open. The page prints the word open when a policy has no end date. A fifth id, `POL-0034`, starts on `2025-01-01`, so it is not in force on `2024-06-01` and the table does not list it.

The app lists the four windows and does not pick one. A person has to record the choice. RT-01 Fab Exception Reviewer asks which policy applies. RT-04 Policy Owner records `keep-wait`. That choice leaves the case waiting. It does not select a policy id.

Both applications have this tab. Do this script on Application A.

### Steps

| Step | Who | App | What they do | What the screen shows | What is stored |
|---|---|---|---|---|---|
| 1 | Presenter | Application A, port 8100 | Click **Start this shift again**. Open the Policy tab. | The situation sentence is "Fab FAB-00000002 has overlapping US policies on 2024-06-01." The table lists `POL-0002`, `POL-0010`, `POL-0018`, and `POL-0026` with the dates above. The count row says "In force on 2024-06-01" and the value is 4. Recorded choice is `none`. | No choice is stored yet. |
| 2 | RT-01 Fab Exception Reviewer | Application A | Sign in as reviewer.tw. Click **Ask which policy applies**. | The result line says "Four policies are in force. The app abstains and waits for RT-04." Recorded choice stays `none`. | The shift record marks the check as run. No policy id is chosen. |
| 3 | RT-01 Fab Exception Reviewer | Application A | Stay on RT-01. Click **Record my decision**. | The result line says "Refused. A policy decision waits for RT-04. The current role is RT-01." Recorded choice stays `none`. | No choice is stored. |
| 4 | RT-04 Policy Owner | Application A | Sign in as policy.owner. Click **Record my decision**. | The result line says "RT-04 recorded keep-wait." Recorded choice changes to `keep-wait`. | The shift record stores `keep-wait`. No policy id is selected. The packaged file is not rewritten. |

## 5. Outage

### Background business scenario

The console reads messages from the source gateway on port 8090. That link can time out. A message can also arrive with a shape the intake does not accept. When that happens, the shift can set the intake aside and bring it back later. The parked id on this page is `DLQ-DEMO-BAD`.

Incident `INC-2025-014` has no follow-up owner in the packaged data. The owner cell stays empty until RT-06 Operations Lead types an id and records it. RT-01 Fab Exception Reviewer can run the link check, the shape check, and the park buttons. RT-01 cannot record the owner.

Both applications have this tab. Do this script on Application A.

### Steps

| Step | Who | App | What they do | What the screen shows | What is stored |
|---|---|---|---|---|---|
| 1 | Presenter | Application A, port 8100 | Click **Start this shift again**. Open the Outage tab. Leave the Owner box empty. | The situation sentence is "Incident INC-2025-014 has no follow-up owner." The owner cell says `empty`. | The shift record has no owner and no parked intake. |
| 2 | RT-01 Fab Exception Reviewer | Application A | Sign in as reviewer.tw. Click **Check the upstream link**. | The result line says "Upstream timed out. Attempt count is 2. The probe target is port 8090." | The shift record keeps that probe sentence. The owner cell stays `empty`. |
| 3 | RT-01 Fab Exception Reviewer | Application A | Click **Check the message shape**. | The result line says "Upstream schema did not match. Attempt count is 1. This probe is not retried." | The shift record keeps that probe sentence. The schema probe does not add a second attempt. |
| 4 | RT-01 Fab Exception Reviewer | Application A | Click **Set this intake aside**. | The result line says "Intake DLQ-DEMO-BAD is parked." The evidence table adds a row `DLQ-DEMO-BAD` with status `PARKED`. | The shift record lists that intake as parked. The packaged file is not rewritten. |
| 5 | RT-01 Fab Exception Reviewer | Application A | Click **Bring the parked intake back**. | The result line says "Intake DLQ-DEMO-BAD is back. Status is REPLAYED." The same row now says `REPLAYED`. | The shift record changes that intake from parked to replayed. |
| 6 | RT-01 Fab Exception Reviewer | Application A | Leave the Owner box empty. Click **Record the owner**. | The result line says "Failed. Type an owner id, then record it." The owner cell stays `empty`. | No owner is stored. The click does not call the server, because the box is empty. |
| 7 | RT-01 Fab Exception Reviewer | Application A | Type `shift-lead-demo` in the Owner box. Stay on RT-01. Click **Record the owner**. | The result line says "Refused. The owner of INC-2025-014 stays empty unless RT-06 types one. The current role is RT-01." The owner cell stays `empty`. | No owner is stored. |
| 8 | RT-06 Operations Lead | Application A | Sign in as opslead. Leave `shift-lead-demo` in the Owner box. Click **Record the owner**. | The result line says "Owner shift-lead-demo is recorded for INC-2025-014." The owner cell shows `shift-lead-demo`. | The shift record stores that typed id for this shift. The packaged incident did not already contain this name. **Start this shift again** clears it. |

## 6. Rule trace

### Background business scenario

The recipe rule in the new console comes from earlier work, not from one new file. The path has five steps. A historical decision named the four programs. Earlier code allowed a policy in script. A specification holds the decision-policy archive. A test covers the 2023 EMEA recipe release. The transformed implementation is the live policy check.

A reviewer uses this list to see which item each step cites. The button does not change a lot, a hold, or a queue count.

Only Application B shows the list. Application A has the tab and tells the person to open Application B. The two servers do not call each other. Any signed-in demo role may click the button. This script uses RT-01.

### Steps

| Step | Who | App | What they do | What the screen shows | What is stored |
|---|---|---|---|---|---|
| 1 | Presenter | Application A, port 8100 | Open the Rule trace tab. | The page says "Application A has no lineage route. Open Application B for this trace." The actions band says "Open Application B for the rule trace." There is no **Show where this rule came from** button. | Nothing is written. |
| 2 | RT-01 Fab Exception Reviewer | Application B, port 8110 | Open the Rule trace tab. Click **Show where this rule came from**. | The situation sentence is "This page shows where the recipe rule came from." The list is: 1 historical decision `decision.bp4.four_programs`. 2 earlier code `code.legacy_policy.js_allow`. 3 specification `data.contract.decision_policies_archive`. 4 test `test.rule.recipe_release.emea_2023`. 5 transformed implementation `code.transformed.evaluate_live_policy`. The result line says "The ordered list above is the path for this rule." | The list is read from Application B. No lot, hold, or queue count changes. Application A is not called. |
