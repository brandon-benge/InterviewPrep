# Workflow Loop

This document isolates the end-to-end flow described in the broader delivery model.

For full detail, see [AI-Native Software Delivery System](./ai-native-software-delivery.md).

## Loop Summary

```text
Intent -> Spec -> Plan -> Build Loop -> Pull Request -> Human Review -> Build -> Release -> Evaluate -> Update Spec -> Repeat
```

## Stages

### 1. Intent
- Humans define the business problem, constraints, and success criteria

### 2. Spec
- Humans and artificial intelligence refine the governing written context
- This usually includes problem framing, requirements, invariants, data model, consistency rules, and architecture

### 3. Plan
- `PlannerAgent` turns the spec into tasks and dependencies

### 4. Build Loop
- `CoderAgent`, `TestAgent`, `SecurityAgent`, `RefactorAgent`, and `Guardrails` iterate until the change satisfies constraints

### 5. Pull Request
- The system prepares a review artifact with diffs, reasoning, validation, and risk signals

### 6. Human Review
- Engineers and leads review against the spec, not only against the diff

### 7. Build
- Continuous integration produces a deployable artifact

### 8. Release
- Delivery progresses through lower-risk environments toward production with gates and telemetry

### 9. Evaluate
- `EvaluationEngine` converts runtime signals into release judgments and improvement suggestions

### 10. Update Spec
- Production lessons, defects, and tradeoffs update the specification before the next iteration

## Why This Matters

The main shift is that the spec is not only written before coding. It stays active through review, release, and learning.
