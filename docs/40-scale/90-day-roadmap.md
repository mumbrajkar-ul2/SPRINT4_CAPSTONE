# 90-day roadmap

| Field | Value |
|---|---|
| Stage | Phase 15 / 40 Scale and roadmap. 90-day roadmap |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Days are calendar plans from 2026-10-18. Feature work stays out |
| Evidence sources | `Execution_Plan.md` Phase 16; `Decision_Tracker.md` BO-10, BO-11, BO-12, BO-13; `docs/36-benefits/benefits-signoff.md`; `docs/38-handover/operator-exercises.md`; FD-21 |
| Assumptions | Day 0 is 2026-10-18. The next build phase on the spine is Phase 16 Final As-Built PRD. This unit does not start Phase 16 |
| Unresolved issues | Signer names Unknown. Official brand assets have not arrived. Numeric floors Unknown |
| Residual risks | Starting Phase 16 in this unit. Booking EDUCATIONAL ROI as a quarter target |

This roadmap names the next 90 days of work that already has an owner or a missing signature. It adds no feature.

Engineering decision ED-P15-06, authority: team-force. The 90 days split into three 30-day blocks. Block 1 is Phase 16 plus live handover drills. Block 2 is signatures and brand restyle. Block 3 is measured floors if an owner names them.

---

## Finding

**Finding.** The spine's next phase is the Final As-Built PRD. Handover live Compose is still NEEDS_HUMAN. BO-10, BO-11, BO-12, and BO-13 stay PROPOSED. Official Birlasoft assets have not arrived. Dollar cells stay Unknown.
**Evidence.** `Execution_Plan.md` Phase 16. Tracker v1.28. This unit's handover sign-off UNSIGNED.
**Impact.** The quarter is signatures, classification of requirements, and a restyle when files arrive. It is not a second product.
**Risk.** Adding a ninth business problem in the quarter.
**Confidence.** High on the Phase 16 folder list. Unknown on when assets arrive.
**Open questions.** BO-12 asset date. BO-13 signer. Who runs the first live Compose drill.

---

## Days 1 to 30 (2026-10-19 to 2026-11-17)

| Item | Owner | Evidence already on disk | Live step |
|---|---|---|---|
| Phase 16 Final As-Built PRD | Later executor. Not this unit | Initial PRD, implementation PRD, specs, ADRs, TEVV, scorecard | Document phase |
| Classify each original requirement | Phase 16 | F-01 to F-15, FR-01 to FR-15 | None |
| Operator Exercise 1 D3 to D5 | Human with Docker | Written in `operator-exercises.md` | NEEDS_HUMAN |
| Keep `MODEL_MODE=replay` | Operator | FD-13. FD-21 | None |

This unit does not write `docs/final-prd/`.

---

## Days 31 to 60 (2026-11-18 to 2026-12-17)

| Item | Owner | State now | Label |
|---|---|---|---|
| Sign BO-10 compliance documents | Business Owner | PROPOSED. Unsigned | Unknown signer |
| Sign BO-11 benefits | Business Owner | `benefits-signoff.md` UNSIGNED. ROI EDUCATIONAL | EDUCATIONAL |
| Receive official Birlasoft assets and restyle the deck | Business Owner. BO-12 | Assets have not arrived. Placeholder in `docs/demo/` | Verified Fact |
| Assign INC-2025-014 owner | RT-06 | Packaged `owner_id` empty | Unknown person |
| Map company titles to RT-01 to RT-06 | Business Owner | Titles Unknown | Unknown |

If assets have not arrived by day 60, the placeholder deck stays the rehearsal deck. **Verified Fact** of BO-12 working answer.

---

## Days 61 to 90 (2026-12-18 to 2027-01-16)

| Item | Owner | Floor today | Label |
|---|---|---|---|
| Name a groundedness percent only if Team-Force measures a new run and records a floor | Team-Force | Unknown | Unknown |
| Name exception cycle time and aged backlog only if clocks and an age cutoff exist | Business Owner | Unknown | Unknown |
| Record an Azure invoice only if a person turned the live path on | Human who holds the key | No invoice on file | NEEDS_HUMAN. Dollars Unknown |
| Copy RC-01 to RC-08 into a second laptop if a later engagement exists | Team-Force | No second engagement on file | Assumption that one may exist |

No item in this block invents a 90 or 95 percent. No item books a dollar return.

---

## What the 90 days exclude

- New features.
- A third application.
- A live kill presented as a new demo result. The pid 29320 result stays the cited kill.
- A branded PowerPoint drawn from invented logos.
