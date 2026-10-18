# Repository assessment

| Field | Value |
|---|---|
| Stage | Phase 1 / 7 Deep repo assessment |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | Inherited tree; `pyproject.toml`; `app/server.py`; seven files in `tests/`; `compose.yaml`; Phase 0 repository overview; read-only database counts on 2026-10-18 |
| Assumptions | Phase 0 file walk of 1,590 hashed files remains the tree size. This unit did not re-hash. |
| Unresolved issues | Live unittest count is Unknown. This unit did not run tests. |
| Residual risks | `tests/test_source_gateway.py` can write `gateway_inbox` on the packaged database. |

This file assesses the inherited repository as it stands. It does not change the tree.

## What the repository is

**Verified Fact.** `pyproject.toml` names `fabpulse-legacy` version 0.1.0. It requires Python 3.10 or newer. It declares no third-party Python package.

**Verified Fact.** The application is a standard-library HTTP server on SQLite. Optional Java and JavaScript programs sit beside it.

**Verified Fact.** Phase 0 counted 1,590 files. `data/` held 1,512 of them.

## Strengths that this unit confirmed

| Strength | Evidence | Label |
|---|---|---|
| Packaged data is already present | 19 tables and 12 tables opened read-only. Workshop check in Phase 0 reported integrity ok | Verified Fact |
| Foreign keys exist on domain tables | `wafer_lots.tool_id` references `fab_tools`. Enterprise child tables reference `operational_objects` | Verified Fact |
| A policy archive exists | `contracts/decision-policies-archive.json` and `policy_register` | Verified Fact |
| Some tests use a temporary database | `test_workflow.py`, `test_domain.py`, `test_historical_fixture.py`, `test_enterprise_legacy_v6.py` | Verified Fact |
| Offline verify scripts exist | `scripts/verify_preloaded.py`, `app/workshop_check.py`, `app/baseline.py` | Verified Fact |

## Gaps that this unit confirmed

| Gap | Evidence | Label |
|---|---|---|
| No authentication on GET routes | `app/server.py`, source gateway | Verified Fact |
| Four rule programs disagree | BP4 catalogue | Verified Fact |
| Thin tests on the eight conflicts | See `characterization-test-plan.md` | Verified Fact of the test files |
| One test writes the default database | `tests/test_source_gateway.py` calls `gateway_bridge.apply()` without a temp `LEGACY_DB` | Verified Fact |
| No close-time column on cases | `PRAGMA table_info(cases)` | Verified Fact |
| No stored region map | Three vocabularies, no join table | Verified Fact |
| SQL report is untuned | `sql/legacy_reports.sql` comment and unrestricted join | Verified Fact |
| Generate reset can replace the freeze | `app/generate.py --reset`. GitHub verify workflow | Verified Fact |

## Runtime surface

**Verified Fact.** Default API: `http://127.0.0.1:8080`. Default gateway: `http://127.0.0.1:8090`.

**Verified Fact.** `compose.yaml` starts three services. The API volume is `legacy_data`. The gateway reads `/opt/legacy/data/legacy.sqlite3` inside the image. The bridge writes the named volume.

**Unknown.** Whether Docker Compose runs on this laptop.

## Test surface

**Verified Fact.** Seven modules. Checks include temp-DB case counts, foreign keys, tiny-lake sizes, and a 120-row night-batch processed count.

**Verified Fact.** No test module asserts the 91 recipe mismatches, the 67 REPLAY rows, the two-clock fields, the four rule outputs on one input, the five status lists, the 34 active policies, the 86 untrusted feeds, or the absence of auth headers.

**Unknown.** Pass count on 2026-10-18.

## Data quality observations

These are catalogue facts. They are not repairs.

**Verified Fact.** 91 recipe mismatches. 67 REPLAY rows. 10 blank vendor amounts. 18 process steps with empty `ended_at`. 8 unresolved outages. 695 unassigned tasks. 1,875 integration attempts that are not SUCCESS.

**Verified Fact.** `state_history` has one row per object. It is not a full state timeline.

## Material finding

**Finding.** The repository can serve a local demo and a measured catalogue. Coverage of the eight conflicts is thin. One test can write the packaged store.
**Evidence.** File reads and query counts in this unit.
**Impact.** Later characterization tests need named checks before behaviour is changed in Phase 7.
**Risk.** Running the current gateway test or Compose against the working copy changes operational rows.
**Confidence.** High.
**Open questions.** Live test count remains Unknown.

## What this file does not do

This file does not add a dependency or a test.
