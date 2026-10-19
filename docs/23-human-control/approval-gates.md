# Approval gates

| Field | Value |
|---|---|
| Stage | Phase 10 / 23 Human control and audit chain. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Names FD-16 rule bodies. Does not write Rego. |
| Evidence sources | `docs/10-architecture/adrs/adr-opa-gates.md`; `docs/12-specs/business-rules.md`; `context-lake/eval/injection-corpus.yaml`; BO-03; BO-08; BO-09 |
| Assumptions | Verdicts are only EXECUTE, HOLD_FOR_REVIEW, and BLOCK. Archive silence waits. Injection yields BLOCK. The policy file contains no amount comparison. |
| Unresolved issues | BO-03, BO-06b, and BO-08 stay PROPOSED. Company titles stay Unknown. |
| Residual risks | Compiling an unsigned cutoff into Rego would sign a Business Owner row in code. Letting the model choose the verdict would make the model the gate. |

This file names the OPA input, the rule ids, and the verdict each rule returns. Half B writes `policy/opa/app_a.rego` from these rows. Half B does not add a fourth verdict. Half B does not add an amount field to the input.

Engineering decision ED-P10A-06, authority: team-force.

---

## Finding

**Finding.** Twelve named rules cover injection, archive silence, overlap, region disagreement, record-changing drafts, duty separation, finance-audit mismatch, invented owners, exhausted budget, empty citations on a write, and read-only continue. BLOCK wins, then HOLD_FOR_REVIEW, then EXECUTE.
**Evidence.** FD-16 deferred into this half. Locked three verdicts. BR-05, BR-06, BR-10, BR-11, BR-12. Group C.
**Impact.** Half B can write one Rego rule per id without inventing a dollar cutoff.
**Risk.** A default EXECUTE on unknown input would auto-run a silent case.
**Confidence.** High on the verdicts. The rule ids are a team-force naming.
**Open questions.** BO-03 signer. BO-08 signer.

---

## Package and evaluate

| Item | Value |
|---|---|
| File | `policy/opa/app_a.rego` |
| Package | `package app_a` |
| Decision path | `data.app_a.verdict` |
| Allowed strings | `EXECUTE`, `HOLD_FOR_REVIEW`, `BLOCK` |
| Evaluate | `opa eval -d policy/opa -i <input.json> --format json 'data.app_a.verdict'` |
| Default | If no rule matches and `record_change` is true: `HOLD_FOR_REVIEW`. If no rule matches and `record_change` is false: `EXECUTE` |

`policy/opa/data.json` may list corpus ids `IC-01` to `IC-06` and the write-from-text actions `approve`, `release`, `ignore-validation`, `close-from-text`. It must not list a live amount cutoff.

---

## Input object Half B must send

| Field | Type | What it holds |
|---|---|---|
| `proposed_action` | string | `explain`, `cite`, `recipe_hold_or_release`, `policy_pick`, `replay_drop`, `assign_owner`, `dispose`, `approve`, `release`, `ignore-validation`, `close-from-text` |
| `record_change` | boolean | True when a stored record would change |
| `injection` | boolean | True when a corpus locator is present and the action is approve, release, ignore-validation, or close-from-text |
| `corpus_id` | string or empty | `IC-01`, `IC-02`, `IC-02-tiny`, `IC-03`, `IC-04`, `IC-05`, `IC-06` |
| `block_flag` | boolean | Lake envelope `block` |
| `archive_match` | string | `none`, `one`, `overlap` |
| `region_disagreement` | boolean | Site versus stored region, or country with no site |
| `silent_threshold` | boolean | Urgent-cutoff question and archive silent |
| `finance_audit_mismatch` | boolean | Operational closed versus finance or audit flag disagree |
| `actor_id` | string | Person on a resume. Empty on a draft |
| `proposed_by` | string | `model_draft` or a person id |
| `actor_role` | string | `RT-01` to `RT-06` or empty |
| `action_type` | string | Approval `action_type` on resume. Empty on a draft |
| `owner_invented` | boolean | True when the model supplied `owner_id` |
| `budget_exhausted` | boolean | Step or tool cap hit |
| `citations_empty` | boolean | No accepted lake id after ground |
| `untrusted_quote_present` | boolean | Quotes list is non-empty |

Code sets these flags. The model does not set them.

---

## Rule bodies

Priority: a matching BLOCK rule ends evaluation. Else a matching HOLD_FOR_REVIEW rule ends evaluation. Else EXECUTE if a read-only rule matches or the default applies.

### OPA-R-01 injection_text_is_data

| Field | Value |
|---|---|
| When | `injection` is true, or `block_flag` is true, or `corpus_id` is one of IC-01 to IC-06 and `proposed_action` is `approve`, `release`, `ignore-validation`, or `close-from-text` |
| Verdict | BLOCK |
| Lake item | `rule.untrusted_text.block` |
| Finding | Harvested instruction language never drives a write. |
| Evidence | Corpus file. 86 partner feeds. Honesty: REAL. |
| Impact | Minutes 36 to 39. EV-12. |
| Risk | Serving the quote as an instruction would leak a write order. |
| Confidence | High |
| Open questions | None for the 86. |

### OPA-R-02 archive_silence

| Field | Value |
|---|---|
| When | `archive_match` is `none` |
| Verdict | HOLD_FOR_REVIEW |
| Lake item | `rule.recipe_release.no_match` |
| Finding | No archive row means wait. Live policy does not insert a substitute number. |
| Evidence | BR-05. |
| Impact | GQ-03, GQ-05. |
| Risk | A JavaScript-style always-pass default would hide the miss. |
| Confidence | High |
| Open questions | None. |

### OPA-R-03 silent_threshold

| Field | Value |
|---|---|
| When | `silent_threshold` is true |
| Verdict | HOLD_FOR_REVIEW |
| Lake item | `rule.threshold.silent` |
| Finding | The archive is silent on an urgent amount cutoff. The case waits. The policy file has no amount comparison. |
| Evidence | BR-11. BO-08 PROPOSED. |
| Impact | Queue ranking may still use the rebuilt Python function as a recorded deviation. Canonical live policy waits. |
| Risk | An amount comparison in Rego would sign BO-08. |
| Confidence | High on the wait. Signature missing. |
| Open questions | BO-08 signer. |

### OPA-R-04 policy_overlap

| Field | Value |
|---|---|
| When | `archive_match` is `overlap` |
| Verdict | HOLD_FOR_REVIEW |
| Lake item | `rule.policy.overlap_or_invalid` |
| Finding | Two active rows or an inverted interval wait. The model does not pick. |
| Evidence | US has 5 active rows. Honesty: REAL. |
| Impact | Scenario 10. RT-04. |
| Risk | First-row-wins would hide POL-0034. |
| Confidence | High |
| Open questions | None for the wait. |

### OPA-R-05 region_disagreement

| Field | Value |
|---|---|
| When | `region_disagreement` is true |
| Verdict | HOLD_FOR_REVIEW |
| Lake item | `rule.region.disagreement` |
| Finding | Site IN-BLR with stored AMER waits. Country AU or ZA with no site waits. |
| Evidence | BR-10. 84 packaged disagreements. Honesty: REAL. |
| Impact | `rule_at` citations. |
| Risk | Binding on stored AMER would hide those 84 rows. |
| Confidence | High |
| Open questions | None for the six mapped sites. |

### OPA-R-06 record_change_needs_person

| Field | Value |
|---|---|
| When | `record_change` is true and no BLOCK rule matched |
| Verdict | HOLD_FOR_REVIEW |
| Lake item | `rule.hold.person_only` |
| Finding | A person approves every record-changing action. BO-03 working answer stays PROPOSED. |
| Evidence | BO-03. Group C. |
| Impact | Recipe hold, replay drop, policy pick, dispose, assign, approve_agent. |
| Risk | EXECUTE on this row would auto-write. |
| Confidence | High on the bound. Signature missing. |
| Open questions | BO-03 signer. |

### OPA-R-07 proposer_equals_approver

| Field | Value |
|---|---|
| When | `actor_id` is non-empty and equals `proposed_by` |
| Verdict | BLOCK |
| Lake item | `term.approval` |
| Finding | The proposer is never the approver. This request stops. The pending interrupt stays for a different person. |
| Evidence | BO-09. |
| Impact | HTTP 403 still applies. OPA agrees. |
| Risk | One login on draft and approve would skip Group C. |
| Confidence | High |
| Open questions | Company titles. |

### OPA-R-08 finance_audit_mismatch

| Field | Value |
|---|---|
| When | `finance_audit_mismatch` is true |
| Verdict | HOLD_FOR_REVIEW |
| Lake item | `rule.open_closed.finance_audit` |
| Finding | Operational closed, finance booked, and audit closed stay three states. A mismatch waits. |
| Evidence | BO-06b PROPOSED. |
| Impact | Queue labels stay separate. |
| Risk | Booking finance from operational closed would treat an unsigned row as code. |
| Confidence | High on the wait. Signature missing. |
| Open questions | BO-06b signer. |

### OPA-R-09 model_invented_owner

| Field | Value |
|---|---|
| When | `owner_invented` is true |
| Verdict | BLOCK |
| Lake item | `decision.inc_2025_014` |
| Finding | INC-2025-014 owner stays empty until RT-06 supplies a name. |
| Evidence | 695 tasks with empty `assigned_to`. Honesty: REAL. |
| Impact | Scenario 11. |
| Risk | A generated name would invent an owner. |
| Confidence | High |
| Open questions | The person RT-06 will type. |

### OPA-R-10 budget_exhausted

| Field | Value |
|---|---|
| When | `budget_exhausted` is true |
| Verdict | HOLD_FOR_REVIEW |
| Lake item | `term.approval` |
| Finding | A hit of the step or tool cap waits with evidence gathered so far. |
| Evidence | ED-P10A-02. |
| Impact | TERM-06. |
| Risk | EXECUTE here would apply a partial draft. |
| Confidence | High |
| Open questions | None. |

### OPA-R-11 cite_or_abstain_readonly

| Field | Value |
|---|---|
| When | `record_change` is false and `injection` is false and `block_flag` is false and `budget_exhausted` is false |
| Verdict | EXECUTE |
| Lake item | `arch.lake.yaml_sqlite` |
| Finding | A cited explanation or an abstain may finish. FD-14 still requires a citation or an empty sentence. |
| Evidence | Scenario 9. FD-14. |
| Impact | TERM-02 and TERM-03. |
| Risk | Setting `record_change` false on a hold proposal would skip RT-03. |
| Confidence | High |
| Open questions | None. |

### OPA-R-12 empty_citations_on_write

| Field | Value |
|---|---|
| When | `citations_empty` is true and `record_change` is true and `injection` is false |
| Verdict | HOLD_FOR_REVIEW |
| Lake item | FD-14 behaviour on a write path |
| Finding | A write proposal with no citation waits. The graph does not invent a lake id. |
| Evidence | FD-14. |
| Impact | Broken retrieve still waits. |
| Risk | EXECUTE would write without a citation. |
| Confidence | High |
| Open questions | None. |

---

## Corpus rows that must produce BLOCK

| Corpus id | Proposed action | Rule |
|---|---|---|
| IC-01 | approve | OPA-R-01 |
| IC-02 | approve | OPA-R-01 |
| IC-02-tiny | approve | OPA-R-01 |
| IC-03 | approve | OPA-R-01 |
| IC-04 | release | OPA-R-01 |
| IC-05 | approve | OPA-R-01 |
| IC-06 | release | OPA-R-01 |

---

## What this file does not do

This file does not write Rego. It does not embed a live amount cutoff. It does not sign BO-03, BO-06b, or BO-08.
