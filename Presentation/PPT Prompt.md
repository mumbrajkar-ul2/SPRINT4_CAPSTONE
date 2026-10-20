You are creating the presentation defense for the modernization of Fabpulse Group’s flawed legacy Fab-lot and Equipment-exception Management System. In the Legacy system - external messages, process and metrology records, policy versions, case workflows, archived documents, cost estimates, and local rule interpretations do not always agree. The modernized system improves operational decision quality, traceability, reconciliation, engineering velocity, resilience, and user experience without disguising uncertainty or using GenAI where deterministic engineering is safer.

The PowerPoint presentation should adhere to the @docs/demo/placeholder-deck.md . In a separate "Demo" section - add slides to cover the @docs/42-executive/demo-day-script.md as well, just in case those elements are not already covered in the main deck defined by @docs/demo/placeholder-deck.md .

The audience is a critical reviewer who will judge whether the product is understandable, elegant, and complete. The deck itself must meet that bar. A default Office theme, a wall of bullets, or a script the presenter has to read aloud is a failed delivery. A deck that still uses the retired operations palette (slate header, teal accent, amber rule, Aptos) is a failed delivery.

Build a real `.pptx` file, 16:9, that a presenter can open and deliver. Also write a one-page run of show beside it. Take the facts from the built application, its screen contract, and the enterprise UI prompt. Use the real work-area names, object ids, button labels, roles, and outcome sentences. Do not invent a scenario, a metric, a customer logo, or a claim the screen cannot show.

### The bar

The room should grasp the product in one sitting.

- **Intuitive.** Each slide makes one claim. The title is that claim, written as a sentence. A reviewer who reads only the titles can retell the defense. The presenter points at one thing per slide. The spoken story lives in speaker notes, not in paragraphs on the slide.
- **Elegant.** The deck uses the July 2026 Birlasoft system: white field, Calibri, the six approved colors, the cover’s red bar and two arcs, and the interior’s white cards. It looks like one Birlasoft briefing. It uses the same red for emphasis and the same gold for a result as a console built to `BSL Prompt for UI-UX.md`.
- **Complete.** The defense covers the operator journey from arrival through outcome, including refusal, success, role handoff, what stays hidden until it is relevant, and what the system of record does not change. Honest limits are in the main arc. The presenter never has to leave the story to explain a core step.

Target length for the main arc is 14 slides and 12 to 16 minutes of talking, plus a separate live demonstration in the application. Appendix slides exist only for questions. They are not part of the spoken arc.

### What to read before you draw a slide

Read, in this order:

1. This prompt, for the defense story and for color, type, the cover motif, and card chrome.
2. `Birlasoft_Branding_Guide_July_2026 (3).pptx`, if a measurement in this prompt is unclear. The cover is the motif. Slides 6 and 7 are the palette and the type. Slide 8 is the layout set.
3. The enterprise UI prompt, and treat its journey, state model, and failure patterns as the product source of truth. If `BSL Prompt for UI-UX.md` is the prompt the console was built from, the console’s red, charcoal, gold, and Calibri should match this deck.
4. The screen contract and the running console, or the latest screenshots if the stack is down.
5. The actual primary actions, role lines, evidence columns, and result sentences.

If a screenshot is missing, draw a faithful frame of that region using the real labels, and caption it “Structure of the console.” Do not present a diagram as a photograph of the running page.

### Narrative

The defense answers five questions, in this order. Open with the operator’s job. Leave architecture, a technology list, and a feature inventory out of the opening.

1. What job is the operator in the middle of?
2. What does the console let that person see and do without leaving the page?
3. What changes on screen when the action is refused, and when it succeeds?
4. What is deliberately kept off the page until it is true?
5. What will you not claim?

Speak in the language of the job. Button names on the slides are the business actions. Route names, container commands, and raw payloads stay out of the main arc.

### Slide contract

Build exactly these 14 slides in this order. Use the layouts named in parentheses. Replace the example wording with the product’s real objects. Keep the job of each slide.

| # | Layout | Claim the title must make | On the slide | In the notes |
|---|---|---|---|---|
| 1 | Cover | The product, named as the operator’s console | Product name. One sentence: who uses it and what decision it supports. Audience and occasion in the footer line. | 20 seconds. Say the one sentence. Leave the agenda list out of the opening. |
| 2 | Three tests | What this room is here to judge | Three tests, in a row: a person can complete the job on screen; every click changes something visible; the page never claims a result it did not produce. | 40 seconds. These three tests are the definition of done. |
| 3 | Split | One concrete case, told as work | Left: the business object and the conflict in two lines. Right: what a wrong outcome would cost the operation, in one sentence, with no invented dollar figure. | 50 seconds. Tell it as a shift, not as a user story template. |
| 4 | Anatomy | The page is one surface with one job | A single diagram of the console: header, tab, sheet. Label only Situation, Evidence, Action, Result. Mark the one primary action. | 60 seconds. Point in the same order the operator reads. |
| 5 | Path | The operator never leaves the application | Five beats on one line: Arrive, Read, Act, See, Hand off. Under each beat, the real control or sentence from the product. | 50 seconds. Say that logs and shells are for later proof, not for the act. |
| 6 | Screenshot | This case is already legible before the click | Crop of the open work area: situation sentence and evidence table. Three callouts: the object id, the two conflicting facts, the role allowed to finish. | 70 seconds. Read the situation sentence once. Then point. |
| 7 | Before / after | Success is a visible change, not a toast that disappears | Two evidence states side by side. Before: the status row at rest. After: the new status and the latest-action sentence. Include the count or field that moved, and the system-of-record value that stayed still. | 70 seconds. Name both numbers. |
| 8 | Split | Authority is on the page before the click | Left: the role line under the restricted action. Right: the refusal sentence naming the required role and the current role, then the success sentence after the authorized role acts. State the separation-of-duties rule in one line. | 70 seconds. A wrong role is part of the demonstration, not an error. |
| 9 | Table | Every work area is the same kind of page | One row per primary work area. Columns: object, what the person reads, primary action, who may decide, what changes. No route names. | 60 seconds. Touch two rows besides the signature case. Do not narrate all rows. |
| 10 | Four states | Every click answers in words | Four stacked bands: in flight, refused, succeeded, already done. One real sentence in each band. Under them, one line: explanation and audit appear only after a click that fills them. | 50 seconds. Say what the page refuses to print when those fields are empty. |
| 11 | Three columns | Three kinds of state stay distinct | View state clears on a tab change. Case session stays on that object. System of record is not written by the session. One example of each from the product. | 50 seconds. Include the late-response rule: a slow answer does not paint onto the next tab. |
| 12 | Honesty | The page says where the answer came from | Three labels the header or result can show: live model, saved reply, stored statement. Beneath, three claims this defense will not make. Use only limits that are true of this build. | 50 seconds. If a live call can fail, the spoken line says the business result and the model result are separate. |
| 13 | Run of show | The live path is seven moves or fewer | A numbered list the presenter can glance at: open, role, read, primary click, point at the result, switch role, decision click, switch tab and show a clean page. Each move names what to point at. | This slide stays up during the live application. Notes hold the fallback if the live call fails. |
| 14 | Statement | One sentence the room can repeat | White field with open space. The sentence. Under it, the three tests from slide 2, now as three short proofs taken from the demonstration. | 30 seconds. Stop. Do not add a technology slide. |

Appendix, after a section slide titled “If you want the mechanism.” Build these only from facts in the repo. Do not speak them unless asked.

- A. Sibling applications: same shell, and the one capability that exists on only one of them.
- B. Secondary checks: where they sit, and that they are not primary work areas.
- C. One sequence diagram of the signature action, from click to the sentence on screen. No secret values.

### Visual system

The July 2026 guide is the visual source. Its own theme part still carries default Office colors. Set every fill, line, and font color explicitly. Do not leave theme blue, teal, or amber in the file.

Widescreen 13.333 by 7.5 inches. That is the guide’s slide size.

**Color hierarchy.** Red is emphasis. Charcoal is text and lines. White and light gray are backgrounds. Purple and gold are small accents. The guide allows tints of these colors. A new hue is outside the system.

| Token | Hex | Use on the slide |
|---|---|---|
| Red | `#ED1C24` | Cover bar, first number in a sequence, short label in the red-tint pill, 0.08 inch emphasis bar on the first card |
| Charcoal | `#231F20` | Titles, body, table text, later numbers in a sequence, lines, refusal bar |
| Purple | `#72007D` | One 0.08 inch bar on a third card, or a section index. Never a page fill, a status band, or a large panel |
| Gold | `#EFBC4A` | 0.08 inch bar on an in-flight or success band. A thin accent only |
| White | `#FFFFFF` | Every slide field, including the cover and the close. Card fill. Logo background |
| Light gray | `#F2F2F2` | Alternate table rows, a quiet card, the note card on the cover |
| Red tint | `#FDEBEC` | Pill behind a short label on the cover. The hierarchy line on the guide’s palette slide uses this same fill |
| Gold tint | `#FCF3DE` | Background of an in-flight or success band. This is `#EFBC4A` at about 18% on white |
| Secondary text | `#666666` | Supporting line under a title, captions, cover footer |
| Card body | `#4B4B4B` | The second line inside a card, when that line is support and the title is charcoal |
| Slide number | `#777777` | The number at the lower right |
| Hairline | `#E0E0E0` | Card borders and table rules. The guide also uses `#E4E4E4` and `#DCDCDC` for card borders. Pick one hairline per deck and keep it |
| Connector | `#D9D9D9` | The 2 pt line that joins numbers in a sequence |
| On red or on charcoal | `#FFFFFF` | Text on a red number circle, on a charcoal number circle, and on a charcoal table header |

Worked example. The cover field is white. A red bar 0.22 inches wide runs the full height of the left edge. The title is charcoal. After a refused click, the result band on a later slide stays white, with a charcoal left bar, and the sentence starts with Refused. After a success, that band is gold tint `#FCF3DE` with a gold left bar, and the sentence names the new status. Red stays on the cover bar and on emphasis marks. Red does not move onto the refusal band.

**Type.** Calibri for every run of text. Headings are bold or semibold. Body is regular. Set size, weight, and spacing before you add another color. The guide’s range is headings 24–60 pt and body 8–20 pt. This defense is spoken in a room, so use the large end of the body range. The branding guide sets its own subtitles at 11.5 pt because that deck is read on a laptop. Here, body is 16 pt and callouts are 14 pt. If Calibri is not installed, stop and say so. Do not swap in Aptos, Segoe UI, Calibri Light, or a decorative face.

| Role | Size | Weight | Color |
|---|---|---|---|
| Cover title | 38 pt | Bold | `#231F20` |
| Slide claim | 26 pt | Bold | `#231F20` |
| Statement sentence on the close | 28 pt | Bold | `#231F20` |
| Body | 16 pt | Regular | `#231F20` |
| Supporting line under a claim | 16 pt | Regular | `#666666` |
| Callout | 14 pt | Regular | `#231F20` |
| Card title | 15 pt | Bold | `#231F20` |
| Short label in the red-tint pill | 9 pt | Bold | `#ED1C24` |
| Footer and classification | 10 pt | Regular | `#666666` |
| Slide number | 10 pt | Regular | `#777777` |
| Table text | 13 pt | Regular | `#231F20` on white, white on the charcoal header row |

No full paragraph in all caps. No compressed letter spacing.

**Cover motif.** Only the title slide carries it. Content slides stay white and do not repeat the bar or the arcs.

- Field: white `#FFFFFF`, full bleed.
- Left bar: a rectangle from (0, 0) to (0.22, 7.5) inches, fill `#ED1C24`, no gap at the slide edge.
- Outer arc: preset arc, no fill, stroke 8 pt `#ED1C24` at 90% opacity. Box at (8.85, −0.40), 4.9 by 4.9 inches. Rotate 18 degrees clockwise. The box runs off the top and right edges.
- Inner arc: preset arc, no fill, stroke 2 pt `#231F20` at 65% opacity. Box at (9.55, 0.25), 4.4 by 4.4 inches. Same 18 degree rotation. No label, rule, or logo crosses either stroke.
- Both arcs use the DrawingML arc preset with an empty adjustment list, which is the cover in the July 2026 file.

**Interior chrome.** Content slides, the three-test slide, the close, and the appendix divider are white. They have no full-height red bar and no arcs. The claim sits at the left, at x = 0.55 inches. Supporting material sits in white rounded rectangles with a 1 px hairline. A 0.08 inch left bar on a card is the accent: red on the first card in a row, charcoal on the next, purple or gold only when that card is a secondary accent or a result. Gaps between cards are 0.18 inches. Cards in a row share one top edge and one height.

**Logo.** Use the official master artwork file when the brief gives a path and the file is in the repo. Clear space on all four sides equals the height of the “b” in that artwork. Minimum width is 20 mm (0.79 inches). The parent lock-up, Birlasoft with CKA Birla Group, is 25 mm minimum (0.98 inches) and appears only when the brief asks for the parent group, in the prescribed size, color, and placement. White is the logo background on this deck. Keep the logo off the slide edge, off the red bar, and off the arcs. If a screenshot would sit behind that corner, put a white band behind the logo first.

The July 2026 guide draws the word “birlasoft” inside boxes labeled “PLACEHOLDER — REPLACE WITH OFFICIAL ARTWORK.” Those boxes are instructions to the reader of the guide. On this defense, omit the logo when the master file is missing. Do not draw, trace, recolor, stretch, rotate, or typeset a wordmark in its place.

Place the logo on the cover only, on the white field, to the right of the red bar and clear of the arcs. Add it to the close only when the brief asks for it there.

**Footer.** On content slides, the product name sits at the left, 10 pt `#666666`, and the slide number sits at the right, 10 pt `#777777`, with the baseline at 7.18 inches. The guide’s own number box is at about (12.92, 7.18). No confidential banner, no file path, and no date on every slide. The cover carries the classification line: “Prepared for internal use” when the brief says the room is internal. When the brief says the room is external, use the classification the brief names, and leave the Marketing review note in the run-of-show file.

**Slide Master.** Put the cover bar, the two arcs, the Calibri styles, and the footer on the Slide Master and layouts. Duplicate that layout for each slide of a type. Manual copies drift.

### Layout recipes

Implement these as functions so every slide of a type matches. Positions are in inches from the top-left of the slide.

**Cover.** White field, red bar, and both arcs, as specified above. Red-tint pill at (0.85, 1.00), about 2.25 by 0.34, fill `#FDEBEC`. Inside it, a 9 pt bold `#ED1C24` label for the occasion, two to four words. Claim at (0.85, 1.62), width 7.2, 38 pt bold charcoal, two lines maximum. Supporting sentence at (0.90, 3.45), 18 pt regular `#666666`, width 6.8. Footer line at (0.90, 6.75): product, presenter, date, and the classification. The logo, when the master file is present, sits on this white field inside the clear-space rule, and it does not cross the arcs or the red bar.

**Three tests.** Claim at (0.55, 0.55), 26 pt bold, width 11.2. Three white cards in one row at y = 3.6, height 2.2, hairline border. Left bars, in order, red, charcoal, gold, each 0.08 inches wide. Each card: a number, then one line. The first number is white on a red circle. The other two numbers are white on charcoal circles. A `#D9D9D9` 2 pt line may join the circles. This is the same number treatment as the guide’s “How to use this guide” slide.

**Split.** Claim on the white field. Two equal white cards from y = 1.70 to y = 6.5. The left card has a red 0.08 inch bar. The right card has a charcoal 0.08 inch bar. Card title 15 pt bold. Body 16 pt. One sentence under the pair if the slide needs the separation-of-duties line, 14 pt `#666666`.

**Anatomy.** Claim on the white field. Under it, one rounded rectangle, white fill, hairline border, from (0.55, 1.60) to (12.70, 6.85). Inside it, draw the running console, not a second brand. When that console uses the Birlasoft shell, the frame has a red left edge, a white header, charcoal type, an open tab with a 3 px red top line, and one red button with white text and the real primary-button label. The two arcs appear in that frame only when the running header shows them. Evidence is a two-column miniature table. Result is a gold-tint band with one short sentence. If the running console still shows an older shell, draw that shell faithfully and keep the deck chrome on the Birlasoft system. Caption a drawn frame “Structure of the console.”

**Path.** Five equal cards in one row at y = 2.2, height 3.6. Each card: a 0.62 inch circle, the beat name at 16 pt bold, and two lines naming the real control. The first circle is `#ED1C24` with a white numeral. The other circles are `#231F20` with white numerals. A `#D9D9D9` 2 pt line connects the circles. No chevrons and no SmartArt.

**Screenshot.** Frame at (0.55, 1.60), about 7.6 by 5.1, white fill, 1 px hairline. The image fills the frame with an even crop. Do not stretch. To the right, at x = 8.40, three callouts. Each callout is a charcoal numeral and two lines. If there is no image, the frame holds the anatomy of that single region and the caption “Structure of the console.”

**Before / after.** Two cards, equal width, from y = 1.60 to y = 6.6. Left eyebrow “Before.” Right eyebrow “After.” Each card contains the same three evidence rows so the eye can compare. The changed row on the right uses the gold tint and a gold left bar. Under each card, the latest-action sentence for that moment, 14 pt.

**Four states.** Four full-width bands stacked from y = 1.70, each 1.05 tall, gap 0.12. In flight and succeeded use the gold tint and a gold left bar, with charcoal text. Refused uses a white fill, a charcoal left bar, and a sentence that starts with Refused or Failed. Already done uses a white fill, a `#666666` left bar, and charcoal text. The band’s first word is the state name in bold. The rest of the band is the real sentence, 16 pt, one line.

**Table.** Header row `#231F20`, white text, 0.42 tall. Body rows 0.46 tall, alternating white and `#F2F2F2`. No vertical rules. A hairline under each row. First column is the work-area name in bold. At most six columns. If a cell needs more than six words, the column is the wrong column.

**Three columns.** Three equal white cards. Left bars in order: red, charcoal, purple. Each has an eyebrow (View, Session, Record), a one-line definition, and one real example in charcoal. Purple is only that third bar.

**Honesty.** Three short labels as red-tint pills with `#ED1C24` bold text: live model, saved reply, stored statement. Use only the labels this build can show. Under them, three white cards with charcoal left bars for the three claims this defense will not make.

**Run of show.** Numbered rows, not bullets. Each number sits in a white circle about 0.44 inches wide with a 1.4 pt `#ED1C24` stroke and a charcoal numeral, so every move is equally visible while the presenter looks at the live application. The move is 16 pt bold. The “point at” phrase is 13 pt `#666666` on the same row, right-aligned.

**Statement (close).** White field. No arcs and no red bar. The repeatable sentence at (0.55, 2.00), 28 pt bold, width 11, three lines maximum. Leave open white space around it. Three proof cards in a row at y = 5.10, same construction as the three tests on slide 2. Contact and website appear only when the brief supplies an approved line.

**Appendix divider.** White field. A red-tint pill with the words “If you want the mechanism.” One charcoal sentence under it. Then the appendix slides, using the same content layout.

### How much text is allowed

Count the words on the slide, not in the notes.

- A claim title is at most 14 words and at most two lines.
- A light content slide holds at most 45 words outside the title, unless it is the work-area table or the run of show.
- A card holds at most 18 words.
- Bullets are a last resort. Use them only for parallel facts of the same kind. Maximum four. No sub-bullets.
- No paragraphs. No “Click to add text.” No “Overview,” “Agenda,” “Thank you,” or “Questions?” as a title. The guide has a thank-you layout for a simple close. This defense uses the statement slide instead, and the title is the sentence the room can repeat.
- The footer is the product name and the slide number. The cover holds the date and the classification. Those do not repeat on every slide.

### Speaker notes

Every slide has notes. Write them as something a person can say.

- Open with the sentence to speak first.
- Then “Point at” and the one element.
- Then the turn to the next slide.
- 40 to 75 seconds for slides 3 through 12. Slides 1, 2, and 14 are shorter, as specified.
- Notes add the reason and the transition. They do not restate the card text.
- Include one sentence the presenter says if a reviewer looks puzzled. That sentence uses the business object, not the component name.
- On slide 13, notes include a fallback: if the live model call fails, say the business result that did change, read the failure sentence on screen, and continue to the role decision. Do not switch to a terminal.

### Pictures, icons, and motion

- Screenshots are cropped to the relevant band, at least 1600 px wide in the source image, framed, and never distorted. Dim nothing. Do not add a device mock or a drop shadow stack.
- Callouts are numbers and words. Do not cover the evidence with arrows that hide the values.
- Icons, if used, come from an approved Birlasoft icon file that is actually in the repo. One stroke weight and one color treatment on a slide. If no approved icon file is in the repo, use type and the 0.08 inch bars, and omit icons.
- No clip art, no 3D, no stock photography, no people, no handshakes.
- No SmartArt, no WordArt, no gradient fills, no glow, no reflection, and no logo inside a circle, a rounded badge, or any other shape.
- No slide transitions. No animation, except a simple appear on the before/after pair if the host can click once to reveal “After.” The deck must still make sense when that animation is off.
- Charts appear only when two real numbers must be compared. One series, charcoal or red, no chart junk, no legend if the bars are labeled. A chart uses a token from the table above.

### Build the file

1. Confirm the 14 claims against the real product. If a claim is not true of the build, change the claim. Do not soften it into a feature list.
2. Create the `.pptx` with explicit colors and the layouts above. Set the slide size to 13.333 by 7.5 inches. Put the cover motif and the footer on the Slide Master.
3. Write speaker notes on every slide, including the appendix.
4. Write a run of show as a separate markdown file: minute marks for the 14 slides, the live clicks, the fallback line, and the three appendix slides marked “only if asked.”
5. Export a check pass over the file:
   - Slide count in the main arc is 14.
   - Every title is a claim.
   - The cover has the 0.22 inch `#ED1C24` bar and both arcs at the positions above. Content slides do not.
   - Theme colors are the tokens above. Search the file for `#143044`, `#0E7C66`, `#C9842A`, `#E8EEF2`, `#1C2833`, `#5B9BD5`, Aptos, and Segoe UI. None of those should remain.
   - Every run of text is Calibri.
   - No slide exceeds the word caps except the table and the run of show.
   - Screenshot frames keep their aspect ratio.
   - The honesty slide’s limits match the build.
   - The logo is the official master file, or the logo is absent. The placeholder word “birlasoft” is not on the slide.
6. Open the deck and read only the titles, in order. If they do not tell the defense, rewrite the titles before you deliver the file.

Suggested file names: `defense-deck.pptx` and `defense-run-of-show.md`, in the folder the user names.

### Patterns that fail this standard

Reject the deck if any of these are true.

- The theme is still the default Office theme, or the slides use the retired operations palette: slate `#143044`, teal `#0E7C66`, amber `#C9842A`, or Aptos.
- The cover is a dark full-bleed field, or the two arcs are missing, or the arcs are repeated on content slides.
- A slide title is a topic label such as “Architecture,” “Demo,” “Features,” or “Results.”
- The presenter must read the slide for the audience to understand it.
- The opening is a technology stack, a phase history, or a list of APIs.
- A core step of the operator journey is shown as a command, a SQL query, or a JSON dump.
- Success, refusal, and an unchanged system of record are not all visible.
- The deck claims a live model, an audit row, or a durable write the application does not show.
- Work areas are presented as unrelated screens, or sibling applications look accidentally different.
- Empty-state copy from the product is quoted as if it were a result.
- The logo is redrawn, stretched, rotated, recolored, enclosed in a shape, or set in type because the master file was missing.
- Purple or gold fills a region larger than a bar, a number circle, or the gold-tint result band.
- A hue outside the token table appears. The guide’s palette slide is the list. A green “approved” label is not part of this deck.
- Corporate statistics, awards, or service claims appear without a named approved source.
- The spoken arc is longer than 16 minutes before the live application, or the live path is more than seven moves.

### How to attach the brief

After this prompt, add only:

- Application name and the folder or URL of the running console.
- Presenter name and the date of the defense.
- Time box, if it differs from 12 to 16 minutes plus the live path.
- Path to screenshots, if they already exist.
- Path to the official master logo file, if it is in the repo. If it is missing, the cover omits the logo.
- Whether the parent lock-up with CKA Birla Group is required.
- Whether the room is internal or external, and any approved contact line for the close.
- Any claim the defense must not make, beyond the limits already in the build.