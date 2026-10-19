# Lake version

| Field | Value |
|---|---|
| Stage | Phase 5 / 11R Review, fix, and revision loop. Half B. |
| Date / version | 2026-10-18, v1.0.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5b-doc-20261018-001 |
| Status | ACCEPTED for this unit. Version 1.0.0 after one review round. |
| Evidence sources | FD-22; ED-P5A-07; `lake-review.md`; `lake-fixes.md`; `generated/manifest.json`; `generated/app-b-pin.json` |
| Assumptions | Later changes go through this loop with an ADR. Add items = patch. Change meaning = minor with an ADR. Remove an id = major. |
| Unresolved issues | Named reviewer for later model-drafted items is Unknown. |
| Residual risks | Editing `context-lake.sqlite3` by hand would disagree with the YAML in Git. |

The Context Lake version is **1.0.0**.

`generated/manifest.json` records the same version. `generated/app-b-pin.json` pins version 1.0.0 and sqlite sha256 `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Honesty: REAL from the file.

One review round is complete. Numbered fixes are in `lake-fixes.md`.

A later change must run this loop again and raise the version with an ADR. Adding items with the same meaning raises the patch number, for example 1.0.1. Changing the meaning of an id raises the minor number, for example 1.1.0, and needs an ADR. Removing an accepted id raises the major number, for example 2.0.0.

This file does not start Phase 6.
