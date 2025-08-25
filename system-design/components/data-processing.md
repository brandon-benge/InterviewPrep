# Data Processing Patterns

This document covers data processing patterns and strategies for system design.

## Components

### Batch Processing
- **Characteristics:** Process large volumes of data in scheduled chunks or batches
- **Benefits:** High throughput, cost-effective resource usage, simpler error handling and recovery
- **Challenges:** Higher latency, delayed insights, less responsive to real-time needs
- **Technologies:** Apache Spark, Hadoop MapReduce, AWS Batch, Google Dataflow
- **Use Cases:** ETL pipelines, data warehousing, financial reporting, log analysis

### Stream Processing
- **Characteristics:** Process data continuously as it arrives in real-time streams
- **Benefits:** Low latency, real-time insights, immediate responsiveness to events
- **Challenges:** Higher complexity, increased resource requirements, harder error handling
- **Technologies:** Apache Kafka Streams, Apache Storm, AWS Kinesis, Google Cloud Dataflow
- **Use Cases:** Real-time analytics, fraud detection, IoT data processing, live dashboards

### Lambda Architecture (Hybrid)
- **Approach:** Combines both batch and stream processing layers
- **Speed Layer:** Real-time processing for immediate results
- **Batch Layer:** Comprehensive processing for accuracy and completeness
- **Serving Layer:** Merges results from both layers for queries
- **Benefits:** Balances latency and throughput, fault tolerance, comprehensive data coverage

### Processing Pattern Comparison

- **When to Use Batch Processing**
  - Large volumes of data that don't require immediate processing
  - Cost optimization is important
  - Complex analytics and reporting
  - Historical data analysis
  - Scheduled operations (nightly reports, data backups)

- **When to Use Stream Processing**
  - Real-time decision making required
  - Low latency is critical
  - Continuous monitoring and alerting
  - Live user interactions
  - Time-sensitive business operations

- **When to Use Lambda Architecture**
  - Need both real-time and comprehensive analytics
  - High availability requirements
  - Complex data processing pipelines
  - Balance between speed and accuracy
  - Large-scale data processing with mixed requirements

## Related Trade-offs

### Batch Processing vs Stream Processing
- **Summary:** Batch processing handles large volumes of data in scheduled chunks, optimizing for throughput and cost efficiency. Stream processing handles data continuously as it arrives, optimizing for low latency and real-time insights.
- **Trade-off:** High throughput and resource efficiency vs. low latency and real-time responsiveness.
- **Processing Comparison:**
  - **Batch Processing:** High throughput, cost-effective, simpler error handling, but higher latency and delayed insights
  - **Stream Processing:** Low latency, real-time processing, immediate insights, but higher complexity and resource requirements
  - **Lambda Architecture (Hybrid):** Combines both batch and stream processing to balance throughput and latency
- **Questions to Ask:**
  - What's the acceptable delay between data arrival and processing results?
  - Is the data volume predictable or highly variable?
  - Are real-time insights critical for business decisions?
  - What's the cost tolerance for processing infrastructure?
  - How complex are the data transformations and analytics required?
  - Can the system tolerate occasional processing delays or must it be always responsive?

### Graph Data Stores

Graph databases are optimized for storing and traversing relationships between entities. They use a flexible schema of nodes and edges, which makes them ideal for use cases like social networks, recommendation systems, and access control.

#### Core Concepts

- **Node** — An entity in the graph (e.g., User, Post, Group).
- **Edge (Association)** — A directed relationship between two nodes (e.g., `UserA → likes → PostB`).
- **Association Type** — The label that defines the nature of the relationship (`friend`, `follows`, `member_of`, etc.).
- **Association Object** — Metadata tied to an edge (e.g., timestamps, permissions, weights).
- **Fan-out Query** — Retrieves all outbound edges for a node (e.g., posts a user liked).
- **Fan-in Query** — Retrieves all inbound edges to a node (e.g., who liked a post).
- **Traversal** — Walking through a graph to find related entities.

#### Example Schema

- **Nodes Table**
  - Fields: `node_id`, `node_type`, `metadata_json`

- **Edges Table**
  - Fields: `from_node_id`, `to_node_id`, `association_type`, `created_at`, `edge_metadata_json`

#### Example Graph Queries

- **Get all friends of a user:**
  ```sql
  SELECT to_node_id FROM edges
  WHERE from_node_id = 'user_123' AND association_type = 'friend';
  ```

- **Get users who liked a post:**
  ```sql
  SELECT from_node_id FROM edges
  WHERE to_node_id = 'post_456' AND association_type = 'like';
  ```

- **Get mutual friends between two users:**
  ```sql
  SELECT e1.to_node_id FROM edges e1
  INNER JOIN edges e2 ON e1.to_node_id = e2.to_node_id
  WHERE e1.from_node_id = 'user_123'
    AND e2.from_node_id = 'user_456'
    AND e1.association_type = 'friend'
    AND e2.association_type = 'friend';
  ```

#### Technologies

- **Purpose-built Graph DBs:** Neo4j, JanusGraph, Amazon Neptune
- **Graph over Key-Value or RDBMS:** TAO (Meta), custom sharded stores, RocksDB or MySQL-based edge stores

#### Use Cases

- Social networks (friend/follow graphs)
- Recommendations (users/products)
- Permission systems (RBAC/ABAC)
- Knowledge graphs and semantic linking

#### Questions to Ask

- What are the read/write query patterns (fanout, traversal depth)?
- How large or dense is the graph? Are there hotspots?
- Do you need strong consistency, or is eventual consistency acceptable?
- Can relationships be cached or precomputed?

### Trie for Typeahead

A trie (prefix tree) is a tree-like data structure that stores a dynamic set of strings, typically used to provide efficient retrieval of keys in dictionaries, autocomplete, and typeahead search.

#### Characteristics

- Each node represents a character of a string.
- Paths from the root to nodes represent prefixes of stored strings.
- Supports fast prefix queries, making it ideal for autocomplete.
- Can be augmented with frequency counts or weights for ranking suggestions.

#### Benefits

- Provides quick lookup for prefix-based search.
- Efficient in memory for common prefixes.
- Supports incremental search as users type.

#### Challenges

- Can be memory-intensive if not implemented with compression (e.g., radix trie).
- Requires careful design for large datasets to avoid performance degradation.

#### Use Cases

- Autocomplete and typeahead search in search engines or applications.
- Spell checking and correction.
- IP routing and longest prefix matching.

#### Example
Example Trie:

          root
            |
            c
            |
            a
           / \
          p   t
         / \
        t [ital]
       / \
    [ion][aio]


#### Questions to Ask

- What is the size and nature of the dataset (number of strings, average length)?
- How frequently does the dataset update (static vs dynamic)?
- Are prefix queries the primary operation?
- Is memory usage a critical constraint?
- Do you need to support ranking or scoring of suggestions?
