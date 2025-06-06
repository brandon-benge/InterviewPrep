# Amazon Ads System

## Overview

Amazon Ads supports real-time bidding and ad delivery across Amazon properties such as Fire TV, IMDb, Alexa, and Amazon.com. This system enables targeting, auctioning, and creative rendering in under 100ms using a modular architecture with strong data compliance and ML-based personalization.

## Key Components

### User Device / Publisher
Initiates the ad request from Fire TV, Alexa, IMDb, or other Amazon-owned properties.

**Runtime Path**: ✅ Yes

### API Gateway / Front Door
The entry point for all ad requests. Performs validation, authentication, and routing. Usually implemented via AWS API Gateway or Lambda@Edge.

**Runtime Path**: ✅ Yes

### Ad Request Orchestrator
Enriches ad requests with user, geo, device, and consent data. Applies targeting rules and compliance filters.

**Runtime Path**: ✅ Yes

**Why It Matters**  
Acts as the central coordinator that determines what data is needed to make an ad decision, enforces compliance (e.g., GDPR/CCPA), and ensures fallback options exist if no bids are returned.

**Typical Technologies**  
- Language: Java, Go  
- Deployment: EKS or ECS  
- Data: Redis for fast lookups, DynamoDB for profiles  
- Integration: Kafka/S3 for logging, SageMaker endpoints for targeting segments

### Bid Request Engine
Converts enriched user and page context into OpenRTB (Open Real-Time Bidding) format and dispatches requests to multiple buyers (DSPs) in parallel. The engine generates standardized bid requests using the OpenRTB protocol to ensure compatibility with both internal and third-party DSPs. Amazon’s implementation may transmit these requests over HTTP or gRPC, and can include Amazon-specific extensions for internal optimization.

**Runtime Path**: ✅ Yes

**Why It Matters**  
The Bid Request Engine ensures every DSP receives a uniform, well-structured ad opportunity to evaluate. It handles eligibility filters, pricing thresholds, and compliance metadata. Its parallel dispatch ensures fair competition among bidders and maximizes auction yield.  
Responses from the DSPs are collected and forwarded to the Ad Auction Service, which evaluates them to determine the winning bid.


**Bid Format**  
The bid request is structured using the OpenRTB (Open Real-Time Bidding) protocol — a standardized, JSON-based specification widely adopted across the advertising industry. This ensures interoperability and fairness when communicating with DSPs. A typical OpenRTB request includes:

- `imp`: Impression object describing ad type, dimensions, placement ID, and bidfloor  
- `site` or `app`: Context of the impression (domain, page URL, or app details)  
- `device`: User-agent, IP address, operating system, device type, geo-location  
- `user`: Anonymized user ID, interest segments, and consent metadata  
- `regs`: Regulatory flags (e.g., GDPR, CCPA, COPPA compliance)

Amazon’s implementation adheres to OpenRTB structure but may extend it with proprietary fields or transmit over gRPC instead of HTTP. This “OpenRTB-like” model ensures compatibility with third-party DSPs while allowing internal optimization.

**Typical Technologies**  
- Language: Java, Rust  
- Protocols: OpenRTB over HTTP or gRPC  
- Queuing: Kafka or Kinesis for async routing  
- Routing: Load-balanced, multi-region outbound calls  
- Features: Supply filtering, campaign rule evaluation, compliance tagging

### Demand-Side Platforms (DSPs)
External or internal systems used by advertisers to receive bid requests and respond with price and creative. Each DSP evaluates targeting, calculates bids, and competes in the auction.

**Runtime Path**: ✅ Yes

**Why It Matters**  
DSPs are the buyers in the real-time auction. They bring advertiser intent into the system and determine whether an impression is monetized and at what value. These systems are not owned or controlled by Amazon. Therefore, the platform enforces strict validation: if a DSP response is malformed, arrives too late, or fails protocol or compliance checks, it is dropped and excluded from the auction.

**Typical Examples**
- Amazon DSP  
- Google DV360  
- The Trade Desk  
- MediaMath

### Ad Auction Service
Conducts second-price auctions or priority-based selection across eligible bids.

**Runtime Path**: ✅ Yes

**Why It Matters**  
The Ad Auction Service is responsible for evaluating all valid bid responses from DSPs and selecting the winning bid. It typically uses a second-price auction model, where the highest bidder wins but pays the price of the second-highest bid. This incentivizes truthful bidding. In cases where direct deals or priority campaigns exist, it may use a priority-based override or fixed-price logic instead.  
To complete this process, the service relies on filtered and pre-vetted bid inputs from the Bid Management Layer, which enforces eligibility rules and pacing logic using data derived from the Campaign Management System and Telemetry / Spend Tracking Systems. The Ad Auction Service itself does not directly interact with these systems; instead, it depends on the Bid Management Layer to supply bids that already adhere to campaign and pacing constraints, thereby maintaining ultra-low latency.  
The service also performs creative validation using metadata from the Creative Asset Store to ensure the selected creative is safe and renderable before declaring a winner.

**Typical Technologies**  
- Language: Java, Scala  
- Frameworks: Netty or Akka for low-latency processing  
- Storage: Redis for ephemeral state, DynamoDB for campaign metadata  
- Queuing: Kafka for event replay and debugging  
- Analytics: CloudWatch and Prometheus for auction health metrics


### Bid Management Layer
Handles campaign pacing, spend throttling, and bid control logic before auction execution.

**Runtime Path**: ✅ Yes

**Why It Matters**  
The Bid Management Layer is responsible for real-time decision-making around whether a campaign is eligible to participate in an auction and how aggressively it should bid. It enforces pacing rules, daily spend limits, and eligibility criteria based on campaign goals and targeting rules. It acts as an intermediary between the Ad Request Orchestrator and the Ad Auction Service, applying control logic to prevent overspending or under-delivery.  
This layer frequently uses in-memory caches populated from the Campaign Management System and Telemetry / Spend Tracking Systems to make sub-millisecond decisions. It may also adjust bid values dynamically based on budget burn rate, time-of-day pacing curves, or performance-based optimization models.

**Typical Technologies**  
- Language: Java, Go  
- Storage: Redis for real-time pacing data  
- Integration: Kafka for event-driven updates from telemetry and campaign systems  
- Optimization: Optional use of ML models for bid tuning

### Creative Renderer
Delivers the winning creative (image, video, or HTML) to the user device by transforming ad markup into renderable assets and interfacing with CDN infrastructure.

**Why It Matters**  
The Creative Renderer ensures the winning ad can be displayed correctly, safely, and within performance constraints. It validates the creative payload (e.g., dimensions, format, compliance with policies), fills templates or markup stubs, and integrates tracking pixels and click URLs. This system also determines optimal CDN endpoints for asset delivery, minimizing latency and maximizing cacheability across geographies. It plays a key role in user experience, impression quality, and measurement accuracy.

**Typical Technologies**  
- Language: JavaScript, Node.js, or Java  
- Rendering: Server-side templating or HTML sanitization engines  
- Integration: CloudFront or Akamai for asset delivery  
- Validation: Rules engine for creative integrity, ad safety, and policy compliance  
- Instrumentation: Embedded tracking beacons for impressions, viewability, and clicks

**Runtime Path**: ✅ Yes

### Advertiser Dashboard & Developer Experience
UI and APIs for advertisers to manage campaigns, budgets, creatives, and reporting.

**Runtime Path**: ❌ No

---

### Campaign Management System  
Stores advertiser campaign configurations, including budgets, targeting rules, creative links, and scheduling constraints.

**Why It Matters**  
This system serves as the source of truth for campaign logic. It is queried by the Bid Management Layer to enforce pacing and eligibility controls.

**Runtime Path**: ❌ No (accessed asynchronously)

**Typical Technologies**  
- Storage: Amazon Aurora, DynamoDB  
- APIs: REST/GraphQL-based config services  
- Sync: Kafka or SQS for event-driven updates

---

### Telemetry / Spend Tracking Systems  
Captures ad delivery logs, auction outcomes, impression tracking, and budget spend events. Provides the feedback loop for monitoring and optimization.

**Why It Matters**  
Used for reporting, pacing decisions, analytics, and ML model training. Powers the Advertiser Dashboard and operational insights.

**Runtime Path**: ❌ No (async data collection)

**Typical Technologies**  
- Logging: Kafka, Kinesis  
- Storage: S3, Redshift, ClickHouse  
- Processing: Apache Flink, Spark, Athena

---

### Creative Asset Store / CDN  
Stores final creative assets (images, videos, JS) and delivers them to user devices via CDN when referenced in ad markup.

**Why It Matters**  
Allows the Creative Renderer to reference fast, globally distributed assets. Ensures user devices can load creatives efficiently.

**Runtime Path**: ⚠️ Partial (user device fetches assets after receiving markup)

**Typical Technologies**  
- Storage: Amazon S3  
- CDN: CloudFront, Fastly, Akamai  
- Upload: Advertiser APIs or dashboard ingestion

## Data Flow Diagram

![Amazon Ads System Diagram](amazon_ads_system_design.excalidraw.png)

## Metrics

- QPS by request type and service
- Auction win rates and bid response times (p50/p99)
- Revenue per mille (RPM)
- Click-through rate (CTR)
- Creative failure rate
- Budget utilization per campaign

## Goals

- Maintain latency budget under 100ms
- Support multiple ad types and channels
- Enable self-service and bulk campaign workflows
- Ensure compliance with GDPR/CCPA
- Provide ML-ready telemetry and reporting