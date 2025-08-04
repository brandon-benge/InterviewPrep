# System Design Approach and Key Questions

This document outlines a structured approach and key questions to consider when tackling system design interviews. Use this as a checklist and guide to demonstrate clear, methodical thinking during interviews.

---

## 🧭 System Design Approach

This structured approach helps you systematically tackle system design interviews. For each step, **clarify requirements early** by asking probing questions (interviewers often leave details vague intentionally), **prioritize** critical vs. nice-to-have features, **discuss trade-offs explicitly** to show architectural thinking, **use real-world examples** from your experience, **maintain balance** between functional and non-functional aspects, and **start simple then iterate** to show logical progression.

### 🎯 Functional Requirements & Core Design

These aspects focus on **what** the system needs to do and **how** it's structured to deliver core functionality.

1. **Clarify Functional Requirements**
   - *Summary:* Understand the core problem, user needs, and what success looks like. This ensures you solve the right problem and avoid wasted effort. **Interview Strategy:** Interviewers often leave requirements vague intentionally to see if you'll probe for critical details.
   - What is the core problem to solve?
   - What specific features and capabilities must the system provide?
   - Who are the users and what are their expectations?
   - What are the primary use cases and user workflows?
   - **Example Probing Questions:**
     - "What's the expected scale? Are we talking about 1K, 1M, or 1B users?"
     - "What are the latency requirements? Is 100ms acceptable or do we need sub-10ms?"
     - "Are there any compliance requirements like GDPR, HIPAA, or PCI?"

2. **High-Level Architecture**
   - *Summary:* Sketch the main system components and their interactions. This provides a roadmap for deeper design and highlights integration points. **Interview Strategy:** Start simple, then iterate. Discuss trade-offs explicitly for each major decision.
   - What are the main components and their responsibilities?
   - How do components interact (APIs, protocols, data flow)?
   - What are the key interfaces and contracts between components?
   - **Trade-off Examples:**
     - "By using a microservices architecture, we get better scalability but increase operational complexity"
     - "A monolithic approach is simpler to start with but may limit future scaling options"
   - **Real-world Reference:** "This is similar to how Netflix structures their services..." or "In my previous project, we faced a similar challenge..."

3. **Data Modeling & Storage**
   - *Summary:* Define what data is stored, how it is structured, and where it lives. Good data modeling is foundational for performance and scalability.
   - What data needs to be stored and retrieved?
   - Which databases or storage systems are appropriate?
   - How will data be partitioned, indexed, and cached?
   - What are the data relationships and access patterns?

4. **User Experience & Interfaces**
   - *Summary:* Consider the end-user's perspective, including user journeys, error handling, and interface design.
   - What is the expected user journey and workflow?
   - How will errors and edge cases be handled gracefully?
   - What APIs or interfaces need to be exposed?
   - How will different client types (web, mobile, API) be supported?

5. **Evolution & Extensibility**
   - *Summary:* Design for change. Make sure the system can adapt to new requirements, scale, and technology shifts.
   - How will the system adapt to new requirements or scale?
   - What is the plan for future improvements and feature additions?
   - How will backward compatibility be maintained?

### ⚡ Non-Functional Requirements & Quality Attributes

These aspects focus on **how well** the system performs and operates under various conditions.

6. **Define Constraints & Assumptions**
   - *Summary:* Identify boundaries and limitations early (scale, latency, compliance, cost). Make explicit any assumptions to avoid surprises later. **Interview Strategy:** Work with the interviewer to prioritize requirements - not all are equally important for system success.
   - What are the scale, latency, and availability targets?
   - Any specific technology, compliance, or cost constraints?
   - What can be assumed about the environment?
   - What are the resource limitations (budget, time, team size)?
   - **Prioritization Questions:**
     - "What's more important: consistency or availability during network partitions?"
     - "Which features are critical for MVP vs. nice-to-have for v2?"
     - "What would break the user experience vs. what would just slow it down?"

7. **Performance & Scalability**
   - *Summary:* Plan for growth and ensure the system meets speed requirements. Consider how the system will handle increased load and maintain responsiveness.
   - What are the latency and throughput requirements?
   - How will the system handle increased load (horizontal vs vertical scaling)?
   - Where are the likely bottlenecks and how will they be addressed?
   - How will you use caching, batching, or parallelism?

8. **Reliability & Availability**
   - *Summary:* Ensure the system stays operational and recovers gracefully from failures.
   - What are the uptime requirements (99.9%, 99.99%, etc.)?
   - What are the strategies for failover, redundancy, and disaster recovery?
   - How will the system handle partial failures and degraded modes?
   - What backup and recovery procedures are needed?

9. **Consistency & Data Integrity**
   - *Summary:* Decide how the system balances up-to-date data with always-on service. Choose the right consistency model for your use case.
   - What consistency model is required (strong, eventual, tunable)?
   - How will data integrity be maintained across distributed components?
   - What are the ACID requirements for transactions?
   - How will concurrent access and race conditions be handled?

10. **User Experience**
    - *Summary:* Consider the end-user’s perspective, including latency, error handling, and graceful degradation.
    - What is the expected user journey?
    - How will errors and downtime be communicated?
    - How will you ensure a responsive and reliable experience?

11. **Monitoring & Observability**
    - *Summary:* Ensure the system is observable and maintainable. Plan for metrics, alerting, and operational readiness.
    - What metrics and alerts will be tracked?
    - How will the system be updated and maintained?
    - What is the plan for incident response and troubleshooting?
    - What logging, tracing, and monitoring tools are needed?

### 🔄 **Interview Balance Check**
Throughout the interview, regularly ensure you're maintaining balance:
- ✅ Have I covered the core user flows? (Functional)
- ✅ Have I addressed scalability and performance? (Non-functional)  
- ✅ Have I considered failure scenarios? (Non-functional)
- ✅ Have I thought about the operational aspects? (Non-functional)
- ✅ Have I discussed trade-offs for major decisions?
- ✅ Have I referenced real-world examples or past experience?

---

## 🔧 Essential System Design Components

These are fundamental building blocks you should understand and consider when designing systems:

### **Data Storage & Management**

**SQL vs NoSQL Databases**
- **SQL (Relational):** ACID compliance, complex queries, structured data, strong consistency
  - Use when: Complex relationships, transactions, strong consistency required
  - Examples: PostgreSQL, MySQL, Oracle
- **NoSQL:** Horizontal scaling, flexible schema, eventual consistency, high performance
  - Document: MongoDB, CouchDB (JSON-like documents)
  - Key-Value: Redis, DynamoDB (simple key-value pairs)
  - Column-Family: Cassandra, HBase (wide column storage)
  - Graph: Neo4j, Amazon Neptune (relationships and connections)

**Data Partitioning (Sharding)**

*Partitioning Types (How data is split):*
- **Horizontal Partitioning:** Split rows across multiple databases
- **Vertical Partitioning:** Split columns/tables across databases
- **Functional Partitioning:** Split by feature/service boundaries - data is partitioned based on the functionality or business domain rather than data characteristics. Each partition contains all data related to a specific feature or service.
  - Example: An e-commerce platform might have separate databases for user management, product catalog, order processing, and payment processing. Each service owns its data completely.
  - Benefits: Clear ownership, easier to scale individual features, supports microservices architecture
  - Use cases: Large applications with distinct business domains, microservices architectures, teams organized by feature
- **Hybrid Partitioning:** Combines both horizontal and vertical partitioning techniques to partition data into multiple shards. This technique can help optimize performance by distributing the data evenly across multiple servers, while also minimizing the amount of data that needs to be scanned.
  - Example: An e-commerce website might partition the customer table horizontally based on geographic location, then partition each shard vertically based on data type. When a customer logs in, the query can be directed to the appropriate shard, minimizing data scanning while enabling parallel processing across different database servers.

*Partitioning Strategies/Techniques:*
- **Key/Hash-based Partitioning:** Apply a hash function to key attributes to determine partition number. For example, with 100 DB servers and numeric IDs, use 'ID % 100' to get the server number. Ensures uniform data allocation but fixes the total number of servers since adding new servers requires changing the hash function and redistributing data. Consistent Hashing solves this problem.
- **List Partitioning:** Each partition is assigned a list of values. When inserting a new record, determine which partition contains the key and store it there. Example: All users from Iceland, Norway, Sweden, Finland, or Denmark stored in a Nordic countries partition.
- **Round-robin Partitioning:** Very simple strategy ensuring uniform data distribution. With 'n' partitions, the 'i' tuple is assigned to partition (i mod n).
- **Composite Partitioning:** Combines multiple partitioning schemes to create a new approach. Example: Apply list partitioning first, then hash-based partitioning. Consistent hashing can be considered a composite of hash and list partitioning where hash reduces key-space to a listable size.
- **Consistent Hashing:** Distribute data evenly, minimize reshuffling when nodes added/removed

**Indexes**

*Index Types:*
- **Primary Index:** Clustered index on primary key
- **Secondary Index:** Non-clustered indexes for faster queries
- **Composite Index:** Multi-column indexes for complex queries

*Trade-offs:*
- **Benefits:** Faster reads, improved query performance
- **Costs:** Slower writes, additional storage overhead, maintenance complexity

**Replication**
- **Master-Slave:** One write node, multiple read replicas
- **Master-Master:** Multiple write nodes, conflict resolution needed
- **Synchronous:** Strong consistency, higher latency
- **Asynchronous:** Better performance, eventual consistency

### **Performance & Scalability**

**Caching**

- **Types of Caching:**
  - **Client-side:** Browser cache, mobile app cache - reduces server load and improves user experience
  - **DNS:** Cache DNS lookups to reduce resolution time and improve initial connection speed
  - **CDN (Content Delivery Network):** Geographic distribution for static content, reduces latency through edge locations
  - **Server-side:** Web server caches (Nginx, Apache) for static/dynamic content, reduces backend processing load
  - **Application-level:** In-memory cache (Redis, Memcached) for fast access to frequently used data
  - **Database-level:** Query result caching to reduce database query execution time
  - **Disk:** Operating system and database disk caches to improve I/O performance

- **Cache Invalidation Methods:**
  - **Time-based (TTL):** Expire cache entries after a set time period
  - **Event-based:** Invalidate when underlying data changes
  - **Manual/Explicit:** Purge specific objects/URLs or clear cache by application logic
  - **Pattern-based (Ban):** Invalidate cached content based on criteria (URL patterns, headers)
  - **Refresh:** Fetch latest content from origin server, update cached version
  - **Dependency-based:** Invalidate when related data changes
  - **Stale-while-revalidate:** Serve stale content immediately while updating in background

- **Cache Invalidation Schemes:**
  - **Cache-aside (Lazy Loading):** Application manages cache, loads on cache miss
  - **Write-through:** Write to cache and database simultaneously
  - **Write-around:** Write directly to database, bypass cache (good for write-heavy workloads)
  - **Write-behind (Write-back):** Write to cache immediately, database asynchronously
  - **Refresh-ahead:** Proactively refresh cache before expiration

- **Cache Read Strategies:**
  - **Read-through Cache:** Cache retrieves data from data store on cache miss, updates itself, and returns data to application. Cache handles all data retrieval logic.
  - **Read-aside (Cache-aside/Lazy Loading):** Application checks cache first; on cache miss, application retrieves from data store, updates cache, then uses data. Application controls caching logic.
  - **Cache-first:** Check cache first, fallback to database on miss (general pattern)
  - **Database-first:** Always read from database, update cache (for critical consistency)
  - **Cache-only:** Only read from cache (for non-critical data)

- **Cache Eviction Policies:**
  - **FIFO (First In, First Out):** Evicts the first block accessed without regard to access frequency
  - **LIFO (Last In, First Out):** Evicts the most recently accessed block without regard to access frequency
  - **LRU (Least Recently Used):** Discards the least recently used items first
  - **MRU (Most Recently Used):** Discards the most recently used items first (opposite of LRU)
  - **LFU (Least Frequently Used):** Counts access frequency, discards least frequently used items
  - **Random Replacement (RR):** Randomly selects and discards items when space is needed

**Load Balancing**
- **Layer 4 (Transport):** Routes based on IP and port
- **Layer 7 (Application):** Routes based on content (HTTP headers, URLs)
- **Algorithms:** Round-robin, least connections, weighted, IP hash
- **Types:** Hardware vs software, active-passive vs active-active

**Proxies**
- **Forward Proxy:** Client-side proxy (corporate firewalls, caching)
- **Reverse Proxy:** Server-side proxy (load balancing, SSL termination)
- **Examples:** Nginx, HAProxy, CloudFlare

### **Communication & Processing**

**Queues & Message Systems**
- **Point-to-Point:** Direct queue between producer and consumer
- **Publish-Subscribe:** Broadcast to multiple subscribers
- **Message Brokers:** Apache Kafka, RabbitMQ, Amazon SQS
- **Use Cases:** Asynchronous processing, decoupling services, event streaming

**Consistent Hashing**
- **Problem:** Minimize data movement when nodes are added/removed
- **Solution:** Hash function maps data to points on a circle
- **Benefits:** Only K/n keys need to be remapped (K=keys, n=nodes)
- **Used by:** DynamoDB, Cassandra, Memcached clusters

---

## ⚖️ Common Trade-offs in System Design

When designing systems, you will often need to balance competing priorities. Below are some of the most common trade-offs, each with a summary, key considerations, and guiding questions:

### 1. Easy-to-Build APIs vs. Long-Term APIs
- **Summary:** Rapidly built APIs speed up early development but may introduce technical debt and backward compatibility issues. Long-term APIs require more upfront design but are stable and extensible.
- **Trade-off:** Short-term velocity vs. long-term maintainability and ecosystem trust.
- **Questions to Ask:**
  - Who are the consumers (internal, external, third-party)?
  - How likely is the API to change in the next 6–12 months?
  - Do we need versioning from the start?
  - What backward compatibility guarantees are needed?
  - Are we building an MVP or a long-term foundation?

### 2. UI Complexity vs. Server Complexity
- **Summary:** Placing logic on the server centralizes control and security, while client-side logic can improve responsiveness and offload server work.
- **Trade-off:** Developer maintainability and centralization vs. better UX responsiveness and reduced server load.
- **Questions to Ask:**
  - What are the capabilities of the frontend vs. backend teams?
  - Are clients resource-constrained (e.g., mobile devices)?
  - How frequently will the logic change?
  - Can the client update easily, or is it distributed?
  - Is the logic sensitive (e.g., security/validation)?
  - Are multiple clients consuming this logic (web, mobile)?

### 3. Performance vs. Scalability
- **Summary:** Performance focuses on speed and efficiency for current loads; scalability ensures the system can grow with demand.
- **Trade-off:** Fast execution under limited load vs. system capacity for future growth.
- **Questions to Ask:**
  - What are current performance requirements?
  - What’s the expected growth in users or data volume?
  - What are the most performance-sensitive parts?
  - Do we need to scale horizontally or vertically?
  - Are we optimizing for time-to-market or long-term robustness?
  - What is our tolerance for cost in achieving performance?

### 4. Latency vs. Throughput
- **Summary:** Latency is about minimizing delay for individual operations (important for real-time systems). Throughput is about maximizing the number of operations over time (important for batch/high-volume workloads).
- **Trade-off:** Responsiveness per operation vs. total processing capacity.
- **Questions to Ask:**
  - Is this a user-facing or backend system?
  - What is the maximum acceptable latency per request?
  - What’s the expected request or data volume?
  - Are we streaming, batching, or queuing data?
  - What are the business/user impacts of delay?
  - Do we need real-time guarantees?

### 5. CAP Theorem
- **Summary:** In the presence of a network partition, you must choose between Consistency and Availability.
- **Trade-off:** Consistency vs. Availability (Partition Tolerance is required in distributed systems).
- **See:** [CAP Theorem](../devops/cross-region-replication/senario.md#-cap-theorem)

### 6. PACELC Theorem
- **Summary:** Extends CAP by considering trade-offs between Consistency and Latency when there is no partition.
- **Trade-off:**
  - During Partition: Consistency vs. Availability
  - Else: Consistency vs. Latency
- **See:** [PACELC Theorem](../devops/cross-region-replication/senario.md#-pacelc-theorem)

Be prepared to explain which trade-offs you are making and why, based on the problem context and requirements.

