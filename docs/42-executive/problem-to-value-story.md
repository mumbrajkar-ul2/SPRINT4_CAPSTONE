# Problem-to-value story

| Field | Value |
|---|---|
| Stage | Phase 15 / 42 Executive defence. Problem to value |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Value claims labelled. Monetary benefit claimed: none |
| Evidence sources | `docs/03-problem-value/problem-statement.md`; `docs/09-initial-prd/initial-prd.md`; `docs/35-value-leakage/before-after-analysis.md`; `docs/36-benefits/roi-model.md`; `docs/model-comparison/scorecard.md`; BO-02; BO-11; FD-20 |
| Assumptions | Value on this page is the labelled change a judge can re-run. It is not a booked return |
| Unresolved issues | Exception cycle time Unknown. Aged backlog Unknown. Dollars Unknown |
| Residual risks | Reading 0.603 hours as recovered labor. Reading 12 matched rows as a finance win |

This page walks problem, solution, and measured result. Every number keeps its honesty label.

---

## Finding

**Finding.** The problem is inconsistent exception close-out across eight defects. The solution is two applications, a versioned lake, human approval, and replay. The measured result is labelled counts, a 12-and-2 harness, HTTP 409 BLOCK, and a surviving correlation id. Headline cycle time stays Unknown. ROI stays EDUCATIONAL. No monetary benefit is claimed.
**Evidence.** Phase 0 problem statement. Phase 3 PRD. Phase 12 and Phase 10 results. Phase 14 scorecard and benefits sign-off.
**Impact.** The 39-minute walk can show value without a dollar slide.
**Risk.** A listener who converts EDUCATIONAL to cash.
**Confidence.** High on the supporting counts. Unknown on headlines and dollars.
**Open questions.** BO-11 signer. Age cutoff. Unit price.

---

## Problem

**Verified Fact.** Eight defects are in scope. No ninth defect was added.

| ID | What operators meet | Packaged count | Honesty |
|---|---|---|---|
| BP1 | Recipe revision on a step differs from the tool | 91 of 125 steps | REAL |
| BP2 | A replayed delivery creates extra queue work | 67 REPLAY feeds | REAL |
| BP3 | Event time and arrival time are mixed | 11,985 of 12,500 evidence events | REAL |
| BP4 | Four local rule programs disagree | 2,090 REVIEW objects | REAL |
| BP5 | Open and closed mean different things | 89 of 125 cases `status != CLOSED` | REAL |
| BP6 | Region words and policies overlap | 34 active policy rows | REAL |
| BP7 | Untrusted text tells a reader to approve or ignore | 86 partner feeds with that language | REAL |
| BP8 | No access control. Ownership disputed. Recovery manual | 695 tasks with no assignee. INC-2025-014 owner Unknown | REAL counts. Owner Unknown |

---

## Solution

**Verified Fact.** FD-04 and FD-05.

| Job | How it is done | What a person still does |
|---|---|---|
| Rank the queue | Code on status, severity, and amount | Opens the next case |
| Evaluate a rule | Code against the governed archive | Waits when the archive is silent |
| Mark a replay | Code on REPLAY status | RT-05 confirms before drop |
| Explain a conflict | Model drafts a cited sentence | Reads both values |
| Approve a write | Model proposes. OPA gates | RT-01 to RT-06 records the write |
| Predict `engineering_hold` | Rejected | No scorer is built |

Worked example. Lot L00000016. Process step recipe R02. Tool recipe R01. Code raises the mismatch. A Process Engineer at RT-03 records hold. The model does not write `engineering_hold`. Honesty of the pair: REAL from PH-S8-01.

---

## Impact that is measured

| Result | Before | After | Honesty |
|---|---|---|---|
| records | 125 | 125 | REAL |
| open_cases | 89 | 89 | REAL for `status != CLOSED` |
| urgent_cases | 2 | 2 | REAL |
| sites | 6 | 6 | REAL |
| mean_amount | 4982.61 | 4982.61 | SIMULATED |
| hours_per_case | 0.603 | 0.603 | SIMULATED |
| Harness rows | n/a at Phase 0 | 14 rows, 12 matched, 2 differed | REAL |
| Injection quotes-plus-approve | HTTP 200 wait before SC-24-01 | HTTP 409 BLOCK | REAL |
| Approval after process kill | n/a | `corr-p10b-kill-20261018-001` stayed on `PS000000016`. `engineering_hold` stayed 0 | REAL |
| Exception cycle time | Unknown | Unknown | Unknown |
| Aged backlog | Unknown | Unknown | Unknown |
| ROI dollars | Unknown | Unknown | EDUCATIONAL |
| Monetary benefit claimed | None | None | Verified Fact |

Worked example. Python `open_cases` is 89 before and 89 after. The product did not invent a drop in open count. Aged backlog stays Unknown because an age threshold is still unnamed.

---

## Business-and-technical balance

| Minute block in the paper walk | Business content | Technical content |
|---|---|---|
| 0:00 to 7:00 | Eight defects. Baseline six fields | Honesty labels |
| 7:00 to 12:00 | Why hold prediction was rejected | 117/125. FD-04 split |
| 12:00 to 24:00 | Scenarios 7 to 11 as operator jobs | Agent trace. Approval gate |
| 24:00 to 31:00 | Same jobs on Application B | Lake item behind the rule |
| 31:00 to 35:00 | Scorecard. No dollar claim | 12 matched. 2 differed. Cite the lake |
| 35:00 to 38:00 | Untrusted text cannot close a case. A wait survives a crash | HTTP 409. pid 29320 |
| 38:00 to 39:00 | Five lessons | Each cites a phase |

**Verified Fact.** FD-21. The walk follows section 10 content. The paper clock sums to 39 minutes.
