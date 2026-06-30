# Nodes

## Linked List Patterns (Critical)

### Move Forward Through a Linked List
```python
curr = head

while curr:
    print(curr.val)      # use current node
    curr = curr.next     # move forward
```

**What:** Walks a singly linked list from `head` to the end.

**Why:** This is the base pattern for searching, counting, comparing, and building linked-list solutions.

**Mental Model:**
- `curr` points at the node you are currently visiting
- `curr.next` is the next node in the chain
- Moving forward means replacing `curr` with `curr.next`

**Step Pattern:**
1. Start at `head`
2. Use or inspect `curr`
3. Move to the next node (`curr = curr.next`)
4. Stop when `curr` becomes `None`

**One-line intuition:**
> Keep one pointer on the current node, do your work, then advance it to the next node.

**Common Use Cases:**
- Count linked list length
- Search for a value
- Compare two lists node by node
- Find the tail node

### Move Forward While Tracking Previous
```python
prev = None
curr = head

while curr:
    if curr.val == target:
        break

    prev = curr          # old current becomes previous
    curr = curr.next     # move current forward
```

**What:** Walks forward while keeping access to the node behind `curr`.

**Why:** Needed when deleting, inserting, or reconnecting nodes because singly linked lists cannot move backward.

**One-line intuition:**
> Before moving `curr` forward, save the old `curr` as `prev`.

### Reverse a Linked List (In-Place)
```python
prev = None
curr = head

while curr:
    nxt = curr.next      # 1. Save next node
    curr.next = prev     # 2. Reverse pointer
    prev = curr          # 3. Move prev forward
    curr = nxt           # 4. Move curr forward

head = prev
```

**What:** Reverses a singly linked list in-place.

**Why:** Core building block for many problems (reorder list, palindrome check, merging patterns).

**Mental Model:**
- You are flipping each arrow: `A → B` becomes `A ← B`
- Build the reversed list one node at a time

**Step Pattern (MEMORIZE THIS):**
1. Save next (`nxt = curr.next`)
2. Reverse pointer (`curr.next = prev`)
3. Advance `prev`
4. Advance `curr`

**One-line intuition:**
> Walk the list once, flipping each node’s pointer to point backward instead of forward.

**Common Use Cases:**
- Reorder List (reverse second half)
- Palindrome Linked List
- Reverse Linked List (direct problem)
- Reverse nodes in k-group


## Node left and right
```python
# diameter-of-binary-tree problem
class Solution(object):
    def diameterOfBinaryTree(self, root):
        if not root:
            return 0
        def recursive_return(node):
            if not node:
                return 0            
            left_size = recursive_return(node.left)
            right_size = recursive_return(node.right)
            self.max_value=max(self.max_value, left_size + right_size )
            return max(left_size, right_size)+1
        
        self.max_value=0
        recursive_return(root)
        return self.max_value
```
