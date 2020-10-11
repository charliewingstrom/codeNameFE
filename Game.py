from cursor import Cursor
from ActionMenu import ActionMenu
from EnemyUnit import EnemyUnit
red = (185, 0, 0)
class Game(object):

    def __init__(self, window, currentMap, playerUnits, enemyUnits):
        
        self.window = window
        self.currentMap = currentMap
        self.playerUnits = playerUnits
        self.enemyUnits = enemyUnits
        self.cursor = Cursor()
        self.menu = ActionMenu(window, currentMap.screenWidth)
        self.getTileCursorIsOn().highlighted()
        self.selectedUnitPrevPos = None
        self.selectedUnitTilesInRange = []
        self.selectedUnitAttackRangeTiles = []
        self.unitIsPlaced = False
        self.unitsInRange = set()
        self.activeUnits = set()
        self.startTurn()

    def startTurn(self):
        print("Turn Start")
        for unit in self.playerUnits:
            unit.active = True
            self.activeUnits.add(unit)

    def endTurn(self):
        print("Turn Over")

    def selectUnit(self):
        if (self.getTileCursorIsOn().currentUnit != None):
            if (self.getTileCursorIsOn().currentUnit.active):
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
            self.unitsInRange = self.getUnitsInAttackRange(self.cursor.unitSelected)
            if (len(self.unitsInRange) > 0):
                self.menu.addAttack()

    def resetSelectedUnit(self):
        self.cursor.unitSelected.setCurrentTile(self.currentMap.Tiles[self.selectedUnitPrevPos[0]][self.selectedUnitPrevPos[1]])
        self.currentMap.Tiles[self.selectedUnitPrevPos[0]][self.selectedUnitPrevPos[1]].setCurrentUnit(self.cursor.unitSelected)
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos = self.selectedUnitPrevPos
        self.getTileCursorIsOn().highlighted()
        self.cleanupAfterAction()
        
    def cleanupAfterAction(self): 
        for tile in self.selectedUnitAttackRangeTiles:
            tile.setColor(tile.defaultColor)
        self.selectedUnitTilesInRange = []
        self.selectedUnitAttackRangeTiles = []
        self.selectedUnitPrevPos = None
        self.activeUnits.remove(self.cursor.unitSelected)
        self.cursor.setUnitSelected(None)
        self.unitIsPlaced = False
        self.unitsInRange = set()
        if (len(self.activeUnits) <= 0):
            self.endTurn()
            self.startTurn()
        
    def selectMenuOption(self):
        action = self.menu.menuItems[self.menu.selectedIndex]
        if (action == "Attack"):
            print("Attack")
            units = list(self.unitsInRange)
            currentHP = units[0].hp
            units[0].hp -= (self.cursor.unitSelected.strength - units[0].defense)
            print("Units hp was " +str(currentHP) + " now it is " + str(units[0].hp))
            self.cursor.unitSelected.active = False
            
        if (action == "Wait"):
            self.cursor.unitSelected.active = False
        self.cleanupAfterAction()
    
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
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].setColor(red)
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j])
                if (cursorPosX-i >= 0 and cursorPosY-j >= 0):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].setColor(red)
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j])
                if (cursorPosX+i < self.currentMap.width and cursorPosY - j >= 0):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].setColor(red)
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j])
                if (cursorPosX-i >= 0 and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].setColor(red)
                    self.selectedUnitAttackRangeTiles.append(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j])
            tmpVal-=1

    def getUnitsInAttackRange(self, unit):
        for tile in self.selectedUnitAttackRangeTiles:
            tile.setColor(tile.defaultColor)
        tile = unit.currentTile
        #print(self.cursor.unitSelected.attackRange)
        attackRange = self.cursor.unitSelected.attackRange+1
        cursorPosX = tile.heightIndex
        cursorPosY = tile.widthIndex
        unitsInRange = set()
        tmpVal = attackRange
        for i in range(attackRange):
            for j in range(tmpVal):
                if (cursorPosX+i <= self.currentMap.width and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].setColor(red)
                    if (type(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].currentUnit) == EnemyUnit):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].currentUnit)
                if (cursorPosX-i >= 0 and cursorPosY-j >= 0):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].setColor(red)
                    if (type(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].currentUnit) == EnemyUnit):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].currentUnit)
                if (cursorPosX+i < self.currentMap.width and cursorPosY - j >= 0):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].setColor(red)
                    if (type(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].currentUnit) == EnemyUnit):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].currentUnit)
                if (cursorPosX-i >= 0 and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].setColor(red)
                    if (type(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].currentUnit) == EnemyUnit):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].currentUnit)
            tmpVal-=1
        return unitsInRange

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
        for unit in self.playerUnits:
            unit.draw()
        for unit in self.enemyUnits:
            unit.draw()
        if (self.unitIsPlaced):
            self.menu.draw()

    