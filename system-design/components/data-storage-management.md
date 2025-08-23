# Data Storage & Management

This document covers data storage modeling, engines, distribution, and consistency concepts for system design.

## Components

### SQL vs NoSQL Databases

- **SQL (Relational)**
	- ACID transactions, complex joins, strong consistency
	- Use for authoritative, financial, inventory, user/account data
	- Examples: PostgreSQL, MySQL, Oracle

- **NoSQL Families**
	- **Document:** MongoDB, CouchDB – evolving entity shapes
	- **Key-Value:** Redis, DynamoDB – hot path lookups, caching, session/state
	- **Column-Family:** Cassandra, HBase – wide sparse/time-series, write-heavy
	- **Graph:** Neo4j, Neptune – multi‑hop relationship traversals

| Criterion | Prefer SQL | Prefer NoSQL |
|-----------|------------|--------------|
| Relationships | Many joins / normalized | Simple aggregates / denormalized |
| Transactions | Multi-row ACID | Single-item atomicity |
| Query Flexibility | Ad‑hoc / reporting | Predictable key/path patterns |
| Schema Volatility | Stable/governed | Rapidly evolving |
| Scaling Emphasis | Strong consistency first | Early horizontal scale |
| Analytics | Run directly | Offload / pipelines |

#### *Heuristics*
- Default to SQL; add specialized NoSQL for latency or scale hot spots.
- \>=90% single-ID fetches & rare joins → document or key-value store.
- Large immutable blobs → object storage; keep pointer + metadata in SQL.

#### *Pitfalls*
- Replacing relational integrity in app code → drift & bugs.
- Over-normalizing documents → chatty multi-fetch patterns.
- Ignoring secondary index limits / hot partitions until late load testing.

#### *Polyglot Patterns*
- System of record (SQL) → emit events / build materialized views in NoSQL/search.
- Introduce a cache layer before attempting a full datastore rewrite.

#### *Interview Checks*
- Top N query patterns (shape + frequency + latency goal)?
- Cross-entity transaction requirement?
- Hot partition risk & mitigation?
- Analytics path (direct OLTP vs ETL pipeline)?

### Indexes

#### *Types*
- Primary (clustered), Secondary (non-clustered), Composite (leftmost prefix rule).

#### *Trade-offs*
- Faster selective reads vs slower writes + extra storage + maintenance.

#### *Guidelines*
- Index WHERE/JOIN/ORDER patterns; avoid low-cardinality single-column indexes; audit unused.

### Inverted Indexes

An inverted index is a data structure commonly used in search engines and text retrieval systems to map content, such as words or terms, to their locations in a set of documents. This enables efficient full-text search by quickly identifying documents containing specific terms.

| Aspect | Benefit | Trade-off |
|--------|---------|-----------|
| Query Speed | Fast full-text search and phrase queries | Additional storage overhead |
| Update Complexity | Efficient for read-heavy workloads | Slower writes due to index maintenance |
| Use Cases | Search engines, log analytics, recommendation systems | Not ideal for transactional workloads |

Example:
Example:

Documents:
- Doc1: "the cat sat"
- Doc2: "the dog barked"

Tokenized:
- Doc1 → [the, cat, sat]
- Doc2 → [the, dog, barked]

Inverted Index for "dog":

| Term | Doc ID | Positions | Term Frequency |
|------|--------|-----------|---------------|
| dog  |   2    |   [1]     |      1        |

Or as a Python-like structure:
```python
{
	"dog": [
		{"doc_id": 2, "positions": [1], "term_freq": 1}
	]
}
```

#### *Heuristics*
- Use inverted indexes when text search or multi-term queries are frequent.
- Combine with other indexes for hybrid query patterns.
- Monitor index size and update latency to avoid performance degradation.

#### *Pitfalls*
- High write amplification when indexing large volumes of data.
- Complexity in handling phrase queries and proximity searches.
- Potential stale results if index updates are asynchronous without proper synchronization.

### Partitioning (Sharding)

#### *Partition Types*
- Horizontal (rows), Vertical (columns/tables), Functional (service/domain), Hybrid (mix).

#### *Routing Strategies*
- Hash/Key, Range/List (geo/time/category), Round-Robin (rare), Composite, Consistent Hashing (virtual nodes).

#### *Checklist*
- Even key distribution, cross-shard joins minimized, rebalance plan, secondary index behavior known.

#### *Smells*
- One shard >60–70% traffic
- Frequent cross-shard fan-out queries

### Replication

#### *Topologies*
- Primary-Replica (leader/followers reads scale).
- Multi-Primary (conflict resolution: LWW, vector clocks, CRDTs).

#### *Timing*
- Synchronous (latency↑, consistency strong), Asynchronous (fast commit, lag window), Semi-Sync (middle ground).

### Consistency Models

- Strong: All reads see latest commit.
- Eventual: Converges; allow stale window.
- Hybrid: Core rows strong; derived data eventual.

#### *Theorems & Models*
- CAP (partition → choose C vs A), PACELC (else latency vs consistency), ACID vs BASE.

#### *Design Patterns*
- Read repair / hinted handoff
- Write-ahead log + deterministic replay
- Region-local synchronous + cross-region asynchronous replication

#### *Decision Prompts*
- Acceptable stale read window?
- Write durability vs latency priority?
- Ordering / causal consistency requirements?

### Storage Engines

- **LSM Trees:** Memtable + immutable SSTables; sequential writes; compaction controls read amp. Best: write-heavy, time-series, ingest.
- **B+ Trees:** In-place page updates; good point & range queries; best: mixed/transactional workloads needing ad‑hoc queries.

### Cassandra vs HDFS

#### *Simple Decision Cues*
- Serve live requests with predictable ms latency → **Cassandra**
- Store petabytes and run batch analytics → **HDFS**
- High write rate time-series with per-key retention → **Cassandra**
- Ad-hoc SQL over years of logs → **HDFS** (+ Hive/Spark)

#### *Common Hybrid*
- Ingest → land raw to HDFS/S3 (cheap, durable).
- Aggregate/feature compute in Spark, then publish hot aggregates to Cassandra for low-latency APIs/dashboards.

### Block vs File vs Object Storage

| Aspect | Block | File | Object |
|--------|-------|------|--------|
| Abstraction | Raw blocks | Hierarchical FS | Flat object namespace |
| Protocols | iSCSI, FC, NVMe | NFS, SMB, POSIX | HTTP/REST (S3, GCS) |
| Cloud Examples | EBS / Persistent Disk | EFS / Filestore / Azure Files | S3 / GCS / Azure Blob |
| Latency | Lowest | Moderate | Higher |
| Scale | Volume striping | Scale-out shares | Virtually unlimited |
| Concurrency | Single host (unless clustered) | Multi-host | Massive global |
| Metadata | Minimal | FS metadata | Custom key–value |
| Mutability | In-place | Byte-range writes | Whole-object PUT/version |
| Consistency | Strong per block | POSIX (varies) | Read-after-write new / eventual overwrite |
| Best For | DBs, low-latency I/O | Shared legacy apps | Media, logs, backups |
| Cost | Highest | Medium | Lowest |

#### *Heuristics (Storage Type Selection)*
- OLTP volumes → Block
- Shared application assets / lift & shift legacy → File
- Large unstructured / append-mostly (images, video, logs, ML artifacts) → Object
- Combine: SQL metadata row + blob in object storage (avoid table bloat)

#### *Pitfalls*
- Large blobs stored directly in RDBMS rows (cache / buffer pollution)
- Expecting directory semantics or atomic rename in object store (emulate via key prefixes)
- Overwrite races under eventual consistency (use versioning or etags)

### Queues & Streams

#### *Core Patterns*
- Point-to-Point Queue (work distribution)
- Publish / Subscribe (fan-out)
- Log-based Stream (append-only replayable log)

#### *Use Cases*
- Asynchronous processing & decoupling
- Burst smoothing / buffering
- Event sourcing & change data capture (CDC)
- Replay / audit trails / analytics fan-out

#### *Examples*
- Kafka, RabbitMQ, Amazon SQS/SNS, Google Pub/Sub, Redis Streams

#### *Design Prompts*
- Ordering scope (global vs per key)
- Delivery guarantees (at-most / at-least / exactly-once)
- Back-pressure visibility (consumer lag metrics)

### Real-Time & Event Delivery Patterns

#### *Options (Ascending Capability)*
- Polling
- Long-Polling
- Server-Sent Events (SSE)
- WebSockets
- Webhooks (server-to-server callbacks)

#### *Selection Guide*
- Sporadic, low criticality updates → Polling
- Simple near real-time, browser only → Long-Polling or SSE
- High-frequency bidirectional messaging → WebSockets
- Server notifying external integrators → Webhooks
- Firehose / continuous stream consumption → WebSockets or SSE

#### *Key Considerations*
- Connection limits (proxies, LB) – many idle sockets may pressure resources
- Ordering & retry semantics (webhooks must be idempotent)
- Authentication & token refresh strategy for long-lived channels

## Related Trade-offs

### SQL vs. NoSQL Databases
- **Summary:** SQL offers ACID + rich queries; NoSQL offers flexible schema + horizontal scale for targeted patterns.
- **Trade-off:** Integrity/complex querying vs flexible evolution & scale.
- **Questions:** Need multi-row transactions? Join complexity? Schema volatility? Horizontal scale urgency? Analytics path? Team expertise?

### Strong vs Eventual Consistency
- **Summary:** Strong simplifies correctness; eventual improves availability & performance with temporary staleness.
- **Trade-off:** Immediate accuracy vs latency/availability.
- **Questions:** Impact of stale reads? Required durability latency? Data categories needing strict ordering? Retry/idempotency strategy?

### Polling vs Long-Polling vs WebSockets vs Webhooks
- **Summary:** Increasing sophistication lowers latency & resource waste but raises complexity.
- **Trade-off:** Simplicity/reliability vs real-time performance & efficiency.
- **Questions:** Update frequency? Directionality? Connection persistence feasibility? Delivery guarantees? Scale of concurrent connections?

### High Availability vs "Always Available"
- **Summary:** High availability (HA) targets a quantified uptime (e.g., 99.95%) via redundancy & rapid recovery; "always available" (continuous availability) aims for zero perceived downtime even during failures & maintenance—far harder and costlier.
- **Key Metrics:** SLA/SLO uptime %, MTTR (repair), MTBF (between failures), RPO (data loss tolerance), RTO (restore time).
- **Approaches:**
	- HA: Active-passive failover, health checks, automated restart, redundancy per layer.
	- Continuous Availability: Active-active multi-region, rolling deploys, zero-downtime schema migrations, quorum writes, automatic traffic re-routing.
- **Design Levers:** Redundancy (N+1), isolation (blast radius), graceful degradation, circuit breakers, idempotent & replayable operations, blue/green or canary releases.
- **Pitfalls:** Single shared state (cache or primary DB) nullifies multi-instance app HA; coordinated failures due to identical config; backups untested (RTO/RPO theoretical); schema changes locking primary; assuming multi-AZ = multi-region DR.
- **Cost Curve:** Each extra "9" sharply increases complexity (operational tooling, observability, chaos testing).
- **Interview Prompts:** Target uptime? Acceptable RPO/RTO? Failure domains (process, node, AZ, region) & mitigation? Deployment strategy? Degraded mode behavior? How is failover tested & detected?

### Interview Checklist
- Dominant read/write patterns (shape, frequency, latency SLO).
- Consistency vs availability under partition (justify choice).
- Failure & recovery: node/region loss RTO/RPO.
- Hot partition risk & key design.
- Growth trajectory (data/QPS; working vs total set).
- Index cost vs read amplification observed.
- Backup & DR (snapshots, PITR, retention policy).
- Observability: replication lag, compaction/vacuum pressure, queue lag.
- Data lifecycle tiering (hot → warm → cold → archive).
