from cursor import Cursor
class Game(object):

    def __init__(self, currentMap):
        self.currentMap = currentMap
        self.cursor = Cursor()
        self.getTileCursorIsOn().highlighted()
        self.selectedUnitPrevPos = None
        self.selectedUnitTilesInRange = []
        self.selectedUnitAttackRangeTiles = []
    def selectUnit(self):
        if (self.getTileCursorIsOn().currentUnit != None):
            self.unitSelectedCursor()
            self.showMovementAndAttackRange()
            self.selectedUnitPrevPos = [self.cursor.pos[0], self.cursor.pos[1]]

    def placeUnit(self):
        if (self.getTileCursorIsOn() in self.selectedUnitTilesInRange):
            self.cursor.unitSelected.setCurrentTile(self.getTileCursorIsOn())
            self.getTileCursorIsOn().setCurrentUnit(self.cursor.unitSelected)

    def resetSelectedUnit(self):
        for tile in self.selectedUnitAttackRangeTiles:
            tile.setColor(tile.defaultColor)
        self.selectedUnitTilesInRange = []
        self.selectedUnitAttackRangeTiles = []
        self.cursor.unitSelected.currentTile.setCurrentUnit(None)
        self.cursor.unitSelected.setCurrentTile(self.currentMap.Tiles[self.selectedUnitPrevPos[0]][self.selectedUnitPrevPos[1]])
        self.currentMap.Tiles[self.selectedUnitPrevPos[0]][self.selectedUnitPrevPos[1]].setCurrentUnit(self.cursor.unitSelected)
        self.selectedUnitPrevPos = None
        self.cursor.setUnitSelected(None)

    def showMovementAndAttackRange(self):
        attackRange = self.cursor.unitSelected.attackRange
        movement = self.cursor.unitSelected.mov +1
        cursorPosX = self.cursor.pos[0]
        cursorPosY = self.cursor.pos[1]
        ##self.ShowMovAttHelper(self.cursor.pos, movement, attackRange, inRangeTiles)
        tmpVal = movement

        for i in range(movement):
            for j in range(tmpVal):
                self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].setColor((0, 0, 255))
                self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].setColor((0, 0, 255))
                self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].setColor((0, 0, 255))
                self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].setColor((0, 0, 255))
                self.selectedUnitTilesInRange.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j])
                self.selectedUnitTilesInRange.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j])
                self.selectedUnitTilesInRange.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j])
                self.selectedUnitTilesInRange.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j])
                self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j])
                self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j])
                self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j])
                self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j])
            tmpVal-=1
        tmpVal = attackRange
        for i in range(movement+1):
            for j in range(movement-i, movement+tmpVal):
                self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].setColor((255, 0, 0))
                self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].setColor((255, 0, 0))
                self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].setColor((255, 0, 0))
                self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].setColor((255, 0, 0))
                self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j])
                self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j])
                self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j])
                self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j])
            tmpVal-=1


    def unitSelectedCursor(self):
        self.cursor.setUnitSelected(self.getTileCursorIsOn().currentUnit)
        
    def selectLeft(self):
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos[1] -= 1
        self.getTileCursorIsOn().highlighted()

    def selectRight(self):
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos[1] += 1
        self.getTileCursorIsOn().highlighted()
    
    def selectUp(self):
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos[0] -= 1
        self.getTileCursorIsOn().highlighted()

    def selectDown(self):
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos[0] += 1
        self.getTileCursorIsOn().highlighted()

    def getTileCursorIsOn(self):
        return self.currentMap.Tiles[self.cursor.pos[0]][self.cursor.pos[1]]

    def draw(self):
        self.currentMap.draw()

    