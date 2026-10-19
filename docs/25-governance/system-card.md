# System card

| Field | Value |
|---|---|
| Stage | Phase 12 / 25 Governance and assurance. Half B evidence. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-25b-doc-20261018-001 |
| Status | MEASURED. HB-25-01, HB-25-04, HB-25-05, and HB-25-09 recorded. Classification stays unsigned. BO-10 stays PROPOSED. |
| Evidence sources | FD-06; FD-13; FD-18; BO-10; BO-03; BO-09; `compose.yaml`; `docs/24-security-privacy/threat-model.md`; `docs/23-human-control/autonomy-matrix.md`; `docs/20-application/deterministic-ai-boundary.md`; `context-lake/generated/app-b-pin.json`; `Decision_Tracker.md`; directory listing of `docs/25-governance/` |
| Assumptions | BO-10 working answer holds. `MODEL_MODE=replay`. Documents stay unsigned. Named people stay Unknown. |
| Unresolved issues | Retention days stay Unknown. Company titles stay Unknown. Azure live behaviour stays Unknown. Port 8080 identity stays Phase 13. Named signer stays Unknown. Percent floors stay Unknown. |
| Residual risks | Calling this card a certificate would invent a compliance pass. Binding port 8080 to a public address would expose the synthetic case list. |

This card describes the Fabpulse exception-review system as built on this laptop. Application A listens on host port 8100. Application B listens on host port 8110. The Context Lake is the SQLite knowledge store on ports 8091 and 8092. This card issues no compliance certificate.

Engineering decision ED-P12-25A-05 continued, authority: team-force. System card id `SCARD-25-01`. Half B recorded the compose, pin, and unsigned-classification cells.

---

## Finding

**Finding.** Two applications, one pinned lake, one agent graph, one policy checker, and one audit file form the in-scope system. People at RT-01 to RT-06 record writes. Replay sentences are PRECOMPUTED. Live Azure stays NEEDS_HUMAN. BO-10 stays unsigned. Half B confirmed Compose still publishes 8100, 8110, 8091, and 8092 with `MODEL_MODE=replay`, the pin hash still matches, BO-10 stays PROPOSED, and this folder has no certificate file.
**Evidence.** FD-06. FD-13. FD-18. Compose host ports 8080, 8090, 8091, 8092, 8100, 8110. Lake pin 1.0.0. HB-25-01, HB-25-04, HB-25-05, and HB-25-09 Recorded sentences.
**Impact.** The reviewer can match this card to running compose names and to the pin hash.
**Risk.** Adding a new listener in this half would add a feature.
**Confidence.** High on the laptop topology and on the four file reads. Unknown on a later hosted environment.
**Open questions.** BO-10 signer. Retention days. Azure live behaviour.

---

## Card identity

| Field | Value | Label |
|---|---|---|
| Card id | SCARD-25-01 | Engineering decision |
| Name | Fabpulse exception-review system | Engineering decision |
| Lake version | 1.0.0 | Verified Fact. HB-25-09 REAL |
| Lake pin hash | `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` | REAL. HB-25-09 |
| Prompt semver | 1.0.0 | Verified Fact |
| `MODEL_MODE` | `replay` | Verified Fact. HB-25-01 REAL |
| Classification | Internal and synthetic. Process data confidential. No personal data | Verified Fact of BO-10 working answer, still PROPOSED. HB-25-04 REAL |

---

## What the system does

**Verified Fact.** FD-04. FD-06. Scenarios 7 to 11.

The system ranks a queue in code. It explains conflicts with a cited sentence. It flags recipe mismatch, replay duplicates, clock disagreement, and overlapping policies. It pauses for a person before a record-changing action. Application B takes pass, fail, or wait from the pinned lake. Application A still uses transformed code for those rule jobs and uses the lake for citations.

Worked example. Scenario 7 lists 67 packaged REPLAY rows. Honesty: REAL. RT-05 confirms a drop. The model does not drop the row.

---

## Parts in scope

**Verified Fact.** `compose.yaml`. FD-13.

| Part | Host port or path | What it does |
|---|---|---|
| Application A | 8100 | Queue, case, query, recovery, approvals, agent run, audit read |
| Application B | 8110 | Same route families. Rules from the lake. Lineage read |
| Lake REST | 8091 | `search_items`, `get_item`, `get_links`, `rule_at` |
| Lake MCP | 8092 | The same four lake reads over MCP |
| Open Policy Agent | in-process `opa eval` on `policy/opa/app_a.rego` | Returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK |
| Audit file | `apps/app_a/audit/audit_chain.sqlite3` | One row per agent step and per human approval |
| Replay store | `operations/model-replay/` | PRECOMPUTED sentences |
| Packaged operational store | inherited `data/legacy.sqlite3` opened `mode=ro` | Synthetic cases and lots |
| Packaged enterprise store | inherited `enterprise_legacy.sqlite3` opened `mode=ro` | Synthetic archive objects |

Legacy listener port 8080 and source-gateway port 8090 stay on the laptop compose. They have no identity check. They stay a residual for Phase 13. They are out of the write path for Application A and Application B.

---

## Users and owners

**Verified Fact.** BO-09. Accountability map.

Intended users are demo actors `demo-rt01-1` through `demo-rt06-1` with roles RT-01 to RT-06. Company job titles stay Unknown. Named people stay Unknown.

| Duty | Owner |
|---|---|
| Live write | RT-01 to RT-06 by `action_type` |
| INC-2025-014 owner | Unknown until RT-06 assigns a supplied name |
| Classification sign-off | Business Owner. Unsigned |
| Engineering change | Team-Force |
| Industry role names | FDE SME |

The model is a drafter. The model is not a user of record. The model is not an approver.

---

## Data and privacy handling

**Verified Fact** of the BO-10 working answer. Status PROPOSED. Unsigned.

| Rule | What the system does |
|---|---|
| Internal and synthetic | Packaged SQLite, documents, and lake items stay on this laptop |
| Process data is confidential | Recipe, hold, feed, and policy fields stay in the local stores and in audit rows for the demo |
| No personal data | Actor fields use laptop demo ids. Company staff names stay Unknown |
| Untrusted text | Feed notes and document bodies stay data. Injection BLOCK drives no action |

Retention days stay Unknown. Encryption-at-rest product choice stays Phase 13.

Worked example. Actor `demo-rt03-1` is a laptop label. It is not a company staff record.

---

## Human control and failure handling

**Verified Fact.** BO-03 working answer. FD-16. FD-18. FD-23.

| Event | What the system does |
|---|---|
| Record-changing proposal | `interrupt()` waits. Person at the mapped RT role resumes |
| Injection text plus write-from-text | BLOCK. HTTP 409. No approval wait. No record write |
| AI answer with no lake item | Rewrite to ABSTAIN or require a retrieved id |
| Replay miss | Abstain. No invented sentence |
| Silent threshold | HOLD_FOR_REVIEW. No compiled cutoff |
| Same person proposes and approves | HTTP 403 or OPA-R-07 BLOCK |
| Invented INC owner | OPA-R-09 BLOCK. Owner stays Unknown |

Audit rows join on correlation id. Phase 10 scenario 8 under `corr-p10b-doc-20261018-001` wrote 12 rows. Honesty: REAL.

---

## AI systems inside this card

| Register id | Role in this system |
|---|---|
| SYS-AI-01 | Application A drafts |
| SYS-AI-02 | Application B drafts |
| SYS-AI-03 | Agent graph on 8100 |
| SYS-AI-04 | Rejected. Not deployed |
| SYS-AI-05 | Replay files. PRECOMPUTED |
| MC-25-01 | Model card for the language path |

Live Azure stays NEEDS_HUMAN.

---

## Residual risks this card accepts

| Residual | Why it stays | Later home |
|---|---|---|
| Port 8080 case GET has no identity check | Baseline characterization. CT-35 HTTP 200 with no header. Honesty REAL | Phase 13 |
| Port 8090 fixture is ungated | Fixture only | Phase 13 |
| Retention days Unknown | No signed count | Business Owner |
| BO-10 unsigned | Accepted PROPOSED | Business Owner signature |
| Live Azure unmeasured | `MODEL_MODE=replay` | NEEDS_HUMAN rehearsal |
| Percent floors Unknown | FD-18 | Sub-stage 26 records counts. Floors stay Unknown unless a later FD sets one |

---

## Half B evidence this file names

| Check | What Half B records | Honesty when recorded |
|---|---|---|
| HB-25-01 | Compose still publishes 8100, 8110, 8091, 8092 and sets `MODEL_MODE: replay` | REAL |
| HB-25-04 | This card still shows BO-10 PROPOSED and unsigned | REAL |
| HB-25-05 | This folder still contains no certificate file | REAL |
| HB-25-09 | Pin hash still matches the value in this card | REAL |

### Recorded

Recorded 2026-10-18 under `corr-p12-25b-doc-20261018-001`. Half B did not add a listener. Half B did not sign this card.

HB-25-01. `compose.yaml` publishes host ports 8100, 8110, 8091, and 8092. Service `app-a` line 122 and service `app-b` line 152 set `MODEL_MODE: ${MODEL_MODE:-replay}`. Honesty: REAL.

HB-25-04. This card still shows BO-10 PROPOSED and unsigned. `Decision_Tracker.md` row BO-10 status is PROPOSED. Named signer stays Unknown. Honesty: REAL.

HB-25-05. Directory `docs/25-governance/` contains seven markdown files and no certificate file. Honesty: REAL.

HB-25-09. `context-lake/generated/app-b-pin.json` has `lake_version` `1.0.0` and `sqlite_sha256` `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. That hash matches the value in this card. Honesty: REAL.

---

## What this file does not do

This file describes the laptop system. It issues no compliance certificate. It does not write sub-stage 26. It does not invent a signer.

STOP. Do not start sub-stage 26.
