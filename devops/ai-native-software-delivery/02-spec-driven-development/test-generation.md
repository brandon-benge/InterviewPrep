# Test Generation

<a id="validation-coverage-model"></a>
## Validation Coverage Model

Validation is derived from the Spec, not ad hoc testing.

```
Problem + Requirements + Invariants + Architecture
→ required validation categories
→ test artifacts + release gates
```

Every spec change must declare what validation is required across build, release, and production.

<a id="validation-matrix"></a>
### Validation Matrix (Example)

| Validation Category | Driven By | Example Checks | Gate Type |
|---|---|---|---|
| Functional | Requirements | API behavior, workflows, acceptance | pre-merge |
| Correctness | Invariants | duplicates, ordering, stale writes, reconciliation | pre-merge + pre-release |
| Security | Invariants, Security | SAST, dependency scans, secrets, authz | pre-merge + pre-release |
| Performance | Non-Functional, Scaling | latency, throughput, saturation | pre-release |
| A/B / Experiment | Problem, Success Definition | conversion, user behavior, impact deltas | staged release |
| Rollout Safety | Architecture, Observability | canary health, telemetry present, rollback works | release gate |
| DR / Recovery | Failure Handling | backup restore, failover, replay, RTO/RPO | scheduled + release readiness |
| Reliability | Architecture, Observability | restart tolerance, queue lag, dependency degradation | staged release |
| Observability | Architecture, Observability | logs, metrics, traces emitted, alert coverage | pre-release |

A/B tests validate business outcomes, not system correctness.

<a id="validation-where-happens"></a>
### Where Validation Happens

**Build Loop ([Step 4](../01-core-model/ai-native-software-delivery.md#step-4-build-loop))**
- Functional tests
- Invariant/correctness tests
- Security scans
- Basic integration tests

**Human Review ([Step 6](../01-core-model/ai-native-software-delivery.md#step-6-human-review))**
- Validate coverage across required categories
- Ensure no validation gaps vs spec

**Build & Release ([Step 7](../01-core-model/ai-native-software-delivery.md#step-7-build-artifact) - [Step 8](../01-core-model/ai-native-software-delivery.md#step-8-release))**
- Performance qualification
- Rollout readiness (canary, telemetry, rollback)
- Observability validation

**Evaluation ([Step 9](../01-core-model/ai-native-software-delivery.md#step-9-evaluation))**
- A/B experiment results
- Regression detection
- Reliability signals
- Production correctness

<a id="validation-enforcement-pattern"></a>
### Enforcement Pattern

Every spec change must produce a validation obligation table:

This table must be included in:
- PR review bundle ([Step 6](../01-core-model/ai-native-software-delivery.md#step-6-human-review))
- Release readiness checks ([Step 7](../01-core-model/ai-native-software-delivery.md#step-7-build-artifact) - [Step 8](../01-core-model/ai-native-software-delivery.md#step-8-release))

Missing categories must be explicitly marked as:
- Not applicable (with justification)
- Deferred (with release-stage validation defined)

| Spec Area | Required Validation |
|---|---|
| Problem | acceptance / A/B |
| Requirements | functional / integration |
| Invariants | correctness |
| Architecture | integration / rollout |
| Non-Functional | performance |
| Failure / DR | recovery / failover |
| Observability | telemetry / health gating |

If any row is missing validation, the spec is incomplete.

<a id="validation-ownership"></a>
### Validation Ownership

- TestAgent → generates functional and invariant tests
- SecurityAgent → enforces security validation
- RefactorAgent → ensures maintainability and performance signals
- Guardrails → enforce validation gates
- HumanEngineer → validates completeness and correctness of coverage

---
---
