# Consistency Model Template

> Purpose: Make read, write, ordering, and concurrency behavior explicit
> Goal: Prevent hidden assumptions about correctness under distributed or concurrent operation

---

## 1. Consistency Goals

For each critical workflow, define the required consistency level.

### Workflow: _[name]_
- Business importance:
- Required guarantee:
- Acceptable staleness:
- Failure tolerance:

### Workflow: _[name]_
- Business importance:
- Required guarantee:
- Acceptable staleness:
- Failure tolerance:

---

## 2. Read Semantics

Describe what readers are allowed to observe.

### Strong Reads
- Required for:
- Source of truth:
- Cost / latency tradeoff:

### Stale-Tolerant Reads
- Allowed for:
- Maximum staleness:
- How staleness is surfaced:

### Read-Your-Writes
- Required or not:
- Scope:

### Monotonic Reads
- Required or not:
- Scope:

---

## 3. Write Semantics

Describe when writes are considered committed and what guarantees they provide.

### Commit Point
- A write is committed when:

### Durability
- Required durability guarantee:

### Idempotency
- Idempotency key:
- Duplicate write behavior:

### Partial Failure Handling
- If downstream work fails after commit:
- If commit is uncertain:

---

## 4. Ordering Guarantees

Define where order matters and where it does not.

### Per-Entity Ordering
- Required or not:
- Ordering key:
- Enforcement mechanism:

### Cross-Entity Ordering
- Required or not:
- Scope:
- Justification:

### Version Monotonicity
- Version source:
- Conflict behavior:

---

## 5. Concurrency Strategy

Describe how simultaneous operations are handled.

### Concurrency Control
- Strategy: _[optimistic / pessimistic / single-writer / partitioned ownership / other]_
- Protected resource:
- Why this strategy is sufficient:

### Duplicate Requests
- Detection mechanism:
- Resolution behavior:

### Concurrent Updates
- Winner selection:
- Retry behavior:

---

## 6. Conflict Resolution

Describe what happens when concurrent or replicated state disagrees.

- Conflict types:
- Detection mechanism:
- Resolution rule:
- Whether resolution is automatic or manual:
- Audit requirements:

---

## 7. Replication

Describe how data propagates across replicas, regions, or systems.

- Replication topology:
- Sync vs async:
- Expected lag:
- Lag visibility:
- Reconciliation behavior:
- Failover implications:

---

## 8. Explicit Non-Guarantees

State what the system does not guarantee so consumers cannot infer stronger semantics.

- _
- _
- _
