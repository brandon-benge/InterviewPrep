# Director-Level Problem Framing Cheat Sheet

> Purpose: Guard rails for Step 1 of a system design interview  
> Goal: Force explicit scope, success, and authority before design

---

## 1. One-Sentence Mission

**We are building _[X]_ so that _[Y]_ can _[Z]_, under constraints _[A / B / C]_.**

- X = system or capability
- Y = primary user or actor
- Z = measurable outcome
- A/B/C = hard constraints (latency, cost, regulation, trust)

---

## 2. Users / Actors

Primary:
- _

Secondary:
- _

---

## 3. Scope Boundaries

### In Scope
- _

### Out of Scope
- _

### Deferred / Assumed
- _

---

## 4. Inputs / Outputs

Inputs:
- _

Outputs:
- _

---

## 5. Success Definition

### Business Outcome
- _[e.g., cost avoidance, revenue protection, risk reduction]_

### User / Platform Outcome
- _[e.g., p99 latency, determinism, availability]_

### Safety Outcome
- _[e.g., never overspend, never corrupt records, never bypass audit]_

---

## 6. Constraints

- Latency:
- Scale:
- Cost:
- Compliance:
- Data sensitivity:

---

## 7. Tradeoff Authority Line

When _[A]_ conflicts with _[B]_, we choose _[A]_ because _[reason]_.

- Escalation path:
  - _[e.g., executive override, break-glass policy, manual approval]_

---

## 8. Explicit Assumptions

1. _
2. _
3. _
