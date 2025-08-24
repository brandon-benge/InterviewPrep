# Architecture Patterns & State Management

This document covers architectural patterns and state management strategies for system design.

## Components

### Stateful vs Stateless Design

- **Stateful Architecture**
  - **Characteristics:** Server maintains client session information between requests
  - **Benefits:** Rich user experience, simpler application logic, faster interactions (no repeated auth)
  - **Challenges:** Sticky sessions required, harder horizontal scaling, session failure points
  - **Use Cases:** Gaming, real-time collaboration, complex multi-step workflows, enables complex workflows, faster user interactions (no repeated authentication/context)
  - **Implementation Details:**
    - In-memory sessions
    - Database-backed sessions
    - Sticky load balancing
  - **Data Stored in Session:**
    - user_id, roles, csrf, device info, workflow state, timestamps, etc.

- **Stateless Architecture**
  - **Characteristics:** Each request contains all necessary information, no server-side session storage
  - **Benefits:** Excellent horizontal scalability, fault tolerance, any server handles any request
  - **Challenges:** Larger request payloads, complex client logic, repeated authentication overhead
  - **Implementation:** JWT(JSON Web Token) tokens, client-side storage, external session stores (Redis)
  - **Implementation Details:**
    - JWT tokens
    - Client-side storage
    - External session stores (Redis)
    - Database lookups per request
  - **Use Cases:**
    - High horizontal scale
    - CDN edge auth
    - Mobile/web APIs
    - Event ingestion
  - **JWT How It Works:**
    - header.payload.signature
    - issuance
    - validation
    - revocation
    - short TTL/refresh
  - **When Redis Is Used:**
    - refresh token store
    - revocation lists
    - rate limiting
    - session concurrency limits
  - **Caveats/Best Practices:**
    - short TTL
    - no sensitive claims
    - key rotation
    - HttpOnly cookies
    - scoped tokens


### Feature Extraction

- **Stateful Embeddings**
  - **What:** Represent users or items as learned vectors (embeddings) that reflect behavior and preferences over time.
  - **How Extracted:** Stateful systems collect real-time interactions (clicks, likes, views) and process them through stream jobs (e.g., Flink, Kafka Streams) to update user/item state.
  - **Storage:** Embeddings are stored in vector stores (e.g., Redis, Faiss, Pinecone) or key-value stores keyed by user/item ID.
  - **Serving:** During ranking or recommendation, embeddings are fetched in real time using the session’s user ID and combined with item embeddings for scoring.
  - **Stateful Role:** The system maintains evolving user state (e.g., recent engagement patterns) that feeds into embedding retraining or real-time personalization.

### Client-Server Logic Distribution

- **Server-Side Logic (Thick Server, Thin Client)**
  - **Characteristics:** Business logic, validation, processing handled on server
  - **Benefits:** Centralized control, security, easier updates, consistent behavior across clients
  - **Challenges:** Higher server load, increased latency, requires network for all operations
  - **Use Cases:** Financial systems, enterprise applications, security-critical operations
  - **Examples:** Traditional web applications, SaaS platforms, banking systems

- **Client-Side Logic (Thick Client, Thin Server)**
  - **Characteristics:** Business logic, validation, processing handled on client
  - **Benefits:** Responsive UI, reduced server load, offline capability, better user experience
  - **Challenges:** Harder to update, potential security risks, inconsistent behavior across devices
  - **Use Cases:** Gaming, creative tools, offline-capable applications, mobile apps
  - **Examples:** Desktop applications, mobile games, offline-first PWAs, rich SPAs

- **Hybrid Approach**
  - **Strategy:** Distribute logic based on specific requirements and constraints
  - **Server-Side:** Security validation, business rules, data persistence, complex calculations
  - **Client-Side:** UI logic, input validation, caching, user interactions
  - **Examples:** Modern web applications, mobile apps with local caching, collaborative editors


## Related Trade-offs
- **Trade-off:** Developer maintainability and centralization vs. better UX responsiveness and reduced server load.
- **Questions to Ask:**
  - What are the capabilities of the frontend vs. backend teams?
  - Are clients resource-constrained (e.g., mobile devices)?
  - How frequently will the logic change?
  - Can the client update easily, or is it distributed?
  - Is the logic sensitive (e.g., security/validation)?
  - Are multiple clients consuming this logic (web, mobile)?


### UI Complexity vs. Server Complexity
- **Summary:** Placing logic on the server centralizes control and security, while client-side logic can improve responsiveness and offload server work.
- **Trade-off:** Control and security vs. responsiveness and scalability.
- **Questions to Ask:**
  - How responsive does the UI need to be?
  - Is the logic sensitive (e.g., security/validation)?
  - Are multiple clients consuming this logic (web, mobile)?

### Failure Modes & Resilience

- **Circuit Breakers**
  - **What:** Prevent services from calling a failing dependency repeatedly by short-circuiting requests.
  - **Benefits:** Avoids cascading failures, improves system stability, fails fast.
  - **How It Works:** Transitions through Closed → Open → Half-Open based on failure thresholds and recovery attempts.
  - **Use Cases:** Downstream service unavailability, dependency flakiness, rate-limited APIs.

- **Exponential Backoff**
  - **What:** Retry strategy where delay increases exponentially between attempts.
  - **Benefits:** Reduces retry storms, allows time for recovery.
  - **Best Practices:** Add jitter to prevent synchronized retries, limit max retries, apply to idempotent operations.

- **Backpressure**
  - **What:** Mechanism to signal upstream producers to slow down when overwhelmed.
  - **Benefits:** Prevents queue overflows, protects system memory and throughput.
  - **How It’s Implemented:** Queue thresholds, 429 responses, streaming control signals, request rejection.

- **Graceful Degradation**
  - **What:** Maintain partial functionality when full service is unavailable.
  - **Benefits:** Preserves core UX, prevents full outages, reduces support burden.
  - **Examples:** Fallback to cached data, omitting non-critical components, showing stale results.

- **Retry Logic**
  - **What:** Re-attempt operations that fail due to transient issues.
  - **Benefits:** Increases reliability for recoverable failures like timeouts or network glitches.
  - **Best Practices:** Use exponential backoff, limit retries, track retry metrics, avoid retrying non-idempotent actions.

- **Feature Flags**
  - **What:** Toggle features at runtime without code deployments.
  - **Benefits:** Enables safe rollouts, A/B testing, and instant rollback.
  - **Use Cases:** Gradual feature rollout, emergency disablement, experiment control.

- **Related Trade-offs**
  - **Trade-off:** Reliability vs. latency and system complexity.
  - **Questions to Ask:**
    - Are downstream services reliable or rate-limited?
    - Can failures be gracefully handled without full system outage?
    - Which features are critical to preserve under partial failure?
    - How can we monitor and test our failure handling mechanisms?
