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
            if self.tags:
                for tag in self.tags:
                    self.tag_ids.append(tag.id)
        else:
            self.tag_ids=tag_ids
        
        self.tags_deactivated = []
        if self.tags:
            for tag in self.tags:
                if tag.deactivated == True:
                    self.tags_deactivated.append(tag)
                    self.tags.remove(tag)