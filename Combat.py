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

        self.selectingTarget = False
        self.selectingWeapon = False
        self.checkingNumbers = False

        ## for attack menu calculation
        self.damage = 0
        self.hit = 0
        self.crit = 0

    def startCombat(self, unit):
        self.currentTarget = self.unitsInRange[self.targetIndex]
        self.currentTarget.currentTile.borderColor = yellow
        self.currentUnit = unit    
    def endCombat(self):
        self.currentTarget.currentTile.borderColor = self.currentTarget.currentTile.defaultBorderColor
        self.targetIndex = 0
        self.currentUnit = None
        self.currentTarget = None
        
    def changeAttackTarget(self):
        currentTargetTile = self.currentTarget.currentTile
        currentTargetTile.borderColor = currentTargetTile.defaultBorderColor
        if self.targetIndex+1 == len(self.unitsInRange):
            self.targetIndex = 0
        else:
            self.targetIndex+=1
        self.currentTarget = self.unitsInRange[self.targetIndex]
        self.currentTarget.currentTile.borderColor = yellow
        
    def doMathForAttack(self, attackingUnit, defendingUnit):
        #get damage
        damage = max(0, attackingUnit.strength - defendingUnit.defense)
        #get hit chance

        #get crit chance

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
            if (currentTile.distance <= unit.attackRange):

                currentTile.setColor(red)
                if (type(currentTile.currentUnit) == oppositeType):
                    unitsInRange.append(currentTile.currentUnit)
                for tile in currentTile.adjList:
                    if not tile.visited:
                        tile.visited = True
                        tile.distance = currentTile.distance+1
                        queue.append(tile)
        return unitsInRange
                        
    
    def drawSelectingWeapon(self):
        pass
    
    def drawSelectingNumbers(self):
        pass 

    
    def draw(self):
        pass
        if (self.selectingWeapon):
            self.drawSelectingWeapon()
        elif (self.checkingNumbers):
            self.drawCheckingNumbers()
