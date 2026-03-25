# Failure Modes Template

> Purpose: Define how the system behaves when components, dependencies, or assumptions fail
> Goal: Make failure handling explicit before production exposure
> Example policy: Any block labeled `Example Only` is illustrative only.

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

### Example Only

### Scenario: `regional cache stale beyond policy`
- Trigger: Config propagation worker is delayed or stuck
- Affected components: Assignment runtime in one region
- User-visible impact: Subjects may receive decisions based on an older experiment version
- Data risk: Wrong experiment policy applied within stale window
- Detection mechanism: Cache age metric and version-skew alert

### Scenario: `exposure sink unavailable`
- Trigger: Analytics broker outage
- Affected components: Exposure pipeline
- User-visible impact: Assignment API still works, analytics lag grows
- Data risk: Potential duplicate or delayed exposure events if retries are mishandled
- Detection mechanism: Queue depth, publish failures, retry backlog

---

## 2. Expected System Behavior

For each scenario, define the intended system response.

- Fail open or fail closed:
- Retry behavior:
- Degradation behavior:
- Manual intervention required or not:
- Recovery condition:

### Example Only

- Fail open or fail closed: Assignment runtime may serve from last-known-good cache within the freshness policy; admin publish path fails closed
- Retry behavior: Exposure pipeline retries with backoff and idempotent keys
- Degradation behavior: Mark assignment responses with config version and stale status in diagnostics
- Manual intervention required or not: Manual intervention only if staleness exceeds policy or backlog growth continues
- Recovery condition: Latest config applied and backlog returns below threshold

---

## 3. Containment Strategy

- Isolation boundary:
- Blast radius expectation:
- Circuit breaker / backpressure behavior:
- Escalation path:

### Example Only

- Isolation boundary: Tenant-scoped auth boundary plus region-local runtime caches
- Blast radius expectation: One region or one downstream analytics dependency at a time
- Circuit breaker / backpressure behavior: Stop exposure fan-out before it impacts assignment latency
- Escalation path: Runtime on-call -> platform on-call -> product owner if stale window must be extended

---

## 4. Recovery Strategy

- Automatic recovery path:
- Manual recovery path:
- Reconciliation required:
- Recovery validation:

### Example Only

- Automatic recovery path: Retry propagation and replay queued exposure events
- Manual recovery path: Pause affected experiments or force global fallback treatment
- Reconciliation required: Yes, compare emitted exposure count with persisted assignment count
- Recovery validation: Confirm latest config version present in all regions and backlog drained

---

## 5. Open Risks

1. _
2. _
3. _

### Example Only

1. Break-glass fallback treatment may affect experiment validity.
2. Duplicate exposure replay policy may not be fully aligned with downstream analytics assumptions.
3. Region isolation policy during partial control-plane outage needs explicit approval.
