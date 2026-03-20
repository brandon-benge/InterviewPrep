# AI-Native Software Delivery System (Built on Spec-Driven Development)

An emerging, spec-centered workflow where humans remain accountable for intent, constraints, correctness, and risk, while AI increasingly assists with planning, implementation, validation, and review. This document reflects common patterns visible in current industry guidance and tooling, not a universal standard.

For a deeper explanation of how this landscape is being defined in practice, see [Spec-Driven Development Landscape](./spec-driven-development-landscape.md).

For the condensed workflow and agent summaries, see [Workflow Loop](./workflow-loop.md) and [Roles and Agents](./roles-and-agents.md).

---

## Common Industry Patterns

These are the patterns most commonly emphasized in current AI-assisted and agentic software delivery guidance:

- **Repo-native context**: agents perform better when they read requirements, architecture notes, instructions, and code directly from the repository rather than from a single prompt.
- **Spec-centered planning**: teams increasingly use written requirements, contracts, design notes, and checklists to guide implementation, review, and testing.
- **Human accountability**: humans still own problem framing, architectural tradeoffs, approvals, and production risk decisions.
- **Automation-heavy validation**: code generation, test generation, static analysis, security scanning, and review preparation are increasingly automated.
- **Continuous feedback**: telemetry, evaluation, and production signals feed future changes, even when the process is not fully "spec-driven."

This is best understood as an emerging direction, not a single industry-wide standard.

---

## Spec-First vs Spec-Driven (Clarification)

### Spec-First Architecture
- Commonly emphasizes defining key interfaces, contracts, data shapes, and boundaries before implementation begins
- Focuses on:
  - APIs and contracts
  - Data models
  - System boundaries
- Primary goal:
  - Reduce ambiguity before coding
- Typical artifacts:
  - ARCHITECTURE.md
  - DATA_MODEL.md
  - API_CONTRACTS.yaml

### Spec-Driven Development (This System)
- Uses written specs, requirements, and constraints as a stronger center of gravity across the lifecycle than traditional ticket-driven delivery
- The spec drives:
  - Planning (PlannerAgent)
  - Implementation (CoderAgent)
  - Testing (TestAgent via invariants and requirements)
    - [Validation Coverage Model](../02-spec-driven-development/test-generation.md#validation-coverage-model)
    - [Where Validation Happens](../02-spec-driven-development/test-generation.md#validation-where-happens)
    - [Validation Ownership](../02-spec-driven-development/test-generation.md#validation-ownership)
  - Release decisions (Guardrails + Human)
  - Evaluation (EvaluationEngine)
  - Iteration (Spec updates from production feedback)
- Primary goal:
  - Ensure the system continuously aligns with intent, constraints, and real-world behavior

### Key Difference

| Dimension | Spec-First Architecture | Spec-Driven Development |
|----------|------------------------|--------------------------|
| Scope | Design phase only | Entire lifecycle |
| Purpose | Define system upfront | Drive system continuously |
| Feedback Loop | Minimal | Continuous (via EvaluationEngine) |
| AI Alignment | Partial | Native |
| Output | Contracts and design | Code, tests, rollout, evaluation, and updates |

### How Systems Uses Both

- **spec-first** thinking by capturing problem framing, requirements, constraints, and architecture before implementation.
- The broader workflow becomes more **spec-centered** or **spec-driven** when those written artifacts also shape planning, review, validation, release decisions, and iteration.
- In practice, many organizations today are somewhere in the middle: more spec-centered than traditional Agile, but not fully spec-driven in every step.

---

## Roles (Human vs AI)

### Humans typically own
- Problem framing and business outcomes
- Constraints, risk tolerance, and success criteria
- Architectural tradeoffs and system boundaries
- Review and approval for high-impact changes
- Production release decisions and escalation paths

### AI commonly assists with
- Planning and task decomposition
- Implementation and refactoring
- Test generation and validation support
- Security and quality scanning
- Review preparation and evaluation summaries

### Common accountability pattern
- Product Manager: usually leads problem framing, scope, and success criteria
- Tech Lead / Architect: usually accountable for technical design quality, constraints, and tradeoffs
- Engineers: usually contribute implementation detail, edge cases, feasibility input, and review feedback

This shared model is more common in practice than a single role authoring the entire specification alone.

---

## SpecRepo (Source of Truth)


SpecRepo:
- **PROBLEM.md** (or PRD/brief): problem statement, users, scope, success metrics
- **REQUIREMENTS.md**: functional + non-functional requirements, acceptance criteria
- **ARCHITECTURE.md**: high-level design, components, interactions, tradeoffs
- **DATA_MODEL.md**: entities, relationships, keys, lifecycle
- **CONSISTENCY.md** (optional): read/write semantics, ordering, concurrency strategy
- **INVARIANTS.md** (increasingly adopted): correctness constraints and safety rules
- **API_CONTRACTS.yaml(___only in api-first systems___)**: interfaces and schemas

> [SpecRepo](../02-spec-driven-development/spec-repo.md) is used by **both humans and AI**. It is continuously updated from production feedback.

---

## End-to-End Workflow

### 1) Intent (Human)
- Product Manager defines business goal, success metrics, constraints.

### 2) Spec (Human-led, AI-assisted)
- Product, tech lead / architect, and engineers collaboratively refine the written problem framing, requirements, and design context.
- Tech leads or architects are commonly accountable for technical coherence, constraints, and tradeoffs, but not necessarily the sole authors of every spec artifact.
- AI can draft, summarize, or expand specifications, but humans review and approve the final design intent.

### 3) Plan (AI)
- **PlannerAgent** creates execution graph from SpecRepo.
- Uses retrieval (docs/code patterns) + memory.
- Output: tasks, dependencies, milestones.

<a id="step-4-build-loop"></a>
### 4) Build Loop (AI, iterative)

| Agent         | Purpose                                                      | Required Attributes                                      | Optional Attributes                          | Signals / Tools (via ToolExecutor)                    |
|---------------|--------------------------------------------------------------|----------------------------------------------------------|----------------------------------------------|------------------------------------------------------|
| CoderAgent    | Generates implementation based on spec and plan              | Problem, Architecture, Requirements, Data Model, Consistency | API Contracts, Non-Functional, Scaling        | Compilers, formatters (Prettier/Black), type checkers (tsc/mypy) |
| TestAgent     | Generates and runs unit, integration, and edge case tests ([validation matrix](../02-spec-driven-development/test-generation.md#validation-matrix)) | Invariants, Requirements                                 | Testing Strategy, Observability               | Unit/integration frameworks (JUnit/PyTest), coverage (JaCoCo/Istanbul) |
| SecurityAgent | Scans dependencies, secrets, and enforces security policies  | Invariants                                               | Security, Architecture (trust boundaries)     | SAST (SonarQube, CodeQL), dependency scan (Snyk, Dependabot), secret scan (gitleaks) |
| RefactorAgent | Optimizes code structure, performance, and maintainability   | Architecture, Data Model                                 | Non-Functional, Scaling                      | Code smell & complexity (SonarQube), linters (ESLint/Checkstyle), profilers |
| Guardrails    | Enforces invariants, policy constraints, and scope boundaries| Invariants, Requirements                                 | Security, Consistency                        | Quality gates (SonarQube thresholds), policy-as-code (OPA/Conftest), lint/type gates |

Loop until all constraints pass. If violations occur, the system iterates.

### 5) PR Artifact (AI)
- AI opens PR with:
  - code + tests
  - security findings
  - diffs
  - reasoning / plan trace
- **PR is the primary human review artifact**

<a id="step-6-human-review"></a>
### 6) Human Review (Critical, automation-assisted)
Automation prepares a review bundle:
- PR Summary: What changed, why, impacted components, and risk areas
- Spec Traceability: Maps changes to Problem, Requirements, Invariants, and Architecture
- Invariant Coverage Check: Ensures invariants have matching validation/tests (see [Enforcement Pattern](../02-spec-driven-development/test-generation.md#validation-enforcement-pattern))
- Risk Scoring: Classifies PR (low / medium / high) based on impact and complexity
- Security & Quality Reports: SAST, dependency scan, secrets, code smells, test results
- Diff Segmentation: Groups changes into functional, refactor, test, and config
- Review Checklist: Contextual checklist derived from spec and invariants
- Suggested Reviewers: Based on ownership, risk, and components touched
Human reviewers (typically engineers and, for higher-risk changes, tech leads or designated owners) review against the bundle:
- Validate correctness, edge cases, risk
- Request changes → back to Build Loop

<a id="step-7-build-artifact"></a>
### 7) Build & Artifact (CI/CD)
- CI builds, tests, and produces deployable artifact (image/binary)
- **Branch = source artifact; build output = deployable artifact**

<a id="step-8-release"></a>
### 8) Release (Hybrid)
- Progressive delivery: **dev → stage → prod**
- AI can manage rollout (canary, traffic shifting, auto-rollback)
- **Human approval** required for elevated environments (e.g., prod)
- **Invariant**: Every release must emit telemetry (logs, metrics, traces)

<a id="step-9-evaluation"></a>
### 9) Evaluation (AI)
- [**EvaluationEngine**](../02-spec-driven-development/deployment-health-checks.md)
- Scores correctness, regressions, reliability, policy adherence
- Stores results and proposes improvements

### 10) Spec Update (AI + Human)
- PlannerAgent proposes backlog/spec updates
- Architect reviews and updates **SpecRepo**
- Next iteration begins from updated context

---

## Continuous Loop

```
Intent → Spec → Plan → Build Loop → PR → Human Review → Build → Release → Evaluate → Update Spec → Repeat
```

---

## Invariants (Always Enforced)

- **Correct Data**: state is valid (exactly-once, atomicity, reconciliation)
- **Correct Order**: updates are sequenced (per-entity ordering, monotonic versions)
- **Safe Retries**: idempotent operations (no duplicate effects)
- **Safe Resources**: rate limits, quotas, admission control
- **Safe Governance**: auth, privacy, auditability

Guardrails, tests, CI, and runtime monitoring must all enforce these.

---

## Artifacts (First-Class)

Agents produce verifiable artifacts, not just code:
- Plans (task graphs)
- PRs (diffs + reasoning)
- Test reports
- Security reports
- Build artifacts (images/binaries)
- Evaluation reports (from production)

---

## Evaluation vs Monitoring

- **Monitoring**: What is happening? (metrics/logs/traces)
- **Evaluation**: Did the system behave **correctly** vs spec/invariants?

Evaluation gates promotions and drives the next iteration.

---

## Key Shift

- Traditional baseline: `Backlog / Tickets → Code → Test → Deploy → Monitor`
- Emerging AI-assisted pattern: `Problem / Spec / Context → Generate → Validate → Review → Deploy → Evaluate → Iterate`

**Humans remain accountable for intent, tradeoffs, and risk; AI increasingly assists with execution, validation, and iteration.**
