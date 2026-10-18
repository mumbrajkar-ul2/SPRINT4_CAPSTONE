# Measurement methodology

| Field | Value |
|---|---|
| Stage | Phase 0 / 4 Before-AI KPIs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `app/baseline.py`; `app/workshop_check.py`; `scripts/verify_preloaded.py`; `scripts/offline_inventory.py`; `app/store.py`; `app/legacy_logic.py`; `docs/baseline-measurement-notes.md`; `operations/baseline-evidence.md`; `PRELOADED_DATA.md` |
| Assumptions | Repeating the same three commands on the packaged database is the freeze method |
| Unresolved issues | Cycle time and aged-backlog queries are not in the current tools |
| Residual risks | A later generate --reset would invalidate this method's population |

## Purpose

Freeze how the current-state numbers were produced so Phase 14 can measure the same way, or record a deliberate change.

## Population

**Verified Fact.** Packaged `data/legacy.sqlite3` and the other stores listed by `scripts/verify_preloaded.py`. `PRELOADED_DATA.md` says do not generate on first run. This unit did not generate.

**Verified Fact.** `domain.json` records seed 4552. That seed was not used in this unit because no generator ran.

**Verified Fact.** `docs/baseline-measurement-notes.md` says record the data window, denominator, exclusions, and assumptions before comparing outcomes. The current tools do not expose a time window. Window: Unknown.

## Tools

| Tool | Command | What it reads | What it writes |
|---|---|---|---|
| Preloaded verify | `python scripts/verify_preloaded.py` | Packaged SQLite in `mode=ro`, lake manifests, document folders | Nothing in the data files |
| Workshop check | `python -m app.workshop_check` | Table counts, foreign keys, integrity | `init()` runs `CREATE TABLE IF NOT EXISTS` only |
| Baseline | `python -m app.baseline` | `cases` and `operating_costs` | `setup()` runs `CREATE TABLE IF NOT EXISTS` only |

## Baseline formulas

**Verified Fact.** From `app/baseline.py`.

- `records` = number of rows from `SELECT status, severity, amount, site FROM cases`.
- `open_cases` = count of those rows where `status != 'CLOSED'`.
- `urgent_cases` = count where `priority(status, severity, amount) == 'urgent'`.
- `mean_amount` = `statistics.fmean(amount)` rounded to 2 decimals.
- `sites` = number of distinct `site` values.
- `hours_per_case` = sum(`labor_hours`) / sum(`total_cases`) from `operating_costs`, rounded to 3 decimals.

**Verified Fact.** From `app/legacy_logic.py`. Urgent means severity is CRITICAL or amount is greater than 50,000, and status is not CLOSED.

These formulas are the current-state Python reading. They are not the SME operational meaning of open. BO-06a is a later semantic fact.

## Repeat method

1. Use the inherited working copy. Do not pass `--reset`.
2. Run the three commands in the inherited root.
3. Run them a second time.
4. Diff the JSON. Every field must match.
5. If a command fails, record the error and mark that number Unknown.

**Verified Fact.** On 2026-10-18 both runs exited 0 and matched.

## Integrity check after the runs

SHA-256 of all inherited files was taken before the runs and after the runs. After removing six `__pycache__` files created by import, 1,590 files remained and every hash matched the before-run set. The register uses that 1,590-file set.

## What later phases must add before they claim the headlines

| Measure | Missing method | Do not do |
|---|---|---|
| Exception cycle time | Name the start timestamp, the end timestamp, the open/closed rule, and the exclusions | Invent a mean hour figure |
| Aged backlog | Name the age threshold and the open rule | Call 89 the aged backlog |
| Decision quality | Expert-labelled set | Guess a percent |
| Performance | Time the live HTTP calls | Copy an inherited SLO |
| AI quality | Evaluation suite | Score a model that was not called |
| ROI | Educational model with stated assumptions | Claim a saving |

## Honesty

**Verified Fact.** `operations/baseline-evidence.md`. Values in this archive are synthetic and cannot be claimed as observed enterprise financial benefits.

**Verified Fact.** `Execution_Plan.md` section 9 honesty labels stay as written.
