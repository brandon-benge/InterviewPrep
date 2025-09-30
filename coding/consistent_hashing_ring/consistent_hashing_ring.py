import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, vnodes: int = 100):
        self.vnodes = vnodes
        self.ring = {}            # hash -> server
        self.sorted_keys = []     # sorted list of hash keys, allows to find the index lookup for the ring
        self.servers = set()      # for easy lookup for add or remove. Not core logic

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add(self, server: str):
        if server in self.servers:
            return
        self.servers.add(server)
        for i in range(self.vnodes):
            vnode_key = f"{server}#{i}"
            hash_val = self._hash(vnode_key)
            self.ring[hash_val] = server
            bisect.insort(self.sorted_keys, hash_val)

    def remove(self, server: str):
        if server not in self.servers:
            return
        self.servers.remove(server)
        for i in range(self.vnodes):
            vnode_key = f"{server}#{i}"
            hash_val = self._hash(vnode_key)
            if hash_val in self.ring:
                del self.ring[hash_val]
                index = bisect.bisect_left(self.sorted_keys, hash_val)
                if index < len(self.sorted_keys) and self.sorted_keys[index] == hash_val:
                    self.sorted_keys.pop(index)

    def get_server(self, key: str) -> str | None:
        if not self.ring:
            return None
        hash_val = self._hash(key)
        index = bisect.bisect(self.sorted_keys, hash_val) % len(self.sorted_keys) # mod here is to go around they ring if last value
        server_hash = self.sorted_keys[index]
        return self.ring[server_hash]

# Example usage
if __name__ == "__main__":
    ring = ConsistentHashRing(vnodes=10)
    ring.add("A")
    ring.add("B")

    print("Initial:")
    print("user:1 →", ring.get_server("user:1"))
    print("user:2 →", ring.get_server("user:2"))

    ring.add("C")
    print("\nAfter adding C:")
    print("user:1 →", ring.get_server("user:1"))
    print("user:2 →", ring.get_server("user:2"))

    ring.remove("B")
    print("\nAfter removing B:")
    print("user:1 →", ring.get_server("user:1"))
    print("user:2 →", ring.get_server("user:2"))