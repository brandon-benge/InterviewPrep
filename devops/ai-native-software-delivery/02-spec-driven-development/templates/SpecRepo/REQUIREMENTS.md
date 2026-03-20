# System Requirements Template

> Purpose: Translate the problem definition into concrete system obligations
> Goal: Make functional behavior, quality targets, and acceptance criteria testable

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

---

## 4. Out of Scope

Capture requirements that are explicitly not part of this phase.

- _
- _
- _

---

## 5. Open Questions

Questions that block precision or should be resolved before implementation:

1. _
2. _
3. _
