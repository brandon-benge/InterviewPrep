# KV Store with Nested Transactions

# Problem Statement:
# Implement a KV store with `set/get/delete` and `begin/commit/rollback` supporting **nested transactions**.

# Examples:
# 1. `set('a',1)`; `begin()`; `set('a',2)`; `get('a')` → `2`
# 2. `begin()`; `set('a',3)`; `rollback()`; `get('a')` → `2`
# 3. `commit()`; `get('a')` → `2`

import threading

class Session:
    def __init__(self, transaction_level):
        self.transaction_level =  transaction_level
        self.kv = {}

        
class TxnKV:
    def __init__(self):
        self.sessions = [] # this has to be a list of tuples because you do not want to delete from the datastore
        self.transaction_level = 0
        self.lock = threading.Lock()
        self.seed = {}

    def change_transaction(self, int_change):
        with self.lock:
            self.transaction_level += int_change
            return self.transaction_level
        
    def get(self, key: str) -> object | None:
        for session in reversed(self.sessions):
            if key in session.kv:
                return session.kv[key]
        if key in self.seed:
            return self.seed[key]
        return None
    
    def set(self, key: str, val: str) -> str:
        if len(self.sessions) == 0:
            self.seed[key] = val
            return
        session = self.sessions[-1]
        session.kv[key] = val

    
    def delete(self, key: str):
        self.set(key, None)

    def begin(self):
        newSessionNumber = self.change_transaction(1) #increase 
        newSession = Session(newSessionNumber)
        self.sessions.append(newSession)
    
    def commit(self):
        num_sessions = len(self.sessions)
        if num_sessions == 0:
            raise Exception("Error: No sessions to commit!")
        elif num_sessions == 1:
            root = self.seed | self.sessions[-1].kv 
            self.seed = root
        else:
            result = self.sessions[-2].kv | self.sessions[-1].kv 
            self.sessions[-2].kv = result
        self.change_transaction(-1)
        del self.sessions[-1]
        
    
    def rollback(self):
        self.change_transaction(-1)
        del self.sessions[-1]  
        
    
if __name__ == "__main__":
    print("=== Demonstrating Examples from Problem Statement ===\n")
    
    # Example 1: set('a',1); begin(); set('a',2); get('a') → 2
    print("Example 1: set('a','1'); begin(); set('a','2'); get('a')")
    txn = TxnKV()
    txn.set('a', '1')
    txn.begin()
    txn.set('a', '2')
    result1 = txn.get('a')
    print(f"Result: {result1}")  # Should be '2'
    print()
    
    # Example 2: begin(); set('a',3); rollback(); get('a') → 2
    print("Example 2: begin(); set('a','3'); rollback(); get('a')")
    txn.begin()
    txn.set('a', '3')
    txn.rollback()
    result2 = txn.get('a')
    print(f"Result: {result2}")  # Should be '2'
    print()
    
    # Example 3: commit(); get('a') → 2
    print("Example 3: commit(); get('a')")
    txn.commit()
    result3 = txn.get('a')
    print(f"Result: {result3}")  # Should be '2'
    print()
    
    print("=== Examples completed ===")