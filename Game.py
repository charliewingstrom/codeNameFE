from cursor import Cursor
from ActionMenu import ActionMenu
from MapHealthMenu import MapHealthMenu
from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit
from TurnManager import TurnManager
from movement import Movement
import copy
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
        self.currentSelectedUnit = None
        self.selectedUnitPreviousTile = None
        self.unitIsPlaced = False
        self.unitsInRange = set()
        
        self.movement = Movement(self.currentMap)
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
        self.startEnemyPhase()

    def startEnemyPhase(self):
        print("start enemy phase")
        
        for enemy in self.enemyUnits:
            self.currentMap.reset()
            ## TODO find closest unit to enemy
            closestUnit = self.movement.findClosestOppositeUnit(enemy)
            ## find path to closest unit
            self.currentMap.reset()
            path = self.movement.findPath(enemy, closestUnit.currentTile)
            print(path)
            ## TODO move unit to closest possible tile

            ## TODO if possible, Attack!!

    """
        End Turn State
    """

    def selectUnit(self):
        if (self.getTileCursorIsOn().currentUnit != None and self.getTileCursorIsOn().currentUnit.active):
            self.currentSelectedUnit = self.getTileCursorIsOn().currentUnit
            self.cursor.selectedUnitPreviousPos = copy.deepcopy(self.cursor.pos)
            self.selectedUnitPreviousTile = self.getTileCursorIsOn()
            self.movement.findTilesInRange(self.getTileCursorIsOn().currentUnit)

    def placeUnit(self):
        if (self.getTileCursorIsOn().selectable == True):
            self.currentSelectedUnit.currentTile.setCurrentUnit(None)
            self.currentSelectedUnit.setCurrentTile(self.getTileCursorIsOn())
            self.getTileCursorIsOn().setCurrentUnit(self.currentSelectedUnit)
            self.actionMenu.reset()
            self.actionMenu.checkPos(self.getTileCursorIsOn())
            self.unitIsPlaced =True
            #self.unitsInRange = self.getUnitsInAttackRange(self.cursor.unitSelected)
            if (len(self.unitsInRange) > 0):
                self.actionMenu.addAttack()

    def resetSelectedUnit(self):
        print("reset called")
        self.currentSelectedUnit.setCurrentTile(self.selectedUnitPreviousTile)
        self.selectedUnitPreviousTile.setCurrentUnit(self.currentSelectedUnit)
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos = self.cursor.selectedUnitPreviousPos
        self.getTileCursorIsOn().highlighted()
        self.currentMap.reset()
        self.unitIsPlaced = False
        self.currentSelectedUnit = None

        
    def cleanupAfterAction(self): 
        self.currentMap.reset()
        self.selectedUnitPrevPos = None
        self.currentSelectedUnit = None
        self.unitIsPlaced = False
        self.unitsInRange = set()
        if (len(self.activeUnits) <= 0):
            self.endTurn()
            self.startTurn()
        
    def selectMenuOption(self):
        action = self.actionMenu.menuItems[self.actionMenu.selectedIndex]
        playerUnit = self.currentSelectedUnit
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
        self.activeUnits.remove(playerUnit)
        self.cleanupAfterAction()
 
   


    """ 
    def showMovementAndAttackRange(self, unit):
        oppositeType = EnemyUnit
        if type(unit) == EnemyUnit:
            oppositeType = PlayerUnit
        currentTile = self.getTileCursorIsOn()
        attackRange = unit.attackRange
        movement = unit.mov 
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

    """
    """    
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
    """

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

    