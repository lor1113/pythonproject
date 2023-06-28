class Merchant:
    def __init__(self,name,auto_tags,colour,deactivated = False,id=None,tag_ids = []):
        self.name = name
        self.auto_tags = auto_tags
        self.colour = colour
        self.id = id
        self.deactivated = deactivated
        if not tag_ids:
            self.tag_ids = []
            for tag in self.auto_tags:
                self.tag_ids.append(tag.id)
        else:
            self.tag_ids=tag_ids

    def deactivate(self):
        self.deactivated = True
    
    def reactivate(self):
        self.deactivated = False