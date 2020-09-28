from cursor import Cursor
from Menu import Menu
class Game(object):

    def __init__(self, window, currentMap):
        
        self.window = window
        self.currentMap = currentMap
        self.cursor = Cursor()
        self.menu = Menu(window, self.cursor.pos, currentMap.screenWidth)
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

    ## finds the tiles that the current unit can move to and changes their color,
    ## then finds the tiles that a unit can attack (but not move to) and makes them a different color
    def showMovementAndAttackRange(self):
        attackRange = self.cursor.unitSelected.attackRange
        movement = self.cursor.unitSelected.mov +1
        cursorPosX = self.cursor.pos[0]
        cursorPosY = self.cursor.pos[1]
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
        if (self.getTileCursorIsOn().posX < self.currentMap.tileSize ):
            self.currentMap.scrollLeft()

    def selectRight(self):
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos[1] += 1
        self.getTileCursorIsOn().highlighted()
        if (self.getTileCursorIsOn().posX > self.currentMap.screenWidth - self.currentMap.tileSize):
            self.currentMap.scrollRight()
    
    def selectUp(self):
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos[0] -= 1
        self.getTileCursorIsOn().highlighted()
        if (self.getTileCursorIsOn().posY < self.currentMap.tileSize ):
            self.currentMap.scrollUp()

    def selectDown(self):
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos[0] += 1
        self.getTileCursorIsOn().highlighted()
        if (self.getTileCursorIsOn().posY > self.currentMap.screenHeight - self.currentMap.tileSize):
            self.currentMap.scrollDown()

    def getTileCursorIsOn(self):
        return self.currentMap.Tiles[self.cursor.pos[0]][self.cursor.pos[1]]

    def draw(self):
        self.currentMap.draw()
        self.menu.draw()

    