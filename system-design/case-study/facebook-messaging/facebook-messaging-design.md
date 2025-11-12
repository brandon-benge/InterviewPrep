# Facebook Messaging System Design

## Overview

> This document outlines the architecture and data flow of the real-time Facebook Messaging system. The system uses WebSockets for real-time communication, while still supporting HTTP for media uploads and message history retrieval.

---

## Key Components and Flow

1. **Mobile Clients**
   - Connect via WebSockets for real-time events and HTTP for uploads and history.
2. **WebSocket Gateway Fleet**
   - Handles authentication, heartbeats, and backpressure for persistent WebSocket connections.
3. **API Gateway / Edge**
   - Handles HTTP traffic and media uploads.
4. **Durable Log (Kafka/Redpanda)**
   - Append-only log for message events and system actions.
5. **Message Store (KV (Key-Value) / Columnar)**
   - Stores message archives.
6. **Mailbox/Outbox KV (Key-Value)**
   - Offline message storage for replay.
7. **Realtime Fan-out Service**
   - Distributes messages to online users.
8. **MySQL/Postgres**
   - Stores user profiles and room metadata.
9. **Presence & Session Service (Redis TTL (Time To Live))**
   - Tracks user presence and session(backed by a JWT (JSON Web Token) or mTLS (Mutual Transport Layer Security)) data.
10. **GCM (Google Cloud Messaging)/APNs (Apple Push Notification service)**
    - Sends notifications to offline users.
11. **CDN**
    - Delivers media content to clients.

---

## Data Flow

- Clients connect over WebSockets for real-time messaging and HTTP for media uploads and message history retrieval.
- WebSocket Gateway manages persistent connections, authenticates users, maintains heartbeats, and applies backpressure, forwarding events to the Realtime Fan-out service.
- Messages are appended to the Durable Log, stored in the Message Store, and delivered to online users via the Realtime Fan-out service or queued in the Mailbox KV (Key-Value) for offline replay.
- Presence is tracked in Redis with TTL (Time To Live); offline users receive push notifications via GCM (Google Cloud Messaging)/APNs (Apple Push Notification service).
- Media files are uploaded over HTTP through the API Gateway to Object Storage, and served to clients via CDN.

---


## Architecture Diagram

> One diagram covers the write flow, and the other covers the read flow.  
> You can edit these diagrams by uploading the PNGs to [Excalidraw](https://excalidraw.com).

### Write Flow — Detailed Steps

> ![Write Flow](./websocket-messaging-write.excalidraw.png)

1. **Open WS (WebSocket) & Auth**: Client establishes a WebSocket to the WS (WebSocket) Gateway and presents a short‑lived token (JWT (JSON Web Token)/mTLS (Mutual TLS)). Gateway verifies token and associates the connection with the user/session.
2. **Join Room(s)**: Client sends `join_room(room_id, since_seq?)`. Server validates membership using room metadata in MySQL/Postgres.
3. **Send Message**: Client sends `send_message(room_id, client_msg_id, body, media_refs[])` over WS (WebSocket). Optional media is uploaded separately over HTTP (see steps 12–14).
4. **Admission Control**: WS (WebSocket) Gateway enforces per‑connection rate limits and backpressure (credit/window size). Non‑critical signals (typing/presence) can be deprioritized.
5. **Realtime Fan‑out Intake**: Fan‑out service validates room permissions, normalizes the payload, and assigns a **monotonic sequence** per `(room_id, partition)` and a **server msg_id**.
6. **Durable Append**: Event is appended once to the **Durable Log (Kafka/Redpanda)** for durability, ordering within the room, and replay.
7. **Persist for History**: An async worker writes the message to the **Message Store (KV (Key-Value)/columnar)** with indices on `(room_id, seq)` and timestamps for pagination/search.
8. **Mailbox Writes (Offline)**: Per‑recipient **Mailbox/Outbox KV (Key-Value)** entries are created with the next expected seq to support catch‑up after reconnect.
9. **Presence Check**: Presence/Session service (Redis TTL (Time To Live)) is consulted to determine which recipients are online.
10. **Deliver to Online**: For online recipients, the Fan‑out service pushes the message to the appropriate gateway shard; Gateway sends over the established WS (WebSocket).
11. **Acks & Receipts**: Clients acknowledge delivery via `ack(room_id, last_received_seq)` and optionally send read markers `last_read_seq`. Server records cursors.
12. **Media Init (HTTP)**: If the message includes media, the client first requests an upload URL via the **API Gateway**.
13. **Upload to Object Store**: Client uploads the binary to **Object Storage**; CDN is primed for delivery.
14. **Attach Media Record**: Server stores media metadata (hash, size, mime, object key) in RDBMS and references it from the message body for downstream fetch.
15. **Push Notifications (Offline)**: For offline recipients, the server triggers APNs (Apple Push Notification service)/FCM (Firebase Cloud Messaging) notifications (compact payload, deep link to thread).
16. **Metrics/Tracing**: Emit per‑message latency (send→append, append→deliver), delivery fan‑out counts, dropped/queued signals.

### Read Flow — Detailed Steps

> ![Read Flow](./websocket-messaging-read.excalidraw.png)  

1. **Reconnect & Resume**: Client opens WS (WebSocket) to Gateway and immediately sends `resume(last_seq, rooms[])` derived from local SQLite cache.
2. **Session Restore**: Gateway validates token and session; Fan‑out registers routing for the user’s active rooms.
3. **Catch‑up Source Selection**: Server determines replay source starting at `last_seq + 1` — typically **Mailbox KV (Key-Value)** for recent gaps; durable log can be consulted if mailbox is sparse.
4. **Replay Delivery**: Gateway streams missed messages to the client in seq order. Client merges into local cache without duplications using `(room_id, seq)` or `msg_id`.
5. **Live Stream**: After replay drain, the connection switches to live delivery for new messages in the joined rooms.
6. **Acks & Read Cursors**: Client periodically sends `ack(last_received_seq)` and `read(last_read_seq)`. Server updates per‑user cursors and emits read receipts as needed.
7. **Presence & Typing**: Client may send presence/typing updates; server publishes deltas (TTL (Time To Live)’d) and relays to peers as lightweight events.
8. **History Paging (HTTP)**: When user scrolls up beyond local cache, client calls `GET /history?room_id=...&before_seq=...&limit=...` to the **History API**.
9. **History Query**: History API reads from the **Message Store** (KV (Key-Value)/columnar) using `(room_id, seq)` or time range indexes and returns a page of older messages.
10. **Prepend & De‑dupe**: Client prepends the page in the UI, de‑duping by `seq/msg_id`. Further scrolls request additional pages.
11. **Attachment Fetch**: For messages with media, client retrieves signed URLs/redirects via HTTP and downloads via CDN as needed.
12. **Error/Recovery**: On transient errors or WS (WebSocket) drops, client backs off and reconnects with the same `last_seq` to ensure idempotent replay.
