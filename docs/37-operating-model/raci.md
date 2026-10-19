# RACI for the laptop solution

| Field | Value |
|---|---|
| Stage | Phase 15 / 37 Target operating model. RACI |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE for this unit. Roles only. Named people stay Unknown |
| Evidence sources | `docs/25-governance/accountability-map.md`; `docs/02-stakeholders/approval-authority-map.md`; `Decision_Tracker.md` sections 1 and 7; FD-13; FD-16; FD-21; FD-23; FD-24; BO-09; BO-11; BO-12 |
| Assumptions | One letter per cell. R means the role does the work. A means the role answers for the result. C means the role is asked. I means the role is told |
| Unresolved issues | Named people Unknown. Company titles Unknown. INC-2025-014 owner Unknown |
| Residual risks | Putting two A letters on one row. Filling a demo actor as the accountable person |

This table says who does each recurring duty. Letters are R, A, C, and I. Company titles stay Unknown.

Engineering decision ED-P15-02, authority: team-force. One Accountable letter per row. Delivery rows use Team-Force, SME, Business Owner, or Reviewer. Live-case rows use one RT id.

---

## Finding

**Finding.** Recurring duties already have owners in the accountability map. This page copies those owners into RACI letters. INC-2025-014 owner stays Unknown. The Business Owner stays Accountable for Group B sign-off. The Reviewer stays Accountable for accepting a Team-Force unit.
**Evidence.** HB-25-07 `CLOSED_ROLES` is RT-01 to RT-06. FD-24. BO-09. BO-12.
**Impact.** An operator can look up one row and see who acts.
**Risk.** Marking the model as Responsible for a write.
**Confidence.** High on the role ids. Unknown on people and titles.
**Open questions.** Who signs BO-12. Who owns INC-2025-014.

---

## Delivery and policy rows

| Duty | Team-Force | FDE SME | Business Owner | Reviewer | Model | Label |
|---|---|---|---|---|---|---|
| Change application code, tests, Compose | R / A | I | I | C | — | Verified Fact. FD-13 |
| Accept a finished unit | I | I | I | R / A | — | Verified Fact. FD-24 |
| Industry meaning of status, site, recipe, roles | C | R / A | I | I | — | Verified Fact. BO-09 |
| Sign charter, headline KPIs, ROI, brand | I | C | R / A | I | — | Verified Fact of the role. Artifacts UNSIGNED |
| Draft a cited sentence | C | I | I | I | R | Verified Fact. FD-04. Model is not A |
| Write a case, hold, or feed status | — | — | I | — | — | Verified Fact. Model has no write tool |
| Publish a match percent | — | — | — | — | — | Verified Fact. FD-17 forbids it |
| Claim a dollar return | — | C | A | — | — | Verified Fact. BO-11 PROPOSED. Claim is none |

Worked example. The model drafts a cited sentence for recipe R02 and R01 on `PS000000016`. The model is Responsible for the draft. RT-03 is Accountable for the hold. The model cell on the write row stays empty.

---

## Live-case rows

| Duty | RT-01 | RT-02 | RT-03 | RT-04 | RT-05 | RT-06 | Model | Label |
|---|---|---|---|---|---|---|---|---|
| Dispose HOLD_FOR_REVIEW | R / A | I | C | C | I | I | — | Verified Fact |
| Approve or hold an agent proposal | I | R / A | C | C | I | I | — | Verified Fact. Proposer is never approver |
| Recipe hold or release | I | C | R / A | I | I | I | — | Verified Fact. PH-S8-01 |
| Policy overlap pick | I | I | C | R / A | I | I | — | Verified Fact. PH-S10-01 |
| Confirm a replay duplicate | I | I | I | I | R / A | I | — | Verified Fact. PH-S7-01 |
| Assign INC-2025-014 owner | I | I | I | I | I | R / A | — | Verified Fact of the duty. Owner still Unknown |
| Read audit by correlation id | C | C | C | C | C | C | — | Verified Fact. FD-23 |
| Retry an injection BLOCK | — | — | — | — | — | — | — | Verified Fact. CON-29-01. No role retries BLOCK |

Worked example. `POST /api/agent/run` on `REPLAY-000000000` with `proposed_action=approve` and no corpus id. After Phase 12 SC-24-01 the reply is HTTP 409 BLOCK. Honesty: REAL. No RT role is offered a write button for that text.

---

## Gaps that stay open

| Gap | Missing fact | Do not invent |
|---|---|---|
| G-01 | Named signer of Business Owner artifacts | A person's name |
| G-02 | Company job titles for RT-01 to RT-06 | A local title |
| G-03 | INC-2025-014 follow-up owner | A person's name |
| G-05 | Person who supplies Birlasoft assets | A person's name |

**Verified Fact.** Those gap ids already sit in `docs/02-stakeholders/decision-rights-map.md`.
