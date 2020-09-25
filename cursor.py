
class Cursor(object):

    def __init__(self):
        self.pos = [1, 1]
        self.unitSelected = None
        
    def setUnitSelected(self, unit):
        self.unitSelected = unit