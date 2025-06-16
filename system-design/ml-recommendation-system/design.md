# ML Recommendation System Design

## 🧠 Overview

This document outlines the architecture and data flow of a real-time machine learning recommendation system similar to those used by large social media platforms such as Facebook. The system ingests user behavioral events, generates candidate content, ranks it using machine learning models, and delivers a personalized feed to the user.

⸻

## 🔄 Components and Flow

1. User Event Ingestion  
   - User actions captured: clicks, views, likes, scrolls, watch time.  
   - Transport: Kafka pipelines events in real time.

2. Real-Time Stream Processing  
   - Flink consumes from Kafka and transforms events for:  
     - Feature computation  
     - Candidate filtering  
     - Metadata enrichment

⸻

## 🗂️ Data Sources

### Feature Store  
- Includes data on:  
    - Users: age, interests, avg_dwell_time, embeddings  
    - Items: category, freshness, engagement_score  
    - Context: device_type, time_of_day, language  
- Storage: S3 for batch storage, Redis for hot data (e.g., top-ranked candidates)

### Metadata Store  
- Backed by RDBMS or RocksDB  
- Stores social and graph data:  
    - Friend relationships (Edge)  
    - Group memberships (Edge)  
    - NSFW, region, language flags (Node)  
    - Follow/block/visibility rules (Edge)

### ANN Index (FAISS)  
- Built offline using Spark  
- Persisted in S3/blob store  
- Loaded into in-memory or memory-mapped sharded servers for fast vector similarity search

⸻

## 🎯 Candidate Generation

Inputs: Feature Store, Metadata, ANN Index, Redis Cache

Responsibilities:  
- Pull content based on user signals  
- Query FAISS for nearest-neighbor matches  
- Merge candidates from multiple sources  
- Remove ineligible/blocked items  
- Enforce source quotas and diversity rules  
- Limit final output to Top-K (e.g., 500–1000 candidates)

Output: Feature-enriched candidate list to Ranking Service

Example features per candidate:  
- friend_post, ann_similarity, item_category, item_freshness_hours  
- engagement_score, user_dwell_time, device, language, time_of_day

### 🧪 Example Vector Payload to Ranking Service

```json
{
  "user_id": "u_12345",
  "request_context": {
    "device": "iOS",
    "time_of_day": "evening",
    "region": "US",
    "language": "en"
  },
  "candidates": [
    {
      "item_id": "post_001",
      "features": {
        "user_embedding": [0.12, 0.87, -0.33],
        "item_embedding": [0.49, 0.21, 0.73],
        "friend_post": false,
        "same_group": false,
        "ann_similarity": 0.91,
        "item_category": "sports",
        "item_freshness_hours": 1.2,
        "item_engagement_score": 0.78,
        "user_avg_dwell_time": 5.4,
        "device_type": "iOS",
        "time_of_day": "evening",
        "is_hot_item": false
      }
    }
  ]
}
```
⸻

## 🏅 Ranking Service (ML Models)

Pipeline:  
- Pre-Ranker:  
  - Filters 500 → 200 candidates  
  - Uses fast ML (logistic regression or tiny GBDTs)  
  - Latency: ~5 ms  

- Main Ranker:  
    - Scores ~200 candidates  
    - Uses heavy ML (XGBoost, DNNs, Two-Tower Models)  
    - Latency: ~10–20 ms

Output: Ranked candidate list with scores

⸻

## 🧾 Post-Ranking Logic

- Final filtering and reordering:  
  - Top-N selection (e.g., 50)  
  - Diversity enforcement  
  - Business rules (e.g., NSFW demotion, engagement balancing)

⸻

## 🏗️ Feed Assembly

- Ranked items are passed via Kafka to Feed Assembly Service  
- Creative Renderer hydrates content with:  
  - Images, video URLs, text  
  - User profile metadata  
  - CDN asset links

⸻

## 📱 User Delivery

- Final feed sent to mobile or web client  
- Client renders using app-native frameworks  
- User actions feed back into Kafka for the next cycle

⸻

## 📉 Logging and Feedback

- All impressions and clicks are logged  
- Used for:  
  - Offline model training  
  - Real-time metrics and observability  
  - A/B testing and experimentation

⸻

## ⚡ Performance Summary

- Candidate Generator: ~50 ms  
- Pre-Ranker: ~5 ms  
- Main Ranker: ~10–20 ms  
- Total ranking latency: ~20–30 ms  
- End-to-end (including rendering): ~50–150 ms

⸻

---

## 📊 Architecture Diagram

![ML Recommendation System Architecture](ml-recommendation-system.excalidraw.png)

You can edit this diagram by uploading the PNG to [Excalidraw](https://excalidraw.com).