# Director-Level Problem Framing Cheat Sheet

> Purpose: Guard rails for Step 1 of a system design interview  
> Goal: Force explicit scope, success, and authority before design
> Example policy: Any block labeled `Example Only` is illustrative only. Humans and agents must not treat it as the actual problem statement.

---

## 1. One-Sentence Mission

**We are building _[X]_ so that _[Y]_ can _[Z]_, under constraints _[A / B / C]_.**

- X = system or capability
- Y = primary user or actor
- Z = measurable outcome
- A/B/C = hard constraints (latency, cost, regulation, trust)

### Example Only

**We are building a tenant-scoped experiment assignment service so that product backends can fetch deterministic treatments in real time, under constraints sub-50 ms p99 latency, strict tenant isolation, and bounded infra cost.**

---

## 2. Users / Actors

Primary:
- _

Secondary:
- _

### Example Only

Primary:
- Product application backend requesting assignment decisions

Secondary:
- Growth engineer creating experiments
- Analyst consuming exposure logs
- SRE operating the service

---

## 3. Scope Boundaries

### In Scope
- _

### Out of Scope
- _

### Deferred / Assumed
- _

### Example Only

### In Scope
- Create and publish experiments
- Evaluate assignments for subjects
- Log exposures for analytics

### Out of Scope
- Client-side SDK rendering
- Statistical significance calculations
- BI dashboarding

### Deferred / Assumed
- Multi-region active-active write support is deferred
- We assume tenant IDs are provided by the caller's trusted identity layer

---

## 4. Inputs / Outputs

Inputs:
- _

Outputs:
- _

### Example Only

Inputs:
- `tenant_id`, `experiment_key`, `subject_id`, optional context attributes

Outputs:
- Assigned treatment variant
- Evaluation reason and config version
- Exposure event for downstream analytics

---

## 5. Success Definition

What outcomes prove this solution is successful if delivered?
These are target results or acceptance criteria, not hard limits.

### Business Outcome
- _[e.g., cost avoidance, revenue protection, risk reduction]_

### User / Platform Outcome
- _[e.g., p99 latency target, determinism, availability, adoption]_

### Safety Outcome
- _[e.g., auditable actions, no silent data loss, bounded blast radius]_

### Example Only

### Business Outcome
- Product teams can launch experiments without asking platform engineers for manual rollout support

### User / Platform Outcome
- Assignment lookups complete under 50 ms p99 at forecast peak load
- Treatment decisions are deterministic for the same subject and experiment version

### Safety Outcome
- Cross-tenant reads never succeed
- Exposure logging failures are visible within 5 minutes

---

## 6. Constraints

What limits are non-negotiable regardless of solution quality?
These are boundaries the design is not allowed to violate.

- Latency ceiling:
- Scale floor / peak load:
- Cost cap:
- Compliance / regulatory limits:
- Data sensitivity / residency:
- Time / staffing / dependency limits:

### Example Only

- Latency ceiling: assignment API must stay below 100 ms p99 under peak load
- Scale floor / peak load: sustain 40k assignment requests per second at 3x launch-day burst
- Cost cap: remain within the existing shared platform budget envelope
- Compliance / regulatory limits: audit admin actions and preserve immutable publish history
- Data sensitivity / residency: subject identifiers are pseudonymous and region-bound
- Time / staffing / dependency limits: one staff engineer plus one platform engineer for initial delivery

---

## 7. Tradeoff Authority Line

When _[A]_ conflicts with _[B]_, we choose _[A]_ because _[reason]_.

- Escalation path:
  - _[e.g., executive override, break-glass policy, manual approval]_

### Example Only

When latency conflicts with perfectly fresh config propagation, we choose deterministic correctness and tenant isolation because serving a wrong assignment is worse than serving a slightly stale one.

- Escalation path:
  - Product engineering director can approve temporary stale-read windows during incidents

---

## 8. Explicit Assumptions

1. _
2. _
3. _

### Example Only

1. Subject IDs are already normalized by the caller.
2. Experiment definitions are low write volume compared with assignment traffic.
3. Exposure analytics may lag assignment decisions by several minutes without harming the product workflow.
