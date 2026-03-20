# Observability Template

> Purpose: Define what the system must expose through logs, metrics, traces, and alerts
> Goal: Make correctness, performance, and failure states observable enough to operate safely

---

## 1. Observability Goals

- What operators must know:
- What developers must debug:
- What business owners must measure:
- What auditors must reconstruct:

---

## 2. Logs

- Required structured fields:
- Sensitive fields that must be excluded or masked:
- Correlation identifiers:
- Retention policy:

### Required Log Events
- _
- _
- _

---

## 3. Metrics

### Golden Signals
- Latency:
- Traffic:
- Errors:
- Saturation:

### Business / Domain Metrics
- _
- _
- _

### Invariant / Safety Metrics
- _
- _
- _

---

## 4. Traces

- Critical flows to trace:
- Required span attributes:
- Sampling strategy:
- Cross-service propagation mechanism:

---

## 5. Alerts

### Page-Worthy Alerts
- Condition:
- Threshold:
- Runbook target:

### Ticket / Investigation Alerts
- Condition:
- Threshold:
- Owner:

---

## 6. Dashboards and Reporting

- Operational dashboard:
- Executive / product dashboard:
- Compliance / audit reporting:

---

## 7. Gaps

1. _
2. _
3. _
