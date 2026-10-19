# Pattern catalog

| Field | Value |
|---|---|
| Stage | Phase 15 / 40 Scale and roadmap. Pattern catalog |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Each pattern cites a phase that already ran |
| Evidence sources | `docs/08-ai-qualification/qualification-decision.md`; `docs/10-architecture/adrs/`; `docs/22-agentic-engineering/`; `docs/23-human-control/`; `reusable-components.md`; FD-04; FD-05; FD-06; FD-16; FD-23 |
| Assumptions | A pattern is a repeatable design that this build already used. A pattern without a measured example stays out |
| Unresolved issues | Fit to a second fab line stays Unknown |
| Residual risks | Selling a pattern as a product. Dropping the human-approval step when copying the agent pattern |

This catalog names the designs this capstone already used. Each row points at evidence.

---

## Finding

**Finding.** Six patterns have both a design file and a measured example: deterministic-versus-GenAI split, lake-as-source-for-the-second-app, interrupt-and-approve, injection-as-data, replay-offline, and correlation-id audit.
**Evidence.** Phase 2 117/125. Phase 5 and Phase 11. Phase 10 interrupt and kill. Phase 12 HTTP 409. Phase 8 replay default. Phase 10 audit.
**Impact.** A later team can copy a named pattern with its check.
**Risk.** Copying interrupt-and-approve without the proposer-is-not-approver rule.
**Confidence.** High on the six. Unknown on a second site.
**Open questions.** Whether a later line needs a second lake version.

---

## Patterns

| Id | Pattern | What it does | Measured example | Phase |
|---|---|---|---|---|
| PAT-01 | Deterministic work stays in code | Ranking, rules, reconciliation, and de-duplication use written tests. The model drafts cited text | `priority()` ranks on status, severity, and amount. Hold prediction rejected. Majority and leave-one-out both 117/125 | Phase 2 |
| PAT-02 | Second app reads only the lake | Application B has no inherited-repo path and no call to port 8100 | Harness 14 rows. 12 matched. 2 differed. Each difference cites a lake item | Phase 5, Phase 11, Phase 14 |
| PAT-03 | Agent drafts and waits | The model has six read tools. Write-tool list is empty. A person records the write | Tool list that reaches the model is six read names. `engineering_hold` stayed 0 across the pid 29320 kill | Phase 10 |
| PAT-04 | Untrusted text stays data | Approve-or-ignore notes do not become an order | `REPLAY-000000000` quotes-plus-approve returned HTTP 409 BLOCK after SC-24-01 | Phase 12 |
| PAT-05 | Offline replay | Saved prompt hashes play back. A miss abstains | Compose default `MODEL_MODE=replay`. 77 files besides README. Shown replay tokens 0 and 0 | Phase 8, Phase 13, Phase 14 |
| PAT-06 | One correlation id for the trace | Every agent step and every approval writes a row. A GET by that id returns the trace | `corr-p10b-kill-20261018-001` stayed on `PS000000016` after restart | Phase 10 |

Worked example for PAT-01. 125 lots. 8 held. 117 not held. Leave-one-out logistic regression scored 117/125. The project built no production hold scorer. Honesty: REAL.

Worked example for PAT-04. Partner note says disregard validation and auto approve. That string is data. OPA returns BLOCK. HTTP 409. The case status stayed `REPLAY`. Honesty: REAL.

---

## Patterns this catalog does not claim

- A multi-region live deployment. This product runs one laptop set. **Verified Fact.** FD-13.
- A branded customer deck. Official assets have not arrived. **Verified Fact.** BO-12.
- A monetary ROI pattern. ROI stays EDUCATIONAL. **Verified Fact.** FD-20.
