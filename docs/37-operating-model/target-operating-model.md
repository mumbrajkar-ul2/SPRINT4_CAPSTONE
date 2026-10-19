# Target operating model

| Field | Value |
|---|---|
| Stage | Phase 15 / 37 Target operating model |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE for this unit. Ownership assigned to roles. Named people stay Unknown. Company titles stay Unknown |
| Evidence sources | `docs/00-preflight/operating-contract/provisional-operating-contract.md`; `docs/02-stakeholders/decision-rights-map.md`; `docs/25-governance/accountability-map.md`; `Decision_Tracker.md` sections 1, 5, and 7; FD-13; FD-19; FD-21; BO-09; BO-12; `compose.yaml`; `docs/model-comparison/scorecard.md` |
| Assumptions | `MODEL_MODE=replay` stays the laptop default. BO rows that are PROPOSED stay PROPOSED. A later company title map does not change the role ids |
| Unresolved issues | Named signer Unknown. Company job titles Unknown. INC-2025-014 owner Unknown. Numeric floors Unknown. ROI dollars Unknown |
| Residual risks | Filling a person into a role cell. Treating replay as a signed production mode. Presenting EDUCATIONAL ROI as a booked return |

This file names how the laptop solution is run after Phase 15. It assigns duties to roles that already exist. It does not invent a person. It does not invent a company title.

Engineering decision ED-P15-01, authority: team-force. Steady-state ownership uses the four delivery parties plus RT-01 to RT-06. Those ids already sit in `Decision_Tracker.md` section 7 and `docs/25-governance/accountability-map.md`.

---

## Finding

**Finding.** The run after handover has four delivery parties and six live-case roles. Replay is the default path when the live model is off. Both applications stay on the same Compose file. The Context Lake at version 1.0.0 stays the rule store for Application B. Company titles stay Unknown. INC-2025-014 owner stays Unknown.
**Evidence.** FD-13. FD-19. FD-21. BO-09. Accountability map HB-25-06 and HB-25-07. Packaged `owner_id` empty. Playbook log Phase 5 lake version 1.0.0.
**Impact.** An operator can name the owner of a duty without inventing a person.
**Risk.** Writing `demo-rt06-1` as the INC-2025-014 owner.
**Confidence.** High on the role ids and the replay default. Unknown on names, titles, and production hours.
**Open questions.** Who signs the closed contract. Which company titles match RT-01 to RT-06. Who owns INC-2025-014.

---

## What stays running

**Verified Fact.** FD-13. One Compose file at the capstone root. Host ports: 8080 legacy, 8090 source gateway, 8091 lake REST, 8092 lake MCP, 8100 Application A, 8110 Application B.

**Verified Fact.** FD-13 and `operations/model-replay/README.md`. `MODEL_MODE=replay` is the Compose default. Replay reads a file whose name is the SHA-256 of the prompt. This unit counted 77 files in `operations/model-replay/` besides `README.md`. Honesty of that count: REAL for this laptop on 2026-10-18.

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric latency, availability, recovery-time, and recovery-point floors stay Unknown.

**Verified Fact.** Phase 5. Lake version 1.0.0. The build wrote 148 items, 180 edges, and 267 term rows.

Worked example. An operator starts the stack from `c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE` with `docker compose up`. That step is NEEDS_HUMAN. This unit did not start Compose. This unit did not call Azure.

---

## Steady-state duties

| Duty | Owner role | Owner id | Person | Company title | Label |
|---|---|---|---|---|---|
| Change Compose, ports, tests, lake schema | Team-Force | Group A | Role only | n/a for an agent | Verified Fact |
| Industry meaning of open, closed, site, recipe | FDE SME (Semiconductor) | BO-05, BO-06a, BO-07, BO-09 | Role only | Unknown | Verified Fact of the role. Unknown title |
| Charter, headline KPIs, ROI, brand, compliance sign-off | Business Owner | Group B | Unknown | Unknown | Unknown person |
| Accept a Team-Force unit | Reviewer | FD-24 | Agent role | n/a | Verified Fact |
| Dispose a HOLD_FOR_REVIEW case | Fab Exception Reviewer | RT-01 | Unknown | Unknown | Unknown person |
| Approve, hold, or block an agent proposal | Shift Lead or Process Engineer (Approver) | RT-02 | Unknown | Unknown | Unknown person |
| Recipe hold or release | Process Engineer | RT-03 | Unknown | Unknown | Unknown person |
| Policy overlap pick | Policy Owner | RT-04 | Unknown | Unknown | Unknown person |
| Confirm a replay duplicate | Operations Analyst | RT-05 | Unknown | Unknown | Unknown person |
| Assign a missing incident owner | Operations Lead | RT-06 | Unknown | Unknown | Unknown person |

Worked example. INC-2025-014. Packaged `owner_id` is empty. Task `T-00000000` is unassigned. RT-06 assigns a name that a person supplies. This file leaves the owner Unknown. Honesty of the empty field: REAL from Phase 12 HB-25-06.

---

## How a case moves

1. A feed or a packaged case is loaded. Ranking uses stored status, severity, and amount. **Verified Fact.** FD-04.
2. Application A or Application B shows both disagreeing values when two values exist. **Verified Fact.** Scenarios SP-07 to SP-11.
3. The model may draft a cited sentence. The model has no write tool. **Verified Fact.** FD-02. FD-15. `WRITE_TOOLS` is empty.
4. OPA returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK. **Verified Fact.** FD-16.
5. A person in RT-01 to RT-06 records the write. The proposer is never the approver. **Verified Fact.** BO-09.
6. Each agent step and each human approval writes one audit row keyed by correlation id. **Verified Fact.** FD-23.

Worked example. Case `PS000000016`. Recipe pair is R02 and R01. Honesty: REAL from PH-S8-01. RT-03 records hold. The model does not write `engineering_hold`.

---

## Modes the operator may use

| Mode | What it does | When it is used | Label |
|---|---|---|---|
| `MODEL_MODE=replay` | Reads a saved file under `operations/model-replay/` | Laptop demo and this operating model | Verified Fact. FD-13. FD-21 |
| `MODEL_MODE=azure` | Calls Azure OpenAI | Only when a person supplies a key | NEEDS_HUMAN. This unit does not set it |

Containment default CON-29-01 keeps replay on this laptop. Do not set `azure` to rehearse the demo. **Verified Fact.** `operations/containment-procedures.md`.

---

## What this model does not claim

- A named person for any role.
- A company job title for RT-01 to RT-06.
- A signed Business Owner artifact.
- A dollar return. ROI stays EDUCATIONAL. **Verified Fact.** FD-20. BO-11 stays PROPOSED.
- A numeric floor. Exception cycle time stays Unknown. Aged backlog stays Unknown.
- Official Birlasoft brand assets. BO-12 stays PROPOSED. **Verified Fact.**

---

## Phase boundary

This file assigns steady-state roles. The 0B provisional contract is closed in `operating-contract-closure.md`. That closure file stays UNSIGNED. Phase 16 stays unstarted.
