# Time & Space Complexity (Quick Reference)

## Ranking

| Complexity | Name | Common Example |
| --- | --- | --- |
| `O(1)` | Constant | Array access or hash map lookup |
| `O(log n)` | Logarithmic | Binary search, where the input is halved each step |
| `O(n)` | Linear | Traversing an array once |
| `O(n log n)` | Linearithmic | Efficient sorting algorithms like merge sort or heap sort |
| `O(n^2)` | Quadratic | Nested loops, such as bubble sort |
| `O(n^k)` | Polynomial | Algorithms where runtime grows by a fixed power of `n` |
| `O(2^n)` | Exponential | Recursive Fibonacci or exhaustive subset generation |
| `O(n!)` | Factorial | Generating all permutations |


## Grouping → HashMap
- Time: O(n)
- Space: O(n)
- Notes: One pass through data, stores all keys

## Time-Based → Sort / Binary Search / Deque
- Sort:
  - Time: O(n log n)
  - Space: O(1) or O(n)
- Binary Search:
  - Time: O(log n)
  - Space: O(1)
- Deque (sliding window):
  - Time: O(n)
  - Space: O(n)
  - Notes: Each element added/removed once

## Ranking → Heap
- Time: O(n log k)
- Space: O(k)
- Notes: Efficient for top-k problems

## Intervals → Merge Logic
- Time: O(n log n)
- Space: O(n)
- Notes: Sorting dominates, merging is linear

---

# Mental Shortcut

- If you see grouping → O(n)
- If you see sorting → O(n log n)
- If you see top-k → O(n log k)
- If you see sliding window → O(n)
