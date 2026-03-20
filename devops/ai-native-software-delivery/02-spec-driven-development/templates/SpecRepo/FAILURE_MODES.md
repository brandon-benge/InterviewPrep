# Failure Modes Template

> Purpose: Define how the system behaves when components, dependencies, or assumptions fail
> Goal: Make failure handling explicit before production exposure

---

## 1. Failure Scenarios

### Scenario: _[name]_
- Trigger:
- Affected components:
- User-visible impact:
- Data risk:
- Detection mechanism:

### Scenario: _[name]_
- Trigger:
- Affected components:
- User-visible impact:
- Data risk:
- Detection mechanism:

---

## 2. Expected System Behavior

For each scenario, define the intended system response.

- Fail open or fail closed:
- Retry behavior:
- Degradation behavior:
- Manual intervention required or not:
- Recovery condition:

---

## 3. Containment Strategy

- Isolation boundary:
- Blast radius expectation:
- Circuit breaker / backpressure behavior:
- Escalation path:

---

## 4. Recovery Strategy

- Automatic recovery path:
- Manual recovery path:
- Reconciliation required:
- Recovery validation:

---

## 5. Open Risks

1. _
2. _
3. _
