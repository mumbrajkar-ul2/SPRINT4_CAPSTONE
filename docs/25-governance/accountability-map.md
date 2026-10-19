# Accountability map

| Field | Value |
|---|---|
| Stage | Phase 12 / 25 Governance and assurance. Half B evidence. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-25b-doc-20261018-001 |
| Status | MEASURED. HB-25-06 and HB-25-07 recorded. Named people stay Unknown. INC-2025-014 owner stays Unknown. |
| Evidence sources | `Decision_Tracker.md` sections 5 and 7; BO-09; BO-10; BO-03; `docs/12-specs/business-rules.md`; `docs/02-stakeholders/decision-rights-map.md`; `docs/02-stakeholders/approval-authority-map.md`; `docs/23-human-control/autonomy-matrix.md`; `apps/app_a/store.py`; `apps/app_b/fixtures/scenarios.yaml`; `apps/shared/identity.py`; packaged `enterprise_legacy.sqlite3` opened `mode=ro`; `operations/incidents/INC-2025-014.md` |
| Assumptions | BO-09 Group C roles stay in force. Company titles stay Unknown. INC-2025-014 owner stays Unknown until RT-06 assigns a supplied name. |
| Unresolved issues | Named signer stays Unknown. Company job titles stay Unknown. Named people stay Unknown. INC-2025-014 owner stays Unknown. |
| Residual risks | Writing a person's name into an owner cell would invent an owner. Coding a company title would skip the Business Owner title check. |

This file names who owns a duty. Delivery duties use Business Owner, FDE SME, Team-Force, and Reviewer. Live-case duties use RT-01 to RT-06. Named people stay Unknown. This file issues no compliance certificate.

Engineering decision ED-P12-25A-06, authority: team-force. Accountability rows use the existing RT-01 to RT-06 ids plus the four delivery parties. Half B recorded those ids. Half B did not invent a person.

---

## Finding

**Finding.** Policy and sign-off sit with Business Owner, SME, Team-Force, and Reviewer. One live case sits with RT-01 to RT-06. INC-2025-014 owner stays Unknown. Company titles stay Unknown. Half B read packaged `owner_id` as empty and `CLOSED_ROLES` as RT-01 to RT-06.
**Evidence.** BO-09 DECIDED, authority: sme. Group C. Gaps G-01, G-02, G-03 in `decision-rights-map.md`. Packaged incident `INC-2025-014` has an empty owner field. HB-25-06 and HB-25-07 Recorded sentences.
**Impact.** Register and model card owner cells use these ids. Half B confirmed the empty owner field.
**Risk.** Filling INC-2025-014 with `demo-rt06-1` as the real owner would invent a person.
**Confidence.** High on the role ids and on the empty owner field. Unknown on names and titles.
**Open questions.** BO-10 signer. Company titles. INC-2025-014 owner.

---

## Locked facts this design applies

**Verified Fact.** BO-09. The SME set the six fab exception-handling roles. The proposer of an action is never its approver. The Business Owner still confirms the company's own job titles.

**Verified Fact.** BO-10 working answer, still PROPOSED. Documents stay unsigned. The person's name stays Unknown.

**Verified Fact.** Group C. RT-01 to RT-06 apply fixed policy to one case. They do not change the governed policy.

---

## Delivery and policy owners

These rows decide or accept a governed rule. They are not a live-case click.

| Duty | Owner id | Owner role | Person | Company job title | Sign-off state |
|---|---|---|---|---|---|
| Charter | BO-01 | Business Owner | Unknown | Unknown | Accepted. Document unsigned |
| Headline KPIs | BO-02 | Business Owner | Unknown | Unknown | Accepted. Document unsigned |
| AI write risk | BO-03 | Business Owner | Unknown | Unknown | PROPOSED, accepted, unsigned |
| Compliance and data classification | BO-10 | Business Owner | Unknown | Unknown | PROPOSED, accepted, unsigned |
| Industry role map | BO-09 | FDE SME | Unknown | Unknown | DECIDED. Company titles still Unknown |
| Threat model, roles, hallucination rule | FD-18 | Team-Force | n/a for an agent | n/a | DECIDED 2026-10-18 |
| Accept this Half A | FD-24 | Reviewer agent | n/a for an agent | n/a | Not this executor's job |
| Silent threshold | BO-08 | Business Owner | Unknown | Unknown | PROPOSED. Case routes HOLD_FOR_REVIEW |

Worked example. A Team-Force agent wrote this file. That agent does not sign BO-10. The Business Owner role owns that signature. The person's name stays Unknown.

---

## Live-case owners

These rows apply the already-governed rule to one case. Owners use RT-01 to RT-06.

| Id | Live decision | SME role name | Company job title | Person | Who is refused | Lake item |
|---|---|---|---|---|---|---|
| RT-01 | Dispose a case that routed to HOLD_FOR_REVIEW | Fab Exception Reviewer | Unknown | Unknown | The model. The person who proposed the draft | `term.approval` |
| RT-02 | Approve, hold, or block an agent-proposed action | Shift Lead or Process Engineer (Approver) | Unknown | Unknown | The proposing agent. The same person as `proposed_by` | `rule.hold.person_only` |
| RT-03 | Approve a recipe-mismatch hold or release | Process Engineer | Unknown | Unknown | Operations Analyst acting alone. The model | `rule.recipe.mismatch_show_both` |
| RT-04 | Pick a policy on overlap, or keep the wait | Policy Owner | Unknown | Unknown | The model | `rule.policy.overlap_or_invalid` |
| RT-05 | Confirm a replay duplicate before it is dropped | Operations Analyst | Unknown | Unknown | An unattended job. The model | `rule.feed.replay_duplicate` |
| RT-06 | Assign the follow-up owner when none is recorded | Operations Lead | Unknown | Unknown | A made-up name. The model | `decision.inc_2025_014` |

Worked example. Scenario 8. Code shows recipe `R02` and `R01` on lot `L00000016`. Honesty of those ids: REAL. RT-03 records hold. The model does not write `engineering_hold`. The person who clicks stay Unknown until a real operator uses the screen.

Worked example. INC-2025-014. Packaged owner field is empty. Task `T-00000000` is unassigned. Honesty of those ids: REAL. RT-06 may assign a name that a person supplies. This map leaves the owner Unknown.

---

## Gaps carried forward

**Verified Fact.** `docs/02-stakeholders/decision-rights-map.md`.

| Gap | Missing fact | Do not invent |
|---|---|---|
| G-01 | Named signer of Business Owner artifacts | A person's name |
| G-02 | Company job titles for RT-01 to RT-06 | A local title |
| G-03 | INC-2025-014 follow-up owner | A person's name |
| G-04 | Person who may reset the packaged database | A person's name |
| G-05 | Person who supplies Birlasoft assets | A person's name |

---

## What the model may own

**Verified Fact.** FD-02. FD-04. BO-03 working answer.

The model may draft a cited sentence. The model may store `draft_plan` as a proposal. The model owns no write. The model owns no approval. The model owns no incident owner field.

Injection text owns no action. OPA returns BLOCK. No RT role is offered a write button for that text.

---

## Half B evidence this file names

| Check | What Half B records | Honesty when recorded |
|---|---|---|
| HB-25-06 | Packaged `INC-2025-014` owner field is still empty. This map still says Unknown | REAL |
| HB-25-07 | Runtime write routes still name RT-01 to RT-06 only | REAL |

### Recorded

Recorded 2026-10-18 under `corr-p12-25b-doc-20261018-001`. Half B did not type a person into the owner cell.

HB-25-06. Packaged INC-2025-014 `owner_id` is empty. `apps/app_a/store.py` SCENARIO_BINDINGS sets `owner_id` to None. `load_packaged()` returned `owner_id` None and `task_id` `T-00000000`. `apps/app_b/fixtures/scenarios.yaml` sets `owner_id: null`. Enterprise table `workflow_tasks` row `T-00000000` has `assigned_to` None. Incident file `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/operations/incidents/INC-2025-014.md` ends "Follow-up owner unknown." This map still says Unknown. Honesty: REAL.

HB-25-07. `CLOSED_ROLES` is exactly `('RT-01', 'RT-02', 'RT-03', 'RT-04', 'RT-05', 'RT-06')`. `ACTION_ROLE_MAP` still maps `dispose` to RT-01, `approve_agent` to RT-02, `recipe_hold_or_release` to RT-03, `policy_pick` and `keep_wait` to RT-04, `replay_confirm` to RT-05, and `assign_owner` to RT-06. Honesty: REAL.

---

## What this file does not do

This file maps duties to RT-01 to RT-06 and to the four delivery parties. Named people stay Unknown. It issues no compliance certificate. It does not write sub-stage 26.

STOP. Do not start sub-stage 26.
