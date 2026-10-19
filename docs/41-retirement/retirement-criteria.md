# Retirement criteria

| Field | Value |
|---|---|
| Stage | Phase 15 / 41 Retirement |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Safe-stop criteria exist. Hours and dollars stay Unknown |
| Evidence sources | `docs/33-vendor-risk/exit-plan.md`; `docs/33-vendor-risk/vendor-inventory.md`; `docs/28-resilience/ai-disabled-mode.md`; FD-04; FD-13; FD-19; BO-11 |
| Assumptions | Retirement here means this laptop solution is taken out of use. It is not a company plant shutdown |
| Unresolved issues | Exit hours Unknown. Exit dollars Unknown. Named retiree Unknown |
| Residual risks | Writing a cancellation fee. Setting Azure on to prove an exit |

This file names when the laptop solution may be stopped. Ranking, intake, rules, and reconciliation stay available with the live model off. That fact is already true on replay.

---

## Finding

**Finding.** Azure live use is already off. Application B has no `azure_client`. Replay is the Compose default. Ranking and intake stay up without a live model. A later full stop needs the decommission checklist. Hours and dollars stay Unknown. BO-11 stays PROPOSED.
**Evidence.** HB-33-01. FD-04. FD-13. FD-19. `exit-plan.md`.
**Impact.** An operator can stop the live-model path today by leaving replay on. A full file wipe waits on the checklist.
**Risk.** Saying exit cost is zero dollars.
**Confidence.** High on the already-off Azure path. Unknown on wipe hours.
**Open questions.** Who later records an Azure invoice if a person turns the live path on.

---

## When a part may be stopped

| Part | Safe to stop when | What stays | Label |
|---|---|---|---|
| Azure live path | `MODEL_MODE=replay` and the four Azure variables unset | Health, ranking, intake, lake, OPA, approval, replay or abstain | Verified Fact. Already true |
| Application A agent graph | Application B still answers the same scenarios from the lake | Application B on 8110 | Verified Fact. FD-06 |
| Application B | The defence no longer needs the second app | Application A and the lake files | Verified Fact of the split |
| Legacy 8080 and gateway 8090 | No demo step still opens those ports | 8091, 8092, 8100, 8110 | Verified Fact of the port list |
| Packaged sqlite | Characterization 70 and baseline six fields are archived | Copies under git history | REAL prior for those numbers |
| Replay files | A person accepts that demo questions will miss | Abstain on miss | Verified Fact |
| Whole Compose stack | Handover sign-off is closed or the engagement ends | Git history and `docs/` | Sign-off today UNSIGNED |

Worked example. Azure stop on this laptop is the running state. Phase 32 wrote `prompt_tokens=0` and `completion_tokens=0` on the shown replay hit. Honesty of those zeros: REAL. Honesty of a dollar exit cost: Unknown.

---

## Criteria that stay unmet until a person names them

| Criterion | Value today | Label |
|---|---|---|
| Recovery-time floor after stop | Unknown | Unknown |
| Retention days for audit sqlite | Unknown | Unknown |
| Named person who may wipe packaged sqlite | Unknown. Gap G-04 | Unknown |
| Cancellation clause | None on file | Unknown |

**Verified Fact.** `exit-plan.md` already left those cells Unknown. This page does not fill them.
