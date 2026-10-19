# AI system register

| Field | Value |
|---|---|
| Stage | Phase 12 / 25 Governance and assurance. Half B evidence. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-25b-doc-20261018-001 |
| Status | MEASURED. Register evidence cells for HB-25-01, HB-25-02, HB-25-03, HB-25-08, HB-25-09, and HB-25-10 recorded 2026-10-18. Live Azure stays NEEDS_HUMAN. |
| Evidence sources | FD-04; FD-05; FD-13; FD-14; FD-15; FD-18; `docs/19-intelligence/prompt-registry.md`; `docs/19-intelligence/model-configuration.md`; `docs/08-ai-qualification/qualification-decision.md`; `compose.yaml`; `operations/model-replay/README.md`; `context-lake/generated/app-b-pin.json`; `apps/app_a/prompts/`; `apps/app_b/prompts/`; `apps/` file scan |
| Assumptions | `MODEL_MODE=replay` stays the Compose default. Replay sentences stay PRECOMPUTED. Live Azure stays NEEDS_HUMAN. |
| Unresolved issues | Azure endpoint, deployment name, and API version stay Unknown. Token cost stays Unknown. Named operator stays Unknown. Percent floors stay Unknown. |
| Residual risks | Listing the rejected hold predictor as an in-use system would hide FD-05. Treating replay files as a live Azure pass would skip FD-13. |

This file lists every AI system this capstone uses, plus the one ML job this capstone rejected. The Context Lake is the SQLite knowledge store built in Phase 5. This file issues no compliance certificate.

Engineering decision ED-P12-25A-03, authority: team-force. Register ids `SYS-AI-01` to `SYS-AI-05`. Half B copied these rows into the evidence cells on 2026-10-18. Half B did not add a sixth in-use model.

---

## Finding

**Finding.** Three in-use AI paths share replay files and three prompt ids. One replay store supplies PRECOMPUTED sentences. One hold predictor stays rejected and undeployed. Live Azure stays NEEDS_HUMAN. Half B confirmed Compose still defaults `MODEL_MODE` to `replay`, named one replay file, found no `engineering_hold` model file under `apps/`, matched the lake pin hash, and found the three prompt ids at semver 1.0.0.
**Evidence.** FD-04. FD-05. Prompt registry semver 1.0.0. Compose `MODEL_MODE=replay`. Recorded paragraph under this file.
**Impact.** The reviewer can tick each row against files on disk. The model card and the system card reuse these ids.
**Risk.** Calling Azure from a Half B check would leave replay.
**Confidence.** High on the five ids and on the six recorded checks. Unknown on Azure deployment name.
**Open questions.** Azure rehearsal. Azure endpoint. Azure deployment name. Azure API version.

---

## How to read a row

Each row stands alone. `Status` is `in use`, `supporting store`, or `rejected`. `Owner of change` is who may edit the path. `Owner of a write` is who records a case change. Named people stay Unknown.

Worked example. SYS-AI-01 drafts a cited sentence for scenario 8. RT-03 records hold. The register row stays `in use` under replay. The write owner stays RT-03.

---

## Register

| Id | System | What it does | Status | Model path | Owner of change | Owner of a write | Data it may see |
|---|---|---|---|---|---|---|---|
| SYS-AI-01 | Application A GenAI path | Drafts cited sentences for conflict explanation, natural-language query, and a read-only plan | in use | `MODEL_MODE=replay` reads `operations/model-replay/{sha256}`. Prompts P-EXPLAIN-CONFLICT, P-NL-QUERY, P-DRAFT-PLAN at 1.0.0 | Team-Force | RT-01 to RT-06 on a record change. The model writes nothing | Retrieved lake items, case fields, untrusted quotes marked as data |
| SYS-AI-02 | Application B GenAI path | Same three prompt ids. Rules come from the pinned lake. Pass, fail, or wait come from lake cards | in use | Same replay store. `apps/app_b/intelligence/generate.py` opens no Azure socket | Team-Force | RT-01 to RT-06 on a record change. The model writes nothing | Pinned lake version 1.0.0. No inherited-repo path |
| SYS-AI-03 | Agent graph `app_a_investigate` | Gathers with six read-only tools, calls Open Policy Agent, then waits on `interrupt()` | in use | Uses SYS-AI-01 for `plan_draft`. Write-tool list is empty | Team-Force | Person at the mapped RT role after OPA HOLD_FOR_REVIEW or EXECUTE | Case, lake reads, OPA input. Injection sets BLOCK |
| SYS-AI-04 | `engineering_hold` predictor | Would guess hold from lot fields | rejected | No model file. FD-05 Reject ML. Majority and leave-one-out both 117/125 | Team-Force records the reject | RT-03 already owns hold | None. No production model is built |
| SYS-AI-05 | Replay file store | Returns a saved sentence for a SHA-256 of the prompt bytes | supporting store | Files under `operations/model-replay/`. Missing file returns `replay_miss` | Team-Force | None. A miss abstains. The store does not write a case | Prompt bytes only |

Worked example for SYS-AI-04. Packaged `wafer_lots` has 125 lots. 8 have `engineering_hold = 1`. Honesty: REAL. Logistic regression scored 117 of 125. Majority scored 117 of 125. No hold model ships.

Worked example for SYS-AI-05. Prompt bytes `phase8-replay-fixture-prompt` hash to `adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7`. That file holds a PRECOMPUTED unit-test body. It is not a live Azure answer.

---

## What is out of the register as an AI system

These stay off the in-use AI list. They are deterministic code.

| Job | Why it is off the AI list |
|---|---|
| Queue ranking | `priority()` is code. FD-04 |
| Rule pass-or-fail | `evaluate_live_policy()` is code. Application B reads lake cards |
| Reconciliation and REPLAY mark | Identifier and status tests |
| Lake FTS5 search | Retrieval is code. It feeds SYS-AI-01 and SYS-AI-02 |
| Open Policy Agent | Policy checker. Three verdict strings |
| Legacy listener on port 8080 | Baseline fixture. No model |

---

## Purpose, users, and stop rules

**Verified Fact.** FD-04. FD-14. FD-18. BO-03 working answer.

| Id | Intended purpose | Intended users | Stop rule |
|---|---|---|---|
| SYS-AI-01 | Explain a conflict. Answer a golden or free-text question. Draft a plan | A caller with RT-01 to RT-06 headers on port 8100 | Cite a retrieved lake item or abstain. Injection BLOCK. Replay miss abstains |
| SYS-AI-02 | Same three draft jobs, with rules from the lake | A caller with the same headers on port 8110 | Same cite-or-abstain rule. No inherited-repo read |
| SYS-AI-03 | Gather facts and pause for a person | Same 8100 caller | `recursion_limit` 12. Step budget 8. Empty write list. OPA BLOCK drives no action |
| SYS-AI-04 | None. Rejected | None | Stay undeployed |
| SYS-AI-05 | Play back a saved sentence | Application A or Application B in process | Missing hash returns `replay_miss`. No invented sentence |

Live Azure for SYS-AI-01 and SYS-AI-02 stays NEEDS_HUMAN. Azure endpoint, deployment name, and API version stay Unknown.

---

## Change, monitor, and retire

Engineering decision ED-P12-25A-08, authority: team-force. These criteria are the working register rules. They are not a signed statute.

| Event | What happens | Who |
|---|---|---|
| Prompt wording change | Raise prompt semver. Rewrite replay files. Re-run the freeze set | Team-Force |
| Lake meaning change | Raise lake version with an ADR. Refresh the Application B pin | Team-Force |
| Add a write tool | Forbidden under FD-02 and BO-03 working answer unless a later signed row changes that | Business Owner for agency. Team-Force for the tool list |
| Live Azure rehearsal | Person sets `MODEL_MODE=azure` and supplies a key. Pause NEEDS_HUMAN until then | Human who holds the key |
| Retire SYS-AI-04 | Already retired by FD-05 | Team-Force |
| Retire a prompt id | Major semver drop plus an ADR. Freeze set must drop that job | Team-Force |

Monitor counts already exist: freeze 42 of 42, injection BLOCK runs, audit rows per correlation id. Percent floors stay Unknown. Sub-stage 26 records the next eval numbers.

---

## Half B evidence this file names

Half B fills the `Recorded` column. Design cells stay as written.

| Check | What Half B records | Honesty when recorded | Recorded 2026-10-18 |
|---|---|---|---|
| HB-25-01 | `compose.yaml` still sets `MODEL_MODE: replay` on Application A and Application B | REAL | `app-a` line 122 and `app-b` line 152 set `MODEL_MODE: ${MODEL_MODE:-replay}` |
| HB-25-02 | At least one replay file exists. README still labels fixture bodies PRECOMPUTED | REAL path. PRECOMPUTED body | Path `operations/model-replay/adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7` exists. README still says PRECOMPUTED |
| HB-25-03 | Azure endpoint, deployment name, and API version stay unset or Unknown. Live row stays NEEDS_HUMAN | REAL | Process env unset. No `AZURE_` key in `compose.yaml`. Live Azure stays NEEDS_HUMAN. Those three names stay Unknown |
| HB-25-08 | No `engineering_hold` model file exists under `apps/` | REAL | No model-weight file under `apps/`. No filename contained `engineering_hold`. SYS-AI-04 stays rejected |
| HB-25-09 | Pin still shows lake 1.0.0 and hash `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` | REAL | `lake_version` `1.0.0`. `sqlite_sha256` `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` |
| HB-25-10 | Three prompt files exist at semver 1.0.0 | REAL | Six files at semver `1.0.0`: the three ids on Application A and the same three ids on Application B. Each has `allowed_tools` `[]` |

### Recorded

Register-entry timestamp 2026-10-18. Correlation id `corr-p12-25b-doc-20261018-001`. Half B did not add SYS-AI-06. Half B did not call Azure.

SYS-AI-01 and SYS-AI-02 stay in use under `MODEL_MODE=replay`. SYS-AI-03 stays in use with an empty write-tool list. SYS-AI-04 stays rejected. SYS-AI-05 stays the supporting replay store. Replay sentences stay PRECOMPUTED. Live Azure stays NEEDS_HUMAN.

---

## What this file does not do

This file lists the five register ids. It issues no compliance certificate. It does not write sub-stage 26. It does not invent an Azure deployment name.

STOP. Do not start sub-stage 26.
