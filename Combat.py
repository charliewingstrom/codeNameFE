from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit

red = (185, 0, 0)
yellow = (255, 255, 23)
class Combat(object):

    def __init__(self,currentMap):
        self.currentMap = currentMap
        self.unitsInRange = []
        self.targetIndex = 0
        self.currentTarget = None
        self.currentUnit = None

        ## for attack menu calculation
        self.damage = 0
        self.hit = 0
        self.crit = 0

    def startCombat(self, unit):
        self.currentTarget = self.unitsInRange[self.targetIndex]
        self.currentTarget.currentTile.borderColor = yellow
        self.currentUnit = unit 
        self.doMathForAttack(self.currentUnit, self.currentTarget)
        print("currentWeapon: " + str(self.currentUnit.weapons[self.currentUnit.equippedWeaponIndex]))
        print("attack: " + str(self.damage))
        print("hit: " + str(self.hit))
        print("crit: " + str(self.crit))  
        self.checkUIPos()

    def endCombat(self):
        self.currentTarget.currentTile.borderColor = self.currentTarget.currentTile.defaultBorderColor
        self.unitsInRange = []
        self.targetIndex = 0
        self.currentUnit = None
        self.currentTarget = None

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
        self.doMathForAttack(self.currentUnit, self.currentTarget)
        self.unitsInRange = self.getUnitsInAttackRange(self.currentUnit)
        print("currentWeapon: " + str(self.currentUnit.weapons[self.currentUnit.equippedWeaponIndex]))
        print("attack: " + str(self.damage))
        print("hit: " + str(self.hit))
        print("crit: " + str(self.crit))


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

    def checkUIPos(self):
        pass
    def draw(self):
        pass


        
