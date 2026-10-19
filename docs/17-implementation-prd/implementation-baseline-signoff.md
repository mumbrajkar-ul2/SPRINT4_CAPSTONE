# Implementation baseline signoff

| Field | Value |
|---|---|
| Stage | Phase 8 / 17 Implementation PRD. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | UNSIGNED. BO-04 is PROPOSED, accepted 2026-10-18, not signed DECIDED. Other Business Owner rows that are PROPOSED stay PROPOSED. |
| Evidence sources | BO-04; `Decision_Tracker.md` sections 5.1 and 5.2; `docs/09-initial-prd/initial-prd.md`; `docs/17-implementation-prd/implementation-prd.md`; `docs/17-implementation-prd/prd-change-log.md` |
| Assumptions | The accepted working answer is the text below. The owner has not signed this file. |
| Unresolved issues | Named signer Unknown. Headline KPI values Unknown. No target set. FD-13 stays DEFERRED until HALF_A_ACCEPTED. |
| Residual risks | Treating this page as a signed baseline would hide the PROPOSED status. |

This is the BO-04 sign-off sheet for the implementation PRD. The Business Owner accepted the working answer on 2026-10-18. The owner has not signed this file. A Business Owner row that is still PROPOSED keeps this artifact unsigned.

---

## Finding

**Finding.** The implementation PRD names both applications, the AI limits, the eight business problems, and the demo flow, and it adds only platform facts needed to build that product. The owner has not signed.
**Evidence.** `implementation-prd.md`. `Decision_Tracker.md` BO-04 and section 5.2.
**Impact.** The run does not pause. Half B may start after HALF_A_ACCEPTED. Policy numbers stay out of code.
**Risk.** Marking this file signed would invent a signer name.
**Confidence.** High on the unsigned status. Unknown on the signer name.
**Open questions.** Signer name. Coordinator record of FD-13 after acceptance.

---

## SME recommendation (mandatory to show)

**Verified Fact.** `Decision_Tracker.md` section 5.1 for BO-04.

Approve the initial PRD once it names both apps, the AI limits, the eight business problems, and the demo flow, and nothing beyond them. Scope held to the evidenced defects keeps the build demoable on the laptop and honest.

The implementation PRD keeps that four-part bound. Platform rows (ports, headers, compose, CI, logs, replay) serve those four parts. They do not add a ninth business problem.

---

## Working answer the owner accepted

**Verified Fact.** Section 5.2 Accept on 2026-10-18.

Approve the initial PRD once it names both applications, the AI limits, the eight business problems, and the demo flow, and nothing beyond.

| Required name | Where it still sits | Present |
|---|---|---|
| Both applications | `implementation-prd.md` section "What the Initial PRD still requires" | Yes |
| AI limits | Same file. FD-04, FD-05, BO-03 working answer | Yes |
| Eight business problems | Same file. FR-01 to FR-15 disposition. No ninth problem | Yes |
| Demo flow | Execution_Plan section 10. Replay wiring named | Yes |
| Nothing beyond | `release-boundaries.md` out-of-release list | Yes |

---

## What is frozen as engineering

These lines are team-force records. They are not a Business Owner signature.

| Item | Frozen value | Signed by the owner? |
|---|---|---|
| Product bound | BP1 to BP8. Scenarios 7 to 13. Two applications | No. BO-04 unsigned |
| AI split | FD-04 DECIDED. Hold predictor rejected (FD-05) | No. BO-03 unsigned |
| Four locked listeners | 8080, 8090, 8091, 8092 | No. FD-06 is team-force |
| Two app host ports | 8100, 8110 | No. ED-P8A-01 team-force |
| Identity scaffolding | Three headers. `FABPULSE_API_KEY`. Default `local-demo-only` | No. ED-P8A-02 team-force |
| Replay | `MODEL_MODE=replay`. Hash-of-prompt files | No. Section 10 already stated this |
| Numeric SLO percents | Unknown | n/a |
| Headline KPI values | Unknown | No. BO-02 unsigned |

---

## Business Owner rows that keep this file unsigned

**Verified Fact.** `Decision_Tracker.md` section 5. Each row below stays PROPOSED.

| ID | Why it blocks a signature on this sheet |
|---|---|
| BO-04 | This sheet is the implementation PRD sign-off. The owner has not signed the artifact DECIDED |
| BO-02 | Headline KPI pair is accepted as a working answer. Values stay Unknown |
| BO-03 | AI-risk bound is accepted as a working answer. It is not signed code |
| BO-06b | Three closure states stay a working answer |
| BO-08 | Silent-threshold rule stays a working answer. 50,000 stays PROPOSED |
| BO-10 | Classification stays a working answer. Phase 12 still owns the row |
| BO-11 | ROI honesty stays a working answer |
| BO-12 | Brand assets stay later |
| BO-13 | Final as-built baseline stays later |

SME rows BO-05, BO-06a, BO-07, and BO-09 are already DECIDED. They do not sign this Business Owner sheet.

---

## Executor record

| Item | Value |
|---|---|
| Unit | Phase 8 Half A |
| Executor read | PASS for the design unit. The reviewer makes the real call |
| Authority of this line | team-force record only. Not the reviewer grade. Not a Business Owner signature |
| Date | 2026-10-18 |
| Correlation id | corr-p8a-doc-20261018-001 |
| Owner signature | Blank |
| Owner name | Unknown |

Phase 8 Half B is not started.

---

## What the owner is not asked to sign here

The owner is not asked to sign FD-13. That row is team-force engineering.

The owner is not asked to sign 8100, 8110, or the header names.

The owner is not asked to invent a cycle-time number or an availability percent.

---

## What this file does not do

This file does not invent a signer name. It does not mark BO-04 DECIDED. It does not update `Decision_Tracker.md`. It does not start Half B.
