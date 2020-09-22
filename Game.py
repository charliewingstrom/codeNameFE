from cursor import Cursor
class Game(object):

    def __init__(self, currentMap):
        self.currentMap = currentMap
        self.cursor = Cursor()
        self.getTileCursorIsOn().selected()

    def showMovementAndAttackRange(self):
        attackRange = self.cursor.unitSelected.attackRange
        movement = self.cursor.unitSelected.mov
        #startTile = self.cursor.unitSelected.currentTile
        inRangeTiles = set()
        self.ShowMovAttHelper(self.cursor.pos, movement, attackRange, inRangeTiles)
    
    def ShowMovAttHelper(self, cursorPos, movement, attackRange, inRangeTiles):
        if (movement <= 0 and attackRange <= 0):
            return
        elif (self.currentMap.width-1 < cursorPos[1] or cursorPos[1] < 0):
            return
        elif (self.currentMap.height-1 < cursorPos[0] or cursorPos[0] < 0):
            return
        currTile = self.currentMap.Tiles[cursorPos[0]][cursorPos[1]]
        if (movement>=0):
            print("movement")
            
            if (currTile not in inRangeTiles): 
                inRangeTiles.add(currTile)
                currTile.setColor((0, 0, 255))
            self.ShowMovAttHelper([cursorPos[0]+1, cursorPos[1]], movement-1, attackRange, inRangeTiles)
            self.ShowMovAttHelper([cursorPos[0], cursorPos[1]+1], movement-1, attackRange, inRangeTiles)
            self.ShowMovAttHelper([cursorPos[0]-1, cursorPos[1]], movement-1, attackRange, inRangeTiles)
            self.ShowMovAttHelper([cursorPos[0], cursorPos[1]-1], movement-1, attackRange, inRangeTiles)
        elif (attackRange>0):
            print("attackRange")
            if (currTile not in inRangeTiles): 
                inRangeTiles.add(currTile)
                currTile.setColor((255, 0, 0))
            self.ShowMovAttHelper([cursorPos[0]+1, cursorPos[1]], movement, attackRange-1, inRangeTiles)
            self.ShowMovAttHelper([cursorPos[0], cursorPos[1]+1], movement, attackRange-1, inRangeTiles)
            self.ShowMovAttHelper([cursorPos[0]-1, cursorPos[1]], movement, attackRange-1, inRangeTiles)
            self.ShowMovAttHelper([cursorPos[0], cursorPos[1]-1], movement, attackRange-1, inRangeTiles)
        else:
            print("That's a wall")

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

    