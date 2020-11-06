from cursor import Cursor
from ActionMenu import ActionMenu
from MapHealthMenu import MapHealthMenu
from inventory import Inventory
from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit
from movement import Movement
from Combat import Combat
import copy
import random

red = (185, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

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
        self.inventory = Inventory(window, currentMap.screenWidth, currentMap.screenHeight)
        self.activeUnits = set()
        self.getTileCursorIsOn().highlighted()
        
        self.unitSelected = False
        self.unitIsPlaced = False
        self.attacking = False
        self.inventoryOpen = False
        self.movement = Movement(currentMap)
        self.combat = Combat(window, currentMap)
        self.startTurn()

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
            ## TODO find closest unit to enemy
            closestUnit = self.movement.findClosestOppositeUnit(enemy)
            print("Closest unit : " + closestUnit.name)
            ## find path to closest unit
            path = self.movement.findPath(enemy, closestUnit.currentTile)
            print("path for " + enemy.name)
            for tile in path:
                print(tile)
            ## TODO move unit to closest possible tile
            ## this area needs a lot of work ... 
            if (closestUnit not in self.combat.getUnitsInAttackRange(enemy)):
                index = min(len(path)-1, enemy.mov-1)
                while(index > 0 and (path[index].currentUnit != None or path[index].currentUnit == enemy)):
                    index-=1
                    
                print(index)
                if (index < 0):
                    index = 0
                tileToMoveTo = path[index]
                enemy.currentTile.setCurrentUnit(None)
                enemy.setCurrentTile(tileToMoveTo)
                tileToMoveTo.setCurrentUnit(enemy)

                ## TODO if possible, Attack!!

            ## get targets in range of enemy
            targets = self.combat.getUnitsInAttackRange(enemy)
            if (len(targets) > 0):
                self.combat.currentUnit = enemy
                self.combat.currentTarget = targets[0]
                self.combat.doMathForAttack(enemy, targets[0])
                self.combat.startAttack()
                
        self.currentMap.reset()


    def attack(self):
        self.combat.startAttack()
        if (self.combat.currentUnit.hp <=0):
            self.removeUnit(self.combat.currentUnit)
        if (self.combat.currentTarget.hp <= 0):
            self.removeUnit(self.combat.currentTarget)
        self.attacking = False              
        self.currentMap.reset()
        self.combat.currentUnit.active = False
        self.activeUnits.remove(self.combat.currentUnit)
        self.combat.endCombat()
        self.cleanupAfterAction()

    def selectUnit(self):
        if (self.getTileCursorIsOn().currentUnit != None and self.getTileCursorIsOn().currentUnit.active):
            self.unitSelected = True
            self.movement.currentUnit = self.getTileCursorIsOn().currentUnit
            self.cursor.selectedUnitPreviousPos = copy.deepcopy(self.cursor.pos)
            self.movement.selectedUnitPreviousTile = self.getTileCursorIsOn()
            self.movement.findTilesInRange(self.getTileCursorIsOn().currentUnit)
        elif (type(self.getTileCursorIsOn().currentUnit) == EnemyUnit):
            self.movement.findTilesInRange(self.getTileCursorIsOn().currentUnit)

    def placeUnit(self):
        if (self.getTileCursorIsOn().selectable == True and (self.getTileCursorIsOn().currentUnit == None or self.getTileCursorIsOn().currentUnit == self.movement.currentUnit)):
            self.movement.moveCurrentUnitToTile(self.getTileCursorIsOn())
            self.actionMenu.reset()
            self.actionMenu.checkPos(self.getTileCursorIsOn())
            self.unitIsPlaced =True
            self.combat.unitsInRange = self.combat.getUnitsInAttackRange(self.movement.currentUnit)
            print(len(self.combat.unitsInRange))
            if (len(self.combat.unitsInRange) > 0):
                self.actionMenu.addAttack()
            if (len(self.movement.currentUnit.inventory) > 0 or len(self.movement.currentUnit.weapons) > 0):
                self.actionMenu.addInventory()

    def resetSelectedUnit(self):
        print("reset called")
        self.unitSelected = False
        self.movement.moveCurrentUnitToTile(self.movement.selectedUnitPreviousTile)
        self.getTileCursorIsOn().unhighlighted()
        self.cursor.pos = self.cursor.selectedUnitPreviousPos
        self.currentMap.reset()
        self.getTileCursorIsOn().highlighted()
        self.unitIsPlaced = False
        self.movement.currentUnit = None
        if self.attacking:
            self.attacking = False
            self.combat.endCombat()
        
    def cleanupAfterAction(self): 
        self.currentMap.reset()
        self.selectedUnitPrevPos = None
        self.movement.currentUnit = None
        self.unitIsPlaced = False
        self.unitSelected = False
        if (len(self.activeUnits) <= 0):
            self.endTurn()
            self.startTurn()
        
    def selectMenuOption(self):
        action = self.actionMenu.menuItems[self.actionMenu.selectedIndex]
        playerUnit = self.movement.currentUnit
        if (action == "Attack"):
            self.combat.startCombat(playerUnit)
            self.attacking = True
        if (action == "Items"):
            self.inventoryOpen = True
            self.inventory.setCurrentUnit(playerUnit)
        if (action == "Wait"):
            playerUnit.active = False
            self.activeUnits.remove(playerUnit) 
            self.cleanupAfterAction()
               
 
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
        if (self.unitIsPlaced and not self.attacking and not self.inventoryOpen):
            self.actionMenu.draw() 
        elif (self.attacking):
            self.combat.draw()
        elif (self.inventoryOpen):
            self.inventory.draw()