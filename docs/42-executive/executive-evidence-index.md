# Executive evidence index

| Field | Value |
|---|---|
| Stage | Phase 15 / 42 Executive defence. Evidence index |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Every material claim in the script maps to a file |
| Evidence sources | The paths in the table. FD-21 |
| Assumptions | A judge opens the path and reads the labelled number. This index does not copy the full sheets |
| Unresolved issues | Live Compose health today Unknown |
| Residual risks | A slide that cites this index and then drops the label |

This index maps each material claim in the 39-minute script to a file already on disk.

---

## Finding

**Finding.** The script's counts, BLOCK row, kill row, harness integers, freeze print, and Unknown cells each have a source file. Official brand files are absent. A live Compose pass from this unit is absent.
**Evidence.** Tables below.
**Impact.** A reviewer can check a claim without trusting the slide text.
**Risk.** Pointing at a Phase 8 paste as if it were a Phase 15 health check.
**Confidence.** High on the path list. Unknown on today's containers.
**Open questions.** Who pastes the first live health after handover.

---

## Claims in the script

| Claim | Label | Source file |
|---|---|---|
| records 125, open_cases 89, urgent_cases 2, sites 6 | REAL | `docs/model-comparison/scorecard.md`; Phase 0 baseline JSON |
| mean_amount 4982.61, hours_per_case 0.603 | SIMULATED | Same scorecard |
| Exception cycle time, aged backlog | Unknown | Same scorecard. BO-02 |
| 91 recipe mismatches, 67 REPLAY feeds | REAL | `docs/09-initial-prd/initial-prd.md` |
| 11,985 clock mismatches, 2,090 REVIEW objects | REAL | Same PRD |
| 89 open cases, 34 policies, 86 untrusted notes, 695 unassigned tasks | REAL | Same PRD |
| 125 lots, 8 held, 117 not held, 117/125 both models | REAL | `docs/08-ai-qualification/qualification-decision.md` |
| Lake 1.0.0, 148 items, 180 edges, 267 term rows | REAL | `docs/_playbook-log.md` Phase 5 |
| Ports 8080, 8090, 8091, 8092, 8100, 8110 | Verified Fact | `compose.yaml`; FD-13 |
| `MODEL_MODE=replay` default | Verified Fact | `compose.yaml`; FD-13; FD-21 |
| 77 replay files besides README | REAL on 2026-10-18 | `operations/model-replay/` |
| S7 `REPLAY-000000000` | REAL | `apps/app_a/eval/freeze-set.yaml`; PH-S7-01 |
| S8 `PS000000016` R02 / R01 | REAL | PH-S8-01 |
| S9 `E-00000000` clocks 2020-12-30 / 2021-01-01 | REAL | PH-S9-01 |
| S10 `FAB-00000002` five policy ids | REAL | PH-S10-01 |
| S11 `INC-2025-014` owner empty | REAL empty field. Owner Unknown | HB-25-06; `operations/incidents/INC-2025-014.md` |
| Harness 14 rows, matched 12, differing 2 | REAL. No percent | `docs/model-comparison/scorecard.md`; `parity-results.json` |
| Freeze `rows=42 pass=42 fail=0` | REAL. Floor Unknown | `docs/26-tevv/tevv-results.md` |
| Grounded 42 of 42, recall 40 of 41, precision 79 of 79, abstain 6 of 42 | REAL. Floor Unknown | Same TEVV sheet |
| Replay tokens 0 and 0 on the shown path | REAL for that path | Phase 14 scorecard |
| ROI cells | EDUCATIONAL | `docs/36-benefits/roi-model.md` |
| Monetary benefit claimed none | Verified Fact | `docs/36-benefits/benefits-signoff.md` UNSIGNED |
| Quotes-plus-approve HTTP 409 BLOCK | REAL prior | `docs/24-security-privacy/security-test-results.md` |
| Application B same BLOCK after SC-26-01 | REAL prior | `docs/26-tevv/tevv-results.md` |
| pid 29320 kill. `corr-p10b-kill-20261018-001` on `PS000000016`. `engineering_hold` 0 | REAL prior | `docs/_playbook-log.md` Phase 10 |
| Company titles | Unknown | `docs/02-stakeholders/stakeholder-map.md` |
| Official Birlasoft assets | Have not arrived. BO-12 PROPOSED | `Decision_Tracker.md` |
| Live `docker compose up` in Phase 15 | NEEDS_HUMAN. Not run | `docs/38-handover/operator-exercises.md` |
| Characterization 70 passed | REAL prior | `docs/_playbook-log.md` Phase 7 |
| Phase 8 8080 and 8090 health paste | REAL on 2026-10-18. Not this unit | `docs/_playbook-log.md` Phase 8 |

---

## Demo folder

| File | What it is |
|---|---|
| `docs/demo/README.md` | Neutral placeholder notice. BO-12 pending |
| `docs/demo/placeholder-deck.md` | Slide text. No logo. No signer |
| `docs/demo/paper-rehearsal.md` | Timed walk. 39 minutes. No audience |

---

## What this index does not point at

- A branded PowerPoint file. Official assets have not arrived.
- A Phase 15 kill log. None was written.
- An Azure invoice. None is on file.
