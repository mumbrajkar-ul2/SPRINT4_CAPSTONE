# Scope boundaries

| Field | Value |
|---|---|
| Stage | Phase 0 / 0B Provisional operating contract |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | PROVISIONAL |
| Evidence sources | FD-01, FD-02, FD-03 in `Decision_Tracker.md`; `Execution_Plan.md` sections 3, 4, 5, and 11; `Project_Intent.md` sections 3, 8, and 17; `PRELOADED_DATA.md` |
| Assumptions | The eight business problems in `Execution_Plan.md` section 3 are the in-scope defects. |
| Unresolved issues | BO-04 will confirm the initial PRD later. That sign-off is not this phase. |
| Residual risks | Scope can grow if a later phase adds a defect that is not in BP1 to BP8 without a recorded decision. |

These boundaries are PROVISIONAL. They hold until a later signed PRD replaces them.

## In scope

**Verified Fact.** FD-01. The only system later phases may change is `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`.

**Verified Fact.** `Execution_Plan.md` section 3. The eight business problems the work must show are:

1. Recipe revision differs between dispatch and equipment (BP1).
2. Replayed deliveries inflate the exception queue (BP2).
3. Event time, arrival time, and effective date are confused (BP3).
4. The same rule is built four ways and they disagree (BP4).
5. Open and closed differ across sites and systems (BP5).
6. Three region vocabularies and overlapping policies (BP6).
7. Untrusted text tries to drive decisions (BP7).
8. No API authorization, disputed ownership, and manual reconciliation (BP8).

**Verified Fact.** `Execution_Plan.md` section 4. The locked later target is two independently useful applications over one shared read-only Context Lake. Application A is the transformed legacy workflow. Application B is built only from the lake.

**Verified Fact.** FD-03. The eight KPI families in `Execution_Plan.md` section 9 are the frozen measurement set. The headline pair is exception cycle time and aged backlog (BO-02 working answer).

**Verified Fact.** Phase 0 itself is read-only. It writes documents and `sources/register.yaml` at the capstone root. It changes no file inside the inherited repo.

## Out of scope

**Verified Fact.**

- Any other repository.
- Real customer, employee, or patient records. All records are synthetic (`PRELOADED_DATA.md`).
- Real fab equipment control or a real production release.
- Write tools for the model (FD-02).
- Application behaviour change in Phases 0 to 6 (`Execution_Plan.md` section 11).
- Invented KPI targets, dollar benefits, or success percentages (`Project_Intent.md` section 14.1; BO-02).
- Official Birlasoft brand assets. They are not in hand (`Execution_Plan.md` unresolved issues).
- The optional workshop (500k) and stress (2M) lake tiers. They are not packaged (`PRELOADED_DATA.md`).

## Phase 0 exclude list

**Verified Fact.** `playbook/phase_00_frame_baseline.md` and the coordinator unit. This unit excludes any code change and any app behaviour change. It does not start Phase 1.

## Material finding

**Finding.** Scope is the inherited Fabpulse simulator, the eight named defects, and the eight KPI families. Nothing else is in this contract.
**Evidence.** FD-01, FD-03, `Execution_Plan.md` section 3, `PRELOADED_DATA.md`.
**Impact.** Qualification can name what is in and what is out.
**Risk.** A later demo that uses a 6,000-case regenerated database would leave this scope.
**Confidence.** High.
**Open questions.** The initial PRD (BO-04) can narrow the demo flow later. That does not change this Phase 0 boundary.
