# Systems, contracts and operating constraints

**MESDispatch** publishes RECIPE_CHANGE, METROLOGY_RESULT, YIELD_EXCURSION messages. **PLM-Metrology** supplies competing facts and effective-dated master data. Partner files can be replayed and have schema revisions 1.0, 1.1, 2.0, and unsupported variants.

The business manages ETCH, LITHO, DEPOSITION, CMP; human queues track QUEUED, PROCESSING, HOLD, ENGINEERING_REVIEW, RELEASED. Source timestamps, ingestion timestamps and revision dates are distinct.

Process maps and terminology are not fully agreed across teams. No assumption is made that AI is appropriate for any particular processing step.

Synthetic evidence includes policy exceptions and upstream outages; some records disagree. Historic incidents and operational practice must be cross-checked before proposing changes.
