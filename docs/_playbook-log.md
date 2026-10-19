# Playbook log — Sprint 4 Fabpulse capstone

This file is the narrative history. The live board is `playbook/STATUS.md`.

## 2026-10-18 — Phase 0 Frame, govern, and freeze the baseline

Phase 0 passed. Correlation ids: `corr-p0-doc-20261018-001` (executor), `corr-p0-rev-20261018-001` (reviewer), `corr-p0-gate-20261018-001` (coordinator gate). Sub-stages 0A, 0B, 0C, 1, 2, 3, and 4 are in `docs/00-preflight/discovery/`, `docs/00-preflight/operating-contract/`, `docs/00-preflight/ai-economics/`, `docs/01-engagement/`, `docs/02-stakeholders/`, `docs/03-problem-value/`, and `docs/04-baseline-kpis/`, plus `sources/register.yaml`. The reviewer returned STAGE_ACCEPTED. The baseline tools matched on two runs: 125 records, 89 open cases, 2 urgent cases, mean amount 4982.61, 6 sites, 0.603 hours per case. The register has 1,590 hashes for 1,590 inherited files. FD-03 was decided by Team-Force: freeze the eight KPI families in `Execution_Plan.md` section 9. BO-01 and BO-02 stay PROPOSED and unsigned. Engagement is Conditional Go. Exception cycle time and aged backlog stay Unknown. This phase added no new short code. SHA-256 was already in `PROJECT_ACRONYMS.md`.

## 2026-10-18 — Phase 1 Discovery and deep brownfield

Phase 1 passed. Correlation ids: `corr-p1-doc-20261018-001` (executor), `corr-p1-rev-20261018-001` (reviewer), `corr-p1-gate-20261018-001` (coordinator gate). Sub-stages 5, 6, and 7 are in `docs/05-current-state/`, `docs/06-root-cause/`, and `docs/07-repo-assessment/`. The reviewer returned STAGE_ACCEPTED. The eight conflict queries matched the catalogue: BP1 91, BP2 67, BP3 11,985, BP4 2,090, BP5 89, BP6 34, BP7 86, BP8 695. ED-P1-01 records that each row's checkable count is one SQL query. BO-06a still says REVIEW and HOLD are open. The night-batch file flags REVIEW and its comment says it treats REVIEW as open. Exception cycle time and aged backlog stay Unknown. FD-12 stays pending until Phase 7. New short codes: `RC-01` to `RC-08`, the `C-BP*` evidence rows, and `ED-P1-01`.

## 2026-10-18 — Phase 2 AI-versus-no-AI qualification

Phase 2 passed. Correlation ids: `corr-p2-doc-20261018-001` (executor), `corr-p2-rev-20261018-001` (first review, STAGE_CONDITIONAL), `corr-p2-fix-20261018-001` (wording fix), `corr-p2-rev2-20261018-001` (re-review), `corr-p2-gate-20261018-001` (coordinator gate). The folder is `docs/08-ai-qualification/`. The second reviewer returned STAGE_ACCEPTED. The first review failed only because four files still said FD-04 and FD-05 were deferred after those rows were decided. The fix changed that wording. Labels were not changed. The null test on `wafer_lots.engineering_hold` is 125 lots, 8 held, 117 not held. Majority accuracy is 117/125. Leave-one-out logistic regression is 117/125. It does not beat the majority guess. FD-05 is Reject ML. FD-04 is deterministic for triage, rule evaluation, reconciliation, and intake de-duplication. It is GenAI for conflict explanation, natural-language query, and agentic planning. Predicting the hold column is ML-rejected. BO-03 stays PROPOSED. New short codes: `R-P2-01` to `R-P2-08`, and `ED-P2-01` to `ED-P2-03`.

## 2026-10-18 — Phase 3 Initial PRD

Phase 3 passed. Correlation ids: `corr-p3-doc-20261018-001` (executor), `corr-p3-rev-20261018-001` (reviewer), `corr-p3-gate-20261018-001` (coordinator gate). The folder is `docs/09-initial-prd/`. The reviewer returned STAGE_ACCEPTED. The PRD names both apps, the AI limits, BP1 to BP8, and the 40-minute demo flow. Features F-01 to F-15 each map to a business problem. BO-04 stays PROPOSED and the PRD stays unsigned. New short codes: `F-01` to `F-15`, `FR-01` to `FR-15`, and `ED-P3-01` to `ED-P3-03`.

## 2026-10-18 — Phase 4 Target architecture and ADRs

Phase 4 passed. Correlation ids: `corr-p4-doc-20261018-001` (executor), `corr-p4-rev-20261018-001` (reviewer), `corr-p4-gate-20261018-001` (coordinator gate). The folders are `docs/10-architecture/` and `docs/10-architecture/adrs/`. The reviewer returned STAGE_ACCEPTED. Nine ADRs record the locked FD-06 choices, each with rejected options, including the audit chain and the Context Lake review loop. FD-22 and FD-23 were still pending in those ADRs at review time. FD-22 was decided when Phase 5 opened. This phase added no new short code. ADR, OPA, and FTS5 were already in `PROJECT_ACRONYMS.md`.

## 2026-10-18 — Phase 5 Context Lake

Phase 5 passed. Correlation ids: `corr-p5a-doc-20261018-001` (Half A executor), `corr-p5a-rev-20261018-001` (Half A reviewer, HALF_A_ACCEPTED), `corr-p5b-doc-20261018-001` (Half B executor), `corr-p5b-rev-20261018-001` (Half B reviewer, STAGE_ACCEPTED), `corr-p5-gate-20261018-001` (coordinator gate). Folders: `docs/11-data-context/`, `context-lake/`, and `context-lake/review/`. The lake version is 1.0.0. The build wrote 148 items, 180 edges, and 267 term rows. Pytest reported 46 passed. Injection tests did not leak. FD-07, FD-09, FD-10, and FD-22 are DECIDED. BO-06b and BO-08 stay PROPOSED. New short codes: `GQ-01` to `GQ-26`, `ED-P5A-01` to `ED-P5A-09`, and `ED-P5B-01` to `ED-P5B-08`.

## 2026-10-18 — Phase 6 Spec-driven design and traceability

Phase 6 passed. Correlation ids: `corr-p6-doc-20261018-001` (executor), `corr-p6-rev-20261018-001` (reviewer), `corr-p6-gate-20261018-001` (coordinator gate). Folders: `docs/12-specs/` and `docs/13-traceability/`. The reviewer returned STAGE_ACCEPTED. Eight cited lake item ids exist in the lake. FR-01 to FR-15 are not orphans. Numeric SLOs stay Unknown. FD-11 is DECIDED from these specs. New short codes: `EV-01` to `EV-12` and `ED-P6-01` to `ED-P6-05`.

## 2026-10-18 — Phase 7 Transform the repo

Phase 7 passed. Correlation ids: `corr-p7a-doc-20261018-001` (Half A executor), `corr-p7a-rev-20261018-001` (HALF_A_ACCEPTED), `corr-p7b-doc-20261018-001` (Half B executor), `corr-p7b-rev-20261018-001` (STAGE_ACCEPTED), `corr-p7-gate-20261018-001` (coordinator gate). Folders: `docs/14-transformation/`, `docs/15-modernization/`, `docs/16-repo-validation/`, and `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/tests/characterization/`. The characterization suite ran 70 tests and they passed. The six Phase 0 fields matched twice. The approved change is `evaluate_live_policy` returning HOLD_FOR_REVIEW when the archive is silent or has no match. New short codes: `ED-P7A-01` to `ED-P7A-06` and `ED-P7B-01` to `ED-P7B-05`.

## 2026-10-18 — Phase 8 Implementation PRD and delivery foundations

Phase 8 passed. Correlation ids: `corr-p8a-doc-20261018-001` (Half A executor), `corr-p8a-rev-20261018-001` (HALF_A_ACCEPTED), `corr-p8b-doc-20261018-001` (Half B executor), `corr-p8b-rev-20261018-001` (STAGE_CONDITIONAL, Compose health needed a person), `corr-p8-human-20261018-001` (Team-Force paste), `corr-p8-gate-20261018-001` (coordinator gate). Folders: `docs/17-implementation-prd/`, `docs/18-delivery/`, plus `compose.yaml` at the capstone root. Platform pytest reported 24 passed. Team-Force pasted port 8080 `{"status": "ok", "service": "fabpulse-legacy"}` and port 8090 `{"status": "ok", "service": "source-gateway", "domain": "High Tech"}`. FD-13 is DECIDED. Application A is port 8100. Application B is port 8110.

## 2026-10-18 — Phase 9 Intelligence core and Application A

Phase 9 passed. Correlation ids: `corr-p9a-doc-20261018-001` (Half A executor), `corr-p9a-rev-20261018-001` (HALF_A_ACCEPTED), `corr-p9b-doc-20261018-001` (Half B executor), `corr-p9b-rev-20261018-001` (STAGE_ACCEPTED), `corr-p9-gate-20261018-001` (coordinator gate). Folders: `docs/19-intelligence/`, `docs/20-application/`, and `apps/app_a/`. The reviewer re-ran `python apps/app_a/eval/run_freeze.py` and saw 42 of 42. The reviewer re-ran `python -m pytest tests/platform -q` and saw 44 passed. Every AI answer cites a lake item or abstains. Percent floors stay Unknown. The model has no write tool. New short codes: `ED-P9A-01` to `ED-P9A-08`.

## 2026-10-18 — Phase 10 Agents, human approval, and audit chain

Phase 10 passed. Correlation ids: `corr-p10a-doc-20261018-001` (Half A executor), `corr-p10a-rev-20261018-001` (HALF_A_ACCEPTED), `corr-p10b-doc-20261018-001` (Half B executor), `corr-p10b-rev-20261018-001` (STAGE_CONDITIONAL until a process kill), `corr-p10-kill-20261018-001` (coordinator kill), `corr-p10-gate-20261018-001` (coordinator gate). The reviewer re-ran 13 phase tests and 57 platform tests. Injection returned BLOCK. The tool list that reaches the model is six read names. The coordinator started Application A on port 8765, posted case PS000000016, killed pid 29320, started a new process, and read the same correlation id `corr-p10b-kill-20261018-001` back. `engineering_hold` stayed 0. New short codes: `ED-P10A-01` to `ED-P10A-09`.

## 2026-10-18 — Phase 11 Application B from the lake

Phase 11 passed. Correlation ids: `corr-p11a-doc-20261018-001` (Half A executor), `corr-p11a-rev-20261018-001` (HALF_A_REJECTED, one sentence about amount 50000), `corr-p11a-fix-20261018-001` (wording fix), `corr-p11a-rev2-20261018-001` (HALF_A_ACCEPTED), `corr-p11b-doc-20261018-001` (Half B executor), `corr-p11b-rev-20261018-001` (STAGE_ACCEPTED), `corr-p11-gate-20261018-001` (coordinator gate). The reviewer re-ran `python -m pytest tests/platform/test_parity_harness.py -q --tb=line` and saw 7 passed. The harness compared 14 rows. 12 matched. 2 differed. Each difference cites a lake item. No match percent. Application B source has no inherited-repo path, no Application A rule import, and no call to port 8100. New short codes: `ED-P11A-01` to `ED-P11A-08` and `ED-P11B-01` to `ED-P11B-02`.

## 2026-10-18 — Phase 12 Security, governance, TEVV, and red team

Phase 12 passed. Sub-stage 24: correlation ids `corr-p12-24a-doc-20261018-001`, `corr-p12-24a-rev-20261018-001` (HALF_A_ACCEPTED), `corr-p12-24b-doc-20261018-001`, `corr-p12-24b-rev-20261018-001` (STAGE_ACCEPTED). Before the control, approve on feed REPLAY-000000000 with quotes and no corpus id returned HTTP 200 and waited. After the control, the same post returned HTTP 409 BLOCK and changed no record. Pytest: 17 passed, 1 skipped. Sub-stage 25: correlation ids `corr-p12-25a-doc-20261018-001`, `corr-p12-25a-rev-20261018-001` (HALF_A_ACCEPTED), `corr-p12-25b-doc-20261018-001`, `corr-p12-25b-rev-20261018-001` (STAGE_ACCEPTED). Ten file-read checks were recorded. BO-10 stays PROPOSED. No certificate. Sub-stage 26: correlation ids `corr-p12-26a-doc-20261018-001`, `corr-p12-26a-rev-20261018-001` (HALF_A_ACCEPTED), `corr-p12-26b-doc-20261018-001`, `corr-p12-26b-rev-20261018-001` (STAGE_ACCEPTED). Application B quotes-without-id approve went from HTTP 200 EXECUTE to HTTP 409 BLOCK. Freeze re-run: 42 of 42. Pytest: 27 passed, 1 skipped. Percent floors stay Unknown. New short codes: `ED-P12A-01` to `ED-P12A-06`, `ED-P12-25A-01` to `ED-P12-25A-08`, and `ED-P12-26A-01` to `ED-P12-26A-08`.

## 2026-10-18 — Phase 13 Production hardening

Phase 13 passed. Each of sub-stages 27 through 33 has a Half A design and a Half B measured check. Sub-stage 27: a missing server key returns HTTP 503 and health stays 200. Sub-stage 28: a bad intake stays listed after replay. Sub-stage 29: four runbooks are in `operations/` and pytest scored 5 passed. Sub-stage 30: Application A bind-mounts three host sqlite files and pytest scored 9 passed. A live container recreate was not run. Sub-stage 31: a replay miss writes `event=replay_miss`. Sub-stage 32: a replay hit writes `prompt_tokens=0` and `completion_tokens=0`. Dollars stay Unknown. Sub-stage 33: pytest scored 9 passed. Application B has no Azure client. BO-11 stays PROPOSED. Numeric floors stay Unknown.

## 2026-10-18 — Phase 14 Measure, before-versus-after, ROI, and comparison

Phase 14 passed. Correlation ids: `corr-p14-doc-20261018-001` (executor), `corr-p14-rev-20261018-001` (STAGE_ACCEPTED). The reviewer re-ran the parity harness and saw 14 rows, 12 matched, 2 differed. The frozen six-field baseline still matches. Exception cycle time and aged backlog stay Unknown. Every ROI cell is EDUCATIONAL. BO-11 stays PROPOSED and unsigned. New short code: `ED-P14-01` to `ED-P14-04`.

## 2026-10-18 — Phase 15 Operating model, handover, and executive defence

Phase 15 passed. Correlation ids: `corr-p15-doc-20261018-001` (executor), `corr-p15-rev-20261018-001` (STAGE_ACCEPTED). The demo script minute blocks sum to 39. The script cites the Phase 12 HTTP 409 BLOCK and the Phase 10 restart of correlation id `corr-p10b-kill-20261018-001`. Five lessons each cite a phase that ran. The deck is a neutral placeholder. BO-12 stays PROPOSED. Sign-off files stay unsigned. New short codes: `ED-P15-01` to `ED-P15-07`.

## 2026-10-18 — Phase 16 Final as-built PRD

Phase 16 passed. Correlation ids: `corr-p16-doc-20261018-001` (executor), `corr-p16-rev-20261018-001` (STAGE_ACCEPTED). Folder: `docs/final-prd/`. The matrix classifies 75 requirements from the Initial PRD and the Implementation PRD. 54 are Delivered and each cites a spec, a test, a KPI, or an ADR. The as-built ports are 8080, 8090, 8091, 8092, 8100, and 8110. The reviewer re-ran the parity harness and saw 14 rows, 12 matched, 2 differed. BO-13 stays PROPOSED. The sign-off file stays unsigned. The playbook run is complete. New short code: `ED-P16-01`.
