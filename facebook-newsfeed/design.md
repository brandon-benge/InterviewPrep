# Facebook News Feed System Design

This folder contains system design artifacts for modeling how Facebook generates and serves user news feeds. The included `.excalidraw` file diagrams the high-level architecture.

## Contents

- `FacebookNewsFeed.excalidraw`: Visual diagram showing:
    - Fan-out on write and read logic
    - Feed page structure
    - MySQL sharded storage using RocksDB
    - Memcache layers
    - Routing and API flows
    - Association edges

## Summary

The diagram models the Facebook News Feed system using:
- **Nodes**: User, Feed Page, Post, etc.
- **Edges**: Like, Follow, Comment (represented as Association Pages)
- **Cache**: Memcache stores hot nodes and edges
- **Fan-out Decisions**: Write for normal users, Read for high-profile users

Each node and edge format follows an internal schema (see Feed Page and Association Page annotations).