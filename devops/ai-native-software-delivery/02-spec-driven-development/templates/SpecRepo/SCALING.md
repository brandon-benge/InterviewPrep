# Scaling Template

> Purpose: Describe how the system handles growth in traffic, tenants, data, and operational complexity
> Goal: Make scaling assumptions and bottlenecks explicit before they become incidents
> Example policy: Any block labeled `Example Only` is illustrative only.

---

## 1. Growth Assumptions

- Current load:
- Expected steady-state growth:
- Peak growth pattern:
- Tenant / user growth:
- Data growth:

### Example Only

- Current load: 12k assignment requests per second
- Expected steady-state growth: 2x over 12 months
- Peak growth pattern: 3x burst during product launches
- Tenant / user growth: from 500 to 1,500 tenants
- Data growth: 2 billion exposure events per month

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

### Example Only

### Suspected Bottleneck: `regional assignment cache refresh`
- Why it may bottleneck: Burst publishes can fan out config invalidations to many nodes
- Leading indicator: Cache age and propagation lag
- Breaking point estimate: Sustained publish bursts across many tenants
- Mitigation options: Batched propagation, config snapshot compression, staged rollout

### Suspected Bottleneck: `exposure pipeline`
- Why it may bottleneck: Every assignment emits an event under peak traffic
- Leading indicator: Queue depth and producer latency
- Breaking point estimate: 100k events/sec during simultaneous launches
- Mitigation options: Partition increase, async buffering, downstream backpressure isolation

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

### Example Only

### Compute
- Horizontal or vertical: Horizontal scale for assignment runtime, modest vertical scale for control plane
- Autoscaling signal: Request rate plus p95 latency plus CPU saturation
- Warm-up concerns: New nodes need latest config snapshot before taking traffic

### Storage
- Partitioning strategy: Partition assignment/exposure data by tenant and time
- Retention strategy: Keep recent events hot, archive older events
- Archival strategy: Daily export to cheaper object storage

### Network / Dependency Limits
- External dependency ceilings: Analytics broker throughput and identity provider token verification rate
- Rate limit strategy: Per-tenant request shaping and admin API write limits
- Queueing / buffering strategy: Isolate analytics buffering from synchronous assignment path

---

## 4. Capacity Guardrails

- Maximum safe QPS:
- Maximum safe queue depth:
- Maximum tenant concentration:
- Cost ceiling at peak:

### Example Only

- Maximum safe QPS: 40k sustained assignment RPS per region
- Maximum safe queue depth: 10 minutes of exposure backlog
- Maximum tenant concentration: No single tenant may exceed 25% of regional runtime capacity
- Cost ceiling at peak: Must remain within approved quarterly platform budget

---

## 5. Validation Plan

- Load test scope:
- Soak test scope:
- Failure-under-load test:
- Success criteria:

### Example Only

- Load test scope: 40k RPS assignment traffic with realistic tenant skew
- Soak test scope: 24-hour run with steady traffic and periodic experiment publishes
- Failure-under-load test: Drop analytics broker and verify assignment latency remains healthy
- Success criteria: p99 under 50 ms, no cross-tenant bleed, backlog recovers after dependency restoration

---

## 6. Unknowns

1. _
2. _
3. _

### Example Only

1. Tenant skew may be more extreme than current forecasts.
2. Experiment publish storms may produce unexpected cache fan-out costs.
3. Exposure replay under regional failover needs performance validation.
