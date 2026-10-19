# Rule card design

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | FD-08; BO-05; BO-06a; BO-06b PROPOSED; BO-07; BO-08 PROPOSED; the archive JSON; the four rule files; catalogue BP1 to BP7; `mapping-design.md` |
| Assumptions | One card per business rule. Observed implementations sit on the card. They do not replace the canonical `decision_table`. Half B writes YAML cards that match this list. A small evaluator in Half B runs the `tests` list. Application A and Application B must pass the canonical tests. Deviation tests lock the recorded disagreement. |
| Unresolved issues | BO-06b and BO-08 stay unsigned. Cards RC-10 and RC-14 keep `authority: unresolved`. Aged-backlog cutoff stays Unknown. No card invents that cutoff. |
| Residual risks | Copying the JavaScript 1.05 line into the canonical table would make the deviation the rule. Marking 50,000 as decided would sign BO-08 in code. |

This file lists every rule card Half B must write. Each card has an `authority` label and the test cases that lock it.

Canonical numbers come from `contracts/decision-policies-archive.json` and `policy_register`. Where that source is silent, overlapping, or self-contradictory, the card expects `HOLD_FOR_REVIEW`.

---

## Finding

**Finding.** Twenty-five cards cover the governed archive, the four deviations, open and closed, site mapping, clocks, replay, untrusted text, and the unsigned rows.
**Evidence.** 15 archive versions. Four source files. BO-06a, BO-07. Catalogue counts.
**Impact.** Half B can write cards without inventing a threshold. Application B later evaluates the same tests.
**Risk.** A missing `no_match` row would let 999,999 leak in as a default.
**Confidence.** High on the card list. Unknown on evaluator line count until Half B.
**Open questions.** Signer of BO-06b and BO-08. Aged-backlog age in days.

---

## Card shape Half B must use

| Field | Required |
|---|---|
| `id` | yes |
| `kind` | `business_rule` |
| `statement` | yes |
| `inputs` | list of `{ name, term }` |
| `decision_table` | rows of `{ when, then }` |
| `authority` | `policy_archive`, `sme`, or `unresolved` |
| `owner` | role or `unknown` |
| `policy_status` | `decided`, `proposed`, `n/a` |
| `tests` | list of `{ given, expect }` |
| `observed_implementations` | list, may be empty |
| source, claim, trust, lake_version, item_status, honesty | as in `knowledge-model.md` |

`then.route` is one of `ALLOW`, `DENY`, `URGENT`, `QUEUE`, `ARCHIVE`, `HOLD_FOR_REVIEW`, `BLOCK`, `OPEN`, `CLOSED_OPERATIONAL`.

---

## Archive `recipe_release` cards

### RC-01 Canonical `recipe_release` limit

| Field | Value |
|---|---|
| id | `rule.recipe_release.limit` |
| authority | `policy_archive` |
| policy_status | `decided` |
| owner | Policy Owner (RT-04). Company title Unknown. |

`decision_table`: one row per archive version. 15 rows. Inputs: `amount`, `sales_region`, `on_date`. Then: `{ limit, currency: USD, within_limit: amount <= limit }`.

Child items: one accepted item per version, for example `rule.recipe_release.limit.v2023.emea`.

Tests (canonical; Half B may add the remaining 12 year-region pairs the same way):

| given | expect |
|---|---|
| amount 18000, sales_region EMEA, on_date 2023-07-01 | within_limit true, limit 18600 |
| amount 19000, sales_region EMEA, on_date 2023-07-01 | within_limit false, limit 18600 |
| amount 25000, sales_region APAC, on_date 2026-06-01 | within_limit true, limit 25000 |
| amount 25001, sales_region APAC, on_date 2026-06-01 | within_limit false, limit 25000 |
| amount 27200, sales_region AMER, on_date 2026-06-01 | within_limit true, limit 27200 |

Honesty on those limits: REAL from the archive file.

### RC-02 No matching archive row

| Field | Value |
|---|---|
| id | `rule.recipe_release.no_match` |
| authority | `policy_archive` |
| policy_status | `decided` |

When no archive row matches the derived sales region and date, `then.route` is `HOLD_FOR_REVIEW`. Do not use 999,999.

| given | expect |
|---|---|
| amount 100, country IN without going through site, on_date 2026-01-01, and no derived sales region supplied | route HOLD_FOR_REVIEW |
| amount 100, sales_region APAC, on_date 2021-06-01 | route HOLD_FOR_REVIEW |

Country IN is not an archive region. Site IN-BLR derives APAC. The no-match card is for a lookup that still has no archive row after derivation, or for a date outside 2022-2026.

### RC-03 Overlap or invalid interval

| Field | Value |
|---|---|
| id | `rule.policy.overlap_or_invalid` |
| authority | `policy_archive` |
| policy_status | `decided` |

When two active `policy_register` rows match one country on `on_date`, or when `valid_from` is after `valid_to`, route `HOLD_FOR_REVIEW`.

| given | expect |
|---|---|
| country US, on_date 2026-06-01, family FAB-RULE (all active US rows) | route HOLD_FOR_REVIEW |
| policy_id POL-0039 | route HOLD_FOR_REVIEW |

US has 5 active register rows. Honesty: REAL. POL-0039 has from 2025-01-01 and to 2024-12-31. Honesty: REAL.

---

## Deviation cards (parity tests)

These cards record what the local program does. They do not replace RC-01.

### RC-04 JavaScript 1.05 allow

| Field | Value |
|---|---|
| id | `rule.recipe_release.limit.impl.js` |
| authority | `unresolved` |
| policy_status | `n/a` |

Observed: `Number(amount) <= threshold(region,year)*1.05`. Lines 4-5 of `legacy_js/legacy_policy.js`.

| given | expect on this implementation | expect on RC-01 |
|---|---|---|
| amount 15700, region APAC, year 2022 | within_limit true (limit 15000 times 1.05 = 15750) | within_limit false |
| amount 27000, region APAC, year 2026 | within_limit false (25000 times 1.05 = 26250) | within_limit false |

### RC-05 JavaScript 999,999 default

| Field | Value |
|---|---|
| id | `rule.recipe_release.limit.impl.js_default` |
| authority | `unresolved` |
| policy_status | `n/a` |

Observed: missing year or region returns 999999. Never copy that number into RC-01.

| given | expect on this implementation | expect on RC-02 |
|---|---|---|
| amount 100, region IN, year 2026 | within_limit true | HOLD_FOR_REVIEW |

### RC-06 Python 50,000 urgent cutoff

| Field | Value |
|---|---|
| id | `rule.urgent.amount.impl.python` |
| authority | `unresolved` |
| policy_status | `proposed` |

Observed: `amount > 50000` returns urgent. Archive is silent on this cutoff. BO-08: demo may use 50,000 marked PROPOSED. Never 999,999. Canonical route when a number is required and the archive is silent: `HOLD_FOR_REVIEW`.

| given | expect on this implementation | expect canonical |
|---|---|---|
| status OPEN, severity LOW, amount 50001 | urgent | HOLD_FOR_REVIEW as live policy; demo may show 50,000 labelled PROPOSED |
| status OPEN, severity LOW, amount 49999 | queue (if other branches miss) | HOLD_FOR_REVIEW as live policy for the cutoff itself |

Packaged `SELECT COUNT(*) FROM cases WHERE amount > 50000` returned 0. Honesty: REAL. The two urgent packaged cases come from CRITICAL severity (RC-08).

### RC-07 Python CLOSED to archive

| Field | Value |
|---|---|
| id | `rule.priority.closed.impl.python` |
| authority | `unresolved` |
| policy_status | `n/a` |

Observed: `status=='CLOSED'` returns `archive`. SME closed needs a final disposition and no pending engineering action. A Python CLOSED word is not enough.

| given | expect on this implementation | expect on RC-09 |
|---|---|---|
| status CLOSED, no engineering-action field | archive | HOLD_FOR_REVIEW for operational-closed confirmation |

### RC-08 Python CRITICAL to urgent

| Field | Value |
|---|---|
| id | `rule.urgent.severity.impl.python` |
| authority | `unresolved` |
| policy_status | `n/a` |

Observed: `severity=='CRITICAL'` returns urgent. Archive is silent on severity words.

| given | expect on this implementation |
|---|---|
| status OPEN, severity CRITICAL, amount 1 | urgent |

Canonical severity ranking stays a recorded deviation until an SME or archive row states it. Queue ranking in the apps still uses the rebuilt Python function in Application A (FD-04). Application B may implement the same ranking only when this card and its tests sit in the lake. The 50,000 branch stays PROPOSED.

### RC-09 Operational open and closed

| Field | Value |
|---|---|
| id | `rule.open_closed.operational` |
| authority | `sme` |
| policy_status | `decided` |

BO-06a.

| given | expect |
|---|---|
| status REVIEW | OPEN |
| status HOLD | OPEN |
| status UNDER_REVIEW | OPEN |
| status ESCALATED | OPEN |
| status REOPENED | OPEN |
| status OPEN | OPEN |
| status CLOSED, engineering action pending | OPEN |
| status CLOSED, final disposition recorded, engineering action none | CLOSED_OPERATIONAL |

### RC-10 Finance and audit closure

| Field | Value |
|---|---|
| id | `rule.open_closed.finance_audit` |
| authority | `unresolved` |
| policy_status | `proposed` |

BO-06b unsigned. Three states. Mismatch routes to `HOLD_FOR_REVIEW`.

| given | expect |
|---|---|
| operational closed, no finance booked_at | HOLD_FOR_REVIEW when the question is finance-closed |
| operational closed, no audit mark | HOLD_FOR_REVIEW when the question is audit-closed |

### RC-11 Site is canonical

| Field | Value |
|---|---|
| id | `rule.region.site_canonical` |
| authority | `sme` |
| policy_status | `decided` |

BO-07. See `mapping-design.md`.

| given | expect |
|---|---|
| site IN-BLR | country IN, sales_region APAC |
| site US-TX | country US, sales_region AMER |
| site DE-BY | country DE, sales_region EMEA |
| site GB-ENG | country GB, sales_region EMEA |
| site BR-SP | country BR, sales_region AMER |
| site JP-KN | country JP, sales_region APAC |

### RC-12 Most specific scope wins

| Field | Value |
|---|---|
| id | `rule.region.specificity` |
| authority | `sme` |
| policy_status | `decided` |

Order: site, then country, then sales region.

| given | expect |
|---|---|
| site IN-BLR and a country-level FAB-RULE row for IN | bind the country row for that family; archive `recipe_release` still binds at derived APAC |

### RC-13 Scope disagreement

| Field | Value |
|---|---|
| id | `rule.region.disagreement` |
| authority | `sme` |
| policy_status | `decided` |

| given | expect |
|---|---|
| site IN-BLR, stored sales_region AMER | HOLD_FOR_REVIEW |
| country AU, no site | HOLD_FOR_REVIEW |
| country ZA, no site | HOLD_FOR_REVIEW |

### RC-14 Silent threshold

| Field | Value |
|---|---|
| id | `rule.threshold.silent` |
| authority | `unresolved` |
| policy_status | `proposed` |

BO-08 unsigned. Do not invent a number. Route to `HOLD_FOR_REVIEW`. Demo fallback, if a screen must show a number, is 50,000 labelled PROPOSED. Never 999,999.

| given | expect |
|---|---|
| amount 60000, archive silent on urgent cutoff | HOLD_FOR_REVIEW as live policy |
| demo display of Python cutoff | show 50000 with policy_status proposed |

### RC-15 Java blank skip

| Field | Value |
|---|---|
| id | `rule.month_end.blank.impl.java` |
| authority | `unresolved` |
| policy_status | `n/a` |

Observed: unreadable `amount_text` is skipped. Packaged blanks: 10. Honesty: REAL.

| given | expect on this implementation | expect canonical |
|---|---|---|
| amount_text empty | row omitted from count and total | HOLD_FOR_REVIEW or a reported skip; do not silently drop |

Canonical month-end handling of a blank is unresolved. Card expects `HOLD_FOR_REVIEW` on a blank when Application B evaluates the governed path.

### RC-16 Java float total

| Field | Value |
|---|---|
| id | `rule.month_end.float.impl.java` |
| authority | `unresolved` |
| policy_status | `n/a` |

Observed: `Double.parseDouble` into a `double` total. Canonical path records the deviation. It does not pick a binary money type here. Open question for Phase 6 if a money type is required.

### RC-17 Night batch flags REVIEW and HOLD as outstanding

| Field | Value |
|---|---|
| id | `rule.open_flag.impl.night_batch` |
| authority | `sme` |
| policy_status | `decided` |

The flag on REVIEW and HOLD matches BO-06a. Parity test: a REVIEW object is in the flagged set.

| given | expect |
|---|---|
| status REVIEW | flagged, OPEN |
| status HOLD | flagged, OPEN |
| status CLOSED | not flagged for status (threshold branch is separate) |

### RC-18 Night batch join multiplication

| Field | Value |
|---|---|
| id | `rule.night_batch.join_multiply` |
| authority | `unresolved` |
| policy_status | `n/a` |

Observed: join on country to every active register row. US has 5 active rows. One US object becomes 5 joined rows. `LIMIT 500` applies to joined rows.

| given | expect on this implementation | expect canonical |
|---|---|---|
| 1 US object, 5 active policies | up to 5 flagged joined rows | 1 object, overlap HOLD_FOR_REVIEW (RC-03) |

### RC-19 Replay is a duplicate candidate

| Field | Value |
|---|---|
| id | `rule.feed.replay_duplicate` |
| authority | `policy_archive` |
| policy_status | `n/a` |

Observed: 67 REPLAY rows. `reconcile()` marks DUPLICATE. This unit does not run `reconcile()`. Canonical: a REPLAY feed is a duplicate candidate. Drop waits for RT-05.

| given | expect |
|---|---|
| processing_status REPLAY | duplicate candidate, no auto drop |

### RC-20 Recipe mismatch shows both revisions

| Field | Value |
|---|---|
| id | `rule.recipe.mismatch_show_both` |
| authority | `sme` |
| policy_status | `decided` |

BO-05 governs the limit, not the winning revision string.

| given | expect |
|---|---|
| recipe_version R02, recipe_rev R01 | both values shown, route to RT-03, no model write of engineering_hold |

### RC-21 Event time and arrival time stay two fields

| Field | Value |
|---|---|
| id | `rule.clock.event_vs_arrival` |
| authority | `policy_archive` |
| policy_status | `n/a` |

11,985 of 12,500 evidence rows differ. Honesty: REAL. No signed cut-off owner.

| given | expect |
|---|---|
| event_time T1, arrival_time T2 | both fields shown; month-end uses event_time unless a later signed rule says otherwise. A signed cut-off is Unknown, so a cut-off question routes HOLD_FOR_REVIEW. |

### RC-22 Untrusted text is data

| Field | Value |
|---|---|
| id | `rule.untrusted_text.block` |
| authority | `policy_archive` |
| policy_status | `n/a` |

Harvested instruction language never drives approve, release, or ignore-validation. Expected verdict BLOCK. Locators in `injection-corpus-design.md`.

| given | expect |
|---|---|
| partner note with auto-approve language, proposed action approve | block true |
| bundled event source_claim, proposed action release | block true |

### RC-23 Never use 999,999 as live policy

| Field | Value |
|---|---|
| id | `rule.threshold.never_999999` |
| authority | `unresolved` |
| policy_status | `proposed` |

BO-08 working answer.

| given | expect |
|---|---|
| no archive match | HOLD_FOR_REVIEW, not 999999 |

### RC-24 Demo fallback 50,000 stays PROPOSED

| Field | Value |
|---|---|
| id | `rule.threshold.demo_50000` |
| authority | `unresolved` |
| policy_status | `proposed` |

| given | expect |
|---|---|
| demo display needs a cutoff | 50000 with proposed label |

### RC-25 Engineering hold is a person action

| Field | Value |
|---|---|
| id | `rule.hold.person_only` |
| authority | `sme` |
| policy_status | `proposed` |

FD-05 rejects a hold predictor. BO-03 working answer: a person approves every record-changing action. The tracker row is PROPOSED. Card stays `proposed`.

| given | expect |
|---|---|
| model proposes engineering_hold=1 | HOLD_FOR_REVIEW, no write |

---

## What this file does not do

This file does not write the YAML cards. It does not sign BO-06b or BO-08. It does not start Half B.
