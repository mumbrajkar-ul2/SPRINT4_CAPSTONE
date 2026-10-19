# Final as-built PRD

| Field | Value |
|---|---|
| Stage | Phase 16 / Final as-built PRD |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p16-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED. BO-13 stays PROPOSED. |
| Evidence sources | `docs/09-initial-prd/`; `docs/17-implementation-prd/`; `docs/12-specs/`; `docs/10-architecture/adrs/`; `docs/26-tevv/tevv-results.md`; `docs/34-after-kpis/after-intervention-kpi-sheet.md`; `docs/model-comparison/scorecard.md`; `docs/final-prd/requirement-disposition-matrix.md`; `Decision_Tracker.md` BO-13 |
| Assumptions | `MODEL_MODE=replay`. Packaged 125-case file is the population. BO rows that are PROPOSED stay unsigned. |
| Unresolved issues | Exception cycle time Unknown. Aged backlog Unknown. Numeric percent floors Unknown. Company titles Unknown. INC-2025-014 owner Unknown. Live Azure NEEDS_HUMAN. Official Birlasoft assets not arrived. BO-13 unsigned. |
| Residual risks | Treating this unsigned file as a signed product baseline. Inventing a dollar benefit from 0.603 hours or 4982.61 mean amount. |

This file is the as-built product baseline. It states what was delivered, what changed, and what still waits. It reconciles the Initial PRD, the Implementation PRD, the specs, the ADRs, the TEVV results, and the after-intervention KPIs. It does not copy those files. It does not add a feature.

---

## Finding

**Finding.** The product that runs is two applications on the same fab-exception workflow for business problems BP1 to BP8. Application A on port 8100 takes rules from transformed code. Application B on port 8110 takes rules from the lake. Replay is the laptop model path. Fourteen of fifteen Initial functional requirements are Delivered. FR-08 is Changed. Hold prediction stays Rejected. Headline cycle time and aged backlog stay Unknown. No dollar benefit is claimed. BO-13 stays PROPOSED. This file stays UNSIGNED.
**Evidence.** Disposition matrix. Scorecard `PARITY matched=12 differing=2`. TEVV `rows=42 pass=42 fail=0`. `compose.yaml` ports 8080, 8090, 8091, 8092, 8100, 8110. `Decision_Tracker.md` BO-13.
**Impact.** A later change starts from this baseline, not from the Phase 3 wish list.
**Risk.** Reading the Initial PRD as the as-built product.
**Confidence.** High on the measured rows. Unknown on headline clocks and live Azure.
**Open questions.** BO-13 signer. Cycle-time clocks. Aged-backlog cutoff. INC-2025-014 owner.

---

## BO-13 recorded as PROPOSED / unsigned

**Verified Fact.** `Decision_Tracker.md` BO-13. The Business Owner accepted the working answer on 2026-10-18. The owner has not signed this artifact DECIDED. This file stays UNSIGNED. The run does not pause at this row.

Working answer in force: sign the as-built baseline once every requirement is classified with evidence and the known limitations are listed.

SME recommendation from `Decision_Tracker.md` section 5.1. Shown here because the owner must see it beside the row.

| ID | SME recommendation | Why |
|---|---|---|
| BO-13 | Sign the as-built baseline once every requirement is classified Delivered, Changed, Deferred, Rejected, or Superseded with evidence, and the known limitations are listed. | A signed as-built baseline is what operations, audit, and future change rely on. An unsigned one leaves ownership unclear. |

This file copies that recommendation. It does not invent a signer name. The sign-off page is `final-product-baseline-signoff.md`.

---

## What actually shipped

The product is still two applications that run the same fab-exception workflow on BP1 to BP8. That bound comes from the Initial PRD and still holds.

What changed after Phase 3 is the platform that makes those applications reachable.

| Item | As-built fact | Honesty |
|---|---|---|
| Application A | Port 8100. FastAPI serves `/api` and the React screens. Rules from transformed code | Verified Fact |
| Application B | Port 8110. Same workflow. Rules only from the lake. Lineage view on scenario 12 | Verified Fact |
| Context Lake | Version 1.0.0. REST on 8091. MCP on 8092. Read only | Verified Fact |
| Current-system baseline | Legacy API on 8080. No identity check | Verified Fact. EV-H8080 REAL |
| Source fixture | Gateway on 8090. No identity check | Verified Fact. EV-H8090 REAL |
| Identity on the two apps | Headers `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role`. Missing set is HTTP 401 | Verified Fact |
| Laptop model path | `MODEL_MODE=replay`. File named by SHA-256 of the prompt. 77 saved files | REAL file count. PRECOMPUTED file bodies |
| Person on writes | `WRITE_TOOLS` empty. Proposer and approver differ | REAL |
| Two-app compare | 14 harness rows. 12 matched. 2 differed. Each difference cites a lake item | REAL. No match percent |
| AI answers | Freeze 42 of 42 cite or abstain | REAL. Floor Unknown |
| Injection | HTTP 409 BLOCK on the named corpus posts | REAL |
| Headline KPIs | Exception cycle time Unknown. Aged backlog Unknown | Unknown |
| Dollars | None claimed | Verified Fact of this page |

Worked example. Application A marks case PS000000016 with step recipe R02 and tool recipe R01. Application B shows the same pair. A Process Engineer at RT-03 records the hold. The model drafts the sentence. The model does not write `engineering_hold`. Honesty of the pair: REAL.

---

## How this baseline differs from the earlier PRDs

The Initial PRD named the product. The Implementation PRD named the ports, headers, replay wiring, CI, and logs. This file names what those later phases actually proved.

| Earlier statement | As-built statement | Disposition |
|---|---|---|
| Application host ports Unknown | 8100 and 8110 | Named in Phase 8. Delivered as IP-01 |
| Identity design later | Three headers on 8100 and 8110. 8080 stays open | FR-08 Changed |
| Replay assumed until Phase 15 | Replay is the default laptop path | NFR-24 Delivered |
| FD-17 harness later | 14 rows, 12 matched, 2 differed | FR-14 Delivered |
| FD-15 tool list later | Six read tools. Write list empty | NFR-02 Delivered |
| FD-23 audit later | 12 rows, 27 columns, one correlation id | NFR-20 Delivered |
| Phase 8 app stubs only | Scenario routes and lineage exist | IP-09 Superseded |
| Hold predictor rejected | Still absent | NFR-06 Rejected |
| Exception cycle time Unknown | Still Unknown | NFR-10 Unknown |
| No dollar benefit | Still none | NFR-14 Delivered as a constraint |

The Initial PRD and the Implementation PRD remain the historical record. They are not the as-built baseline.

---

## Requirement summary

Full rows sit in `requirement-disposition-matrix.md`. Evidence links sit in `final-acceptance-evidence-map.md`.

| Disposition | What it means on this product | Count |
|---|---|---|
| Delivered | Built and tied to a spec, a test, a KPI, or an ADR | 54 |
| Changed | Built, and the mechanism or live step differs from the earlier wording | 3 |
| Deferred | Still later. Official assets, live Azure, BO-13 signature | 3 |
| Rejected | Will not be built. Hold predictor. Ninth problem | 2 |
| Superseded | Replaced by a later increment. Phase 8 stubs | 1 |
| Unknown | No acceptance evidence for a delivered value. Waits for the Business Owner | 12 |

Changed rows: FR-08 identity mechanism named and INC-2025-014 owner empty; IP-10 live Compose recreate still a human step; NFR-23 paper path 39 minutes with live clicks NEEDS_HUMAN. Total rows in the matrix: 75.

Unknown rows include exception cycle time, aged backlog, availability percent, recovery time, recovery point, API p95, retrieval p95, percent floors, dollar cost, company titles, INC-2025-014 owner, and expert-label percent.

---

## Architecture that must match what runs

The as-built picture is in `as-built-architecture.md`.

| Port | Listener | Rule source or role |
|---|---|---|
| 8080 | Legacy API | Current-system baseline |
| 8090 | Source gateway | Scenario 11 fixture |
| 8091 | Lake REST | Screens read lake items |
| 8092 | Lake MCP | Agents read the same lake as tools |
| 8100 | Application A | Transformed code for pass or fail |
| 8110 | Application B | Lake only for pass or fail |

Phase 4 left 8100 and 8110 Unknown. Those ports now run. Replay is the laptop model path. Application A does not call Application B. Application B does not call Application A.

A later live `docker compose up --build` recreate is NEEDS_HUMAN. Dated health bodies for all six listeners are REAL in `docs/18-delivery/evidence-checklist.md`.

---

## Acceptance evidence in one page

| Capability | What a reviewer can re-run or open | Honesty |
|---|---|---|
| S7 Replay | PH-S7-01 duplicate true. PH-S7-02 count 67 | REAL |
| S8 Recipe | PH-S8-01 R02 / R01. T-KILL wait survived pid 29320 | REAL |
| S9 Two clocks | PH-S9-01 2020-12-30 / 2021-01-01 | REAL |
| S10 Overlap | PH-S10-01 five policy ids. SP-10 HOLD_FOR_REVIEW | REAL |
| S11 Recovery and owner | Recovery GET. INC-2025-014 owner empty | REAL empty field |
| S12 Lineage | Application B 2023 EMEA item. Application A `view_absent` | REAL |
| S13 Compare | `PARITY matched=12 differing=2` | REAL. No percent |
| BP7 Injection | HTTP 409 BLOCK. Seven Application B corpus posts | REAL |
| Cite or abstain | `rows=42 pass=42 fail=0` | REAL. Floor Unknown |
| Person gate | PH-PERSON-01 hold both apps. T-SEP 403 | REAL |
| Replay cost on shown path | prompt_tokens 0, completion_tokens 0 | REAL for that path |
| Packaged baseline | records 125, open_cases 89, urgent_cases 2, sites 6 | REAL |
| Synthetic money fields | mean_amount 4982.61, hours_per_case 0.603 | SIMULATED |
| ROI | Unknown dollars | EDUCATIONAL |

Supporting benefits stay supporting. They are listed in `docs/36-benefits/verified-benefits.md`. This page does not move them into a dollar cell.

---

## Known limitations that stay open

Full text sits in `known-limitations.md`.

1. Exception cycle time is Unknown.
2. Aged backlog is Unknown.
3. Numeric percent floors are Unknown.
4. Company titles are Unknown.
5. INC-2025-014 owner is Unknown.
6. Live Azure is NEEDS_HUMAN.
7. Official Birlasoft assets have not arrived.
8. Business Owner rows that are PROPOSED stay unsigned.

This file does not fill those cells.

---

## Residual risks

Full rows sit in `residual-risk-register.md`.

The material set is an unsigned baseline, empty headline clocks, empty money cells, empty percent floors, an empty incident owner, and unrun live Azure and Compose steps.

A later author who copies 42 of 42 as a 90 percent floor, or 12 of 14 as a match percent, or 0.603 as recovered labor, would invent a claim this baseline forbids.

---

## What this file does not do

This file does not copy the Initial PRD or the Implementation PRD. It does not add a ninth business problem. It does not invent a cycle-time number, an aged-backlog cutoff, a percent floor, or a dollar benefit. It does not sign BO-13. It does not invent a signer. It does not update `Decision_Tracker.md` or `STATUS.md`.
