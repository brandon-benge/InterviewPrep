# Notification System Design

## Overview

> This document outlines the architecture and data flow of the Notification System. The system delivers personalized notifications to users through various channels (Push, In-App, Email, SMS) with support for preference management, retry handling, and delivery analytics.

---

## Key Components and Flow

1. **API Gateway**
   - Receives notification requests, provides security, rate limiting, and routing.
2. **Distribution Logic**
   - Validates payloads, enriches messages, and routes based on user preferences.
3. **Channel Preference Data**
   - Stores user delivery settings and opt-in preferences.
4. **Queueing System with DLQ**
   - Handles message buffering, retry, and dead-lettering (Kafka, RabbitMQ, AWS SQS).
5. **Router**
   - Routes messages to the correct delivery channel.
6. **Channels**
   - Sends notifications via Push (APNs/FCM), In-App, Email, or SMS.
7. **Analytics System**
   - Monitors system performance and tracks user engagement.
8. **Subscriber Acknowledgement Service**
   - Collects delivery receipts, open/click events, and acknowledgement signals from subscriber devices or providers and updates the RDBMS.

---

## Data Flow

- Requests are received and validated.
- User preferences are checked and messages are enriched.
- Messages are queued and routed to the appropriate channel.
- Delivery and engagement metrics are tracked for analytics.
- Subscriber acknowledgement events (delivery receipts, opens, clicks) are received from channels or providers and processed by the Subscriber Acknowledgement Service, which records them in the RDBMS for analytics and notification status updates.

---

## RDBMS Model

```mermaid
erDiagram
    USERS {
        UUID user_id PK
        string email
        string phone
        datetime created_at
    }

    CHANNEL_PREFERENCES {
        UUID pref_id PK
        UUID user_id FK
        string channel
        boolean enabled
        time quiet_hours_start
        time quiet_hours_end
        string locale
    }

    TEMPLATES {
        UUID template_id PK
        string channel
        string locale
        text body
        int version
    }

    NOTIFICATIONS {
        UUID notification_id PK
        UUID user_id FK
        string channel
        string status
        json payload
        datetime created_at
        datetime updated_at
    }

    DELIVERY_RECEIPTS {
        UUID receipt_id PK
        UUID notification_id FK
        string provider_status
        datetime received_at
    }

    USERS ||--o{ CHANNEL_PREFERENCES : has
    USERS ||--o{ NOTIFICATIONS : sends
    NOTIFICATIONS ||--o{ DELIVERY_RECEIPTS : yields
```

---

## Key Metrics

- Total notifications processed (by type)
- Success/failure rates
- Retry counts, DLQ volume
- Delivery time per channel
- Open/click-through rates
- Failure reasons and error logs
- Processing latency at each layer
- Acknowledgement metrics: delivery receipts received, open/click rates, acknowledgement latency, failed or missing receipts.

---

## High-Volume Subscription Store (NoSQL Model)

```mermaid
flowchart TD
    RDBMS[(Authoritative Subscriptions)] -->|async replication| A[subscription_shards]
    A -->|partition: event_id| B[shard_id]
    B --> C[users array<UUID>]

    D[reverse_index] -->|partition: user_id| E[subscribed_events array<string>]

    %% Notes
    A:::nosql
    D:::nosql

    classDef nosql fill:#f4f4f4,stroke:#333,stroke-width:1px;
```

---

## Architecture Diagram

### 1. Trigger → Fan-Out → Delivery Flow
```mermaid
flowchart TD
    API[API Gateway]
    DL[Distribution Logic]
    PREF[Channel Preference Data]
    SUBS[(High-Volume Subscription Store)]
    FOS[Fan-Out Scaler / Batcher]
    QUEUE[Queueing System]
    ROUTER[Router]
    QP[Push Queue]
    QI[In-App Queue]
    QE[Email Queue]
    QS[SMS Queue]
    PUSH[Push]
    INAPP[In-App]
    EMAIL[Email]
    SMS[SMS]
    AN[Analytics]

    API --> DL
    DL -->|Pref Lookup| PREF
    DL --> SUBS
    SUBS --> FOS
    FOS --> QUEUE
    QUEUE --> ROUTER

    ROUTER --> QP
    ROUTER --> QI
    ROUTER --> QE
    ROUTER --> QS

    QP --> PUSH
    QI --> INAPP
    QE --> EMAIL
    QS --> SMS

    PUSH --> AN
    INAPP --> AN
    EMAIL --> AN
    SMS --> AN
```

### 2. Notification Update Flow (Modify / Cancel / Resend)
```mermaid
flowchart TD
    NUM[Notification Update Manager]
    NDB[(Notifications Table - RDBMS)]
    QCTL[Queue Controller]
    DL2[Distribution Logic]
    SUBS2[(High-Volume Subscription Store)]
    FOS2[Fan-Out Scaler]
    QUE2[Queueing System]

    NUM --> NDB

    %% Cancel or modify queued messages
    NUM --> QCTL
    QCTL --> QUE2

    %% Optional re-notify
    NUM --> DL2
    DL2 --> SUBS2
    SUBS2 --> FOS2
    FOS2 --> QUE2
```

### 3. Subscriber Acknowledgement Flow
```mermaid
flowchart TD
    CHAN[Channel Providers]
    ACK[Subscriber Acknowledgement Service]
    RDBMSACK[(Delivery Receipts - RDBMS)]
    AN3[Analytics]

    CHAN --> ACK
    ACK --> RDBMSACK
    ACK --> AN3
```
