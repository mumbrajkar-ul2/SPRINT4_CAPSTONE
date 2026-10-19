# Project acronyms — Sprint 4 Fabpulse capstone

| Field | Value |
|---|---|
| Stage | Reader guide. Runs beside `Execution_Plan.md`, `Decision_Tracker.md`, and `playbook/STATUS.md`. |
| Date / version | 2026-10-18, v1.11 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | Seeded before the run. It holds the short codes and acronyms already used in the plan, the tracker, and the playbook. The coordinator adds a row each time a phase introduces a new short code. |
| Evidence sources | `Execution_Plan.md`, `Decision_Tracker.md`, `Project_Intent.md`, and the `playbook/` prompts. |
| Assumptions | A sample id such as `FD-07` is one row of a group. This file lists the group once and gives examples. |

## What this file is

This file says what each short label means. A short label is a few letters, sometimes with a number, that stands for a longer name. The rows below cover the labels already used in the plan, the decision tracker, and the playbook.

This file explains labels. It adds no new id. The lake YAML ids in `context-lake/` stay the source for lake terms. When a later phase introduces a new short code, the coordinator adds it to the "New terms by phase" table at the end.

## Decision ids

These ids number the decisions in `Decision_Tracker.md`. The letters say which group owns the decision.

| Group | What it is | Range | Owner | Example |
|---|---|---|---|---|
| `FD-xx` | A Team-Force engineering or method decision. | `FD-01` to `FD-25` | Team-Force (the FDE team) | `FD-06` is the locked architecture. `FD-24` is the reviewer-agent acceptance rule. `FD-25` is the executor-agent build rule. |
| `BO-xx` | A Business Owner or SME decision. The owner column of each row says which. | `BO-01` to `BO-13` | Business Owner, or the FDE SME where marked | `BO-05` is the recipe authority (SME). `BO-11` is the ROI sign-off (Business Owner). |
| `BO-06a`, `BO-06b` | The split of BO-06. `BO-06a` is the operational meaning of open and closed (SME). `BO-06b` is whether operational closure also means finance-booked and audit-closed (Business Owner). | two rows | SME and Business Owner | `BO-06a` is DECIDED. `BO-06b` is still with the Business Owner. |
| `RT-xx` | A run-time decision a named role makes inside the live app, one case at a time. | `RT-01` to `RT-06` | A fab role (see Group C) | `RT-01` is disposing a case that routed to HOLD_FOR_REVIEW. |
| `BP1` to `BP8` | A business problem the project must solve. | `BP1` to `BP8` | — | `BP1` is the recipe mismatch (91 of 125 steps). `BP8` is no API auth and the unknown incident owner. |

## Phase and spine ids

The plan runs in 17 phases. Each phase holds one or more spine sub-stages.

| Label | What it is | Where |
|---|---|---|
| Phase 0 to Phase 16 | The 17 playbook phases. The coordinator runs them in order. | `playbook/phase_00_*.md` to `phase_16_*.md` |
| Spine unit | One of the 46 units of the Production Delivery Spine: `0A`, `0B`, `0C`, stages `1` to `42`, and `FINAL`. Each maps to one phase and one `docs/NN-*/` folder. | `Execution_Plan.md` section 7 |
| `11R` | The Context Lake review, fix, and revision loop inside Phase 5. The `R` marks a review. | `context-lake/review/` |
| `20p` | Application B, the port of stage 20 built only from the lake, inside Phase 11. The `p` marks the port. | `apps/app_b/` |
| Half A | The analysis and design half of a build phase. It writes documents and changes no code. | Build phases 5, 7, 8, 9, 10, 11, 12, 13 |
| Half B | The code and tests half of a build phase. It starts only after the reviewer accepts Half A. | Same |

## Status and honesty words

These are written in capitals. They are status words, not ids.

| Word | What it means here |
|---|---|
| `DECIDED` | The owner gave the answer. The decision tracker row names the date and the source. |
| `PENDING` | No answer yet. The phase that needs it must ask before it starts. |
| `DEFERRED` | No answer yet, but the phase may run under the stated default until the owner decides. |
| `PROPOSED` | The SME filled in a recommended answer for a Business Owner row. It is not signed. After the one-time review it holds and the run does not pause at it. A policy value behind it is never written into code. |
| `PASS` | The phase met its gate. |
| `CONDITIONAL PASS` | The phase met its gate with a named open item still to close. |
| `BLOCKED` | A required piece is missing. The next phase waits. |
| `REAL` | The running app computed this number from the case in front of you. |
| `PRECOMPUTED` | A script computed this number earlier and the screen reads it back. |
| `SIMULATED` | The number stands in for a live service that was not called. |
| `EDUCATIONAL` | A teaching figure or formula. It is not a real business benefit or a price. |

## Claim labels

Every claim in an artifact carries one of these.

| Label | What it means here |
|---|---|
| `Verified Fact` | A claim that names a file, a table, an API, a schema, a test, a lake item id, or a log line. |
| `Inference` | A claim drawn from facts, with no direct proof. |
| `Assumption` | Something taken as true so the work can go on. It is listed in the artifact header. |
| `Unknown` | The repo or the owner has not said. |

## Reviewer verdicts

Three agents run the delivery: the coordinator (Grok 4.7) orchestrates, the executor (Grok 4.6) builds each unit, and the reviewer (Composer 2.5) checks it. See `playbook/EXECUTION_ARCHITECTURE.md`. The reviewer returns one of these verdicts.

| Verdict | What it means here |
|---|---|
| `HALF_A_ACCEPTED` | The Half A design is good enough to build from. Half B may start. |
| `HALF_A_CONDITIONAL` | Only small, named fixes remain. Apply them, then start Half B. |
| `HALF_A_BLOCKED` | The design needs a change before any code. Half B does not start. |
| `STAGE_ACCEPTED` | The finished output met the Expected output and the Done test passed. The next phase may start. |
| `STAGE_CONDITIONAL` | Small fixes remain, or the Done test needs a person. The coordinator applies the fix or prints a pause card. |
| `STAGE_BLOCKED` | A file is missing, a check failed, or the Done test failed. The next phase does not start. |
| `NEEDS_HUMAN` | A Done test needs a credential, a running service, or a network call the sandbox blocks. |

## Policy outcomes

The OPA gate returns one of these for an agent action.

| Outcome | What it means here |
|---|---|
| `EXECUTE` | Carry out the action. |
| `HOLD_FOR_REVIEW` | Stop and wait for a person to decide. |
| `BLOCK` | Refuse the action. An injection record must yield this. |

## Lake terms

These describe the Enterprise Context Lake.

| Term | What it means here |
|---|---|
| `authority: policy_archive` | The rule card's value comes from the governed, effective-dated archive (`contracts/decision-policies-archive.json` and `policy_register`). This is canonical. |
| `authority: sme` | The rule card's value is set by the designated FDE SME from fab-industry practice. |
| `authority: unresolved` | The governed source is silent, overlapping, or self-contradictory. The case routes to HOLD_FOR_REVIEW. |
| Semantic layer | The way the lake is written: Markdown explains, YAML defines, JSON Schema validates, tests protect, generated output serves. |
| `edges` table | The knowledge graph is a table of edges plus recursive SQL queries, not a graph database. |
| `FTS5` | The full-text search feature of SQLite the lake build uses. |

## Capital-word acronyms

Each row says what the letters stand for in this project and where they show up.

| Letters | What they mean here | Where |
|---|---|---|
| `OPA` | Open Policy Agent. The policy engine that returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK. | Phase 4 ADR, Phase 10 `policy/opa/` |
| `RAG` | Retrieval-augmented generation. The model answers from text the retrieval step pulled from the lake. | Phase 9 `docs/19-intelligence/` |
| `MCP` | Model Context Protocol. One of the two lake interfaces, on port 8092. | Phase 4, Phase 5 |
| `REST` | The web API style of the lake's other interface, on port 8091. | Phase 4, Phase 5 |
| `ADR` | Architecture decision record. One file per fixed choice, with its rejected options. | Phase 4 `docs/10-architecture/adrs/` |
| `PRD` | Product requirements document. The Initial PRD is Phase 3; the Implementation PRD is Phase 8; the Final As-Built PRD is Phase 16. | Phases 3, 8, 16 |
| `KPI` | Key performance indicator. A number the business watches. | Phase 0 baseline, Phase 14 |
| `SLO` | Service level objective. A stated target for the running service. | Phase 13 `docs/31-observability/` |
| `SLA` | Service level agreement. The service promise the data records in `sla_tier`. | Phase 1, Phase 6 |
| `TEVV` | Test, evaluation, verification, and validation. The Phase 12 quality and red-team work. | Phase 12 `docs/26-tevv/` |
| `BCDR` | Business continuity and disaster recovery. The Phase 13 continuity plans. | Phase 13 `docs/29-incident-bcdr/` |
| `RTO` | Recovery time objective. How fast a service must come back. | Phase 13 |
| `RPO` | Recovery point objective. How much data loss is acceptable. | Phase 13 |
| `DLQ` | Dead-letter queue. Where a bad message is parked for replay. | Phase 13 |
| `SBOM` | Software bill of materials. The list of libraries in a build. | Phase 13 `docs/27-hardening/` |
| `RBAC` | Role-based access control. Access from a job role. | Phase 12 |
| `ABAC` | Attribute-based access control. Access from extra facts such as purpose and risk. | Phase 12 |
| `FinOps` | Cost management for the AI calls. The Phase 13 cost and token work. | Phase 13 `docs/32-finops/` |
| `CI/CD` | The path that builds, tests, and releases the software. | Phase 8 `docs/18-delivery/` |
| `IaC` | Infrastructure as code. In this project it is the Docker Compose topology. | Phase 8 |
| `HITL` | Human in the loop. The approval pause before an agent action runs. | Phase 10 `docs/23-human-control/` |
| `SEMI` | The semiconductor industry standards body. The change-control style the rule archive follows. | Phase 5 rule-authority policy |
| `p95` | The value that 95 of every 100 calls stay under. A latency measure. | Phase 9, Phase 14 |
| `YAML` | The text format the lake is written in. | `context-lake/` |
| `JSON` | A text shape for an object. Schemas and policy inputs use it. | Phases 5, 10 |
| `SQLite` | The single-file database the lake build writes (`context-lake.sqlite3`). | Phase 5 |
| `LangGraph` | The library that runs the agent with `interrupt()` and `Command(resume=...)`. | Phase 10 |
| `SHA-256` | The hash function the source register uses to show a file was not changed. | Phase 0 `sources/register.yaml` |

## New terms by phase

The coordinator adds a row here each time a phase introduces a short code that is not already above. It writes the term, its one-line meaning, and the file where it is used. Until a phase runs, this table is empty.

| Phase | Term | Meaning | Where |
|---|---|---|---|
| 0 | — | This phase added no new short code. SHA-256 was already listed above. | — |
| 1 | `RC-01` to `RC-08` | One confirmed root-cause row. The number matches the business problem. Example: `RC-01` is the recipe-revision mismatch. | `docs/06-root-cause/confirmed-root-causes.md` |
| 1 | `C-BP1-count` and the other `C-BP*` rows | One evidence row in the confidence matrix. The middle part is the business problem. Example: `C-BP2-hist` is the 2025 rollback sentence, correlated with the replay rows, not proven as their cause. | `docs/06-root-cause/evidence-confidence-matrix.md` |
| 1 | `ED-P1-01` | The Phase 1 method note. Each business-problem row has one SQL query as the checkable count. A file scan is an extra count. | `Decision_Tracker.md` change log v1.11 |
| 2 | `R-P2-01` to `R-P2-08` | A retired AI cost assumption from the Phase 0 envelope. Example: model cost is not kept on a job that Phase 2 labelled deterministic. | `docs/08-ai-qualification/economics-baseline-reconciliation.md` |
| 2 | `ED-P2-01` to `ED-P2-03` | Phase 2 method notes. `ED-P2-01` is the hold-column null test. `ED-P2-02` keeps case ranking in deterministic code. `ED-P2-03` says no model file is saved. | `Decision_Tracker.md` change log v1.13 |
| 3 | `F-01` to `F-15` | One feature in the Initial PRD. Example: a feature is one user-facing job tied to BP1–BP8. | `docs/09-initial-prd/initial-prd-traceability.md` |
| 3 | `FR-01` to `FR-15` | One functional requirement. The number matches the feature. `FR-01` is the requirement for `F-01`. | `docs/09-initial-prd/functional-requirements.md` |
| 3 | `ED-P3-01` to `ED-P3-03` | Phase 3 method notes. `ED-P3-01` is the feature set F-01 to F-15. `ED-P3-02` shows BP7 as a control on scenarios 7 to 11. `ED-P3-03` keeps the port numbers out of the PRD requirements. | `Decision_Tracker.md` change log v1.14 |
| 5 | `GQ-01` to `GQ-26` | One golden question the lake must answer with a citation. Example: `GQ-01` is the first question in the set. | `context-lake/eval/golden-questions.yaml` |
| 5 | `ED-P5A-01` to `ED-P5A-09` | Phase 5 design notes. Example: `ED-P5A-01` keeps conflicts as decision items. There is no eighth content kind. | `Decision_Tracker.md` change log v1.16 |
| 5 | `ED-P5B-01` to `ED-P5B-08` | Phase 5 build notes. Example: `ED-P5B-01` allows capital letters in an item id so `map.site.IN-BLR` validates. | `Decision_Tracker.md` change log v1.17 |
| 6 | `EV-01` to `EV-12` | One event type in the Phase 6 event contract. Example: `EV-01` is the first event in that list. | `docs/12-specs/event-contracts.md` |
| 6 | `ED-P6-01` to `ED-P6-05` | Phase 6 contract notes. Example: `ED-P6-01` names the lake read paths on port 8091. | `Decision_Tracker.md` change log v1.18 |
| 7 | `ED-P7A-01` to `ED-P7A-06` | Phase 7 design notes. Example: `ED-P7A-01` names the five characterization test modules. | `Decision_Tracker.md` change log v1.19 |
| 7 | `ED-P7B-01` to `ED-P7B-05` | Phase 7 build notes. Example: `ED-P7B-01` is the shape of `evaluate_live_policy`. | `Decision_Tracker.md` change log v1.19 |
| 8 | `ED-P8A-01` to `ED-P8A-08` | Phase 8 design notes. Example: `ED-P8A-01` names Application A port 8100 and Application B port 8110. | `docs/17-implementation-prd/prd-change-log.md` |
| 8 | `ED-P8B-01` to `ED-P8B-05` | Phase 8 build notes. Example: `ED-P8B-01` is one `Dockerfile.platform` with a different command per service. | `docs/_playbook-log.md` Phase 8 record |
| 9 | `ED-P9A-01` to `ED-P9A-08` | Phase 9 design notes. Example: `ED-P9A-04` scores an answer as grounded only when it cites retrieved lake item ids, or as a clean abstain. No percent floor. | `Decision_Tracker.md` change log v1.21 |
| 10 | `ED-P10A-01` to `ED-P10A-09` | Phase 10 design notes. Example: `ED-P10A-01` sets the LangGraph recursion limit to 12. That number is an engineering default. | `Decision_Tracker.md` change log v1.23 |
| 10 | `OPA-R-01` to `OPA-R-12` | One OPA rule. Example: `OPA-R-01` returns BLOCK when injection text is treated as an order. | `docs/23-human-control/approval-gates.md` |
| 11 | `ED-P11A-01` to `ED-P11A-08` | Phase 11 design notes. Example: `ED-P11A-01` names the parity fields and forbids a match percent. | `Decision_Tracker.md` change log v1.25 |
| 11 | `ED-P11B-01` to `ED-P11B-02` | Phase 11 build notes. Example: `ED-P11B-01` builds a cited sentence from lake statements when replay misses. | `docs/_playbook-log.md` Phase 11 record |
| 12 | `ED-P12A-01` to `ED-P12A-06` | Phase 12 security design notes. Example: `ED-P12A-02` blocks a write action when the feed already carries untrusted quotes, even with no corpus id. | `docs/24-security-privacy/prompt-injection-controls.md` |
| 12 | `SC-24-01` | The small code control that sets injection when untrusted quotes meet a write action. | `apps/app_a/agent/nodes.py` |
| 12 | `ED-P12-25A-01` to `ED-P12-25A-08` | Phase 12 governance design notes. Example: `ED-P12-25A-07` keeps unread statutes Unknown and issues no certificate. | `docs/25-governance/compliance-obligations.md` |
| 12 | `ED-P12-26A-01` to `ED-P12-26A-08` | Phase 12 TEVV design notes. Example: `ED-P12-26A-07` names behaviours and recorded counts. Percent floors stay Unknown. | `docs/26-tevv/release-thresholds.md` |
| 12 | `SC-26-01` | The same quotes-plus-write block on Application B. | `apps/app_b/opa.py` |
| 13 | `ED-P13-27A-01` to `ED-P13-33B` | Phase 13 design and build notes, one set per hardening sub-stage. Example: `ED-P13-27A-01` returns HTTP 503 when the server key is missing. Health stays 200. | `docs/27-hardening/` through `docs/33-vendor-risk/` |
| 14 | `ED-P14-01` to `ED-P14-04` | Phase 14 measure notes. Example: `ED-P14-01` reuses the Phase 0 formulas on the same 125-case file. `ED-P14-04` prints matched 12 and differing 2 and prints no match percent. | `docs/34-after-kpis/kpi-comparability-check.md` |
| 15 | `ED-P15-01` to `ED-P15-07` | Phase 15 operating notes. Example: `ED-P15-07` shortens the first demo block from 8 minutes to 7 so the paper walk sums to 39. | `docs/42-executive/demo-day-script.md` |
| 16 | `ED-P16-01` | The as-built matrix uses `IP-01` to `IP-10` for the implementation platform rows and `NFR-01` to `NFR-33` for the initial non-functional rows. `SLO-B1` to `SLO-B10` keep the Phase 8 ids. | `docs/final-prd/requirement-disposition-matrix.md` |
| 16 | `IP-01` to `IP-10` | One implementation platform row from the Implementation PRD. | `docs/17-implementation-prd/implementation-prd.md` |
| 3 | `NFR-01` to `NFR-33` | One non-functional requirement from the Initial PRD. | `docs/09-initial-prd/nfrs.md` |

## Change log

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-17 | First issue. Seeded the decision ids, phase and spine ids, status and honesty words, claim labels, reviewer verdicts, policy outcomes, lake terms, and capital-word acronyms already in use. Added the empty "New terms by phase" table for the run to grow. |
| v1.1 | 2026-10-18 | Extended the FD range to `FD-25` (the executor-agent build rule) and named the three run agents and their models by the reviewer verdicts. |
| v1.2 | 2026-10-18 | Named the current three models: coordinator Grok 4.7, executor Grok 4.6, reviewer Composer 2.5. |
| v1.3 | 2026-10-18 | Phase 0 added no new short code. Phase 1 added the `RC-` root-cause ids, the `C-BP*` evidence ids, and `ED-P1-01`. |
| v1.4 | 2026-10-18 | Phase 2 added `R-P2-01` to `R-P2-08` and `ED-P2-01` to `ED-P2-03`. |
| v1.5 | 2026-10-18 | Phase 3 added `F-01` to `F-15`, `FR-01` to `FR-15`, and `ED-P3-01` to `ED-P3-03`. |
| v1.6 | 2026-10-18 | Phase 6 added `EV-01` to `EV-12` and `ED-P6-01` to `ED-P6-05`. Phase 7 added `ED-P7A-01` to `ED-P7A-06` and `ED-P7B-01` to `ED-P7B-05`. Phase 4 added no new short code. |
| v1.7 | 2026-10-18 | Phase 8 added `ED-P8A-01` to `ED-P8A-08` and `ED-P8B-01` to `ED-P8B-05`. Phase 9 Half A added `ED-P9A-01` to `ED-P9A-08`. |
| v1.8 | 2026-10-18 | Phase 10 added `ED-P10A-01` to `ED-P10A-09` and `OPA-R-01` to `OPA-R-12`. |
| v1.9 | 2026-10-18 | Phase 11 added `ED-P11A-01` to `ED-P11A-08` and `ED-P11B-01` to `ED-P11B-02`. |
| v1.10 | 2026-10-18 | Phase 12 added `ED-P12A-01` to `ED-P12A-06`, `SC-24-01`, `ED-P12-25A-01` to `ED-P12-25A-08`, `ED-P12-26A-01` to `ED-P12-26A-08`, and `SC-26-01`. |
| v1.11 | 2026-10-18 | Phases 13 to 16 added `ED-P13-27A-01` through `ED-P13-33B`, `ED-P14-01` to `ED-P14-04`, `ED-P15-01` to `ED-P15-07`, `ED-P16-01`, `IP-01` to `IP-10`, and `NFR-01` to `NFR-33`. |
