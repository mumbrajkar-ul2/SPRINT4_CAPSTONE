# Attack-surface map

| Field | Value |
|---|---|
| Stage | Phase 12 / 24 Security, privacy, responsible AI. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-24a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No security code in this half. |
| Evidence sources | `Project_Intent.md` section 12.1; `compose.yaml`; `docs/10-architecture/security-architecture.md`; `docs/17-implementation-prd/implementation-prd.md` identity section; `apps/app_a/agent/`; `apps/app_b/`; `policy/opa/`; `context-lake/eval/injection-corpus.yaml` |
| Assumptions | Host ports stay 8080, 8090, 8091, 8092, 8100, 8110. Applications do not call each other at run time. `MODEL_MODE=replay`. |
| Unresolved issues | Supply-chain scanning and SBOM stay Phase 13. Operations runbooks stay Phase 13. Live Azure surface stays unmeasured. |
| Residual risks | Port 8080 and port 8090 stay reachable without identity. A later public bind of those ports would expose the synthetic case list. |

This file maps each Project Intent surface onto the listeners and files that exist on this laptop. A surface is a place an attacker or a mistaken caller can reach.

Engineering decision ED-P12A-01 continued, authority: team-force. Surface ids `AS-24-01` to `AS-24-07`.

---

## Finding

**Finding.** Seven surfaces from `Project_Intent.md` section 12.1 map onto six host ports, the agent graph, the replay files, and the two SQLite sidecar files. The Half B change sits on surface AS-24-04 (language-model retrieval) and AS-24-05 (agents and tools). It does not add a listener.
**Evidence.** Intent table 12.1. `compose.yaml` port list. FD-13. FD-15. FD-16. FD-18.
**Impact.** Half B can name the file it will edit without inventing a new port.
**Risk.** Treating port 8080 as already gated would hide CT-35.
**Confidence.** High on the port map. Unknown on a future public bind.
**Open questions.** Phase 13 identity on 8080. HALF_A_ACCEPTED.

---

## Surface map

**Verified Fact.** Intent 12.1. Mapping onto locked components is Inference from that table plus the compose file.

### AS-24-01 Application and APIs

Representative threats from Intent: broken access control, injection, insecure object access, tenant or site leakage.

| Piece | Port or path | Identity now | Linked threat |
|---|---|---|---|
| Application A FastAPI | 8100 `/api/*` | `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` on case routes | TM-24-03, TM-24-01 |
| Application A health and UI | 8100 `/health`, static GET | Open | Read of health JSON |
| Application B FastAPI | 8110 `/api/*` | Same three headers | TM-24-03 |
| Legacy workshop listener | 8080 `/api/cases` | None | TM-24-12 |
| Shared identity helper | `apps/shared/identity.py` | Closed list RT-01 to RT-06 | TM-24-03, TM-24-04 |

Worked example. `GET /api/cases/CASE-1` on 8100 with no headers is HTTP 401 `missing_identity`. Honesty of that Phase 8 probe: REAL. The same GET on 8080 returns HTTP 200 with no header (CT-35). Honesty: REAL. FD-18 keeps access on 8100 and 8110 as RT-01 to RT-06. It does not add a new attribute-based product. Site code stays a data field on the case.

### AS-24-02 Data and documents

Representative threats: sensitive-data exposure, tampering, retention failure, untrusted text.

| Piece | Path | Trust label | Linked threat |
|---|---|---|---|
| Packaged cases and lots | `data/legacy.sqlite3` | Synthetic, internal, confidential process data | TM-24-11 |
| Enterprise objects | `data/enterprise_legacy.sqlite3` | Same. IC-06 payloads in `evidence_events.payload` | TM-24-01, TM-24-11 |
| Partner feeds | `partner_feeds.raw_json` | 86 rows with auto-approve or disregard-validation language. Honesty REAL | TM-24-01 |
| Archive email | `data/archive_documents/*.eml` | IC-03. 3 files. Honesty REAL | TM-24-01 |
| Archive HTML | `data/archive_documents/*.html` | IC-05. 2 files. Honesty REAL | TM-24-01 |
| Source documents | `data/documents/source_documents.jsonl` | IC-04. 22 rows. Honesty REAL | TM-24-01 |
| Context Lake | `context-lake/context-lake.sqlite3` | Runtime read-only. `build.py` writes | TM-24-07 |
| Audit chain | `apps/app_a/audit/audit_chain.sqlite3` | Demo actor ids. Retention Unknown | TM-24-11 |

**Verified Fact** of BO-10 working answer. Packaged rows do not contain personal data. Demo actor ids such as `demo-rt01-1` are laptop labels.

### AS-24-03 Integration

Representative threats: replay, duplicate, schema downgrade, spoofed source, delayed messages.

| Piece | Port or path | Control now | Linked threat |
|---|---|---|---|
| Source gateway | 8090 | Ungated fixture | TM-24-09 |
| Gateway bridge | compose service | Limit 50 in compose | Schema and replay stay visible as data |
| Application A recovery | `GET /api/recovery` | Identity required. User-visible retry | Scenario 11 |
| Replay duplicate rule | `rule.feed.replay_duplicate` | Drop waits for RT-05 | TM-24-09 |

Worked example. 67 packaged rows have `processing_status=REPLAY`. Honesty: REAL. Drop waits for RT-05. The model does not drop the row.

### AS-24-04 Language-model retrieval

Representative threats: prompt injection, unsupported output, data leakage, stale context.

| Piece | Path | Control now | Linked threat |
|---|---|---|---|
| Retrieve | `apps/app_a/intelligence/retrieve.py` | Calls lake `injection_block` on untrusted items | TM-24-01 |
| Generate | `apps/app_a/intelligence/generate.py` | Replay. `WRITE_TOOLS` empty | TM-24-02 |
| Ground | `apps/app_a/intelligence/ground.py` | Cite or abstain. `check_claim` | TM-24-06 |
| Prompts | `apps/app_a/prompts/*.v1.0.0.json` | Harvested text is data. `allowed_tools` empty | TM-24-01 |
| Freeze eval | `apps/app_a/eval/run_freeze.py` | 42 of 42 cited or abstained. Injection 8 of 8 `block: true` | TM-24-01, TM-24-06 |

Worked example. GQ-18 and IC-01 through IC-06 set `block: true` on the freeze run. Honesty: REAL. Percent floor stays Unknown.

Half B SC-24-01 lives here and on AS-24-05: untrusted quotes plus a write-from-text action must set OPA `injection` even when the caller omits `corpus_id`.

### AS-24-05 Agents and tools

Representative threats: excess authority, tool misuse, runaway loops, hidden side effects.

| Piece | Path | Control now | Linked threat |
|---|---|---|---|
| Graph | `apps/app_a/agent/graph.py` `app_a_investigate` | Named nodes. Model only in `plan_draft` | TM-24-02 |
| Tools | `apps/app_a/agent/tools.py` | Six read names. Write list empty | TM-24-02 |
| Budget | `apps/app_a/agent/budget.py` | recursion_limit 12, step 8, tools 8, gather 3 | TM-24-08 |
| OPA client | `apps/app_a/agent/opa_client.py` | Builds the input. Evaluates `data.app_a.verdict` | TM-24-01, TM-24-10 |
| Checkpoint | `apps/app_a/runtime/checkpoints.sqlite3` | `thread_id` equals `correlation_id` | Restart keeps the wait |
| Application B agent route | `apps/app_b/routes/agent.py` | Lake `block_untrusted`. No write tool | TM-24-01, TM-24-02 |

Worked example. Phase 10 `test_no_write_tool_reaches_the_model` asserted six read names and an empty write list. Honesty: REAL.

### AS-24-06 Supply chain and platform

Representative threats: vulnerable images, secrets leakage, drift, unreviewed deployment.

| Piece | Path | Control now | What stays later |
|---|---|---|---|
| Compose | `compose.yaml` at capstone root | Seven named services. Healthchecks | Image scan, SBOM: Phase 13 |
| API key | `FABPULSE_API_KEY` from environment. Default named in `.env.example` as `local-demo-only` | Not hard-coded in application source | Rotation: Phase 13 |
| GitHub Actions | capstone root | Present from Phase 8 | Gated deploy: later |
| `opa` binary | Local path when present | `evaluate()` records the engine | Pin and hash: Phase 13 |

This half does not add a scanner. Residual: TM-24-12 style exposure if compose ports bind beyond the laptop.

### AS-24-07 Operations

Representative threats: weak detection, disputed ownership, unsafe recovery.

| Piece | Path | Control now | What stays later |
|---|---|---|---|
| JSON logs | stdout | FD-13 | SLO numbers: Phase 13, Unknown |
| Audit read | `GET /api/audit/{correlation_id}` | Identity required | Retention: Unknown |
| Incident INC-2025-014 | Case id | Owner Unknown. RT-06 assigns a supplied name | Named person stays Unknown |
| Recovery GET | `/api/recovery` | Visible retry and error class | RTO and RPO Unknown |

---

## Cross-surface traffic that must stay absent

**Verified Fact.** FD-06. Applications do not call each other at run time. Application B source has no inherited-repo path, no Application A rule import, and no call to port 8100. Phase 11 reviewer recorded those checks.

A caller who reaches 8100 still cannot use that hop to write the lake. Lake writes stay `build.py`.

---

## Where Half B touches the map

| Surface | File | Change after HALF_A_ACCEPTED |
|---|---|---|
| AS-24-04 and AS-24-05 | `apps/app_a/agent/nodes.py` `load_case` | Set `block` from untrusted quotes plus write-from-text |
| AS-24-04 and AS-24-05 | `apps/app_a/agent/opa_client.py` `build_opa_input` | Set `injection` from the same pair even when `corpus_id` is empty |
| AS-24-05 | `tests/platform/test_app_a_phase12_security.py` | HB-24-01 before-and-after |

No new port. No new header. No new role.

---

## What this file does not do

This file does not write code. It does not start Half B. It does not add identity to 8080. It does not invent a retention number.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
