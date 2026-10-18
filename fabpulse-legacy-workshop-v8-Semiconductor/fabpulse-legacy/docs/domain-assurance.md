# Domain operational record
System: Semiconductor yield and engineering change. Domain entities include: process_steps, metrology_measurements, engineering_changes, supplier_parts; shared reference records, finance ledger and historical events are in separate file/database estates.

Decision requiring authorized human review: `recipe_release`.
Applicable background concerns: SEMI-style process traceability and product change control. This exercise provides a synthetic training environment, **not** compliance certification.

Business metrics: backlog aging, unsafe action count, reconciliation delay, time to evidence, and unresolved exception rate. Domain safety acceptance requires preserving existing human approval gates, no silent cross-tenant action, and source attribution for each decision.
