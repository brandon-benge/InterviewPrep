# System Requirements Template

> Purpose: Translate the problem definition into concrete system obligations
> Goal: Make functional behavior, quality targets, and acceptance criteria testable
> Example policy: Any block labeled `Example Only` is illustrative only. Replace it before relying on this file.

---

## 1. Functional Requirements

For each requirement, describe:
- Trigger or actor
- Required system behavior
- Expected output or side effect
- Relevant invariant or dependency

Template:

### FR-1: _[short name]_
- Actor:
- Trigger:
- The system must:
- Output / side effect:
- Failure behavior:
- Related invariants:

### FR-2: _[short name]_
- Actor:
- Trigger:
- The system must:
- Output / side effect:
- Failure behavior:
- Related invariants:

### FR-N: _[short name]_
- Actor:
- Trigger:
- The system must:
- Output / side effect:
- Failure behavior:
- Related invariants:

### Example Only

### FR-1: Evaluate assignment
- Actor: Product application backend
- Trigger: Backend calls the assignment API with `tenant_id`, `experiment_key`, and `subject_id`
- The system must: Determine the correct treatment for the subject using the currently active experiment version
- Output / side effect: Return `variant_key`, `experiment_version`, and evaluation metadata
- Failure behavior: If the experiment is unknown or inactive, return a deterministic `not_eligible` result rather than a random fallback
- Related invariants: Tenant isolation, deterministic evaluation, read-your-writes for published configs

### FR-2: Record exposure
- Actor: Assignment service
- Trigger: A successful assignment decision is returned
- The system must: Emit one exposure event for the decision using an idempotency key
- Output / side effect: Exposure event written to the analytics stream
- Failure behavior: If analytics sink is unavailable, queue for retry without changing the assignment result returned to the caller
- Related invariants: Idempotency, auditability, bounded retry

### FR-3: Publish experiment configuration
- Actor: Growth engineer
- Trigger: Engineer promotes a draft experiment to active
- The system must: Validate targeting rules, persist an immutable version, and make it available to the assignment path
- Output / side effect: New version recorded with publish timestamp and actor identity
- Failure behavior: Reject publish if validation fails or required rollout metadata is missing
- Related invariants: Version monotonicity, authorization boundaries, audit immutability

---

## 2. Non-Functional Requirements

Define explicit targets, not adjectives.

### Performance
- p50 latency:
- p95 latency:
- p99 latency:
- Throughput:

### Reliability
- Availability target:
- Durability target:
- Recovery objective (RTO):
- Recovery point objective (RPO):

### Scale
- Expected QPS / events per second:
- Peak multiplier:
- Data volume:
- Tenant count / user count:

### Cost
- Cost guardrail:
- Unit economics target:

### Security / Compliance
- Data classification:
- Regulatory requirements:
- Audit requirements:

### Operability
- Required observability:
- Required manual controls:

### Example Only

### Performance
- p50 latency: 10 ms
- p95 latency: 25 ms
- p99 latency: 50 ms
- Throughput: 40k assignment requests per second

### Reliability
- Availability target: 99.95% monthly for assignment API
- Durability target: published experiment versions are durably persisted before activation
- Recovery objective (RTO): 15 minutes for control plane; 5 minutes for assignment API
- Recovery point objective (RPO): 0 for experiment definitions; under 5 minutes for exposure analytics

### Scale
- Expected QPS / events per second: 12k steady-state assignment QPS
- Peak multiplier: 3x during launches
- Data volume: 2 billion exposure events per month
- Tenant count / user count: 500 tenants

### Cost
- Cost guardrail: fit within current shared platform budget
- Unit economics target: assignment lookup cost under $0.05 per 10k requests

### Security / Compliance
- Data classification: pseudonymous subject IDs, internal experiment metadata
- Regulatory requirements: audit admin actions and support data-region boundaries
- Audit requirements: publish, rollback, and break-glass actions must be logged immutably

### Operability
- Required observability: per-tenant latency, cache staleness, exposure backlog, auth failures
- Required manual controls: experiment pause, global kill switch, tenant-level traffic disable

---

## 3. Acceptance Criteria

Define how we know the system is acceptable for launch or handoff.

### Capability Acceptance
- _[e.g., user can submit request and receive deterministic result]_

### Correctness Acceptance
- _[e.g., duplicate requests do not create duplicate authoritative records]_

### Performance Acceptance
- _[e.g., p99 under X ms at Y load]_

### Safety Acceptance
- _[e.g., unauthorized cross-tenant access is impossible]_

### Operational Acceptance
- _[e.g., failures are visible and actionable within Z minutes]_

### Example Only

### Capability Acceptance
- A caller can request an assignment and receive a valid variant for an active experiment

### Correctness Acceptance
- The same subject and experiment version always return the same assignment outcome

### Performance Acceptance
- p99 stays under 50 ms at 40k RPS in load test

### Safety Acceptance
- Cross-tenant assignment requests are rejected and logged

### Operational Acceptance
- Assignment errors page the on-call engineer within 5 minutes of threshold breach

---

## 4. Out of Scope

Capture requirements that are explicitly not part of this phase.

- _
- _
- _

### Example Only

- Statistical significance computation
- End-user UI rendering logic
- Automated experiment design recommendations

---

## 5. Open Questions

Questions that block precision or should be resolved before implementation:

1. _
2. _
3. _

### Example Only

1. Do we require sticky assignments across experiment republish or only within a version?
2. What is the maximum allowed config staleness in regional caches?
3. Must exposure writes be exactly-once or is at-least-once acceptable with dedup downstream?
