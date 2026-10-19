# ADR: Application B reads only the lake

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | ACCEPTED. Documents FD-06. Does not change the lock. |
| Evidence sources | `Execution_Plan.md` section 4 and Phase 11; `Project_Intent.md` sections 8 and 8.2; `docs/09-initial-prd/functional-requirements.md` FR-04, FR-14, FR-15; `docs/09-initial-prd/capability-map.md`; `Decision_Tracker.md` FD-06 |
| Assumptions | Shared lake reads for evidence are allowed for Application A. Shared run-time calls between the two apps stay forbidden. |
| Unresolved issues | Parity-harness design is FD-17 PENDING for Phase 11. Lake item schema is FD-07 PENDING for Phase 5. |
| Residual risks | Importing `legacy_logic.py` into Application B would hide a missing lake item. Building Application B from the inherited repo would break the Phase 11 exclude. |

This ADR records the locked rule-source split. Application A takes its rules from its own transformed code. Application B takes its rules only from the Context Lake. That split keeps the comparison honest.

---

## Decision

**Verified Fact.** `Execution_Plan.md` section 4. `Project_Intent.md` section 8.

- Application B decides pass, fail, or wait by reading the Context Lake.
- Application B does not import the transformed rule code.
- Application B does not call Application A at run time.
- Application B does not read the inherited repo at build time. Phase 11 excludes that.
- Application A may read the lake for evidence, citations, and explanation. Application A still takes its rules from its own transformed code.
- Both applications still run scenarios 7 to 11 with the same inputs. Scenario 13 names matches and traces each difference to a lake item.

Worked example. Four programs today apply different urgent tests. Packaged REVIEW count is 2,090. Honesty: REAL. Application A can still evaluate a rebuilt archive test in its own code. Application B evaluates that test when the archive item is in the lake. If the lake leaves out the JavaScript 1.05 tolerance, Application B can mark a case differently. The team then traces that difference to the missing item.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected |
|---|---|---|
| Application B imports transformed code (`legacy_logic.py` or its rebuilt twin) | A second copy of Application A's rules | A missing lake item would not show. FR-14 would always match |
| Application B calls Application A's HTTP API | Application B as a client of Application A | Intent 8.1: each app must work without the other |
| Application B harvests the inherited repo at build time | Read `fabpulse-legacy` while compiling Application B | Phase 11 exclude: reading the legacy repo at build time |
| Both applications take rules only from the lake | Application A also drops its transformed rule path | Application A would no longer show what AI-assisted transformation of the legacy repository delivers. The two-app split in Intent 8 would collapse to one rule source |
| Application B reads operational SQLite tables as if they were lake items | Treat 125 lot rows as knowledge | Phase 5 exclude: copying raw data rows into the lake. Application B would bypass the YAML |

---

## Why this wins for a laptop demo

Minutes 25 to 32 run Application B on the same scenarios, then open the context view. Minutes 32 to 36 compare the two apps.

If Application B can reach Application A's rules, those minutes would always match. A missing lake item would stay hidden.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Accidental shared module | Phase 11 sub-gate: Application B runs without Application A and uses only lake rules |
| Lake missing a rule item | Scenario 13 names the difference and traces it to that item. The open-question channel back to Phase 5 raises the lake version |
| Application A secretly using the lake as its only rule source | Application A rule path stays in transformed code. Lake reads are evidence, not the pass-or-fail test |

---

## Cost and token or runtime impact

Application B retrieval uses lake REST or lake MCP. Those calls are local. They add no model tokens by themselves.

A missing item may cause extra explanation tokens on the comparison slot. That cost is the point of the test. Token numbers stay Unknown.

Honesty: 2,090 REVIEW objects is REAL. Application B result counts are Unknown until Phase 11.

---

## Portability lesson

To test a knowledge store, build a working application that has no other rule source. A second application that can fall back to the first application's code will always look complete.

---

## Finding

**Finding.** Application B takes its rules only from the Context Lake. Application A takes its rules from its own transformed code. Both may read the shared lake for evidence.
**Evidence.** `Execution_Plan.md` section 4. Intent 8. FR-14. FD-06.
**Impact.** Phase 11 builds `apps/app_b/` under that bound. FD-17 designs the harness later.
**Risk.** A hidden import of transformed code would invalidate scenario 13.
**Confidence.** High.
**Open questions.** FD-17 harness design. FD-07 item schema that Application B will read.

---

## What this ADR does not do

This ADR does not write Application B. It does not design the parity harness. It does not start Phase 11. It does not copy legacy code into the lake.
