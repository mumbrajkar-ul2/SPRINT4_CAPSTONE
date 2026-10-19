# Known limitations

| Field | Value |
|---|---|
| Stage | Phase 16 / Final as-built PRD |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p16-doc-20261018-001 |
| Status | COMPLETE. These limits stay open. Artifact UNSIGNED with the as-built baseline. |
| Evidence sources | `docs/34-after-kpis/after-intervention-kpi-sheet.md`; `docs/26-tevv/tevv-results.md`; `docs/36-benefits/benefits-signoff.md`; `docs/demo/paper-rehearsal.md`; `docs/38-handover/handover-acceptance-signoff.md`; `Decision_Tracker.md` BO-02, BO-03, BO-06b, BO-08, BO-10, BO-11, BO-12, BO-13 |
| Assumptions | A known limitation is a fact that remains true after the build. It is not a new feature request. |
| Unresolved issues | The rows below. |
| Residual risks | Presenting a limitation as a delivered target. Inventing a signer to close a row. |

This file lists the limits that stay open. It does not close them. It does not invent a dollar benefit.

---

## Finding

**Finding.** Exception cycle time is Unknown. Aged backlog is Unknown. Numeric percent floors are Unknown. Company titles are Unknown. INC-2025-014 owner is Unknown. Live Azure is NEEDS_HUMAN. Official Birlasoft assets have not arrived. Business Owner rows that are PROPOSED stay unsigned.
**Evidence.** After-KPI headline rows. TEVV floor cells. PH-S11-01. Paper rehearsal. BO rows in `Decision_Tracker.md`.
**Impact.** The as-built baseline can be used with these limits visible.
**Risk.** Filling any row with a demo name or a guessed percent.
**Confidence.** High that each cell below is empty or unsigned.
**Open questions.** Who signs BO-13 after reading this list.

---

## Limits that stay open

| Id | Limitation | Current fact | Label | Owner of a later close |
|---|---|---|---|---|
| KL-01 | Exception cycle time | No start field. No end field. After value Unknown | Unknown | Business Owner (BO-02) |
| KL-02 | Aged backlog | No age in days. Python open_cases is 89. That integer is not aged backlog | Unknown. 89 is REAL for `status != CLOSED` | Business Owner (BO-02) |
| KL-03 | Numeric percent floors | Groundedness, citation, and abstention floors stay empty. Freeze 42 of 42 is a count, not a 90 or 95 target | REAL count. Floor Unknown | Business Owner if a later floor is wanted |
| KL-04 | Company job titles | RT-01 to RT-06 have no company title map. Person names Unknown | Unknown | Business Owner with the company |
| KL-05 | INC-2025-014 owner | `owner_id` empty on both applications. Task `T-00000000` unassigned | REAL empty field | RT-06 at run time. Do not invent a name |
| KL-06 | Live Azure | Endpoint, deployment name, and API version Unknown. Path not run | NEEDS_HUMAN | A person who supplies Azure values |
| KL-07 | Official Birlasoft assets | Files not in hand. Deck stays on the neutral placeholder | Verified Fact of absence | BO-12 |
| KL-08 | BO rows that are PROPOSED | BO-02, BO-03, BO-04, BO-06b, BO-08, BO-10, BO-11, BO-12, BO-13 stay PROPOSED | Verified Fact of the tracker | Business Owner signature on each artifact |

Worked example for KL-01. `python -m app.baseline` still prints no cycle-time field. A later model of that number would be SIMULATED. This file does not write that model.

Worked example for KL-05. PH-S11-01 and PH-S11-02 both print empty `owner_id`. SP-11 expected verdict is ABSTAIN. This file leaves the owner Unknown.

---

## Related limits that stay visible

These rows support the eight open limits. They do not add a ninth business problem.

| Id | Limitation | Current fact | Label |
|---|---|---|---|
| KL-09 | Live seven-container recreate | Phase 15 did not start Compose. Dated health bodies exist | NEEDS_HUMAN for a new start |
| KL-10 | Paper rehearsal was not a room rehearsal | Minute total 39. Audience none | Verified Fact |
| KL-11 | Dollar cells | Avoided effort Unknown. Cost dollars Unknown. ROI EDUCATIONAL | Unknown dollars. No monetary benefit claimed |
| KL-12 | Expert-label disposition percent | No expert-label set | Unknown |
| KL-13 | API p95, retrieval p95, agent time | One-request `duration_ms` is not a target | Unknown |
| KL-14 | Recovery time and recovery point | Inherited 8 hours and 24 hours not adopted | Unknown |
| KL-15 | Availability percent | Inherited 99.5 percent not adopted | Unknown |
| KL-16 | Demo 50,000 cutoff | Shown as `proposed` on Application B. Live silent cutoff stays HOLD_FOR_REVIEW | PROPOSED. BO-08 |
| KL-17 | 999,999 JavaScript default | Not used as live policy | Verified Fact of the working answer |
| KL-18 | Handover acceptance | Written drills exist. Live D3 to D5, O1 to O3, R1, and R4 unrun | UNSIGNED. NEEDS_HUMAN |
| KL-19 | Phase 2 `reconcile()` | Not run on the packaged store. 67 rows remain REPLAY | Verified Fact |

---

## What a later person may close

A Business Owner may sign BO-13 after this list is read. That signature does not fill KL-01 to KL-07. Those cells stay empty until the named owner of each row supplies a value.

A person at RT-06 may type an INC-2025-014 owner. This file does not type one.

A person may run `docker compose up --build` and paste new health bodies. This file does not invent those bodies.

---

## What this file does not do

This file does not invent a cycle-time number, an aged-backlog cutoff, a percent floor, a company title, an incident owner, an Azure pass, a brand file, or a dollar benefit. It does not sign a Business Owner row.
