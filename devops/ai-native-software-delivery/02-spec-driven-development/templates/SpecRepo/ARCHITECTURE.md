# Architecture Template

> Purpose: Describe the major system components and how they satisfy the spec
> Goal: Make boundaries, interactions, and tradeoffs reviewable before implementation

---

## 1. Overview

**System statement:** _[one paragraph describing what the system is, who uses it, and what it must guarantee]_

### Primary Design Drivers
- _[e.g., low latency, tenant isolation, auditability, cost efficiency]_

### Architecture Style
- _[e.g., request/response service, event-driven pipeline, control plane + workers, batch + streaming hybrid]_

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

---

## 7. Risks and Unknowns

Capture what still needs validation.

1. _
2. _
3. _
