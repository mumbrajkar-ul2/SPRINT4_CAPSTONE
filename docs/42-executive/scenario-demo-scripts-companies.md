# Company stories for the six demos

This file is the spoken version of the six demos. The click script is [scenario-demo-scripts.md](scenario-demo-scripts.md). Read that file for the button order. Read this file when you want to say the same steps with company names.

The six incidents are made up. NVIDIA, TSMC, Micron, and ASML are real companies. The product is the NVIDIA Blackwell B200. TSMC manufactures the GPU wafers. Micron supplies the HBM3E memory that is later placed on the B200 package. ASML builds the EUV scanners that print the wafer layers inside the TSMC fab.

The feed ids, lot ids, dates, policy ids, and button results are the ones on the console. Say the company names while you point at those ids. The counts in these stories are the console counts: 196, 197, and 67.

Application A is http://127.0.0.1:8100. Application B is http://127.0.0.1:8110. Sign in as the person named in the step. There is no role picker. Sign in again if the one-time code is older than five minutes. The draft author stays `model_draft`.

Before each story, click **Start this shift again** on the app you are about to use. That click clears the shift record. It leaves the packaged files as they are.

On Application A, after that click, the work-queue start count is 196. Packaged replay rows stay 67. Application B has its own queue count.

The role names on the picker are:

- RT-01 Fab Exception Reviewer
- RT-02 Shift Lead
- RT-03 Process Engineer
- RT-04 Policy Owner
- RT-05 Operations Analyst
- RT-06 Operations Lead

In these stories, RT-01, RT-03, RT-04, RT-05, and RT-06 are people on the TSMC shift that is building B200 wafers.

## 1. Replay

### Who is in this moment

Micron sends TSMC a notice about HBM3E stacks that will be paired with NVIDIA Blackwell B200 packages. The notice uses reference `C00001646`. TSMC already has that reference. The same notice then arrives a second time.

The other 66 packaged replay rows are the same kind of second copy, each on its own reference. This story uses one of them.

### The notice

Say this sentence while the Replay tab is open:

"METROLOGY_RESULT. HBM3E stack for NVIDIA Blackwell B200. Quality flag REVIEW. Reference C00001646."

That sentence is the spoken notice. The page prints the feed id and the two ingest times.

### What the person does

The first copy arrived at `2022-04-25T19:09` as feed `FEED-000000000`. The second copy arrived at `2022-04-25T20:09` as feed `REPLAY-000000000`. Both copies share the source time `2022-04-25T19:39`.

If both copies stay on the work queue, the shift counts one Micron notice twice. RT-01 Fab Exception Reviewer reads the two times and clicks **Review this delivery**. The work-queue count goes from 196 to 197. Packaged replay rows stay 67.

Sign in as reviewer.tw and click **Drop this duplicate**. The page refuses that role. Sign in as analyst.az and click **Drop this duplicate**. The second copy leaves this shift's queue. The work-queue count returns to 196. The packaged file still has 67 replay rows.

Do this story on Application A. Application B has the same tab.

### What the screen still shows

1. After **Start this shift again**, the situation sentence is "Partner feed REPLAY-000000000 is a second delivery of C00001646." Feed ingest is `2022-04-25T19:09`. Replay ingest is `2022-04-25T20:09`. Packaged REPLAY rows is 67. This delivery is `not on the queue`. The result line says Ready.
2. After **Review this delivery**, the result line says "The second delivery is on the work queue. Work-queue count is 197. Packaged replay count is 67." This delivery changes to `on the work queue`. Read the sentence, the answer source, and the cited item ids under that line.
3. After RT-01 clicks **Drop this duplicate**, the result line says "Refused. Confirm drop waits for RT-05. The current role is RT-01." This delivery stays `on the work queue`.
4. After RT-05 clicks **Drop this duplicate**, the result line says "RT-05 dropped the duplicate. The work-queue count returned to the start value. Work-queue count is 196. Packaged replay count is 67." This delivery changes to `dropped`.

## 2. Recipe

### Who is in this moment

TSMC is etching wafer lot `L00000016` for the NVIDIA Blackwell B200. The lot is on etch tool `T0000013` in the TSMC fab. Dispatch is the system that names the recipe for the lot. The tool keeps its own recipe row.

ASML supplies the EUV scanners in this same fab. The etch tool in this story is a separate tool. The clock story below is the one that uses an ASML scanner.

### The notice

Say this sentence while the Recipe tab is open:

"RECIPE_CHANGE. NVIDIA Blackwell B200 lot L00000016. Etch. Dispatch recipe R02. Tool recipe R01. Change ECN0000001 effective 2023-01-01T07:00."

That sentence is the spoken notice. The page prints the lot, the tool, both recipes, and the change.

### What the person does

The lot started at `2023-01-05T16:00` with dispatch recipe `R02`. The tool row still says `R01` and has no effective date. Change `ECN0000001` was approved to move the etch recipe from `R01` to `R02`, effective `2023-01-01T07:00`. That effective time is four days before the lot started.

RT-01 clicks **Explain this mismatch**. The result sentence names both recipes, change `ECN0000001`, the effective time, the lot start, and the missing tool date. The cited items include `rule.recipe.mismatch_show_both`. Hold stays `not recorded`. The model drafts the sentence. RT-03 records the hold.

Sign in as reviewer.tw and click **Hold**. The page refuses that role. Sign in as engineer.az within five minutes of the one-time code and click **Hold**. Confirm the signature. The draft author stays `model_draft`. The page records the hold for case `PS000000016`.

Do the clicks on Application A. Application B has the same two buttons and the same evidence rows.

### What the screen still shows

1. After **Start this shift again**, the situation sentence is "Lot L00000016 on tool T0000013 shows dispatch recipe R02 and tool recipe R01." Dispatch is `R02` at `2023-01-05T16:00`. Tool recipe is `R01` on `T0000013`, with effective date none. Change is `ECN0000001` effective `2023-01-01T07:00` APPROVED. Hold is `not recorded`.
2. After **Explain this mismatch**, the result line says "The mismatch is explained." The sentence says dispatch recipe `R02` and tool recipe `R01` disagree. It names change `ECN0000001`, effective `2023-01-01T07:00`, and the lot start `2023-01-05T16:00`. It says the tool row still says `R01` and has no effective date. Read the answer source from the screen. Hold stays `not recorded`.
3. After RT-01 clicks **Hold**, the result line says "Refused. Hold waits for RT-03. The current role is RT-01." Hold stays `not recorded`.
4. After engineer.az clicks **Hold**, the result line says "Hold recorded by engineer.az." Hold changes to `recorded by engineer.az`.

On Application B, the Audit band also shows "Phase 10 chain corr-p10b-doc-20261018-001." That id is the earlier chain. It is already on the page.

## 3. Clocks

### Who is in this moment

An ASML EUV scanner in the TSMC fab raises an alarm while a NVIDIA Blackwell B200 wafer layer is in process. The scanner records one time when the alarm happens. The console records a second time when the message arrives. Those two times fall on different dates.

### The notice

Say this sentence while the Clocks tab is open:

"TOOL alarm E-00000000. ASML EUV scanner. Event time 2020-12-30. Arrival time 2021-01-01. NVIDIA Blackwell B200 layer in process."

That sentence is the spoken notice. The page prints event `E-00000000` and the two times in two cells.

### What the person does

Event `E-00000000` happened on `2020-12-30`. The message arrived on `2021-01-01`. The metrology samples for this case have no clock, so they stay off this line.

RT-01 clicks **Place this event on the timeline**. The event time becomes `2020-12-30`. The arrival time stays `2021-01-01`.

Do this story on Application A. Application B has the same tab.

### What the screen still shows

1. After **Start this shift again**, the situation sentence is "Evidence E-00000000 has an event time and a later arrival time." Event is `E-00000000`. Event time is `not applied`. Arrival time is `2021-01-01`. Metrology is "Metrology samples have no clock."
2. After **Place this event on the timeline**, the result line says "Event E-00000000 is on the timeline at 2020-12-30. Arrival time 2021-01-01 stays a second mark." Event time changes to `2020-12-30`. Arrival time stays `2021-01-01`. Metrology stays "Metrology samples have no clock."

## 4. Policy

### Who is in this moment

On `2024-06-01`, TSMC fab `FAB-00000002` is running NVIDIA Blackwell B200 wafers. Several US policy windows cover that same date. The stored rows have an id, a start date, and an end date. A row with no end date prints the word open. The rows do not store a title.

### The notice

Say this sentence while the Policy tab is open:

"Fab FAB-00000002, 2024-06-01, NVIDIA Blackwell B200 wafers. Four US policy windows are in force. The page lists the four ids and waits."

That sentence is the spoken notice. The page prints the policy ids and the dates. It does not print a policy title.

### What the person does

Four windows are in force on `2024-06-01`:

- `POL-0002` from `2023-01-01` to open
- `POL-0010` from `2021-01-01` to open
- `POL-0018` from `2024-01-01` to `2024-12-31`
- `POL-0026` from `2022-01-01` to open

`POL-0034` starts on `2025-01-01`. The table leaves it out.

Sign in as reviewer.tw and click **Ask which policy applies**. The page lists the four and waits for RT-04. reviewer.tw clicks **Record my decision**. The page refuses that role. Sign in as policy.owner and click **Record my decision**. The recorded choice is `keep-wait`. The case stays waiting. The four policy ids stay on the page.

Do this story on Application A. Application B has the same tab.

### What the screen still shows

1. After **Start this shift again**, the situation sentence is "Fab FAB-00000002 has overlapping US policies on 2024-06-01." The table lists `POL-0002`, `POL-0010`, `POL-0018`, and `POL-0026` with the dates above. The count row says "In force on 2024-06-01" and the value is 4. Recorded choice is `none`.
2. After **Ask which policy applies**, the result line says "Four policies are in force. The app abstains and waits for RT-04." Recorded choice stays `none`.
3. After RT-01 clicks **Record my decision**, the result line says "Refused. A policy decision waits for RT-04. The current role is RT-01." Recorded choice stays `none`.
4. After RT-04 clicks **Record my decision**, the result line says "RT-04 recorded keep-wait." Recorded choice changes to `keep-wait`.

## 5. Outage

### Who is in this moment

The console reads partner messages through the source gateway on port 8090. During this shift the link to that gateway times out. A Micron message about HBM3E for the NVIDIA Blackwell B200 then arrives with a field the intake rejects. Incident `INC-2025-014` is the follow-up for this break. The packaged incident has no owner until RT-06 types one.

### The notice

Say this sentence while the Outage tab is open:

"YIELD_EXCURSION. Micron HBM3E lot for NVIDIA Blackwell B200. Field missing. Intake DLQ-DEMO-BAD."

That sentence is the spoken notice. The page prints the probe results, the parked id, and the owner cell.

### What the person does

RT-01 clicks **Check the upstream link**. The probe times out. The attempt count is 2. The probe target is port 8090.

RT-01 clicks **Check the message shape**. The shape does not match. The attempt count is 1. That probe is not retried.

RT-01 clicks **Set this intake aside**. Intake `DLQ-DEMO-BAD` is parked. RT-01 clicks **Bring the parked intake back**. The same row changes to `REPLAYED`.

The owner cell is still empty. Sign in as reviewer.tw and click **Record the owner** with an empty box. The page asks for an owner id. reviewer.tw types `shift-lead-demo` and clicks **Record the owner** again. The page refuses that role. Sign in as opslead and click **Record the owner**. The owner cell shows `shift-lead-demo`.

Do this story on Application A. Application B has the same tab.

### What the screen still shows

1. After **Start this shift again**, the situation sentence is "Incident INC-2025-014 has no follow-up owner." The owner cell says `empty`.
2. After **Check the upstream link**, the result line says "Upstream timed out. Attempt count is 2. The probe target is port 8090."
3. After **Check the message shape**, the result line says "Upstream schema did not match. Attempt count is 1. This probe is not retried."
4. After **Set this intake aside**, the result line says "Intake DLQ-DEMO-BAD is parked." The evidence table adds a row `DLQ-DEMO-BAD` with status `PARKED`.
5. After **Bring the parked intake back**, the result line says "Intake DLQ-DEMO-BAD is back. Status is REPLAYED." The same row now says `REPLAYED`.
6. With an empty Owner box, **Record the owner** says "Failed. Type an owner id, then record it." The owner cell stays `empty`.
7. With `shift-lead-demo` typed and the role still RT-01, the result line says "Refused. The owner of INC-2025-014 stays empty unless RT-06 types one. The current role is RT-01." The owner cell stays `empty`.
8. After RT-06 clicks **Record the owner**, the result line says "Owner shift-lead-demo is recorded for INC-2025-014." The owner cell shows `shift-lead-demo`.

## 6. Rule trace

### Who is in this moment

A reviewer asks where the etch-recipe rule for the NVIDIA Blackwell B200 lot came from. The rule was assembled from earlier work. Application A tells the reviewer to open Application B. Application A answers its own page. Application B answers its own page.

### The notice

Say this sentence while the Rule trace tab is open on Application B:

"The etch-recipe rule for the NVIDIA Blackwell B200 lot is the five items on this page, in this order."

That sentence is the spoken notice. The page prints the five item ids.

### What the person does

On Application A, open the Rule trace tab. The page has no **Show where this rule came from** button.

On Application B, RT-01 opens the Rule trace tab and clicks **Show where this rule came from**. The page lists five items. The click reads that list. The B200 lot, the hold, and the queue count stay as they were.

### What the screen still shows

1. On Application A, the page says "Application A has no lineage route. Open Application B for this trace." The actions band says "Open Application B for the rule trace."
2. On Application B, the situation sentence is "This page shows where the recipe rule came from." The list is: 1 historical decision `decision.bp4.four_programs`. 2 earlier code `code.legacy_policy.js_allow`. 3 specification `data.contract.decision_policies_archive`. 4 test `test.rule.recipe_release.emea_2023`. 5 transformed implementation `code.transformed.evaluate_live_policy`. The result line says "The ordered list above is the path for this rule."
