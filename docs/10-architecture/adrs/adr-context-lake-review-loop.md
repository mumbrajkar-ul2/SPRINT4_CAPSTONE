# ADR: Context Lake review loop (default in force)

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | COMPLETE for documenting the default. FD-22 remains PENDING. Open for Phase 5. This unit does not decide FD-22. |
| Evidence sources | `Execution_Plan.md` sections 4, 5 (11R), and 11; `Decision_Tracker.md` FD-22; Phase 5 locked fact on lake version 1.0.0 |
| Assumptions | The tracker default holds until Phase 5 Team-Force decides FD-22. Version string 1.0.0 is that default start, not a new number invented here. |
| Unresolved issues | FD-22 PENDING for Phase 5: how the review, fix, and revision loop runs in detail, and how the version is raised. Reviewer identity for the lake round stays later. |
| Residual risks | Treating this ADR as a DECIDED FD-22 would skip the Phase 5 decision gate. Silent YAML edits after 1.0.0 would skip the version raise. |

This ADR records the default now in force for the Context Lake review loop. It does not decide FD-22.

---

## Default in force

**Verified Fact.** `Decision_Tracker.md` FD-22 PENDING. Default until decided:

1. One review round before Phase 6.
2. The version starts at 1.0.0.
3. A later change goes through the loop and raises the version with an ADR.

**Verified Fact.** `Execution_Plan.md` section 4. The Context Lake carries a version. A change goes through a review, a fix round, and a revision that raises the version and records an ADR. This is the Sprint 3 S03 review loop.

**Verified Fact.** `Execution_Plan.md` Phase 5 sub-stage 11R output: `context-lake/review/lake-review.md`, `lake-fixes.md`, `lake-version.md`.

This unit leaves FD-22 PENDING. Phase 5 is the owner.

---

## What Phase 5 still decides

FD-22 is Team-Force. Phase 5 must still settle:

| Topic | Why it is not settled here |
|---|---|
| Who performs the lake review | Not in the default sentence |
| What fails a review | Five contract gates are Phase 5 work (FD-07) |
| How a later phase files an "open question for the lake" | Channel is named in Phase 5. Procedure is not specified here |
| Whether a second review round can be required | Default is one round before Phase 6. FD-22 may keep or change that |
| How the version string steps (1.0.1 versus 1.1.0 versus 2.0.0) | Default says the version is raised. The step rule is not written |

This ADR does not fill those cells.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected as the default, or rejected for this unit |
|---|---|---|
| No version file | Application B would be built from unmarked YAML | The plan requires a version. Phase 5 locked fact starts at 1.0.0 |
| Silent YAML edits after the review | Change a rule with no ADR | `Execution_Plan.md` section 11: a later file that disagrees is fixed or gets an ADR |
| Zero review rounds before Phase 6 | Skip 11R | The default is one round. Zero would drop the Sprint 3 S03 practice |
| This unit deciding the full FD-22 policy | Freeze reviewers, bump rules, and fail criteria now | FD-22 is a Phase 5 decision. The coordinator's instruction is to mark it open for Phase 5 |
| Unlimited review rounds as a Phase 4 lock | Hold Phase 6 until many loops finish | The default is one round before Phase 6. Extra rounds would steal the remaining calendar |
| Version starting at 0.0.0 or unversioned drafts as the shipped lake | Application B built from a draft label | The default start is 1.0.0 |

Worked example. Phase 5 Half B runs `build.py`, runs tests, then runs one 11R round. Fixes are numbered in `lake-fixes.md`. `lake-version.md` is set to 1.0.0. Phase 6 may start. A missing term found in Phase 9 returns through the open-question channel. That later change raises the version and records an ADR. The bump rule itself is still FD-22.

---

## Why the default wins for a laptop demo

Phase 5 is already the largest knowledge build. One recorded review round is enough to show the S03 practice before specs start. A version string of 1.0.0 is what Application B later hashes and cites.

The default leaves room for Phase 5 to tighten the loop without this unit inventing a reviewer roster.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Phase 4 treated as FD-22 DECIDED | Status line: PENDING, open for Phase 5 |
| Skipping 11R | Phase 5 completion gate requires the review round and the version |
| Later silent edit | Section 11 rule: fix the file or write an ADR and raise the version |
| BO policy numbers sneaking into YAML as signed | PROPOSED rows stay labelled. This ADR does not sign them |

---

## Cost and token or runtime impact

One review round is reviewer time. It adds no run-time tokens.

A later version raise rebuilds `context-lake.sqlite3`. That is local CPU.

Honesty: review hours are Unknown. Start version 1.0.0 is the tracker default, not a measured artifact yet.

---

## Portability lesson

Ship the lake with a version file. Review it once before the next phase consumes it. Raise the version through a recorded loop when a later phase finds a missing term. Do not freeze the full loop policy in the architecture phase if the tracker still names it PENDING for the lake phase.

---

## Finding

**Finding.** The default in force is one review round before Phase 6, version starting at 1.0.0, and a later change going through the loop with an ADR. FD-22 stays PENDING for Phase 5.
**Evidence.** `Decision_Tracker.md` FD-22. `Execution_Plan.md` sections 4, 5, and 11.
**Impact.** Phase 5 runs 11R under this default unless FD-22 changes it.
**Risk.** Deciding FD-22 here would skip the Phase 5 gate.
**Confidence.** High that the default is correctly copied. Unknown on the detailed loop policy.
**Open questions.** FD-22. Reviewer identity. Version-step rule.

---

## What this ADR does not do

This ADR does not decide FD-22. It does not write `lake-version.md`. It does not start Phase 5. It does not sign a Business Owner row.
