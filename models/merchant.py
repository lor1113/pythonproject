class Merchant:
    def __init__(self,name,auto_tags,colour,deactivated = False,id=None):
        self.name = name
        self.auto_tags = auto_tags
        self.colour = colour
        self.id = id
        self.deactivated = deactivated

    def deactivate(self):
        self.deactivated = True
    
    def reactivate(self):
        self.deactivated = False