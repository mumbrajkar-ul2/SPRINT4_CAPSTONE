# Five whys

| Field | Value |
|---|---|
| Stage | Phase 1 / 6 Root cause |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `docs/05-current-state/conflict-catalogue.md`; generator and rule files cited in each chain; BO-06a; FD-08 |
| Assumptions | Each "why" stops when the next answer would invent a person, a policy, or a number that is not in the files. |
| Unresolved issues | Several chains end at Unknown. |
| Residual risks | A five-why chain can look like a single cause. Parallel conditions still apply. See `root-cause-tree.md`. |

This file walks each business problem from the measured fact to the last evidenced condition. A step marked Inference is a reading of the files. A step marked Verified Fact names a file, table, or query.

## BP1 Recipe mismatch

1. Why do reviewers see two recipe revisions for one step? Because 91 of 125 `process_steps` rows have `recipe_version` different from the joined `fab_tools.recipe_rev`. **Verified Fact.** Query count 91.
2. Why do the two columns differ? Because `app/enterprise_data.py` picks `recipe_version` from R01, R02, R03, R04 and `app/domain_data.py` picks `recipe_rev` from R01, R02, R03. **Verified Fact** of the two choice lists. **Inference** that those generators produced the packaged 91.
3. Why is there no single stored revision for a step? Because the two tables keep separate columns and no current query in the API joins them for a decision. **Verified Fact** of the schemas and `app/server.py` routes.
4. Why can a decision still proceed? Because `GET /api/domain/process_steps` and `GET /api/domain` tool reads return each table on its own. **Verified Fact.**
5. Why is that the last step? Because the next why would invent an owner for recipe authority. BO-05 is already decided for a later phase. This unit does not re-decide it. **Unknown** person. **Verified Fact** of BO-05 status.

## BP2 Replay inflation

1. Why can the exception queue grow without a new event? Because 67 rows sit in `partner_feeds` with `processing_status = 'REPLAY'`. **Verified Fact.** Count 67.
2. Why do those rows exist? Because `app/partner_feeds.py` appends a `REPLAY-` copy when the generator index is a multiple of 127. **Verified Fact.**
3. Why are they still REPLAY? Because `reconcile()` writes DUPLICATE only when it is run, and this packaged file was left before that write. **Verified Fact** of the function. **Inference** that reconcile was not applied to the packaged 67.
4. Why does a replay matter to operations? Because `docs/historic-decisions.md` records a 2025 rollback after a replayed partner delivery inflated the queue. **Verified Fact** of the note. That note and the 67 rows are correlated facts. This chain does not label the 67 rows as the 2025 cause.
5. Why is there no further person? Because no named owner sits on replay handling. **Unknown.**

## BP3 Time confusion

1. Why can a late result look current? Because 11,985 of 12,500 `evidence_events` rows have `arrival_time` different from `event_time`. **Verified Fact.** Count 11,985.
2. Why are there two clocks? Because `app/enterprise_legacy.py` writes `event_time` and `arrival_time` as separate columns. `app/partner_feeds.py` writes `source_ts` and `ingest_ts`. **Verified Fact.**
3. Why do effective dates also overlap? Because 45 `reference_versions` pairs on the same `ref_key` have overlapping `valid_from` / `valid_to`. **Verified Fact.** Count 45.
4. Why does the current API not keep the clocks apart for the reader? Because `GET /api/cases/{id}` returns `events.recorded_at` only. It does not return `source_ts` and `ingest_ts` as a pair. **Verified Fact.**
5. Why is cut-off still open? Because no signed month-end cut-off owner exists in the inherited files. **Unknown.**

## BP4 Four disagreeing implementations

1. Why do reports disagree on the same work? Because four programs apply different tests. **Verified Fact** of the four files.
2. Why does Python differ? Because `priority()` uses 50,000 and CRITICAL. **Verified Fact.** `amount > 50000` count is 0 on this set.
3. Why does JavaScript differ? Because `legacyAllows` uses archive limit times 1.05 and returns 999,999 when no year matches. **Verified Fact.**
4. Why does Java differ? Because it adds `Double.parseDouble` on column 5 and skips a blank. **Verified Fact.** Blank `amount_text` count is 10.
5. Why does the night batch differ? Because it flags HOLD and REVIEW. REVIEW count is 2,090. **Verified Fact.** FD-08 already names the archive as canonical. The next why would re-decide FD-08. Stop.

## BP5 Open and closed differ

1. Why can two teams report a different open count? Because 89 cases are not CLOSED on the Python test, while enterprise objects use REVIEW and HOLD, and the domain profile uses ENGINEERING_REVIEW. **Verified Fact.**
2. Why are the words different? Because five lists were stored in five places. **Verified Fact** of the lists in the catalogue.
3. Why does that change a backlog? Because BO-06a treats REVIEW and HOLD as open, and the Python baseline treats only `status != 'CLOSED'` on `cases`. **Verified Fact** of both rules.
4. Why is finance still separate? Because BO-06b stays PROPOSED. Operational, finance, and audit closure remain three working states. **Verified Fact** of the tracker row. Not signed policy.
5. Why is aged backlog still Unknown? Because no age cutoff exists in `policy_register` or the archive. `created_at` exists. A cutoff is not invented. **Unknown.**

## BP6 Three region vocabularies

1. Why can one lot sit in more than one region reading? Because `cases.region` has 3 values, `operational_objects.region` has 8 country codes, and site codes are 6 city tags. **Verified Fact.**
2. Why do policies overlap? Because 34 active `policy_register` rows sit 4 or 5 per country code. **Verified Fact.** Count 34.
3. Why does the night batch multiply rows? Because it joins on `region` and `active=1` only. **Verified Fact.**
4. Why is there no stored map? Because no table maps APAC to IN or to IN-BLR. **Verified Fact** of the schemas.
5. Why is the map not decided here? Because FD-09 is a later decision. **Verified Fact** of the tracker. Stop.

## BP7 Untrusted approve or ignore text

1. Why can text try to drive a decision? Because 86 feeds, 150 bundled lake events, 3 emails, and 22 source documents contain approve or ignore instructions. **Verified Fact.** Counts match the plan.
2. Why is that text present? Because four generators write those strings. **Verified Fact** of `partner_feeds.py`, `historical_fixture.py`, `archived_documents.py`, and `generate_documents.py`.
3. Why can a reader treat it as an instruction? Because the API returns `cases.note` and partner `raw_json` without a trust label on the HTTP response. **Verified Fact** of `app/server.py`.
4. Why does that matter for a later model? Because FD-02 already limits the model to read-only tools. The text is still in the data. **Verified Fact.**
5. Why is there no further policy here? Because treating harvested text as an instruction is already forbidden by the engagement rules. Stop.

## BP8 No auth and unknown owner

1. Why can any caller read cases? Because `app/server.py` `do_GET` has no identity check. **Verified Fact.**
2. Why does a disputed outage sit without a person? Because `INC-2025-014.md` says follow-up owner unknown. **Unknown** person. **Verified Fact** of the sentence.
3. Why do 695 tasks have no assignee? Because `workflow_tasks.assigned_to` is empty on those rows. **Verified Fact.** Count 695.
4. Why did recovery use a spreadsheet on 2025-11-18? Because the incident file records a 04:00 UTC spreadsheet after two retries. **Verified Fact** of the file. This is correlation with the missing owner, not labelled as the only cause.
5. Why is an owner not named here? Because RT-06 assigns one later in the live app. Company job titles are not mapped. Stop.

## What this file does not do

This file does not assign a new owner. It does not write a repair.
