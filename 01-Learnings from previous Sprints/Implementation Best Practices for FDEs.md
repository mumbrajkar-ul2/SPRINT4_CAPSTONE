*** Implementation Best Practices ***
This consolidated playbook translates the principles and lessons from the FDE sessions into repeatable implementation practices. Apply the guidance proportionately to the use case, risk, scale, and delivery stage, and retain evidence for important decisions and exceptions.

** 5.1 Start with discovery, scope, and measurable outcomes
·       Complete discovery artifacts collaboratively with stakeholders; document the current state, target outcome, users, constraints, dependencies, risks, assumptions, exclusions, and decision owners.

·       Define success criteria before solutioning or evaluation. Make them specific, measurable, and connected to user, operational, and business outcomes.

·       Design for the end-to-end workflow and last-mile adoption rather than an isolated feature or technology demonstration.

·       Use rapid prototypes and vibe coding to learn, but transition to controlled, specification-driven engineering before production.

·       Make unresolved questions and conflicting dates, dependencies, or ownership explicit; do not allow ambiguity to become hidden scope.

** 5.2 Use specifications, decisions, and provenance as the delivery backbone
·       Maintain one authoritative, version-controlled baseline for specifications, prompts, repositories, ground truth, generated artifacts, infrastructure definitions, and release evidence.

·       Keep specifications modular, testable, and current. Carry a shared specification identifier through requirements, design, prompts, code, tests, reviews, deployment, and release records.

·       Use living Architecture Decision Records to capture context, alternatives, decisions, consequences, security and compliance considerations, owners, open items, and review triggers.

·       Preserve provenance for AI-assisted work: source references, assumptions, confidence, prompt and model versions, evaluation results, human decisions, unresolved issues, and exceptions.

·       Update decisions and evidence when technology, models, data, assumptions, controls, or risks change; a prior approval is not a substitute for ongoing validation.

** 5.3 Engineer AI and data solutions for evidence-based quality
·       Select architecture from the use case and access patterns. Treat hybrid RAG as a practical starting point, not a universal answer, and use semantic layers or knowledge graphs where governed meaning and reusable context are needed.

·       Test prebuilt document models before building custom models. Reconcile evidence across documents and systems rather than trusting one source independently.

·       Set field-, feature-, and decision-specific confidence thresholds based on business risk. Compare exact identifiers as text, and route missing, conflicting, or low-confidence evidence to human review.

·       Evaluate retrieval and generation with explicit measures such as recall, precision, faithfulness, and answer relevancy. Maintain an evolving golden set and rerun evaluations after ingestion, model, prompt, or pipeline changes.

·       Test the evaluator as well as the solution; LLM-as-judge can introduce bias. Record model, prompt, dataset, and evaluation versions with results.

·       Keep computed explanation evidence, such as SHAP values, outside the LLM reasoning layer. Use language models only to render grounded explanations, then validate deletion, stability, and consistency before production.

·       Use rules for known patterns, machine learning for unknown patterns, and human authority for high-impact decisions. Screen features for availability at prediction time, bias, and proxy effects.

** 5.4 Design for failure, recovery, and operational ownership
·       Define a failure taxonomy that distinguishes transient, retryable, terminal, business-rule, dependency, and human-approval failures.

·       Build idempotency, bounded retries, timeouts, checkpoints, resumable stages, compensation, fallback behavior, and partial-response rules into the design.

·       Use deterministic idempotency keys and state-transition events to prevent duplicate notifications, records, charges, or payments.

·       Run independent checks in parallel and dependent steps sequentially. Separate interactive and background workloads, and bound concurrency to protect downstream systems.

·       Route terminal failures to a dead-letter queue with primary and secondary owners, retention rules, privacy-safe telemetry, triage targets, replay procedures, and escalation paths.

·       Test recovery deliberately, including duplicate delivery, partial completion, delayed approval, downstream outage, model or service version changes, and replay before retention windows expire.

·       Use mock or fallback modes when lab or non-production dependencies fail so analysis and learning can continue without disguising the limitation.

** 5.5 Embed security, privacy, governance, and auditability
·       Apply security, privacy, governance, and regulatory controls from the MVP onward; treat them as delivery work rather than documentation added at the end.

·       Maintain an inventory of models, data sources, RAG resources, agents, tools, identities, users, actions, and data flows. Classify risk using impact, likelihood, autonomy, data sensitivity, and business criticality.

·       Separate management-plane and data-plane permissions, scope access to the narrowest required resource, and separate identities by function.

·       Prefer managed identity and keyless access. When secrets are unavoidable, use Key Vault, rotation, restricted access, monitoring, and auditable evidence.

·       Classify signing keys and similar credentials as crown-jewel assets; operationalize isolation, authentication, validation, auditing, rotation, and incident response.

·       Record deterministic audit events in application logic, retain a queryable working copy, and use immutable storage for final evidence where required.

·       Resolve legal basis, PII handling, retention, access, approval ownership, and deletion obligations before locking evidence immutably. Use separated audit permissions and tamper-evident techniques where appropriate.

·       Keep humans accountable for high-impact outcomes. Missing or uncertain evidence must trigger review, hold, or stop rather than silent automation.

** 5.6 Measure performance, cost, and business impact together
·       Define realistic non-functional requirements and measure each stage of the workflow. Use P50, P95, and P99 latency rather than averages alone.

·       Quantify volume, token usage, request units, concurrency, queue size, storage, compute, and uncertainty. Compare performance gains with incremental cost instead of assuming optimization is free.

·       Translate technical measures into business consequences, including user wait time, reviewer workload, missed-risk cost, false-positive cost, throughput, and service-level impact.

·       Model Cosmos DB and similar stores from access patterns. Prefer partition-local queries, avoid hot partitions, and use intentional duplication only when the latency, compute, consistency, and RU trade-offs are understood.

·       Select monitoring metrics that drive decisions. Combine leading and lagging indicators, and pair detection with diagnostic context and actionable ownership.

·       Track team and environment consumption, preserve regional and quota assumptions, and avoid deleting resources until required learning and evidence have been captured.

** 5.7 Industrialize delivery and communicate with discipline
·       Use controlled environments, dependency management, environment configuration, and documented deployment details to make builds reproducible.

·       Manage infrastructure through modular, version-controlled Bicep or Terraform. Prevent drift between repository definitions and deployed environments, and apply change control to data-bearing resources.

·       Sequence deployments intentionally: establish observability first, then data services, then compute and application components.

·       Test features, navigation, contracts, edge cases, security controls, failure behavior, recovery paths, models, and service versions before demonstration or release.

·       Use peer challenge and evidence-based reasoning to improve designs. Record why a decision was made, not only the selected option.

·       Capture reusable knowledge in templates, ADRs, prompt libraries, playbooks, runbooks, and shared repositories; keep the method tool-agnostic.

·       Present a concise value story that connects the current state, recommendation, rejected alternatives, priorities, risks, controls, working behavior, evidence, trade-offs, and business impact.

·       Assign explicit ownership across architecture, engineering, domain, security, reliability, performance, commercial analysis, governance, and synthesis; bring in specialists where deeper expertise is required.

5.8 Minimum release-readiness checklist
·       Outcome: Scope, exclusions, users, success measures, and business value are agreed.

·       Design: Specifications and ADRs are current; assumptions, alternatives, owners, and review triggers are visible.

·       Quality: Functional, edge-case, regression, model, retrieval, explainability, and failure-path evaluations meet defined thresholds.

·       Safety: Human authority, hold/stop conditions, bias considerations, privacy, retention, and regulatory obligations are implemented.

·       Security: Least privilege, identity separation, secret or key controls, constrained-access evidence, and auditability are proven.

·       Reliability: Idempotency, retry, timeout, checkpoint, compensation, DLQ, replay, recovery, and ownership are tested.

·       Operations: Observability, leading and lagging indicators, diagnosis, alerts, runbooks, support ownership, and service levels are ready.

·       Economics: Latency, throughput, volume, request units, tokens, storage, queue load, manual-review demand, and uncertainty are quantified.

·       Delivery: Infrastructure, configuration, repositories, prompts, tests, artifacts, and deployed environments are versioned and aligned.

·       Traceability: Evidence links requirements and sources to decisions, code, controls, tests, approvals, releases, residual risks, and unresolved issues.

5.9 September 30 production-hardening additions
·       Map identity and access, secrets and encryption, infrastructure as code, secure CI/CD, observability, performance, and production-readiness validation to the 42-step production spine.

·       Use the production spine to identify unresolved AI-versus-no-AI rationale, concrete capstone evidence, and required readiness gates.

·       Treat the FDE prompt harness as a shared implementation asset only after evaluating it for reuse, governance, and operating ownership.

·       Place human review at key stages of the prompt harness to prevent early errors from propagating into downstream artifacts and decisions.

·       Before release and demonstration, confirm that each readiness gate has objective evidence and an accountable owner.

** 5.10 October 5-6 execution, observability, and incident-response additions
·       Begin the production-delivery spine with a reusable execution contract that defines objectives, boundaries, artifact paths, evidence expectations, assumptions, unknowns, validation rules, and lineage.

·       Complete repository and system orientation, operating-contract definition, and token, latency, infrastructure, cost, and platform-impact assessment before qualification or implementation.

·       Treat prompts as code: version them, review changes, test outputs, use multi-shot follow-ups for gaps, and preserve prompt-to-artifact-to-test traceability.

·       Do not mark a spine stage complete because a document exists; require artifact validation, objective evidence, accountable approval, and readiness to proceed.

·       Propagate a correlation identifier across the complete request path and capture structured logs, metrics, traces, model interactions, tool calls, retrieval activity, errors, latency, and outcome status.

·       Design unified telemetry so application and system signals can be investigated together without losing ownership, security, privacy, and retention boundaries.

·       Define SLOs, SLIs, alert thresholds, incident severity, incident-command roles, escalation paths, evidence-preservation rules, and customer-agreed log-retention periods before production.

·       Use traces and investigation queries to diagnose latency and quality issues across gateways, orchestrators, agents, MCP or external tools, retrieval pipelines, and downstream services.

·       Close incidents with verified preventive actions and compare recovery times for recurring incident classes; lessons learned are complete only when they measurably improve operations.

** 5.11 October 7-16 semantic-layer portability, capstone validation, and Sprint 4 transition additions
·       Sequence transformation before abstraction. Understand and stabilize the brownfield repository first; then capture the transformed business knowledge in a semantic layer, create the PRD and application, and validate the result against repository evidence.

·       Build the semantic layer as a governed product. Keep it model- and application-independent, multi-file, versioned, reviewable, and testable. Use explanatory Markdown, structured YAML for entities, relationships, rules, metrics, taxonomies, and access semantics, schemas or code for validation, consistency tests, and JSON where runtime services require it.

·       Separate portable knowledge from repository-dependent context. Explicitly classify what can transfer across models and applications, what depends on source code or data, and what must be regenerated or revalidated in a new target environment.

·       Test portability iteratively rather than once at the end. Run model or application comparisons as the semantic layer evolves; preserve prompts, configurations, versions, inputs, outputs, validation results, defects, remediation, and residual differences so claims of portability are evidence-based.

·       Use contract and negative-path validation. Apply repository-grounded instructions, representative few-shot examples, schema and contract checks, source controls, and tests for invalid, missing, contradictory, and unauthorized inputs. Distinguish clearly among implemented, proposed, and unavailable capabilities.

·       Keep production readiness independent of demonstration success. A working application or persuasive presentation does not override unresolved data defects, identity, consent, clinical or domain assurance, operational evidence, security controls, or other readiness gaps; retain an explicit NO-GO where evidence is insufficient.

·       Preserve an end-to-end capstone evidence package. Retain the repository baseline, intent and execution plan, prompts, semantic-layer artifacts, PRD, application outputs, tests, model-comparison results, ADRs, controls, approvals, readiness decisions, residual risks, and presentation evidence in a versioned location.

·       Use demonstrations as implementation reviews. Present architecture, semantic/context definitions, transformation decisions, model comparisons, governance controls, negative-path results, cost visibility, trade-offs, residual gaps, and the production decision—not only the successful user journey.

·       Carry Sprint 3 learning into Sprint 4 without losing lineage. Reuse validated templates, playbooks, semantic patterns, tests, controls, and decision records, while tracing Sprint 4 design choices back to source evidence and recording where broader data conditions, moonshots, or team-created designs require new validation.

·       Close the sprint with explicit reinforcement actions. Identify gaps against the production-delivery spine, assign owners and due dates, and prioritize unresolved portability, governance, cost, assurance, and operational-readiness work before treating the approach as reusable.