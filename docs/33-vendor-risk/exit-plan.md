# Exit plan

| Field | Value |
|---|---|
| Stage | Phase 13 / 33 Vendor and concentration risk. Half B measured results. SC-33-01 / HB-33-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-33b-doc-20261018-001 |
| Status | MEASURED. HB-33-01 records that the Azure exit steps are already true on disk. Replay is the Compose default. Application B has no `azure_client`. BO-11 stays PROPOSED. `mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. They are not vendor spend. Unit price stays Unknown. |
| Evidence sources | FD-19; FD-13; FD-06; FD-04; BO-11; `compose.yaml`; `.env.example`; `apps/app_a/intelligence/azure_client.py`; `apps/app_b/intelligence/generate.py`; `docs/28-resilience/ai-disabled-mode.md`; `docs/29-incident-bcdr/bc-plan.md`; `docs/32-finops/cost-guardrails.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/model-comparison/app-b-from-lake.md`; `tests/platform/test_phase13_vendor_risk.py`; `vendor-inventory.md` |
| Assumptions | `MODEL_MODE=replay`. Azure stays NEEDS_HUMAN. Half B ran HB-33-01 only. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | A vendor contract stays Unknown. Exit hours stay Unknown. Exit dollars stay Unknown. Numeric recovery floors stay Unknown. A signer name stays Unknown. A unit price stays Unknown. |
| Residual risks | Writing a cancellation fee would invent a contract. Setting `MODEL_MODE=azure` to “test the exit” would open a public-network socket. |

This file names the steps to stop using a named supplier on this laptop. Exit here means those steps. No contract is on file, so no cancellation clause is written. Recovery-time and recovery-point stay Unknown.

Engineering decision ED-P13-33A-07, authority: team-force. Company titles and the signer stay Unknown. BO-11 stays PROPOSED.

Engineering decision ED-P13-33A-08, authority: team-force. Half B does not execute an Azure exit rehearsal and does not call Azure.

---

## Finding

**Finding.** The laptop is already off the Azure live path. HB-33-01 measured Compose Application A and Application B `MODEL_MODE` as `${MODEL_MODE:-replay}`. The four Azure variables stay unset on those Compose blocks. Application B `PYTHONPATH` is `/opt/platform:/opt/platform/context-lake`. Application B source has no `azure_client`. Application A query under replay finished without the Azure boom-patch. Hours and dollars for later file edits stay Unknown. BO-11 stays PROPOSED. `mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. They are not vendor spend.
**Evidence.** `tests/platform/test_phase13_vendor_risk.py`. `compose.yaml`. FD-19. BO-11. Honesty: REAL for the pytest. Unknown for exit hours and exit dollars.
**Impact.** Half B recorded the unused-Azure and Application B isolation facts. Half B did not cancel a service and did not rewrite Application A.
**Risk.** A later author who writes “exit cost is zero dollars” would invent a unit price.
**Confidence.** High on the replay-already-off-Azure steps and the pytest. Unknown on hours to leave LangGraph or Compose.
**Open questions.** Reviewer grades HB-33-01. Who later records an Azure invoice if a person turns the live path on.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. Recovery-time and recovery-point stay Unknown. This half invents no dollar benefit.

**Verified Fact.** FD-13. Modes `replay` and `azure`. No third offline mode.

**Verified Fact.** FD-06. Application B already runs without Application A.

**Verified Fact.** FD-04. Ranking, intake, rules, and reconciliation stay up with the live model off.

**Verified Fact** of BO-11. Label every ROI number EDUCATIONAL. Claim no monetary benefit. The row stays PROPOSED. Company titles and the signer stay Unknown.

**Verified Fact.** Azure live use stays NEEDS_HUMAN.

---

## Exit steps by supplier

Minutes for each row stay Unknown. These are the steps. They are not a recovery-time floor. Dollar cells stay Unknown.

| Supplier | Steps on this laptop | What stays running | Contract step | Label |
|---|---|---|---|---|
| Azure OpenAI | Keep `MODEL_MODE=replay`. Leave `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT`, and `AZURE_OPENAI_API_VERSION` unset | Health, ranking, intake, lake, OPA, approval, replay or abstain | None on file | Verified Fact of the mode. Unknown of a later invoice |
| Inherited workshop tree for a second app | Already done. Application B source and compose `PYTHONPATH` omit that tree | Application B from the lake | Not a commercial supplier | Verified Fact |
| Inherited workshop tree for Application A | Out of this half. Application A still imports `adapter.py` | Application B | None | Verified Fact that the edit is unnamed here |
| LangGraph | Application B already answers without it. Application A agent pause still uses it | Application B approvals and Application A deterministic routes | Unknown | Verified Fact of Application B. Unknown hours for Application A |
| Docker Compose | Pytest already runs on host Python. Full six-port demo still uses Compose | File checks and unit tests | Unknown | Verified Fact that tests live in-repo |
| GitHub Actions | Run the same pytest locally | Local verify | Unknown | Verified Fact |
| Open Policy Agent binary | Leave the binary absent. `local_evaluate()` already returns the three verdicts | EXECUTE, HOLD_FOR_REVIEW, BLOCK | Unknown | Verified Fact |
| `python:3.12-slim` | Host Python 3.12 in CI. A replacement tag is unnamed | Pytest on the host interpreter | Unknown | Verified Fact of CI Python 3.12. Unknown of a replacement tag |

Worked example. Azure exit on this laptop is already the running state. A person does not log into Azure. A person does not unset a billed resource because this half has no resource id. `POST /api/query` under replay still returns a PRECOMPUTED sentence or `replay_miss`. Phase 32 wrote `prompt_tokens=0` and `completion_tokens=0` on the shown hit. Honesty of those zeros: REAL. Honesty of a dollar exit cost: Unknown.

Worked example. Inherited-tree exit for a second application is already the running state. Application B `PYTHONPATH` has two parts. Application A `PYTHONPATH` keeps the third part so Application A still imports `priority`. Removing that third part in this half would break Application A.

---

## Order if a person later turns Azure on, then wants it off again

1. Set `MODEL_MODE=replay` in the process environment and in Compose.
2. Leave the four Azure variables unset, or remove them from the local environment. Do not write them into source.
3. Confirm `complete_azure` is uncalled by running HB-33-01.
4. Keep saved replay files under `operations/model-replay/`. Those files stay the laptop sentences.
5. Leave unit price Unknown. Leave BO-11 PROPOSED.

A person who ran a live Azure rehearsal still holds the only key. That step stays NEEDS_HUMAN. This half does not do it. This half does not name a cloud portal click, because no resource id is on file.

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery |
|---|---|---|---|
| FM-33-17 | Exit is described as a signed saving | A benefit sentence | Delete the sentence. Keep BO-11 PROPOSED |
| FM-33-18 | Exit rehearsal sets `MODEL_MODE=azure` | A public-network call or `missing_model_config` | Set `MODEL_MODE=replay` |
| FM-33-19 | Application A `PYTHONPATH` loses the inherited part during an Application B check | Application A import fails | Restore the three-part Application A path |
| FM-33-20 | Replay files are deleted as part of an Azure exit | Every GenAI question abstains | Restore `operations/model-replay/` from version control |

---

## Dead-letter queue and replay

Exit of Azure uses replay files. Exit of a bad intake uses `apps/app_a/runtime/dlq.sqlite3`. Those stores stay separate.

Do not delete the dead-letter file to “leave a vendor.” That file is first-party Application A state.

---

## Runbook — stop using Azure on this laptop

1. Read `MODEL_MODE` on `app-a` and `app-b`. Expect `replay`.
2. Confirm the four `AZURE_OPENAI_*` names are absent from Compose environment blocks.
3. Run `python -m pytest tests/platform/test_phase13_vendor_risk.py -v --tb=short`. Expect the boom-patch to stay unused.
4. If a sentence claims a dollar saving, stop.

This half did not copy this runbook into `operations/`. The accepted check is the pytest only.

---

## SLOs and observability

Exit time stays Unknown. Recovery-time and recovery-point stay Unknown. **Verified Fact.** FD-19.

Observability is Compose `MODEL_MODE`, the unset Azure variables, stdout `model_mode=replay`, and HB-33-01.

---

## Cost and the 0C envelope

The 0C envelope left inference cost Unknown. Phase 32 measured 0 and 0 live tokens on the shown Application A replay query. Honesty: REAL. That pair is not an exit invoice. Unit price stays Unknown. ROI stays unsigned. BO-11 stays PROPOSED.

`mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. They are not a vendor cancellation figure.

---

## Exact Half B check HB-33-01

The same check as `vendor-inventory.md`. Half B recorded that the Azure exit steps are already true on disk: replay default, Application B without `azure_client`, Application B `PYTHONPATH` without the inherited tree.

| Cell | Expected after | Measured after | Honesty |
|---|---|---|---|
| Vendor-risk pytest file | `tests/platform/test_phase13_vendor_risk.py` exists | present. 9 passed | REAL |
| Compose Application A `MODEL_MODE` | `${MODEL_MODE:-replay}` | `${MODEL_MODE:-replay}` | REAL |
| Compose Application B `MODEL_MODE` | `${MODEL_MODE:-replay}` | `${MODEL_MODE:-replay}` | REAL |
| Compose Application B path | two parts. no inherited tree | `/opt/platform:/opt/platform/context-lake` | REAL |
| Azure call on one Application A replay query | uncalled | boom-patch unused. miss `ABSTAIN`. cite `ANSWER` | REAL |
| Extra `operations/` runbook | none | none | REAL |
| Exit hours | Unknown | Unknown | Unknown |
| Exit dollars | Unknown | Unknown | Unknown |
| Unit price | Unknown | Unknown | Unknown |
| Contract | Unknown | Unknown | Unknown |
| BO-11 | PROPOSED | PROPOSED | PROPOSED |
| `mean_amount` 4982.61 | SIMULATED. Not vendor spend | SIMULATED. Not vendor spend | SIMULATED |
| `hours_per_case` 0.603 | SIMULATED. Not vendor spend | SIMULATED. Not vendor spend | SIMULATED |

Half B did not create a cloud resource. Half B did not delete `azure_client.py`. Half B did not add a feature.

---

## What this file does not do

This file does not cancel an Azure resource. It does not invent a contract, a unit price, or a dollar benefit. It does not sign BO-11. It does not name a company title or a signer. It does not copy an extra runbook into `operations/`. It does not start Phase 14. It does not update a tracker.
