# Apache Cassandra – System Design Summary

## Summary

Apache Cassandra is a **distributed**, **decentralized**, **scalable**, and **highly available** NoSQL database. It was designed with the understanding that **software and hardware failures are inevitable**, and aims to maintain availability in the face of such failures.

### Key Features:
- **Peer-to-peer architecture**: All nodes are equal; there is no leader or follower.
- **Automatic data distribution**: Data is evenly partitioned across the cluster using **Consistent Hashing**.
- **Data replication**: Ensures fault tolerance and redundancy.
- **Ring topology**: Nodes are logically arranged in a ring for hashing and partitioning.
- **Tunable consistency**: Read and write operations can be configured for desired consistency levels.
- **Gossip protocol**: Used for inter-node communication.
- **Hybrid design**: Combines features from **Bigtable** (SSTables/MemTables) and **DynamoDB** (replication, partitioning).

---


## System Design Patterns in Cassandra

### 1. **Consistent Hashing**
Used to distribute data uniformly across nodes in a ring-like structure.

### 2. **Quorum-Based Writes**
Writes succeed if acknowledged by a quorum of replicas, improving consistency.

### 3. **Write-Ahead Log (Commit Log)**
Ensures durability by logging writes before memory operations.

### 4. **Segmented Commit Logs**
Split into smaller segments to minimize disk seeks. Logs are truncated after flushing to SSTables.

### 5. **Gossip Protocol**
Decentralized protocol used for propagating state information between nodes.

### 6. **Generation Number**
Nodes increment a generation number on restart. Included in gossip messages to differentiate old state from current.

### 7. **Phi Accrual Failure Detector**
Outputs a suspicion level based on heartbeat patterns, enabling adaptive failure detection.

### 8. **Bloom Filters**
Attached to each SSTable to quickly check if a key might exist, reducing unnecessary disk reads.
**On a read request, the Bloom filter helps avoid unnecessary disk I/O by indicating whether the requested data might exist in an SSTable.**

### 9. **Hinted Handoff**
Failed writes are temporarily stored and replayed to the target node when it becomes available again.

### 10. **Read Repair**
On reads, Cassandra checks for outdated replicas and updates them with the latest data.

---

**SSTables are stored on disk in two files**: an **index file** containing the Bloom filter and key-offset pairs, and a **data file** storing actual column data.

## Cassandra Characteristics

- **Distributed**: Operates across many machines seamlessly.
- **Decentralized**: No single point of failure; every node can serve reads/writes.
- **Scalable**: Add nodes without downtime or manual rebalancing; scales linearly.
- **Highly Available**: Data is available even during node or datacenter failures.
- **Fault-Tolerant**: Data replication provides strong reliability.
- **Tunable Consistency**: Adjustable per-query consistency settings.
- **Durable**: Data is written to disk persistently.
- **Eventually Consistent**: Prioritizes availability; eventual convergence of data.
- **Geo-Distributed**: Supports replication across multiple regions or clouds.

**Cassandra uses consistent hashing, and with the help of Vnodes, adding nodes to the cluster is quite easy.** When a new node is added, it receives many Vnodes from the existing nodes to maintain a balanced cluster.

**Each piece of data is replicated to multiple nodes to ensure high availability.** The **replication factor** determines how many nodes store each piece of data. For example, if the replication factor is 3, then **each row will be stored on three different nodes**, allowing the system to tolerate up to two node failures.

**Cassandra ensures durability by replicating data across multiple replicas and storing them on disk.**

**Cassandra favors availability and provides tunable consistency levels** for read and write operations.

**To achieve strong consistency, Cassandra follows the formula: R + W > RF**, where R = read replica count, W = write replica count, and RF = replication factor.

**Cassandra offers various consistency levels**: **One, Two, Three, Quorum, ALL, Local_quorum, Each_quorum, and Any** for writes; **all the same except Each_quorum** are available for reads.

---

## See Also
- [Sharding: Concepts & Trade-offs](../../components/sharding.md)
- Example: [Consistent Hashing Ring](../../../coding/consistent_hashing_ring/consistent_hashing_ring.md)
- [Replication: Concepts & Trade-offs](../../components/replication.md)
- [Consistency: Concepts & Trade-offs](../../components/consistency.md)
- [Caching: Concepts & Trade-offs](../../components/caching.md)
- Example: [LRU Cache Implementation](../../../coding/caching_kv_store/lru_cache.md)
- Example: [TTL Cache Implementation](../../../coding/caching_kv_store/ttl_cache.md)

- [Write-Ahead Log (WAL): Concepts & Trade-offs](../../components/wal.md)
 - [Raft Consensus Algorithm](../../components/raft.md)