from cursor import Cursor
class Game(object):

    def __init__(self, currentMap):
        self.currentMap = currentMap
        self.cursor = Cursor()
        self.getTileCursorIsOn().selected()

    def showMovementAndAttackRange(self):
        attackRange = self.cursor.unitSelected.attackRange
        movement = self.cursor.unitSelected.mov

    def unitSelectedCursor(self):
        if (self.getTileCursorIsOn().currentUnit != None):
            print("Theres a guy there")
            self.cursor.setUnitSelected(self.getTileCursorIsOn().currentUnit)
        else:
            print("Theres no one home")

    def selectLeft(self):
        self.getTileCursorIsOn().unselected()
        self.cursor.pos[1] -= 1
        self.getTileCursorIsOn().selected()

    def selectRight(self):
        self.getTileCursorIsOn().unselected()
        self.cursor.pos[1] += 1
        self.getTileCursorIsOn().selected()
    
    def selectUp(self):
        self.getTileCursorIsOn().unselected()
        self.cursor.pos[0] -= 1
        self.getTileCursorIsOn().selected()

    def selectDown(self):
        self.getTileCursorIsOn().unselected()
        self.cursor.pos[0] += 1
        self.getTileCursorIsOn().selected()

    def getTileCursorIsOn(self):
        return self.currentMap.Tiles[self.cursor.pos[0]][self.cursor.pos[1]]

    def draw(self):
        self.currentMap.draw()

    