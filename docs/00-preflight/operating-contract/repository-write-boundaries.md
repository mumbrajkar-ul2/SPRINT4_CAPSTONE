# Repository write boundaries

| Field | Value |
|---|---|
| Stage | Phase 0 / 0B Provisional operating contract |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL |
| Evidence sources | `Execution_Plan.md` section 11; FD-01; `PRELOADED_DATA.md`; `app/store.py`; `app/partner_feeds.py`; `app/generate.py` name in `README.md`; `compose.yaml`; `.github/workflows/verify.yml` |
| Assumptions | People who work on this capstone will read this page before they run a generator or Compose. |
| Unresolved issues | No named person is assigned as the only one who may run `generate --reset`. That owner is Unknown. |
| Residual risks | Python may write `__pycache__` when a module is imported. Those files are not source. They must not stay in the inherited tree. |

These write rules are PROVISIONAL. They protect the frozen baseline.

## What may be written now

**Verified Fact.** `Execution_Plan.md` section 11. New deliverables are written at the capstone root: `docs/`, `apps/`, `context-lake/`, `policy/`, `sources/`, `operations/`, and a later full-stack Compose file.

Phase 0 may write:

- `docs/00-preflight/`, `docs/01-engagement/`, `docs/02-stakeholders/`, `docs/03-problem-value/`, `docs/04-baseline-kpis/`
- `sources/register.yaml`

Phase 0 may not write:

- Any file under `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`
- `playbook/STATUS.md`
- `Decision_Tracker.md`
- `PROJECT_ACRONYMS.md`
- `docs/_playbook-log.md`

**Verified Fact.** Only the Phase 7 transform edits files inside the inherited repo.

## Commands that write inside the inherited repo

Treat these as write commands. Do not run them against the working copy in Phases 0 to 6.

| Command | What it writes | Evidence | Label |
|---|---|---|---|
| `python -m app.generate --reset` | Replaces `data/legacy.sqlite3` rows | `README.md`, `.github/workflows/verify.yml` | Verified Fact |
| `python -m app.partner_feeds` without a read-only flag | Inserts partner rows | `app/partner_feeds.py` `generate()` | Verified Fact |
| `python -m app.partner_feeds --reconcile` | Updates `processing_status` | `app/partner_feeds.py` `reconcile()` | Verified Fact |
| `python -m app.gateway_bridge` | Writes inbox and checkpoints | `PRELOADED_DATA.md`, `compose.yaml` | Verified Fact |
| `docker compose up` on the inherited file | Starts the bridge, which writes | `compose.yaml` | Verified Fact |
| `python -m app.enterprise_legacy` / document generators | Rebuild archive rows | `README.md` | Verified Fact |

## Commands that this unit ran

**Verified Fact.** This unit ran, twice, from the inherited root:

1. `python scripts/verify_preloaded.py`
2. `python -m app.workshop_check`
3. `python -m app.baseline`

`scripts/verify_preloaded.py` opens SQLite with `mode=ro`. `app.workshop_check` and `app.baseline` call `setup()` / `init()`, which run `CREATE TABLE IF NOT EXISTS`. After both runs, SHA-256 hashes of all 1,590 inherited files matched the hashes taken before the runs. Import created `__pycache__` files. Those files were removed. The tree hash count returned to 1,590.

## Rule for later phases

**Inference.** A command that can change a packaged row must be run on a copy, or it must wait until Phase 7 with a characterization test already in place.

**Unknown.** The named person who may authorize a reset of the packaged database.

Flag that owner. Do not invent a name.
