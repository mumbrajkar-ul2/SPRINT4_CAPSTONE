# SBOM summary

| Field | Value |
|---|---|
| Stage | Phase 13 / 27 Hardening. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-27a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No SBOM file is generated in this half. |
| Evidence sources | FD-19; `requirements-platform.txt`; `Dockerfile.platform`; `compose.yaml`; `docs/24-security-privacy/attack-surface-map.md` AS-24-06; `importlib.metadata` on this laptop 2026-10-18 |
| Assumptions | First-cut inventory is the declared platform packages plus the two `python:3.12-slim` Dockerfiles plus the optional `opa` binary. Transitive packages stay Unknown until a generator runs. |
| Unresolved issues | CycloneDX or SPDX file stays absent. Image digest stays Unknown. Transitive tree stays Unknown. |
| Residual risks | Treating this table as a complete bill of materials would hide packages pulled by FastAPI and LangGraph. |

This file is the first-cut software bill of materials. A software bill of materials is the list of components this stack is built from. Phase 12 left supply-chain scanning and this list to Phase 13. This half writes the list from files on disk. It does not run a generator. It does not invent a CVE.

Engineering decision ED-P13-27A-04, authority: team-force. First-cut inventory ids `SBOM-27-01` to `SBOM-27-12`. Control SC-27-10 is this inventory. Half B does not generate a machine file. The one Half B code control stays SC-27-01.

---

## Finding

**Finding.** Twelve first-cut components cover the platform image, the inherited image, nine declared Python packages, and the optional Open Policy Agent binary. Observed versions on this laptop on 2026-10-18 are listed. Honesty: REAL for those nine reads. Image digests stay Unknown. Transitive packages stay Unknown. Half B leaves this inventory as design. Half B changes the missing-key response.
**Evidence.** `requirements-platform.txt`. `Dockerfile.platform` line 1. Workshop `Dockerfile` line 1. `importlib.metadata` on 2026-10-18.
**Impact.** Reviewer can count twelve named rows. A later generator can add hashes.
**Risk.** Copying a public CVE list into `vulnerability-disposition.md` would invent findings.
**Confidence.** High on the declared nine. Unknown on the image digest and the transitive tree.
**Open questions.** HALF_A_ACCEPTED. Generator format. Image digest.

---

## Locked facts this design applies

**Verified Fact.** FD-19. This half invents no cost floor for a component upgrade.

**Verified Fact.** BO-10 working answer, still PROPOSED. Packaged records are internal and synthetic. This inventory lists software, not case rows.

---

## First-cut inventory

Each row stands alone. `Observed version` is this laptop on 2026-10-18 unless the cell says Unknown.

| Id | Component | Source | Observed version | Hash or digest | Supplier path |
|---|---|---|---|---|---|
| SBOM-27-01 | Python base for platform | `Dockerfile.platform` `FROM python:3.12-slim` | Tag `3.12-slim` | Unknown | Docker Hub python image. Digest Unknown |
| SBOM-27-02 | Python base for legacy | Workshop `Dockerfile` `FROM python:3.12-slim` | Tag `3.12-slim` | Unknown | Same |
| SBOM-27-03 | fastapi | `requirements-platform.txt` | 0.128.2 | Unknown | PyPI |
| SBOM-27-04 | uvicorn | `requirements-platform.txt` | 0.48.0 | Unknown | PyPI |
| SBOM-27-05 | httpx | `requirements-platform.txt` | 0.28.1 | Unknown | PyPI |
| SBOM-27-06 | pytest | `requirements-platform.txt` | 9.0.2 | Unknown | PyPI |
| SBOM-27-07 | PyYAML | `requirements-platform.txt` as `pyyaml>=6.0` | 6.0.3 | Unknown | PyPI |
| SBOM-27-08 | jsonschema | `requirements-platform.txt` | 4.26.0 | Unknown | PyPI |
| SBOM-27-09 | langgraph | `requirements-platform.txt` pin `==1.0.3` | 1.0.3 | Unknown | PyPI |
| SBOM-27-10 | langgraph-checkpoint | `requirements-platform.txt` pin `==3.0.1` | 3.0.1 | Unknown | PyPI |
| SBOM-27-11 | langgraph-checkpoint-sqlite | `requirements-platform.txt` pin `==3.0.1` | 3.0.1 | Unknown | PyPI |
| SBOM-27-12 | Open Policy Agent binary | Optional local tool | Unknown on this half | Unknown | Record `opa version` when present |

Worked example. SBOM-27-03 FastAPI 0.128.2 was the version `importlib.metadata` returned on this laptop on 2026-10-18. A CI runner can install a different 0.12x that still matches `fastapi>=0.110`. Both facts can be true.

Application source under `apps/` and lake YAML under `context-lake/items/` are this project's own files. They are not third-party packages. They stay out of this twelve-row list.

Replay files under `operations/model-replay/` are PRECOMPUTED model JSON. They are not installable packages.

---

## Failure modes and recovery

| Failure | What happens | Recovery |
|---|---|---|
| Inventory row is missing a hash | The row still names the component | A later generator fills the hash. This half leaves it Unknown |
| A machine has a different FastAPI version | The observed cell on that machine differs from 0.128.2 | Record the new version as REAL. Do not invent a CVE |
| `opa` is absent | SBOM-27-12 stays Unknown or is recorded as absent | The Python fallback in `opa_client.py` still evaluates the named rules |

---

## Dead-letter queue and replay

An SBOM row is a list entry. It is not an intake message. Dead-letter parking stays sub-stage 28.

Language-model replay stays `MODEL_MODE=replay`. **Verified Fact.** FD-19.

---

## Runbook — refresh the first-cut list

1. Read `requirements-platform.txt`.
2. Read both Dockerfiles for the `FROM` line.
3. Read installed versions with `importlib.metadata` or `pip freeze`.
4. Update the observed-version cells. Label them REAL.
5. Leave hash cells Unknown until a generator or `pip hash` run exists.
6. Do not paste a public vulnerability bulletin into this table.

A machine-readable CycloneDX or SPDX file stays later. This half does not pick a generator.

---

## SLOs and observability

CI proving `pip install -r requirements-platform.txt` succeeded is the install signal. Count of listed components is 12. Twelve is how many rows this list has. An availability percent stays Unknown.

---

## Cost and the 0C envelope

Listing a package adds no token. Token lines B2 to B7 stay Unknown. This half claims no dollar benefit from having twelve named rows.

---

## Exact Half B check HB-27-01

The same check as `identity-rbac-hardening.md`.

SBOM assertion after Half B: this file still has twelve first-cut rows. Half B does not emit `sbom.json`. Half B does not add a CI generator step.

---

## What this file does not do

This file does not write SC-27-01. It does not start Half B. It does not generate CycloneDX. It does not invent a CVE or a digest. It does not sign a Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
