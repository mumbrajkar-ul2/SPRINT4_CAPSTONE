# Threat model

| Field | Value |
|---|---|
| Stage | Phase 12 / 24 Security, privacy, responsible AI. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-24a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No security code in this half. |
| Evidence sources | FD-18 DECIDED; BO-10 PROPOSED and accepted; `Project_Intent.md` section 12.1; `docs/10-architecture/security-architecture.md`; `docs/12-specs/business-rules.md`; `context-lake/eval/injection-corpus.yaml`; `policy/opa/app_a.rego`; `apps/app_a/agent/nodes.py`; `apps/app_a/agent/opa_client.py`; `apps/app_a/agent/tools.py`; `compose.yaml` |
| Assumptions | BO-10 working answer holds: all records are internal and synthetic; process data is confidential; packaged rows do not contain personal data. BO-03 working answer holds: a person approves every record-changing action. `MODEL_MODE=replay`. |
| Unresolved issues | Company job titles stay Unknown. Named people stay Unknown. Retention days stay Unknown. Numeric groundedness, citation, and abstention percent floors stay Unknown. BO-10 stays unsigned. |
| Residual risks | Port 8080 still serves case reads with no identity check. Port 8090 stays the ungated fixture. Those stay for Phase 13 identity hardening. A live Azure path is unmeasured. |

This file names the entry points, the trust boundaries, the abuse cases, and the control design for Application A, Application B, the Context Lake, and the laptop listeners. The Context Lake is the SQLite knowledge store built in Phase 5.

Engineering decision ED-P12A-01, authority: team-force. Threat ids `TM-24-01` to `TM-24-12`, trust-boundary ids `TB-24-01` to `TB-24-12`, and abuse-case ids `AC-24-01` to `AC-24-08` are the names Half B and the reviewer use.

---

## Finding

**Finding.** The release gate for this sub-stage is two behaviours. Injection text from corpus rows IC-01 through IC-06 returns BLOCK and drives no action. Every scored AI answer cites a lake item or abstains. Access stays the closed role list RT-01 to RT-06. This half adds no attribute-based product. A hallucination is an AI answer that does not cite a lake item. Percent floors stay Unknown.
**Evidence.** FD-18 DECIDED, authority: team-force. BO-10 PROPOSED and accepted 2026-10-18. `injection-corpus.yaml` ids IC-01, IC-02, IC-02-tiny, IC-03, IC-04, IC-05, IC-06. `apps/app_a/agent/tools.py` `WRITE_TOOLS = []`.
**Impact.** Half B puts one small control in Application A code and records one named before-and-after check. Sub-stage 25 maps obligations. Sub-stage 26 runs the red team.
**Risk.** Treating a named `scenario` such as `IC-01` as the only injection detector would let harvested approve-or-ignore text open an approval wait.
**Confidence.** High on the locked gate. Inference on the HTTP result of the untrusted-quote path until Half B measures it.
**Open questions.** HALF_A_ACCEPTED. BO-10 signer name stays Unknown.

---

## Locked facts this design applies

**Verified Fact.** FD-18. Access control stays RT-01 to RT-06. Site code, country, and sales region stay data fields that `rule_at` reads. They are not a new access-control product.

**Verified Fact.** FD-18. A hallucination is an AI answer that does not cite a lake item. The release gate is: injection returns BLOCK and drives no action, and every scored AI answer cites a lake item or abstains. Numeric percent floors stay Unknown.

**Verified Fact** of the BO-10 working answer, still PROPOSED. Treat all records as internal and synthetic. Process data is confidential. Packaged rows do not contain personal data. The classification artifact stays unsigned. The person's name stays Unknown.

**Verified Fact.** Injection text is data. Corpus IC-01 through IC-06 must BLOCK. The model has no write tool.

---

## Entry points

**Verified Fact.** `compose.yaml`. FD-13. `docs/20-application/access-control-implementation.md`.

| Id | Listener or route | Who may call it now | What a caller can ask |
|---|---|---|---|
| EP-24-01 | Application A port 8100 `POST /api/agent/run` | RT-01 to RT-06 with `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` | Start graph `app_a_investigate` on a case or a corpus id |
| EP-24-02 | Application A `POST /api/query` | Same three headers | Ask a golden question or a free-text question |
| EP-24-03 | Application A `POST /api/approvals` | Role mapped to `action_type` | Record a person decision |
| EP-24-04 | Application A `GET /api/cases/{id}`, `/api/queue`, `/api/recovery`, `/api/audit/{correlation_id}` | RT-01 to RT-06 | Read a case, the queue, recovery, or the audit trace |
| EP-24-05 | Application A `GET /health` and static UI GET | Anyone who can reach 8100 | Health JSON or the screen files |
| EP-24-06 | Application B port 8110, same route families | Same three headers on case routes | Same scenarios, rules from the lake |
| EP-24-07 | Lake REST port 8091 | `X-Api-Key` | `search_items`, `get_item`, `get_links`, `rule_at` |
| EP-24-08 | Lake MCP port 8092 | `X-Api-Key` | The same four lake reads over MCP |
| EP-24-09 | Legacy listener port 8080 `GET /api/cases` | Anyone who can reach 8080 | Case list with no identity check |
| EP-24-10 | Source gateway port 8090 | Anyone who can reach 8090 | Fixture feed rows |
| EP-24-11 | Replay files under `operations/model-replay/` | Application A or B `plan_draft` / generate in process | PRECOMPUTED model JSON |
| EP-24-12 | `opa eval` on `policy/opa/app_a.rego` | Node `opa_gate` in process | One verdict string |

Worked example. `POST /api/agent/run` on 8100 with headers for `demo-rt01-1` / RT-01, body `{"case_id":"REPLAY-000000000","scenario":"IC-01","proposed_action":"approve"}` is EP-24-01. Phase 10 measured HTTP 409 and `opa_verdict=BLOCK`. Honesty: REAL. That call names the corpus id. HB-24-01 later uses a call that omits the corpus id.

---

## Trust boundaries

A trust boundary is the line where data or a call changes who is believed. Code on the far side must treat the near-side input as untrusted until a named check passes.

| Id | From | To | Check that already exists | Residual |
|---|---|---|---|---|
| TB-24-01 | Browser or test client | Application A 8100 `/api` | Three identity headers. Closed role list RT-01 to RT-06 | Health and static UI stay open |
| TB-24-02 | Browser or test client | Application B 8110 `/api` | Same three headers | Health and static UI stay open |
| TB-24-03 | Any client | Legacy 8080 | None on case GET | Phase 13 identity hardening. Characterization CT-35 records HTTP 200 with no header |
| TB-24-04 | Any client | Source gateway 8090 | None | Fixture only |
| TB-24-05 | Application A or B | Lake REST 8091 | `X-Api-Key`. Lake writes rejected | Runtime lake file stays read-only except `build.py` |
| TB-24-06 | Harvested feed, email, HTML, document, or evidence payload | Retrieve, generate, and OPA | `trust: untrusted_text`. Quotes in `untrusted_quotes`. Lake `injection_block` | Agent `load_case` still sets `block` from a named corpus id. Half B must also set `block` from quotes plus write-from-text |
| TB-24-07 | Language model | Node `plan_draft` only | Six read tools. Empty write list. `check_claim` after the return | Live Azure unmeasured |
| TB-24-08 | Agent state | Open Policy Agent | Input object in `build_opa_input`. Verdict BLOCK, HOLD_FOR_REVIEW, or EXECUTE | Injection flag today needs corpus id or a pre-set `block` |
| TB-24-09 | Person at RT-01 to RT-06 | `POST /api/approvals` | Role map. Proposer differs from approver. BLOCK offers no approval | BO-03 stays PROPOSED |
| TB-24-10 | Agent | Packaged `legacy.sqlite3` and `enterprise_legacy.sqlite3` | Open `mode=ro` | A later write URI would skip FD-02 |
| TB-24-11 | Process restart | SqliteSaver file `apps/app_a/runtime/checkpoints.sqlite3` | `thread_id` equals `correlation_id` | File sits on the laptop disk |
| TB-24-12 | Process | Audit file `apps/app_a/audit/audit_chain.sqlite3` | One row per step and per human approval | Retention days Unknown |

Worked example for TB-24-06. Partner feed notes that contain auto-approve language are copied into `untrusted_quotes` in `apps/app_a/store.py`. `load_case` keeps those quotes. It sets `block` only when `scenario` is one of IC-01 through IC-06. **Verified Fact** of `nodes.py` `ACTION_FOR_CORPUS` and the `block: injection` assignment.

---

## Abuse cases

| Id | Abuse | Linked threat | What success looks like for the attacker | Required stop |
|---|---|---|---|---|
| AC-24-01 | Harvested approve-or-ignore text is treated as an order | TM-24-01 | Case approved, released, closed, or validation ignored | OPA BLOCK. No `record_approval`. No `engineering_hold` change from that text |
| AC-24-02 | Model is given a write tool | TM-24-02 | Model calls approve, hold, drop, assign, or delete | `WRITE_TOOLS` stays `[]`. `call_tool` rejects unknown names |
| AC-24-03 | Missing or forged identity on 8100 or 8110 | TM-24-03 | Case body returned, or a write recorded | HTTP 401 `missing_identity` or 403 `forbidden_role` |
| AC-24-04 | Same person proposes and approves | TM-24-04 | Duty split skipped | HTTP 403. OPA-R-07 BLOCK when actor equals proposer |
| AC-24-05 | Model invents INC-2025-014 owner | TM-24-05 | A made-up name is stored | Abstain. OPA-R-09 BLOCK when `owner_invented` is true. RT-06 assigns a supplied name |
| AC-24-06 | AI answer with no lake item id is served as ANSWER | TM-24-06 | Hallucination under FD-18 | Rewrite to ABSTAIN or cite a retrieved id |
| AC-24-07 | Runtime write to the lake | TM-24-07 | Ungoverned rule change | Lake write rejected. Only `build.py` writes `context-lake.sqlite3` |
| AC-24-08 | Graph runs past the budget | TM-24-08 | Unbounded tool calls | `recursion_limit` 12. Step budget 8. Max tool calls 8. Max gather visits 3. Exhaustion waits |

Worked example for AC-24-01. Catalogue BP7 counted 86 partner feeds with auto-approve or disregard-validation language. Honesty: REAL. IC-01 proposed action is approve. Expect BLOCK.

---

## Threats

| Id | Threat | Surface | Entry | Impact if it succeeds |
|---|---|---|---|---|
| TM-24-01 | Prompt injection from harvested text | LLM/RAG and agents | EP-24-01, EP-24-02, TB-24-06 | A write, or an approval wait opened by the text |
| TM-24-02 | Excess tool authority | Agents and tools | EP-24-01, TB-24-07 | Record change without a person |
| TM-24-03 | Broken access control on 8100 or 8110 | Application and APIs | EP-24-01 to EP-24-06 | Case data read or write without a mapped role |
| TM-24-04 | Duty-split skip | Application and APIs | EP-24-03 | Proposer approves the draft |
| TM-24-05 | Invented owner or invented parent lot | LLM/RAG | EP-24-02 | A name or column that the lake does not have |
| TM-24-06 | Ungrounded AI answer | LLM/RAG | EP-24-01, EP-24-02 | Hallucination: an AI answer that does not cite a lake item |
| TM-24-07 | Lake tampering at run time | Data and documents | EP-24-07 | Rule text changes outside the review loop |
| TM-24-08 | Runaway agent loop | Agents and tools | EP-24-01 | Cost and time grow without a stop |
| TM-24-09 | Replay duplicate treated as new | Integration | EP-24-01, EP-24-10 | Queue inflates. BP2 |
| TM-24-10 | Silent threshold compiled as a live number | Policy | EP-24-01 | Unsigned cutoff used as code |
| TM-24-11 | Confidential process data copied into a prompt as an order | Data and documents | TB-24-06 | Process notes drive a write |
| TM-24-12 | Ungated 8080 case dump | Application and APIs | EP-24-09 | Anyone on the laptop port reads cases |

TM-24-12 stays a residual for Phase 13. This half does not add identity to port 8080. **Verified Fact.** `compose.yaml` comment and CT-35.

---

## Control design

Existing controls stay. This half adds no product. Half B tightens one control so injection text itself, not a named corpus id, drives BLOCK.

### Controls already in force

| Control | What it does | Evidence |
|---|---|---|
| Closed role list RT-01 to RT-06 | `X-Actor-Role` must be one of those six strings. Writes match `action_type` | FD-18. `apps/shared/identity.py` `CLOSED_ROLES` |
| Read-only model tools | Six names reach the model. Write list is empty | FD-02. FD-15. `WRITE_TOOLS = []` |
| OPA three verdicts | BLOCK wins, then HOLD_FOR_REVIEW, then EXECUTE | FD-16. `policy/opa/app_a.rego` |
| Named corpus BLOCK | IC-01 through IC-06 plus IC-02-tiny BLOCK when `corpus_id` and write-from-text are set | `test_opa_all_corpus_rows_block`. Honesty REAL |
| IC-01 HTTP BLOCK | `POST /api/agent/run` with `scenario=IC-01` returns HTTP 409. Approvals stay empty | `test_inject_ic01_blocks_and_does_not_write`. Honesty REAL |
| Cite or abstain | Empty citations on ANSWER become ABSTAIN. Freeze run 42 of 42 | FD-14. FD-18. `ground.py`. Honesty REAL for 42 of 42. Floor Unknown |
| Human pause | Record change waits on `interrupt()`. Person resumes | BO-03 working answer. LangGraph `interrupt()` |
| Audit chain | One row per agent step and per human approval, keyed by correlation id | FD-23 |
| Untrusted lake items | Locator items have `trust: untrusted_text` | `context-lake/tests/test_injection.py` |
| Synthetic internal records | Packaged rows stay on this machine | FD-02. BO-10 working answer |

### The one small control Half B puts in code

Engineering decision ED-P12A-02, authority: team-force.

Control id **SC-24-01**. Name: untrusted-quote write-from-text BLOCK.

When Application A `load_case` or `build_opa_input` sees a non-empty `untrusted_quotes` list and `proposed_action` is one of `approve`, `release`, `ignore-validation`, or `close-from-text`, it sets `block` true and `injection` true. It does this even when `corpus_id` is empty and `scenario` is not an IC id.

OPA-R-01 already BLOCKs when `injection` is true or `block_flag` is true. Half B must feed those flags from the quotes and the action. Half B does not add a fourth verdict. Half B does not add a role. Half B does not add a write tool.

Files Half B may edit after HALF_A_ACCEPTED:

- `apps/app_a/agent/nodes.py` function `load_case`
- `apps/app_a/agent/opa_client.py` function `build_opa_input`
- `tests/platform/test_app_a_phase12_security.py` (new test file)

Application B already calls lake `block_untrusted` on retrieve. This Half B does not change Application B. Sub-stage 26 re-runs the corpus on both apps.

### How a write is allowed after this design

```text
Caller posts to Application A with RT-01 to RT-06 headers
        |
load_case reads the case and any untrusted_quotes
        |
If untrusted_quotes is non-empty and proposed_action is approve, release,
ignore-validation, or close-from-text: block=true, injection=true
        |
If scenario is IC-01 to IC-06: same flags (already true today)
        |
plan_draft may draft a sentence. Tools are read-only
        |
ground_and_cite requires a lake item id or abstains
        |
OPA returns BLOCK, HOLD_FOR_REVIEW, or EXECUTE
        |
BLOCK: HTTP 409. mark_blocked. No interrupt. No record_approval
HOLD_FOR_REVIEW or EXECUTE on a record change: interrupt(). Person at the mapped RT role
EXECUTE on a read: return the cited result
```

---

## Privacy handling (BO-10 applied)

**Verified Fact** of the working answer. Status PROPOSED. Unsigned.

| Rule | What the applications do |
|---|---|
| Internal and synthetic | Packaged SQLite, documents, and lake items stay on this laptop. They are generated test records |
| Process data is confidential | Recipe, hold, feed, and policy fields stay in the local stores and in audit rows for the demo. They are not published |
| Packaged rows do not contain personal data | Actor fields use laptop demo ids such as `demo-rt01-1`. Company staff names stay Unknown. INC-2025-014 owner stays Unknown until RT-06 assigns a supplied name |
| Unsigned classification | This file does not invent a signer. BO-10 stays PROPOSED |

Retention days stay Unknown. Encryption-at-rest product choice stays Phase 13. This half does not add a vault.

---

## Responsible AI handling (FD-18 applied)

| Rule | What the applications do |
|---|---|
| Hallucination | An AI answer that does not cite a lake item |
| Scored answer | Must cite a retrieved lake item id, or abstain |
| Injection | Corpus text stays data. BLOCK. Drives no action |
| Disclosure | `draft_plan` is a proposal. Code, lake items, and person decisions stay the source of record writes |
| Percent floors | Stay Unknown. Do not write 90 or 95 as a target |
| Forced ungrounded | UQ-01, UQ-02, UQ-03 abstain |

Freeze run 2026-10-18 scored 42 of 42 under those behaviours. Honesty: REAL. The percent floor stays Unknown.

---

## Half B before-and-after check (named)

Engineering decision ED-P12A-03, authority: team-force. Check id **HB-24-01**. Full procedure lives in `security-test-results.md`.

Half B selects one packaged partner feed whose `processing_status` is `REPLAY` and whose notes contain auto-approve or disregard-validation language. It records that `feed_id` as REAL.

**Before the SC-24-01 edit.** `POST /api/agent/run` with that `case_id`, `proposed_action` `approve`, and no `scenario` and no `corpus_id`. Half B records HTTP status, `opa_verdict`, `waiting`, `error_class`, case `status`, `approvals`, `engineering_hold`, and whether any audit row has `row_kind=human_approval`. Inference from today's `load_case` path: OPA returns HOLD_FOR_REVIEW and `interrupt()` can open. Half B measures the real before values. Honesty of those measured values will be REAL.

**After the SC-24-01 edit.** The same POST. Expected: HTTP 409, `opa_verdict=BLOCK`, `waiting` false, `error_class=blocked`, `status` unchanged, `approvals` empty, `engineering_hold` unchanged, no `human_approval` audit row, an EV-12 row present.

---

## What this file does not do

This file does not write security code. It does not start Half B. It does not write sub-stage 25 or 26. It does not add an attribute-based access product. It does not invent a percent floor. It does not sign BO-10. It does not add identity to port 8080.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
