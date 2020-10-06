from cursor import Cursor
from Menu import Menu
from EnemyUnit import EnemyUnit
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
        if (self.getTileCursorIsOn() in self.selectedUnitTilesInRange and (self.getTileCursorIsOn().currentUnit == None or self.getTileCursorIsOn().currentUnit == self.cursor.unitSelected)):
            self.cursor.unitSelected.currentTile.setCurrentUnit(None)
            self.cursor.unitSelected.setCurrentTile(self.getTileCursorIsOn())
            self.getTileCursorIsOn().setCurrentUnit(self.cursor.unitSelected)
            self.menu.reset()
            self.menu.checkPos(self.getTileCursorIsOn())
            self.unitIsPlaced =True
            self.getUnitsInAttackRange()
            if (len(self.unitsInRange) > 0):
                self.menu.addAttack()

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

    def selectMenuOption(self):
        
        if (self.menu.menuItems[self.menu.selectedIndex] == "Attack"):
            print("Attack")
            units = list(self.unitsInRange)
            currentHP = units[0].hp
            units[0].hp -= (self.cursor.unitSelected.strength - units[0].defense)
            print("Units hp was " +str(currentHP) + " now it is " + str(units[0].hp))

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
        attackRange = self.cursor.unitSelected.attackRange+1
        cursorPosX = self.cursor.pos[0]
        cursorPosY = self.cursor.pos[1]
        unitsInRange = set()
        tmpVal = attackRange
        for i in range(attackRange):
            for j in range(tmpVal):
                if (cursorPosX+i <= self.currentMap.width and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].setColor((255, 0, 0))
                    if (type(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].currentUnit) == EnemyUnit):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].currentUnit)
                if (cursorPosX-i >= 0 and cursorPosY-j >= 0):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].setColor((255, 0, 0))
                    if (type(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].currentUnit) == EnemyUnit):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].currentUnit)
                if (cursorPosX+i < self.currentMap.width and cursorPosY - j >= 0):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].setColor((255, 0, 0))
                    if (type(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].currentUnit) == EnemyUnit):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].currentUnit)
                if (cursorPosX-i >= 0 and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].setColor((255, 0, 0))
                    if (type(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].currentUnit) == EnemyUnit):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].currentUnit)
            tmpVal-=1
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

    