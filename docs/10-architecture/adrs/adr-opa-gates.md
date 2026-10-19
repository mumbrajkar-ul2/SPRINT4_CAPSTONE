# ADR: OPA gates

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | ACCEPTED. Documents FD-06. Does not change the lock. Rego rule bodies stay later (FD-16). |
| Evidence sources | `Execution_Plan.md` section 4 and Phase 10; `Project_Intent.md` sections 10.2 and 12; `docs/09-initial-prd/functional-requirements.md` FR-06, FR-07, FR-13; `Decision_Tracker.md` FD-06, FD-16, BO-03, BO-08 |
| Assumptions | OPA is Open Policy Agent. It loads a policy file and returns a verdict. Sprint 3 used EXECUTE, HOLD_FOR_REVIEW, and BLOCK. This lock reuses those three strings. |
| Unresolved issues | FD-16 PENDING for Phase 10: the actual policy rules. BO-03 and BO-08 stay PROPOSED. |
| Residual risks | Letting the language model choose EXECUTE would make the model the gate. Writing unsigned policy numbers into Rego would treat a PROPOSED row as code. |

This ADR records the locked policy-gate choice. OPA returns one of three results: EXECUTE, HOLD_FOR_REVIEW, or BLOCK.

---

## Decision

**Verified Fact.** `Execution_Plan.md` section 4. Phase 10 locked facts.

OPA decides whether a proposed action may run, must wait for a person, or must stop.

| Verdict | What the application does |
|---|---|
| EXECUTE | The next code step may run. A record-changing action still waits on the human gate under the BO-03 working answer |
| HOLD_FOR_REVIEW | The case waits for a named run-time role (RT-01 to RT-06) |
| BLOCK | The action stops. The injection corpus in Phase 5 and Phase 10 must produce this result |

The policy files will live under `policy/opa/` in Phase 10. This ADR does not write them.

**Verified Fact.** BO-08 working answer, still PROPOSED. Where the governed source is silent, the case routes to review. No new threshold is invented. This ADR does not sign BO-08.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected |
|---|---|---|
| Allow or deny only | Two states | Overlap (BP6), silent threshold (BO-08), and unsigned policy have no wait state. HOLD_FOR_REVIEW would disappear |
| The language model as the gate | The model judges its own draft | BP7 untrusted text could drive that judgment. Intent 10.2 keeps authorization and policy enforcement in code |
| Scattered `if` tests in each application | Each app encodes the gate in Python | Application A and Application B could disagree on the same action. The shared policy file would be missing |
| Mixing HOLD into EXECUTE | Auto-run the draft when the model is "sure" | BO-03 working answer: a person approves every record-changing action |
| A commercial decision-engine SaaS | Hosted rules | The laptop demo and the offline replay path would depend on a network product that this plan does not name |

Worked example. 34 active `policy_register` rows sit on eight country codes. Honesty: REAL. Two overlapping rows match one object. OPA returns HOLD_FOR_REVIEW. A Policy Owner at RT-04 picks a policy or keeps the wait. The model does not pick.

Worked example. 86 partner feeds carry `auto approve` or `disregard validation`. Honesty: REAL. OPA returns BLOCK on the injection path. The feed text stays a flagged quote.

---

## Why this wins for a laptop demo

Minutes 36 to 39 must show an injection that is blocked. Scenario 10 must show a wait.

Three named strings are easy to show on a trace panel. OPA  runs locally. Sprint 3 already used these three outcomes, so the names stay stable across sprints.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Policy files drift between Application A and Application B | One `policy/opa/` tree. Both apps call it |
| Unsigned numbers compiled into Rego | PROPOSED rows stay out of code. Route those cases to HOLD_FOR_REVIEW |
| EXECUTE on a write skipping the person | Human gate still sits after OPA for record changes (BO-03 working answer) |
| Inventing the Rego now | Leave FD-16 PENDING |

---

## Cost and token or runtime impact

OPA evaluation is local CPU. It adds no model tokens.

Putting the gate in the model would spend tokens on every policy check and would vary with wording. That cost and that variance are avoided.

Honesty: OPA latency is Unknown until measured. Injection feed count 86 is REAL.

---

## Portability lesson

Keep the allow, wait, and stop decision in a policy file that both applications call. Keep the three-way wait state. A two-way allow-or-deny drops the review path this engagement needs for overlap, silence, and unsigned liability.

---

## Finding

**Finding.** OPA returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK. That three-verdict gate is locked.
**Evidence.** `Execution_Plan.md` section 4. Phase 10. FD-06.
**Impact.** Phase 10 writes `policy/opa/`. FD-16 fills the rule bodies.
**Risk.** Using the model as the gate would let untrusted text drive a write.
**Confidence.** High on the three verdicts. Unknown on the rule bodies.
**Open questions.** FD-16. BO-03 unsigned. BO-08 unsigned.

---

## What this ADR does not do

This ADR does not write Rego. It does not invent a threshold. It does not sign BO-03 or BO-08. It does not start Phase 10.
