# Task Execution with Cooldown (Rate-Limited Scheduler)

## Problem

You are given a list of tasks. Each task has:

(task_id: str, timestamp: int)

Each task takes 1 unit of time to execute.

There is a cooldown period `k` such that:

The same task_id cannot be executed again until k units of time have passed since its last execution.

---

## Goal

Return the minimum total time required to execute all tasks.

- You may reorder tasks
- You may insert idle time if needed

---

## Example

tasks = [
    ("A", 0),
    ("A", 1),
    ("B", 2),
    ("A", 3)
]

k = 2

One valid execution:

time 0: A  
time 1: B  
time 2: idle  
time 3: A  
time 4: idle  
time 5: A  

Output:

6

---

## Constraints

- 1 ≤ len(tasks) ≤ 10^5
- k ≥ 0
- timestamps are NOT guaranteed to be sorted
- timestamps can be ignored for scheduling

---

## What This Tests

- Greedy scheduling
- Heap / priority queue (optional)
- Frequency counting
- Constraint handling

---

## Hints

- Count frequency of each task_id
- Most frequent task determines structure
- Consider using a max heap
- Or derive a formula based on max frequency

---

## Edge Cases

- k = 0
- All tasks identical
- All tasks unique
- Multiple tasks with same frequency

---

## Follow-Ups

1. How would you handle real-time streaming tasks?
2. How would you distribute this across workers?
3. How would you track cooldown efficiently?
