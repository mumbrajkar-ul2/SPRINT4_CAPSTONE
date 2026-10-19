# Project intent

## Document navigation


| **Report sections**                                        |
| ---------------------------------------------------------- |
| Executive intent and assignment interpretation             |
| Guideline-to-assignment traceability                       |
| Business and stakeholder context                           |
| Repository evidence and current-state architecture         |
| Data, integrations, business rules, and technical debt     |
| Problem statement and transformation hypotheses            |
| Intended future-state capabilities and architecture        |
| Two-application strategy                                   |
| Context Lake, semantic layer, and knowledge graph          |
| GenAI and agentic engineering boundaries                   |
| Specification, testing, evidence, and traceability         |
| Security, responsible AI, compliance, and governance       |
| Production engineering and cloud readiness                 |
| KPI and experiment framework                               |
| Live demonstration and executive defence                   |
| Delivery phases aligned to the adaptable spine             |
| Risks, assumptions, evidence gaps, and acceptance criteria |
| Recommended immediate actions and evidence index           |




## 1. Executive intent and assignment interpretation

The capstone is an evidence-led modernization exercise over a deliberately production-shaped legacy simulator. The repository is not the target architecture and does not contain a completed AI solution. The assignment is to discover how the system actually behaves, preserve legitimate semiconductor workflows, define measurable baselines, and engineer a defensible transition to two independently functional modern applications.

The core business context is Fabpulse Group’s fab-lot and equipment-exception process. External messages, process and metrology records, policy versions, case workflows, archived documents, cost estimates, and local rule interpretations do not always agree. The intended transformation must therefore improve operational decision quality, traceability, reconciliation, engineering velocity, resilience, and user experience without disguising uncertainty or using GenAI where deterministic engineering is safer.

**Capstone intent statement.** Build and demonstrate a secure, governed, cloud-native semiconductor engineering intelligence capability that converts a fragmented legacy estate into explainable, evidence-backed workflows. The delivery must prove where AI adds differentiated value, where deterministic services remain authoritative, and how both transformed applications improve identical business scenarios under comparable conditions.

**This document distinguishes three evidence states:**

- Observed: capabilities, data, tests, and constraints directly present in the repository.
- Proposed: future-state architecture and transformation choices that must be validated through SDD, experiments, threat modeling, and stakeholder decisions.
- Unresolved: definitions, owners, thresholds, service objectives, regulatory applicability, and 42-stage details that are not fully supplied.

**Evidence note:** *The guidelines require two functional applications, Context Lake engineering, agentic workflows, semantic governance, SDD/TDD, security, production readiness, evidence-based comparison, and a live executive demonstration.*

## 2. Guideline-to-assignment traceability

The guidelines are treated as mandatory outcome constraints, while allowing the sequencing and depth of the 42-stage spine to adapt to the semiconductor use case.


| **Guideline discipline**    | **Fabpulse interpretation**                                                                                                                                                                                                          | **Required proof**                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Adaptable 42-stage spine    | Preserve discovery, baseline, architecture, implementation, validation, and readiness disciplines; tailor ordering to findings.                                                                                                      | Stage outputs, decision log, traceability matrix, evidence index                               |
| Enterprise Context Lake     | Store business rules, domain knowledge, architecture, code intelligence, data relationships, dependencies, and decisions. Each item has a version and links to its evidence. The lake is the input that Application B is built from. | Ingested evidence, metadata, provenance, version history, retrieval evaluation                 |
| Two functional applications | Application A is the legacy fab-exception system, transformed with AI. Application B runs the same fab-exception workflow and is built from the Context Lake. Each app runs without the other.                                       | Working deployments of both apps, the same business scenarios run on both, comparative results |
| Enterprise-grade UI/UX      | Support realistic exception queues, case/lot views, approvals, evidence, status, role experiences, and error states.                                                                                                                 | Usability walkthrough, role tests, exception handling                                          |
| Agentic AI                  | Use bounded planning and tool orchestration only for justified multi-step tasks; retain approval gates.                                                                                                                              | Agent traces, tool policies, approval records, failure tests                                   |
| Knowledge graph             | Link lots, tools, recipes, events, rules, documents, cases, and organizations where a relationship question needs it. Build it only where the use case justifies it.                                                                 | Graph model, graph queries that answer named questions, lineage                                |
| Semantic layer              | Define canonical business entities, standard terms, relationships, and metrics. Map each term across systems. Example: the night batch treats REVIEW as an open case, so the layer records how each system reads "open".             | Semantic contracts, cross-system mappings, schema validation, consistency tests                |
| SDD and TDD                 | Drive implementation from contracts and acceptance criteria, with characterization through end-to-end tests.                                                                                                                         | Specifications, ADRs, test pyramid, CI evidence                                                |
| Security and governance     | Threat-model application, data, APIs, LLM/RAG, agents, tools, and integrations.                                                                                                                                                      | Threat model, controls, audit trail, evaluation and governance records                         |
| Evidence comparison         | Run identical business scenarios and definitions across both applications.                                                                                                                                                           | Accuracy, latency, productivity, reliability, cost and ROI scorecard                           |
| Executive defence           | Tell a concise Problem → Solution → Impact story and show working software.                                                                                                                                                          | 40-minute explanation/demo, 10-minute Q&A, evidence-linked narrative                           |


**Important boundary.** The detailed 42-stage catalogue was not included in the supplied guideline file. This document therefore provides phase-level alignment and explicitly avoids inventing stage names or deliverables.

## 3. Business and stakeholder context



### 3.1 Operating concern and value chain

Fabpulse Group is a fictional multi-region semiconductor organization with inherited operational systems. The operating concern is rising effort and inconsistency in fab-lot and equipment-exception handling. External sources create messages; legacy integration reconciles or imports them; operations users prioritize cases; local systems record decisions; and monthly measures are reviewed.

The process covers ETCH, LITHO, DEPOSITION, and CMP. Human queues include QUEUED, PROCESSING, HOLD, ENGINEERING_REVIEW, and RELEASED. Source timestamps, ingestion timestamps, and rule-effective dates are separate concepts and must not be collapsed.

### 3.2 Stakeholder outcomes


| **Stakeholder**                | **Primary concern**                         | **Capstone outcome**                                                         |
| ------------------------------ | ------------------------------------------- | ---------------------------------------------------------------------------- |
| Fab operations lead            | Throughput, handling time, case quality     | Prioritized queues, explainable evidence, faster and safer resolution        |
| Enterprise application owner   | Uptime, interfaces, release process         | Cloud-operable services, contracts, observability, rollback                  |
| Finance partner                | Case cost and avoidable rework              | Comparable cost definitions and evidenced benefit model                      |
| Risk and security partner      | Authorization, retention, audit evidence    | Identity controls, provenance, approvals, retention and auditability         |
| Integration lead               | Delivery semantics and reconciliation       | Idempotency, replay safety, schema evolution, checkpoints and data contracts |
| Domain quality and engineering | Recipe, metrology, tool and lot correctness | Canonical semantics, temporal rules, lineage and exception evidence          |




### 3.3 Business ambiguity to resolve

- Sites interpret a “closed” case differently.
- Finance and operations reports may use different monthly cut-offs.
- Recipe revision differs between dispatch and equipment systems.
- Rule ownership and effective dates vary; older workflows remain for compatibility.
- Support requests can use case identifiers or semiconductor domain identifiers.
- A disputed incident used manual spreadsheet reconciliation and has no confirmed follow-up owner.



## 4. Repository evidence and current-state architecture

The repository contains 1,590 files and is dominated by synthetic archived data. The executable baseline uses only the Python standard library, can run without internet access, and supports local or Docker Compose execution.


| **Evidence area**     | **Observed implementation**                                                                                     | **Interpretation**                                                            |
| --------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Legacy API            | Threaded Python HTTP server exposing health, cases, metrics, incidents, partner resources and domain resources. | Simple and runnable, but tightly coupled to SQLite and direct queries         |
| Transactional store   | SQLite connection helper, foreign keys, busy timeout, cases/events/messages/cost tables.                        | Useful baseline; not an enterprise cloud data platform                        |
| Source gateway        | Independent HTTP simulator on port 8090 with paginated events and failure simulation.                           | Provides upstream-system boundary and resilience scenarios                    |
| Ingestion bridge      | Checkpoint and inbox tables, required-field checks, parent validation, duplicate handling.                      | Starting point for idempotent integration patterns                            |
| Partner feed workflow | Mutable staging, multiple schemas, replay, validation, duplicate and negative-quantity handling.                | High-value modernization target with temporal and trust issues                |
| Archived estate       | Night batch, Java reconciliation, JavaScript policy consumer, enterprise archive database.                      | Demonstrates duplicated rule interpretations and heterogeneous technical debt |
| Runtime packaging     | Dockerfile and three-service Compose topology: legacy, source gateway, one-shot bridge.                         | Runnable baseline, but not a production platform architecture                 |
| Tests                 | Fifteen unit/characterization tests passed in review execution.                                                 | Useful safety net; coverage is not sufficient proof of production readiness   |




### 4.1 Current-state logical flow

MESDispatch / PLM-Metrology / partner files → source gateway or local staging → ingestion and reconciliation → SQLite cases and semiconductor domain records → synchronous API and operational reports → manual review, local decisions, and month-end reconciliation.

### 4.2 Validated repository evidence


| **Validation item**       | **Observed result**                                                                                           | **Use in capstone**                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Automated tests           | 15 tests passed                                                                                               | Characterization baseline and regression seed       |
| Workshop verification     | Integrity OK; zero foreign-key errors                                                                         | Dataset readiness proof                             |
| Packaged operational data | 125 cases; 145 events; 8,567 partner feeds; 224 policy exceptions; 72 outages; 60 batch runs                  | Scenario population; not production volume evidence |
| Enterprise archive        | 12,500 operational objects plus histories, evidence, tasks, finance, integration, audit and retention records | Context and migration discovery population          |
| Baseline execution        | 89 open cases; 2 urgent cases; mean amount 4,982.61; 6 sites; 0.603 hours per case                            | Reproducible synthetic technical baseline only      |


**Evidence note:** *The README documents a default generator target of 6,000 cases and larger optional workloads. The packaged database reviewed here contains 125 cases. Any benchmark must record the exact seed, population, command, window, denominator, and exclusions.*

## 5. Data, integrations, business rules, and technical debt



### 5.1 Semiconductor data model


| **Entity**                      | **Meaning and key relationships**                                                         |
| ------------------------------- | ----------------------------------------------------------------------------------------- |
| Fab tools                       | Tool family, chamber and recipe revision                                                  |
| Wafer lots                      | Tool-linked lots with wafer count, defects, measured yield and engineering-hold indicator |
| Process steps                   | Lot/tool/recipe step with start and end timestamps                                        |
| Metrology                       | Lot measurements with units and specification bounds                                      |
| Engineering changes             | Tool-family revision transition, effective date and approval state                        |
| Supplier parts                  | Vendor, tool family, lead time and qualification state                                    |
| Cases and events                | Shared exception intake and lifecycle evidence                                            |
| Documents and archives          | Versioned, multilingual and potentially conflicting extracted evidence                    |
| Policy and reference versions   | Effective-dated rules with overlaps and exceptions                                        |
| Costs and financial adjustments | Operational estimates with reporting-window ambiguity                                     |




### 5.2 Observed business-rule implementation

- Closed cases are assigned archive priority even when amount is high.
- Critical severity or amount above 50,000 produces urgent priority.
- High severity or escalated status produces review priority.
- High/critical severity and escalated/reopened status require manual review.
- Partner reconciliation rejects missing identifiers and negative quantities, detects replay duplicates, and mutates processing status.
- A legacy JavaScript consumer applies an archived regional threshold with 5% tolerance, which may conflict with server-side rules.
- The night-shift batch embeds a distinct interpretation that treats REVIEW as open.



### 5.3 Technical-debt themes


| **Theme**             | **Evidence**                                                                      | **Modernization implication**                                               |
| --------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Rule duplication      | Python, batch, Java and JavaScript implementations                                | Externalize and version rules; prove parity before retirement               |
| Temporal ambiguity    | Source, arrival, revision and effective dates differ                              | Adopt bitemporal/temporal semantics and visible conflict handling           |
| Trust ambiguity       | Untrusted notes, conflicting feeds and mixed-confidence documents                 | Enforce provenance, content trust labels and instruction isolation          |
| Tight coupling        | Direct SQL, dynamic table reads and SQLite-specific deployment                    | Introduce explicit domain/service contracts and migration seams             |
| Weak access control   | Audit-shaped data exists, but API authentication/authorization is not implemented | Identity, RBAC/ABAC, tenant/site scope and policy enforcement are mandatory |
| Limited observability | stderr logging and basic health checks                                            | Add structured telemetry, correlation, SLOs, alerts and traces              |
| Manual recovery       | Spreadsheet reconciliation, reruns and disputed ownership                         | Automate safe replay while retaining human exception ownership              |
| Definition drift      | Closed state, cut-offs, region maps and approvals differ                          | Govern canonical semantics and preserve local variants explicitly           |




## 6. Problem statement and transformation hypotheses

**Problem statement.** Fabpulse cannot consistently explain or reconcile semiconductor exception decisions across fragmented feeds, local rules, archived evidence, and heterogeneous legacy components. This increases handling effort, creates queue inflation and reporting disagreements, and weakens auditability and change confidence.

### 6.1 Transformation hypotheses to test


| **Hypothesis**                                                   | **Why it may help**                                                                                           | **Required validation**                                                                    |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Canonical event and semantic model reduces reconciliation effort | Current schemas, identifiers and effective dates conflict                                                     | Replay identical feeds; measure unresolved conflicts and manual touches                    |
| Context Lake improves discovery and change safety                | Rules, code, documents, contracts and decisions are fragmented                                                | Measure retrieval precision, lineage coverage and analyst time                             |
| Context Lake is complete enough to rebuild the workflow          | Application B is built from the lake, so any missing rule, dependency, or decision shows up as a wrong result | Run the same scenarios on both apps; trace each difference to a missing or wrong lake item |
| Evidence-grounded AI assists exception triage                    | Users must interpret multiple contradictory records                                                           | Blind evaluation against expert-labelled scenarios; abstention and citation required       |
| Bounded agents reduce repetitive multi-system work               | Reconciliation spans tools, evidence and approvals                                                            | Compare steps/time/errors; require tool allow-list and approvals                           |
| Cloud-native decomposition improves resilience and delivery      | Legacy server and batch logic are tightly coupled                                                             | Failure injection, recovery, deployment and rollback evidence                              |
| Governed rule service reduces drift                              | Logic is duplicated across languages and reports                                                              | Characterization parity and effective-date tests                                           |
| Role-based experience improves operational quality               | Current API is technical and lacks enterprise workflow UX                                                     | Task completion, error rate and usability testing                                          |


**Evidence note:** *These are testable propositions, not predetermined conclusions. GenAI should be removed from any step where it does not outperform a simpler, safer, or cheaper deterministic approach.*

## 7. Intended future-state capabilities and architecture

The target should use cloud-native principles while remaining cloud-provider-neutral until platform constraints are confirmed. The architecture must separate deterministic operational truth from probabilistic assistance.

### 7.1 Target logical architecture


| **Layer**            | **Intended responsibility**                                                                                                      |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Experience           | Role-based operations dashboard, exception queue, lot/tool timeline, evidence panel, approvals, administration and accessibility |
| API and workflow     | Case/lot services, task orchestration, approval workflow, rule evaluation, notification and reporting contracts                  |
| Integration          | Schema registry, adapters, event ingestion, idempotency, dead-letter handling, replay, reconciliation and source health          |
| Domain               | Canonical lot, tool, recipe, process, metrology, engineering-change, supplier, case and decision models                          |
| Context intelligence | Context Lake, indexing, retrieval, knowledge graph, semantic mappings, provenance and versioning                                 |
| AI services          | Grounded summarization, conflict explanation, assisted triage, controlled planning and evaluation services                       |
| Data platform        | Operational store, event store, analytical lakehouse/warehouse, metadata, retention and backups                                  |
| Platform engineering | Container orchestration, identity, secrets, policy, CI/CD, observability, resilience and cost controls                           |




### 7.2 Modernization strategy

1. Freeze and reproduce the legacy baseline, including seed, dataset, tests, metrics and incident scenarios.
2. Extract seams through characterization tests and stable contracts before changing behavior.
3. Introduce canonical semantics and integration boundaries alongside the legacy system.
4. Strangle high-value workflows incrementally: feed intake, reconciliation, rule evaluation, evidence assembly, case experience and reporting.
5. Run legacy and transformed paths in parallel for defined scenarios; reconcile differences explicitly.
6. Migrate by evidence and rollback readiness, not by code-completion claims.

**Authoritative boundary.** AI-generated summaries, classifications, plans, or recommendations must never silently become source-of-record facts, engineering release decisions, or approvals. Authoritative state changes require deterministic validation and an accountable human or policy-controlled approval.

## 8. Two-application strategy


| **Dimension**            | **Application A — AI-transformed operational application**                                                    | **Application B — Context Lake ported application**                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| How it is built          | Transform the legacy repository with AI-assisted engineering                                                  | Build from the Context Lake and the semantic layer. The build reads the legacy code only through what the lake holds.   |
| Primary purpose          | Modernize the fab exception workflow and operational decision experience                                      | Run the same fab exception workflow, so the lake's content is tested by a working app                                   |
| Core users               | Operations, quality, integration, engineering, risk, application support                                      | The same users as Application A                                                                                         |
| Functional scope         | Exception intake, prioritization, lot/tool evidence, reconciliation, approvals, metrics, agent-assisted tasks | The same workflow as Application A. It also has a context view that shows the lake items behind each rule and decision. |
| AI use                   | Grounded triage, conflict explanation, case summarization, controlled agent workflows                         | The same AI tasks as Application A. Its agents and retrieval read only from the Context Lake.                           |
| Deterministic core       | State machine, rules, calculations, authorization, persistence, validation, workflow transitions              | The same deterministic core, built from the rule versions and contracts stored in the lake                              |
| Independence requirement | Deployable and useful without relying on a static mock of Application B                                       | Deployable and useful without calling Application A at run time                                                         |
| Comparison basis         | Same business scenarios, data definitions and test conditions                                                 | The same business scenarios, data definitions and test conditions as Application A                                      |




### 8.1 Shared contract, separate proof

The two applications may share governed contracts and platform services. The demo must show that each app works without the other. Shared infrastructure must not hide an unfinished user workflow.

Application A shows what AI-assisted transformation of the legacy repository delivers. Application B shows whether the Context Lake holds enough knowledge to build the same workflow. Both apps run the same business scenarios and are measured on the same KPIs: accuracy, latency, productivity, reliability, cost, and ROI.

### 8.2 Why Application B tests the Context Lake

Application B is built from the lake, so its results show what the lake is missing. Example: suppose the lake stores the Python rule "amount above 50,000 means urgent". Suppose it leaves out the JavaScript consumer's regional threshold with 5% tolerance. Then Application B can mark a case urgent where Application A does not. The team then traces that difference to the missing lake item and adds it.

The same pattern ran in Sprint 3 with less input. There a second model built an app from the semantic layer alone. The test was whether the meanings survived the change of model. Sprint 4 needs more than meanings, because Application B must behave like Application A. It needs the rule logic, dependencies, architecture decisions, and evidence as well.

**Guideline reading.** The guidelines name Application B only as the "Context Lake ported application". This document reads it as a working business app. Three guidelines support that reading. Guideline 5 asks both apps for real workflows and exception handling. Guideline 14 compares both apps on identical business scenarios. Guideline 17 asks for a live demo of both apps with agentic execution and human approvals. Confirm this reading with the trainer.

## 9. Context Lake, semantic layer, and knowledge graph

The guidelines list these as three separate requirements. Guideline 3 is the Context Lake. Guideline 7 is knowledge graphs. Guideline 8 is the semantic layer. Each one has its own deliverable and its own tests.


| **Part**        | **What it holds**                                                                                                                                                       | **What it answers**                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Context Lake    | Business rules, domain knowledge, architecture, code intelligence, data relationships, dependencies, and decisions. Each item has a version and a link to its evidence. | What does the business do, how does the code do it, and what evidence supports each answer? |
| Semantic layer  | One canonical name and definition for each entity, term, status, relationship, and metric, plus the mapping of each term to each system                                 | What does a word mean, and how does each system read it?                                    |
| Knowledge graph | Links between lots, tools, recipes, events, rules, documents, cases, and code                                                                                           | Which records connect to which, and what does a change affect?                              |


Worked example. A user asks why case 00000 was marked urgent. The semantic layer defines "urgent" and lists how Python, Java, JavaScript, and the night batch each decide it. The Context Lake holds those four code versions, the policy version in force on the event date, and the test that compares them. The knowledge graph links the case to its lot, its tool, and that policy version.

The guidelines do not say whether the semantic layer and graph sit inside the lake or beside it. Record that choice in an ADR.

### 9.1 Context Lake content model

The lake must cover every kind of content guideline 3 names. Domain knowledge sits under Business. Code intelligence and dependencies sit under Application. Data relationships sit under Data.


| **Context domain**                | **Examples from repository**                                                                                                                                        | **Required metadata**                                    |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Business and domain knowledge     | Stakeholders, workflows, service levels, incidents, historic decisions, semiconductor process knowledge (ETCH, LITHO, DEPOSITION, CMP, metrology, recipe revisions) | Owner, scope, effective date, confidence, status         |
| Application and code intelligence | Python services, batch, Java, JavaScript, containers, tests, and the dependencies between them                                                                      | Component, version, dependency, interface, lifecycle     |
| Data and data relationships       | Schemas, tables, payloads, documents, archives, identifiers, and the keys that join them                                                                            | Source, lineage, classification, quality, retention      |
| Rules                             | Priority, review, replay, thresholds, policy exceptions                                                                                                             | Rule ID, version, effective interval, authority, tests   |
| Architecture                      | Boundaries, contracts, ADRs, deployment and integration topology                                                                                                    | Decision, rationale, alternatives, risk, approval        |
| Evidence                          | Test results, traces, benchmarks, evaluations and approvals                                                                                                         | Scenario, build, timestamp, actor, result, artifact link |




### 9.2 Semantic layer

The semantic layer should establish canonical business entities and metrics while retaining mappings to local terms. Guideline 8 also asks for cross-system mappings. For each term, the layer records how Python, Java, JavaScript, the night batch, and each source system read it. The Sprint 3 format can be reused here: Markdown explains, YAML defines, JSON Schema validates, tests protect, and generated JSON serves. It must define, at minimum, lot, wafer, tool, chamber, recipe revision, process step, metrology sample, excursion, engineering hold, engineering change, case, evidence, decision, policy, source message, replay, duplicate, outage, cost period, and approval.

Metric definitions must include the population, event time, ingestion time, calculation window, exclusions, status interpretation, unit, currency, and owner. “Open case,” “closed,” “handling time,” “yield excursion,” and “hours per case” are not safe until these fields are explicit.

### 9.3 Knowledge graph justification

A knowledge graph is justified for relationship-heavy questions that are difficult to answer reliably with isolated tables or vector retrieval: which lots used a recipe revision, which tools and metrology results support an excursion, which policy version applied at event time, which documents and code implement that policy, and which changes affect a workflow.

**Graph boundary.** Use the graph for explainable relationships, impact analysis, lineage and contextual retrieval—not as a substitute for transactional state, quantitative computation, or authoritative rule execution.

## 10. GenAI and agentic engineering boundaries



### 10.1 Justified GenAI opportunities

- Summarize a case or lot timeline from structured and documentary evidence with citations and conflict flags.
- Explain why sources disagree, including schema version, timestamp, identifier and policy-effective-date differences.
- Assist legacy discovery by connecting code, tests, schemas, documents, incidents and decisions.
- Draft investigation plans, test cases, change-impact notes and operator handoffs for human review.
- Normalize terminology and propose mappings, subject to governed approval.



### 10.2 Tasks that should remain deterministic

- Authorization, tenant/site access, secrets and policy enforcement.
- State transitions, engineering release, hold/release approval and source-of-record writes.
- Numeric KPI calculations, specification-limit comparisons and cost calculations.
- Idempotency, duplicate detection, schema validation and retention enforcement.
- Final reconciliation decisions where contractual rules are explicit.



### 10.3 Bounded agent patterns


| **Agent workflow**            | **Allowed tools**                                                        | **Human control**                                       |
| ----------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------- |
| Exception investigation       | Read-only case, lot, tool, metrology, policy and document retrieval      | Reviewer approves conclusion and any operational action |
| Feed reconciliation assistant | Read feed, compare schemas, retrieve reference data, propose disposition | Operator approves replay, reject or escalation          |
| Change-impact analyst         | Search code/context, map dependencies, propose tests and rollout risks   | Architect/engineer approves plan                        |
| Evidence-pack assembler       | Collect test results, traces, evaluations and decisions                  | Capstone owner validates completeness                   |
| Operational handoff           | Summarize unresolved evidence and create draft work item                 | Named owner accepts assignment                          |


Every agent must have a scoped identity, explicit tool allow-list, bounded iterations and cost, input/output schema, provenance, approval policy, audit trail, retry/cancellation behavior, and tested responses to malicious or untrusted content.

## 11. Specification, testing, evidence, and traceability



### 11.1 Specification-driven development

Implementation should begin from explicit business scenarios, contracts, non-functional requirements, threat assumptions and acceptance criteria. Specifications should include canonical schemas, API/event contracts, workflow states, rule-effective-date behavior, error semantics, role permissions, agent tool policies and measurable SLOs.

### 11.2 Test strategy


| **Test layer**   | **Fabpulse focus**                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |
| Characterization | Freeze current priority, manual-review, feed replay, batch and report behavior before refactoring                  |
| Unit             | Rules, temporal logic, mappings, calculations, validators, redaction and prompt/tool guards                        |
| Contract         | MESDispatch, PLM-Metrology, source gateway, events, APIs, schema versions and Context Lake interfaces              |
| Integration      | Operational store, event ingestion, graph, search, identity, workflow and observability                            |
| Regression       | Legacy-parity scenarios, incident replay and historical policy cases                                               |
| AI evaluation    | Groundedness, citation correctness, conflict detection, abstention, harmful instruction resistance and consistency |
| Agent evaluation | Tool selection, bounded execution, approval enforcement, rollback and partial-failure recovery                     |
| Performance      | Ingestion throughput, API latency, retrieval latency, queue processing and scale tiers                             |
| Resilience       | Timeouts, duplicates, delayed messages, schema mismatch, dependency loss and replay                                |
| End to end       | Problem → evidence → decision → approval → state change → audit → KPI                                              |




### 11.3 Traceability chain

Business problem → scenario → requirement → specification → architecture decision → implementation → test/evaluation → execution evidence → KPI → executive claim.

Critical claims in the final presentation must be navigable back to evidence. A screenshot alone is not sufficient; store the build/version, dataset seed, scenario, input, output, test condition and result.

## 12. Security, responsible AI, compliance, and governance



### 12.1 Threat surfaces


| **Surface**               | **Representative threats**                                                    | **Required control direction**                                                        |
| ------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Application and APIs      | Broken access control, injection, insecure object access, tenant/site leakage | Identity federation, RBAC/ABAC, validation, API gateway, secure defaults              |
| Data and documents        | Sensitive-data exposure, tampering, retention failure, untrusted text         | Classification, encryption, lineage, retention, integrity and trust labels            |
| Integration               | Replay, duplicate, schema downgrade, spoofed source, delayed messages         | Signed identity, idempotency, schema policy, checkpoints, DLQ and reconciliation      |
| LLM/RAG                   | Prompt injection, unsupported output, data leakage, stale context             | Instruction isolation, grounded retrieval, citations, filters, evaluation, abstention |
| Agents and tools          | Excess authority, tool misuse, runaway loops, hidden side effects             | Least privilege, allow-lists, budgets, approvals, immutable traces, cancellation      |
| Supply chain and platform | Vulnerable images, secrets leakage, drift, unreviewed deployment              | Scanning, SBOM, signing, secret vault, policy as code, gated CI/CD                    |
| Operations                | Weak detection, disputed ownership, unsafe recovery                           | SLOs, alerts, runbooks, incident roles, tested backup/restore and rollback            |




### 12.2 Responsible AI requirements

- Disclose AI assistance and distinguish generated interpretation from source facts.
- Require provenance and evidence links for consequential summaries or recommendations.
- Measure groundedness, omission, contradiction handling, abstention and human override.
- Prevent untrusted feed or document text from becoming system instructions.
- Use representative scenarios across sites, languages, schema versions and severities.
- Define data and model governance owners, change approval, monitoring and retirement criteria.

**Evidence note:** *The repository is synthetic and does not establish actual regulatory scope. Applicable semiconductor, privacy, records, cybersecurity, export-control, customer-contract and responsible-AI obligations must be confirmed with qualified owners.*

## 13. Production engineering and cloud readiness


| **Capability**        | **Intent**                                                                                                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Deployment            | Immutable containers, infrastructure as code, environment promotion, signed artifacts and rollback               |
| Scalability           | Stateless service scaling, partitioned ingestion, queue back-pressure and performance-tested storage             |
| Resilience            | Timeouts, retries with jitter, circuit breaking, idempotency, DLQ, replay and dependency isolation               |
| Observability         | Structured logs, metrics, distributed traces, correlation IDs, business events and agent traces                  |
| SLOs                  | Availability, latency, ingestion freshness, reconciliation completion, retrieval quality and approval turnaround |
| Data operations       | Backup/restore, schema migration, lineage, quality checks, retention, archival and disaster recovery             |
| Security operations   | Central identity, secrets, key rotation, vulnerability management, detection and incident response               |
| FinOps                | Cost allocation for compute, storage, search, graph, model inference and data movement                           |
| Release engineering   | Feature flags, canary/blue-green, contract compatibility, automated evidence and release gates                   |
| Operational readiness | Runbooks, ownership, on-call model, support handoffs, failure rehearsals and capacity plan                       |


**Cloud-native does not mean cloud-only.** The design should support reliable local development and test execution while using managed cloud capabilities where they improve security, resilience, scalability or operating cost. Provider-specific choices require platform, data-residency, identity, procurement and skill constraints that were not supplied.

## 14. KPI and experiment framework

The evidence comparison must run the same scenarios with the same definitions and comparable test conditions. Baseline and transformed measurements must identify dataset seed, population, time window, denominator, exclusions, hardware/runtime, build, model configuration and confidence interval where relevant.


| **KPI family**           | **Candidate measures**                                                                           | **Evidence rule**                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| Business outcome         | Exception resolution cycle time, aged backlog, first-pass resolution, rework, release delay      | Use agreed business definition and scenario population            |
| Decision quality         | Correct disposition, conflict detection, evidence completeness, expert agreement                 | Labelled benchmark and reviewer rubric                            |
| Engineering productivity | Discovery time, change lead time, tests generated/accepted, regression escape rate               | Separate AI assistance from conventional automation               |
| Performance              | API latency, ingestion throughput, retrieval latency, agent completion time                      | Report percentiles and load conditions                            |
| Reliability              | Availability, failure recovery, duplicate rate, replay correctness, unresolved reconciliation    | Failure-injection and operational traces                          |
| AI quality               | Groundedness, citation correctness, abstention, hallucination, tool success, approval compliance | Versioned evaluation suite and thresholds                         |
| Cost                     | Infrastructure, storage, inference, support effort, cost per resolved scenario                   | Use comparable volume and explicit allocation                     |
| ROI                      | Avoided effort or delay minus recurring and transformation cost                                  | Treat synthetic results as modeled evidence, not realized benefit |




### 14.1 Baseline already available

A reproducible review execution produced 125 records, 89 open cases, 2 urgent cases, mean amount 4,982.61, 6 sites, and 0.603 hours per case. These values demonstrate measurement mechanics; they do not establish customer economics or a future-state target.

**No invented targets.** Targets such as percentage reduction, ROI, accuracy or latency must be approved or experimentally derived. This intent document deliberately leaves them open rather than manufacturing success criteria.

## 15. Live demonstration and executive defence



### 15.1 Recommended 40-minute flow


| **Time**  | **Narrative and demonstration**                                                                                                                               |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0–4 min   | Business problem, operational consequences and why the current evidence is difficult to reconcile                                                             |
| 4–8 min   | Legacy complexity: systems, data conflicts, duplicated rules, incidents and baseline                                                                          |
| 8–13 min  | Transformation architecture, two applications and GenAI-versus-deterministic boundaries                                                                       |
| 13–25 min | Live Application A: intake/replay, conflict detection, exception investigation, human approval and state/audit evidence                                       |
| 25–32 min | Live Application B: run the same scenarios on the app built from the Context Lake, then open its context view to trace one rule from document to code to test |
| 32–36 min | Before/after scorecard under identical scenarios, including failures and cost                                                                                 |
| 36–39 min | Security, governance, resilience, rollback and production readiness evidence                                                                                  |
| 39–40 min | Four or five lessons learned and explicit next decision                                                                                                       |




### 15.2 Mandatory demonstration scenarios

1. Replayed MESDispatch delivery inflates the queue; system detects duplicate/replay semantics and explains the evidence.
2. Recipe revision differs between dispatch and equipment/PLM evidence; system shows temporal provenance and routes for approval.
3. Late metrology or backfilled event changes the case timeline; system distinguishes event time from arrival time.
4. Policy versions overlap; system identifies ambiguity, abstains from autonomous action and requests accountable approval.
5. Upstream outage or schema mismatch occurs; system demonstrates retry, DLQ/recovery, observability and user-visible status.
6. Context Lake traces a business rule from historical decision and code to specification, test and transformed implementation.
7. Application A and Application B run scenarios 7 to 11 with the same inputs. The team shows where the results match. Each difference is traced to a missing or wrong Context Lake item.

Scenarios 7 to 11 run on both applications, because guideline 17 asks for a live demo of both working apps.

### 15.3 Executive defence topics

- Why GenAI is necessary for selected evidence synthesis and discovery tasks.
- Why deterministic rules and approvals remain authoritative.
- How security and prompt/tool threats are controlled.
- How KPI definitions avoid misleading comparisons.
- How migration and rollback protect operational continuity.
- What remains unproven and what evidence would change the recommendation.



## 16. Delivery phases aligned to the adaptable spine

Because the detailed 42 stages were not supplied, the following phases preserve the guideline disciplines without fabricating stage names.


| **Phase**               | **Primary outcomes**                                                                                                    | **Exit evidence**                                                                        |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1. Frame and govern     | Problem, stakeholders, scope, safety boundary, decision rights, evidence plan                                           | Approved charter and source register                                                     |
| 2. Reproduce baseline   | Environment, data seed, tests, metrics, incidents and current topology                                                  | Repeatable baseline pack                                                                 |
| 3. Discover context     | Code, rules, data, documents, integrations, workflows and ownership                                                     | Context Lake v1 and discovery findings                                                   |
| 4. Define semantics     | Canonical entities, metric definitions, mappings, temporal model and graph scope                                        | Semantic contracts and quality rules                                                     |
| 5. Specify target       | Scenarios, NFRs, APIs/events, agent boundaries, threat model and acceptance criteria                                    | SDD package and ADRs                                                                     |
| 6. Build foundations    | Cloud platform, identity, CI/CD, observability, operational data and integration seams                                  | Deployable platform baseline                                                             |
| 7. Build Application A  | Operational workflow, UX, deterministic services and bounded AI assistance                                              | Functional transformed application                                                       |
| 8. Build Application B  | The fab exception workflow built from the Context Lake and semantic layer, plus a context view for evidence and lineage | Functional Context Lake ported application that runs the same scenarios as Application A |
| 9. Verify and compare   | TDD, AI/agent evaluation, performance, resilience, security and scenario comparison                                     | Evidence scorecard and defect closure                                                    |
| 10. Rehearse and defend | End-to-end demo, executive story, Q&A, lessons and next-step decision                                                   | Timed rehearsal and evidence-linked deck                                                 |


Prompts, tools, retrieval strategies and stage depth should change when evidence exposes domain complexity, source conflicts, technical constraints or business risk. Adaptation must be recorded as a decision, not performed invisibly.

## 17. Risks, assumptions, evidence gaps, and acceptance criteria



### 17.1 Material risks and mitigations


| **Risk**                    | **Consequence**                                  | **Mitigation intent**                                                 |
| --------------------------- | ------------------------------------------------ | --------------------------------------------------------------------- |
| AI force-fit                | Complexity, cost or unsafe recommendations       | Require deterministic comparator and removal criterion                |
| Definition drift            | Misleading KPI and workflow comparison           | Govern semantic definitions before measurement                        |
| Legacy parity error         | Valid behavior lost during modernization         | Characterization tests, shadow runs and discrepancy review            |
| Replay and temporal defects | Duplicate queues or incorrect decision context   | Idempotency, event/arrival/effective-time model and scenario tests    |
| Untrusted content           | Prompt/tool manipulation or false evidence       | Trust labels, instruction isolation, retrieval controls and approvals |
| Insufficient access control | Data or action exposure across roles/sites       | Federated identity, least privilege and policy tests                  |
| Demo-only engineering       | Working happy path without operational readiness | Failure demos, runbooks, telemetry, recovery and rollback evidence    |
| Synthetic-value overclaim   | Unsupported financial or production claim        | Label synthetic evidence and keep benefit model assumptions explicit  |




### 17.2 Assumptions

- The repository is the authoritative current-state training baseline for this assignment.
- All included people, company, operational and financial records are synthetic.
- The two applications may share contracts and platform services but must be demonstrably functional independently.
- Application B runs the same fab exception workflow as Application A and is built from the Context Lake. This reading comes from guidelines 4, 5, 14, and 17. It needs trainer confirmation.
- A cloud platform, identity provider, approved model provider and compliance scope will be selected later.



### 17.3 Evidence gaps requiring closure

- Detailed 42-stage spine and any mandatory stage artifact templates.
- Official Birlasoft brand assets and presentation template.
- Approved cloud/provider constraints, target environment and cost guardrails.
- Authoritative owners and definitions for states, rules, KPIs, cut-offs and approvals.
- Target SLOs, scale profile, data classification, retention and regulatory applicability.
- Approved model, evaluation thresholds and responsible-AI governance process.



### 17.4 Capstone acceptance criteria

- Both applications deploy and execute independently with enterprise-grade workflows and exception handling.
- Identical scenarios and definitions are executed against baseline and transformed solutions.
- Every material claim is supported by a test, trace, evaluation, benchmark or live function.
- GenAI contribution is isolated from conventional modernization contribution.
- Agents are bounded, auditable and subject to human approvals for consequential actions.
- Security, threat modeling, governance, observability, resilience and rollback are demonstrated.
- The Context Lake is versioned, evidence-backed, searchable, traceable and portable.
- Application B is built from the Context Lake and runs the same business scenarios as Application A. Each difference in results is traced to a lake item.
- The semantic layer is a separate governed deliverable with canonical entities, terms, relationships, metrics, and cross-system mappings.
- A knowledge graph is built where a named relationship question needs it, and each graph use states that question.
- The final presentation fits 40 minutes plus 10 minutes Q&A and ends with 4–5 substantive lessons.



## 18. Recommended immediate actions and evidence index



### 18.1 Immediate actions

1. Obtain the detailed 42-stage spine, official capstone artifact expectations and approved Birlasoft presentation assets.
2. Create a clean immutable copy of the packaged baseline; record hashes, seed, commands and environment.
3. Agree the first three executive business scenarios and their KPI definitions before selecting AI features.
4. Build the source/evidence register and ingest repository artifacts into Context Lake v1.
5. Create characterization tests for duplicated rules, temporal semantics, replay behavior and month-end reporting.
6. Define canonical semiconductor entities, identifiers, statuses and effective-time rules.
7. Draft target contracts, threat model, agent tool policies and human-approval matrix.
8. Select cloud and AI platform options using security, operability, portability and cost evidence.
9. Implement one vertical slice end to end, including failure handling, observability, evaluation and rollback.
10. Establish the evidence scorecard and update it continuously rather than at presentation time.



### 18.2 Repository evidence index


| **Evidence group**          | **Representative artifacts**                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Orientation                 | README.md, PRELOADED_DATA.md, DATA_READINESS.md, domain.json, domain-profile.json                                         |
| Business and history        | docs/business-context.md, legacy-operations-history.md, historic-decisions.md, correspondence and incident records        |
| Architecture and interfaces | docs/source-system-landscape.md, service-boundaries.md, interface-notes.md, source-gateway.md, compose.yaml               |
| Data and semantics          | docs/data-dictionary.md, domain-contracts.md, source-systems-and-constraints.md, SQLite databases and JSON/JSONL archives |
| Implementation              | app/, services/source_gateway/, legacy_batch/, legacy_java/, legacy_js/                                                   |
| Testing and verification    | tests/, scripts/verify.sh, app/workshop_check.py, operations/baseline-evidence.md                                         |
| Operations                  | operations/runbook.md, upstream outage data, batch runs and integration attempts                                          |
| Contracts                   | integration/source-contract-v1.json, source-gateway.json, contracts/decision-policies-archive.json                        |


**Final interpretation.** The strongest capstone will not be the one with the most AI components. It will be the one that most clearly proves how a governed combination of modern cloud engineering, explicit semantics, evidence-backed context, carefully bounded AI, human accountability, and measurable experiments improves this legacy semiconductor workflow.