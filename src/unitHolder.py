class UnitHolder():

    def __init__(self):
        self.__enemyUnits   = set()
        self.__playerUnits  = set()
        self.__mapToEnemies = {}

    def addUnit(self, unit):
        if unit.getIsPlayer():
            self.__playerUnits.add(unit)

    def setEnemiesToMap(self, tileMap, enemies):
        self.__mapToEnemies[tileMap] = set(enemies)

    def removeUnit(self, unit):
        # discard does not throw an error if unit is not in units
        if unit.getIsPlayer():
            self.__playerUnits.discard(unit)
        else:
            self.__enemyUnits.discard(unit)

    def resetForNextTurn(self):
        for unit in self.__playerUnits.union(self.__enemyUnits):
            unit.active = True

    def drawUnits(self, screen, tileSize, xCamera, yCamera):
        for unit in self.__playerUnits.union(self.__enemyUnits):
            unit.draw(screen, tileSize, xCamera, yCamera)

    def addUnitsToNewMap(self, tileMap):
        for unit in self.__playerUnits: 
            if tileMap.addUnitToStartTile(unit):
                break

    def getActiveEnemyUnit(self):
        toReturn = None
        for unit in self.__enemyUnits:
            if unit.active == True:
                toReturn = unit
                unit.active = False
                break
        return toReturn

    def getEnemies(self):
        return self.__enemyUnits

    def getPlayers(self):
        return self.__playerUnits

    def moveToNextMap(self, tileMap):
        self.__enemyUnits = self.__mapToEnemies.get(tileMap)
        for unit in self.__playerUnits:
            tileMap.addUnitToStartTile(unit)
