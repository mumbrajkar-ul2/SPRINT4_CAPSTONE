# Executive narrative

| Field | Value |
|---|---|
| Stage | Phase 15 / 42 Executive defence. Narrative |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Every material claim labelled. BO-12 stays PROPOSED |
| Evidence sources | `docs/03-problem-value/problem-statement.md`; `docs/09-initial-prd/initial-prd.md`; `docs/model-comparison/scorecard.md`; `docs/_playbook-log.md`; FD-04; FD-05; FD-21; BO-11; BO-12 |
| Assumptions | The audience is a smart adult who has not studied this product. Official Birlasoft assets have not arrived |
| Unresolved issues | Company titles Unknown. INC-2025-014 owner Unknown. ROI dollars Unknown. Headline KPI values Unknown |
| Residual risks | Hearing 42 of 42 as a 90 percent target. Hearing 12 matched rows as a business win. Hearing EDUCATIONAL ROI as cash |

This narrative is the spoken story for the defence. Numbers keep their honesty labels. The deck beside it is a neutral placeholder.

---

## Finding

**Finding.** Fabpulse cannot consistently explain or close a fab-lot or equipment exception when feeds, local rules, archived documents, and month-end reports disagree. The build is two applications on one laptop. Ranking and rules stay in code. The model drafts cited sentences and waits. Injection returns HTTP 409 BLOCK. An approval kept its correlation id after pid 29320 was killed. ROI stays EDUCATIONAL. Headlines stay Unknown.
**Evidence.** Problem statement. FD-04. FD-05. Phase 12 HB-24-01. Phase 10 kill. Phase 14 scorecard.
**Impact.** A 39-minute paper walk can tell that story without a new live kill and without a dollar claim.
**Risk.** A slide that drops the honesty label.
**Confidence.** High on the measured rows. Unknown on headlines and dollars.
**Open questions.** BO-12 assets. BO-11 signer. INC-2025-014 owner.

---

## The problem

Fabpulse Group handles fab-lot and equipment exceptions. External messages, process records, policy versions, case workflows, archived documents, and local rule programs do not always agree.

**Verified Fact.** Operators then spend extra time reconciling. Queues grow. Two teams can report a different open count for the same week. A disputed outage can sit with no owner.

Worked example. INC-2025-014. On 2025-11-18 a partner feed was delayed. The queue was retried twice. Downstream totals diverged. Staff used a spreadsheet at 04:00 UTC. Follow-up owner unknown. Honesty of that file: REAL as packaged text. The owner field stays Unknown.

---

## What was built

| Piece | What the user sees | Label |
|---|---|---|
| Application A on port 8100 | Queue, case evidence, agent draft, approval gate, recovery list | Verified Fact. FD-13 |
| Application B on port 8110 | The same workflow, plus the lake item behind a rule | Verified Fact. FD-06 |
| Context Lake 1.0.0 | 148 items, 180 edges, 267 term rows | REAL. Phase 5 |
| Replay mode | Saved answers play back. No network call | Verified Fact. FD-21. 77 files besides README |

The model does not write a case, a hold, or a feed status. **Verified Fact.** FD-02. BO-03 working answer.

---

## What the defence will show

1. The eight business problems and the packaged baseline. records 125, open_cases 89, urgent_cases 2, sites 6. Honesty: REAL. mean_amount 4982.61 SIMULATED. hours_per_case 0.603 SIMULATED.
2. The code-versus-model split. Hold prediction rejected. 117/125 majority. 117/125 leave-one-out. Honesty: REAL. Phase 2.
3. Application A scenarios 7 to 11 on replay.
4. Application B on the same cases, plus one rule trace.
5. The scorecard. 14 harness rows, 12 matched, 2 differed. No match percent. ROI EDUCATIONAL.
6. One injection that returned HTTP 409 BLOCK. Phase 12. One approval that kept `corr-p10b-kill-20261018-001` on `PS000000016` after pid 29320 was killed. Phase 10.
7. Five lessons. Each cites a phase that already ran.

`docker compose up` for a live show is NEEDS_HUMAN. This narrative does not invent that pass.

---

## What this narrative will not say

- A named company title for RT-01 to RT-06.
- A named owner for INC-2025-014.
- A dollar benefit.
- A numeric floor of 90 or 95.
- That official Birlasoft brand files are on disk.
- That a new process kill was run in Phase 15.
