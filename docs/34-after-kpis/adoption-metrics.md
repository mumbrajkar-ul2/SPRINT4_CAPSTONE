# Adoption metrics

| Field | Value |
|---|---|
| Stage | Phase 14 / 34 After-intervention KPIs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p14-doc-20261018-001 |
| Status | MEASURED for laptop demo and eval use. Production user adoption stays Unknown. |
| Evidence sources | `docs/model-comparison/parity-results.json`; `docs/model-comparison/parity-harness.md`; `docs/26-tevv/tevv-results.md`; `apps/app_a/eval/freeze-set.yaml`; BO-09; `kpi-comparability-check.md` |
| Assumptions | Adoption on this page is recorded demo and evaluation use on this laptop. Company job titles stay Unknown. |
| Unresolved issues | Production login count Unknown. Named company roster Unknown. Live 40-minute audience count Unknown. |
| Residual risks | Treating six demo actors as a fab workforce. Treating 42 freeze rows as daily user volume. |

Adoption here means who ran a recorded request on Application A or Application B, and which scenario pack they ran. This is a laptop stack. Production plant-user counts stay Unknown.

Engineering decision ED-P14-02, authority: team-force. This page records demo actors, scenario rows, freeze rows, and person posts. It does not invent a production user total.

---

## Finding

**Finding.** The parity harness this unit re-ran used demo actors `demo-rt01-1` through `demo-rt06-1` and roles RT-01, RT-03, RT-04, RT-05, and RT-06. Fourteen compare rows ran. Twelve matched. Two differed. The Phase 12 freeze scored 42 rows. One person hold posted on `PS000000016` as `demo-rt03-1` with proposer `demo-rt02-1`. Production user adoption stays Unknown.
**Evidence.** `parity-results.json` actor_role cells. Pytest this unit. `tevv-results.md`. PH-PERSON-01.
**Impact.** The demo path has named roles and named cases. A workforce percent stays unclaimed.
**Risk.** Calling 14 harness rows an adoption rate.
**Confidence.** High on the recorded actors and row counts. Unknown on production use.
**Open questions.** Company titles that map to RT-01 through RT-06. Audience size for Phase 15.

---

## Recorded actors

Identity headers on `/api` calls are `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role`. Demo actors stay `demo-rt01-1` through `demo-rt06-1`.

| Role | Demo actor used on a harness row | What that actor requested | Honesty |
|---|---|---|---|
| RT-01 | `demo-rt01-1` | Clock pair, lineage, queue flags, query, rule limit, injection question | REAL |
| RT-03 | `demo-rt03-1` | Recipe pair on `PS000000016`. Person hold post | REAL |
| RT-04 | `demo-rt04-1` | Overlapping policies on `FAB-00000002` | REAL |
| RT-05 | `demo-rt05-1` | Replay duplicate case and replay count 67 | REAL |
| RT-06 | `demo-rt06-1` | INC-2025-014 owner and recovery | REAL |
| RT-02 | `demo-rt02-1` as `proposed_by` only | Named as proposer on the hold. The approver on that post is `demo-rt03-1` | REAL |

Worked example. PH-PERSON-01 posts `action_type=recipe_hold_or_release`, `decision=hold`, `actor_role=RT-03`, `actor_id=demo-rt03-1`, `proposed_by=demo-rt02-1`. Both apps record decision `hold` and `engineering_hold=1`. Honesty: REAL. BO-03 stays PROPOSED. A person still writes the hold.

**Verified Fact.** BO-09. The proposer of an action is never its approver. Company job titles stay Unknown.

---

## Recorded scenario use

| Pack or scenario | Rows that ran | Apps | Honesty |
|---|---|---|---|
| S7 / SP-07 | PH-S7-01, PH-S7-02 | Both | REAL |
| S8 / SP-08 | PH-S8-01, PH-CITE-01, PH-PERSON-01 | Both | REAL |
| S9 / SP-09 | PH-S9-01 | Both | REAL |
| S10 / SP-10 | PH-S10-01 | Both | REAL |
| S11 / SP-11 | PH-S11-01, PH-S11-02 | Both | REAL |
| S12 | PH-S12-01 | Application B returns the item. Application A `view_absent` | REAL |
| RANK | PH-RANK-01, PH-RANK-02 | Both | REAL |
| RULE | PH-RULE-01 | Both. Application B second check 2026 APAC 25000 | REAL |
| BP7 | PH-BP7-01 | Both `block=true` | REAL |
| Freeze GQ/SP/UQ/IC | 42 rows, `rows=42 pass=42 fail=0` | Application A freeze. Application B nine-row slice | REAL |

Worked example. S12 is present only on Application B. That designed gap cites `decision.fd06.two_apps`. Application A returns `view_absent`. User-drop counts stay Unknown.

---

## What stays Unknown

| Measure | Status | Why |
|---|---|---|
| Daily active plant users | Unknown | No plant directory in this repo |
| Share of roles that adopted the new screens | Unknown | Only demo actors ran |
| 40-minute talk attendance | Unknown | Phase 15 has not run |
| Repeat use after the hold post | Unknown | Runtime reset on the next harness start |

This page sets no adoption target.
