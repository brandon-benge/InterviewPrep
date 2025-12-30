# Retry Strategies

Retry strategies handle transient failures in distributed systems. Proper retry logic prevents cascade failures while improving reliability.

---

## Exponential Backoff

**Formula:** `wait_time = base_delay * (2 ^ attempt_number)`

**Example:** 1s → 2s → 4s → 8s → 16s (doubles each attempt)

**Use case:** API retries, database reconnects, transient failures

---

## Jitter (Randomized Delay)

**Formula:** `wait_time = random(0, base_delay * (2 ^ attempt_number))`

**Why:** Prevents retry storms when many clients fail simultaneously. Without jitter, all clients retry at exact same intervals (1s, 2s, 4s) causing thundering herd.

**Types:** Full jitter (random 0 to max), Equal jitter (always wait at least 50%), Decorrelated jitter (smooth growth)

---

## Per-Resource Retry Budgets(client)

**Problem:** 1000 clients × 5 retries = 5000 extra requests overwhelming failing service

**Solution:** Track retry ratio `retries / (requests + retries)`. If exceeds threshold (e.g., 10%), fail fast instead of retrying.

**Example:** 1000 requests + 100 retries = 9.1% ratio ✅ Allow. 1000 requests + 200 retries = 16.7% ratio ❌ Fail fast.

---

## Circuit Breaker(client, api gateway/proxy, or sidecar/service mesh)

**Definition:** Automatic mechanism that stops calling a failing service after threshold is reached, preventing cascading failures and resource exhaustion.

**States:**
- **Closed:** Normal operation, track failures
- **Open:** Fail fast (no requests), after timeout → Half-Open
- **Half-Open:** Send probe, if succeeds → Closed, if fails → Open

**Why critical for lock services:** ZooKeeper/etcd are single points of failure. Circuit breaker prevents cascading failure by failing fast when lock service is down.

**Example:** 5 failures → Open (30s) → Probe → Close or Re-open

---

## Global Admission Control

**Definition:** System-wide throttling to prevent overload by rejecting requests before processing

**Who rejects:** Frontend/API Gateway or load balancer intercepts requests, checks admission controller (Redis/etcd), and returns 503/429 before forwarding to backend.

**Strategy:** Track global capacity (RPS), reject when at limit. Use token bucket or centralized coordinator (Redis, etcd).

**Example:** Backend capacity 80k RPS, frontend receives 100k RPS → API Gateway rejects 20k immediately with 503 (prevents backend overload)

**Priority-based:** Critical requests (payments, auth) always accepted, best-effort (analytics) rejected under load.

---

## Layered Approach

```
Layer 1: Exponential Backoff + Jitter (prevent thundering herd)
Layer 2: Retry Budgets (limit amplification)
Layer 3: Circuit Breaker (fail fast on critical deps)
Layer 4: Admission Control (system-wide load shedding)
```

---

## Best Practices

- Always use jitter (full jitter recommended)
- Max 3-5 retries (prevent infinite loops)
- Only retry transient errors (5xx, timeouts) - NOT 4xx
- Use circuit breakers for lock services, databases
- Monitor retry ratios (alert >10%)
- Idempotency tokens for writes (payments, orders)

---

## See Also
- [rate-limiting.md](./rate-limiting.md)
- [circuit-breaker.md](./circuit-breaker.md)
- [load-balancing.md](./load-balancing.md)
