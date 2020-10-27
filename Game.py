from cursor import Cursor
from ActionMenu import ActionMenu
from MapHealthMenu import MapHealthMenu
from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit
from TurnManager import TurnManager
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
        self.TurnManager = TurnManager()
        self.activeUnits = set()
        self.getTileCursorIsOn().highlighted()
        
        self.unitSelected = False
        self.unitIsPlaced = False
        self.attacking = False
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
            ## find path to closest unit
            path = self.movement.findPath(enemy, closestUnit.currentTile)
            ## TODO move unit to closest possible tile
            index = min(len(path)-1, enemy.mov)
            tileToMoveTo = path[index]
            enemy.currentTile.setCurrentUnit(None)
            enemy.setCurrentTile(tileToMoveTo)
            enemy.currentTile.setCurrentUnit(enemy)

            ## TODO if possible, Attack!!

    def attack(self):
        print(self.combat.currentUnit.name + " attacks with a " + str(self.combat.currentUnit.weapons[self.combat.currentUnit.equippedWeaponIndex]))
        if (self.combat.hit > random.randint(1,101)):
            print("Hit!")
            if (self.combat.crit > random.randint(1,101)):
                print("Crit!!")
                self.combat.damage *= 3
            self.combat.currentTarget.hp -= self.combat.damage
        else:
            print("Miss!")
        # if target unit died
        if (self.combat.currentTarget.hp <= 0):
            self.removeUnit(self.combat.currentTarget)
        # check for possible counter attack
        else:
            targetUnitsInRange = self.combat.getUnitsInAttackRange(self.combat.currentTarget)
            if self.combat.currentUnit in targetUnitsInRange:
                print(self.combat.currentTarget.name + " counters")
                self.combat.doMathForAttack(self.combat.currentTarget, self.combat.currentUnit)
                if (self.combat.hit > random.randint(1,101)):
                    print("Hit!")
                    if (self.combat.crit > random.randint(1,101)):
                        print("Crit!!")
                        self.combat.damage *= 3
                    self.combat.currentUnit.hp -= self.combat.damage  
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

    def placeUnit(self):
        if (self.getTileCursorIsOn().selectable == True):
            self.movement.currentUnit.currentTile.setCurrentUnit(None)
            self.movement.currentUnit.setCurrentTile(self.getTileCursorIsOn())
            self.getTileCursorIsOn().setCurrentUnit(self.movement.currentUnit)
            self.actionMenu.reset()
            self.actionMenu.checkPos(self.getTileCursorIsOn())
            self.unitIsPlaced =True
            self.combat.unitsInRange = self.combat.getUnitsInAttackRange(self.movement.currentUnit)
            if (len(self.combat.unitsInRange) > 0):
                self.actionMenu.addAttack()

    def resetSelectedUnit(self):
        print("reset called")
        self.unitSelected = False
        self.movement.currentUnit.setCurrentTile(self.movement.selectedUnitPreviousTile)
        self.movement.selectedUnitPreviousTile.setCurrentUnit(self.movement.currentUnit)
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
            print("Attack")
            self.combat.startCombat(playerUnit)
            self.attacking = True
        if (action == "Wait"):
            self.cleanupAfterAction()
            playerUnit.active = False
            self.activeUnits.remove(playerUnit)    
 
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
        if (self.unitIsPlaced and not self.attacking):
            self.actionMenu.draw() 
        elif (self.attacking):
            self.combat.draw()