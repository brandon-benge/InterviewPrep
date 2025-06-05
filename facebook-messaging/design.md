# Messaging System Architecture

This document outlines the design of the real-time messaging system diagram.

## Overview

The system uses XMPP and HTTP for communication, along with a variety of backend systems to support real-time messaging, media storage, and offline notifications.

## Key Components

- **Mobile Clients**: Communicate via XMPP and HTTP.
- **Ejabberd Cluster**: Handles XMPP messaging and presence.
- **YAWS Server**: Handles HTTP traffic and uploads.
- **Riak**: Message archive.
- **MySQL/Postgres**: Media metadata, user data.
- **Mnesia**: Session and presence data.
- **GCM/APNs**: Offline user notifications.
- **CDN**: Media delivery.

## Diagram

![Messaging System](FacebookMessaging.excalidraw.png)

You can edit this diagram by uploading the PNG to [Excalidraw](https://excalidraw.com).
