# Controlled-change process

| Field | Value |
|---|---|
| Stage | Phase 15 / 39 Drift and continuous improvement. Controlled change |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE for this unit. Uses the review loop and two-half gate already on disk |
| Evidence sources | FD-22; FD-24; FD-25; `Execution_Plan.md` section 11; `docs/11-data-context/`; `playbook/executor.md`; `change-trigger-thresholds.md`; `docs/30-release/rollback-plan.md` |
| Assumptions | A change that touches the lake, a prompt, OPA, or a KPI definition follows this process. Feature work stays out of Phase 15 |
| Unresolved issues | Named change approver Unknown. Company title Unknown |
| Residual risks | Editing the lake without raising the version. Writing a policy number into code while the BO row is PROPOSED |

This process is how a later change is proposed, checked, and released on the laptop. It reuses the loop Phase 5 already ran. It does not add a new workflow product.

---

## Finding

**Finding.** Lake changes already go through review, fix, and revision, then raise the version with an ADR. Build changes already split into Half A then Half B, with a fresh reviewer. A PROPOSED policy number still routes to HOLD_FOR_REVIEW. Rollback is git restore plus Compose.
**Evidence.** FD-22. FD-24. FD-25. Phase 5 lake version 1.0.0. Phase 13 rollback plan.
**Impact.** An operator has one process for the seven drift families.
**Risk.** A silent YAML edit that Application B then treats as governed fact.
**Confidence.** High on the existing gates. Unknown on the named approver.
**Open questions.** Who signs a later lake ADR. Who may retune prompts.

---

## Steps

1. Name the trigger from `change-trigger-thresholds.md`. Write a correlation id for the change.
2. Say which family moved: lake, prompt, freeze, parity, baseline, injection, or replay files.
3. If the change is a company-liability number, stop coding it. Route cases to HOLD_FOR_REVIEW. Ask the Business Owner. **Verified Fact.** Tracker rule for PROPOSED rows.
4. If the change is a lake item, open the Phase 5 review loop. Raise the version above 1.0.0 with an ADR. **Verified Fact.** FD-22.
5. If the change is application behaviour, write Half A design first. Wait for HALF_A_ACCEPTED. Then write Half B code and a before-and-after check. **Verified Fact.** `Execution_Plan.md` section 11.
6. Re-run the named commands for that family. Use the snapshot integers as the compare sheet. Do not invent a percent floor.
7. A fresh reviewer reads the files on disk. The builder is not the checker. **Verified Fact.** FD-24. FD-25.
8. If the change fails a behaviour trigger, roll back with git plus Compose. Keep the three Application A host sqlite files. **Verified Fact.** `rollback-plan.md`.

Worked example. A person edits `rule.recipe_release.limit.v2023.emea` and changes 18600. That item is cited by GQ-01. The person opens the review loop, raises the lake version, re-runs the freeze, and records the new expected number only after the ADR. Honesty of 18600 today: REAL from Phase 12.

---

## Commands the change must re-run

| Family | Command | Snapshot to compare |
|---|---|---|
| Freeze or prompt | `python apps/app_a/eval/run_freeze.py` | `rows=42 pass=42 fail=0` |
| Parity | `python -m pytest tests/platform/test_parity_harness.py -q --tb=line -s` | matched 12, differing 2 |
| Baseline | `python -m app.baseline` in the inherited app folder | records 125, open_cases 89, urgent_cases 2, sites 6 |
| Injection | `python -m pytest tests/platform/test_app_a_phase12_security.py -q --tb=short` and the Application B TEVV file | HTTP 409 BLOCK |
| Compose file | `docker compose config` | Seven named services. Live `up` stays NEEDS_HUMAN |

---

## What this process refuses

- A new feature during a defence rehearsal. Phase 15 excludes last-minute feature work. **Verified Fact.** Phase 15 scope.
- A live Azure call to hide a replay miss.
- A published match percent.
- A signer name invented to close the change.
