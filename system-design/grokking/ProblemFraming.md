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

## 2. Scope Boundaries (Three-Box Model)

### In Scope
- We explicitly own:
  - _
  - _

### Out of Scope (Non-Goals)
- We do **not** solve:
  - _
  - _

### Deferred / Assumed
- We assume the existence of:
  - _
- We integrate with it but do not own it.

---

## 3. Success Definition

### Business Outcome
- _[e.g., cost avoidance, revenue protection, risk reduction]_

### User / Platform Outcome
- _[e.g., p99 latency, determinism, availability]_

### Safety Outcome
- _[e.g., never overspend, never corrupt records, never bypass audit]_

---

## 4. Tradeoff Authority Line

**When _[A]_ conflicts with _[B]_, we choose _[A]_ because _[reason]_.**

- Escalation path:
  - _[e.g., executive override, break-glass policy, manual approval]_

---

## 5. Explicit Assumptions (Limit: 3)

Only assumptions you are willing to be judged on:

1. _
2. _
3. _

---

## 6. Top Failure Modes (Named Only)

- _
- _
- _

---

## Stop Here

Do **not** proceed to:
- Architecture
- APIs
- Data models
- Storage or implementation details

Next step: **Declare non-negotiable correctness invariants.**