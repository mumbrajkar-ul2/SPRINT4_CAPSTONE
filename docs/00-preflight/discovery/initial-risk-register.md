# Initial risk register

| Field | Value |
|---|---|
| Stage | Phase 0 / 0A Pre-flight orientation |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `Project_Intent.md` section 17.1; `Execution_Plan.md` sections 3 and 11; `Decision_Tracker.md`; `operations/incidents/INC-2025-014.md`; `docs/historic-decisions.md`; `docs/correspondence/operations-vs-risk-2024.md`; `app/server.py`; `app/legacy_logic.py`; `legacy_js/legacy_policy.js`; `legacy_batch/shift_reconciliation.py`; `.github/workflows/verify.yml` |
| Assumptions | These are current-state risks. Likelihood is Inference from the files, not a measured rate. |
| Unresolved issues | INC-2025-014 still has no follow-up owner. Charter and KPI sign-off are unsigned. |
| Residual risks | This register is initial. Phase 1 will deepen the conflict catalogue. New risks may appear then. |

This file records current-state risks. It does not recommend a transformation.

## How to read the table

Each row states the finding, the evidence, the impact, the risk, the confidence, and the open questions. Likelihood and impact use High, Medium, or Low as Inference.

## Register

| ID | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| R-01 | Four rule programs disagree on urgency, open status, and totals | `app/legacy_logic.py` (50,000); `legacy_js/legacy_policy.js` (limit × 1.05, default 999,999); `legacy_batch/shift_reconciliation.py` (REVIEW treated as open); `legacy_java/ReconcileLegacy.java` (float sums, dropped blanks). Execution_Plan BP4 | Reports and queues will not match | High. Comparison claims can be false | High | Which source is canonical is already decided for later phases (FD-08). No Phase 0 action |
| R-02 | Sites and teams use different meanings of closed | `docs/correspondence/operations-vs-risk-2024.md`; `docs/business-context.md`; Execution_Plan BP5 | Open-case and aged-backlog counts can shift when the definition changes | High | High | BO-06a is DECIDED for operational meaning. BO-06b is still unsigned |
| R-03 | A replayed partner delivery already inflated the queue | `docs/historic-decisions.md` 2025 rollback; Execution_Plan BP2; `app/partner_feeds.py` REPLAY rows | Replay can create duplicate work | High | High | None for orientation |
| R-04 | Recipe revision differs between dispatch and equipment | `domain-profile.json` legacy note; Execution_Plan BP1; `docs/partner-feed-operations.md` | A lot can be judged on the wrong recipe | High | High | Recipe authority is later SME fact (BO-05, already DECIDED) |
| R-05 | Event time, arrival time, and effective date are separate and can be confused | `docs/source-systems-and-constraints.md`; Execution_Plan BP3 | A late metrology event can be treated as a current fact | High | High | None for orientation |
| R-06 | Untrusted text tells the reader to approve or ignore | `app/partner_feeds.py` injected note; Execution_Plan BP7 | A model or a person can treat a feed note as an instruction | High | High | FD-02 already limits the model to read-only tools |
| R-07 | The HTTP API has no authentication | `app/server.py` has no auth code; Execution_Plan BP8 | Anyone who can reach port 8080 can read cases | High on a shared network. Low on a closed laptop loopback | High | Identity design is a later Team-Force decision (FD-13) |
| R-08 | INC-2025-014 has no follow-up owner | `operations/incidents/INC-2025-014.md` | A disputed outage has no accountable person | Medium | High | Owner is Unknown. RT-06 assigns this at run time later. Do not invent a name now |
| R-09 | Finance and operations disagree on month-end cut-off | `docs/legacy-operations-history.md`; `docs/historic-decisions.md` 2024 | Cost and backlog reports can disagree | Medium | Medium | No signed cut-off owner |
| R-10 | Historical SLOs are unmeasured | `docs/operations-service-levels.md` | A 99.5% availability claim would be unsupported | Medium | High | No measured availability number exists |
| R-11 | A generate --reset command can replace the packaged baseline | `README.md`; `.github/workflows/verify.yml` | The frozen 125-case numbers would no longer match | High if the command is run | High | Who may run generate against this working copy is not named |
| R-12 | Charter and KPI sheet are unsigned | `Decision_Tracker.md` BO-01, BO-02 | Later phases can treat working answers as signed policy | Medium | High | Named signer is Unknown |
| R-13 | Synthetic cost numbers look like money | `app/baseline.py` mean_amount 4982.61; `operating_costs` hours | A reader can report a business saving that was never earned | High for the final defence | High | BO-11 working answer labels ROI EDUCATIONAL |

## Material finding

**Finding.** The largest current-state risks are rule disagreement, status-word disagreement, replay, untrusted text, and an unsigned charter.
**Evidence.** Rows R-01, R-02, R-03, R-06, R-12 and the files they cite.
**Impact.** Qualification can continue if those risks stay visible. They do not block orientation.
**Risk.** Hiding any of these rows would make later Go decisions look cleaner than the evidence.
**Confidence.** High.
**Open questions.** R-08 owner remains Unknown. R-12 signer remains Unknown.

## What this file does not do

This file does not rank a modernization option. It does not assign a new owner.
