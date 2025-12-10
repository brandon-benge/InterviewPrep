# Kafka Messaging Queue System Design

## Overview

> This document summarizes the architecture and data flow of a modern Apache Kafka deployment, including core components, operational semantics, and system behaviors. The design separates the **Data Plane** (message flow and storage) from the **Control Plane** (cluster coordination and metadata management).

---

## Key Components and Flow

### Data Plane (Topic Partitions & ISR)
- **Producers** append messages to partitioned topics.
- **Partitions** are replicated across brokers using **In-Sync Replicas (ISR)**.
- **Consumers** pull messages and track offsets.
- Delivery guarantees: at-least-once (default), exactly-once (when configured).

### Control Plane (Metadata, Coordination)
- Managed using **KRaft** (Kafka Raft mode) or legacy **ZooKeeper**.
- Handles broker registration, controller election, partition leadership, and metadata.

---

## Storage Model

- Log-structured storage: each partition is an append-only log segmented into files.
- Older segments are sealed and compressed.
- Enables fast sequential writes and efficient disk IO.

Kafka uses segmented logs to optimize disk usage, minimize latency during purging, and reduce the performance impact of large continuous files.

---

## Retention & Durability

- **Retention**: time-based, size-based, or log compaction.
- **Durability**: replication across brokers, committed on all ISR.
- **Raft consensus** for metadata in KRaft mode.

---

## Scalability & Partitioning

- Scales horizontally by partitioning topics across brokers.
- Controller dynamically reassigns partitions during broker changes or topic updates.

---

## Reliability & Scaling Patterns

### Topic, Broker, Producer, and Consumer Scaling

- **Topics**: Kafka scales topics by spreading them over many partitions. Each partition can be placed on a separate broker.
- **Producers**: Kafka supports multiple producers publishing to the same topic. With partitioning, producers can send large volumes of data in parallel.
- **Consumers**: Kafka scales consumers by allowing partitions to be divided across consumer instances in a group. Each partition is processed by only one consumer in a group at any time.
- **Brokers**: Brokers are added or removed easily. Kafka rebalances partition leadership and replication accordingly. Kafka attempts to distribute leaders and followers across different brokers for load balancing and fault tolerance.

### Fault Tolerance & High Availability

- **Broker Failures**: Detected by ZooKeeper (or Raft in KRaft mode), with partition replicas on other brokers taking over.
- **Partition Leader Failures**: New leaders are elected automatically from in-sync replicas.
- **Controller Failures**: ZooKeeper (or Raft) detects failure and initiates a new controller election.
- **ZooKeeper**: Stores critical metadata and replicates it. Kafka recovers the metadata when ZooKeeper restarts.
- **Partition Replication**: Each partition has a leader and multiple follower replicas to ensure availability.

### Delivery Guarantees

- **Producer to Broker**:
  1. *Async*: No acknowledgment required.
  2. *Leader Acknowledgment*: Wait for leader to commit.
  3. *Leader + Quorum Acknowledgment*: Wait for leader and all in-sync replicas to commit.
- **Broker to Consumer**:
  - *At-most-once*: Possible message loss.
  - *At-least-once*: Possible duplication.
  - *Exactly-once*: No loss, no duplication.

### Consistency & Durability

- **High-Water Mark**: Brokers expose only messages that are replicated to the full ISR set, ensuring consistent reads.
- **Durability**: Messages are persisted to disk and replicated across brokers.

### Throughput and Consumer Scaling

- **Consumer Groups**: Enable high throughput by allowing parallel reads from partitions. Each consumer in a group gets assigned partitions exclusively.
- **Failover**: If a consumer dies, remaining consumers in the group are rebalanced to handle unassigned partitions.

### Throttling

- Kafka applies byte-rate quotas per client-ID. If a client exceeds its quota, the broker delays responses to throttle throughput.

### Broker Failover

- If a broker dies, Kafka redistributes partition leadership to other brokers in the cluster to maintain service availability.
---

## Flow Summary

1. Producer sends messages to a topic partition.
2. Broker leader appends to log and replicates to ISR followers.
3. Consumer fetches and commits offsets.
4. KRaft controller manages metadata and coordination.

---

## System Design Considerations

- **Per-Partition Ordering**: Kafka preserves message ordering **only within each partition**, not across partitions within a topic.
- **Broker Storage Boundaries**: Each partition replica resides fully on a single broker. Kafka does not support splitting a single partition across multiple brokers.
- **Broker Leadership**: A single broker may serve as the leader for multiple partitions across different topics.
- **High-Water Mark (HWM)**: Kafka brokers track the highest offset that all in-sync replicas (ISR) have acknowledged. Consumers only see data up to this high-water mark to ensure durability.
- **Split-Brain Prevention**: To avoid multiple active controllers (split-brain), Kafka uses a monotonically increasing *epoch number*. The controller with the highest epoch is considered valid. This epoch is persisted in ZooKeeper in legacy deployments.

---

## Architecture Diagram

> ![Kafka Architecture](./kafka.excalidraw.png)

> You can edit this diagram by uploading the PNG to [Excalidraw](https://excalidraw.com).
