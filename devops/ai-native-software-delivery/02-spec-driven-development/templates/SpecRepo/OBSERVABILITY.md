# Observability Template

> Purpose: Define what the system must expose through logs, metrics, traces, and alerts
> Goal: Make correctness, performance, and failure states observable enough to operate safely
> Example policy: Any block labeled `Example Only` is illustrative only.

---

## 1. Observability Goals

- What operators must know:
- What developers must debug:
- What business owners must measure:
- What auditors must reconstruct:

### Example Only

- What operators must know: regional latency, stale config age, assignment error rate, exposure backlog
- What developers must debug: per-request evaluation path, rule-matching decisions, duplicate suppression
- What business owners must measure: assignment volume by tenant and experiment adoption
- What auditors must reconstruct: who published what config and when it took effect

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

### Example Only

- Required structured fields: `timestamp`, `service`, `tenant_id`, `request_id`, `experiment_key`, `config_version`, `outcome`
- Sensitive fields that must be excluded or masked: raw subject identifiers, tokens, secrets
- Correlation identifiers: `request_id`, trace ID, publish operation ID
- Retention policy: 30 days hot, 1 year archived for audit logs

### Required Log Events
- Experiment publish succeeded or failed
- Assignment request evaluated with config version
- Exposure write retry exhausted

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

### Example Only

### Golden Signals
- Latency: assignment API p50/p95/p99 by tenant and region
- Traffic: assignment QPS and publish QPS
- Errors: assignment failures, auth failures, exposure write failures
- Saturation: CPU, memory, queue depth, cache refresh lag

### Business / Domain Metrics
- Active experiments per tenant
- Assignments served per variant
- Exposure delivery lag

### Invariant / Safety Metrics
- Cross-tenant auth rejection count
- Duplicate assignment collapse rate
- Config version skew across regions

---

## 4. Traces

- Critical flows to trace:
- Required span attributes:
- Sampling strategy:
- Cross-service propagation mechanism:

### Example Only

- Critical flows to trace: assignment evaluation, experiment publish, exposure delivery
- Required span attributes: `tenant_id`, `experiment_key`, `config_version`, `decision_reason`
- Sampling strategy: head-based baseline plus tail-based retention for high-latency and error traces
- Cross-service propagation mechanism: W3C trace context

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

### Example Only

### Page-Worthy Alerts
- Condition: assignment API p99 latency breach
- Threshold: above 100 ms for 10 minutes
- Runbook target: assignment-runtime-oncall

### Ticket / Investigation Alerts
- Condition: cache age exceeds target but remains below hard stale ceiling
- Threshold: above 30 seconds for 30 minutes
- Owner: platform team

---

## 6. Dashboards and Reporting

- Operational dashboard:
- Executive / product dashboard:
- Compliance / audit reporting:

### Example Only

- Operational dashboard: latency, errors, version skew, backlog, auth failures
- Executive / product dashboard: experiment traffic, tenant adoption, feature usage
- Compliance / audit reporting: publish history, privileged admin actions, break-glass events

---

## 7. Gaps

1. _
2. _
3. _

### Example Only

1. Rule-level evaluation traces may be too expensive to retain at full volume.
2. Exposure pipeline replay visibility may be insufficient for auditors.
3. Tenant-specific SLO dashboards may be needed for premium customers.
