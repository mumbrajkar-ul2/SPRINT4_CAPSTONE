# Coverage gap register

| Field | Value |
|---|---|
| Stage | Phase 6 / 13 Traceability |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p6-doc-20261018-001 |
| Status | COMPLETE. No critical requirement is an orphan. Gaps below are named missing tests, later designs, or Unknown numbers. |
| Evidence sources | `docs/13-traceability/requirements-traceability-matrix.md`; `docs/12-specs/`; `Decision_Tracker.md`; lake 1.0.0 queried read-only on 2026-10-18. |
| Assumptions | A gap that says "later phase" is expected. A gap that says "critical orphan" would block this unit. This file has zero critical orphans. |
| Unresolved issues | The gaps themselves. |
| Residual risks | Treating a PLANNED test as done would hide GAP-07. Copying 99.5 percent into a later test would invent GAP-01 as if it were filled. |

This file names every coverage hole this unit can see. A critical orphan is a requirement with no spec. None of FR-01 to FR-15 is an orphan. None of BP1 to BP8 is an orphan.

---

## Finding

**Finding.** Requirements have specs. The remaining holes are unwritten application tests, unsigned policy numbers, Unknown numeric SLOs, and later designs (identity, OPA bodies, audit columns, parity harness).
**Evidence.** Matrix in `requirements-traceability-matrix.md`. Tracker rows FD-13, FD-14, FD-15, FD-16, FD-17, FD-18, FD-19, FD-23 PENDING. BO-06b and BO-08 PROPOSED.
**Impact.** Phase 7 can start from these specs. It cannot treat AT-* as already green.
**Risk.** Filling GAP-01 with an invented p95 would violate FD-11.
**Confidence.** High that no FR row is orphaned. Unknown on later AT-* dates.
**Open questions.** Listed per gap.

---

## Critical orphans

| Requirement | Spec present? | Result |
|---|---|---|
| FR-01 to FR-15 | Yes, in `docs/12-specs/` | No orphan |
| BP1 to BP8 | Yes | No orphan |
| NFR behaviours in the initial PRD | Yes. Numeric cells explicitly Unknown | No orphan |

Worked example. FR-08 needs identity. Specs AC-S11, EH-01, and API-Q-03 name that need. The identity token format is later. That is GAP-02, not an orphaned requirement.

---

## Gaps

### GAP-01 Numeric service targets

| Field | Value |
|---|---|
| Missing | API p95, retrieval p95, availability percent, recovery time, recovery point, groundedness percent, citation percent, abstention percent |
| Why | No governed source states a number. Inherited 99.5 percent is not adopted |
| Spec that records it | `system-spec.md` numeric cells. FD-11 recommended Unknown |
| Test missing | None claimed. A numeric SLO test would be false coverage |
| Owner | Team-Force at FD-14, FD-18, FD-19 |
| Blocks Phase 7? | No |

### GAP-02 Identity mechanism

| Field | Value |
|---|---|
| Missing | Token, header, or cookie format. How an actor_id is issued |
| Why | FD-13 and FD-18 PENDING |
| Spec that records it | EH-01. API shared rules |
| Test missing | AT-ID |
| Owner | Team-Force at Phase 8 and Phase 12 |
| Blocks Phase 7? | No. Transform can proceed. Apps must not copy 8080 open access |

### GAP-03 Application host ports

| Field | Value |
|---|---|
| Missing | Application A port. Application B port |
| Why | Ports ADR left them Unknown. Phase 8 compose assigns them |
| Spec that records it | `system-spec.md`. `api-contracts.md` |
| Test missing | AT-HEALTH for those two ports, once assigned |
| Owner | Team-Force at FD-13 / Phase 8 |
| Blocks Phase 7? | No |

### GAP-04 Company job titles and named people

| Field | Value |
|---|---|
| Missing | Title that matches RT-01 to RT-06. Person names |
| Why | BO-09 leftover. Business Owner confirmation pending |
| Spec that records it | `business-rules.md` role map. Titles Unknown |
| Test missing | None that invents a name |
| Owner | Business Owner for titles. RT-06 at run time for INC-2025-014 |
| Blocks Phase 7? | No |

### GAP-05 BO-06b unsigned

| Field | Value |
|---|---|
| Missing | Signed rule that operational closed also means finance booked and audit closed, or confirmation they stay separate |
| Why | BO-06b PROPOSED |
| Spec that records it | BR-08. GQ-09 HOLD_FOR_REVIEW |
| Test missing | A decided merge test. Must not be written |
| Owner | Business Owner |
| Blocks Phase 7? | No. Cases route to HOLD_FOR_REVIEW |

### GAP-06 BO-08 unsigned

| Field | Value |
|---|---|
| Missing | Signed urgent amount cutoff |
| Why | Archive silent. Working answer: do not invent a number |
| Spec that records it | BR-11. `rule.threshold.silent` |
| Test missing | A decided 50,000 live-policy test. Must not be written |
| Owner | Business Owner |
| Blocks Phase 7? | No |

### GAP-07 Application scenario tests not yet source

| Field | Value |
|---|---|
| Missing | AT-S7 to AT-S13, AT-PERSON, AT-SOD, AT-RANK, AT-CITE, AT-QUERY, AT-RULE, AT-PARITY |
| Why | This unit is DOCUMENT. No code |
| Spec that records it | `spec-to-test-map.md` |
| Test missing | Those AT-* files |
| Owner | Team-Force at Phases 9, 10, 11 |
| Blocks Phase 7? | No. Phase 7 is transform and characterization, not App A UI |

### GAP-08 Characterization tests not yet source

| Field | Value |
|---|---|
| Missing | CT-01 to CT-40 as executable tests |
| Why | Phase 1 wrote a plan. FD-12 still PENDING |
| Spec that records it | `test-to-evidence-map.md` |
| Test missing | `tests/characterization/` in Phase 7 |
| Owner | Team-Force at FD-12 / Phase 7 |
| Blocks Phase 7? | No. Phase 7 is where they are built |

### GAP-09 Audit column list

| Field | Value |
|---|---|
| Missing | Column names, file path, id minting |
| Why | FD-23 PENDING |
| Spec that records it | EV envelope. API-Q-07. SCH audit out of scope |
| Test missing | AT-AUDIT |
| Owner | Team-Force at Phase 10 |
| Blocks Phase 7? | No |

### GAP-10 Agent bounds and OPA bodies

| Field | Value |
|---|---|
| Missing | Recursion-limit number. Tool allow-list beyond the four lake tools. Rego rule bodies |
| Why | FD-15, FD-16 PENDING |
| Spec that records it | EV-08. OPA verdicts named, bodies later |
| Test missing | AT-OPA. AT-RESTART |
| Owner | Team-Force at Phase 10 |
| Blocks Phase 7? | No |

### GAP-11 Parity harness

| Field | Value |
|---|---|
| Missing | Harness design and code |
| Why | FD-17 PENDING |
| Spec that records it | AC-S13. No compare-apps HTTP API |
| Test missing | AT-PARITY |
| Owner | Team-Force at Phase 11 |
| Blocks Phase 7? | No |

### GAP-12 Java money type

| Field | Value |
|---|---|
| Missing | Canonical money type for month-end totals |
| Why | `rule.month_end.float.impl.java` records a float deviation. No signed replacement |
| Spec that records it | BR-15 open question. SCH-09 "what stays out" |
| Test missing | A canonical decimal test. Must not invent a type here |
| Owner | Team-Force if an engineering type is required later. Policy owner if it becomes a finance rule (BO-06b) |
| Blocks Phase 7? | No |

### GAP-13 Headline KPI measures

| Field | Value |
|---|---|
| Missing | Exception cycle time value. Aged backlog cutoff in days |
| Why | Start and end fields unsigned. Age threshold unsigned |
| Spec that records it | AC-MVP numeric cells. CT-40 |
| Test missing | A target-percent test. Must not be written |
| Owner | Business Owner (BO-02). Measure design may be added in Phase 1 leftover / Phase 14 |
| Blocks Phase 7? | No |

### GAP-14 Current inherited tests do not cover HTTP or catalogue counts

| Field | Value |
|---|---|
| Missing | HTTP tests and catalogue assertions in the inherited tree |
| Why | Recorded in the characterization plan |
| Spec that records it | `test-to-evidence-map.md` inherited tests section |
| Test missing | CT-* and AT-HEALTH |
| Owner | Team-Force at Phase 7 |
| Blocks Phase 7? | No. It is the work of Phase 7 |

---

## Gaps this unit must not fill by invention

| Temptation | Why it stays a gap |
|---|---|
| Write 200 ms API p95 | No governed source |
| Write 99.5 percent availability | Inherited note, not adopted |
| Map a company title onto RT-03 | Titles Unknown |
| Sign 50,000 as live policy | BO-08 PROPOSED |
| Merge three closed states | BO-06b PROPOSED |
| Name an INC-2025-014 owner | Unknown |
| Add a compare-apps URL | PRD does not name it |
| Add a user-admin API | PRD does not justify it |

---

## What this file does not do

This file does not close a Business Owner row. It does not write tests. It does not start Phase 7.
