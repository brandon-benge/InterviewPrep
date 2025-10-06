# System Design Approach and Key Questions

This document outlines a structured approach and key questions to consider when tackling system design interviews. Use this as a checklist and guide to demonstrate clear, methodical thinking during interviews.

---

## Step-by-Step Approach to Solve Multiple Design Problems

> This systematic methodology offers a comprehensive framework for approaching any system design interview. Each phase builds upon previous work, ensuring thorough coverage while showcasing structured analytical thinking to interviewers.

### **Step 1: Requirements Clarification**
> Begin by thoroughly understanding the problem scope and objectives. System design problems are typically open-ended with multiple valid solutions, making early clarification essential for interview success. Focus on defining clear goals and boundaries within the available timeframe.

#### *Distinguish Between Functional and Non-Functional Requirements*
- **Functional Requirements:** Define *what* the system should do - the specific features, capabilities, and behaviors that users can directly interact with or observe. These are the core business logic and user-facing features.
  - Examples: User registration, posting content, searching data, sending notifications, processing payments
- **Non-Functional Requirements:** Define *how well* the system should perform - the quality attributes, constraints, and operational characteristics that affect user experience but aren't direct features.
  - Examples: Performance (latency, throughput), scalability, availability, security, consistency, maintainability

#### *Key Areas to Clarify*
- Core user workflows and feature scope
- Expected system scale and performance targets
- Data consistency and availability requirements
- Security and compliance constraints
- Integration and platform requirements

#### *Requirement Prioritization Strategy*
> Always prioritize both functional and non-functional requirements early in the discussion. **This establishes a clear contract between you and the interviewer** about what will be designed and what success looks like:

- **Functional Priorities:** Identify must-have features vs. nice-to-have features for MVP and future iterations
- **Non-Functional Priorities:** Determine critical quality attributes (e.g., is 99.9% availability more important than sub-100ms latency?)
  - **PACELC Theorem Application:** When network partitions occur, choose between Consistency and Availability (CAP). Even when the system is running normally (Else), choose between Latency and Consistency. This framework helps prioritize trade-offs systematically.
- **Business Impact Assessment:** Understand which requirements directly affect user experience and business success
- **Resource Constraints:** Consider time, budget, and team expertise when ranking requirements
- **Risk Evaluation:** Prioritize requirements that mitigate the highest business and technical risks

#### *Interview Contract Establishment*
> Use this phase to create mutual understanding and agreement with your interviewer on:

- **Scope boundaries:** What features and components will be included vs. excluded
- **Success criteria:** How the system's effectiveness will be measured
- **Design constraints:** Technical, business, and resource limitations that guide decisions
- **Assumption validation:** Confirm any assumptions about user behavior, traffic patterns, or infrastructure

### **Step 2: Capacity Planning and Scale Estimation**
> Calculate the expected system scale including user traffic, data storage requirements, and network bandwidth needs. These estimations inform subsequent architectural decisions around scaling strategies, data partitioning, and infrastructure planning.
>
> **Core Purpose:** Turn vague scope into concrete numbers that unlock richer trade-off discussions (e.g., which distribution / replication strategy, what caching layer depth, whether to shard now or later, how strict latency & consistency must be, where bottlenecks or hotspots will form).
>
> **Focus on Order-of-Magnitude, Not Perfection:** You need *directionally correct* estimates to justify or compare approaches—precision comes later. Get peak vs. average, growth rate, and worst-case bursts.
>

#### *Key Scale & Behavior Metrics to Derive / Validate*

- **Load & Traffic** – How much work the system must handle at runtime:
	- **Traffic QPS(Queries Per Second)/QPS(Queries Per Second)** Average & Max, Behavior under sudden surges or outages
	- **Payload Characteristics:** Characteristics of each request or object that affect design trade-offs
	  - **Size** — Bandwidth can bottleneck throughput under load.
	  - **Structure** — Understand Input data 
	  - **Type** — Data Types / Any large columns
	  - **Session information between requests** — Stateful vs Stateless. 
	- **Concurrency:** Simultaneous active users / sessions / connections
	- **Read/Write Mix:** Ratio of reads to writes (informs caching & DB design)
	- **Access Controls:** API Gateway - Authorization & Authentication, Rate Limiting
- **Data Characteristics** – Shape, behavior, and growth of data:
	- **Query Patterns:** Top N query patterns 
	- **Data Volume:** Total data stored
		- Average Character is 2 bytes
		- Auto increment column 2 bytes
		- Epoch seconds 4 bytes
		- Assume a graphdb message is 30 bytes for metadata
		- Average message is 1KB
		- Average a photo is 1MB compressed
		- Average thumbnail is is 50KB
		- On Average one minute of video needs 40MB 			
	- **Growth:** Rate of increase (e.g., GB/day, rows/day)
	- **Fanout Factors:** One input → many outputs (e.g., post → followers)
	- **Hotspot Risk:** Small subset of data accessed disproportionately
- **Reliability & Lifecycle** – Correctness, availability, durability requirements:
	- **Consistency:**  is eventual OK?
	- **Freshness Tolerance:** Acceptable staleness
	- **Retention & Lifecycle:** Required retention period and deletion triggers


#### *Example Interviewer Prompts / Questions to Elicit These*

- "What peak RPS should we design for? Is there a launch / spike scenario that's higher?"
- "Do reads dominate writes or vice versa? Rough percentage?"
- "What latency is acceptable for the core user action at p95? p99?"
- "How fresh must data be? Is a few seconds of eventual consistency OK for (feeds / counts / analytics)?"
- "What’s the expected average & max size of a (message / post / object)? Any large media edge cases?"
- "What's projected user or data growth over the next 6–12 months?"
- "Is traffic global and multi-region from day one, or can we start single-region?"
- "Do we anticipate high-fanout events (celebrity posts, broadcast notifications)? How often?"
- "Are there compliance or retention requirements (e.g., delete within X days, retain for Y years)?"
- "Can we degrade gracefully (slower analytics, partial feed) under extreme load, or is strict SLA required?"
- "Any batch or backfill jobs that could contend with live traffic (reindexing, model retraining exports)?"

#### *How You Use the Answers*

- Decide if a single primary DB + read replicas suffices or if early sharding / partitioning is warranted.
- Determine whether push (fanout-on-write) vs pull (fanout-on-read) patterns suit feed-like workloads.
- Justify a caching hierarchy (CDN → application cache → DB) based on read amplification & latency targets.
- Pick consistency model & replication (sync vs async) grounded in freshness tolerance.
- Highlight potential hotspots and propose key hashing, consistent hashing, or logical partition schemes.
- Identify where queueing / buffering is needed to smooth burst ingestion.


#### *Closing the Step*

Summarize the derived scale assumptions back to the interviewer ("Designing for ~12k peak RPS (80% reads), p95 < 200ms, feed fanout up to 500 recipients, tolerant of 2–3s staleness on counters")—then explicitly state how these numbers will shape upcoming design choices. This gives the interviewer a launchpad to steer you toward the most interesting trade-offs.

### **Step 3: API and Interface Design**
> Specify the expected system interfaces and contracts. This establishes clear boundaries and validates requirement understanding. Consider modern API design principles including RESTful patterns, pagination strategies, versioning approaches, and rate limiting mechanisms.

### **Step 4: Data Architecture and Modeling**
> Define the system's data entities, their interconnections, and information flow patterns. Address database technology selection (relational vs non-relational), storage infrastructure, and data lifecycle management considerations.

### **Step 5: System Architecture Overview**
> Create a high-level architectural diagram showing 5-6 primary system components. Include essential elements like traffic distribution, application logic, data persistence, content storage, performance optimization layers, and specialized services.

### **Step 6: Deep Dive Design Analysis**
> Examine 2-3 critical components in detail based on interviewer guidance. Compare alternative approaches with their respective advantages and limitations. Address data distribution strategies, performance optimization techniques, and edge case handling.

### **Step 7: Risk Assessment and Mitigation**
> Identify potential system vulnerabilities and propose mitigation strategies. Evaluate failure scenarios, redundancy requirements, operational monitoring needs, and performance optimization opportunities.

---


### Interview Balance Check
> Throughout the interview, regularly ensure you're maintaining balance:

- Have I covered the core user flows? (Functional)
- Have I addressed scalability and performance? (Non-functional)
- Have I considered failure scenarios? (Non-functional)
- Have I thought about the operational aspects? (Non-functional)
- Have I discussed trade-offs for major decisions?
- Have I referenced real-world examples or past experience?

---

## Components

![System Design Diagram](master_design_template.png)

---

## Essential System Design Components & Trade-offs

> These are fundamental building blocks you should understand and consider when designing systems. Each component category includes both the technical components and their key trade-offs to help you make informed architectural decisions.

### **Data Storage & Management**
#### *Components*
- [SQL vs NoSQL Databases](components/sql-vs-nosql.md)
- [Data Partitioning & Sharding](components/sharding.md)
- [Indexes](components/indexes.md)
- [Replication](components/replication.md)
- [Queues & Message Systems](components/event-driven-architecture.md)
- [Real-time Communication](components/real-time-communication.md)

#### *Key Trade-offs*
- **[SQL vs. NoSQL Databases](components/sql-vs-nosql.md)** - Structured integrity vs. flexible scalability  
- **[Strong vs. Eventual Consistency](components/consistency.md)** - Data accuracy vs. performance and availability
- **[Polling vs. Long-Polling vs. WebSockets vs. Webhooks](components/real-time-communication.md)** - Simplicity vs. real-time performance

### **Performance & Scalability**
#### *Components*
- [Caching strategies and types](components/caching.md)
- [Cache invalidation methods and schemes](components/caching.md)
- [Cache eviction policies](components/caching.md)
- [Performance vs Scalability fundamentals](components/caching.md)

#### *Key Trade-offs*
- **[Performance vs. Scalability](components/caching.md#performance-vs-scalability-fundamentals)** - Current speed vs. future growth capacity
- **[Latency vs. Throughput](components/caching.md#latency-vs-throughput)** - Individual operation speed vs. total processing capacity
- **[Read-Through vs Write-Through Cache](components/caching.md#read-through-vs-write-through-cache)** - Read optimization vs. write consistency
- **[Server-Side vs. Client-Side Caching](components/caching.md#server-side-caching-vs-client-side-caching)** - Centralized control vs. user experience
- **[CDN Usage vs. Direct Server Serving](components/caching.md#cdn-usage-vs-direct-server-serving)** - Global performance vs. simplicity

### **Network Infrastructure & Traffic Management**
#### *Components*
- [Load Balancing](components/load-balancing.md)
- [Proxies](components/proxies.md)
- [DNS](components/dns.md) & [Content Delivery Networks (CDNs)](components/cdn.md)
- [API Gateway](components/api-gateway.md)
- [Service Exposure Patterns](components/api-gateway.md)

#### *Key Trade-offs*
- **[Load Balancer vs. API Gateway](components/api-gateway.md#load-balancer-vs-api-gateway)** - Simple traffic distribution vs. comprehensive API management
- **[Direct Service Exposure vs. Gateway/Proxy Layer](components/api-gateway.md#direct-service-exposure-vs-gatewayproxy-layer)** - Performance vs. centralized control
- **[API Gateway vs. Reverse Proxy](components/api-gateway.md#api-gateway-vs-reverse-proxy)** - Application-aware features vs. high-performance traffic handling

### **API Design & Communication Patterns**
#### *Components*
- [REST API Design](components/rest-api.md)
- [gRPC API Design](components/grpc-api.md)
- [GraphQL API Design](components/graphql-api.md)
- [API Versioning](components/api-versioning.md)

#### *Key Trade-offs*
- **[Easy-to-Build APIs vs. Long-Term APIs](components/rest-api.md#easy-to-build-apis-vs-long-term-apis)** - Short-term velocity vs. long-term maintainability
- **[REST vs. RPC](components/rest-api.md#rest-vs-rpc-remote-procedure-call)** - Resource-oriented simplicity vs. action-oriented flexibility


### **Architecture Patterns & State Management**
#### *Components*
- [Stateful Architecture](components/stateful-architecture.md)
- [Stateless Architecture](components/stateless-architecture.md)
- [Layered Architecture](components/layered-architecture.md)

#### *Key Trade-offs*
- **[UI Complexity vs. Server Complexity](components/layered-architecture.md#ui-complexity-vs-server-complexity)** - Client responsiveness vs. server control
- **[Stateful vs. Stateless Architecture](components/stateful-architecture.md#stateful-vs-stateless-architecture)** - Rich UX vs. horizontal scalability


### **Data Processing Patterns**
#### *Components*
- [Batch Processing](components/batch-processing.md)
- [Stream Processing](components/stream-processing.md)
- [Lambda Architecture](components/lambda-architecture.md)

#### *Key Trade-offs*
- **[Batch Processing vs. Stream Processing](components/batch-processing.md#batch-processing-vs-stream-processing)** - High throughput efficiency vs. low latency responsiveness

---

### Trade-off Decision Framework

> When evaluating any trade-off, consistently ask:

1. **Current vs. Future Needs:** Are we optimizing for immediate requirements or long-term scalability?
2. **User Impact:** Which choice better serves the end-user experience and business objectives?
3. **Technical Constraints:** What are our team's capabilities, infrastructure limitations, and resource constraints?
4. **Risk Assessment:** What are the failure modes and mitigation strategies for each approach?
5. **Cost Analysis:** What are the development, operational, and maintenance costs over time?
6. **Flexibility:** Which option provides more adaptability for future changes and requirements?
