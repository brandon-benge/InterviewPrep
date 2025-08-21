# Coding Interview Questions & Study Plan

## Overview

> This document contains a comprehensive study plan for preparing for technical coding interviews. The focus is on reinforcing high‑yield problem patterns that emphasize clean problem‑solving, edge‑case handling, and clear communication rather than obscure algorithms.

## Study Guide by Concepts (LeetCode and Non-LeetCode)

### Rate Limiting & TTL

- [Rate Limiter & TTL Cache (custom)](custom_questions/rate_limiting_ttl/rate_limiter.md)

#### Logger with Sampling & Severity Levels

- [Logger with Sampling & Severity Levels (custom)](custom_questions/rate_limiting_ttl/logger_sampling.md)


### Caching & Key–Value Stores

#### LRU Cache
- [LeetCode 146](https://leetcode.com/problems/lru-cache/)
- [Custom](custom_questions/caching_kv_store/lru_cache.md)

#### Time-Based Key-Value Store
- [LeetCode 981](https://leetcode.com/problems/time-based-key-value-store/)
- [Custom: TimeMap](custom_questions/caching_kv_store/time_map.md)
- [Custom: TTLCache](custom_questions/caching_kv_store/ttl_cache.md)

#### KV Store with Nested Transactions
- [Custom](custom_questions/caching_kv_store/txn_kv.md)

#### Transactions
- KV Store with Nested Transactions – [custom](custom_questions/caching_kv_store/txn_kv.md)

### Task Scheduler with Retries & Exponential Backoff
- [Task Scheduler with Retries & Exponential Backoff – custom](custom_questions/task_scheduler/task_scheduler.md)


### Trie / Autocomplete
- [Trie / Autocomplete (custom)](custom_questions/trie_autocomplete/trie_autocomplete.md)

### Consistent Hashing Ring
- [Consistent Hashing Ring (custom)](custom_questions/consistent_hashing_ring/consistent_hashing_ring.md)

### Arrays & Hash Tables
- [Two Sum](https://leetcode.com/problems/two-sum/) – Hash map for O(1) lookups
- [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) – Set operations

### Strings
- [Valid Anagram](https://leetcode.com/problems/valid-anagram/) – Frequency counting
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) – Sliding window

### Intervals
- [Merge Intervals](https://leetcode.com/problems/merge-intervals/) – Interval merging
- [Insert Interval](https://leetcode.com/problems/insert-interval/) – Insertion with merging

### Trees
- [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) – Simple recursion
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) – BFS traversal
- [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) – Track max depth

### Recursion & Backtracking
- [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) – Valid combinations
- [Permutations](https://leetcode.com/problems/permutations/) – All permutations

### Sorting & Heaps
- [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) – Quickselect/heap
- [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) – Heap + counting

### Graphs
- [Number of Islands](https://leetcode.com/problems/number-of-islands/) – DFS/BFS on grid
- [Clone Graph](https://leetcode.com/problems/clone-graph/) – Copy with visited tracking
- [Course Schedule](https://leetcode.com/problems/course-schedule/) – Topological sort

### Linked Lists
- [LRU Cache](https://leetcode.com/problems/lru-cache/) – Dict + doubly linked list
- [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) – Pointer reversal

### Math & Edge Cases
- [Missing Number](https://leetcode.com/problems/missing-number/) – Math/XOR
- [Two Sum II – Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) – Two pointers

## Interview Best Practices

### Problem-Solving Framework
1. **Clarify Requirements** – inputs/outputs, constraints, edge cases
2. **Plan Your Approach** – brute force then optimize; discuss trade-offs
3. **Write Clean Code** – meaningful names, structure, handle edge cases
4. **Test Your Solution** – dry-run examples, edge cases, complexity review

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