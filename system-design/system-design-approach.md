# System Design Approach and Key Questions

This document outlines a structured approach and key questions to consider when tackling system design interviews. Use this as a checklist and guide to demonstrate clear, methodical thinking during interviews.

---

## 🧭 System Design Approach

1. **Clarify Requirements**
   - *Summary:* Understand the core problem, user needs, and what success looks like. This ensures you solve the right problem and avoid wasted effort.
   - What is the core problem to solve?
   - What are the functional and non-functional requirements?
   - Who are the users and what are their expectations?

2. **Define Constraints & Assumptions**
   - *Summary:* Identify boundaries and limitations early (scale, latency, compliance, cost). Make explicit any assumptions to avoid surprises later.
   - What are the scale, latency, and availability targets?
   - Any specific technology, compliance, or cost constraints?
   - What can be assumed about the environment?

3. **High-Level Architecture**
   - *Summary:* Sketch the main system components and their interactions. This provides a roadmap for deeper design and highlights integration points.
   - What are the main components and their responsibilities?
   - How do components interact (APIs, protocols, data flow)?

4. **Data Modeling & Storage**
   - *Summary:* Define what data is stored, how it is structured, and where it lives. Good data modeling is foundational for performance and scalability.
   - What data needs to be stored and retrieved?
   - Which databases or storage systems are appropriate?
   - How will data be partitioned, indexed, and cached?

5. **Scalability & Reliability**
   - *Summary:* Plan for growth and resilience. Consider how the system will handle increased load and recover from failures.
   - How will the system handle increased load?
   - What are the strategies for failover, redundancy, and disaster recovery?

6. **Consistency & Availability**
   - *Summary:* Decide how the system balances up-to-date data with always-on service. Choose the right consistency model for your use case.
   - What consistency model is required (strong, eventual, tunable)?
   - How will the system remain available during failures?

7. **Performance Optimization**
   - *Summary:* Identify and address potential bottlenecks, latency issues, and resource constraints to ensure the system meets performance goals.
   - Where are the likely bottlenecks?
   - What are the latency and throughput requirements?
   - How will you use caching, batching, or parallelism?

8. **Security & Privacy**
   - *Summary:* Protect data and users by planning for authentication, authorization, encryption, and compliance from the start.
   - How is data protected in transit and at rest?
   - What authentication, authorization, and auditing are needed?
   - Are there privacy or regulatory requirements?

9. **Monitoring & Maintenance**
   - *Summary:* Ensure the system is observable and maintainable. Plan for metrics, alerting, and operational readiness.
   - What metrics and alerts will be tracked?
   - How will the system be updated and maintained?
   - What is the plan for incident response and troubleshooting?

10. **User Experience**
    - *Summary:* Consider the end-user’s perspective, including latency, error handling, and graceful degradation.
    - What is the expected user journey?
    - How will errors and downtime be communicated?
    - How will you ensure a responsive and reliable experience?

11. **Evolution & Extensibility**
    - *Summary:* Design for change. Make sure the system can adapt to new requirements, scale, and technology shifts.
    - How will the system adapt to new requirements or scale?
    - What is the plan for future improvements?

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

