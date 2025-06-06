# Amazon Ads System

## Overview

Amazon Ads supports real-time bidding and ad delivery across Amazon properties such as Fire TV, IMDb, Alexa, and Amazon.com. This system enables targeting, auctioning, and creative rendering in under 100ms using a modular architecture with strong data compliance and ML-based personalization.

## Key Components

### User Device / Publisher
Initiates the ad request from Fire TV, Alexa, IMDb, or other Amazon-owned properties.

### API Gateway / Front Door
The entry point for all ad requests. Performs validation, authentication, and routing. Usually implemented via AWS API Gateway or Lambda@Edge.

### Ad Request Orchestrator
Enriches ad requests with user, geo, device, and consent data. Applies targeting rules and compliance filters.

### Bid Request Engine
Generates bid requests to internal Amazon DSPs and external buyers. Ensures OpenRTB-like compatibility and handles pricing logic.

### Bid Management Layer
Handles campaign pacing, spend throttling, and bid control logic before auction execution.

### Ad Auction Service
Conducts second-price auctions or priority-based selection across eligible bids.

### Creative Renderer
Delivers the winning creative (image, video, or HTML) via templating and CDN integration.

### Advertiser Dashboard & Developer Experience
UI and APIs for advertisers to manage campaigns, budgets, creatives, and reporting.

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

## Technologies

- Gateway: AWS API Gateway, Lambda@Edge
- Services: EKS/ECS, Java or Go
- Data: Redis, DynamoDB, Kafka, S3, Athena
- ML: SageMaker, Amazon Personalize
- Analytics: Redshift, CloudWatch, Firehose