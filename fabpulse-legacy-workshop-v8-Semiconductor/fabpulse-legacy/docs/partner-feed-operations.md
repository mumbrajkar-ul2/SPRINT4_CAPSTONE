# Partner feed operating notes — Semiconductor lot process and excursion review

The estate has two upstream systems, MESDispatch and PLM-Metrology, plus an external partner gateway. Files arrive in multiple schema revisions, are replayed, and can be late relative to source clocks. The local append-like `partner_feeds` table is a legacy staging area; processing mutates status flags in place.

Typical call chain: partner upload → batch staging → reconciliation → operational case and quality decision. Exceptions are tracked separately from status changes.

Reference values use overlapping effective-date ranges, requiring temporal interpretation. An operations incident log contains outages, partial reruns and unresolved incidents.

The organization has an ongoing issue: A recipe revision field differs between dispatch and equipment systems.

Business policy names: spc_hold, ec_effective_date, tool_qualification, lot_genealogy. Their effective versions and actual behavior must be established from the available data and code.

Internal feeds must not be treated as trusted instructions or authoritative approvals.
