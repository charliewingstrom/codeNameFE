import pygame
import random
from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit

red = (185, 0, 0)
yellow = (255, 255, 23)
class Combat(object):

    def __init__(self,window, currentMap):
        self.__window = window
        self.currentMap = currentMap
        self.unitsInRange = []
        self.targetIndex = 0
        self.currentTarget = None
        self.currentUnit = None

        ## for attack menu calculation
        # for attacking unit
        self.damage = 0
        self.hit = 0
        self.crit = 0
        # defending unit
        self.counterDmg = 0
        self.counterHit = 0
        self.counterCrit = 0

        self.posX = currentMap.screenWidth - 300
        self.posY = 50

    def startCombat(self, unit):
        self.setCurrentTarget()
        self.currentUnit = unit 
        self.doMathForAttack(self.currentUnit, self.currentTarget)
        self.checkPos()

    def endCombat(self):
        self.unitsInRange = []
        self.targetIndex = 0
        self.currentUnit = None
        self.currentTarget = None
        self.damage = 0
        self.hit = 0
        self.crit = 0
        self.counterDmg = 0
        self.counterHit = 0
        self.counterCrit = 0

    def attack(self):
        print(self.currentUnit.name + " attacks with a " + str(self.currentUnit.weapons[self.currentUnit.equippedWeaponIndex]))
        if (self.hit > random.randint(1,101)):
            print("Hit!")
            if (self.crit > random.randint(1,101)):
                print("Crit!!")
                self.damage *= 3
            self.currentTarget.hp -= self.damage
        else:
            print("Miss!")
        # if target unit died
        if (self.currentTarget.hp <= 0):
            self.removeUnit(self.currentTarget)
        # check for possible counter attack
        else:
            targetUnitsInRange = self.getUnitsInAttackRange(self.currentTarget)
            if self.currentUnit in targetUnitsInRange:
                print(self.currentTarget.name + " counters")
                self.doMathForAttack(self.currentTarget, self.currentUnit)
                if (self.hit > random.randint(1,101)):
                    print("Hit!")
                    if (self.crit > random.randint(1,101)):
                        print("Crit!!")
                        self.damage *= 3
                    self.currentUnit.hp -= self.damage  
                    if (self.currentUnit.hp <= 0):
                        self.removeUnit(self.currentUnit)
                        print(self.currentUnit.name + " died")
                else:
                    print("Miss!")
    
    def doMathForAttack(self, attackingUnit, defendingUnit):
        #get damage
        equippedWeapon = attackingUnit.weapons[attackingUnit.equippedWeaponIndex]
        self.damage = max(0, attackingUnit.strength + equippedWeapon.strength - defendingUnit.defense)
        #get hit chance
        self.hit = (attackingUnit.dex * 2) + equippedWeapon.hit + (attackingUnit.luck //2)
        #get crit chance
        self.crit = (equippedWeapon.crit) + (attackingUnit.dex // 2)
        if (attackingUnit in self.getUnitsInAttackRange(defendingUnit)):
            equippedWeapon = defendingUnit.weapons[defendingUnit.equippedWeaponIndex]
            self.counterDmg = max(0, defendingUnit.strength + equippedWeapon.strength - attackingUnit.defense)
            self.counterHit = (defendingUnit.dex*2) + equippedWeapon.hit + (defendingUnit.luck // 2)
            self.counterCrit = (equippedWeapon.crit) + (attackingUnit.dex // 2)

    def getUnitsInAttackRange(self, unit):
        for row in self.currentMap.Tiles:
            for tile in row:
                tile.distance = 0
                tile.visited = False
        oppositeType = EnemyUnit
        if type(unit) == EnemyUnit:
            oppositeType = PlayerUnit

        unitsInRange = []
        currentTile = unit.currentTile
        queue = []
        currentTile.visited=True
        queue.append(currentTile)
        while (len(queue) > 0):
            currentTile = queue.pop(0)
            if (currentTile.distance <= unit.weapons[unit.equippedWeaponIndex].range):
                if (type(currentTile.currentUnit) == oppositeType):
                    unitsInRange.append(currentTile.currentUnit)
                for tile in currentTile.adjList:
                    if not tile.visited:
                        tile.visited = True
                        tile.distance = currentTile.distance+1
                        queue.append(tile)
        return unitsInRange
                        
    def changeEquippedWeaponCurrentUnit(self, direction):
        
        ## what if some units are out of range after switching weapons?
        self.currentUnit.changeCurrentWeapon(direction)
        self.unitsInRange = self.getUnitsInAttackRange(self.currentUnit)
        while(len(self.unitsInRange) <= 0):
            self.currentUnit.changeCurrentWeapon(direction)
            self.unitsInRange = self.getUnitsInAttackRange(self.currentUnit)
        self.setCurrentTarget()
        self.doMathForAttack(self.currentUnit, self.currentTarget)

    def setCurrentTarget(self):
        if (self.targetIndex >= len(self.unitsInRange)):
            self.targetIndex = len(self.unitsInRange) - 1
        self.currentTarget = self.unitsInRange[self.targetIndex]
        self.currentTarget.currentTile.borderColor = yellow

    def changeAttackTarget(self):
        currentTargetTile = self.currentTarget.currentTile
        currentTargetTile.borderColor = currentTargetTile.defaultBorderColor
        if self.targetIndex+1 == len(self.unitsInRange):
            self.targetIndex = 0
        else:
            self.targetIndex+=1
        self.currentTarget = self.unitsInRange[self.targetIndex]
        self.currentTarget.currentTile.borderColor = yellow
        self.doMathForAttack(self.currentUnit, self.currentTarget)
        print("currentWeapon: " + str(self.currentUnit.weapons[self.currentUnit.equippedWeaponIndex]))
        print("attack: " + str(self.damage))
        print("hit: " + str(self.hit))
        print("crit: " + str(self.crit))

    def checkPos(self):
        if (self.currentUnit.currentTile.posX < self.currentMap.screenWidth // 2):
            self.posX = self.currentMap.screenWidth - 300
        else:
            self.posX = 100
        

    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 24)
        
        unitName = font.render(self.currentUnit.name, True, (0, 0, 0))
        unitNameRect = unitName.get_rect()
        unitNameRect.center = (self.posX + 75, self.posY + 25)

        unitWeapon = font.render(str(self.currentUnit.weapons[self.currentUnit.equippedWeaponIndex]), True, (0,0,0))
        unitWeaponRect = unitWeapon.get_rect()
        unitWeaponRect.center = (self.posX+75, self.posY + 60)

        hp = font.render(str(self.currentUnit.hp), True, (0,0,0))
        hpRect = hp.get_rect()
        hpRect.center = (self.posX+25, self.posY + 100)

        dmg = font.render(str(self.damage), True, (0,0,0))
        dmgRect = dmg.get_rect()
        dmgRect.center = (self.posX+25, self.posY + 160)

        hit = font.render(str(self.hit), True, (0, 0, 0))
        hitRect = hit.get_rect()
        hitRect.center = (self.posX+25, self.posY + 220)

        crit = font.render(str(self.crit), True, (0,0,0))
        critRect = crit.get_rect()
        critRect.center = (self.posX+25, self.posY + 280)

        ## counter 
        counterName = font.render(self.currentTarget.name, True, (0, 0, 0))
        counterNameRect = counterName.get_rect()
        counterNameRect.center = (self.posX + 75, self.posY + 375)

        counterHp = font.render(str(self.currentTarget.hp), True, (0,0,0))
        counterHpRect = counterHp.get_rect()
        counterHpRect.center = (self.posX + 125, self.posY + 100)

        counterDmg = font.render(str(self.counterDmg), True, (0,0,0))
        counterDmgRect = counterDmg.get_rect()
        counterDmgRect.center = (self.posX + 125, self.posY + 160)

        counterHit = font.render(str(self.counterHit), True, (0,0,0))
        counterHitRect = counterHit.get_rect()
        counterHitRect.center = (self.posX + 125, self.posY + 220)

        counterCrit = font.render(str(self.counterCrit), True, (0,0,0))
        counterCritRect = counterCrit.get_rect()
        counterCritRect.center = (self.posX + 125, self.posY + 280)

        pygame.draw.rect(self.__window, (255,255,255), (self.posX, self.posY, 150, 400))

        self.__window.blit(unitName, unitNameRect)
        self.__window.blit(unitWeapon, unitWeaponRect)
        self.__window.blit(hp, hpRect)
        self.__window.blit(dmg, dmgRect)
        self.__window.blit(hit, hitRect)
        self.__window.blit(crit, critRect)

        self.__window.blit(counterName, counterNameRect)
        self.__window.blit(counterHp, counterHpRect)
        self.__window.blit(counterDmg, counterDmgRect)
        self.__window.blit(counterHit, counterHitRect)
        self.__window.blit(counterCrit, counterCritRect)

        
