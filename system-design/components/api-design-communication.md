# API Design & Communication Patterns

This document covers API design patterns and communication strategies for system design.

## Components

### API Design Patterns

- **RESTful APIs**
  - **Resource-oriented, HTTP methods (GET, POST, PUT, DELETE), stateless, cacheable**
  - Standard HTTP status codes and methods
  - Clear resource-based URL structure
  - Stateless communication

- **RPC (Remote Procedure Call)**
  - **Function-oriented, flexible protocols, efficient for complex operations**
  - Direct function call semantics
  - Can use various protocols (HTTP, binary, gRPC)
  - More efficient for complex operations

- **GraphQL**
  - **Query language allowing clients to request specific data, reduces over-fetching**
  - Single endpoint for all operations
  - Client-specified data requirements
  - Strongly typed schema

- **Webhook APIs**
  - **Event-driven, server pushes notifications to client endpoints**
  - Push-based notifications
  - Event-driven architecture
  - Requires public client endpoints

### API Versioning Strategies

- **URL Versioning**
  - `/api/v1/users` vs `/api/v2/users`
  - Clear and explicit versioning
  - Easy to implement and understand
  - Can lead to URL proliferation

- **Header Versioning**
  - `Accept: application/vnd.api+json;version=1`
  - Cleaner URLs
  - Version information in HTTP headers
  - More complex client implementation

- **Query Parameter**
  - `/api/users?version=1`
- Simple to implement
  - Easy to test different versions
  - Can clutter query parameters

- **Content Negotiation**
  - Different response formats based on Accept headers
  - Flexible content delivery
  - Leverages HTTP standards
  - More complex server logic

### Real-Time Communication Strategies

- **Traditional HTTP Protocol**
  - In the standard request/response model, the client opens a connection and sends a request to the server.
  - The server processes the request, generates a response, and sends it back to the client.
  - Once the response is delivered, the connection is typically closed.
  - This model is simple, stateless, and widely supported, but it is not designed for real-time updates since each request is independent and must be initiated by the client.

- **Polling**
  - Polling is the simplest real-time communication strategy where the client periodically sends requests to the server at fixed intervals to check for new data or updates.
  - This approach is easy to implement and works with any HTTP server, but can lead to unnecessary network traffic and increased latency since updates are only received at the next polling interval.
  - Polling is best suited for low-frequency or non-critical updates where real-time responsiveness is not required.

- **Long-Polling**
  - Long-Polling differs from traditional polling by keeping the client’s request open until new data is available or a timeout occurs, rather than repeatedly sending requests at fixed intervals. This approach is often called a “Hanging GET.”
  - When the client sends a request, the server holds the connection open and only responds when there is new data or after a timeout period. After receiving a response, the client immediately sends another request to maintain the connection.
  - This lifecycle reduces unnecessary network traffic compared to frequent polling but requires the client to handle reconnections in case of network interruptions or timeouts.

- **WebSockets**
  - WebSockets begin with an HTTP handshake that upgrades the connection to a persistent TCP connection, allowing full-duplex bi-directional communication between client and server.
  - Once established, this connection remains open, enabling low-latency, real-time data transfer with reduced overhead compared to repeatedly opening and closing HTTP connections.
  - This persistent connection supports simultaneous sending and receiving of messages, making it ideal for interactive applications requiring instant updates.

- **Webhooks** are user-defined HTTP callbacks that allow one system to notify another system about events in real time by sending an HTTP POST request to a specified URL.
- They are commonly used for server-to-server communication, such as notifying external services about status changes, payment events, or new data availability.
- Webhooks are event-driven, push-based, and require the receiving endpoint to be publicly accessible and able to handle incoming requests.
- **Trade-offs:** Webhooks rely on the availability and reliability of the receiving server, require secure endpoint management (authentication, validation), and must be idempotent to handle retries or duplicate notifications.
- **Examples:** GitHub webhooks for repository events, Stripe webhooks for payment updates, Slack webhooks for message posting.

- **Server-Sent Events (SSE)**
  - SSE establishes a persistent, unidirectional connection from the server to the client, allowing the server to push real-time updates as text/event-stream data.
  - This connection remains open, and the client listens for incoming messages, making SSE suitable for live feeds or notifications where only server-to-client communication is needed.
  - Since SSE is unidirectional, any client-to-server communication must occur through a separate channel, such as standard HTTP requests or WebSockets.

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

### Easy-to-Build APIs vs. Long-Term APIs
- **Summary:** Rapidly built APIs speed up early development but may introduce technical debt and backward compatibility issues. Long-term APIs require more upfront design but are stable and extensible.
- **Trade-off:** Short-term velocity vs. long-term maintainability and ecosystem trust.
- **Questions to Ask:**
  - Who are the consumers (internal, external, third-party)?
  - How likely is the API to change in the next 6–12 months?
  - Do we need versioning from the start?
  - What backward compatibility guarantees are needed?
  - Are we building an MVP or a long-term foundation?

### REST vs. RPC (Remote Procedure Call)
- **Summary:** REST (Representational State Transfer) treats system interactions as operations on resources using standard HTTP methods, while RPC (Remote Procedure Call) treats system interactions as function calls that execute remotely. Each approach has different strengths for API design and system integration.
- **Trade-off:** Resource-oriented simplicity and HTTP compatibility vs. action-oriented flexibility and performance.
- **API Comparison:**
  - **REST:** Resource-based URLs, standard HTTP methods (GET, POST, PUT, DELETE), stateless, cacheable, but can be verbose for complex operations and may require multiple round-trips
  - **RPC:** Function-based calls, flexible protocols (HTTP, binary), efficient for complex operations, but tighter coupling, less cacheable, and protocol-dependent tooling
  - **Hybrid Approach:** Use REST for CRUD operations and public APIs, RPC for internal services requiring high performance or complex operations
- **Questions to Ask:**
  - Are you building public APIs or internal service communication?
  - Do your operations map naturally to CRUD on resources?
  - What are your performance and latency requirements?
  - How important is HTTP compatibility and caching?
  - Do you need complex, multi-step operations?
  - What's your team's familiarity with each approach?
  - Are you building for web clients or diverse client types?
  - How important is loose coupling vs. performance optimization?

### Long-Polling vs. WebSockets vs. Server-Sent Events
- **Summary:** These are techniques for real-time communication between clients and servers, each with different capabilities and trade-offs.
- **Long-Polling:**
  - Client sends a request and the server holds the connection open until new data is available.
  - Simple to implement over HTTP.
  - Higher latency and overhead compared to other methods.
- **WebSockets:**
  - Full-duplex communication channel over a single TCP connection.
  - Low latency, bi-directional communication.
  - More complex to implement and maintain.
- **Server-Sent Events (SSE):**
  - Unidirectional communication from server to client.
  - Uses HTTP and EventSource API in browsers.
  - Simpler than WebSockets but only supports server-to-client messages.
- **Trade-offs:**
  - Choose Long-Polling for compatibility and simplicity.
  - Choose WebSockets for interactive, low-latency, bi-directional communication.
  - Choose SSE for simpler, uni-directional real-time updates.
