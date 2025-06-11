# Facebook Messaging System Design

This document describes the architecture behind the Facebook Messaging System diagram.

## Overview

The system enables real-time messaging between users, supporting presence, media sharing, message archiving, and offline notifications. It leverages XMPP for real-time communication and HTTP for media uploads, with a distributed backend for scalability and reliability.

---

## Component Breakdown

### 1. Mobile Clients
**Purpose:**  
Serve as the user interface for sending and receiving messages, media, and presence updates.

**Technologies:**  
- iOS/Android apps  
- XMPP client libraries  
- HTTP clients

**Usage:**  
Communicate with backend via XMPP for real-time chat and HTTP for media uploads/downloads.

---

### 2. Ejabberd Cluster
**Purpose:**  
Handles XMPP-based messaging, presence, and routing between users.

**Technologies:**  
- Ejabberd (Erlang-based XMPP server)

**Usage:**  
Maintains user sessions, delivers messages instantly, and manages presence information.

---

### 3. YAWS Server
**Purpose:**  
Handles HTTP traffic, especially for media uploads and downloads.

**Technologies:**  
- YAWS (Yet Another Web Server, Erlang)

**Usage:**  
Receives media files from clients and stores metadata in the database; serves media to recipients.

---

### 4. Riak
**Purpose:**  
Stores archived messages for durability and retrieval.

**Technologies:**  
- Riak (distributed NoSQL database)

**Usage:**  
Persists chat history and supports message retrieval for users.

---

### 5. MySQL/Postgres
**Purpose:**  
Stores user data and media metadata.

**Technologies:**  
- MySQL or PostgreSQL

**Usage:**  
Holds user profiles, media references, and other relational data.

---

### 6. Mnesia
**Purpose:**  
Stores session and presence data for fast access.

**Technologies:**  
- Mnesia (Erlang in-memory/distributed DB)

**Usage:**  
Tracks online status and session information for active users.

---

### 7. GCM/APNs
**Purpose:**  
Delivers push notifications to offline users.

**Technologies:**  
- Google Cloud Messaging (GCM)  
- Apple Push Notification Service (APNs)

**Usage:**  
Notifies users of new messages when they are not actively connected.

---

### 8. CDN
**Purpose:**  
Delivers media content efficiently to users worldwide.

**Technologies:**  
- Content Delivery Network (CDN)

**Usage:**  
Caches and serves images, videos, and other media assets to reduce latency.

---

## Diagram

![Messaging System](FacebookMessaging.excalidraw.png)

You can edit this diagram by uploading the PNG to [Excalidraw](https://excalidraw.com).
