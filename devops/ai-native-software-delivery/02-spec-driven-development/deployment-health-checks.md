# Deployment Health Checks (Step 9 - EvaluationEngine)

## Core Principle

Raw telemetry is not evaluated directly.

```
Raw telemetry
→ derived health signals
→ policy evaluation
→ rollout decision
```

Deterministic signals drive decisions. AI is used for summarization and insight, not primary pass/fail logic.

---

## Evaluation Layers

### 1. Telemetry Normalization

Collect and standardize:
- Metrics (Prometheus)
- Logs
- Traces
- Deployment metadata
- Test and scan results

---

### 2. Feature Extraction

Convert raw data into structured signals:
- Error rate delta
- Latency (p95/p99) delta
- CPU / memory saturation
- Restart counts
- Queue lag / backlog
- New error signatures
- Invariant violations
- Vulnerability counts
- Policy violations

---

### 3. Decision Engine (Deterministic)

Evaluate signals against rules:
- Pass → promote rollout
- Hold → continue monitoring
- Fail → rollback
- Escalate → require human decision

Examples:
- Error rate > threshold → fail
- Latency regression > X% → hold
- Invariant violation > 0 → fail

---

### 4. AI Explanation Layer

AI summarizes and explains:
- What changed
- Which signals degraded
- Likely root causes
- Recommended next actions

AI does NOT determine pass/fail.

---

## Signal Categories

### Metrics (Prometheus)
- Success rate
- Error rate
- Latency (p95/p99)
- Saturation (CPU, memory)
- Throughput
- Restart counts

Pattern:
- Compare baseline vs canary
- Compare pre vs post deployment

---

### Logs
- Error count by type
- New log signatures
- Exception clustering
- Severity spikes

Pattern:
- Detect new or increasing error classes
- Compare before/after deployment

---

### Correctness (Invariants)
- Synthetic transactions
- Replay validation
- Reconciliation jobs
- Invariant counters

Examples:
- No duplicate events
- No stale writes
- Ordering preserved

---

### Regressions
- Latency changes
- Throughput changes
- Resource usage changes
- Retry amplification

Pattern:
- Compare against last stable version
- Compare canary vs control

---

### Reliability
- Availability
- Error budget burn
- Restart frequency
- Dependency health
- Queue lag

Pattern:
- Multi-window evaluation
- Dependency-aware analysis

---

### Policy Adherence
- No critical vulnerabilities
- No secret exposure
- Required telemetry present
- Deployment rules followed

Pattern:
- Rule-based validation
- Policy-as-code enforcement

---

## Example Evaluation

```
Metrics:
- p95 latency +12%
- error rate +0.02%

Logs:
- minor new warning class

Correctness:
- invariants passing

Reliability:
- stable

Policy:
- no violations
```

Decision:
- Hold or promote based on thresholds

AI Output:
- Summary of changes
- Highlight degraded signals
- Suggest root cause

---

## Key Takeaways

- LLMs should not process raw telemetry directly
- Always reduce telemetry into structured signals first
- Use deterministic rules for decisions
- Use AI for summarization and insight

Evaluation is continuous and feeds back into planning and spec updates.