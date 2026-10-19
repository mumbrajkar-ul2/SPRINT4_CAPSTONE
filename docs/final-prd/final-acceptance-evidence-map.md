# Final acceptance evidence map

| Field | Value |
|---|---|
| Stage | Phase 16 / Final as-built PRD |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p16-doc-20261018-001 |
| Status | COMPLETE. Artifact UNSIGNED with the as-built baseline. |
| Evidence sources | `docs/final-prd/requirement-disposition-matrix.md`; `docs/12-specs/acceptance-criteria.md`; `docs/26-tevv/tevv-results.md`; `docs/34-after-kpis/after-intervention-kpi-sheet.md`; `docs/model-comparison/scorecard.md`; `docs/22-agentic-engineering/agent-test-results.md`; `docs/18-delivery/evidence-checklist.md`; `docs/10-architecture/adrs/` |
| Assumptions | Only Delivered rows appear as accepted. Changed, Deferred, Rejected, Superseded, and Unknown rows are listed so a reader can see why they are absent from the accepted set. |
| Unresolved issues | Unknown rows wait for the Business Owner. Live Azure NEEDS_HUMAN. BO-13 unsigned. |
| Residual risks | Treating a Changed or Unknown row as accepted. Copying 42 of 42 as a 90 or 95 floor. |

This file links each Delivered requirement to the acceptance evidence that supports it. A Delivered row has a spec, a test, a KPI, or an ADR. This file does not invent a number.

---

## Finding

**Finding.** Every Delivered functional requirement, Implementation platform requirement, NFR behaviour, and SLO-B row cites at least one spec, test, KPI, or ADR. FR-08 is Changed and is mapped as accepted-with-change. Twelve Unknown rows have no delivered value and are not accepted. Hold prediction is Rejected and is not accepted as a feature.
**Evidence.** Disposition matrix. Scorecard print `PARITY matched=12 differing=2`. TEVV print `rows=42 pass=42 fail=0`. Agent pytest 13 passed. EV-H8080 to EV-H8110.
**Impact.** A reviewer can re-run the cited commands and open the cited files.
**Risk.** Accepting NFR-10 cycle time because open_cases is 89.
**Confidence.** High on the Delivered links. Unknown on headline clocks.
**Open questions.** BO-13 signer.

---

## How to read the map

| Column | Meaning |
|---|---|
| Requirement | Id from the disposition matrix |
| Spec | Acceptance criterion or contract |
| Test | Measured command or named test id. Honesty REAL unless noted |
| KPI | After-intervention or scorecard cell |
| ADR | Architecture decision, if one locks the behaviour |

A blank KPI cell means the requirement is accepted on a spec, a test, or an ADR. It does not mean a headline target was met.

---

## Delivered functional requirements

| Requirement | Spec | Test | KPI | ADR |
|---|---|---|---|---|
| FR-01 Recipe mismatch | AC-S8 | PH-S8-01. T-TRACE. T-KILL | Recipe pair R02 / R01 both apps | `adr-two-applications.md` |
| FR-02 Replay duplicate | AC-S7 | PH-S7-01. PH-S7-02 | Replay count 67 both apps | `adr-two-applications.md` |
| FR-03 Two clocks | AC-S9 | PH-S9-01 | Clock pair 2020-12-30 / 2021-01-01 | `adr-two-applications.md` |
| FR-04 Governed rule | AC-RULE | PH-RULE-01 | Limit 18600 and 25000 | `adr-app-b-reads-only-the-lake.md` |
| FR-05 Open operational meaning | AC-S13 | PH-RANK-01 | Five scenario cases `open_operational` true. open_cases 89 | BO-06a is DECIDED. Not an ADR |
| FR-06 Policy overlap | AC-S10 | PH-S10-01. TEVV SP-10 | Five POL ids both apps | BO-07 is DECIDED |
| FR-07 Untrusted text | AC-BP7 | PH-BP7-01. HB-26-01 after. HB-26-02. T-INJECT | Injection HTTP BLOCK 7 of 7 | `adr-opa-gates.md` |
| FR-09 Queue ranking | AC-RANK | PH-RANK-01. PH-RANK-02 | urgent_cases 2 | FD-04 |
| FR-10 Cited explanation | AC-CITE | PH-CITE-01. TV-26-01 | Groundedness 42 of 42. Floor Unknown | `adr-lake-yaml-to-sqlite.md` |
| FR-11 Cited natural-language answer | AC-CITE | TEVV GQ-01 to GQ-26. TV-26-05 | Abstention 6 of 6 expected. Floor Unknown | FD-10 |
| FR-12 Draft plan then wait | AC-PERSON | T-TRACE. T-RESTART. T-KILL | Agent time Unknown | `adr-langgraph-interrupt-approval.md` |
| FR-13 Person on every write | AC-PERSON | PH-PERSON-01. T-NO-WRITE-TOOL. T-SEP | Person hold `engineering_hold=1` both apps | `adr-langgraph-interrupt-approval.md` |
| FR-14 Same-scenario run | AC-S13 | `test_parity_harness.py` matched=12 differing=2 | Harness integers 12 and 2 | `adr-two-applications.md` |
| FR-15 Rule lineage | AC-S12 | PH-S12-01 | Application B 2023 EMEA item. Application A `view_absent` | `adr-app-b-reads-only-the-lake.md` |

Worked example. FR-01. Open `docs/model-comparison/scorecard.md` row PH-S8-01. Both applications print R02 and R01. Spec AC-S8 says both revision fields must show and the model must not write the hold.

---

## Changed requirement mapped with evidence

FR-08 is Changed. It is accepted as the named three-header identity plus recovery status, with INC-2025-014 `owner_id` empty.

| Requirement | Spec | Test | KPI | ADR |
|---|---|---|---|---|
| FR-08 Identity, owner, recovery | AC-S11. EH-01 | 401 on 8100 and 8110. PH-S11-01. PH-S11-02. HB-25-06. Recovery GET | INC-2025-014 `owner_id` empty both apps | `adr-ports-and-compose.md` |

The empty owner field is REAL. It is not a delivered name.

IP-10 one Compose command is Changed. Evidence is `compose.yaml` plus dated health rows EV-H8080 to EV-H8110. A later recreate is NEEDS_HUMAN.

NFR-23 forty-minute path is Changed. Evidence is the 39-minute paper walk. Live clicks are NEEDS_HUMAN.

---

## Delivered Implementation platform rows

| Requirement | Spec | Test | KPI | ADR |
|---|---|---|---|---|
| IP-01 Host port map | FD-13. System listener ids | EV-H8080 to EV-H8110 | n/a | `adr-ports-and-compose.md` |
| IP-02 Seven containers | FD-13 | `docker compose config` Phase 8 | n/a | `adr-ports-and-compose.md` |
| IP-03 Identity scaffolding | EH-01 | 401 identity-check | n/a | FD-13 |
| IP-04 Lake REST 8091 | `api-contracts.md` | EV-H8091. POST 405 | Lake version 1.0.0 | `adr-lake-yaml-to-sqlite.md` |
| IP-05 Lake MCP 8092 | Four locked tools | EV-H8092 | n/a | `adr-lake-yaml-to-sqlite.md` |
| IP-06 Replay wiring | Execution_Plan section 10 | T-REPLAY. 77 files | prompt_tokens 0, completion_tokens 0 on the shown path | FD-13 |
| IP-07 Capstone CI | ED-P8A-06 | GNG-30-07 | n/a | FD-13 |
| IP-08 JSON logs | ED-P8A-07 | `docs/31-observability/telemetry-results.md` | p95 Unknown | FD-13 |
| NFR-16 Legacy 8080 open | ED-P8A-03 | GNG-30-05. CT-35 | n/a | `adr-ports-and-compose.md` |
| NFR-17 Gateway 8090 open | ED-P8A-03 | GNG-30-05 | n/a | `adr-ports-and-compose.md` |
| NFR-18 Lake key | ED-P8A-04 | Phase 8 lake tests | n/a | FD-13 |
| NFR-26 Six health bodies | Implementation health need | EV-H8080 to EV-H8110 | n/a | `adr-ports-and-compose.md` |

---

## Delivered NFR and SLO-B behaviours

| Requirement | Spec | Test | KPI | ADR |
|---|---|---|---|---|
| NFR-01 Local synthetic | FD-02 | T-READONLY-DB | records 125 | FD-02 |
| NFR-02 Read-only tools | FD-02 | T-NO-WRITE-TOOL | n/a | FD-02 |
| NFR-03 Person on writes | AC-PERSON | PH-PERSON-01 | Same as FR-13 | `adr-langgraph-interrupt-approval.md` |
| NFR-04 Untrusted text | AC-BP7 | HB-26-02 | Same as FR-07 | `adr-opa-gates.md` |
| NFR-05 Classification working answer | BO-10 working answer | Phase 12 governance files | n/a | n/a. BO-10 unsigned |
| NFR-07 App independence | AC-S13 | Phase 11 independence check | n/a | `adr-two-applications.md` |
| NFR-08 Same scenarios | AC-S13 | Parity harness | 14 rows | `adr-two-applications.md` |
| NFR-09 Same KPI families | FD-03 | After-KPI sheet | Eight families, targets empty | FD-20 |
| NFR-12 Honesty labels | FD-20 | Scorecard labels | Every number labelled | FD-20 |
| NFR-13 Rule source split | AC-RULE | PH-RULE-01 | Same as FR-04 | `adr-app-b-reads-only-the-lake.md` |
| NFR-14 No monetary benefit | BO-11 working answer | Benefits sign-off UNSIGNED | Dollars Unknown. ROI EDUCATIONAL | n/a |
| NFR-15 Identity on A and B | EH-01 | 401 tests | n/a | FD-13 |
| NFR-19 Approval recorded | AC-PERSON | T-TRACE human_approval | n/a | `adr-audit-chain.md` |
| NFR-20 Audit chain | FD-23 | T-TRACE 12 rows | n/a | `adr-audit-chain.md` |
| NFR-21 User-visible recovery | AC-S11 | HB-29-01. GNG-30-03 | Recovery time Unknown | n/a |
| NFR-22 Separation of duties | BO-09. EH-02 | T-SEP | n/a | n/a |
| NFR-24 Offline replay | FD-13 | 77 replay files. T-REPLAY | Tokens 0 and 0 on the shown path | FD-13 |
| NFR-25 Replay tokens 0 on shown path | A-W2 | HB-32-01 | prompt_tokens 0, completion_tokens 0 | FD-13 |
| SLO-B1 to SLO-B10 | `finalized-nfrs.md` | Matching FR and NFR tests above | Matching KPI cells above | Matching ADRs above |

---

## Rows that are not accepted as Delivered

| Requirement | Disposition | Why it is not in the accepted set | What a later owner still needs |
|---|---|---|---|
| FR-08 | Changed | Mechanism named after the Initial PRD. INC-2025-014 owner empty | A person at RT-06 supplies an owner name if the company wants one |
| IP-09 Phase 8 stubs | Superseded | Later phases built the scenario routes | None. Read FR-01 to FR-15 |
| IP-10 Live one-command start | Changed | File exists. Fresh recreate NEEDS_HUMAN | A person runs `docker compose up --build` |
| NFR-06 Hold predictor | Rejected | FD-05 | None. Do not add a scorer |
| REJ-02 Ninth problem | Rejected | BO-04 working answer | None. Do not add FR-16 |
| NFR-10 Cycle time | Unknown | No start and end fields | Business Owner names the clocks |
| NFR-11 Aged backlog | Unknown | No age in days | Business Owner names the cutoff |
| NFR-23 Forty-minute live path | Changed | Paper 39 minutes. Live clicks NEEDS_HUMAN | A person runs the live stack |
| NFR-27 to NFR-33 | Unknown | No signed percent, millisecond, or dollar | Business Owner if a later target is needed |
| UNK-01 Company titles | Unknown | No company map | Business Owner or HR map |
| UNK-02 INC-2025-014 owner | Unknown | Empty field is REAL | RT-06 at run time |
| UNK-03 Expert-label percent | Unknown | No expert-label set | Business Owner if scoring is wanted |
| DEF-01 Birlasoft assets | Deferred | Files not arrived | BO-12 |
| DEF-02 Live Azure | Deferred | NEEDS_HUMAN | A person supplies Azure values |
| DEF-03 BO-13 signature | Deferred | This pack is unsigned | Named signer |

---

## Commands a reviewer can re-run

Working directory for parity: capstone root.

```text
python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s
```

Expected print: `PARITY matched=12 differing=2`. Honesty: REAL on the Phase 14 run.

```text
python apps/app_a/eval/run_freeze.py
```

Expected print: `rows=42 pass=42 fail=0`. Honesty: REAL on the Phase 12 run. Floor Unknown.

Working directory for baseline: `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`.

```text
python -m app.baseline
```

Expected JSON includes records 125, open_cases 89, urgent_cases 2, sites 6. Honesty: REAL for those four. mean_amount 4982.61 and hours_per_case 0.603 are SIMULATED.

---

## What this file does not do

This file does not mark Unknown rows Delivered. It does not invent a percent floor. It does not invent a dollar benefit. It does not sign BO-13.
