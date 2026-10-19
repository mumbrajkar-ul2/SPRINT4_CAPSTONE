# Initial PRD traceability

| Field | Value |
|---|---|
| Stage | Phase 3 / 9 Initial PRD and product intent |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p3-doc-20261018-001 |
| Status | COMPLETE. BO-04 recorded as PROPOSED / unsigned. SME recommendation shown. |
| Evidence sources | `docs/09-initial-prd/initial-prd.md`; `docs/09-initial-prd/capability-map.md`; `docs/09-initial-prd/functional-requirements.md`; `docs/05-current-state/conflict-catalogue.md`; `docs/08-ai-qualification/qualification-decision.md`; `docs/08-ai-qualification/ai-vs-no-ai-matrix.md`; `Execution_Plan.md` sections 3, 8, 10; `Decision_Tracker.md` BO-04, section 5.1, FD-04, FD-05 |
| Assumptions | Feature ids F-01 to F-15 in the capability map are the feature set. Each functional requirement uses the same id. |
| Unresolved issues | BO-04 signer name is Unknown. Exception cycle time is Unknown. Aged backlog cutoff is Unknown. |
| Residual risks | A later feature row that cites no BP1 to BP8 number would fail the Phase 3 Done test. |

This file maps every feature to a business problem and to a Phase 1 or Phase 2 finding. It records BO-04 as PROPOSED. It shows the SME recommendation. It does not sign the row.

---

## BO-04 recorded as PROPOSED / unsigned

**Verified Fact.** `Decision_Tracker.md` BO-04 and section 5.2.

| Field | Value | Label |
|---|---|---|
| Tracker status | PROPOSED | Verified Fact |
| Business Owner review | Accepted on 2026-10-18 | Verified Fact |
| Signed DECIDED | No. `initial-prd.md` stays UNSIGNED | Verified Fact |
| Working answer | Approve the initial PRD once it names both apps, the AI limits, the eight business problems, and the demo flow, and nothing beyond | Verified Fact of the working answer |
| Signer name | Unknown | Unknown |
| Run paused | No. Explicit deferral of the signature | Verified Fact of the coordinator instruction in force for this unit |

SME recommendation from `Decision_Tracker.md` section 5.1. Shown here because the owner must see it beside the row.

| ID | SME recommendation | Why |
|---|---|---|
| BO-04 | Approve the initial PRD once it names both apps, the AI limits, the eight business problems, and the demo flow, and nothing beyond them. | Scope held to the evidenced defects keeps the build demoable on the laptop and honest. |

This file copies that recommendation. It does not invent a signer name. It does not mark BO-04 DECIDED.

Check that the working answer's four names are present:

| Required name | Where it sits | Present |
|---|---|---|
| Both applications | `initial-prd.md` section "The two applications". Application A reads rules from its rebuilt program. Application B reads rules only from the Context Lake | Yes |
| AI limits | `initial-prd.md` section "AI limits". BO-03, FD-04, FD-05 | Yes |
| Eight business problems | `initial-prd.md` section "The eight business problems in scope". BP1 to BP8 | Yes |
| Demo flow | `initial-prd.md` section "40-minute demo flow". Execution_Plan section 10 | Yes |
| Nothing beyond | `non-goals.md` and `mvp-scope.md`. No ninth problem | Yes |

---

## Feature to business problem to finding

Honesty for catalogue counts: REAL.

| Feature | Requirement | Business problem | Demo | Phase 1 or Phase 2 finding | Claim label |
|---|---|---|---|---|---|
| F-01 Recipe mismatch detection and approval route | FR-01 | BP1 | S8 | Phase 1 catalogue BP1: 91 of 125 process steps mismatch `recipe_version` and `recipe_rev`. Phase 2: compare in code, explain with a language model, person at RT-03 | Verified Fact |
| F-02 Replay duplicate detection and confirmation | FR-02 | BP2 | S7 | Phase 1 catalogue BP2: 67 REPLAY feeds. Phase 2: reconciliation and de-duplication are code | Verified Fact |
| F-03 Event time and arrival time kept apart | FR-03 | BP3 | S9 | Phase 1 catalogue BP3: 11,985 of 12,500 evidence events have different arrival and event times. 45 overlapping reference-version pairs | Verified Fact |
| F-04 One governed rule evaluation | FR-04 | BP4 | S12 | Phase 1 catalogue BP4: 2,090 REVIEW objects. Four programs disagree. Phase 2: rule evaluation is code | Verified Fact |
| F-05 Open and closed shown with one operational meaning | FR-05 | BP5 | S13 | Phase 1 catalogue BP5: 89 of 125 cases not CLOSED. Five status word lists | Verified Fact |
| F-06 Overlapping policy detect and abstain | FR-06 | BP6 | S10 | Phase 1 catalogue BP6: 34 active policies, 4 or 5 per country code, three region vocabularies. Phase 2: detect in code, wait for a person | Verified Fact |
| F-07 Untrusted text isolated as data | FR-07 | BP7 | Control on S7 to S11. Minutes 36 to 39 | Phase 1 catalogue BP7: 86 feeds, 150 lake events, 3 emails, 22 source documents. Phase 2: strings stay data | Verified Fact |
| F-08 Identity, owner assignment, recovery status | FR-08 | BP8 | S11 | Phase 1 catalogue BP8: no identity check in `app/server.py`. 695 unassigned tasks. INC-2025-014 owner Unknown | Verified Fact for 695 and missing auth. Unknown for the owner |
| F-09 Queue ranking from stored fields | FR-09 | BP4, BP5 | Queue under S7 to S11 | Phase 2 triage row: ranking is code on status, severity, and amount. Phase 1 BP4 and BP5 are the queue defects | Verified Fact |
| F-10 Cited conflict explanation | FR-10 | BP1 to BP7 | S7 to S11 | Phase 2 conflict-explanation row: GenAI. Phase 1 counts for ten disagreement types | Verified Fact for the counts |
| F-11 Cited natural-language answer | FR-11 | BP1 to BP8 | S7 to S13 | Phase 2 natural-language-query row: GenAI. Intent 15.2 seven jobs. No query log | Verified Fact for the seven jobs |
| F-12 Draft investigation plan, then wait | FR-12 | BP1, BP2, BP6, BP8 | Minutes 13 to 25 | Phase 2 agentic-planning row: GenAI draft. BO-03 working answer. RT-02 | Verified Fact |
| F-13 Person on every record-changing action | FR-13 | BP1, BP2, BP6, BP8 | Approval gate | Phase 2 `minimum-agency-assessment.md`. BO-03 PROPOSED. Catalogue write-risks on BP1, BP2, BP7, BP8 | Verified Fact of the working answer |
| F-14 Same-scenario run on both applications | FR-14 | BP4, BP5 | S13 | Phase 1 BP4 four rule files and BP5 five status lists are the disagreements parity must expose. Execution_Plan section 8 maps S13 to BP4 and BP5 | Verified Fact |
| F-15 Rule lineage in the Application B context view | FR-15 | BP4 | S12 | Phase 1 catalogue BP4 four implementations. Execution_Plan section 8 maps S12 to BP4 | Verified Fact |

Worked example. F-01 maps to BP1. The Phase 1 finding is 91 mismatches of 125. The Phase 2 finding is: the compare stays in code, the sentence may come from a language model, the write waits for RT-03.

Every feature row above has a BP1 to BP8 number. No row cites a ninth problem.

---

## Business problem coverage

| Problem | Features that handle it | Demo scenario in Execution_Plan section 8 |
|---|---|---|
| BP1 | F-01, F-10, F-11, F-12, F-13 | 8 Recipe mismatch |
| BP2 | F-02, F-10, F-11, F-12, F-13 | 7 Replay inflation |
| BP3 | F-03, F-10, F-11 | 9 Late metrology |
| BP4 | F-04, F-09, F-10, F-11, F-14, F-15 | 12 Rule trace. 13 Both apps |
| BP5 | F-05, F-09, F-11, F-14 | 13 Both apps |
| BP6 | F-06, F-10, F-11, F-12, F-13 | 10 Overlapping policies |
| BP7 | F-07, F-10, F-11 | No own section 8 row. Control on S7 to S11. Minutes 36 to 39 |
| BP8 | F-08, F-11, F-12, F-13 | 11 Outage or schema mismatch |

Each of BP1 to BP8 has at least one feature. BP7 is in the product even though section 8 gives it no own scenario row.

---

## Phase 2 intelligence labels carried into the PRD

**Verified Fact.** FD-04 DECIDED. FD-05 DECIDED.

| Capability from Phase 2 | PRD feature | Label kept |
|---|---|---|
| Triage | F-09 | Code |
| Conflict explanation | F-10 | Language model |
| Natural-language query | F-11 | Language model |
| Agentic planning | F-12 | Language model, then a person |
| Rule evaluation | F-04 | Code |
| Reconciliation | F-02 | Code |
| Intake de-duplication | F-02 | Code |
| `engineering_hold` prediction | Non-goal | ML-rejected. 117/125 versus 117/125 |

---

## Done-test checklist for this unit

Open this file. Then open `initial-prd.md`.

| Check | Result |
|---|---|
| Every feature row maps to a business problem BP1 to BP8 | Yes. F-01 to F-15 |
| `initial-prd.md` names Application A | Yes |
| `initial-prd.md` names Application B | Yes |
| `initial-prd.md` names the 40-minute flow | Yes. Execution_Plan section 10 time boxes |
| No requirement adds scope beyond the eight problems | Yes. See `non-goals.md` and the coverage table |
| BO-04 signed or explicitly deferred | Explicitly deferred. PROPOSED. UNSIGNED. SME recommendation shown |

---

## What this file does not do

This file does not edit `Decision_Tracker.md`. It does not sign BO-04. It does not start Phase 4.
