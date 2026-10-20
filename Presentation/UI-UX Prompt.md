

Apply the below UI-UX treatment to the application to align with BIRLASOFT branding.

### Screen anatomy

**Page frame.** The page background is light gray `#F2F2F2`. A solid red bar, `#ED1C24`, 16px wide, runs the full height of the viewport along the left edge. Content starts to the right of that bar. This is the same left bar the July 2026 cover uses.

**Header.** White bar on the light gray page. Charcoal text. From left to right: logo clear-space, application name, location, role picker, actor id, runtime mode. Quiet text actions only (session reset), in `#666666`. The header is white so the logo sits on the approved white background.

On the right side of the header, draw the cover motif once: two open arcs, no fill. The outer arc is an 8px stroke of `#ED1C24`. The inner arc is a 2px stroke of `#231F20`. They sit in the empty right side of the header. No label, control, or logo crosses either stroke. Do not repeat the arcs inside the work sheet.

**Logo.** Use the official master artwork file when it is in the repo. Clear space on all four sides equals the height of the “b” in that artwork. Minimum width is 20 mm (76px at 96 dpi). The parent lock-up, Birlasoft with CKA Birla Group, is 25 mm minimum and appears only when the brief asks for the parent group, in the prescribed size, color, and placement. Keep the logo off the page edge and off the red bar. If a photo or diagram is behind that corner, put a white band behind the logo first.

If the master file is not in the repo, leave the clear-space box empty and set the word Birlasoft in Calibri, charcoal, semibold. That word is a text label. The logo appears only when the master artwork file is in the repo.

**Tab strip.** Directly under the header, on the canvas, one row, about 40px tall. Tabs do not wrap. A narrow window scrolls the strip sideways.

- The strip is `role="tablist"`. Each tab is `role="tab"` with `aria-selected`. The open tab also has `aria-current="page"`.
- An inactive tab has no box and no fill. Text is `#666666`, 14px, weight 400, Calibri.
- The open tab uses the white sheet, weight 600, charcoal text, and a 3px top line in `#ED1C24`. Its bottom edge meets the sheet so the tab and the page are one surface.

**Work sheet.** One white surface directly under the open tab. One border, `#E0E0E0`. No gap between the tab and the first band. A soft shadow separates the sheet from the light gray page. Inside the sheet, in this order:

1. Situation. The one-sentence page title.
2. Evidence. The table for this object only.
3. Actions. The primary action, then any decision that follows it. A short role line under each restricted action.
4. Result. Latest-action line, then explanation lines only when filled.
5. Audit. Only when filled.

**Below the sheet.** Secondary checks, muted `#666666`, smaller type, no red fill.

### Visual system

Use the Birlasoft palette on every page and every defense slide. Red is emphasis. Charcoal is text and lines. White and light gray are backgrounds. Purple and gold are small accents. The guide allows tints of these colors. It does not allow a new hue.

| Token | Value | Use |
|---|---|---|
| Red | `#ED1C24` | Left page bar, open-tab mark, primary button, short emphasis label |
| Charcoal | `#231F20` | Titles, body text, table text, lines, refusal bar |
| Purple | `#72007D` | A small secondary mark only, such as a section index. Never a page fill, a status band, or a primary button |
| Gold | `#EFBC4A` | 4px left bar on the in-flight and success line |
| White | `#FFFFFF` | Header, work sheet, table body, logo background |
| Light gray | `#F2F2F2` | Page around the sheet |
| Red tint | `#FDEBEC` | Pill behind one short label, such as the runtime mode. The guide uses this tint on its cover |
| Gold tint | `#FCF3DE` | Background of the in-flight and success line. This is `#EFBC4A` at 18% on white |
| Secondary text | `#666666` | Tab second lines, role hints, secondary checks. The guide’s own slides use this gray for supporting lines |
| Hairline | `#E0E0E0` | The one border around the sheet, and card borders on the deck |
| Primary text | `#FFFFFF` | Text on the red primary button |
| Refusal | White background, `#231F20` left bar, `#231F20` text | Refusal and failure. The sentence starts with Refused or Failed |

Worked example. The page around the sheet is light gray `#F2F2F2`. The sheet is white. The open tab has a 3px red top line. The one primary button is red with white text, 16px Calibri semibold. After a successful click, the latest-action line is gold tint `#FCF3DE` with a gold left bar, and the sentence names the new status. After a refusal, the line stays white with a charcoal left bar, and the sentence starts with Refused. Purple does not appear on that line.

Also require:

- Calibri for every run of text on the console and the deck. Headings are bold or semibold. Body is regular. Set size, weight, and spacing before you add another color. If Calibri is missing, stop the visual pass and say so. The face stays Calibri.
- A type scale. The situation title is 24px bold charcoal. Body is 16px regular charcoal. Labels are 13px `#666666`. Button text on red is at least 16px semibold, because white on `#ED1C24` needs that size to stay readable.
- Charcoal text on the white sheet. Charcoal text on the white header. The refusal treatment stays on the same white page.
- Spacing that makes the five bands readable as one task. The evidence table is sized for the real values (timestamps, revisions, dates, counts).
- Exactly one primary button on the open page: filled `#ED1C24`, white text. Other actions are quieter: charcoal text, white fill, hairline border. Destructive or restricted actions are not given the red fill unless they are the page’s main job.
- Status color is meaningful. Red marks the selected tab and the primary action. Gold marks the latest action while it is moving and after it succeeds. A refusal uses a charcoal bar, and the sentence starts with Refused or Failed. The sentence states the outcome. Color is a second signal beside that sentence.
- No full paragraph in all caps. No compressed letter spacing. No decorative font.
- No gradient fill, no glow, and no logo inside a circle, a rounded badge, or any other shape.




### Accessibility and craft

- Use real buttons for actions and tabs with the roles above. The open page is programmatically indicated.
- Keyboard users can move across the tab strip and activate the open page’s primary action.
- Text meets contrast on light gray, white, the red button, the gold tint, and the refusal line. White on `#ED1C24` is the primary-button pair, at 16px semibold or larger. Charcoal on white is the body pair.
- The layout holds at a narrow width: the tab strip scrolls, the sheet stacks, the table remains readable, and the red left bar stays 16px.
- Focus states are visible. Do not rely on color alone.

### Build order

1. Write the screen contract: header contents, tab names and second lines, sheet bands, primary action per page, role lines, latest-action versus explanation, conditional audit, Birlasoft tokens, logo rule, and the tab-change and late-response rules.
2. Implement the shell and one work area to that contract.
3. Apply the same shell to every work area and every sibling application.
4. Add tests that read the source for the contract: header fields, tab semantics, open-tab class, the hex values in the table above, primary-button class, role lines, conditional explanation and audit, and the clear-on-switch function. Keep existing action names stable once the contract records them.
5. Rebuild the served bundle. A source save is not the running page when the UI is built into an image or a static bundle.
6. Verify in the browser, on the running application, not only in unit output.