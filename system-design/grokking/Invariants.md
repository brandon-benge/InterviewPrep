# Reusable System Design Invariants

Senior-level, interview-ready invariants that can be applied across infrastructure, data, and platform systems.

---

## Idempotency
- A request with the same idempotency key must never create more than one authoritative record.
- Idempotent retries must return the original outcome, not a recomputed result.

## Deduplication Window
- Duplicates detected within the deduplication window are collapsed before persistence.
- Duplicates outside the window are treated as new logical events.

## Budget / Quota
- Quota enforcement must occur before work is scheduled or resources are allocated.
- Quota exhaustion must degrade or reject requests deterministically.

## Admission Control
- Admission decisions must be made using current capacity, not queued estimates.
- Once admitted, work must not be revoked due to later admission failures.

## Retry Bounds
- Retry attempts must be capped per request.
- Retry backoff must increase monotonically to avoid synchronized retries.

## At-Least-Once vs Exactly-Once
- Delivery guarantees are explicitly documented and enforced per pipeline.
- Consumers must never assume stronger guarantees than the producer provides.

## Isolation (Tenant / Priority / Blast Radius)
- Resource exhaustion in one tenant must not affect scheduling fairness of others.
- Failures must be contained to the smallest possible isolation boundary.

## Monotonicity
- Progress indicators must never move backward.
- Version numbers must increase monotonically across updates.

## Ordering
- Events for a single entity must preserve causal order.
- Cross-entity ordering is explicitly undefined unless stated otherwise.

## Freshness / Staleness
- Reads must declare whether they are strongly consistent or stale-tolerant.
- Stale reads must include metadata indicating last update time.

## Politeness / Rate Limits
- Per-target rate limits must be enforced independently.
- Rate limiting must adapt to downstream errors and latency signals.

## Fail-Open vs Fail-Closed
- Safety-critical operations must fail closed.
- Non-critical paths may fail open to preserve availability.

## Canonicalization
- Canonicalization must occur before hashing or comparison.
- Canonical forms must be stable across versions.

## Versioning
- Breaking changes require a new versioned interface.
- Old versions must remain supported for a defined deprecation window.

## Authorization Boundaries
- Authorization must be evaluated using the caller’s identity, not delegated trust.
- Privilege escalation across services is forbidden.

## Control-Plane vs Data-Plane Separation
- Control-plane outages must not block ongoing data-plane execution.
- Data-plane operations must not mutate control-plane state directly.

## Eventual Consistency Bounds
- Replication lag must be observable and measurable.
- The system must converge without manual intervention.

## Safety vs Liveness
- Invariant violations must halt progress immediately.
- Recovery paths must eventually restore forward progress.

## Audit Immutability
- Audit logs must be append-only.
- Audit records must be tamper-evident and traceable to actors.