class Tag:
    def __init__(self, name, colour, deactivated=False, id=None):
      self.name = name
      self.colour = colour
      self.id = id
      self.deactivated = deactivated
    
    def deactivate(self):
      self.deactivated = True
    
    def reactivate(self):
      self.deactivated = False
