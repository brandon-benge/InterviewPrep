## Interview Must‑Haves (Python)

### Sorting Tricks
*Powerful sorting patterns for custom comparisons and multi-key sorting in interviews.*

**Sorting Tricks** — Quickly sort lists and custom objects.
```python
# By first element only (ascending)
sorted_by_first = sorted(pairs, key=lambda x: x[0])
# By first, then second (both ascending)
sorted_by_first_second_asc = sorted(pairs, key=lambda p: (p[0], p[1]))
# By first ascending, second descending (common interview pattern)
sorted_by_first_asc_second_desc = sorted(pairs, key=lambda p: (p[0], -p[1]))
# All keys descending (global reverse)
sorted_all_desc = sorted(pairs, key=lambda p: (p[0], p[1]), reverse=True)

sorted_nums = sorted(nums)  # sort a list in ascending order
```

### Slicing, Comprehensions, Built‑ins
*Concise Python idioms for data manipulation and iteration that every interview candidate should know.*

```python
# Slicing
rev = s[::-1]                    # reverse string/list
first_n = arr[:n]                # first n elements
last_n = arr[-n:]                # last n elements
skip_first = arr[1:]             # all except first

# List comprehensions
squares = [x**2 for x in nums]                    # transform all
evens = [x for x in nums if x % 2 == 0]          # filter
pairs = [(x, y) for x in a for y in b]           # nested loops
# a=[1,2], b=[3,4] → [(1,3), (1,4), (2,3), (2,4)]
flattened = [item for row in matrix for item in row]  # flatten 2D
# [[1,2], [3,4]] → [1, 2, 3, 4]

# Essential built-ins
pairs = list(zip(a, b))          # combine lists: [("a1", "b1"), ("a2", "b2")]
for i, val in enumerate(arr):    # index + value while looping
doubled = list(map(lambda x: x*2, nums))        # apply function to all
evens = list(filter(lambda x: x%2==0, nums))    # keep matching items
has_any = any(x > 10 for x in nums)             # True if any match
all_positive = all(x > 0 for x in nums)         # True if all match
shortest = min(words, key=len)                  # min/max by custom criteria
```


---

