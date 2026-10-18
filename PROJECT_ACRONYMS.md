# Project acronyms — Sprint 4 Fabpulse capstone

| Field | Value |
|---|---|
| Stage | Reader guide. Runs beside `Execution_Plan.md`, `Decision_Tracker.md`, and `playbook/STATUS.md`. |
| Date / version | 2026-10-18, v1.2 |
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
| — | — | — | — |

## Change log

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-17 | First issue. Seeded the decision ids, phase and spine ids, status and honesty words, claim labels, reviewer verdicts, policy outcomes, lake terms, and capital-word acronyms already in use. Added the empty "New terms by phase" table for the run to grow. |
| v1.1 | 2026-10-18 | Extended the FD range to `FD-25` (the executor-agent build rule) and named the three run agents and their models by the reviewer verdicts. |
| v1.2 | 2026-10-18 | Named the current three models: coordinator Grok 4.7, executor Grok 4.6, reviewer Composer 2.5. |
