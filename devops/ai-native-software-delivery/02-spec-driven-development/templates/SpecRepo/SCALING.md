# Scaling Template

> Purpose: Describe how the system handles growth in traffic, tenants, data, and operational complexity
> Goal: Make scaling assumptions and bottlenecks explicit before they become incidents

---

## 1. Growth Assumptions

- Current load:
- Expected steady-state growth:
- Peak growth pattern:
- Tenant / user growth:
- Data growth:

---

## 2. Bottleneck Hypotheses

### Suspected Bottleneck: _[component or resource]_
- Why it may bottleneck:
- Leading indicator:
- Breaking point estimate:
- Mitigation options:

### Suspected Bottleneck: _[component or resource]_
- Why it may bottleneck:
- Leading indicator:
- Breaking point estimate:
- Mitigation options:

---

## 3. Scaling Strategy

### Compute
- Horizontal or vertical:
- Autoscaling signal:
- Warm-up concerns:

### Storage
- Partitioning strategy:
- Retention strategy:
- Archival strategy:

### Network / Dependency Limits
- External dependency ceilings:
- Rate limit strategy:
- Queueing / buffering strategy:

---

## 4. Capacity Guardrails

- Maximum safe QPS:
- Maximum safe queue depth:
- Maximum tenant concentration:
- Cost ceiling at peak:

---

## 5. Validation Plan

- Load test scope:
- Soak test scope:
- Failure-under-load test:
- Success criteria:

---

## 6. Unknowns

1. _
2. _
3. _
