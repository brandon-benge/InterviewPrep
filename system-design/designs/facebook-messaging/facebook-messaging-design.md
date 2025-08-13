# 💬 Facebook Messaging System Design

## 🧠 Overview

> This document outlines the architecture and data flow of the real-time Facebook Messaging system. The system supports instant messaging, media storage, and offline notifications using scalable backend services and protocols.

---

## 🔄 Key Components and Flow

1. **Mobile Clients**
   - Communicate via XMPP and HTTP.
2. **Ejabberd Cluster**
   - Handles XMPP messaging and presence.
3. **YAWS Server**
   - Handles HTTP traffic and uploads.
4. **Riak**
   - Message archive storage.
5. **MySQL/Postgres**
   - Media metadata and user data.
6. **Mnesia**
   - Session and presence data.
7. **GCM/APNs**
   - Offline user notifications.
8. **CDN**
   - Media delivery to clients.

---

## 🗂️ Data Flow

- Clients send/receive messages via XMPP or HTTP.
- Backend clusters manage message routing, presence, and storage.
- Media and metadata are stored in distributed databases.
- Notifications are sent for offline users.

---

## 🏗️ Architecture Diagram

> ![Messaging System](FacebookMessaging.excalidraw.png)

> You can edit this diagram by uploading the PNG to [Excalidraw](https://excalidraw.com).
