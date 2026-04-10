# Coding Interview Questions & Study Plan

> Directory note: `reference/` contains cheat sheets, active practice lives in the category folders, and stale experiments live in `archive/`.

## Overview

> This document contains a comprehensive study plan for preparing for technical coding interviews. The focus is on reinforcing high‑yield problem patterns that emphasize clean problem‑solving, edge‑case handling, and clear communication rather than obscure algorithms.

## Study Guide by Problem Patterns

### Rate Limiting & Expiration

- [Rate Limiter & TTL Cache (custom)](rate_limiting_ttl/rate_limiter.md)
- [Rate Limiting with TTL (custom)](rate_limiting_ttl/rate_limiting_ttl.md)
- [Token Bucket Algorithm (custom)](token_bucket/token_bucket.md)
- [Sliding Window Rate Limit (custom)](rate_limiting_ttl/sliding_window_rate_limit.md)

#### Logger with Sampling & Severity Levels

- [Logger with Sampling & Severity Levels (custom)](rate_limiting_ttl/logger_sampling.md)

### Ledger Reconciliation & Event Processing

- [Account Balance Aggregator (custom)](stream/account_balance_aggregator.md)
- [Addepar Temporal Aggregation (custom)](stream/addepar_temporal_problem.md)

### Caching, Key–Value Stores & Ranking

#### LRU Cache
- [LeetCode 146](https://leetcode.com/problems/lru-cache/)
- [Custom](caching_kv_store/lru_cache.md)

#### Time-Based Key-Value Store
- [LeetCode 981](https://leetcode.com/problems/time-based-key-value-store/)
- [Custom: TimeMap](caching_kv_store/time_map.md)
- [Custom: TTLCache](caching_kv_store/ttl_cache.md)

#### KV Store with Nested Transactions
- [Custom](caching_kv_store/txn_kv.md)

#### Ranking / Top-K Retrieval
- [Top K Scores Tracker (custom)](caching_kv_store/top_k_scores.md)

### Scheduling & Retry Logic
- [Task Scheduler with Retries & Exponential Backoff – custom](task_scheduler/task_scheduler.md)

### Queues & Worker Coordination
- [Retryable Worker with Job Queue (custom)](job_queue/retryable_worker.md)

### Concurrency & Synchronization
- [Thread-Safe Counter (custom)](concurrency/thread_safe_counter.md)

### Prefix Search & Autocomplete
- [Trie / Autocomplete (custom)](data_structures/trie_autocomplete.md)

### Partitioning & Consistent Hashing
- [Consistent Hashing Ring (custom)](consistent_hashing_ring/consistent_hashing_ring.md)

### Arrays, Hashing & Interval Processing
- [Active Time Ranges (custom)](arrays/active_time_ranges.md)
- [Two Sum](https://leetcode.com/problems/two-sum/) – Hash map for O(1) lookups
- [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) – Set operations
- [Merge Intervals](https://leetcode.com/problems/merge-intervals/) – Interval merging
- [Insert Interval](https://leetcode.com/problems/insert-interval/) – Insertion with merging

### Strings & Sliding Window
- [Valid Anagram](https://leetcode.com/problems/valid-anagram/) – Frequency counting
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) – Sliding window


### Trees & Traversal
- [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) – Simple recursion
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) – BFS traversal
- [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) – Track max depth

### Recursion, Backtracking & Dynamic Programming
- [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) – Valid combinations
- [Permutations](https://leetcode.com/problems/permutations/) – All permutations
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) – Intro to Dynamic Programming (recurrence relation, bottom-up)

### Sorting, Heaps & Selection
- [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) – Quickselect/heap
- [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) – Heap + counting

### Graphs & Dependency Ordering
- [Number of Islands](https://leetcode.com/problems/number-of-islands/) – DFS/BFS on grid
- [Clone Graph](https://leetcode.com/problems/clone-graph/) – Copy with visited tracking
- [Course Schedule](https://leetcode.com/problems/course-schedule/) – Topological sort

### Linked Lists & Pointer Manipulation
- [LRU Cache](https://leetcode.com/problems/lru-cache/) – Dict + doubly linked list
- [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) – Pointer reversal

### Math, Search & Edge Cases
- [Missing Number](https://leetcode.com/problems/missing-number/) – Math/XOR
- [Two Sum II – Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) – Two pointers
- [Binary Search](https://leetcode.com/problems/binary-search/) – Classic binary search template

## Interview Best Practices

### Problem-Solving Framework
1. **Clarify Requirements** – inputs/outputs, constraints, edge cases
2. **Plan Your Approach** – brute force then optimize; discuss trade-offs
3. **Write Clean Code** – meaningful names, structure, handle edge cases
4. **Test Your Solution** – dry-run examples, edge cases, complexity review

### Talk‑Track Template
```text
Goal: <problem>  
Input/Output: <types, ranges, order, duplicates?>  
Constraints: n≈?, time target?, memory?, in‑place?

Baseline: <very short> → O(...).  
Better idea: <DS/algorithm> because <property>.  
Plan: <steps 1‑2‑3>  
Edge cases: <list>
```

### Communication Tips
- Verbalize your thinking
- Ask clarifying questions
- Explain trade-offs clearly
- If stuck, narrate options and choose

### Common Patterns to Master
- Two Pointers, Sliding Window, Hash Maps
- DFS/BFS, Dynamic Programming, Binary Search
- Heaps/Priority Queues, Union-Find, Monotonic Stack

### Additional Resources
- [LeetCode](https://leetcode.com/) – Primary practice platform
- [HackerRank](https://www.hackerrank.com/) – Alternative practice
- [CodeSignal](https://codesignal.com/) – Interview-style challenges
- [Cracking the Coding Interview](https://www.crackingthecodinginterview.com/) – Book
- [Elements of Programming Interviews](http://elementsofprogramminginterviews.com/) – Book
- [Pramp](https://www.pramp.com/) – Free peer mocks
- [Interviewing.io](https://interviewing.io/) – Anonymous mocks
