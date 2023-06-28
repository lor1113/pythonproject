class Merchant:
    def __init__(self,name,tags,colour,deactivated = False,id=None,tag_ids = []):
        self.name = name
        self.tags = tags
        self.colour = colour
        self.id = id
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