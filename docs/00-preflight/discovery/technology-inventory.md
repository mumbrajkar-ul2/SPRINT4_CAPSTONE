# Technology inventory

| Field | Value |
|---|---|
| Stage | Phase 0 / 0A Pre-flight orientation |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `pyproject.toml`; `README.md`; `Dockerfile`; `compose.yaml`; `app/server.py`; `app/store.py`; `app/legacy_logic.py`; `.github/workflows/verify.yml`; `legacy_java/ReconcileLegacy.java`; `legacy_js/legacy_policy.js`; `environments/dev.env.example`; `DATA_READINESS.md` |
| Assumptions | Optional Java and Node runtimes are present only when a person runs those two tools. They are not required for the Python baseline. |
| Unresolved issues | Docker runtime and cross-platform support are not certified by the package (`DATA_READINESS.md`). Whether this laptop can run Compose is Unknown until a later phase starts those containers. |
| Residual risks | The GitHub workflow regenerates 6,000 cases. That command would replace packaged rows if someone runs it against the working copy. |

This file lists the current technologies. It does not recommend replacements.

## Runtime and language

| Item | What it is | Evidence | Label |
|---|---|---|---|
| Python 3.10 or newer | Required language for the application and tests | `pyproject.toml`, `README.md`, `DATA_READINESS.md` | Verified Fact |
| Python standard library only | HTTP server, SQLite, unittest. No third-party package is declared | `pyproject.toml`, `README.md` | Verified Fact |
| Python 3.13.5 | Interpreter used for the Phase 0 baseline runs | Local `python --version` on 2026-10-18 | Verified Fact |
| SQLite | File databases for operational, enterprise, and lake fixtures | `app/store.py`, `scripts/verify_preloaded.py` output | Verified Fact |
| Threaded HTTP server | `ThreadingHTTPServer` in the legacy API and the gateway | `app/server.py`, `services/source_gateway/server.py` | Verified Fact |
| Docker image | `python:3.12-slim`, copies the tree, starts `app.server` | `Dockerfile` | Verified Fact |
| Docker Compose | Three services: legacy, source-gateway, one-shot bridge | `compose.yaml` | Verified Fact |
| GitHub Actions | Checkout, Python 3.12, unittest, optional generate, baseline | `.github/workflows/verify.yml` | Verified Fact |
| Java | Optional month-end totals program | `legacy_java/ReconcileLegacy.java`, `README.md` | Verified Fact |
| Node / JavaScript | Optional policy consumer | `legacy_js/legacy_policy.js`, `README.md` | Verified Fact |

## Data and contract files

| Item | What it is | Evidence | Label |
|---|---|---|---|
| `data/legacy.sqlite3` | 19-table operational database | `scripts/verify_preloaded.py` | Verified Fact |
| `data/enterprise_legacy.sqlite3` | 12-table enterprise archive | `scripts/verify_preloaded.py` | Verified Fact |
| Lake tiny and bundled SQLite + JSONL + CSV | Historical fixtures | `PRELOADED_DATA.md`, verify output | Verified Fact |
| JSON domain files | `domain.json`, `domain-profile.json` | repository root | Verified Fact |
| Policy archive | `contracts/decision-policies-archive.json` | that file | Verified Fact |
| Integration contracts | `integration/source-contract-v1.json`, `integration/source-gateway.json` | those files | Verified Fact |
| Example env files | Host 127.0.0.1, port 8080, source port 8090 | `environments/dev.env.example` | Verified Fact |

## Tests and checks

| Item | What it is | Evidence | Label |
|---|---|---|---|
| 7 test modules | `tests/test_workflow.py` and six sibling files | file walk | Verified Fact |
| Workshop check | Offline table counts and integrity | `app/workshop_check.py` | Verified Fact |
| Preloaded verify | Read-only inventory of packaged stores | `scripts/verify_preloaded.py` | Verified Fact |
| Baseline metrics | Records, open cases, urgent cases, mean amount, sites, hours per case | `app/baseline.py` | Verified Fact |

**Verified Fact.** `Project_Intent.md` section 4.2 records 15 tests passed in a prior review. This Phase 0 unit did not re-run `unittest`. The live test count on 2026-10-18 is Unknown.

## What is absent from the current tree

**Verified Fact.** `app/server.py` has no authentication or authorization code.

**Verified Fact.** The inherited `compose.yaml` has no service on port 8091 or 8092.

**Verified Fact.** `pyproject.toml` lists no FastAPI, React, LangGraph, or OPA dependency. Those names appear in `Execution_Plan.md` as later-phase choices. They are not current-state inventory.

**Unknown.** Whether Java or Node is installed on this laptop. Those tools were not run.

## Material finding

**Finding.** The current application is a Python 3.10+ standard-library HTTP service on SQLite, with optional Java and JavaScript side programs.
**Evidence.** `pyproject.toml`, `app/server.py`, `Dockerfile`, `legacy_java/ReconcileLegacy.java`, `legacy_js/legacy_policy.js`.
**Impact.** Baseline measurement can run offline on this laptop.
**Risk.** The GitHub verify workflow includes `python -m app.generate --count 6000 --seed 4552 --reset`. Running that workflow against this working copy would replace the packaged 125-case database.
**Confidence.** High.
**Open questions.** Docker support on this laptop is Unknown.

## What this file does not do

This file lists what is here. It does not pick a future stack.
