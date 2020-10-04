from cursor import Cursor
from Menu import Menu

red = (255, 0, 0)
class Game(object):

    def __init__(self, window, currentMap):
        
        self.window = window
        self.currentMap = currentMap
        self.cursor = Cursor()
        self.menu = Menu(window, currentMap.screenWidth)
        self.getTileCursorIsOn().highlighted()
        self.selectedUnitPrevPos = None
        self.selectedUnitTilesInRange = []
        self.selectedUnitAttackRangeTiles = []
        self.unitIsPlaced = False
        self.unitsInRange = set()

    def selectUnit(self):
        if (self.getTileCursorIsOn().currentUnit != None):
            self.unitSelectedCursor()
            self.showMovementAndAttackRange()
            self.selectedUnitPrevPos = [self.cursor.pos[0], self.cursor.pos[1]]

    def placeUnit(self):
        if (self.getTileCursorIsOn() in self.selectedUnitTilesInRange and self.getTileCursorIsOn().currentUnit == None):
            self.cursor.unitSelected.currentTile.setCurrentUnit(None)
            self.cursor.unitSelected.setCurrentTile(self.getTileCursorIsOn())
            self.getTileCursorIsOn().setCurrentUnit(self.cursor.unitSelected)
            self.menu.checkPos(self.getTileCursorIsOn())
            self.unitIsPlaced =True
            self.getUnitsInAttackRange()

    def resetSelectedUnit(self):
        for tile in self.selectedUnitAttackRangeTiles:
            tile.setColor(tile.defaultColor)
        self.selectedUnitTilesInRange = []
        self.selectedUnitAttackRangeTiles = []
        self.cursor.unitSelected.currentTile.setCurrentUnit(None)
        self.cursor.unitSelected.setCurrentTile(self.currentMap.Tiles[self.selectedUnitPrevPos[0]][self.selectedUnitPrevPos[1]])
        self.currentMap.Tiles[self.selectedUnitPrevPos[0]][self.selectedUnitPrevPos[1]].setCurrentUnit(self.cursor.unitSelected)
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos = self.selectedUnitPrevPos
        self.getTileCursorIsOn().highlighted()
        self.selectedUnitPrevPos = None
        self.cursor.setUnitSelected(None)
        self.unitIsPlaced = False
        self.unitsInRange = set()

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
                if (cursorPosX+i <= self.currentMap.width and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].setColor((0, 0, 255))
                    self.selectedUnitTilesInRange.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j])
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j])
                if (cursorPosX+i < self.currentMap.width and cursorPosY - j >= 0):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].setColor((0, 0, 255))
                    self.selectedUnitTilesInRange.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j])
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j])
                if (cursorPosX-i >= 0 and cursorPosY-j >= 0):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].setColor((0, 0, 255))
                    self.selectedUnitTilesInRange.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j])
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j])
                if (cursorPosX-i >= 0 and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].setColor((0, 0, 255))
                    self.selectedUnitTilesInRange.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j])
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j])
                
            tmpVal-=1
        tmpVal = attackRange
        for i in range(movement+1):
            for j in range(movement-i, movement+tmpVal):
                if (cursorPosX+i <= self.currentMap.width and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].setColor((255, 0, 0))
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j])
                if (cursorPosX-i >= 0 and cursorPosY-j >= 0):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].setColor((255, 0, 0))
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j])
                if (cursorPosX+i < self.currentMap.width and cursorPosY - j >= 0):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].setColor((255, 0, 0))
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j])
                if (cursorPosX-i >= 0 and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].setColor((255, 0, 0))
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j])
            tmpVal-=1

    def getUnitsInAttackRange(self):
        for tile in self.selectedUnitAttackRangeTiles:
            tile.setColor(tile.defaultColor)
        #print(self.cursor.unitSelected.attackRange)
        attackRange = self.cursor.unitSelected.attackRange
        startPos = self.cursor.pos

        unitsInRange = set()
        unitsInRange.add(1)
        for i in range(1, attackRange+1):
            print(str(i))
            self.currentMap.Tiles[startPos[0]+i][startPos[1]].setColor(red)
            if self.currentMap.Tiles[startPos[0]+i][startPos[1]].currentUnit != None:
                unitsInRange.add(self.currentMap.Tiles[startPos[0]+i][startPos[1]].currentUnit)
            self.currentMap.Tiles[startPos[0]][startPos[1]+i].setColor(red)
            if self.currentMap.Tiles[startPos[0]][startPos[1]+i].currentUnit != None:
                unitsInRange.add(self.currentMap.Tiles[startPos[0]][startPos[1]+i].currentUnit)
            self.currentMap.Tiles[startPos[0]-i][startPos[1]].setColor(red)
            if self.currentMap.Tiles[startPos[0]-i][startPos[1]].currentUnit != None:
                unitsInRange.add(self.currentMap.Tiles[startPos[0]-i][startPos[1]].currentUnit)
            self.currentMap.Tiles[startPos[0]][startPos[1]-i].setColor(red)
            if self.currentMap.Tiles[startPos[0]][startPos[1]-i].currentUnit != None:
                unitsInRange.add(self.currentMap.Tiles[startPos[0]][startPos[1]-i].currentUnit)

        print(unitsInRange)
        self.unitsInRange = unitsInRange

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
        if (self.unitIsPlaced):
            self.menu.draw()

    