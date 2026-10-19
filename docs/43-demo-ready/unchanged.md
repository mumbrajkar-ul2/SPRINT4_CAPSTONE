# What Phase 17 does not change

| Field | Value |
|---|---|
| Stage | Phase 17 / Live demo and React screens. Half A. |
| Date / version | 2026-10-19, v1.0 |
| Author / agent | Executor agent (Grok 4.7), correlation id corr-p17a-doc-20261019-001 |
| Status | DESIGN. These limits bind Half B. |
| Evidence sources | FD-26; `Deviations_From_Original_Execution_Plan.md`; `playbook/STATUS.md` |
| Assumptions | The packaged sqlite files are the inherited data files. The session is a separate overlay. |
| Unresolved issues | The owner name for `INC-2025-014` stays empty until RT-06 types one. |
| Residual risks | Running `reconcile()` on the packaged store would mark `REPLAY` rows as duplicates and would change the 67-row count. |

Half B keeps these facts.

- The packaged sqlite hash stays the hash of the file Half B started with. Phase 17 does not write that file.
- `reconcile()` is not run on the packaged store.
- `MODEL_MODE=replay`.
- The model write-tool list stays empty.
- Application B does not open the inherited sqlite files to decide a rule.
- Application B does not call Application A.
- The owner of `INC-2025-014` stays empty unless a person at RT-06 types one during the outage page.
- Phase 0 to 16 gate cells in `playbook/STATUS.md` stay `PASS`.
- React stays the screen library. This phase does not replace it with HTML in the ADR.
- DEV-010 through DEV-020 stay open at the end of Phase 17.
