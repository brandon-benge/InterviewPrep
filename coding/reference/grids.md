## Grid / Matrix Mental Model (Critical)

### Mental Checklist (Always do this first)

Before coding, define:

1. What does each cell represent?
2. What are valid moves (up/down/left/right or diagonals)?
3. What makes a move valid?
4. Do I need to track visited cells?
   - use sets or build separate graph. Example:
        - `pacific = set()` or `pacific = [[False] * COLS for _ in range(ROWS)]`
5. What am I solving for? (This determines the pattern)

---

### Common Patterns

**1. Connected Components**
- Count islands / regions
- Use DFS or BFS
- Think: explore all reachable cells

**2. Shortest Path**
- Use BFS
- Think: level-by-level expansion = distance/time

**3. Constraint Traversal**
- Only move if condition holds
- Example: `heights[nr][nc] >= heights[r][c]`
- Think: graph traversal with rules

**4. Grid DP**
- Build values per cell
- Example: `dp[r][c] = dp[r-1][c] + dp[r][c-1]`
- Think: reuse results from neighbors

---

### Quick Decision Rules

- Explore everything → DFS  
    - Example: Exploring regions (Number of Islands), Backtracking (Word Search), Full traversal
- Shortest Path / Level Order → BFS
    - Example: Multi-source expansion [Rotting Oranges](https://leetcode.com/problems/rotting-oranges)
- Min / Max / Count → DP(Dynamic Programming)
- Simple local optimal choices → Greedy

---

### Template

*Note:* BFS uses a queue to expand outward level-by-level, while DFS uses a stack (often recursion) to go deep before backtracking.
```python
# Core setup
ROWS, COLS = len(grid), len(grid[0])
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

# DFS (Explore All Paths / Regions)
visited = set()

def dfs(r, c):
    if not in_bounds(r, c):
        return
    if (r, c) in visited:
        return
    if grid[r][c] != "1":  # problem-specific condition
        return

    visited.add((r, c))

    for dr, dc in directions:
        dfs(r + dr, c + dc)

# BFS (Shortest Path / Level Order)
from collections import deque

q = deque([(start_r, start_c)])
visited = {(start_r, start_c)}

while q:
    r, c = q.popleft()

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc) and (nr, nc) not in visited:
            visited.add((nr, nc))
            q.append((nr, nc))
```