

# Recursion Cheat Sheet

## 🧠 Core Idea
Recursion = solving a problem by solving **smaller versions of the same problem**

> Key mental model:
> Recursion rewinds function calls, NOT data mutations

---

## ✅ When to Use Recursion

Use recursion when the problem naturally breaks into **identical subproblems**

### 1. Trees
- Each node is the root of a smaller tree
- Examples: DFS, height, path sum

### 2. Graph DFS
- Explore neighbors recursively
- Useful for traversal, connectivity, path finding

### 3. Backtracking (MOST IMPORTANT)
- You need to explore ALL possibilities

Examples:
- Permutations
- Subsets
- Combinations
- N-Queens

Pattern:
```
Choose → Recurse → Undo
```

### 4. Divide & Conquer
- Split problem into parts
- Merge results

Examples:
- Merge Sort
- Quick Sort

### 5. Nested Structures
- JSON, folders, nested lists

---

## 🚫 When NOT to Use Recursion

### ❌ 1. Simple iteration
- Arrays, strings → use loops

### ❌ 2. No branching (single path)
Signal:
```
Only one valid next step exists
```

Example:
- Following a chain or sequence

### ❌ 3. Heavy mutation confusion
Signal:
```
Why is my list changing across calls?
```

### ❌ 4. Repeated scanning of data
Signal:
```
for loop inside recursion over same list
```

Likely better:
- HashMap
- Graph (adj list)

### ❌ 5. Very deep recursion
- Risk of stack overflow
- Prefer iterative

---

## 🔥 Key Signals Recursion IS the Right Choice

You can say:

- “Try all possibilities”
- “Explore every path”
- “Each step creates smaller subproblems”
- “Tree or graph structure”
- “Pick / not pick decisions”

---

## 🚨 Key Signals Recursion is WRONG

You are:

- Mutating shared lists (`append`, `remove`)
- Returning after first match
- Not exploring multiple branches
- Fighting to "undo" state
- Scanning entire list repeatedly

---

## 🧱 Basic Recursion Template

### 1. Standard DFS Template
```
def dfs(node):
    if not node:
        return
    
    # process node
    
    dfs(node.left)
    dfs(node.right)
```

---

### 2. Backtracking Template (MOST IMPORTANT)
```
def backtrack(path, choices):
    if goal reached:
        result.append(path.copy())
        return

    for choice in choices:
        # choose
        path.append(choice)

        # explore
        backtrack(path, updated_choices)

        # undo (CRITICAL)
        path.pop()
```

---

### 3. Safer Version (No Mutation)
```
def backtrack(path, choices):
    if goal reached:
        result.append(path)
        return

    for choice in choices:
        backtrack(path + [choice], updated_choices)
```

---

### 4. Graph DFS Template
```
def dfs(node):
    if node in visited:
        return

    visited.add(node)

    for neighbor in graph[node]:
        dfs(neighbor)
```

---

## ⚠️ Common Mistakes

- Forgetting base case → infinite recursion
- Mutating shared state without undo
- Not copying result (`path.copy()`)
- Early return killing exploration
- Using recursion when iteration is simpler

---

## 🧩 One-Line Memory Hooks

- Loop = repeat steps  
- Recursion = solve smaller problems  
- Backtracking = try → recurse → undo  
- If only ONE path exists → avoid recursion  
- If MANY possibilities → recursion shines  

---

## 🧠 Interview Tip

If stuck, ask yourself:

```
Am I exploring all possibilities?
```

- YES → recursion/backtracking  
- NO → likely iteration or graph traversal  

---