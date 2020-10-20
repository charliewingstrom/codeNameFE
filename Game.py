from cursor import Cursor
from ActionMenu import ActionMenu
from MapHealthMenu import MapHealthMenu
from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit
from TurnManager import TurnManager
red = (185, 0, 0)
blue = (0, 0, 255)
class Game(object):

    def __init__(self, window, currentMap, playerUnits, enemyUnits):
        
        self.window = window
        self.currentMap = currentMap
        self.playerUnits = playerUnits
        self.enemyUnits = enemyUnits
        self.cursor = Cursor()
        self.actionMenu = ActionMenu(window, currentMap.screenWidth, currentMap.screenHeight)
        self.mapHealthMenu = MapHealthMenu(window, currentMap.screenWidth, currentMap.screenHeight)
        self.mapHealthMenu.setCurrentUnit(self.getTileCursorIsOn().currentUnit)
        self.TurnManager = TurnManager()
        self.activeUnits = set()
        self.getTileCursorIsOn().highlighted()

        self.selectedUnitPrevPos = None
        self.selectedUnitTilesInRange = []
        self.selectedUnitAttackRangeTiles = []
        self.unitIsPlaced = False
        self.unitsInRange = set()
        
        self.startTurn()

    """ 
        Turn state -- related to who's turn it is and what to do when a turn 
        begins or ends
    """
    def startTurn(self):
        print("Turn Start")
        for unit in self.playerUnits:
            unit.active = True
            self.activeUnits.add(unit)

    def endTurn(self):
        print("Turn Over")

    def startEnemyPhase(self):
        print("start enemy phase")
        
    """
        End Turn State
    """

    """
        Movement -- Functions related to the selection and placement of units
    """
    def selectUnit(self):
        if (self.getTileCursorIsOn().currentUnit != None):
            self.unitSelectedCursor()
            self.showMovementAndAttackRange()
            self.selectedUnitPrevPos = [self.cursor.pos[0], self.cursor.pos[1]]

    def placeUnit(self):
        if (type(self.cursor.unitSelected) == PlayerUnit and self.getTileCursorIsOn() in self.selectedUnitTilesInRange and (self.getTileCursorIsOn().currentUnit == None or self.getTileCursorIsOn().currentUnit == self.cursor.unitSelected)):
            self.cursor.unitSelected.currentTile.setCurrentUnit(None)
            self.cursor.unitSelected.setCurrentTile(self.getTileCursorIsOn())
            self.getTileCursorIsOn().setCurrentUnit(self.cursor.unitSelected)
            self.actionMenu.reset()
            self.actionMenu.checkPos(self.getTileCursorIsOn())
            self.unitIsPlaced =True
            self.unitsInRange = self.getUnitsInAttackRange(self.cursor.unitSelected)
            if (len(self.unitsInRange) > 0):
                self.actionMenu.addAttack()

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
            tile.reset()
        self.selectedUnitTilesInRange = []
        self.selectedUnitAttackRangeTiles = []
        self.selectedUnitPrevPos = None
        self.cursor.setUnitSelected(None)
        self.unitIsPlaced = False
        self.unitsInRange = set()
        if (len(self.activeUnits) <= 0):
            self.endTurn()
            self.startTurn()
        
    def selectMenuOption(self):
        action = self.actionMenu.menuItems[self.actionMenu.selectedIndex]
        playerUnit = self.cursor.unitSelected
        if (action == "Attack"):
            print("Attack")
            units = list(self.unitsInRange)
            unit = units[0]
            currentHP = unit.hp
            unit.hp -= max(0, playerUnit.strength - unit.defense)
            print("Units hp was " +str(currentHP) + " now it is " + str(unit.hp))
            if (unit.hp <= 0):
                self.removeUnit(unit)
            else:
                enemyRange = self.getUnitsInAttackRange(unit)
                if (playerUnit in enemyRange):
                    print("Counter Attack")
                    playerUnit.hp -= max(0, unit.strength - playerUnit.defense)
                    print("Player unit hit for " + str(max(0, unit.strength - playerUnit.defense)) + " damage")
                    if (playerUnit.hp <= 0):
                        self.removeUnit(playerUnit)
                        print(str(playerUnit) + " Died")
        if (action == "Wait"):
            pass
        playerUnit.active = False
        self.activeUnits.remove(self.cursor.unitSelected)
        self.cleanupAfterAction()
    """
        End Movement
    """
    ## finds the tiles that the current unit can move to and changes their color,
    ## then finds the tiles that a unit can attack (but not move to) and makes them a different color
    def showMovementAndAttackRange(self):
        oppositeType = EnemyUnit
        if type(self.cursor.unitSelected) == EnemyUnit:
            oppositeType = PlayerUnit
        currentTile = self.getTileCursorIsOn()
        attackRange = self.cursor.unitSelected.attackRange
        movement = self.cursor.unitSelected.mov 
        queue = []
        attackQueue = []

        queue.append(currentTile)
        currentTile.setColor(blue)
        self.selectedUnitTilesInRange.append(currentTile)
        self.selectedUnitAttackRangeTiles.append(currentTile)
        while (len(queue) > 0):
            currentTile = queue.pop(0)
            if currentTile.distance < movement:
                for tile in currentTile.adjList:
                    if not tile.visited:
                        if type(tile.currentUnit) != oppositeType:
                            tile.visited = True
                            tile.distance = currentTile.distance+1
                            tile.setColor(blue)
                            self.selectedUnitTilesInRange.append(tile)
                            self.selectedUnitAttackRangeTiles.append(tile)
                            queue.append(tile)
                        else:
                            tile.visited = True
                            tile.setColor(red)
                            self.selectedUnitAttackRangeTiles.append(tile)
                            attackQueue.append(tile)
            if currentTile.distance < movement+attackRange:
                for tile in currentTile.adjList:
                    if not tile.visited:
                        tile.visited = True
                        tile.distance = currentTile.distance+1
                        tile.setColor(red)
                        self.selectedUnitAttackRangeTiles.append(tile)
                        queue.append(tile)
        ## run bfs again on each of the tiles in the attack queue
        ## this is to get any tiles that can be attacked but were hidden behind an enemy
        for startingTile in attackQueue:
            tmpQueue = []
            tmpQueue.append(startingTile)
            while(len(tmpQueue) > 0):
                currentTile = tmpQueue.pop(0)
                if (currentTile.distance < attackRange-1):
                    for tile in currentTile.adjList:
                        if not tile.visited:
                            tile.visited = True
                            tile.distance = currentTile.distance+1
                            tile.setColor(red)
                            self.selectedUnitAttackRangeTiles.append(tile)
                            tmpQueue.append(tile)

    

    def getUnitsInAttackRange(self, unit):
        for tile in self.selectedUnitAttackRangeTiles:
            tile.setColor(tile.defaultColor)
        tile = unit.currentTile
        attackRange = unit.attackRange+1
        cursorPosX = tile.heightIndex
        cursorPosY = tile.widthIndex
        oppositeType = EnemyUnit
        if type(unit) == EnemyUnit:
            oppositeType = PlayerUnit
        unitsInRange = set()
        tmpVal = attackRange
        for i in range(attackRange):
            for j in range(tmpVal):
                if (cursorPosX+i <= self.currentMap.width and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].setColor(red)
                    if (type(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].currentUnit) == oppositeType):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX+i][cursorPosY+j].currentUnit)
                if (cursorPosX-i >= 0 and cursorPosY-j >= 0):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].setColor(red)
                    if (type(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].currentUnit) == oppositeType):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX-i][cursorPosY-j].currentUnit)
                if (cursorPosX+i < self.currentMap.width and cursorPosY - j >= 0):
                    self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].setColor(red)
                    if (type(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].currentUnit) == oppositeType):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX+i][cursorPosY-j].currentUnit)
                if (cursorPosX-i >= 0 and cursorPosY+j < self.currentMap.height):
                    self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].setColor(red)
                    if (type(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].currentUnit) == oppositeType):
                        unitsInRange.add(self.currentMap.Tiles[cursorPosX-i][cursorPosY+j].currentUnit)
            tmpVal-=1
        return unitsInRange

    def moveCursor(self, direction):
        self.getTileCursorIsOn().unhighlighted()
        if (direction == "left"):
            self.cursor.pos[1] -= 1
        elif (direction == "right"):
            self.cursor.pos[1] += 1
        elif (direction == "up"):
            self.cursor.pos[0] -= 1
        elif (direction == "down"):
            self.cursor.pos[0] += 1
        if (self.getTileCursorIsOn().posX < self.currentMap.tileSize ):
            self.currentMap.scrollLeft()
        elif (self.getTileCursorIsOn().posX > self.currentMap.screenWidth - self.currentMap.tileSize):
            self.currentMap.scrollRight()
        elif (self.getTileCursorIsOn().posY < self.currentMap.tileSize ):
            self.currentMap.scrollUp()
        elif (self.getTileCursorIsOn().posY > self.currentMap.screenHeight - self.currentMap.tileSize):
            self.currentMap.scrollDown()
        self.getTileCursorIsOn().highlighted()
        if (self.getTileCursorIsOn().currentUnit!=None):
            self.mapHealthMenu.checkPos(self.getTileCursorIsOn())
            self.mapHealthMenu.setCurrentUnit(self.getTileCursorIsOn().currentUnit)

    def getTileCursorIsOn(self):
        return self.currentMap.Tiles[self.cursor.pos[0]][self.cursor.pos[1]]

    def unitSelectedCursor(self):
        self.cursor.setUnitSelected(self.getTileCursorIsOn().currentUnit)
        
    def removeUnit(self, unit):
        if (type(unit) == EnemyUnit):
            self.enemyUnits.remove(unit)
        else:
            self.playerUnits.remove(unit)
        currentTile = unit.currentTile
        currentTile.setCurrentUnit(None)
        unit.setCurrentTile(None)

    def draw(self):
        self.currentMap.draw()
        for unit in self.playerUnits:
            unit.draw()
        for unit in self.enemyUnits:
            unit.draw()
        if (self.getTileCursorIsOn().currentUnit!=None):
            self.mapHealthMenu.checkPos(self.getTileCursorIsOn())
            self.mapHealthMenu.draw()
        if (self.unitIsPlaced):
            self.actionMenu.draw()

    