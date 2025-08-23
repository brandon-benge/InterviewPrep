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
  - **Implementation:** JWT tokens, client-side storage, external session stores (Redis)
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
