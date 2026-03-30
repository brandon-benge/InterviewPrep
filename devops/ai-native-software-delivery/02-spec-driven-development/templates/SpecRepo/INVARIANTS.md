# System Invariants

Senior-level, interview-ready invariants that can be applied across infrastructure, data, and platform systems.

---

## Invariant Completeness Framework

Every invariant in this document must be evaluated against the following completeness checklist. These are not invariants themselves, but validation lenses to ensure each invariant is unambiguous, enforceable, and production-safe.

**Example:** ___For any [object] at [scope], exactly/at-most/never [hard rule over time], otherwise [fail-closed or ignore/reject behavior].___

### Required Questions

1. **What object is this about?**  
   Anchor the invariant to a concrete entity (e.g., `event_id`, `user_id`, `AuthoritativeDecisionRecord`).  
   → This defines *what is being protected*.

2. **At what scope does it hold?**  
   Define the consistency boundary (per request, per entity, per tenant, regional, global).  
   → This defines *where the invariant must always be true*.


3. **What must never be violated? (Hard Rule)**  
   Define the core truth constraint. This must be binary, non-negotiable, and falsifiable.  
   → This is the **center of the invariant**—everything else supports this rule.

   **Recommended Hard Rule Language (Use Strong, Falsifiable Verbs):**

   - **Absolute Prohibition:** must never / may never / is forbidden to / is not permitted to  
   - **Integrity / Correctness:** must not produce / must not result in / must not allow / must not expose / must not violate  
   - **Boundary / Safety:** must not cross / must remain within / must be confined to / must be isolated from  
   - **Identity / Uniqueness:** must not create duplicates / must not result in multiple / must map to exactly one / must uniquely identify  
   - **Ordering / Temporal:** must not regress / must not move backward / must not reorder / must not overwrite newer state  
   - **Audit / Immutability:** must not be mutated / must not be deleted / must remain immutable / must not be rewritten

4. **How many are allowed? (Cardinality)**  
   Explicitly define quantity constraints (exactly one, at most one, many but unique, etc.).  
   → This sharpens the hard rule into something enforceable.

5. **What happens over time? (Temporal Behavior)**  
   Define how the invariant evolves (immutability, monotonicity, ordering, version progression).  
   → This ensures the hard rule holds under retries, reordering, and updates.

6. **What happens when things break? (Failure Semantics)**  
   Define system behavior under violation risk (reject, ignore, fail closed, retry, degrade).  
   → This is the **handoff from rule → enforcement behavior**.

7. **How is it enforced?**  
   Define how the invariant is guaranteed by the system, but do not encode implementation details into the invariant itself.  
   → This separates **truth (the invariant)** from **mechanism (the design)**.

   **Important Nuance:**
   - Enforcement is **external to the invariant**
   - It belongs in:
     - architecture
     - data model
     - mechanisms (validation, constraints, coordination)

### Director-Level Extension

8. **What tradeoff does this invariant force?**  
   Every invariant has a cost (latency, availability, complexity, or financial). This must be understood and intentionally accepted.

> Any invariant that cannot be clearly answered across these dimensions is considered incomplete and unsafe for production use.

---


> **Template Notice:** All sections below are illustrative examples intended for both humans and agents to follow as a pattern. They are not the authoritative invariants for any specific system and must be adapted to the target system context **using the completeness framework above**.

### Format Convention (Agent & Human)

All examples below follow a strict two-part structure:

- **Invariant:** A single, technology-agnostic sentence describing what must never be violated.
- **Enforcement:** A separate sentence describing how the system guarantees the invariant.

Rules:
- Do not include implementation details in the invariant.
- Do not omit enforcement; every invariant must be provably enforceable.
- Prefer hard-rule language (e.g., "must never", "must not").
- Keep invariants single-sentence and falsifiable.

---

## Correct Data

### Idempotency
- **Invariant:** A request with the same idempotency key must never create more than one authoritative record.  
  **Enforcement:** Duplicate submissions are rejected or resolved to the original outcome at the persistence boundary using idempotency key validation.
- **Invariant:** Idempotent retries must return the original outcome and must not recompute results.  
  **Enforcement:** Responses are cached and keyed by idempotency key to ensure consistent replay of prior results.

### Deduplication Window
- **Invariant:** Events within the deduplication window must not result in multiple persisted records for the same identity.  
  **Enforcement:** Duplicate identities within the window are detected and collapsed before persistence.
- **Invariant:** Events outside the deduplication window may be treated as new logical events.  
  **Enforcement:** Deduplication logic is bounded by a time or sequence window after which events are accepted as new.

### Canonicalization
- **Invariant:** Inputs must be canonicalized before any hashing or comparison is performed.  
  **Enforcement:** A canonicalization step is applied at ingestion prior to identity derivation or comparison.
- **Invariant:** Canonical representations must remain stable across versions.  
  **Enforcement:** Versioned canonicalization rules ensure consistent transformation across system upgrades.

### Versioning
- **Invariant:** Breaking changes must not be introduced without a new versioned interface.  
  **Enforcement:** Version checks at API boundaries reject incompatible requests.
- **Invariant:** Deprecated versions must remain supported for a defined window.  
  **Enforcement:** Version lifecycle policies enforce compatibility until deprecation deadlines are reached.

### Audit Immutability
- **Invariant:** Audit logs must never be mutated or deleted once written.  
  **Enforcement:** Append-only storage and write-once semantics prevent modification or deletion.
- **Invariant:** Audit records must remain traceable to actors and actions.  
  **Enforcement:** All records include immutable metadata linking actors, actions, and timestamps.

### Correct Order

### Ordering
- **Invariant:** Events for a single entity must not be applied out of causal order.  
  **Enforcement:** Sequence or version checks reject out-of-order updates.
- **Invariant:** Cross-entity ordering must not be assumed unless explicitly defined.  
  **Enforcement:** System design avoids global ordering guarantees unless explicitly enforced.

### Monotonicity
- **Invariant:** Progress indicators must never move backward.  
  **Enforcement:** Updates with lower versions or states are rejected or ignored.
- **Invariant:** Version numbers must strictly increase across updates.  
  **Enforcement:** Version validation ensures only increasing values are accepted.

### Eventual Consistency Bounds
- **Invariant:** Replicated state must converge without manual intervention.  
  **Enforcement:** Reconciliation processes ensure eventual convergence.
- **Invariant:** Replication lag must be observable and bounded.  
  **Enforcement:** Metrics and alerts track and enforce acceptable lag thresholds.

## Safe Retries

### Retry Bounds
- **Invariant:** Retry attempts must not exceed a defined limit per request.  
  **Enforcement:** Retry counters enforce caps at the request boundary.
- **Invariant:** Retry backoff must increase to prevent synchronized retries.  
  **Enforcement:** Backoff policies enforce increasing delay between retries.

### At-Least-Once vs Exactly-Once
- **Invariant:** Consumers must not assume stronger delivery guarantees than provided.  
  **Enforcement:** Contracts explicitly define delivery semantics and consumers validate assumptions.
- **Invariant:** Delivery guarantees must be consistently enforced per pipeline.  
  **Enforcement:** Pipeline configurations define and enforce delivery behavior.

## Safe Resources

### Budget / Quota
- **Invariant:** Work must not be admitted if it exceeds available quota.  
  **Enforcement:** Admission control enforces quota checks before scheduling.
- **Invariant:** Quota exhaustion must deterministically reject or degrade requests.  
  **Enforcement:** Resource checks trigger rejection or controlled degradation paths.

### Admission Control
- **Invariant:** Admission decisions must be based on current capacity.  
  **Enforcement:** Real-time capacity checks gate admission decisions.
- **Invariant:** Admitted work must not be revoked due to later admission failures.  
  **Enforcement:** Execution isolation ensures admitted work continues independently.

### Politeness / Rate Limits
- **Invariant:** Requests must not exceed defined rate limits per target.  
  **Enforcement:** Rate limiting mechanisms enforce per-target quotas.
- **Invariant:** Rate limits must adapt to downstream signals.  
  **Enforcement:** Feedback loops adjust limits based on latency and error rates.

## Safe Governance

### Isolation (Tenant / Priority / Blast Radius)
- **Invariant:** Resource exhaustion in one tenant must not affect others.  
  **Enforcement:** Resource quotas and isolation boundaries prevent cross-tenant impact.
- **Invariant:** Failures must remain confined within defined isolation boundaries.  
  **Enforcement:** Fault containment mechanisms isolate failures per tenant or domain.

### Authorization Boundaries
- **Invariant:** Requests must not access resources outside their authorization scope.  
  **Enforcement:** Authorization checks validate identity against resource ownership.
- **Invariant:** Privilege escalation across services must never occur.  
  **Enforcement:** Identity propagation and validation prevent unauthorized privilege elevation.

### Tenant-Scoped Execution Identity
- **Invariant:** An execution identity must never access or mutate resources outside its associated tenant boundary.  
  **Enforcement:** Every request is validated at the resource boundary using the tenant identity bound to the credential, and cross-tenant access is rejected unless explicitly authorized through auditable and controlled escalation paths.

### Control-Plane vs Data-Plane Separation
- **Invariant:** Control-plane failures must not block data-plane execution.  
  **Enforcement:** Data-plane operates independently of control-plane availability.
- **Invariant:** Data-plane operations must not mutate control-plane state.  
  **Enforcement:** Strict separation of responsibilities prevents unauthorized mutations.

### Fail-Open vs Fail-Closed
- **Invariant:** Safety-critical operations must not proceed under uncertainty.  
  **Enforcement:** Fail-closed logic rejects requests when validation cannot be guaranteed.
- **Invariant:** Non-critical operations may proceed under degraded conditions.  
  **Enforcement:** Fail-open paths allow continued operation with reduced guarantees.

### Safety vs Liveness
- **Invariant:** Invariant violations must halt unsafe progress.  
  **Enforcement:** Detection mechanisms stop execution upon violation.
- **Invariant:** Systems must eventually restore forward progress.  
  **Enforcement:** Recovery workflows re-enable progress after failure.

### Freshness / Staleness
- **Invariant:** Reads must not misrepresent their consistency guarantees.  
  **Enforcement:** Responses include metadata indicating freshness level.
- **Invariant:** Stale reads must disclose their staleness.  
  **Enforcement:** Version or timestamp metadata is attached to responses.
