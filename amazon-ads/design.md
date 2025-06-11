# 🛒 Amazon Ads System Design

## 🧠 Overview

This document outlines the architecture and data flow of Amazon Ads, supporting real-time bidding and ad delivery across Amazon properties (Fire TV, IMDb, Alexa, Amazon.com). The system enables targeting, auctioning, and creative rendering in under 100ms using a modular architecture with strong data compliance and ML-based personalization.

⸻

## 🔄 Key Components and Flow

1. **User Device / Publisher**
   - Initiates the ad request from Fire TV, Alexa, IMDb, or other Amazon-owned properties.
   - **Runtime Path:** ✅ Yes
   - **Core Technologies:** Native apps, browsers, Amazon devices
2. **API Gateway / Front Door**
   - Entry point for all ad requests. Performs validation, authentication, and routing (AWS API Gateway or Lambda@Edge).
   - **Runtime Path:** ✅ Yes
   - **Core Technologies:** AWS API Gateway, Lambda@Edge, REST/gRPC
3. **Ad Request Orchestrator**
   - Enriches ad requests with user, geo, device, and consent data. Applies targeting rules and compliance filters.
   - **Runtime Path:** ✅ Yes
   - **Core Technologies:** Java, Go, AWS EKS/ECS, Redis, DynamoDB, Kafka/S3, SageMaker
4. **Bid Request Engine**
   - Converts enriched context into OpenRTB format and dispatches requests to multiple buyers (DSPs) in parallel.
   - **Runtime Path:** ✅ Yes
   - **Core Technologies:** Java, Rust, OpenRTB (HTTP/gRPC), Kafka/Kinesis
5. **Demand-Side Platforms (DSPs)**
   - External/internal systems used by advertisers to receive bid requests and respond with price and creative.
   - **Runtime Path:** ✅ Yes
   - **Core Technologies:** Amazon DSP, Google DV360, The Trade Desk, MediaMath
6. **Ad Auction Service**
   - Conducts second-price auctions or priority-based selection across eligible bids.
   - **Runtime Path:** ✅ Yes
   - **Core Technologies:** Java, Scala, Netty/Akka, Redis, DynamoDB, Kafka, CloudWatch, Prometheus
7. **Bid Management Layer**
   - Handles campaign pacing, spend throttling, and bid control logic before auction execution.
   - **Runtime Path:** ✅ Yes
   - **Core Technologies:** Java, Go, Redis, Kafka, ML models (optional)
8. **Creative Renderer**
   - Delivers the winning creative (image, video, or HTML) to the user device by transforming ad markup into renderable assets and interfacing with CDN infrastructure.
   - **Runtime Path:** ✅ Yes
   - **Core Technologies:** JavaScript, Node.js, Java, CloudFront/Akamai, HTML sanitization, tracking beacons
9. **Advertiser Dashboard & Developer Experience**
   - UI and APIs for advertisers to manage campaigns, budgets, creatives, and reporting.
   - **Runtime Path:** ❌ No
   - **Core Technologies:** React, REST/GraphQL APIs, S3, Aurora, DynamoDB

⸻

## 🗂️ Data & Supporting Systems

- **Campaign Management System**: Stores advertiser campaign configurations, including budgets, targeting rules, creative links, and scheduling constraints.
  - **Runtime Path:** ❌ No (accessed asynchronously)
  - **Core Technologies:** Aurora, DynamoDB, REST/GraphQL, Kafka/SQS
- **Telemetry / Spend Tracking Systems**: Captures ad delivery logs, auction outcomes, impression tracking, and budget spend events.
  - **Runtime Path:** ❌ No (async data collection)
  - **Core Technologies:** Kafka, Kinesis, S3, Redshift, ClickHouse, Flink, Spark, Athena
- **Creative Asset Store / CDN**: Stores final creative assets (images, videos, JS) and delivers them to user devices via CDN.
  - **Runtime Path:** ⚠️ Partial (user device fetches assets after receiving markup)
  - **Core Technologies:** S3, CloudFront, Fastly, Akamai

⸻

## 🎯 Auction & Delivery Flow

- Ad requests are validated and enriched.
- Bid requests are sent to DSPs in OpenRTB format.
- DSPs respond with bids and creatives.
- Ad Auction Service selects the winning bid (second-price or priority-based).
- Creative Renderer validates and delivers the creative to the user device.
- Telemetry systems log delivery and performance data.

⸻

## 📊 Metrics & Goals

- QPS by request type and service
- Auction win rates and bid response times (p50/p99)
- Revenue per mille (RPM)
- Click-through rate (CTR)
- Creative failure rate
- Budget utilization per campaign
- Maintain latency budget under 100ms
- Support multiple ad types and channels
- Ensure compliance with GDPR/CCPA
- Provide ML-ready telemetry and reporting

⸻

## 🏗️ Architecture Diagram

![Amazon Ads System Diagram](amazon_ads_system_design.excalidraw.png)

You can edit this diagram by uploading the PNG to [Excalidraw](https://excalidraw.com).