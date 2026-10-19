# Integration readiness

| Field | Value |
|---|---|
| Stage | Phase 10 / 21 Enterprise integration. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Half A ready for review. Half B implementation stays later. |
| Evidence sources | This folder; `docs/20-application/application-readiness.md`; `playbook/phase_10_agents_hitl.md` Done test |
| Assumptions | Reviewer accepts Half A before Half B. `MODEL_MODE=replay` for automated tests. |
| Unresolved issues | Measured restart, injection BLOCK, and full-trace read stay Half B REAL results. |
| Residual risks | Starting Half B before HALF_A_ACCEPTED would skip the design gate. |

This file is the Half A gate for spine unit 21. It says whether Half B has every bound it needs to wire the adapters.

---

## Finding

**Finding.** Half A names the ten systems, the ten adapters, the six failure families, and the seven reconciliation marks. Half B can implement those rows without inventing a retry count or a dollar cutoff.
**Evidence.** The four sibling files in this folder. Locked facts FD-15, FD-16, FD-23, BO-09.
**Impact.** The coordinator can send this folder to the reviewer.
**Risk.** Treating this file as a measured pass would hide that no adapter write has run yet.
**Confidence.** High on the design list. Unknown on Half B runtime.
**Open questions.** HALF_A_ACCEPTED. OPA binary. FD-19.

---

## Half A checklist

| Check | Status | Label |
|---|---|---|
| Every inbound system is named | Pass in this half | Verified Fact of `integration-inventory.md` |
| Every adapter has a path and a write rule | Pass in this half | Engineering decision ED-P10A-08 |
| Failure classes reuse EH names | Pass in this half | Verified Fact |
| Replay drop waits for RT-05 | Pass in this half | Verified Fact |
| Injection text is a BLOCK input | Pass in this half | Verified Fact |
| Packaged stores stay `mode=ro` | Pass in this half | Verified Fact |
| Checkpoint path is named | Pass in this half | Engineering decision ED-P10A-04 |
| Audit file path is named | Pass in this half | Engineering decision ED-P10A-07 |
| Restart keeps the wait | Design only | Unknown until Half B |
| Adapter unit tests | Not started | Unknown |

---

## Half B must prove

These rows stay open until Half B.

1. Open SYS-01 and SYS-02 with `mode=ro` during an agent run.
2. Kill the process during `interrupt()` and confirm the same `thread_id` is waiting.
3. Feed one IC-01 record and confirm AD-OPA returns BLOCK.
4. Read one correlation id and receive every agent step and the human approval.

Honesty on those four proofs: Unknown in this half. Half B labels them REAL when they pass.

---

## What this file does not do

This file does not start Half B. It does not mark spine unit 21 complete.
