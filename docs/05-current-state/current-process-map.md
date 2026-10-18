# Current process map

| Field | Value |
|---|---|
| Stage | Phase 1 / 5 Current process and landscape |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `docs/business-context.md`; `app/server.py`; `app/partner_feeds.py`; `app/gateway_bridge.py`; `app/legacy_logic.py`; `legacy_batch/shift_reconciliation.py`; `legacy_js/legacy_policy.js`; `legacy_java/ReconcileLegacy.java`; `operations/incidents/INC-2025-014.md`; read-only queries on `data/legacy.sqlite3` and `data/enterprise_legacy.sqlite3` on 2026-10-18 |
| Assumptions | The packaged simulator is the current-state process. Live fab floors are not present. |
| Unresolved issues | INC-2025-014 follow-up owner is Unknown. Company job titles are not mapped. BO-06b stays PROPOSED. Exception cycle time and aged backlog stay Unknown. |
| Residual risks | A reader who treats the night batch, the API, and the Java totals as one reading will mix four rule paths. |

This file maps the current work from message arrival to month-end totals. It does not propose a new process.

## The human path

**Verified Fact.** `docs/business-context.md` lists five steps.

1. External sources produce case messages.
2. The integration process reconciles or imports them into the legacy system.
3. Operations users review and prioritize work.
4. Case decisions are recorded in local systems.
5. Monthly operating measures are reviewed.

## The technical path that sits under those steps

```text
MESDispatch / PLM-Metrology / partner files / vendor CSV
        |
        +--> source gateway HTTP :8090  (reads wafer_lots, emits events)
        |         |
        |         v
        |    gateway_bridge  (writes gateway_inbox)
        |
        +--> partner_feeds rows  (NEW / RETRY / REPLAY)
        |         |
        |         v
        |    partner_feeds.reconcile()  (writes ACCEPTED / REJECTED / DUPLICATE)
        |
        +--> source_messages  (JSON body, arrival order)
        |
        +--> vendor_file_rows  (raw amount_text from partner_export.csv)
        |
        v
legacy.sqlite3  (19 tables)
        |
        +--> API GET /api/cases  (adds priority from app/legacy_logic.py)
        +--> API GET /api/cases/{id}  (adds manual_review_required)
        +--> API GET /api/metrics  (case counts and operating_costs)
        +--> sql/legacy_reports.sql  (region and status totals)

enterprise_legacy.sqlite3  (12 tables)
        |
        +--> night batch shift_reconciliation.py  (flags HOLD, REVIEW, or value over threshold)
        +--> policy_register lookup by country code

contracts/decision-policies-archive.json
        |
        +--> legacy_js/legacy_policy.js  (limit times 1.05; missing year returns 999999)

vendor CSV amounts
        |
        +--> legacy_java/ReconcileLegacy.java  (float sum; skips a blank amount)
```

**Verified Fact.** `compose.yaml` starts the API on container port 8080, the source gateway on container port 8090, and a one-shot `gateway_bridge` after both health checks pass.

## Queues that hold work today

**Verified Fact.** Read-only counts on 2026-10-18.

| Queue | What it holds | Count | Source |
|---|---|---:|---|
| Partner feeds in NEW | Rows not yet reconciled | 8,000 | `partner_feeds.processing_status` |
| Partner feeds in RETRY | Rows marked for another pass | 500 | same table |
| Partner feeds in REPLAY | Replayed deliveries still in REPLAY | 67 | same table |
| Cases not CLOSED | OPEN 42, UNDER_REVIEW 30, ESCALATED 9, REOPENED 8 | 89 | `cases.status` |
| Cases CLOSED | Final word in this table | 36 | `cases.status` |
| Enterprise objects in REVIEW | Night batch flags these | 2,090 | `operational_objects.status` |
| Enterprise objects in HOLD | Night batch flags these | 2,083 | same table |
| Workflow tasks with no person | `assigned_to` is empty | 695 | `workflow_tasks` |
| Upstream outages with no resolve time | `resolved` is empty | 8 | `upstream_outages` |
| Process steps still running | `ended_at` is empty | 18 | `process_steps` |
| Batch runs FAILED or PARTIAL | Night or partner batch result | 17 + 21 | `batch_runs` |

Worked example. A partner row `REPLAY-000000000` sits in `partner_feeds` with `processing_status = 'REPLAY'`. `reconcile()` later writes `DUPLICATE` on that row. Until that function runs, the 67 REPLAY rows stay in the feed queue.

## Decision points

| Step | Who or what decides | Rule in force today | Label |
|---|---|---|---|
| Feed reconcile | `app/partner_feeds.py` `reconcile()` | Missing key or `unsupported` schema becomes REJECTED. `REPLAY` becomes DUPLICATE. Negative quantity becomes REJECTED. Other NEW or RETRY rows become ACCEPTED. | Verified Fact |
| Case priority | `app/legacy_logic.py` `priority()` | CLOSED becomes archive. CRITICAL or amount above 50,000 becomes urgent. HIGH or ESCALATED becomes review. Everything else becomes queue. | Verified Fact |
| Manual review flag | `manual_review_required()` | HIGH, CRITICAL, ESCALATED, or REOPENED returns true. | Verified Fact |
| Night batch flag | `legacy_batch/shift_reconciliation.py` | HOLD or REVIEW is flagged. A value above the joined `policy_register.threshold` is also flagged. | Verified Fact |
| JavaScript allow | `legacy_js/legacy_policy.js` | Amount is allowed when it is at or below the archive limit times 1.05. A missing year or region returns 999,999. | Verified Fact |
| Java month-end total | `legacy_java/ReconcileLegacy.java` | Column 5 is parsed as a float and added. A blank or unreadable amount is skipped. | Verified Fact |
| Operational open or closed | SME BO-06a, DECIDED | A case is open while any disposition or engineering action is still pending, including REVIEW and HOLD. A case is closed only when a final disposition is recorded and no engineering action is pending. | Verified Fact of the locked decision |

**Verified Fact.** FD-08 DECIDED. The canonical rule source is `contracts/decision-policies-archive.json` and the `policy_register` table. The four programs above are deviations.

## Open and closed on this map

**Verified Fact.** `cases.status` uses OPEN, UNDER_REVIEW, CLOSED, ESCALATED, and REOPENED.

**Verified Fact.** `operational_objects.status` uses OPEN, REVIEW, HOLD, CLOSED, REOPENED, and ESCALATED.

**Verified Fact.** `domain-profile.json` human queue words are QUEUED, PROCESSING, HOLD, ENGINEERING_REVIEW, and RELEASED.

**Verified Fact.** BO-06a treats REVIEW and HOLD as open. BO-06b stays PROPOSED. Operational, finance, and audit closure remain three states on that working answer. This map does not treat that working answer as signed policy.

## Clock fields on the path

**Verified Fact.** Partner feeds store `source_ts` and `ingest_ts`. 7,471 of 8,567 rows have different values.

**Verified Fact.** Enterprise `evidence_events` store `event_time` and `arrival_time`. 11,985 of 12,500 rows have different values.

**Verified Fact.** `reference_versions` stores `valid_from` and `valid_to`. 45 version pairs on the same `ref_key` overlap.

**Verified Fact.** `cases` stores `created_at`. There is no `closed_at` column. Exception cycle time stays Unknown. Columns checked: `cases.created_at`, `cases.status`, `events.recorded_at`, `events.event_type`, `state_history.at_utc`. `state_history` has one row per object.

## Outage path

**Verified Fact.** `operations/incidents/INC-2025-014.md`. On 2025-11-18 a partner feed was delayed. The queue was retried twice. Downstream totals diverged. Staff used a spreadsheet at 04:00 UTC. Follow-up owner unknown.

That path sits beside the API. It is a current recovery step.

## What this file does not do

This file names the current path and the queues. It does not change a rule. It does not assign an owner.
