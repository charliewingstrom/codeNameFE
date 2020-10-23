from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit

red = (185, 0, 0)
yellow = (255, 255, 23)
class Combat(object):

    def __init__(self,currentMap):
        self.currentMap = currentMap
        self.unitsInRange = []
        self.targetIndex = 0

    def startCombat(self):
        self.targetIndex = 0
        self.unitsInRange[self.targetIndex].currentTile.borderColor = yellow

    def attack(self):
        print("Here")
        
    def endCombat(self):
        self.unitsInRange[self.targetIndex].currentTile.borderColor = self.unitsInRange[self.targetIndex].currentTile.defaultBorderColor

        
    def changeAttackTarget(self):
        currentTargetTile = self.unitsInRange[self.targetIndex].currentTile
        currentTargetTile.borderColor = currentTargetTile.defaultBorderColor
        if self.targetIndex+1 == len(self.unitsInRange):
            self.targetIndex = 0
        else:
            self.targetIndex+=1
        self.unitsInRange[self.targetIndex].currentTile.borderColor = yellow
        
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
                        

        
