# Notification System Design

This document describes the architecture behind the Notification System diagram.

## Overview

The system is designed to deliver personalized notifications to users through various channels (Push, In-App, Email, SMS) with support for preference management, retry handling, and delivery analytics.

## Component Breakdown

### 1. API Gateway

**Purpose:**  
Receives external notification requests and provides entry-level security, rate limiting, and request routing.

**Technologies:**
- Kong, NGINX, Envoy
- Express.js, Fastify

**Usage:**  
Handles single and batch message submissions, authenticates callers, and forwards the request to distribution logic.

---

### 2. Distribution Logic

**Purpose:**  
Validates payloads, enriches messages, and routes based on user preferences.

**Technologies:**
- Node.js, Python
- Redis (cache)
- PostgreSQL, MySQL (preference store)

**Usage:**  
Looks up user preferences and formats the message before pushing to the queue.

---

### 3. Channel Preference Data

**Purpose:**  
Stores user delivery settings and opt-in preferences.

**Technologies:**
- Cache: Redis
- Persistent DB: PostgreSQL, MySQL

**Usage:**  
Used by the distribution logic to make routing decisions.

---

### 4. Queueing System with DLQ

**Purpose:**  
Handles message buffering, retry, and dead-lettering.

**Technologies:**
- Kafka, RabbitMQ, AWS SQS
- DLQ as a separate queue or feature within queueing system

**Usage:**  
Receives messages from the distribution layer and ensures reliable routing.

---

### 5. Router

**Purpose:**  
Routes messages to the correct delivery channel.

**Technologies:**
- Custom microservice in Node.js, Go, or Java

**Usage:**  
Reads queue and dispatches messages to Push, In-App, Email, or SMS services.

---

### 6. Channels

**Purpose:**  
Send notifications to end-users via their preferred medium.

**Technologies and Usage:**
- **Push (APNs/FCM)**: Sends to mobile devices.
- **In-App**: Stores in database for in-app feed (PostgreSQL/MongoDB).
- **Email**: Sent via SES, SendGrid, or SMTP.
- **SMS**: Delivered using Twilio, Vonage, or AWS Pinpoint.

---

### 7. Analytics System

**Purpose:**  
Monitors system performance and tracks user engagement.

**Technologies:**
- Prometheus + Grafana
- Elasticsearch + Kibana
- ClickHouse, Redshift, or BigQuery

**Key Metrics:**
- Total notifications processed (by type)
- Success/failure rates
- Retry counts, DLQ volume
- Delivery time per channel
- Open/click-through rates (push/email)
- Failure reasons and error logs
- Processing latency at each layer

---

## Diagram

![Notification System](NotificationSystem.excalidraw.png)

You can edit this diagram by uploading the PNG to [Excalidraw](https://excalidraw.com).