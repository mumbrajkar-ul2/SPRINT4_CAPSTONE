# Repository overview

| Field | Value |
|---|---|
| Stage | Phase 0 / 0A Pre-flight orientation |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` file walk on 2026-10-18; `sources/register.yaml`; `README.md`; `PRELOADED_DATA.md`; `DATA_READINESS.md`; `pyproject.toml`; `compose.yaml`; `scripts/verify_preloaded.py` run output |
| Assumptions | The inherited tree is the current-state system under study. Later phases may change only this tree. |
| Unresolved issues | The named person who will sign the charter is Unknown. The company job titles that map to the SME role names are unconfirmed. |
| Residual risks | Most of the tree is synthetic archive files. A reader who treats those files as live production data will misread volume and risk. |

This file orients on the inherited repository. It does not recommend a transformation.

## What the tree is

**Verified Fact.** The inherited repository lives at `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`. The walk on 2026-10-18 counted 1,590 files. Every file was readable. `sources/register.yaml` stores one SHA-256 hash per file. The hash count is 1,590.

**Verified Fact.** `README.md` names the product `fabpulse-legacy` and the domain High Tech — Semiconductor Engineering Intelligence. `pyproject.toml` sets `requires-python = ">=3.10"` and says the project is a synthetic legacy enterprise workflow.

**Verified Fact.** `PRELOADED_DATA.md` and `DATA_READINESS.md` say the default workshop data is already in the tree. The first run does not generate data.

**Verified Fact.** `README.md` and `DATA_READINESS.md` say the Python path uses the standard library only. No extra Python package is declared in `pyproject.toml`.

## How the files sit

**Verified Fact.** File counts by top-level folder, from the 2026-10-18 walk:

| Folder | File count | What is there |
|---|---:|---|
| `data/` | 1,512 | SQLite databases, lake fixtures, documents, archive mail |
| `app/` | 18 | Python HTTP server, store, rules, generators, reports |
| `docs/` | 18 | Business, interface, measurement, and history notes |
| repository root | 11 | README, Compose, Docker, domain JSON, run script |
| `tests/` | 7 | Unit and characterization tests |
| `scripts/` | 5 | Verify, inventory, smoke, and rehearse scripts |
| `environments/` | 3 | Example env files for host and ports |
| `operations/` | 3 | Runbook, baseline note, incident INC-2025-014 |
| `services/` | 3 | Source gateway HTTP simulator |
| `integration/` | 2 | Source contract and gateway JSON |
| `legacy_batch/` | 2 | Night-shift reconciliation script |
| `.github/` | 1 | Verify workflow |
| `contracts/` | 1 | Decision policy archive |
| `legacy_java/` | 1 | Java month-end totals |
| `legacy_js/` | 1 | JavaScript policy consumer |
| `ops/` | 1 | Log sampler |
| `sql/` | 1 | Legacy report SQL |

The 1,512 data files dominate the tree. **Inference.** Most of the estate under study is packaged synthetic data, not application code.

## What the packaged data holds

**Verified Fact.** `scripts/verify_preloaded.py` run 1 and run 2 both reported `ready: true` and no problems. `data/legacy.sqlite3` has 19 tables. Row counts include 125 cases, 145 events, 15 source messages, 36 operating-cost months, 8,567 partner feeds, 224 policy exceptions, 72 outages, and 60 batch runs. `data/enterprise_legacy.sqlite3` has 12 tables, including 12,500 operational objects. The tiny lake tier has 2,400 transactions, 9,500 events, and 360 documents. The bundled lake tier has 50,000 transactions, 100,000 events, and 600 documents.

**Verified Fact.** `PRELOADED_DATA.md` says the workshop (500k) and stress (2M) tiers are not in this archive.

## How a person starts it

**Verified Fact.** `PRELOADED_DATA.md` lists the no-generation start: `python scripts/offline_inventory.py`, `python -m app.workshop_check`, `python -m unittest discover -s tests -q`, `python -m app.baseline`, then `python -m app.server`. The HTTP server default is `http://127.0.0.1:8080`. `compose.yaml` starts the legacy service on host port 8080 and the source gateway on host port 8090.

**Verified Fact.** `PRELOADED_DATA.md` says `python -m app.gateway_bridge` writes ingestion state. This Phase 0 unit did not run the server, the bridge, or any generator.

## Material finding

**Finding.** The inherited tree is a complete offline workshop: 1,590 files, packaged databases, and a Python standard-library runtime.
**Evidence.** File walk and `sources/register.yaml`. `scripts/verify_preloaded.py` both runs. `README.md`, `PRELOADED_DATA.md`, `pyproject.toml`.
**Impact.** Phase 0 can freeze a source register and a measured baseline without generating data.
**Risk.** A later phase that runs a generator with `--reset` will replace the packaged rows and break this freeze.
**Confidence.** High.
**Open questions.** None for orientation. The named signer of the charter is Unknown.

## What this file does not do

This file records the current tree. It does not propose a new architecture.
