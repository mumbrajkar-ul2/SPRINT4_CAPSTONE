# Decommission checklist

| Field | Value |
|---|---|
| Stage | Phase 15 / 41 Retirement. Decommission checklist |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE as a written list. No wipe was run |
| Evidence sources | `retirement-criteria.md`; `dependency-clearance.md`; `docs/33-vendor-risk/exit-plan.md`; `docs/30-release/rollback-plan.md`; `operations/dr-plan.md`; FD-13; FD-19 |
| Assumptions | The person who later decommissions has git history and a copy of `docs/` | 
| Unresolved issues | Named person who may reset packaged sqlite Unknown. Retention days Unknown |
| Residual risks | Deleting `audit_chain.sqlite3` before a copy exists. Inventing a wipe pass |

This checklist is the later stop sequence. This unit did not stop the stack. This unit did not delete a file.

---

## Finding

**Finding.** A safe stop copies evidence first, leaves replay on until the last demo, then takes Compose down. Packaged sqlite wipe waits on gap G-04. Azure has no resource id to cancel.
**Evidence.** Exit plan. Rollback plan. G-04 in the decision-rights map.
**Impact.** An operator can follow the list without a live wipe today.
**Risk.** Running the wipe rows during Phase 15.
**Confidence.** High on the order. Unknown on wipe hours.
**Open questions.** Who may reset the packaged database.

---

## Checklist

| Step | Action | Done in this unit? | Label |
|---|---|---|---|
| DC-01 | Copy `docs/`, `context-lake/generated/`, `docs/model-comparison/parity-results.json`, and freeze print lines into an archive folder | No. List only | Verified Fact |
| DC-02 | Copy the three Application A host sqlite files | No | Verified Fact |
| DC-03 | Keep `MODEL_MODE=replay`. Leave Azure variables unset | Already the written default | Verified Fact |
| DC-04 | Confirm Application B has no `azure_client` | Already true. Do not re-open Azure to prove it | Verified Fact |
| DC-05 | `docker compose down` from the capstone root | NEEDS_HUMAN. Not run | NEEDS_HUMAN |
| DC-06 | Leave `operations/model-replay/` until a person accepts demo questions will miss | Left in place | Verified Fact |
| DC-07 | Do not delete packaged `legacy.sqlite3` until G-04 names a person | Not deleted | Verified Fact |
| DC-08 | Do not invent a cancellation in a cloud portal | No resource id on file | Verified Fact |
| DC-09 | Record BO-11 still UNSIGNED and ROI still EDUCATIONAL | Recorded on this page | Verified Fact |
| DC-10 | Named retiree signs | Unknown. This page UNSIGNED for that name | Unknown |

Worked example. DC-05 needs Docker. This unit marks it NEEDS_HUMAN. A later paste of `docker compose down` is the only pass.

---

## Sign-off block

| Field | Value |
|---|---|
| Retiree name | Unknown |
| Signature | Not signed |
| Date signed | Not signed |
| Status | UNSIGNED |
| Wipe run | Not run |

This file does not invent a signer. The checklist is written. The wipe is not done.
