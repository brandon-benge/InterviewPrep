# Problem Statement:
# Build a consistent hashing ring with **virtual nodes** supporting server add/remove and `get_server(key)`.

# Examples:
# 1. add A,B; `get_server('user:1')`, `get_server('user:2')` → deterministically A or B
# 2. add C; `get_server('user:1')` → possibly C; **most keys remain on prior server**
# 3. remove B; `get_server('user:2')` → A or C, keys remap clockwise
import hashlib

class ConsistentHashRing:

    def __init__(self, vnodes: int = 100):
        self.vnodes = vnodes
        self.hashkey = {}

    def _hash(self, key: str) -> int:
        """Hash a string to an integer"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.vnodes
    
    def get_server(self, key: str) -> str | None:
        hash_integer = self._hash(key)
        if self.hashkey.get(hash_integer):
            return self.hashkey[hash_integer]
        else:
            return None

    def add(self, server: str):
        for hash_integer in range(self.vnodes):
            if hash_integer > min and hash_integer < max:
                self.hashkey[hash_integer] = server

    def add(self, server: str, min: int, max: int):
        for hash_integer in range(self.vnodes):
            if hash_integer > min and hash_integer < max:
                self.hashkey[hash_integer] = server

    def remove(self, server: str):
        for hash_integer in reversed(range(self.vnodes)):
            if self.hashkey.get(hash_integer) == server:
                self.hashkey[hash_integer] = self.hashkey.get(hash_integer+1)        


if __name__ == "__main__":
    hashring = ConsistentHashRing()
    hashring.add("A", 0, 49)
    hashring.add("B", 50, 99)
    print(hashring.get_server('user:1'))
    print(hashring.get_server('user:2'))
    hashring.add("C", 40, 60)
    hashring.remove("B")
    print(hashring.get_server('user:2'))