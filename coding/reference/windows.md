## 🪟 Sliding Window Pattern (Critical)

### Core Idea

> Expand with right pointer, shrink with left pointer

Sliding window is used for:
- subarrays / substrings
- longest / shortest window
- constraints (unique chars, sum, frequency)

---

### Base Template (Variable Window)

```python
left = 0

for right in range(len(nums)):
    # 1. expand window
    add(nums[right])

    # 2. shrink window if invalid
    while window_invalid:
        remove(nums[left])
        left += 1

    # 3. update result
    update_answer()
```

---

### What Each Step Means

- **add()** → include new element in window (update count/map/sum)
- **window_invalid** → condition that breaks constraint
- **remove()** → remove left element when shrinking
- **update_answer()** → track max/min/valid result

---

### Common Patterns

#### 1. Longest Substring (No Duplicates)

```python
seen = set()
left = 0
max_len = 0

for right in range(len(s)):
    while s[right] in seen:
        seen.remove(s[left])
        left += 1

    seen.add(s[right])
    max_len = max(max_len, right - left + 1)
```

---

#### 2. Minimum Window (Shrink to Optimize)

```python
while valid_window:
    update_answer()
    remove(nums[left])
    left += 1
```

👉 Expand first, then shrink as much as possible

---

#### 3. Fixed Window Size

```python
window_sum = 0
left = 0

for right in range(len(nums)):
    window_sum += nums[right]

    if right - left + 1 > k:
        window_sum -= nums[left]
        left += 1

    if right - left + 1 == k:
        update_answer()
```
