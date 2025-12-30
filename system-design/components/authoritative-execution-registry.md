# Authoritative Execution Registry

## Overview
Coordination service ensuring exactly-once distributed job execution via fencing tokens (monotonic counters), leases (auto-expiring ownership), and resource locks. Prevents duplicate work, zombie workers, and split-brain scenarios through automatic failover and strong consistency guarantees.

---

## Schema
```
job_id: "video_encode_12345"              # Unique identifier
region: "us-east-1"                       # Regional isolation
resource_lock_key: "job:video_encode_12345" # Lock key
state: RUNNING                            # PENDING|RUNNING|COMPLETED|FAILED
owner: "worker-7"                         # Current worker
lease_expiry: 12:05                       # Auto-expire timestamp
fencing_token: 42                         # Monotonic counter (authorizes execution)
attempt: 3                                # Retry count
ttl_deadline: 13:00                       # Hard deadline (prevent infinite retry)
```

---

## Key Concepts

**Fencing Tokens:** Monotonically increasing counters authorizing execution. Registry increments counter per lease request. Downstream services reject stale tokens (lower numbers), preventing zombie workers from submitting duplicate results.

### Fencing Token Safety Patterns

**Pattern 1: Authoritative Lock Store (Safest)**
- Token is monotonic epoch stored in lock service (ZooKeeper/etcd)
- Write proxy validates: `if (token < current_epoch) reject()`
- Every write checks authoritative source (high consistency, adds latency)

**Pattern 2: Fast Path Cache + Bounded Staleness (Balanced)**
- Proxy caches current epoch locally (avoid lock service per request)
- Fast path: Check cached epoch (low latency)
- If token ≈ cached epoch (within threshold), fallback to authoritative check
- Bounded staleness: Cache expires after 5-10 seconds (prevents accepting very stale tokens)
- Example: token=42, cache=41 → Close enough, check authoritative. token=30, cache=41 → Too stale, reject immediately.

**Pattern 3: Write-Through Cache (Performance)**
- Lock service publishes epoch updates via pub/sub (Redis, Kafka)
- Proxy subscribes and updates local cache
- Reject if `token < cached_epoch`, no authoritative check needed
- Risk: Missed updates if subscriber lags (use heartbeat to detect staleness)

**Leases:** Exclusive job ownership with 5-min expiration, 30-sec heartbeat interval. Auto-expires on worker crash/network failure, enabling automatic failover.
---

## Flow
1. **Acquire:** Worker requests lease → Registry returns fencing_token, lease_expiry → State: PENDING→RUNNING
2. **Heartbeat:** Worker sends heartbeat every 30s with fencing_token → Registry extends lease_expiry
3. **Complete:** Worker submits result with fencing_token → Registry validates token → State: RUNNING→COMPLETED
4. **Failover:** Lease expires (no heartbeat) → State: RUNNING→PENDING → New worker acquires with incremented fencing_token
---

## Scenarios

**Duplicate Prevention:** worker-7 acquires lease (token #42) → worker-9 attempts same job → Rejected ("Job owned by worker-7") → Exactly-once execution

**Crash Failover:** worker-7 acquires (token #42) → worker-7 crashes → Lease expires → worker-9 acquires (token #43) → worker-7 recovers, submits with #42 → Rejected (stale) → worker-9 completes with #43 → Accepted

---

---

## API

**Acquire:** `POST /registry/acquire-job {job_id, worker_id, region}` → `{fencing_token, lease_expiry, attempt, ttl_deadline}`

**Heartbeat:** `POST /registry/heartbeat {job_id, worker_id, fencing_token}` → `{new_lease_expiry}`

**Complete:** `POST /registry/complete-job {job_id, worker_id, fencing_token, result}` → `{success}`

**Status:** `GET /registry/job-status/{job_id}` → `{state, owner, fencing_token, lease_expiry, attempt}`

**Release:** `POST /registry/release-job {job_id, worker_id, fencing_token, reason}` → `{state: PENDING, attempt: incremented}`
---

## Benefits & Trade-offs

**Pros:**
- ✅ Exactly-once execution (prevents duplicate work, zombie workers)
- ✅ Automatic failover (no manual intervention)
- ✅ Split-brain prevention (strong consistency)
- ✅ Audit trail (owner, attempt count, fencing token ordering)
- ✅ Resource efficiency (TTL prevents infinite retry)

**Cons:**
- ❌ +100ms latency (lease acquisition)
- ❌ Coordination service required (ZooKeeper/etcd)
- ❌ Heartbeat overhead (30s network calls)
- ❌ Single point of failure
- ❌ Reduced availability during network partition
---

## When to Use

**Use when:** Multiple workers process same job (distributed queue), duplicate execution is expensive (video encoding, payments), jobs have side effects, strong consistency > availability (CP)

**Skip if:** Jobs are idempotent, single-worker system, eventual consistency acceptable, high-frequency (>1000/sec) where overhead too high


## Alternative: Idempotency Keys

Simpler approach: Job has unique key, storage deduplicates submissions (only first accepted). **Pros:** No coordination service, lower latency, higher availability. **Cons:** Does NOT prevent duplicate execution (wasted compute), no automatic failover, no ownership tracking. **Use when:** Jobs cheap to execute, AP > CP, downstream services deduplicate.

## Industry Examples

**Google Chubby:** Lock service for GFS/Bigtable, issues sequence numbers (fencing tokens), 60s lease
**Kafka:** ZooKeeper ephemeral znodes for broker liveness, epoch number prevents stale leaders
**Temporal:** Workflow exclusive lease with heartbeats, event history prevents duplicate execution
**Kubernetes:** etcd lease-based leader election for control plane


## Implementation

**Tech:** ZooKeeper (mature), etcd (Kubernetes-native), Consul (service discovery + coordination)
## Best Practices

**Lease Duration:** 5 min (balance recovery vs overhead). Long jobs use 15 min.
**Heartbeat Interval:** 1/10 of lease (30s for 5-min lease). Fail after 3 missed heartbeats.
**TTL Deadline:** P99 job duration × 3 (allow retries). Alert if frequently hit.
**Retry Strategy:** Max 5-10 attempts with exponential backoff. Alert if jobs consistently fail.
## Summary

Ensures exactly-once job execution through fencing tokens (monotonic counters), leases (auto-expiring ownership), resource locks (prevent concurrent execution), and TTL deadlines (prevent infinite retries).

**Critical for:** Distributed job processing (video encoding, ML training, ETL), message queue consumers with side effects, batch processing with worker failures.

**Trade-off:** Exactly-once guarantee + automatic failover at cost of availability and coordination overhead.
```

**Pros:**
- ✅ Simpler (no external registry)
- ✅ Lower latency (no token acquisition)
- ✅ No single point of failure

**Cons:**
- ❌ Client must handle conflicts manually
- ❌ No clear ownership (anyone can try to write)
- ❌ Higher contention under load
- ❌ Lost work if conflict detected after editing

**When to Use:**
- Low contention scenarios
- Read-heavy workloads
- Simple conflict resolution (last write wins)


