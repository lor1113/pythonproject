class Transaction:
    def __init__(self,name,amount,tags,merchant,timestamp,deactivated=False,id=None,tag_ids=[]):
        self.id = id
        self.name = name
        self.amount = amount
        self.tags = tags
        self.merchant = merchant
        self.timestamp = timestamp
        self.deactivated = deactivated
        if not tag_ids:
            self.tag_ids = []
            for tag in self.tags:
                self.tag_ids.append(tag.id)
        else:
            self.tag_ids=tag_ids