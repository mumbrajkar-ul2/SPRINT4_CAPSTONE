# Dependency clearance

| Field | Value |
|---|---|
| Stage | Phase 15 / 41 Retirement. Dependency clearance |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p15-doc-20261018-001 |
| Status | COMPLETE. Clearance is a file check. No supplier was cancelled |
| Evidence sources | `docs/33-vendor-risk/vendor-inventory.md`; `docs/33-vendor-risk/exit-plan.md`; `docs/33-vendor-risk/lock-in-analysis.md`; `compose.yaml`; `apps/app_b/intelligence/generate.py`; FD-06; FD-13 |
| Assumptions | Clearance means the operator knows what still points at a named supplier or a named file |
| Unresolved issues | Vendor contract Unknown. Exit hours Unknown |
| Residual risks | Cancelling a cloud resource that has no resource id on file |

This page lists what still depends on what. A row that is already clear says so.

---

## Finding

**Finding.** Application B already clears the inherited workshop tree and the Azure client. Application A still imports the inherited adapter and still contains an Azure client file that replay does not call. Compose still names `python:3.12-slim` and the workshop Dockerfile. No commercial contract is on file.
**Evidence.** HB-33-01. Application B `PYTHONPATH` is `/opt/platform:/opt/platform/context-lake`. Application A `PYTHONPATH` keeps the workshop path.
**Impact.** A full stop of Application A still needs the inherited tree. A full stop of Azure is already the replay state.
**Risk.** Removing Application A's third `PYTHONPATH` part in a retirement rehearsal and breaking `priority()`.
**Confidence.** High on the path facts. Unknown on contract text.
**Open questions.** Whether a later engagement keeps Application A.

---

## Clearance table

| Dependency | Who still uses it | Already clear? | Evidence | Label |
|---|---|---|---|---|
| Azure OpenAI | Application A client file. Uncalled under replay | Yes for runtime on this laptop | Compose default replay. Four Azure variables unset on Compose blocks | Verified Fact |
| Inherited workshop tree | Application A | No | Application A still imports `adapter.py` | Verified Fact |
| Inherited workshop tree | Application B | Yes | No inherited-repo path. No call to 8100 | Verified Fact |
| LangGraph interrupt | Application A agent pause | No for Application A | Phase 10 checkpoint file | Verified Fact |
| LangGraph | Application B | Yes | Application B answers without it | Verified Fact |
| Open Policy Agent binary | Optional. Local evaluate already returns three verdicts | Yes if the binary is absent | FD-16. `local_evaluate()` | Verified Fact |
| Docker Compose | Full six-port demo | No if the demo still runs | `compose.yaml` | Verified Fact. Live `up` NEEDS_HUMAN |
| Replay file folder | Both apps under replay | No until demo retirement | 77 files besides README | REAL count |
| Packaged `legacy.sqlite3` | Baseline tool and characterization | No until those archives are copied | Six-field JSON. 70 tests | REAL prior |
| Birlasoft brand files | Deck restyle | Nothing to clear | Assets have not arrived | Verified Fact |

Worked example. Application B source has no `azure_client`. A person who retires Azure does not edit Application B. Honesty: REAL from HB-33-01.
