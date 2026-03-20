# SpecRepo

> Purpose: Shared source of truth for humans and AI during system design and delivery
> Goal: Make problem framing, invariants, requirements, data, consistency, and architecture explicit before implementation

---

## 1. Purpose

This repository captures the minimum set of design documents needed to define a system clearly enough for:

- Humans to review scope, risk, and tradeoffs
- AI to plan, implement, test, and validate against explicit constraints
- Teams to reason from the same source of truth across design and delivery

---

## 2. How to Use This Repo

Recommended order:

1. Start with `PROBLEM.md` to define mission, scope, constraints, and success.
2. Define non-negotiable guarantees in `INVARIANTS.md`.
3. Translate the problem into capabilities in `REQUIREMENTS.md`.
4. Define core entities and ownership in `DATA_MODEL.md`.
5. Define read/write behavior and concurrency in `CONSISTENCY.md`.
6. Describe the system shape and boundaries in `ARCHITECTURE.md`.

Rules:

- Fill in concrete decisions, not vague intent.
- When a tradeoff exists, record the decision and why.
- If something is intentionally deferred, say so explicitly.
- If AI is used to generate plans or code, this repo is the governing context.

---

## 3. File Map

### `PROBLEM.md`
- Defines the business and system problem being solved.
- Establishes scope, constraints, and decision authority.

### `INVARIANTS.md`
- Defines properties that must always hold.
- Guards correctness, safety, and governance.

### `REQUIREMENTS.md`
- Defines what the system must do and how well it must do it.
- Converts problem framing into verifiable expectations.

### `DATA_MODEL.md`
- Defines core entities, keys, ownership, and lifecycle.
- Prevents ambiguity in system state and boundaries.

### `CONSISTENCY.md`
- Defines read/write semantics, ordering, and conflict handling.
- Prevents hidden assumptions about system behavior.

### `ARCHITECTURE.md`
- Defines major components, interactions, and trust boundaries.
- Explains how the system satisfies the spec.

---

## 4. Workflow Summary

Use this repo as the decision backbone for the delivery loop:

1. Define the problem.
2. Define invariants.
3. Define requirements and data shape.
4. Define consistency model and architecture.
5. Implement and test against the spec.
6. Review changes against this repo, not intuition alone.
7. Update the spec when reality changes.

---

## 5. Working Agreement

- Humans own correctness, risk tolerance, and approval.
- AI may assist with drafting, implementation, and validation.
- When code or behavior conflicts with this repo, the repo wins until intentionally revised.
