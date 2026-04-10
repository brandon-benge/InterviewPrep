"""Account Balance Aggregator starter file."""


class AccountBalanceAggregator:
    def __init__(self):
       self.transactions=[]

    def add_transaction(self, txn_id: str, account_id: str, amount: int, timestamp: int) -> None:
      self.transactions.append([txn_id, account_id, amount, timestamp])

    def get_summary(self) -> dict[str, tuple[int, int, int]]:
      d = {}
      txs = []
      for transaction in self.transactions:
         if transaction[0] in txs:
            continue
         else:
            txs.append(transaction[0])
         if not d:
            d[transaction[1]] = [transaction[2],1,transaction[3]]
         elif transaction[1] not in d:
            d[transaction[1]] = [transaction[2],1,transaction[3]]
         else:
            d[transaction[1]][0]=d[transaction[1]][0]+transaction[2]
            d[transaction[1]][1]=d[transaction[1]][1]+1
            if transaction[3] > d[transaction[1]][2]:
               d[transaction[1]][2]=transaction[3]
      return d

if __name__ == "__main__":
   bank =AccountBalanceAggregator()
   bank.add_transaction("t1", "A", 100, 10)
   bank.add_transaction("t2", "A", -20, 12)
   bank.add_transaction("t3", "B", 50, 11)
   d = bank.get_summary()
   print(d["A"] == [80, 2, 12])
   print(d["B"] == [50, 1, 11])

   bank =AccountBalanceAggregator()
   bank.add_transaction("t1", "A", 100, 10)
   bank.add_transaction("t1", "A", 100, 10)
   bank.add_transaction("t2", "A", -30, 9)
   d = bank.get_summary()
   print(d["A"] == [70, 2, 10])

   bank =AccountBalanceAggregator()
   bank.add_transaction("t1", "A", 40, 5)
   bank.add_transaction("t2", "A", -10, 5)
   bank.add_transaction("t3", "A", 15, 6)
   d = bank.get_summary()
   print(d["A"] == [45, 3, 6])   
