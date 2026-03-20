# Scrum to AI Native

## Overview

Agile does not go away in AI-native workflows. What changes is the **unit of execution**.

Traditional Agile:
- Tickets drive development
- Humans decompose work
- Sprints organize execution

AI-Native Agile:
- Spec drives development
- AI decomposes and executes work
- Continuous loops replace rigid sprints

---

## The Core Shift

| Aspect | Traditional Agile | AI-Native Agile |
|-------|------------------|-----------------|
| Execution Flow | Product → Tickets → Dev → Release | Product → Spec → AI Plan → Build Loop → PR → Evaluate → Spec Update |
| Unit of Work | Tickets | Spec Changes + PRs |
| Decomposition | Human-driven | AI-driven (PlannerAgent) |
| Iteration Model | Sprints | Continuous execution loops |

- **SpecRepo replaces most detailed tickets**
- **PlannerAgent generates execution tasks dynamically**
- **PR becomes the primary unit of work and review**

---

## Do Tickets Still Exist?

Yes, but their role changes significantly.

### 1. Strategic Tickets (Still Human-Created)
Used for:
- Large initiatives
- Cross-team coordination
- Roadmap tracking

These map to **SpecRepo creation or major updates**.

---

### 2. Spec Changes (Replace Most Tickets)
Instead of writing tickets like:
- "Add retry logic"

You update:
- INVARIANTS.md
- REQUIREMENTS.md

The system then regenerates execution work.

---

### 3. AI-Generated Execution Tasks
- Created by PlannerAgent
- Ephemeral and regenerated per iteration
- Not stored long-term like Jira tickets

These are effectively **machine-generated tickets**.

---

## What Replaces Scrum Concepts

| Scrum Concept | Traditional Agile | AI-Native Equivalent |
|--------------|------------------|----------------------|
| Backlog | List of tickets | Spec + Spec changes |
| Stories | Ticket-level work items | Spec deltas (changes to PROBLEM.md, INVARIANTS.md, REQUIREMENTS.md) |
| Sprint | Fixed time-box (e.g., 2 weeks) | Planning window / continuous execution cycle |
| Dev Work | Engineers execute tickets | AI agents execute task graph |
| Unit of Review | Ticket / Story | Pull Request (PR) |

---

## Updated Agile Rituals

| Ritual | Traditional Agile | AI-Native Agile |
|--------|------------------|-----------------|
| 3-in-the-Box | Backlog grooming, ticket prioritization | Outcome alignment, spec change review, tradeoffs |
| Standup | Ticket status updates | Blockers, PR status, evaluation signals |
| Retro | Process reflection | Spec quality, invariant gaps, workflow improvements |
| Demo | Feature delivery | Outcomes, value, evaluation results |
| 1-on-1 | Career and performance | System design, judgment, spec quality, ownership |

---

## Roles and Ownership

| Role | Traditional Agile Responsibility | AI-Native Responsibility |
|------|--------------------------------|--------------------------|
| Product Manager | Defines features and backlog | Owns PROBLEM.md (mission, users, success) |
| Tech Lead / Architect | Designs system, supports team | Owns technical spec (INVARIANTS, REQUIREMENTS, DATA_MODEL, CONSISTENCY, ARCHITECTURE) |
| Engineers | Implement tickets | Contribute to spec, validate edge cases, refine implementation |

---

### Key Principle

```
Ownership = Tech Lead
Authorship = Distributed
```

---

## What Humans Still Do

Humans remain responsible for:
- Prioritization
- Tradeoffs
- Ambiguity resolution
- Risk management
- Final approval

---

## What AI Does

AI handles:
- Task decomposition
- Code generation
- Test generation
- Iterative refinement

---

## Why Tickets Become Less Important

Tickets assume:
- Humans break down work
- Humans execute tasks

In AI-native systems:
- AI decomposes faster than humans
- Tickets become stale quickly
- Spec provides a more reliable source of truth

---

## Final Mental Model

```
Old Scrum:
Backlog → Tickets → Sprint → Dev → Release

AI-Native Agile:
Spec → Spec Change → AI Plan → Build Loop → PR → Evaluate → Spec Update
```

---

## Summary

- Agile remains, but evolves
- Spec replaces tickets as the execution driver
- AI generates and executes work
- Humans guide, validate, and govern
- PR and evaluation loops become central