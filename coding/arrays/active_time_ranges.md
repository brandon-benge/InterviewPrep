# Active Time Ranges

Problem Statement:
You are given a list of active intervals for a user session. Each interval is represented as `[start, end]`, where `start < end`.

Build a component that merges overlapping intervals and calculates the total active time.

Rules:
- Intervals may be unsorted.
- Overlapping intervals should be merged.
- Touching intervals should also be merged. For example, `[1, 3]` and `[3, 5]` become `[1, 5]`.
- The result should return merged intervals sorted by start time.

Examples:
1. intervals = `[[1, 3], [2, 6], [8, 10], [15, 18]]`
   merged -> `[[1, 6], [8, 10], [15, 18]]`
   total active time -> `10`

2. intervals = `[[1, 4], [4, 5]]`
   merged -> `[[1, 5]]`
   total active time -> `4`

3. intervals = `[[7, 9], [1, 2], [2, 4], [10, 12]]`
   merged -> `[[1, 4], [7, 9], [10, 12]]`
   total active time -> `7`

```python
class ActiveTimeRanges:
    def merge_and_measure(self, intervals: list[list[int]]) -> tuple[list[list[int]], int]:
        ...
```
