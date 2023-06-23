class Transaction:
    def __init__(self,name,amount,tags,merchant,timestamp,id=None):
        self.id = id
        self.name = name
        self.amount = amount
        self.tags = tags
        self.merchant = merchant
        self.timestamp = timestamp