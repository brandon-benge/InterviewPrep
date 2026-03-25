# Consistency Model Template

> Purpose: Make read, write, ordering, and concurrency behavior explicit
> Goal: Prevent hidden assumptions about correctness under distributed or concurrent operation
> Example policy: Any block labeled `Example Only` is illustrative only.

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

### Example Only

### Workflow: `publish experiment`
- Business importance: High; wrong config changes user treatment
- Required guarantee: Strong consistency for publish acknowledgement
- Acceptable staleness: 0 at control plane, under 60 seconds at regional caches
- Failure tolerance: Publish must fail closed if propagation status is unknown

### Workflow: `serve assignment`
- Business importance: High-volume, latency-sensitive
- Required guarantee: Deterministic read from last accepted config snapshot
- Acceptable staleness: Up to 60 seconds if explicitly allowed by policy
- Failure tolerance: Service may use last known good snapshot during control-plane outage

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

### Example Only

### Strong Reads
- Required for: Admin reads immediately after publishing or pausing an experiment
- Source of truth: Control-plane database
- Cost / latency tradeoff: Higher latency is acceptable for admin paths

### Stale-Tolerant Reads
- Allowed for: Assignment runtime config fetches from regional caches
- Maximum staleness: 60 seconds
- How staleness is surfaced: Cache version and age are returned in diagnostics

### Read-Your-Writes
- Required or not: Required
- Scope: Admin who publishes an experiment must see it as active immediately in control-plane reads

### Monotonic Reads
- Required or not: Required
- Scope: A regional evaluator must not observe config version 12 and later regress to version 11

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

### Example Only

### Commit Point
- A publish is committed when the new immutable version is durably stored and marked active in the control-plane store

### Durability
- Required durability guarantee: No acknowledged publish may be lost

### Idempotency
- Idempotency key: `request_id` on admin writes and `assignment_request_id` on exposure writes
- Duplicate write behavior: Return original result without creating a second authoritative record

### Partial Failure Handling
- If downstream work fails after commit: Keep the publish committed and retry cache propagation asynchronously
- If commit is uncertain: Return an error and force caller reconciliation before retry

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

### Example Only

### Per-Entity Ordering
- Required or not: Required
- Ordering key: `tenant_id + experiment_key`
- Enforcement mechanism: Single-writer publish path per experiment

### Cross-Entity Ordering
- Required or not: Not required
- Scope: Between unrelated experiments
- Justification: Independent experiments do not require shared global order

### Version Monotonicity
- Version source: Control-plane version counter
- Conflict behavior: Reject concurrent publish if base version is stale

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

### Example Only

### Concurrency Control
- Strategy: Optimistic concurrency with version checks
- Protected resource: Experiment definition and activation state
- Why this strategy is sufficient: Writes are low volume and conflicts should be explicit

### Duplicate Requests
- Detection mechanism: Request ID persisted with assignment/exposure record
- Resolution behavior: Return original response payload

### Concurrent Updates
- Winner selection: First successful publish against current version wins
- Retry behavior: Loser must re-read latest version and re-apply changes intentionally

---

## 6. Conflict Resolution

Describe what happens when concurrent or replicated state disagrees.

- Conflict types:
- Detection mechanism:
- Resolution rule:
- Whether resolution is automatic or manual:
- Audit requirements:

### Example Only

- Conflict types: Concurrent experiment edits, cache lag, duplicate exposure events
- Detection mechanism: Version mismatch, propagation version skew metrics, idempotency key collision
- Resolution rule: Control-plane version is authoritative; duplicates collapse by key
- Whether resolution is automatic or manual: Mostly automatic, manual for conflicting admin edits
- Audit requirements: Record actor, old version, new version, and resolution path

---

## 7. Replication

Describe how data propagates across replicas, regions, or systems.

- Replication topology:
- Sync vs async:
- Expected lag:
- Lag visibility:
- Reconciliation behavior:
- Failover implications:

### Example Only

- Replication topology: Control-plane primary plus region-local read caches
- Sync vs async: Async to caches, synchronous in primary control-plane store
- Expected lag: Under 60 seconds
- Lag visibility: Exposed via version skew and cache age metrics
- Reconciliation behavior: Cache refresh retries until latest version applied
- Failover implications: Runtime may continue serving last-known-good config during control-plane outage

---

## 8. Explicit Non-Guarantees

State what the system does not guarantee so consumers cannot infer stronger semantics.

- _
- _
- _

### Example Only

- The service does not guarantee globally ordered assignment events across different experiments.
- The service does not guarantee zero-lag analytics ingestion.
- The service does not guarantee instant config propagation to every region.
