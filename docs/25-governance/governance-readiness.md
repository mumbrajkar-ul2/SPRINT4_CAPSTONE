# Governance readiness

| Field | Value |
|---|---|
| Stage | Phase 12 / 25 Governance and assurance. Half B evidence. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-25b-doc-20261018-001 |
| Status | MEASURED. HB-25-01 to HB-25-10 recorded 2026-10-18. BO-10 stays PROPOSED. Replay sentences stay PRECOMPUTED. Live Azure stays NEEDS_HUMAN. |
| Evidence sources | This folder; `compose.yaml`; `operations/model-replay/README.md`; `operations/model-replay/adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7`; `.env.example`; `Decision_Tracker.md`; `apps/shared/identity.py`; `apps/app_a/agent/tools.py`; `apps/app_a/intelligence/generate.py`; `apps/app_b/intelligence/generate.py`; `apps/app_a/store.py`; `apps/app_b/fixtures/scenarios.yaml`; `context-lake/generated/app-b-pin.json`; `apps/app_a/prompts/`; `apps/app_b/prompts/`; packaged SQLite opened `mode=ro`; FD-18; BO-10 |
| Assumptions | Reviewer already returned HALF_A_ACCEPTED. `MODEL_MODE=replay`. Documents stay unsigned. This half adds no feature. |
| Unresolved issues | Statute applicability stays Unknown. Named signer stays Unknown. Company job titles stay Unknown. INC-2025-014 owner stays Unknown. Retention days stay Unknown. Percent floors stay Unknown. Azure endpoint, deployment name, and API version stay Unknown. |
| Residual risks | Marking this file as a signed compliance pack would invent a certificate. Starting sub-stage 26 in this half would skip the stage-25 reviewer. |

This file is the gate for spine unit 25. Half A named the ten checks. Half B recorded the values on 2026-10-18 under correlation id `corr-p12-25b-doc-20261018-001`. This file issues no compliance certificate.

---

## Finding

**Finding.** Half A named twelve working obligations, fourteen controls, six live-case roles, five register ids, one model card, and one system card. Half B then read the ten named checks from disk. Compose still defaults `MODEL_MODE` to `replay` on Application A and Application B. Replay file `operations/model-replay/adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7` exists. Replay sentence bodies stay PRECOMPUTED. Live Azure stays NEEDS_HUMAN. BO-10 stays PROPOSED. This folder has no certificate file. Packaged INC-2025-014 `owner_id` is empty. `CLOSED_ROLES` is RT-01 to RT-06. `WRITE_TOOLS` is empty. No `engineering_hold` model file sits under `apps/`. The lake pin is still version 1.0.0 with hash `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. The three prompt ids exist at semver 1.0.0.
**Evidence.** The Recorded table in this file. The six sibling files. Locked facts FD-18 and BO-10.
**Impact.** The coordinator can send this folder to the Half B reviewer.
**Risk.** Treating this file as a signed compliance pack would hide that BO-10 stays unsigned.
**Confidence.** High on the ten file reads. Unknown on statute fit and on a live Azure call.
**Open questions.** BO-10 signer. Company titles. Statute applicability. Retention days. Percent floors. Azure deployment name.

---

## Half A checklist

| Check | Status | Label |
|---|---|---|
| Working obligations OB-25-01 to OB-25-12 named | Pass in this half | Verified Fact of `compliance-obligations.md` |
| Statute families ST-25-01 to ST-25-05 left Unknown | Pass in this half | Engineering decision ED-P12-25A-07 |
| Controls GC-25-01 to GC-25-14 mapped to owners | Pass in this half | Verified Fact of `compliance-control-matrix.md` |
| Live-case owners use RT-01 to RT-06 | Pass in this half | Verified Fact of `accountability-map.md` |
| Named people stay Unknown | Pass in this half | Verified Fact |
| INC-2025-014 owner stays Unknown | Pass in this half | Verified Fact |
| Register ids SYS-AI-01 to SYS-AI-05 named | Pass in this half | Engineering decision ED-P12-25A-03 |
| Model card says replay sentences are PRECOMPUTED | Pass in this half | Verified Fact of `model-card.md` |
| Model card says live Azure is NEEDS_HUMAN | Pass in this half | Verified Fact of `model-card.md` |
| System card names the laptop parts and BO-10 | Pass in this half | Verified Fact of `system-card.md` |
| No certificate file in this folder | Pass in this half | Engineering decision ED-P12-25A-07 |
| Half B checks HB-25-01 to HB-25-10 named | Pass in this half | Engineering decision ED-P12-25A-04 |
| Measured register evidence | Recorded 2026-10-18 under `corr-p12-25b-doc-20261018-001` | REAL for the ten checks |
| Signed BO-10 | Out of this half | Unknown person. Document stays unsigned |

---

## Half B must record

These rows were open until Half B. Honesty on the recorded values is REAL except where a cell stays PRECOMPUTED or Unknown by design.

Engineering decision ED-P12-25A-04 continued, authority: team-force.

| Check | What Half B records | Where Half B writes it | Honesty when recorded |
|---|---|---|---|
| HB-25-01 | `compose.yaml` still sets `MODEL_MODE: replay` on Application A and Application B. Ports 8100, 8110, 8091, 8092 still published | `ai-system-register.md` and this file | REAL |
| HB-25-02 | At least one replay file path. README and the model card still label sentence bodies PRECOMPUTED | `model-card.md` | REAL path. PRECOMPUTED body |
| HB-25-03 | Azure endpoint, deployment name, and API version stay Unknown. Live Azure stays NEEDS_HUMAN | `model-card.md` | REAL |
| HB-25-04 | `Decision_Tracker.md` still shows BO-10 PROPOSED. No signer name in `docs/25-governance/` | `compliance-obligations.md` and this file | REAL |
| HB-25-05 | Directory listing of `docs/25-governance/` contains no certificate file | this file | REAL |
| HB-25-06 | Packaged `INC-2025-014` owner field is empty. Accountability map still says Unknown | `accountability-map.md` | REAL |
| HB-25-07 | `CLOSED_ROLES` is RT-01 to RT-06. `WRITE_TOOLS` is empty | `compliance-control-matrix.md` | REAL |
| HB-25-08 | No `engineering_hold` model file under `apps/` | `ai-system-register.md` | REAL |
| HB-25-09 | Pin still shows lake 1.0.0 and hash `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` | `ai-system-register.md` and `system-card.md` | REAL |
| HB-25-10 | Prompt files P-EXPLAIN-CONFLICT, P-NL-QUERY, and P-DRAFT-PLAN exist at semver 1.0.0 | `ai-system-register.md` | REAL |

### Recorded

Recorded 2026-10-18. Correlation id `corr-p12-25b-doc-20261018-001`. Half B added no feature. Half B did not sign BO-10. Half B did not invent a retention day count. Half B did not start sub-stage 26.

| Check | Recorded value | Honesty |
|---|---|---|
| HB-25-01 | `compose.yaml` service `app-a` line 122 sets `MODEL_MODE: ${MODEL_MODE:-replay}`. Service `app-b` line 152 sets the same default. Host ports still publish 8100, 8110, 8091, and 8092 | REAL |
| HB-25-02 | File `operations/model-replay/adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7` exists. Size 63 bytes. The folder holds 77 replay files besides `README.md`. `operations/model-replay/README.md` still labels fixture bodies PRECOMPUTED. The model card still labels replay sentence honesty PRECOMPUTED | REAL path. PRECOMPUTED body |
| HB-25-03 | Process environment has no `AZURE_OPENAI_ENDPOINT`, no `AZURE_OPENAI_DEPLOYMENT`, and no `AZURE_OPENAI_API_VERSION`. `compose.yaml` has no `AZURE_` key. `.env` is absent. `.env.example` has no Azure names and sets `MODEL_MODE=replay`. The model card still says live Azure is NEEDS_HUMAN. Endpoint, deployment name, and API version stay Unknown | REAL |
| HB-25-04 | `Decision_Tracker.md` row BO-10 status is PROPOSED. Search of `docs/25-governance/*.md` found no `Signed by`, `Signature:`, `I certify`, `certificate of`, or `Attested by` line. Named signer stays Unknown | REAL |
| HB-25-05 | Directory `docs/25-governance/` contains seven markdown files: `accountability-map.md`, `ai-system-register.md`, `compliance-control-matrix.md`, `compliance-obligations.md`, `governance-readiness.md`, `model-card.md`, `system-card.md`. None is named as a certificate | REAL |
| HB-25-06 | Packaged INC-2025-014 `owner_id` is empty. `apps/app_a/store.py` sets `owner_id` to None. `load_packaged()` returned `owner_id` None and `task_id` `T-00000000`. Enterprise table `workflow_tasks` row `T-00000000` has `assigned_to` None. Incident file `operations/incidents/INC-2025-014.md` ends "Follow-up owner unknown." Accountability map still says Unknown | REAL |
| HB-25-07 | `CLOSED_ROLES` in `apps/shared/identity.py` is exactly `('RT-01', 'RT-02', 'RT-03', 'RT-04', 'RT-05', 'RT-06')`. `WRITE_TOOLS` is `[]` in `apps/app_a/agent/tools.py`, `apps/app_a/intelligence/generate.py`, and `apps/app_b/intelligence/generate.py` | REAL |
| HB-25-08 | Search under `apps/` found no `.pkl`, `.joblib`, `.onnx`, `.pt`, `.pth`, `.h5`, `.sav`, `.model`, `.bin`, `.cbm`, or `.xgb` file. No filename contained `engineering_hold`. SYS-AI-04 stays rejected | REAL |
| HB-25-09 | `context-lake/generated/app-b-pin.json` has `lake_version` `1.0.0` and `sqlite_sha256` `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` | REAL |
| HB-25-10 | Six prompt files exist at semver `1.0.0`: `P-EXPLAIN-CONFLICT`, `P-NL-QUERY`, and `P-DRAFT-PLAN` under `apps/app_a/prompts/` and the same three ids under `apps/app_b/prompts/`. Each file has `allowed_tools` `[]` | REAL |

Worked example. HB-25-02. Half B named file `operations/model-replay/adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7`. Honesty of the path: REAL. Honesty of the body: PRECOMPUTED.

---

## What ready means in this half

Half B recorded the ten named checks. Register evidence cells that this half measured now hold those values.

The system is still not a signed compliance pack. BO-10 stays PROPOSED and unsigned. Replay sentences stay PRECOMPUTED. Live Azure stays NEEDS_HUMAN.

---

## What this file does not do

This file names the Half A gate and records the ten Half B checks. It issues no compliance certificate. It does not sign BO-10. It does not write sub-stage 26. It does not update `STATUS.md` or `Decision_Tracker.md`.

STOP. Do not start sub-stage 26.
