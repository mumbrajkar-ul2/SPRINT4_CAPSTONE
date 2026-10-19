# Compliance control matrix

| Field | Value |
|---|---|
| Stage | Phase 12 / 25 Governance and assurance. Half B evidence. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-25b-doc-20261018-001 |
| Status | MEASURED. HB-25-07, HB-25-09, and HB-25-10 recorded. Statute applicability stays Unknown. Percent floors stay Unknown. Retention days stay Unknown. |
| Evidence sources | `compliance-obligations.md`; FD-18; BO-09; BO-10; FD-02; FD-14; FD-16; FD-23; `docs/24-security-privacy/security-control-matrix.md`; `docs/12-specs/business-rules.md`; `policy/opa/app_a.rego`; `apps/shared/identity.py`; `apps/app_a/agent/tools.py`; `apps/app_a/intelligence/generate.py`; `apps/app_b/intelligence/generate.py`; `apps/app_a/audit/store.py`; `context-lake/generated/app-b-pin.json`; `apps/app_a/prompts/`; `apps/app_b/prompts/`; `Decision_Tracker.md` |
| Assumptions | BO-03 and BO-10 working answers hold. Closed role list stays RT-01 to RT-06. Sub-stage 24 Half B already measured SC-24-01. This half adds no security product. |
| Unresolved issues | Percent floors stay Unknown. Retention days stay Unknown. Statute applicability stays Unknown. BO-10 signer stays Unknown. |
| Residual risks | Treating a prior REAL security count as a signed compliance pass would invent a certificate. Adding an attribute-based access product would add a feature this phase excludes. |

This file maps each working obligation to a control that already exists or to a named gap. Open Policy Agent is the policy checker that returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK. This file issues no compliance certificate.

Engineering decision ED-P12-25A-02, authority: team-force. Governance control ids `GC-25-01` to `GC-25-14`. Half B re-measured the named cells. Half B did not add a control product.

---

## Finding

**Finding.** Fourteen controls cover classification, local stores, tools, human pause, roles, citations, injection, audit, lake version, honesty labels, unsigned artifacts, disclosure, and the retention gap. Half B recorded evidence. Half B changed no feature. `CLOSED_ROLES` is RT-01 to RT-06. `WRITE_TOOLS` is empty. The lake pin still shows version 1.0.0 and hash `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Retention days stay Unknown. Percent floors stay Unknown.
**Evidence.** FD-18. BO-10 working answer. `CLOSED_ROLES` in `identity.py`. `WRITE_TOOLS = []`. Phase 24 `security-test-results.md` HB-24-01 HTTP 409 after SC-24-01. Recorded table under this file.
**Impact.** Reviewer can trace OB-25-01 to OB-25-12 onto one control each and onto the recorded cells.
**Risk.** Inventing a percent floor in a matrix cell would skip FD-18.
**Confidence.** High on existing controls and on the file reads. Unknown on statute fit.
**Open questions.** BO-10 signer. Statute applicability. Retention days. Percent floors.

---

## How to read a row

Each row stands alone. `Half B action` is `record` for every row. This half adds no tighten edit. Prior REAL runs sit in `Prior evidence`. `Measured this half` now holds the Half B file-read values. Cells that stay Unknown by design stay Unknown.

Worked example. GC-25-08 already BLOCKs injection. Half B recorded that the control still exists and cited HB-24-01. Half B did not rewrite `load_case`.

---

## Matrix

| Id | Control | Obligation | What it does | Owner of the check | Half B action | Prior evidence | Measured this half |
|---|---|---|---|---|---|---|---|
| GC-25-01 | Classification handling | OB-25-01 | Packaged records stay internal and synthetic. Process fields stay on this laptop. Actor fields use demo ids | Business Owner for sign-off. Team-Force for handling | record HB-25-04 | BO-10 accepted 2026-10-18. SC-24-11 | BO-10 still PROPOSED. No signer name in this folder. Honesty REAL |
| GC-25-02 | Local synthetic stores | OB-25-02 | Packaged SQLite and lake files stay on this machine. Apps open packaged stores `mode=ro` | Team-Force | record HB-25-06 owner field empty; stores still local | Phase 10 T-READONLY-DB. Honesty REAL | INC-2025-014 `owner_id` empty. `load_packaged()` opened both packaged sqlite files `mode=ro`. Honesty REAL |
| GC-25-03 | Empty write-tool list | OB-25-02 | Six read tools reach the model. Write list is empty | Team-Force | record `WRITE_TOOLS == []` in HB-25-07 notes | Phase 10 T-NO-WRITE-TOOL. Honesty REAL | `WRITE_TOOLS == []` in `tools.py` and both `generate.py` files. Honesty REAL |
| GC-25-04 | Human pause on a record change | OB-25-03 | LangGraph `interrupt()` waits. A person at the mapped RT role resumes | Run-time role RT-01 to RT-06. BO-03 working answer | record that BO-03 stays PROPOSED and unsigned | Phase 10 T-TRACE. RT-03 recorded hold. Honesty REAL | `Decision_Tracker.md` row BO-03 status is PROPOSED. Honesty REAL |
| GC-25-05 | Closed role list | OB-25-04 | `X-Actor-Role` must be RT-01 to RT-06. Writes match `action_type` | Team-Force. BO-09 SME map | record HB-25-07 | Phase 9 identity tests. EH-01 HTTP 401 | `CLOSED_ROLES` is RT-01 to RT-06. Honesty REAL |
| GC-25-06 | Duty split | OB-25-04 | Proposer and approver are different people. The model is never the approver | Team-Force. BO-09 | record the rule still in `check_write_action` / OPA-R-07 | Phase 10 T-SEP HTTP 403. Honesty REAL | `check_write_action` still returns forbidden when `actor_id == proposed_by`. `policy/opa/app_a.rego` still has OPA-R-07. Honesty REAL |
| GC-25-07 | Cite or abstain | OB-25-05 | An AI answer cites a retrieved lake item id or abstains. Empty ANSWER citations become ABSTAIN | Team-Force. FD-14. FD-18 | record the 42-of-42 prior count and keep the floor Unknown | Freeze 42 of 42. Honesty REAL. Floor Unknown | Prior freeze 42 of 42 copied. Floor stays Unknown. This half did not re-run the freeze |
| GC-25-08 | Injection BLOCK | OB-25-06 | Harvested approve-or-ignore text sets BLOCK. No approval wait. No record write | Team-Force. FD-16. SC-24-01 | record HB-24-01 after-values as prior REAL. Do not re-edit the control | HB-24-01 after: HTTP 409, `opa_verdict=BLOCK`. Honesty REAL | Copied HB-24-01 after: HTTP 409, `opa_verdict=BLOCK`. This half did not re-edit `load_case` |
| GC-25-09 | Audit chain | OB-25-07 | One row per agent step and per human approval. Key is correlation id | Team-Force. FD-23 | record that `audit_chain` still has the 27 named columns | Phase 10 T-TRACE 12 rows. Honesty REAL | `apps/app_a/audit/store.py` `COLUMNS` length 27. Honesty REAL |
| GC-25-10 | Lake review and runtime read-only | OB-25-08 | `build.py` writes `context-lake.sqlite3`. Apps read version 1.0.0 | Team-Force | record HB-25-09 pin hash | Pin `lake_version` 1.0.0. `sqlite_sha256` `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Honesty REAL | Pin still `lake_version` 1.0.0 and hash `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Honesty REAL |
| GC-25-11 | Honesty labels | OB-25-09 | Model card and system card mark replay sentences PRECOMPUTED. Live Azure stays NEEDS_HUMAN | Team-Force | record HB-25-01, HB-25-02, HB-25-03 | `operations/model-replay/README.md`. Compose `MODEL_MODE=replay` | Compose still `MODEL_MODE=replay`. Replay bodies PRECOMPUTED. Live Azure NEEDS_HUMAN. Honesty REAL |
| GC-25-12 | Unsigned classification | OB-25-10 | Classification and this folder stay unsigned. No signer name. No certificate file | Business Owner for a later signature. Team-Force records the gap | record HB-25-04 and HB-25-05 | Tracker v1.26. BO-10 PROPOSED | BO-10 PROPOSED. Seven markdown files. No certificate file. Signer stays Unknown. Honesty REAL |
| GC-25-13 | Draft disclosure | OB-25-11 | Prompts and the agent mark `draft_plan` as a proposal. Code, lake items, and person decisions stay the write source | Team-Force for prompts. RT roles for writes | record prompt files still say the model must not write | `docs/19-intelligence/prompt-registry.md` semver 1.0.0 | Six prompt files at semver 1.0.0. Each `allowed_tools` `[]`. Each system text still says the model must not call a write tool. Honesty REAL |
| GC-25-14 | Retention gap recorded | OB-25-12 | Retention days stay Unknown. The audit file is kept. No day count is invented | Business Owner for a later signed count | record the Unknown cell. Do not fill a number | Audit-chain unresolved issue | Unknown |

Worked example. GC-25-07. Freeze run 2026-10-18 scored 42 grounded answers of 42 scored answers. Honesty: REAL. Half B copied that prior count into the evidence cell. Half B left the floor Unknown.

---

## Access control this matrix uses

**Verified Fact.** FD-18. Access stays the closed role list. This phase adds no attribute-based product.

| `action_type` | Allowed `X-Actor-Role` | Who is refused |
|---|---|---|
| `dispose` | RT-01 Fab Exception Reviewer | The model. The same person as `proposed_by` |
| `approve_agent` | RT-02 Shift Lead or Process Engineer (Approver) | The proposing agent. The same person as `proposed_by` |
| `recipe_hold_or_release` | RT-03 Process Engineer | RT-05 acting alone. The model |
| `policy_pick` or `keep_wait` | RT-04 Policy Owner | The model |
| `replay_confirm` | RT-05 Operations Analyst | An unattended job. The model |
| `assign_owner` | RT-06 Operations Lead | A made-up name. The model |

Company job titles that match these SME role names stay Unknown. Demo actors `demo-rt01-1` through `demo-rt06-1` are laptop labels.

---

## Release gate mapped to controls

**Verified Fact.** FD-18.

| Gate sentence | Controls that implement it | Percent |
|---|---|---|
| Injection returns BLOCK and drives no action | GC-25-03, GC-25-08 | None. Behaviour only |
| Every scored AI answer cites a lake item or abstains | GC-25-07, GC-25-13 | Floor Unknown. 42 of 42 is a prior REAL count, not a target |

Do not write 90 or 95 in a target cell.

---

## Statute families on this matrix

**Verified Fact** of the design rule. ST-25-01 to ST-25-05 stay Unknown. They reuse the working controls above. They do not gain a new control.

| Statute id | Working controls used while applicability is Unknown |
|---|---|
| ST-25-01 privacy statute | GC-25-01, GC-25-02 |
| ST-25-02 AI-product statute | GC-25-07, GC-25-08, GC-25-11, GC-25-13 |
| ST-25-03 export-control statute | GC-25-01, GC-25-02 |
| ST-25-04 records-retention statute | GC-25-09, GC-25-14 |
| ST-25-05 customer contract | None beyond OB-25-01 to OB-25-12 |

---

## Half B evidence this file names

| Check | What Half B records | Honesty when recorded |
|---|---|---|
| HB-25-07 | `CLOSED_ROLES` in `apps/shared/identity.py` is exactly RT-01 to RT-06. `WRITE_TOOLS` is empty | REAL |
| HB-25-09 | `context-lake/generated/app-b-pin.json` still shows `lake_version` 1.0.0 and the hash named in GC-25-10 | REAL |
| HB-25-10 | Prompt files P-EXPLAIN-CONFLICT, P-NL-QUERY, and P-DRAFT-PLAN exist at semver 1.0.0 | REAL |

### Recorded

Recorded 2026-10-18 under `corr-p12-25b-doc-20261018-001`. Half B did not edit identity, OPA, or tools to pass a check.

HB-25-07. `CLOSED_ROLES` is exactly `('RT-01', 'RT-02', 'RT-03', 'RT-04', 'RT-05', 'RT-06')`. `WRITE_TOOLS` is `[]` in `apps/app_a/agent/tools.py`, `apps/app_a/intelligence/generate.py`, and `apps/app_b/intelligence/generate.py`. Six read names remain `search_items`, `get_item`, `get_links`, `rule_at`, `get_case`, `get_recovery_status`. Honesty: REAL.

HB-25-09. `context-lake/generated/app-b-pin.json` has `lake_version` `1.0.0` and `sqlite_sha256` `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Honesty: REAL.

HB-25-10. Six prompt files exist at semver `1.0.0`: `P-EXPLAIN-CONFLICT`, `P-NL-QUERY`, and `P-DRAFT-PLAN` on Application A and the same three ids on Application B. Each has `allowed_tools` `[]`. Honesty: REAL.

---

## What this file does not do

This file maps working obligations to existing controls. It issues no compliance certificate. It does not write sub-stage 26. It does not add an attribute-based access product.

STOP. Do not start sub-stage 26.
