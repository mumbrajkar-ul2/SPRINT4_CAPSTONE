# Security control matrix

| Field | Value |
|---|---|
| Stage | Phase 12 / 24 Security, privacy, responsible AI. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-24a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No security code in this half. |
| Evidence sources | FD-18; BO-09; BO-10; FD-02; FD-14; FD-15; FD-16; FD-23; `docs/12-specs/business-rules.md`; `apps/shared/identity.py`; `policy/opa/app_a.rego`; `apps/app_a/agent/tools.py`; `docs/22-agentic-engineering/agent-test-results.md` |
| Assumptions | BO-03 working answer holds. BO-10 working answer holds. Closed role list stays RT-01 to RT-06. |
| Unresolved issues | Percent floors stay Unknown. Retention stays Unknown. Port 8080 identity stays Phase 13. BO-10 signer stays Unknown. |
| Residual risks | SC-24-01 is still missing in `load_case`. A caller who omits `corpus_id` can still open a wait on approve-from-text. Half B adds the quotes-plus-action flags there. |

This file lists each control, the threat it covers, the owner of the check, and the Half B evidence cell. Measured before-and-after values stay Unknown until Half B. Existing Phase 9 and Phase 10 runs are cited as prior REAL evidence. They do not replace HB-24-01.

Engineering decision ED-P12A-04, authority: team-force. Control ids `SC-24-01` to `SC-24-12`.

---

## Finding

**Finding.** Twelve controls cover injection, tools, roles, citations, the human pause, the audit chain, lake writes, budgets, classification, and the ungated 8080 residual. Half B changes one control: SC-24-01. The other eleven stay as built. Access stays RT-01 to RT-06. This half adds no attribute-based product.
**Evidence.** FD-18. Group C. `CLOSED_ROLES` in `identity.py`. `WRITE_TOOLS = []`. OPA-R-01 in `app_a.rego`.
**Impact.** Half B has one edit pair and one pytest file.
**Risk.** Re-implementing identity on 8080 in this half would add a feature the phase excludes.
**Confidence.** High on the existing eleven. Inference on today's HTTP result for SC-24-01 until HB-24-01 runs.
**Open questions.** HALF_A_ACCEPTED.

---

## How to read a row

Each row stands alone. `Half B action` is `tighten` for SC-24-01 and `re-measure` or `defer` for the others. `Measured before` and `Measured after` stay Unknown in this half. Prior REAL runs are named in `Prior evidence` so the reviewer can see what already passed.

Worked example. SC-24-03 already rejects a missing key on 8100. Half B does not change that helper. HB-24-01 still records that the injection POST uses valid RT-01 headers, so a 401 cannot be mistaken for a BLOCK.

---

## Matrix

| Id | Control | Threat | What it does | Owner of the check | Half B action | Prior evidence | Measured before | Measured after |
|---|---|---|---|---|---|---|---|---|
| SC-24-01 | Untrusted-quote write-from-text BLOCK | TM-24-01 | Non-empty `untrusted_quotes` plus `approve` / `release` / `ignore-validation` / `close-from-text` sets `block` and `injection` even when `corpus_id` is empty | Team-Force. Test HB-24-01 | tighten | Inference from `load_case`: `block` follows named IC ids only | Unknown | Unknown |
| SC-24-02 | Named corpus BLOCK | TM-24-01 | IC-01 through IC-06 and IC-02-tiny BLOCK when corpus id and write-from-text are set | Team-Force. OPA-R-01 | re-measure on the HTTP path as HB-24-02 | Phase 10 T-INJECT-ALL: seven BLOCK from `opa eval`. Honesty REAL. T-INJECT-01 HTTP 409 for IC-01 only | Unknown | Unknown |
| SC-24-03 | Closed role list on 8100 and 8110 | TM-24-03 | `X-Actor-Role` must be RT-01 to RT-06. Writes match `action_type` | Team-Force. BO-09 SME map | re-measure headers on HB-24-01 | Phase 9 identity tests. EH-01 HTTP 401 | Unknown | Unknown |
| SC-24-04 | Duty split | TM-24-04 | Proposer and approver are different people. Model is never the approver | Team-Force. BO-09 | leave | Phase 10 T-SEP HTTP 403 when actor equals proposer. Honesty REAL | Unknown | Unknown |
| SC-24-05 | Empty write-tool list | TM-24-02 | Six read tools reach the model. Write list is empty | Team-Force. FD-02, FD-15 | re-measure `WRITE_TOOLS == []` in the new test file | Phase 10 T-NO-WRITE-TOOL. Honesty REAL | Unknown | Unknown |
| SC-24-06 | Cite or abstain | TM-24-06 | An AI answer cites a retrieved lake item id or abstains. Empty ANSWER citations become ABSTAIN | Team-Force. FD-14, FD-18 | re-measure on the HB-24-01 response body | Freeze 42 of 42. Honesty REAL. Floor Unknown | Unknown | Unknown |
| SC-24-07 | Forced ungrounded abstain | TM-24-05 | UQ-01 parent lot, UQ-02 INC owner, UQ-03 unknown limit abstain and invent no fact | Team-Force | leave. Sub-stage 26 re-runs eval | Phase 9 grounding-results.md. Honesty REAL | Unknown | Unknown |
| SC-24-08 | Human pause on record change | TM-24-02, TM-24-10 | `interrupt()` waits. Person at the mapped RT role resumes | Run-time role RT-01 to RT-06. BO-03 working answer | leave | Phase 10 T-TRACE. RT-03 recorded hold. Honesty REAL | Unknown | Unknown |
| SC-24-09 | Audit chain | TM-24-08 | One row per agent step and per human approval. Key is correlation id | Team-Force. FD-23 | HB-24-01 asserts EV-12 and no `human_approval` | Phase 10 T-TRACE 12 rows. Honesty REAL | Unknown | Unknown |
| SC-24-10 | Runtime lake read-only | TM-24-07 | `build.py` writes the lake. Apps reject lake writes. Packaged DBs open `mode=ro` | Team-Force | HB-24-01 must not write `cases.status` or `wafer_lots.engineering_hold` in packaged files | Phase 10 T-READONLY-DB. Honesty REAL | Unknown | Unknown |
| SC-24-11 | Classification handling | TM-24-11 | Records treated as internal and synthetic. Process data confidential. Packaged rows do not contain personal data | Business Owner for sign-off. Team-Force for handling | leave. Do not invent a signer | BO-10 PROPOSED accepted 2026-10-18 | n/a | n/a |
| SC-24-12 | Ungated 8080 residual | TM-24-12 | Port 8080 stays the baseline listener with no identity check | Phase 13 | defer | CT-35 HTTP 200 without header. Honesty REAL | n/a this half | n/a this half |

---

## Access control (FD-18)

**Verified Fact.** FD-18. Access control stays the closed role list.

| `action_type` | Allowed `X-Actor-Role` | Who is refused |
|---|---|---|
| `dispose` | RT-01 Fab Exception Reviewer | The model. The same person as `proposed_by` |
| `approve_agent` | RT-02 Shift Lead or Process Engineer (Approver) | The proposing agent. The same person as `proposed_by` |
| `recipe_hold_or_release` | RT-03 Process Engineer | RT-05 acting alone. The model |
| `policy_pick` or `keep_wait` | RT-04 Policy Owner | The model |
| `replay_confirm` | RT-05 Operations Analyst | An unattended job. The model |
| `assign_owner` | RT-06 Operations Lead | A made-up name. The model |

Site, country, and sales region stay fields on the case and on `rule_at`. They do not become a second access product.

Company job titles that match these SME role names stay Unknown. Demo actors `demo-rt01-1` through `demo-rt06-1` are laptop labels.

---

## Release gate mapped to controls

**Verified Fact.** FD-18.

| Gate sentence | Controls that implement it | Percent |
|---|---|---|
| Injection returns BLOCK and drives no action | SC-24-01, SC-24-02, SC-24-05, SC-24-08, SC-24-10 | None. Behaviour only |
| Every scored AI answer cites a lake item or abstains | SC-24-06, SC-24-07 | Floor Unknown. 42 of 42 is a prior REAL count, not a target |

Do not write 90 or 95 in a target cell.

---

## OPA rules this matrix relies on

**Verified Fact.** FD-16. `policy/opa/app_a.rego`.

| Rule | When it fires | Verdict |
|---|---|---|
| OPA-R-01 | `injection` true, or `block_flag` true, or corpus id plus write-from-text | BLOCK |
| OPA-R-07 | `actor_id` equals `proposed_by` and both are non-empty | BLOCK |
| OPA-R-09 | `owner_invented` true | BLOCK |
| OPA-R-06 | `record_change` true | HOLD_FOR_REVIEW after BLOCK rules |
| OPA-R-11 | Read path, not injection, budget remaining | EXECUTE |

SC-24-01 feeds OPA-R-01. It does not add a new Rego verdict. Half B may leave `app_a.rego` unchanged if `injection` and `block_flag` are set in Python. If Half B needs a Rego input field, it adds `untrusted_quote_present` already in the input object and uses it only with write-from-text. **Engineering decision ED-P12A-05, authority: team-force.** Prefer the Python flag set. Do not add an amount comparison. Do not add a fourth verdict.

`untrusted_quote_present` already exists on the OPA input. **Verified Fact.** `build_opa_input` sets it from `state.untrusted_quotes`. Today's Rego does not BLOCK on that field alone. A quote with proposed action `explain` must still be allowed to return a cited sentence. SC-24-01 pairs the quotes with write-from-text.

---

## What this file does not do

This file does not write the SC-24-01 edit. It does not start Half B. It does not sign BO-10. It does not add an attribute-based access product.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
