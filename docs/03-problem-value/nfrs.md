# Non-functional requirements

| Field | Value |
|---|---|
| Stage | Phase 0 / 3 Frame problem and value |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | COMPLETE. Thresholds that are not in a governed source stay Unknown or PROPOSED |
| Evidence sources | `Project_Intent.md` sections 12 and 13; `docs/operations-service-levels.md`; FD-02; BO-03; BO-10; `app/server.py`; `Execution_Plan.md` section 9 |
| Assumptions | Inherited SLO numbers are historical notes. They are not this project's targets |
| Unresolved issues | Availability, latency, and RTO/RPO targets are Unknown. FD-11 and FD-19 are PENDING |
| Residual risks | Copying 99.5% from the inherited notes would invent a target |

These are needs, not invented numbers.

## Safety and data

| Need | Statement | Target | Label |
|---|---|---|---|
| Data residency | All records stay local and synthetic | In force now (FD-02) | Verified Fact |
| Model tools | Read-only | In force now (FD-02) | Verified Fact |
| Record writes | A person approves each one | BO-03 working answer. Unsigned | Assumption of the working answer |
| Classification | Internal synthetic. Process data confidential. No personal data | BO-10 working answer. Unsigned | Assumption of the working answer |
| Untrusted text | Feed and document text is data, not an instruction | `PRELOADED_DATA.md`, BP7 | Verified Fact of the rule |

## Integrity and audit

| Need | Statement | Target | Label |
|---|---|---|---|
| Baseline freeze | Packaged rows stay until Phase 7 | In force now | Verified Fact |
| Source register | One SHA-256 per inherited file | 1,590 = 1,590 | Verified Fact |
| Audit later | One row per agent step and per approval, with a correlation id | FD-23 default. Design PENDING | Assumption of the default |
| Honesty labels | REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL | In force now | Verified Fact |

## Operability

| Need | Statement | Target | Label |
|---|---|---|---|
| Offline Python path | Standard library. No internet for baseline | Observed on 2026-10-18 | Verified Fact |
| Health endpoint | `GET /health` exists on 8080 and 8090 in code | Present in code. Not timed in this unit | Verified Fact of presence. Latency Unknown |
| Availability | Inherited note 99.5% | Not adopted | Unknown as a project target |
| Recovery time | Inherited note 8 hours | Not adopted | Unknown |
| Recovery point | Inherited note 24 hours | Not adopted | Unknown |
| API p95 | Needed later | Unknown | Unknown |
| Access control | Needed. Missing now | Unknown design (FD-13) | Verified Fact that it is missing |

## Quality

| Need | Statement | Target | Label |
|---|---|---|---|
| Groundedness and citation | Needed for AI answers later | Unknown percent (FD-14) | Unknown |
| Abstention | Silence or overlap routes to review | Working rule | Assumption of the working rule |
| Test characterization | Lock current rules before Phase 7 changes | Later | Verified Fact of the plan |

No numeric SLO is invented on this page.
