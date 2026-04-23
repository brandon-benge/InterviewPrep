# Nodes

## Linked List Patterns (Critical)

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