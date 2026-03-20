# Test Plan Template

> Purpose: Define how the system will be validated against requirements and invariants
> Goal: Make correctness strategy explicit before implementation and release

---

## 1. Test Objectives

- What must be proven:
- Highest-risk behaviors:
- Invariants that require direct validation:
- Release-blocking failures:

---

## 2. Test Layers

### Unit Tests
- Scope:
- Target components:
- Main purpose:

### Integration Tests
- Scope:
- Target boundaries:
- Main purpose:

### End-to-End Tests
- Scope:
- Critical workflows:
- Main purpose:

### Failure / Resilience Tests
- Scope:
- Fault injection targets:
- Main purpose:

---

## 3. Invariant-to-Test Mapping

### Invariant: _[name]_
- Validation strategy:
- Test layer:
- Pass condition:

### Invariant: _[name]_
- Validation strategy:
- Test layer:
- Pass condition:

---

## 4. Test Data Strategy

- Synthetic vs production-like data:
- Sensitive data handling:
- Deterministic fixtures:
- Data reset strategy:

---

## 5. Environment Strategy

- Local expectations:
- CI expectations:
- Staging expectations:
- Production verification expectations:

---

## 6. Exit Criteria

- Required pass rate:
- Required coverage areas:
- Performance gates:
- Security / correctness gates:

---

## 7. Known Gaps

1. _
2. _
3. _
