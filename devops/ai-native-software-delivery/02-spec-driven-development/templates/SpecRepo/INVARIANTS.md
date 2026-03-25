# System Invariants

Senior-level, interview-ready invariants that can be applied across infrastructure, data, and platform systems.

> Example policy: Any block labeled `Example Only` is illustrative only. Humans and agents must not treat the example system as the real invariant set.

---

## Correct Data

### Idempotency
- A request with the same idempotency key must never create more than one authoritative record.
- Idempotent retries must return the original outcome, not a recomputed result.

### Deduplication Window
- Duplicates detected within the deduplication window are collapsed before persistence.
- Duplicates outside the window are treated as new logical events.

### Canonicalization
- Canonicalization must occur before hashing or comparison.
- Canonical forms must be stable across versions.

### Versioning
- Breaking changes require a new versioned interface.
- Old versions must remain supported for a defined deprecation window.

### Audit Immutability
- Audit logs must be append-only.
- Audit records must be tamper-evident and traceable to actors.

### Example Only

For an experiment assignment service, these would mean:
- Replaying the same exposure event must not create a second authoritative assignment record.
- The same `tenant_id`, `experiment_key`, and `subject_id` must canonicalize identically before bucketing.
- Publishing experiment version 13 must never silently mutate version 12.
- Every publish or pause action must remain visible in append-only audit history.

## Correct Order

### Ordering
- Events for a single entity must preserve causal order.
- Cross-entity ordering is explicitly undefined unless stated otherwise.

### Monotonicity
- Progress indicators must never move backward.
- Version numbers must increase monotonically across updates.

### Eventual Consistency Bounds
- Replication lag must be observable and measurable.
- The system must converge without manual intervention.

### Example Only

For the example system:
- Updates to one experiment must preserve publish order for that experiment.
- A regional cache may lag, but it must move from version 12 to 13 and never back to 12.
- Cache lag must be visible in metrics and bounded by policy.

## Safe Retries

### Retry Bounds
- Retry attempts must be capped per request.
- Retry backoff must increase monotonically to avoid synchronized retries.

### At-Least-Once vs Exactly-Once
- Delivery guarantees are explicitly documented and enforced per pipeline.
- Consumers must never assume stronger guarantees than the producer provides.

### Example Only

For the example system:
- Exposure delivery retries must stop after a bounded policy and surface an alert.
- Analytics consumers may receive at-least-once exposure delivery and must deduplicate by idempotency key.

## Safe Resources

### Budget / Quota
- Quota enforcement must occur before work is scheduled or resources are allocated.
- Quota exhaustion must degrade or reject requests deterministically.

### Admission Control
- Admission decisions must be made using current capacity, not queued estimates.
- Once admitted, work must not be revoked due to later admission failures.

### Politeness / Rate Limits
- Per-target rate limits must be enforced independently.
- Rate limiting must adapt to downstream errors and latency signals.

### Example Only

For the example system:
- A single tenant must not consume all assignment runtime capacity during a launch.
- If the exposure sink is saturated, the system should shed or buffer analytics work without destabilizing assignment lookups.

## Safe Governance

### Isolation (Tenant / Priority / Blast Radius)
- Resource exhaustion in one tenant must not affect scheduling fairness of others.
- Failures must be contained to the smallest possible isolation boundary.

### Authorization Boundaries
- Authorization must be evaluated using the caller’s identity, not delegated trust.
- Privilege escalation across services is forbidden.

### Tenant-Scoped Execution Identity
- Guarantee: Any credential, session, token, or execution identity is bound to a single tenant and cannot be used to access resources in another tenant.
- Enforcement & Observability: Every credential MUST include an immutable `tenant_id` claim validated by every service before authorization; authorization decisions MUST be logged (including `actor_id`, `tenant_id`, target tenant, and outcome). Explicit cross-tenant flows require documented, auditable escalation and elevated approval.

### Control-Plane vs Data-Plane Separation
- Control-plane outages must not block ongoing data-plane execution.
- Data-plane operations must not mutate control-plane state directly.

### Fail-Open vs Fail-Closed
- Safety-critical operations must fail closed.
- Non-critical paths may fail open to preserve availability.

### Safety vs Liveness
- Invariant violations must halt progress immediately.
- Recovery paths must eventually restore forward progress.

### Freshness / Staleness
- Reads must declare whether they are strongly consistent or stale-tolerant.
- Stale reads must include metadata indicating last update time.

### Example Only

For the example system:
- A token for `tenant_acme` must never be usable to fetch assignments for `tenant_beta`.
- The assignment runtime may continue serving last-known-good config during control-plane outage, but it may never publish config changes.
- Unauthorized publish actions fail closed; optional analytics fan-out may degrade to preserve assignment availability.
- If the runtime serves stale config, the response and telemetry should expose config age and version.
