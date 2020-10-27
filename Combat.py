import pygame
from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit

red = (185, 0, 0)
yellow = (255, 255, 23)
class Combat(object):

    def __init__(self,window, currentMap):
        self.window = window
        self.currentMap = currentMap
        self.unitsInRange = []
        self.targetIndex = 0
        self.currentTarget = None
        self.currentUnit = None

        ## for attack menu calculation
        self.damage = 0
        self.hit = 0
        self.crit = 0

        self.posX = currentMap.screenWidth - 300
        self.posY = 50

    def startCombat(self, unit):
        self.setCurrentTarget()
        self.currentUnit = unit 
        self.doMathForAttack(self.currentUnit, self.currentTarget)
        self.checkPos()

    def endCombat(self):
        self.currentTarget.currentTile.borderColor = self.currentTarget.currentTile.defaultBorderColor
        self.unitsInRange = []
        self.targetIndex = 0
        self.currentUnit = None
        self.currentTarget = None
        self.damage = 0
        self.hit = 0
        self.crit = 0
        
    def doMathForAttack(self, attackingUnit, defendingUnit):
        #get damage
        equippedWeapon = attackingUnit.weapons[attackingUnit.equippedWeaponIndex]
        self.damage = max(0, attackingUnit.strength + equippedWeapon.strength - defendingUnit.defense)
        #get hit chance
        self.hit = (attackingUnit.dex * 2) + equippedWeapon.hit - (defendingUnit.dex * 2)
        #get crit chance
        self.crit = (equippedWeapon.crit + attackingUnit.spd) - defendingUnit.spd

    def getUnitsInAttackRange(self, unit):
        self.currentMap.reset()
        for row in self.currentMap.Tiles:
            for tile in row:
                tile.distance = 0
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

                currentTile.setColor(red)
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

        pygame.draw.rect(self.window, (255,255,255), (self.posX, self.posY, 150, 400))

        self.window.blit(unitName, unitNameRect)
        self.window.blit(unitWeapon, unitWeaponRect)
        self.window.blit(hp, hpRect)
        self.window.blit(dmg, dmgRect)
        self.window.blit(hit, hitRect)
        self.window.blit(crit, critRect)


        
