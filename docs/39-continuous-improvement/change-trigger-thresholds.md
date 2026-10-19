# Change-trigger thresholds

| Field | Value |
|---|---|
| Stage | Phase 15 / 39 Drift and continuous improvement. Thresholds |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Behaviour triggers are DECIDED from earlier FD rows. Numeric percent floors stay Unknown and PROPOSED where unnamed |
| Evidence sources | FD-14; FD-17; FD-18; FD-19; FD-22; BO-08; BO-11; `docs/26-tevv/release-thresholds.md`; `docs/31-observability/slo-sla-definitions.md`; `docs/39-continuous-improvement/drift-framework.md` |
| Assumptions | A trigger starts the controlled-change process. A missing numeric floor stays Unknown. No new percent is invented |
| Unresolved issues | Numeric floors Unknown. Silent amount cutoff still HOLD_FOR_REVIEW. Signer Unknown |
| Residual risks | Writing 90 or 95 as a pass line. Writing a dollar trigger. Writing a live silent cutoff |

This page names when a person must start a controlled change. Behaviour triggers copy earlier decided gates. Numeric percent floors stay Unknown.

Engineering decision ED-P15-04, authority: team-force. Triggers split into behaviour (already decided) and numeric (stay Unknown). Watch integers from the drift framework are snapshots. They are not new floors.

---

## Finding

**Finding.** The release gate that already exists is: injection returns BLOCK and drives no action, and every scored AI answer cites a lake item or abstains. Those two behaviours are triggers. Percent floors stay Unknown. ROI stays EDUCATIONAL. The silent amount cutoff stays HOLD_FOR_REVIEW.
**Evidence.** FD-18. FD-14. BO-08. BO-11. `tevv-release-gate.md`.
**Impact.** An operator starts a change when a behaviour breaks. The operator does not wait for a percent this project never set.
**Risk.** Copying 42 of 42 into a 90 percent trigger.
**Confidence.** High on the behaviour list. Unknown on later numeric owners.
**Open questions.** Who may later name a percent floor. BO-08 owner for a live cutoff.

---

## Behaviour triggers (in force)

| Id | Trigger | What the person does | Source | Label |
|---|---|---|---|---|
| CT-01 | Quotes-plus-approve returns HTTP 200 and waits | Stop. Re-open Phase 12 control. Do not record an approval | FD-18. HB-24-01 after is HTTP 409 | Verified Fact |
| CT-02 | A scored AI answer has no lake citation and does not abstain | Stop release. Re-run the freeze | FD-14. FD-18 | Verified Fact |
| CT-03 | A parity false row lists no lake item id | Fail the harness. Do not print a match percent | FD-17 | Verified Fact |
| CT-04 | Lake YAML changes | Run the FD-22 review loop. Raise the version with an ADR | FD-22 | Verified Fact |
| CT-05 | Packaged six-field baseline JSON changes | Re-run `python -m app.baseline`. Compare to 125, 89, 2, 4982.61, 6, 0.603 | FD-03. Phase 14 | Verified Fact of the command. mean_amount and hours_per_case SIMULATED |
| CT-06 | Replay miss on a demo question that already has a saved file | Keep replay. Investigate the prompt hash. Do not set Azure | FD-13. CON-29-01 | Verified Fact |
| CT-07 | A policy number is missing | Route the case to HOLD_FOR_REVIEW | BO-08 PROPOSED | Verified Fact of the route |

Worked example. After SC-24-01, `POST /api/agent/run` on `REPLAY-000000000` with `proposed_action=approve` and no corpus id returned HTTP 409. If a later edit returns HTTP 200, CT-01 fires. Honesty of the 409: REAL.

---

## Numeric cells that stay unnamed

| Measure | Floor today | Owner who would name it later | Label |
|---|---|---|---|
| Groundedness percent | Unknown | Team-Force after a measured run | Unknown |
| Citation recall percent | Unknown | Team-Force after a measured run | Unknown |
| API p95 milliseconds | Unknown | Team-Force after a measured run | Unknown |
| Availability percent | Unknown | Business Owner for a company SLO | Unknown |
| Exception cycle time | Unknown | Business Owner. BO-02 | Unknown |
| Aged backlog age cutoff | Unknown | Business Owner. BO-02 | Unknown |
| Silent amount cutoff | HOLD_FOR_REVIEW | Business Owner. BO-08 | PROPOSED |
| ROI dollars | Unknown | Business Owner. BO-11 | EDUCATIONAL |

**Verified Fact.** `docs/26-tevv/release-thresholds.md` and FD-19 already leave those floors Unknown. This page does not fill them.

---

## Snapshot integers that are not floors

These numbers are watch values. A change is investigated. The number is not a pass percent.

| Snapshot | Value | Honesty |
|---|---|---|
| Freeze rows passed | 42 of 42 | REAL |
| Citation recall | 40 of 41 | REAL |
| Parity matched | 12 | REAL |
| Parity differing | 2 | REAL |
| Replay files besides README | 77 | REAL on 2026-10-18 |

Do not write 12/14 as a published match percent. **Verified Fact.** FD-17.
