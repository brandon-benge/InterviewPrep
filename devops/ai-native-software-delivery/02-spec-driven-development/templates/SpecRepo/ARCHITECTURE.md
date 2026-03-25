# Architecture Template

> Purpose: Describe the major system components and how they satisfy the spec
> Goal: Make boundaries, interactions, and tradeoffs reviewable before implementation
> Example policy: Any block labeled `Example Only` is illustrative only.

---

## 1. Overview

**System statement:** _[one paragraph describing what the system is, who uses it, and what it must guarantee]_

### Primary Design Drivers
- _[e.g., low latency, tenant isolation, auditability, cost efficiency]_

### Architecture Style
- _[e.g., request/response service, event-driven pipeline, control plane + workers, batch + streaming hybrid]_

### Example Only

**System statement:** The system is a tenant-scoped experiment assignment platform used by product backends and growth engineers. It must publish experiment configs safely, serve low-latency deterministic assignments, and emit exposure events without violating tenant boundaries.

### Primary Design Drivers
- Low-latency runtime evaluation
- Strong admin-path correctness
- Tenant isolation
- Auditability of publish actions

### Architecture Style
- Control plane + low-latency data plane

---

## 2. Components

List the major parts of the system and their responsibilities.

### Component: _[name]_
- Responsibility:
- Inputs:
- Outputs:
- State owned:
- Failure impact:

### Component: _[name]_
- Responsibility:
- Inputs:
- Outputs:
- State owned:
- Failure impact:

### Component: _[name]_
- Responsibility:
- Inputs:
- Outputs:
- State owned:
- Failure impact:

### Example Only

### Component: `Experiment Control API`
- Responsibility: Create, validate, publish, pause, and archive experiments
- Inputs: Admin requests
- Outputs: Versioned experiment configs and audit events
- State owned: Authoritative experiment definitions
- Failure impact: Admin changes are blocked, but existing assignment traffic may continue

### Component: `Assignment Runtime`
- Responsibility: Evaluate subject context against the active experiment config
- Inputs: Assignment API requests and cached config snapshots
- Outputs: Variant decisions and exposure events
- State owned: Regional config cache only
- Failure impact: User-facing latency or stale assignment decisions

### Component: `Exposure Pipeline`
- Responsibility: Persist and deliver exposure events to analytics systems
- Inputs: Exposure events from assignment runtime
- Outputs: Durable analytics-ready records
- State owned: Buffered event stream and delivery offsets
- Failure impact: Analytics lag, but not assignment correctness

---

## 3. Interaction Flow

Describe the end-to-end request or event path.

### Primary Flow
1. _
2. _
3. _
4. _

### Alternate / Failure Flow
1. _
2. _
3. _

### Example Only

### Primary Flow
1. Growth engineer publishes an experiment through the control API.
2. The control plane stores an immutable version and emits cache refresh metadata.
3. The assignment runtime receives a subject lookup request and evaluates against the latest local snapshot.
4. The runtime returns the assigned variant and emits an exposure event.

### Alternate / Failure Flow
1. Control-plane propagation is delayed.
2. Runtime serves from the last-known-good version within the allowed staleness bound.
3. Operators are alerted if cache age exceeds policy.

---

## 4. Trust Boundaries

Define where identity, authorization, and data sensitivity boundaries exist.

### External Boundary
- External actors:
- Entry points:
- Authentication mechanism:

### Internal Boundary
- Service-to-service trust model:
- Authorization model:
- Secret handling:

### Sensitive Data Boundary
- Sensitive data types:
- Encryption expectations:
- Audit expectations:

### Example Only

### External Boundary
- External actors: Product backends, growth engineers
- Entry points: Admin API and assignment API
- Authentication mechanism: OIDC for humans, mTLS or signed service tokens for services

### Internal Boundary
- Service-to-service trust model: Mutual TLS plus workload identity
- Authorization model: Tenant-scoped RBAC with explicit admin scopes
- Secret handling: Secrets pulled from centralized secret manager at startup

### Sensitive Data Boundary
- Sensitive data types: Tenant identifiers, subject identifiers, admin identities
- Encryption expectations: TLS in transit, KMS-managed encryption at rest
- Audit expectations: Publish, pause, and break-glass actions are immutably logged

---

## 5. Control Plane vs Data Plane

Separate configuration/governance concerns from execution concerns.

### Control Plane
- Responsibilities:
- State owned:
- Failure mode:

### Data Plane
- Responsibilities:
- State owned:
- Failure mode:

### Separation Rule
- _[what data-plane code may never mutate directly, and what must go through governed control paths]_

### Example Only

### Control Plane
- Responsibilities: Experiment authoring, validation, publishing, audit logging
- State owned: Authoritative config and version history
- Failure mode: New publishes stop, but running experiments may continue serving from cached snapshots

### Data Plane
- Responsibilities: Assignment evaluation and exposure emission
- State owned: Ephemeral caches and request-scoped evaluation data
- Failure mode: Assignment lookups fail or degrade, but cannot directly alter experiment definitions

### Separation Rule
- The assignment runtime may never mutate experiment state directly; all config changes must go through the governed publish workflow.

---

## 6. Tradeoffs

Record the major architectural choices and why they were made.

### Decision: _[name]_
- Chosen approach:
- Alternative considered:
- Why chosen:
- Cost of this choice:

### Decision: _[name]_
- Chosen approach:
- Alternative considered:
- Why chosen:
- Cost of this choice:

### Example Only

### Decision: `regional config cache`
- Chosen approach: Region-local read cache in assignment runtime
- Alternative considered: Strong read to primary store on every request
- Why chosen: Meets low-latency targets and reduces control-plane dependency
- Cost of this choice: Accepts bounded config staleness

### Decision: `immutable experiment versions`
- Chosen approach: Publish creates immutable versions
- Alternative considered: In-place updates to active experiments
- Why chosen: Easier auditability and rollback
- Cost of this choice: More version management complexity

---

## 7. Risks and Unknowns

Capture what still needs validation.

1. _
2. _
3. _

### Example Only

1. Whether regional cache invalidation can stay inside the 60-second freshness bound during incidents.
2. Whether the exposure pipeline can absorb launch-day burst traffic without backpressure.
3. Whether sticky-assignment requirements vary by tenant tier.
