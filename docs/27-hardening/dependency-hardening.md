# Dependency hardening

| Field | Value |
|---|---|
| Stage | Phase 13 / 27 Hardening. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-27a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No hardening code in this half. |
| Evidence sources | FD-13; FD-15; FD-19; `requirements-platform.txt`; `Dockerfile.platform`; `.github/workflows/verify.yml`; `apps/app_a/agent/opa_client.py`; `docs/24-security-privacy/attack-surface-map.md` |
| Assumptions | Platform installs stay `python -m pip install -r requirements-platform.txt`. `MODEL_MODE=replay`. Half B does not pin ranges. |
| Unresolved issues | A lock file with hashes stays absent. Open Policy Agent binary hash stays Unknown. Image scan stays unrun. |
| Residual risks | Lower-bound pins such as `fastapi>=0.110` can install a later version on the next CI run. That drift is unmeasured. |

This file names the declared Python packages, the image base, and the optional Open Policy Agent binary. Open Policy Agent is the policy checker that returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK. The one Half B control is SC-27-01. This half does not pin packages and does not add a scanner.

Engineering decision ED-P13-27A-04 continued, authority: team-force. The first-cut inventory is `requirements-platform.txt` plus `python:3.12-slim` plus the optional local `opa` binary. Observed laptop versions below are one machine on 2026-10-18. They are not a signed lock file.

---

## Finding

**Finding.** `requirements-platform.txt` lists nine packages. Three LangGraph lines are pinned. Six lines are lower bounds. CI installs that file on Python 3.12. This laptop's `importlib.metadata` on 2026-10-18 read `fastapi=0.128.2`, `uvicorn=0.48.0`, `httpx=0.28.1`, `pytest=9.0.2`, `PyYAML=6.0.3`, `jsonschema=4.26.0`, `langgraph=1.0.3`, `langgraph-checkpoint=3.0.1`, `langgraph-checkpoint-sqlite=3.0.1`. Honesty: REAL for this machine. A later machine can differ. Half B leaves the file unpinned. Half B changes the missing-key response.
**Evidence.** `requirements-platform.txt`. `.github/workflows/verify.yml` setup-python 3.12. `importlib.metadata` on 2026-10-18.
**Impact.** Reviewer can compare a later `pip` list to this table. No version is published as a Business Owner target.
**Risk.** Treating the laptop versions as a lock file would hide CI drift.
**Confidence.** High on the declared file. Medium on this laptop's versions. Unknown on another machine.
**Open questions.** HALF_A_ACCEPTED. OPA hash. Image scan.

---

## Locked facts this design applies

**Verified Fact.** FD-13. GitHub Actions at the capstone root. `verify.yml` already runs characterization tests, lake tests, platform tests, and `docker compose config`.

**Verified Fact.** FD-15. Recursion limit 12, step budget 8, max tool calls 8, max gather visits 3. Those numbers are engineering defaults. A later measured quality percent stays Unknown.

**Verified Fact.** FD-19. This half invents no cost floor for a package upgrade.

---

## Declared packages

**Verified Fact** of `requirements-platform.txt`.

| Line in the file | Constraint | Observed on this laptop 2026-10-18 | Label |
|---|---|---|---|
| `fastapi>=0.110` | Lower bound | 0.128.2 | REAL on this machine. Not a lock |
| `uvicorn>=0.27` | Lower bound | 0.48.0 | REAL on this machine. Not a lock |
| `httpx>=0.27` | Lower bound | 0.28.1 | REAL on this machine. Not a lock |
| `pytest>=8.0` | Lower bound | 9.0.2 | REAL on this machine. Not a lock |
| `pyyaml>=6.0` | Lower bound | PyYAML 6.0.3 | REAL on this machine. Not a lock |
| `jsonschema>=4.0` | Lower bound | 4.26.0 | REAL on this machine. Not a lock |
| `langgraph==1.0.3` | Pin | 1.0.3 | REAL |
| `langgraph-checkpoint==3.0.1` | Pin | 3.0.1 | REAL |
| `langgraph-checkpoint-sqlite==3.0.1` | Pin | 3.0.1 | REAL |

Worked example. CI can install FastAPI 0.128.2 today and a later 0.129 on the next run. Both satisfy `>=0.110`. This half does not change that line.

Transitive packages pulled by those nine lines stay unlisted here. The first-cut SBOM in `sbom-summary.md` says the same. A full tree stays Unknown until a generator runs.

---

## Image and optional binary

| Component | What the file says | Hash | Label |
|---|---|---|---|
| Platform image base | `FROM python:3.12-slim` in `Dockerfile.platform` | Unknown | Verified Fact of the tag. Digest Unknown |
| Inherited workshop image | `FROM python:3.12-slim` in the workshop `Dockerfile` | Unknown | Same |
| Open Policy Agent binary | Used when present. Python fallback in `opa_client.py` when absent | Unknown | Phase 10 recorded a local path and version 1.21.2 on one machine. This half does not invent a hash |

Phase 12 named "pin and hash" for `opa` as later work. A hash without a measured file is invented. This half leaves the hash Unknown.

---

## Failure modes and recovery

| Id | Failure | What happens | Recovery |
|---|---|---|---|
| FM-27-08 | A lower-bound install pulls a later version | CI or a laptop can change behaviour | Read the installed version. Compare to this table. Pin only after a named finding |
| Missing `opa` binary | `evaluate()` uses the local Python rules | Record the engine name. Verdict strings stay EXECUTE, HOLD_FOR_REVIEW, or BLOCK | Install `opa` if the person wants the binary engine. The fallback stays |
| `pip install` fails | CI job `test` fails | Fix the constraint or the index. Re-run `verify.yml` | Unknown minutes |

A broken install is visible as a failed CI job. It is not parked in a dead-letter queue.

---

## Dead-letter queue and replay

Dependency install failures stay in CI logs. They are not intake messages.

Language-model replay stays `MODEL_MODE=replay`. **Verified Fact.** FD-19.

---

## Runbook — record what is installed

1. Run `python -c` with `importlib.metadata` for the nine names, or run `python -m pip freeze`.
2. Write the versions into the Half B evidence if they differ from this table.
3. Do not invent a CVE from a version string.
4. If `opa` is on PATH, record `opa version` as REAL. If it is absent, record absent.

A copy of this runbook into `operations/` belongs to sub-stage 29.

---

## SLOs and observability

CI already prints pytest results. That output proves the install ran. It does not prove an availability percent.

Time to install stays Unknown. Cost of CI minutes stays Unknown.

---

## Cost and the 0C envelope

Package versions belong to the install list. Token lines B2 to B7 stay Unknown. This half claims no dollar benefit from pinning or from leaving a range.

---

## Exact Half B check HB-27-01

The same check as `identity-rbac-hardening.md`.

Dependency assertion after Half B: `requirements-platform.txt` is unchanged. `test_application_source_has_no_key_literal` still passes. Half B does not add a lock file. Half B does not add a scanner job.

---

## What this file does not do

This file does not write SC-27-01. It does not start Half B. It does not pin the six lower bounds. It does not invent an Open Policy Agent hash. It does not invent a CVE. It does not sign a Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
