# Assumptions and unknowns

| Field | Value |
|---|---|
| Stage | Phase 0 / 0A Pre-flight orientation |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `Project_Intent.md` sections 17.2 and 17.3; `Execution_Plan.md` header and section 11; `Decision_Tracker.md`; `README.md`; `DATA_READINESS.md`; `docs/operations-service-levels.md`; baseline tool runs on 2026-10-18 |
| Assumptions | Listed in the table below. Each row is an Assumption unless a source already decided it. |
| Unresolved issues | The list of Unknowns below. None of these rows invents an owner or a number. |
| Residual risks | Treating an Assumption as a Verified Fact will leak into later KPI or ROI claims. |

This file separates what is decided, what we are treating as working, and what is Unknown. It does not recommend a transformation.

## Decided facts that orientation relies on

These are locked facts. They are not assumptions.

| Item | Value | Label | Source |
|---|---|---|---|
| System under change | Only `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` | Verified Fact | FD-01 in `Decision_Tracker.md` |
| Data boundary | All data is local and synthetic. The model gets read-only tools only | Verified Fact | FD-02 in `Decision_Tracker.md` |
| KPI families | Eight families in `Execution_Plan.md` section 9 | Verified Fact | FD-03 in `Decision_Tracker.md` |
| Headline business KPIs | Exception cycle time and aged backlog | Verified Fact of the working answer; the row is still PROPOSED | BO-02 in `Decision_Tracker.md` |
| Phase 0 to 6 | No application behaviour change | Verified Fact | `Execution_Plan.md` section 11 |
| File inventory | 1,590 files, all hashed | Verified Fact | `sources/register.yaml` |

## Assumptions in force

| ID | Assumption | Why it is in force | Who must confirm |
|---|---|---|---|
| A-01 | The packaged 125-case database is the measurement population for this freeze | `PRELOADED_DATA.md` says do not generate on first run. The baseline tool read this file | Team-Force if a later phase changes seed or count |
| A-02 | Azure OpenAI is the later model path, with a recorded-replay mode for the laptop demo | `Execution_Plan.md` header Assumptions | Team-Force at Phase 9; live key is a human step from Phase 8 on |
| A-03 | Application B is a full fab-exception app built only from the Context Lake | `Execution_Plan.md` header; trainer confirmed 2026-10-17 | Already recorded. No new confirmation needed for orientation |
| A-04 | Historical service numbers in `docs/operations-service-levels.md` are planning notes, not measured SLOs | That file says they are historical working targets | Business Owner later if a live SLO is signed |
| A-05 | Java and Node are optional and were not needed for this baseline | `README.md` | Anyone who later claims those tools ran |

## Unknowns

| ID | Unknown | Why it is Unknown | Do not invent |
|---|---|---|---|
| U-01 | Named person who signs the charter and the KPI sheet | BO-01 and BO-02 are accepted and still unsigned | An owner name |
| U-02 | Company job titles that match the SME role map | BO-09 is DECIDED for standard roles. The company match is still open | A local title |
| U-03 | Follow-up owner for INC-2025-014 | `operations/incidents/INC-2025-014.md` says the owner is unknown | A new owner |
| U-04 | Whether operational closed also means finance-booked and audit-closed as signed policy | BO-06b is accepted and still PROPOSED. The working answer keeps the three states separate | A merged meaning |
| U-05 | Exception cycle time in hours or days from the baseline tools | `app/baseline.py` does not emit cycle time | A cycle-time number |
| U-06 | Aged backlog count from the baseline tools | `app/baseline.py` emits open_cases and does not define age | An aged-backlog number |
| U-07 | API latency, token counts, and model unit prices | This unit did not start the server and did not call a model | A latency, token, or dollar figure as fact |
| U-08 | Whether Docker Compose runs on this laptop | `DATA_READINESS.md` does not certify Docker | A Compose pass |
| U-09 | Official Birlasoft brand assets | `Execution_Plan.md` unresolved issues | Brand files |
| U-10 | Live unittest count on 2026-10-18 | This unit did not run `unittest` | A new test-pass number |

## Material finding

**Finding.** Orientation can proceed because the decided facts and the packaged tree are enough to qualify. Several business numbers and owners remain Unknown.
**Evidence.** FD-01, FD-02, FD-03. Baseline tool output. `Decision_Tracker.md` BO-01 and BO-02. `app/baseline.py` field list.
**Impact.** Qualification can be a Conditional Go. KPI targets and dollar benefits stay unwritten.
**Risk.** A later author copies the sample 14.1 numbers without a tool run, or fills U-05 and U-06 with invented values.
**Confidence.** High.
**Open questions.** U-01 through U-10 stay open.

## What this file does not do

This file does not close an Unknown. It does not propose a design that would close one.
