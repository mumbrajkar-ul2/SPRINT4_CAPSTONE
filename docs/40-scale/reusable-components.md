# Reusable components

| Field | Value |
|---|---|
| Stage | Phase 15 / 40 Scale and roadmap. Reusable components |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Only assets with evidence on disk are marked reusable |
| Evidence sources | `docs/_playbook-log.md`; `docs/11-data-context/`; `docs/model-comparison/parity-harness.md`; `docs/23-human-control/audit-chain.md`; `policy/opa/`; `operations/model-replay/README.md`; `compose.yaml`; FD-06; FD-07; FD-13; FD-16; FD-17; FD-23 |
| Assumptions | Reusable means a later team can copy the asset and the test that proved it. An idea without a file is not reusable |
| Unresolved issues | Hours to copy into a second company stay Unknown. Company titles Unknown |
| Residual risks | Marking Application A's inherited adapter as reusable for Application B. Marking Azure live mode as reusable on this laptop |

This page lists assets that already exist and already have a measured check. Assets without that evidence stay off the reusable list.

Engineering decision ED-P15-05, authority: team-force. Reusable means the file path plus one measured check are both on disk.

---

## Finding

**Finding.** Eight assets meet that bar: the lake schema and build, the replay folder, the OPA three-verdict gate, the audit chain keyed by correlation id, the parity harness, the two-app Compose file, the characterization suite, and the injection BLOCK tests. Application A's inherited-repo import is in use and is not marked reusable for a second app. Azure live mode is not marked reusable.
**Evidence.** Phase 5 pytest 46 passed. Phase 7 characterization 70 passed. Phase 10 audit and kill. Phase 11 and 14 harness 14 rows. Phase 12 HTTP 409. Compose file at the root.
**Impact.** A later roadmap can copy those eight. It cannot copy a brand pack that has not arrived.
**Risk.** Calling the unsigned ROI model reusable as a booked finance tool.
**Confidence.** High on the eight. Unknown on copy hours.
**Open questions.** Whether a later lake version adds a 67-id feed list.

---

## Marked reusable

| Id | Asset | Path | Evidence on disk | Honesty |
|---|---|---|---|---|
| RC-01 | Context Lake item schema and SQLite build | `context-lake/`, `docs/11-data-context/` | Version 1.0.0. 148 items, 180 edges, 267 term rows. Pytest 46 passed | REAL |
| RC-02 | Replay lookup | `operations/replay_lookup.py`, `operations/model-replay/` | 77 files besides README. Miss returns `replay_miss`. No public-network socket | REAL count. PRECOMPUTED file bodies |
| RC-03 | OPA EXECUTE / HOLD_FOR_REVIEW / BLOCK | `policy/opa/app_a.rego`, Application B `opa.py` | FD-16. Injection HTTP 409 after SC-24-01 and SC-26-01 | REAL |
| RC-04 | Audit chain by correlation id | `apps/app_a/audit/` | FD-23. `GET /api/audit/{correlation_id}`. Kill kept `corr-p10b-kill-20261018-001` | REAL |
| RC-05 | Two-app parity harness | `tests/platform/test_parity_harness.py` | 14 rows, matched 12, differing 2. Each difference cites lake items | REAL |
| RC-06 | Laptop Compose stack | `compose.yaml` | Ports 8080, 8090, 8091, 8092, 8100, 8110. `MODEL_MODE` default replay | Verified Fact of the file. Live `up` NEEDS_HUMAN |
| RC-07 | Characterization suite | `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/tests/characterization/` | 70 tests passed in Phase 7 | REAL prior |
| RC-08 | Quotes-plus-approve BLOCK tests | `tests/platform/test_app_a_phase12_security.py`, `tests/platform/test_app_b_phase12_tevv.py` | App A 17 passed, 1 skipped. App B seven HTTP 409 rows | REAL |

Worked example. RC-05. The harness posts the same inputs to 8100 and 8110. PH-S12-01 differs because Application A has no lineage route. The false row lists `decision.fd06.two_apps` and `arch.graph.edges_table`. A later copy must keep that cite rule.

---

## Present and not marked reusable

| Asset | Why it stays off the list | Label |
|---|---|---|
| Application A import of inherited `adapter.py` | Application B must not read that tree. FD-06 | Verified Fact |
| Azure live client on Application A | Live call is NEEDS_HUMAN. This laptop stays on replay | Verified Fact |
| Official Birlasoft deck | Assets have not arrived. BO-12 PROPOSED | Verified Fact |
| ROI spreadsheet | Every cell EDUCATIONAL. Dollars Unknown | EDUCATIONAL |
| Numeric SLO floors | Values Unknown | Unknown |
| Company title map | Titles Unknown | Unknown |

---

## What a later team still needs from a person

- A Business Owner signer.
- Official brand files.
- Docker on the target laptop if they want the six listeners.
- An Azure key only if they later choose the live path. That step stays NEEDS_HUMAN.
