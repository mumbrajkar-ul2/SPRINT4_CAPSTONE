# Concentration risk analysis

| Field | Value |
|---|---|
| Stage | Phase 13 / 33 Vendor and concentration risk. Half B measured results. SC-33-01 / HB-33-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-33b-doc-20261018-001 |
| Status | MEASURED. HB-33-01 records the Compose `PYTHONPATH` split and unused Azure on replay. BO-11 stays PROPOSED. `mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. They are not vendor spend. Unit price stays Unknown. |
| Evidence sources | FD-19; FD-13; FD-06; FD-04; FD-15; BO-11; `compose.yaml`; `Dockerfile.platform`; `apps/app_a/intelligence/generate.py`; `apps/app_a/intelligence/azure_client.py`; `apps/app_b/intelligence/generate.py`; `apps/app_a/rules/adapter.py`; `apps/app_b/opa.py`; `docs/28-resilience/ai-disabled-mode.md`; `docs/32-finops/finops-model.md`; `docs/model-comparison/app-b-from-lake.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `tests/platform/test_phase13_vendor_risk.py`; `vendor-inventory.md` |
| Assumptions | `MODEL_MODE=replay`. Azure stays NEEDS_HUMAN. Half B ran HB-33-01 only. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | A later second live-model supplier stays unnamed. Image digest stays Unknown. Numeric floors stay Unknown. A vendor contract stays Unknown. A unit price stays Unknown. |
| Residual risks | Calling Azure on a replay miss would put every GenAI sentence on one unused live path. Adding the inherited path to Application B `PYTHONPATH` would hide a missing lake card. |

This file names where one supplier or one path holds more than one job. Concentration here means that count of jobs. The laptop already splits some of those jobs. This half invents no percent floor for how many jobs one supplier may hold.

Engineering decision ED-P13-33A-03, authority: team-force. Concentration ids `CR-33-01` to `CR-33-06`.

---

## Finding

**Finding.** Six concentration rows sit in this stack. The live language-model path names one supplier: Azure OpenAI. The laptop path uses replay files instead, so that supplier is unused today. HB-33-01 measured Application B compose `PYTHONPATH` as `/opt/platform:/opt/platform/context-lake`. That string has no `fabpulse-legacy`. Application A compose `PYTHONPATH` still ends with `/opt/platform/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`. The Azure boom-patch on one Application A replay miss and one cited hit stayed unused. Four platform services still share one image that copies the inherited tree. Half B did not split that image. BO-11 stays PROPOSED.
**Evidence.** `tests/platform/test_phase13_vendor_risk.py`. `compose.yaml`. `vendor-inventory.md` HB-33-01 after table. FD-06. FD-19. Honesty: REAL.
**Impact.** Half B recorded the Compose split. Half B did not split the image.
**Risk.** Treating the shared image copy as Application B’s rule source would make the lake pin look optional.
**Confidence.** High on the six rows and the pytest output. Unknown on a later second model supplier.
**Open questions.** Reviewer grades HB-33-01. Whether a later phase names a second live-model client.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric floors stay Unknown. This half invents no dollar benefit.

**Verified Fact.** FD-13. Modes `replay` and `azure`. GitHub Actions at the capstone root. Docker Compose at the capstone root.

**Verified Fact.** FD-06. Application B works without Application A. Application B reads only the lake for rules.

**Verified Fact.** FD-15. Application A agent bounds stay recursion limit 12, step budget 8, max tool calls 8, max gather visits 3. Those numbers are engineering defaults. They are not concentration floors.

**Verified Fact** of BO-11. The row stays PROPOSED. No monetary benefit.

---

## Concentration rows

| Id | What is concentrated | Jobs that sit there | What already splits the jobs | Label |
|---|---|---|---|---|
| CR-33-01 | Azure OpenAI | Later live query, explain, and agent draft | `MODEL_MODE=replay` reads `operations/model-replay/`. Application B `generate.py` has no Azure client | Verified Fact of the client and the replay branch |
| CR-33-02 | Inherited workshop tree | Application A `priority`, `evaluate_live_policy`, `intake_apply`, `reconcile_feeds`, packaged SQLite | Application B resolver reads lake cards. Application B source has no `fabpulse-legacy-workshop` string | Verified Fact |
| CR-33-03 | One `Dockerfile.platform` | Image for lake REST, lake MCP, Application A, and Application B. The file copies the inherited tree | Application B compose `PYTHONPATH` omits that tree. Application B still starts from lake REST or the pin | Verified Fact of the file. Inference that a later image-only scan still sees those copied files |
| CR-33-04 | LangGraph | Application A agent pause and checkpoint file | Application B approvals and OPA run in Application B code. Application B has no LangGraph import | Verified Fact |
| CR-33-05 | GitHub Actions | The one CI workflow `verify.yml` | The same pytest files also run on a laptop | Verified Fact |
| CR-33-06 | `python:3.12-slim` tag | Base of the platform image and the inherited image | Digest stays Unknown. A second tag is unnamed | Verified Fact of the tag. Unknown of the digest |

Worked example for CR-33-01. Three GenAI jobs exist: conflict explanation, natural-language query, and agentic planning. **Verified Fact.** FD-04. All three later live calls would use `complete_azure`. On this laptop all three read a SHA-256 file or abstain. Phase 32 measured 0 and 0 live tokens on the shown Application A query. Honesty: REAL. Azure spend stays Unknown.

Worked example for CR-33-02. Application A `adapter.py` sets `LEGACY_ROOT` to `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`. Application B `resolver.py` calls `get_item` on the pin. Parity harness row PH-S8-01 both return recipe `R02` and `R01`. Honesty: REAL. Application B still produced that pair with no inherited import.

---

## What stays up if one concentrated path is down

| Down path | What still runs | Label |
|---|---|---|
| Azure OpenAI unset or unreachable | Health, identity, ranking, intake, lake reads, OPA, approval pause, replay or abstain | Verified Fact of `ai-disabled-mode.md` and FD-19 |
| Inherited workshop import broken | Application B queue, cases, lineage, and query from the lake | Verified Fact of FD-06 and the stopped-A check |
| LangGraph import broken | Application B approvals. Application A deterministic routes that do not start the graph | Inference from Application B having no LangGraph import. Application A graph-down minutes stay Unknown |
| GitHub Actions down | Local `python -m pytest tests/platform` | Verified Fact that the tests live in this repo |
| `python:3.12-slim` pull blocked | Host Python already used by pytest on this machine | Assumption that the host interpreter stays installed. Image rebuild minutes stay Unknown |

Numeric minutes for each row stay Unknown. This table is the split. It is not a recovery-time floor.

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery |
|---|---|---|---|
| FM-33-05 | Replay miss is sent to Azure | A public-network socket on the laptop | Keep the `elif mode == "azure"` branch. Leave replay on a miss as `replay_miss` |
| FM-33-06 | Application B compose gains the inherited `PYTHONPATH` part | Application B can import `legacy_logic` | Restore the two-part path. Re-run HB-33-01 |
| FM-33-07 | Lake pin hash disagrees | Application B start fails | Restore `context-lake/generated/context-lake.sqlite3` that matches the pin |
| FM-33-08 | A later author counts 4982.61 as Azure spend | A fake vendor invoice | Keep bucket 2 SIMULATED and bucket 1 at the measured zeros |

---

## Dead-letter queue and replay

Concentration failures on Azure are recovered by replay or abstain. They are not parked in `dlq.sqlite3`.

Concentration failure on a missing lake card is `HOLD_FOR_REVIEW` or `ABSTAIN` with the item id named. That wait is not a dead-letter intake row.

---

## Runbook — watch concentration

1. Read the six rows in this file.
2. Confirm replay is still the Compose default.
3. Confirm Application B `PYTHONPATH` still has two parts.
4. Confirm Application A `PYTHONPATH` still has the inherited third part. That third part is the Application A rule path. Removing it would break Application A imports.
5. Do not add a second live-model client in this half. Naming a second supplier is a later design.

---

## SLOs and observability

No concentration SLO is set. A percent such as “no supplier may hold more than 30 percent of jobs” is invented here. That cell stays Unknown.

Observability for CR-33-01 is Compose `MODEL_MODE` `${MODEL_MODE:-replay}` and the boom-patch in HB-33-01. Observability for CR-33-02 and CR-33-03 is the Compose `PYTHONPATH` strings plus HB-33-01 and `test_no_app_b_feature_handlers`. Honesty of those pytest facts: REAL.

---

## Cost and the 0C envelope

Concentration does not create a dollar figure. Azure unit price stays Unknown. Replay bucket 1 on the shown path is 0 and 0. Honesty: REAL. This half claims no saving from leaving Azure unused. BO-11 stays PROPOSED.

---

## Exact Half B check HB-33-01

The same check as `vendor-inventory.md`. Half B asserted the Compose `PYTHONPATH` split that keeps CR-33-02 and CR-33-03 from meeting in Application B imports. Half B boom-patched `complete_azure` so CR-33-01 stayed unused on replay.

| Cell | Expected after | Measured after | Honesty |
|---|---|---|---|
| Application B `PYTHONPATH` | `/opt/platform:/opt/platform/context-lake`. No `fabpulse-legacy` | `/opt/platform:/opt/platform/context-lake` | REAL |
| Application A `PYTHONPATH` third part | inherited tree remains | `/opt/platform/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` | REAL |
| Azure boom-patch on Application A replay query | unused | unused. miss `ABSTAIN`, cite `ANSWER` | REAL |
| Shared image split | none in this half | none. `Dockerfile.platform` stays as built | REAL |
| Concentration percent | Unknown | Unknown | Unknown |
| Unit price | Unknown | Unknown | Unknown |
| BO-11 | PROPOSED | PROPOSED | PROPOSED |
| 4982.61 and 0.603 | SIMULATED. Not vendor spend | SIMULATED. Not vendor spend | SIMULATED |

Half B did not split `Dockerfile.platform`. The shared image copy stays as built.

---

## What this file does not do

This file does not write a second model client. It does not split the platform image. It does not invent a concentration percent. It does not call Azure. It does not invent a contract, a unit price, or a dollar benefit. It does not sign BO-11. It does not start Phase 14. It does not update a tracker.
