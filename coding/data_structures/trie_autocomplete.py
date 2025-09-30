# Trie / Autocomplete

# Problem Statement:
# Implement an autocomplete supporting `insert(word)` and `top_k(prefix, k)` that returns up to `k` most frequent completions (ties broken lexicographically). Frequency increments on repeated inserts.

# Examples:
# 1. inserts `[apple, app, app, apex, apply, apple]`; `top_k('ap', 3)` → ["apple", "app", "apex"]
# 2. after above, `top_k('app', 2)` → ["app", "apple"]
# 3. `top_k('b', 5)` → []
import heapq

class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False
        self.frequency = 0  # Track word frequency

class Autocomplete:
    def __init__(self):
        self.root = TrieNode()



    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += 1  # Increment on repeat inserts 


    def top_k(self, prefix: str, k: int) -> list[str]:
        # 1. Find prefix node
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  # Prefix doesn't exist
            node = node.children[char]
        
        # 2. DFS to collect all words with frequencies
        candidates = []
        self._dfs(node, prefix, candidates)
        
        # 3. Use min-heap to find top-k
        heap = []
        for word, freq in candidates:
            if len(heap) < k:
                heapq.heappush(heap, (freq, word))  # Min-heap by frequency
            elif freq > heap[0][0] or (freq == heap[0][0] and word < heap[0][1]):
                heapq.heapreplace(heap, (freq, word))
        
        # 4. Extract and sort by frequency (desc), then lexicographically
        result = sorted(heap, key=lambda x: (-x[0], x[1]))
        return [word for freq, word in result]

    def _dfs(self, node, current_word, candidates):
        if node.is_end:
            candidates.append((current_word, node.frequency))
        
        for char, child in node.children.items():
            self._dfs(child, current_word + char, candidates)

if __name__ == "__main__":
    trie = Autocomplete()
    for word in ["apple", "app", "app", "apex", "apply", "apple"]:
        trie.insert(word)
    print(trie.top_k('ap', 3))
    print(trie.top_k('ap', 2))
    print(trie.top_k('b', 2))