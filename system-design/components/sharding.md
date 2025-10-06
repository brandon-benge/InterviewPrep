# Sharding

Sharding is the process of splitting data across multiple databases or servers to improve scalability and performance.

## Types
- **Horizontal Sharding:** Split rows across shards (most common)
- **Vertical Sharding:** Split tables/columns across shards
- **Directory-Based Sharding:** Use a lookup service to map keys to shards

## Trade-offs
- Increases scalability and write throughput
- Adds complexity for cross-shard queries and transactions
- Rebalancing shards can be operationally challenging

## Interview Q&A
- How do you choose a sharding key?
- What happens if a shard becomes a hotspot?
- How do you handle rebalancing and resharding?

## Architecture Diagram
```mermaid
graph TD
    Client --> Router[Shard Router]
    Router --> Shard1[Shard 1]
    Router --> Shard2[Shard 2]
    Router --> Shard3[Shard 3]
```
