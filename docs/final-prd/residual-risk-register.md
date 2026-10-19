# Residual risk register

| Field | Value |
|---|---|
| Stage | Phase 16 / Final as-built PRD |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p16-doc-20261018-001 |
| Status | COMPLETE. Residual risks stay open. Artifact UNSIGNED with the as-built baseline. |
| Evidence sources | `docs/final-prd/known-limitations.md`; `docs/final-prd/requirement-disposition-matrix.md`; `docs/00-preflight/discovery/initial-risk-register.md`; `docs/36-benefits/benefits-signoff.md`; `docs/30-release/go-no-go-criteria.md`; `Decision_Tracker.md` |
| Assumptions | Likelihood and impact use High, Medium, or Low as Inference unless a measured rate exists. |
| Unresolved issues | Named signer Unknown. Live Azure NEEDS_HUMAN. INC-2025-014 owner Unknown. |
| Residual risks | Treating this register as a closed risk file. Inventing a dollar benefit to retire R-16-03. |

This file records risks that remain after the as-built baseline. It does not add a feature. It does not invent a saving.

---

## Finding

**Finding.** The largest residual risks are an unsigned baseline, empty headline clocks, a guessed percent floor, an invented dollar benefit, a guessed incident owner, and a live Azure or Compose pass that was not run.
**Evidence.** BO-13 PROPOSED. After-KPI headline rows. TEVV floor cells. Benefits sign-off UNSIGNED. PH-S11-01. Paper rehearsal NEEDS_HUMAN.
**Impact.** A later reader can misuse a supporting integer as a business win.
**Risk.** Hiding any row below would make the baseline look finished.
**Confidence.** High on the empty cells. Inference on likelihood.
**Open questions.** Who signs BO-13. Who owns INC-2025-014.

---

## How to read the table

Each row states the finding, the evidence, the impact, the risk, the confidence, and the open questions. Likelihood and impact use High, Medium, or Low as Inference.

---

## Register

| ID | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| R-16-01 | BO-13 is PROPOSED. This pack is UNSIGNED | `Decision_Tracker.md` BO-13. `final-product-baseline-signoff.md` | Operations and audit have no signed owner for the as-built set | High. An unsigned baseline can be treated as signed policy | High | Named signer |
| R-16-02 | Exception cycle time and aged backlog stay Unknown | After-KPI headline rows. BO-02 | No headline business movement is measured | High. A reader can call open_cases 89 a cycle-time win | High | Start and end fields. Age in days |
| R-16-03 | No monetary benefit is claimed. Dollar cells stay Unknown | BO-11. `verified-benefits.md`. hours_per_case 0.603 SIMULATED | A later slide can book a saving that was never earned | High for a defence audience | High | Unit price. Wage. BO-11 signer |
| R-16-04 | Numeric percent floors stay Unknown | TEVV TV-26-01 to TV-26-05. FD-14. FD-18 | Release uses behaviour, not a 90 or 95 line | High if 42 of 42 is copied as a target | High | Whether a later owner wants a floor |
| R-16-05 | INC-2025-014 owner stays empty | PH-S11-01. HB-25-06 | A disputed outage still has no named person | Medium | High | Who RT-06 will name |
| R-16-06 | Company titles for RT-01 to RT-06 stay Unknown | `business-rules.md` title and person columns | A company roster cannot be printed | Medium | High | Company map |
| R-16-07 | Live Azure stays NEEDS_HUMAN | Paper rehearsal. Model card | A live-model claim would be unsupported | High if marked passed | High | Endpoint, deployment, API version |
| R-16-08 | Live seven-container recreate stays NEEDS_HUMAN | Phase 15 did not start Compose. GNG-30-02 | A room rehearsal can fail on a cold start | Medium | High | Who runs `docker compose up --build` |
| R-16-09 | Official Birlasoft assets have not arrived | BO-12. Placeholder deck | A final brand review cannot finish | Medium | High | Who supplies the files |
| R-16-10 | BO-03, BO-06b, and BO-08 stay PROPOSED | Tracker section 5 | A later author can treat 50,000 as live policy or merge three closure states | High if written into code | High | Signers for those rows |
| R-16-11 | Port 8080 still has no identity check | CT-35. GNG-30-05 | Anyone who can reach that port can read the baseline cases | High on a shared network. Low on laptop loopback | High | None for the baseline choice |
| R-16-12 | Application B can still be broken by an import of transformed code | ADR `adr-app-b-reads-only-the-lake.md` | A missing lake item would stop showing | Medium if a later edit lands | High | None if the ADR holds |
| R-16-13 | Capstone CI omits `generate --reset` | GNG-30-07 | Re-adding `--reset` would replace the packaged store | High if the command is run | High | Who may run generate on this copy |
| R-16-14 | Parity prints 12 matched and 2 differed | Scorecard. FD-17 | A later author can publish 12/14 as a percent | Medium | High | None. Do not publish a match percent |
| R-16-15 | Replay sentences are PRECOMPUTED | TEVV header. 77 files | A live model can spend tokens and change wording | Medium when Azure is later turned on | High | Live token cost |
| R-16-16 | Other PROPOSED BO rows stay unsigned | BO-02, BO-04, BO-10, BO-11, BO-12 | Working answers can be read as signed policy | Medium | High | Each artifact signer |

Worked example for R-16-03. hours_per_case is 0.603. Honesty: SIMULATED. Multiplying that field by a wage would invent a labor saving. This register forbids that claim.

Worked example for R-16-14. The harness print is `PARITY matched=12 differing=2`. Honesty: REAL. Dividing 12 by 14 would create a match percent the plan forbids.

---

## Material finding

**Finding.** The residual set is unsigned policy, empty headline clocks, empty money cells, empty percent floors, empty owner and title cells, and unrun live Azure and Compose steps.
**Evidence.** Rows R-16-01 to R-16-09.
**Impact.** The product can be demonstrated on replay with these risks visible.
**Risk.** Closing this register without a Business Owner signature.
**Confidence.** High.
**Open questions.** BO-13 signer. INC-2025-014 owner.

---

## What this file does not do

This file does not retire a risk by inventing a number. It does not sign BO-13. It does not invent a dollar benefit.
