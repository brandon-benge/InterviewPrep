# Roles and Agents

This document gives a focused summary of who does what in the AI-native delivery model.

For the full system context, see [AI-Native Software Delivery System](./ai-native-software-delivery.md).

## High-Level Architecture

The [canonical service catalog](../02-spec-driven-development/canonical-service-catalog.md) is the cross-repo map of business capabilities, runtime components, owners, interfaces, and dependency relationships. Agents read it as planning and review context. In this model, the catalog is maintained from approved repo metadata and release artifacts; post-release evaluation informs follow-up work but is not treated as the primary catalog update path.

```mermaid
flowchart TD
    request[Customer or business request]
    pm[Product Manager]
    discovery[AI-assisted discovery]
    lead[Tech Lead / Architect]
    spec[SpecRepo feature branch]
    planner[PlannerAgent]
    coder[CoderAgent]
    test[TestAgent]
    security[SecurityAgent]
    refactor[RefactorAgent]
    guardrails[Guardrails]
    pr[Pull request bundle]
    ci[CI / build tool]
    quality[Quality and policy gates]
    review[Human review]
    merge[Merge]
    artifact[Release artifact]
    rollout[Progressive release]
    eval[EvaluationEngine]
    catalog[Canonical service catalog]
    update[Spec update proposal]

    request -- business intent --> pm
    pm -- discovery questions --> discovery
    discovery -- context and options --> pm
    pm -- scope and success criteria --> lead
    lead -- approved technical direction --> spec
    spec -- governing repo context --> planner

    catalog -- ownership and dependency context --> planner
    planner -- task graph --> coder
    coder -- implementation changes --> test
    coder -- security-relevant changes --> security
    coder -- maintainability candidates --> refactor
    test -- validation results --> guardrails
    security -- risk findings --> guardrails
    refactor -- code quality findings --> guardrails
    guardrails -- violations or gaps --> planner
    guardrails -- passing change set --> pr

    pr -- reviewable change bundle --> ci
    ci -- build, test, and scan results --> quality
    quality -- rejected gate --> planner
    quality -- passing gate evidence --> review
    review -- requested changes --> planner
    review -- approval --> merge

    merge -- accepted source changes --> artifact
    artifact -- deployable version --> rollout
    artifact -- declared component metadata --> catalog
    rollout -- telemetry and release signals --> eval

    eval -- production findings --> update
    update -- proposed spec revisions --> lead
    lead -- approved spec changes --> spec
```

## Human Roles

### Product Manager
- Defines the business problem, target users, scope, and success criteria
- Usually drives `PROBLEM.md`

### Tech Lead or Architect
- Owns technical coherence, constraints, tradeoffs, and system boundaries
- Usually governs `INVARIANTS.md`, `REQUIREMENTS.md`, `DATA_MODEL.md`, `CONSISTENCY.md`, and `ARCHITECTURE.md`

### Engineers
- Refine edge cases, implementation detail, feasibility, and review feedback
- Review artificial-intelligence-generated changes against correctness and risk

## Agent Roles

### PlannerAgent
- Converts the governing specification into tasks, dependencies, and execution order

### CoderAgent
- Produces implementation changes from the spec and plan

### TestAgent
- Generates and runs tests against requirements and invariants

### SecurityAgent
- Checks dependencies, secrets, and policy-sensitive changes

### RefactorAgent
- Improves code structure, maintainability, and sometimes performance

### Guardrails
- Enforces scope boundaries, invariants, and quality gates

### EvaluationEngine
- Interprets release and runtime signals and proposes follow-up improvements

## What a Developer Interacts With Most

In day-to-day work, a developer most often interacts with:

- `PlannerAgent` for task decomposition
- `CoderAgent` for implementation
- `TestAgent` for validation support
- `Guardrails` during review and release gating

`SecurityAgent`, `RefactorAgent`, and `EvaluationEngine` usually act more like specialized reviewers than direct collaborators.

## Accountability Rule

Artificial intelligence can draft, decompose, implement, and summarize.

Humans still own:

- correctness
- tradeoffs
- production risk
- approval for high-impact changes
