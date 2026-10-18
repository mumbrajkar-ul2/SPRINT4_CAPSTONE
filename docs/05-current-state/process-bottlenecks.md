# Process bottlenecks

| Field | Value |
|---|---|
| Stage | Phase 1 / 5 Current process and landscape |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | Read-only queries on both SQLite files on 2026-10-18; `app/partner_feeds.py`; `legacy_batch/shift_reconciliation.py`; `operations/incidents/INC-2025-014.md`; `docs/historic-decisions.md` |
| Assumptions | A bottleneck here is a place where packaged rows already pile up or where two readings of the same work disagree. |
| Unresolved issues | Time spent per queue is Unknown. The baseline tools do not emit hours on a case. Aged backlog cutoff is Unknown. |
| Residual risks | Treating 89 open cases as an aged backlog would invent an age rule that is not in the data. |

This file names where current work piles up. It does not change a queue.

## B1 Replay rows sit in the feed queue

**Finding.** 67 partner rows are still `REPLAY`.
**Evidence.** `SELECT COUNT(*) FROM partner_feeds WHERE processing_status = 'REPLAY'` returned 67. `docs/historic-decisions.md` records a 2025 rollback after a replayed delivery inflated the exception queue.
**Impact.** Those 67 rows remain in the same status list as 8,000 NEW rows and 500 RETRY rows until `reconcile()` runs.
**Risk.** A person or a later job that counts every non-ACCEPTED row as new work will add 67 duplicates to the load.
**Confidence.** High.
**Label.** Verified Fact for the count. Inference for the load effect.
**Open questions.** None for the count.

## B2 Recipe revision differs on most process steps

**Finding.** 91 of 125 process steps have a `recipe_version` that differs from the tool `recipe_rev`.
**Evidence.** Join query in `conflict-catalogue.md` BP1. Plan figure 91 of 125. This-query figure 91 of 125.
**Impact.** A reviewer who reads only the tool, or only the step, sees a different revision.
**Risk.** A hold or a release can be judged on the wrong revision.
**Confidence.** High.
**Label.** Verified Fact.
**Open questions.** Recipe authority is already decided later as BO-05. This unit does not re-decide it.

## B3 Two clocks on the same event

**Finding.** 11,985 of 12,500 evidence events have `arrival_time` different from `event_time`. 7,471 of 8,567 partner feeds have `ingest_ts` different from `source_ts`.
**Evidence.** Queries in `conflict-catalogue.md` BP3.
**Impact.** A late metrology result can be read as a current fact if the arrival clock is used as the event clock.
**Risk.** Month-end cut-off and late-event handling will disagree.
**Confidence.** High.
**Label.** Verified Fact for the counts. Inference for the cut-off effect.
**Open questions.** No signed cut-off owner.

## B4 Four programs rank the same work in four ways

**Finding.** Python, JavaScript, Java, and the night batch apply different tests to overlapping facts.
**Evidence.** The four source files. 2,090 enterprise objects have status REVIEW. 10 vendor rows have a blank `amount_text`. 0 of 125 cases have `amount` above 50,000.
**Impact.** A case can be urgent in one program and allowed in another.
**Risk.** Queue size and month-end totals will not match.
**Confidence.** High.
**Label.** Verified Fact.
**Open questions.** None. FD-08 already names the canonical archive.

## B5 Open and closed use different word lists

**Finding.** `cases` uses UNDER_REVIEW. `operational_objects` uses REVIEW and HOLD. `domain-profile.json` uses ENGINEERING_REVIEW and RELEASED. `policy_exceptions` uses WAIVED and BLOCKED.
**Evidence.** Distinct status lists in `conflict-catalogue.md` BP5. 89 cases have `status != 'CLOSED'`.
**Impact.** Two teams can report a different open count for the same week.
**Risk.** Aged backlog will move when the word list changes. The age cutoff is still Unknown, so the aged number stays Unknown.
**Confidence.** High.
**Label.** Verified Fact for the lists and the 89. Unknown for aged backlog.
**Open questions.** BO-06b remains PROPOSED.

## B6 Several active policies share one country code

**Finding.** `policy_register` has 34 active rows. Each of the eight country codes has 4 or 5 active rows. The night batch joins on region and active only.
**Evidence.** `SELECT region, COUNT(*) FROM policy_register WHERE active=1 GROUP BY region`. AU 4, BR 4, DE 5, GB 4, IN 4, JP 4, US 5, ZA 4.
**Impact.** One object matches several thresholds. The default `LIMIT 500` counts joined rows.
**Risk.** Flagged_count can grow without a new object arriving.
**Confidence.** High.
**Label.** Verified Fact.
**Open questions.** None for the counts.

## B7 Untrusted text tells a reader to approve or ignore

**Finding.** Instruction text sits in feeds, lake events, emails, and source documents.
**Evidence.** BP7 counts: 86 feeds, 150 bundled lake events, 3 emails, 22 source documents.
**Impact.** A person or a later model can treat that text as a decision.
**Risk.** A hold can be released from a feed note.
**Confidence.** High.
**Label.** Verified Fact.
**Open questions.** None for the counts.

## B8 No identity check, and work with no person

**Finding.** The API has no authentication code. 695 workflow tasks have `assigned_to` empty. INC-2025-014 follow-up owner is Unknown.
**Evidence.** `app/server.py`. `SELECT COUNT(*) FROM workflow_tasks WHERE assigned_to IS NULL` returned 695. Incident file text.
**Impact.** Anyone who can reach port 8080 can read cases. A disputed outage has no named owner.
**Risk.** Recovery stays on a spreadsheet, as it did at 04:00 UTC on 2025-11-18.
**Confidence.** High.
**Label.** Verified Fact. Owner remains Unknown.
**Open questions.** RT-06 assigns an incident owner later. Do not invent a name.

## Other piles

**Verified Fact.** 8 of 72 upstream outages have no resolve time.

**Verified Fact.** 18 of 125 process steps have `ended_at` empty.

**Verified Fact.** 1,875 of 2,500 integration attempts are FAILED, TIMEOUT, or RETRY.

**Verified Fact.** 8 of 125 wafer lots have `engineering_hold = 1`.

**Unknown.** Hours waiting in each pile. `operating_costs.hours_per_case` is 0.603 from Phase 0 tools. That is a monthly ratio. It is not wait time on these piles.

## What this file does not do

This file names the piles. It does not reorder a queue.
