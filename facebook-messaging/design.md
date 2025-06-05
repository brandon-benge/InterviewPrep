# Messaging System Architecture

This document outlines the architecture of a real-time messaging system using the messaging.excalidraw diagram.

## Overview

The system uses a combination of XMPP (via a custom Ejabberd cluster), HTTP (via YAWS), and distributed storage (Riak, Mnesia, MySQL/Postgres) to support real-time messaging, media delivery, and offline notifications.

## Key Components

- **Mobile Clients**: Communicate with servers via XMPP and HTTP.
- **Ejabberd Cluster**: Handles message routing, presence, and real-time delivery using XMPP.
- **YAWS Server**: Manages HTTP requests and media upload endpoints.
- **Mnesia DB**: Stores session and presence data.
- **MySQL/Postgres**: Stores user profiles, contacts, and metadata.
- **Riak**: Write-optimized archive for message history.
- **Media CDN**: Delivers uploaded media efficiently.
- **GCM/APNs**: Push notification services for offline users.

## Diagram

You can view the system architecture diagram here:

[Messaging System Architecture Diagram](https://excalidraw.com/#json=messaging.excalidraw,https://raw.githubusercontent.com/brandon-benge/Excalidraw/main/facebook-messaging/messaging.excalidraw)
