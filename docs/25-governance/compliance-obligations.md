# Compliance obligations

| Field | Value |
|---|---|
| Stage | Phase 12 / 25 Governance and assurance. Half B evidence. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-25b-doc-20261018-001 |
| Status | MEASURED. HB-25-04 and HB-25-05 recorded. BO-10 stays PROPOSED. Statute applicability stays Unknown. |
| Evidence sources | BO-10 PROPOSED and accepted; FD-18 DECIDED; FD-02; FD-14; FD-16; FD-23; BO-03; BO-09; `Project_Intent.md` section 12.2; `Decision_Tracker.md` section 5.1 and 5.2; `docs/24-security-privacy/threat-model.md`; `docs/12-specs/business-rules.md`; directory listing of `docs/25-governance/` |
| Assumptions | BO-10 working answer holds: all records are internal and synthetic; process data is confidential; packaged rows do not contain personal data. `MODEL_MODE=replay`. Documents stay unsigned. |
| Unresolved issues | Named statute applicability stays Unknown. Retention days stay Unknown. Named signer stays Unknown. Company job titles stay Unknown. |
| Residual risks | Copying an unread statute into a duty row would invent an obligation. Issuing a certificate from this folder would invent a compliance pass. |

This file names the working obligations this capstone already accepted. The Context Lake is the SQLite knowledge store built in Phase 5. This file issues no compliance certificate.

Engineering decision ED-P12-25A-01, authority: team-force. Working-obligation ids `OB-25-01` to `OB-25-12`. Statute-family ids `ST-25-01` to `ST-25-05`. Half B recorded those ids. Half B did not add a statute.

---

## Finding

**Finding.** Twelve working obligations come from locked tracker rows and the BO-10 classification. Five statute families stay Unknown. Each Unknown family maps to the working classification instead of a copied law. Half B confirmed BO-10 stays PROPOSED and this folder has no certificate file.
**Evidence.** BO-10 PROPOSED and accepted 2026-10-18. FD-18 DECIDED. `Project_Intent.md` section 12.2 evidence note: the repository is synthetic and does not establish actual regulatory scope. HB-25-04 and HB-25-05 Recorded sentences.
**Impact.** The control matrix and the register use these ids. Half B filled evidence cells. Half B signed nothing.
**Risk.** Treating an accepted PROPOSED row as a signed law would hide that BO-10 stays unsigned.
**Confidence.** High on the working rows and on the two file reads. Unknown on every named statute.
**Open questions.** BO-10 signer name stays Unknown. Statute applicability stays Unknown. Retention days stay Unknown.

---

## Locked facts this design applies

**Verified Fact.** BO-10 working answer, still PROPOSED. Treat all records as internal and synthetic. Process data is confidential. There is no personal data. The classification artifact stays unsigned. The person's name stays Unknown.

**Verified Fact.** FD-18. A hallucination is an AI answer that does not cite a lake item. Injection BLOCK drives no action. Numeric percent floors stay Unknown.

**Verified Fact.** FD-02. All data is local and synthetic. The model gets read-only tools only.

**Verified Fact.** `Project_Intent.md` section 12.2. Semiconductor, privacy, records, cybersecurity, export-control, customer-contract, and responsible-AI statutes must be confirmed with qualified owners. This half does not confirm them.

---

## How to read a row

Each row stands alone. `Source` is the locked tracker or intent sentence. `Status` is the tracker status. `Owner of the duty` is the role that accepts or applies the duty. Named people stay Unknown.

Worked example. OB-25-01 says process data is confidential. Recipe revision `R02` versus `R01` on lot `L00000016` stays on this laptop. That pair is synthetic process data. It is not a person's name.

---

## Working obligations

These rows are the duties this build already follows. They are not a certificate.

| Id | Working obligation | Source | Status | Owner of the duty | What a reader can picture |
|---|---|---|---|---|---|
| OB-25-01 | Treat every packaged record as internal and synthetic. Keep process fields confidential. Packaged rows contain no personal data. | BO-10 | PROPOSED, accepted 2026-10-18, unsigned | Business Owner signs later. Team-Force applies the handling now | `data/legacy.sqlite3` stays on this laptop. Actor `demo-rt01-1` is a laptop label |
| OB-25-02 | Keep data local and synthetic. Give the model read-only tools only. | FD-02 | DECIDED | Team-Force | `WRITE_TOOLS` stays `[]`. Packaged stores open `mode=ro` |
| OB-25-03 | AI explains and proposes. A person approves every record-changing action. | BO-03 | PROPOSED, accepted, unsigned | Business Owner signs later. RT-01 to RT-06 record the write | Scenario 8 wait. RT-03 records hold |
| OB-25-04 | Use the closed role list RT-01 to RT-06. The proposer of an action is never its approver. | BO-09 | DECIDED, authority: sme | FDE SME set the map. Business Owner still confirms company titles | `X-Actor-Role` is one of six strings. Company title stays Unknown |
| OB-25-05 | Every scored AI answer cites a retrieved lake item id or abstains. A hallucination is an AI answer that does not cite a lake item. | FD-14. FD-18 | DECIDED | Team-Force | Empty ANSWER citations become ABSTAIN. Floor stays Unknown |
| OB-25-06 | Injection text stays data. The gate returns BLOCK. That text drives no action. | FD-18. FD-16. IC-01 to IC-06 | DECIDED | Team-Force | Phase 24 after-check: HTTP 409, empty approvals. Honesty REAL |
| OB-25-07 | Write one audit row per agent step and one audit row per human approval. Join them by correlation id. | FD-23 | DECIDED | Team-Force | `GET /api/audit/{correlation_id}` returns the full list in `seq` order |
| OB-25-08 | Change lake knowledge through the review loop. Runtime apps read the lake. `build.py` writes the lake file. | FD-07. FD-22 | DECIDED | Team-Force | Lake version 1.0.0. Pin hash in `app-b-pin.json` |
| OB-25-09 | Label every claim. Label every demo number REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL. | FD-20. Execution plan honesty rule | DECIDED for the label set | Team-Force | Replay sentence wording is PRECOMPUTED. Freeze counts are REAL |
| OB-25-10 | Keep accepted PROPOSED artifacts unsigned until a named Business Owner signs. Do not invent a signer. | BO-10. BO-01. BO-13 | PROPOSED rows stay unsigned | Business Owner | This folder has no signature block with a person's name |
| OB-25-11 | Mark generated text as a draft. Source facts stay in code, lake items, and person decisions. | `Project_Intent.md` 12.2 | Intent requirement. Working practice in prompts | Team-Force for prompts. RT roles for writes | `draft_plan` is a proposal. `engineering_hold` waits for RT-03 |
| OB-25-12 | Record retention as Unknown until a signed owner sets a day count. Keep the audit file until that owner decides. | Audit-chain unresolved issue. No signed retention row | Unknown | Business Owner for a later signed count. Team-Force records the gap | `apps/app_a/audit/audit_chain.sqlite3` exists. Day count stays blank |

Worked example for OB-25-05. Freeze run 2026-10-18 scored 42 of 42 under cite-or-abstain. Honesty of the count: REAL. The percent floor stays Unknown. 42 of 42 is a measured count. It is not a 90 or 95 target.

Worked example for OB-25-06. Corpus row IC-01 proposes approve from harvested text. Application A returns BLOCK. No `record_approval` runs. Honesty of the Phase 10 and Phase 24 BLOCK runs: REAL.

---

## Statute families left Unknown

Engineering decision ED-P12-25A-07, authority: team-force. A statute family with no confirmed applicability stays Unknown. The working classification is the row Half B records. This half copies no article text.

| Id | Statute family | Applicability | Working map instead | Who can later confirm |
|---|---|---|---|---|
| ST-25-01 | A privacy statute that governs personal data, including any GDPR-class rule | Unknown | OB-25-01. Packaged rows contain no personal data. Actor fields are laptop demo ids | Business Owner with a qualified privacy owner |
| ST-25-02 | An AI-product statute, including any EU AI Act-class rule | Unknown | OB-25-05, OB-25-06, OB-25-11, plus the model card and the system card | Business Owner with a qualified compliance owner |
| ST-25-03 | An export-control statute for semiconductor process data | Unknown | OB-25-01. Process data stays confidential and on this laptop | Business Owner with a qualified trade-control owner |
| ST-25-04 | A records-retention statute | Unknown | OB-25-12. Retention days stay Unknown. The audit file stays until a signed count exists | Business Owner |
| ST-25-05 | A customer contract that names extra duties | Unknown | No customer contract sits in this repository. Working duties stay OB-25-01 to OB-25-12 | Business Owner |

Worked example. A later owner may say ST-25-01 applies. Until that sentence is signed, Half B records `Applicability: Unknown` and keeps the BO-10 handling.

---

## What is out of this list

ROI numbers stay EDUCATIONAL under BO-11. That row belongs to Phase 14. This half does not add an ROI duty.

Brand-asset sign-off stays BO-12. That row belongs to Phase 15.

The as-built baseline sign-off stays BO-13. That row belongs to Phase 16.

This half adds no feature to satisfy an unread statute.

---

## Half B evidence this file names

Engineering decision ED-P12-25A-04, authority: team-force. Check ids start here and continue in the sibling files.

| Check | What Half B records | Honesty when recorded |
|---|---|---|
| HB-25-04 | `Decision_Tracker.md` still shows BO-10 PROPOSED. No signer name appears in `docs/25-governance/` | REAL |
| HB-25-05 | No file in `docs/25-governance/` is named or titled as a compliance certificate | REAL |

### Recorded

Recorded 2026-10-18 under `corr-p12-25b-doc-20261018-001`. Half B did not sign BO-10. Half B did not add a statute row as DECIDED. Statute applicability stays Unknown.

HB-25-04. `Decision_Tracker.md` row BO-10 status is PROPOSED. The notes say the Business Owner accepted on 2026-10-18 and the artifact stays unsigned. Search of `docs/25-governance/*.md` found no `Signed by`, `Signature:`, `I certify`, `certificate of`, or `Attested by` line. Named signer stays Unknown. Honesty: REAL.

HB-25-05. Directory `docs/25-governance/` contains seven markdown files: `accountability-map.md`, `ai-system-register.md`, `compliance-control-matrix.md`, `compliance-obligations.md`, `governance-readiness.md`, `model-card.md`, `system-card.md`. None is named as a certificate. Honesty: REAL.

---

## What this file does not do

This file records working obligations from locked facts. It issues no compliance certificate. It does not write sub-stage 26. It does not invent a signer.

STOP. Do not start sub-stage 26.
