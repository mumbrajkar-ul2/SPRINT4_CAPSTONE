# Decision rights after handover

| Field | Value |
|---|---|
| Stage | Phase 15 / 37 Target operating model. Decision rights |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE for this unit. Same four parties as 0B. PROPOSED Business Owner rows stay unsigned |
| Evidence sources | `docs/00-preflight/operating-contract/provisional-operating-contract.md`; `docs/02-stakeholders/decision-rights-map.md`; `Decision_Tracker.md` sections 1, 4, 5, and 7; FD-21; FD-24; BO-11; BO-12 |
| Assumptions | The 0B rights split stays the source. This page does not add a fifth party |
| Unresolved issues | Named signer Unknown. Company titles Unknown. INC-2025-014 owner Unknown |
| Residual risks | A later file that moves a Group B row to Team-Force. A later file that lets the model approve a write |

This page is the steady-state rights map. It matches the 0B split. Industry expertise does not transfer company liability.

---

## Finding

**Finding.** Team-Force still owns engineering. The SME still owns industry fact. The Business Owner still owns company liability. Run-time roles still own one live case. FD-21 is DECIDED. BO-11 and BO-12 stay PROPOSED.
**Evidence.** `Decision_Tracker.md` v1.28. Phase 0 decision-rights map. FD-21 text in the tracker.
**Impact.** Handover does not change who may decide.
**Risk.** Treating an accepted PROPOSED row as a signed policy number in code.
**Confidence.** High on the four parties. Unknown on the signer.
**Open questions.** Who signs BO-11 and BO-12.

---

## Rights matrix

| Decision class | Example already on disk | Owner | Status now | Label |
|---|---|---|---|---|
| Engineering / method | Demo flow, replay mode, lessons | Team-Force | FD-21 DECIDED 2026-10-18 | Verified Fact |
| Engineering / method | Lake schema, ports, OPA, audit columns | Team-Force | FD-07, FD-13, FD-16, FD-23 DECIDED | Verified Fact |
| Industry fact | REVIEW and HOLD are open. Site is the canonical key | FDE SME | BO-05, BO-06a, BO-07, BO-09 DECIDED | Verified Fact |
| Company liability | Headline KPIs, ROI label, brand assets | Business Owner | BO-02, BO-11, BO-12 PROPOSED | Verified Fact of status |
| Live case | One hold on `PS000000016` | RT-03 | Role assigned. Person Unknown | Unknown person |
| Team-Force output accept | This Phase 15 unit | Reviewer | FD-24 DECIDED | Verified Fact |
| Policy value missing | Silent amount cutoff | No one invents it | BO-08 PROPOSED. Case routes HOLD_FOR_REVIEW | Verified Fact |

Worked example. PH-RANK-02. Application A queue body has no amount cutoff label. Application B labels demo 50000 as `proposed`. Live silent cutoff stays HOLD_FOR_REVIEW. Honesty: REAL from the Phase 14 scorecard.

---

## What each party may not decide

| Party | Out of this party's rights | Label |
|---|---|---|
| Team-Force | Sign a Business Owner row. Invent a company title. Invent a dollar return | Verified Fact |
| FDE SME | Take company finance liability. Name a Birlasoft signer | Verified Fact |
| Business Owner | Pick the lake schema. Change the OPA rule file | Verified Fact |
| Reviewer | Sign BO-11 or BO-12 | Verified Fact. FD-24 |
| Run-time role | Change the governed policy archive | Verified Fact. Group C |
| Model | Approve a write. Own INC-2025-014 | Verified Fact. FD-02. BO-03 working answer |

---

## Reconciliation with 0B

| 0B statement | This page | Result |
|---|---|---|
| Team-Force owns engineering | Same | Match |
| SME owns industry fact | Same | Match |
| Business Owner owns liability | Same | Match |
| Run-time roles own one live case | Same | Match |
| Unresolved owners flagged, not invented | Same. G-01 to G-05 still open | Match |
| Contract unsigned | Closure file stays UNSIGNED | Match on signature. Status of the delivery contract is closed in `operating-contract-closure.md` |

**Verified Fact.** Closing the delivery contract does not invent a signer. The owner name stays Unknown.
