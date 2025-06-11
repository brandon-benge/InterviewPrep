# 📰 Facebook News Feed System Design

## 🧠 Overview

This document outlines the architecture and data flow of the Facebook News Feed system. The system leverages backend services to precompute, store, and deliver a personalized feed to users efficiently, using ranking algorithms and optimized data stores.

⸻

## 🔄 Key Components and Flow

1. **Feed Generation**
   - Aggregates and precomputes candidate posts for each user.
2. **Ranking Algorithms**
   - Scores and orders feed items based on relevance, engagement, and freshness.
3. **Data Stores**
   - Store user activity, content, and feed state.
4. **Edge Caching**
   - Reduces latency by caching feed data close to users.
5. **Read-Optimized Databases**
   - Serve feed data efficiently at scale.

⸻

## 🗂️ Data Flow

- User actions and content updates trigger feed generation.
- Backend services compute and rank feed items.
- Feed is cached and delivered to the client.

⸻

## 🏗️ Architecture Diagram

![Facebook News Feed](FacebookNewsFeed.excalidraw.png)

You can edit this diagram by uploading the PNG to [Excalidraw](https://excalidraw.com).
