# Rollback strategy

| Field | Value |
|---|---|
| Stage | Phase 7 / 14 Transformation plan. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p7a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Documents only. No tests written. Inherited repo not edited. |
| Evidence sources | FD-12; `docs/04-baseline-kpis/measurement-methodology.md`; `docs/07-repo-assessment/repo-assessment.md`; `sources/register.yaml`; `app/store.py`; `app/gateway_bridge.py`; `app/partner_feeds.py` |
| Assumptions | The old function body was left in the tree at cutover. Packaged SQLite files were not opened for write. Temporary copies can be deleted. |
| Unresolved issues | Named on-call person stays Unknown. Compose volume `legacy_data` rollback stays Unknown if Compose was used. |
| Residual risks | A generate reset after a failed slice would replace the freeze instead of rolling back the caller. Deleting the old function at cutover would leave no in-tree rollback. |

This file says how to undo one slice. It does not change a function.

---

## Finding

**Finding.** Rollback is a caller change back to the old function, then the characterization suite and the six-field check. Restore packaged files only when their hashes moved.
**Evidence.** `app/store.py` reads `LEGACY_DB`. Phase 0 hash set is 1,590 files in `sources/register.yaml`. Phase 1 residual risk: `apply()` on the default path writes `gateway_inbox`.
**Impact.** Half B can undo slice 3 without undoing slice 1, or undo all three from last to first.
**Risk.** Restoring a written packaged file from memory instead of from the hash-checked source.
**Confidence.** High when the harness-safety tests stayed green. Unknown if a Half B run wrote the packaged file.
**Open questions.** Whether Compose wrote the named volume.

---

## When to roll back

Roll back the slice that just cut over when any of these is true:

- A characterization test that calls an old function name fails.
- The six Phase 0 fields are not an exact match.
- A shadow field that was listed as exact match differs.
- Packaged file hashes no longer match the source register.
- An unexplained behaviour difference appears.

Do not roll back because exception cycle time is Unknown. That cell was already Unknown.

Do not roll back because aged backlog is Unknown. That cell was already Unknown.

---

## Shared rollback steps

1. Point the caller at the old function name. Slice table below.
2. Leave the new function in the tree. Do not delete it in the rollback. Deletion is a later clean-up after the phase sign-off.
3. Discard temporary database copies used by the failed slice.
4. Run the characterization suite. All tests that call old names must pass.
5. Run `python -m app.baseline` twice on a copy of the packaged cases. The six fields must match exactly: records 125, open_cases 89, urgent_cases 2, mean_amount 4982.61, sites 6, hours_per_case 0.603.
6. Confirm packaged `data/legacy.sqlite3` and `data/enterprise_legacy.sqlite3` hashes match the source register.
7. Record the rollback in `docs/15-modernization/transformation-log.md` and in `docs/16-repo-validation/behavior-difference-report.md`.

If step 6 fails, stop. The packaged freeze was written. Restore those two files from the hashed source tree. Re-run step 6. This is a file restore, not a policy change.

---

## Slice 1 — feed intake

| Field | Value |
|---|---|
| Caller rollback | `pull` / CLI calls `apply` again. |
| New function | `intake_apply` stays in the file, unused by the CLI. |
| Data | Discard the temp `LEGACY_DB` copy. Packaged `gateway_inbox` stays at 1 RECEIVED row when hashes match. |
| Finding | Current `apply` writes `received_at` from the clock at insert time. A temp copy that accepted a test event is discarded. |
| Evidence | `app/gateway_bridge.py`. Phase 1 inbox count. |
| Impact | New events enter through `apply` again. |
| Risk | Leaving Compose on a volume that already accepted extra inbox rows. |
| Confidence | High on the in-process caller. Unknown on Compose. |
| Open questions | Compose volume state. |

---

## Slice 2 — reconciliation

| Field | Value |
|---|---|
| Caller rollback | `--reconcile` calls `reconcile()` again. |
| New function | `reconcile_feeds` stays in the file, unused by the CLI. |
| Data | Discard the temp copies that ran reconcile. Packaged NEW 8,000, RETRY 500, REPLAY 67 stay when hashes match. |
| Finding | `reconcile()` updates `processing_status` on the file it opens. A packaged write would flip the 67 REPLAY rows. |
| Evidence | `app/partner_feeds.py`. CT-06. |
| Impact | The packaged store stays unreconciled, which is the Phase 1 recorded state. |
| Risk | Treating a discarded copy's DUPLICATE rows as the new freeze. |
| Confidence | High |
| Open questions | None if hashes match. |

---

## Slice 3 — rule evaluation

| Field | Value |
|---|---|
| Caller rollback | `GET /api/cases` already calls `priority()`. Night batch CLI calls `run()` again if it had moved to `run_flag()`. Live-policy callers stop calling `evaluate_live_policy`. |
| New function | `evaluate_live_policy` and `run_flag` stay in the tree, unused. |
| Data | Night-batch tests pass a copied enterprise file. Discard that copy. The job does not write `operational_objects` today. |
| Finding | Night batch returns a JSON report. It does not update object status in the current `run()`. |
| Evidence | `legacy_batch/shift_reconciliation.py`. |
| Impact | Ranking stays the current `priority()` deviation. Live-policy HOLD_FOR_REVIEW waits until a later cutover. |
| Risk | Leaving a caller on `evaluate_live_policy` after the rollback note. |
| Confidence | High |
| Open questions | None for `priority()` on this fixture. |

---

## Order when more than one slice must roll back

Undo the last cutover first.

Worked example. Slice 3 fails the six-field check. Half B points night-batch and live-policy callers back first. Re-runs the six-field check. If it still fails, points `--reconcile` back to `reconcile()`. Re-runs. If it still fails, points intake back to `apply()`. Re-runs. If it still fails after all three callers are old, the miss is in the packaged data or in `baseline.py`. Those two were not in the slice list. Stop and record Unknown on the cause until the hashes and the baseline function are checked.

---

## What rollback does not do

Rollback does not invent a tolerance percent on the six fields.

Rollback does not write 50,000 or 999,999 into the old functions.

Rollback does not merge finance-closed into operational-closed.

Rollback does not set an aged-backlog cutoff.

---

## What this file does not do

This file does not write test source. It does not edit the inherited repo. It does not start Half B.
