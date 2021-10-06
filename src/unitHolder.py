
class UnitHolder():

    def __init__(self):
        self.__units                = set()
        self.__tooManyPlayerUnits   = False

    def addUnit(self, unit):
        self.__units.add(unit)

    def addUnitSet(self, units : set):
        self.__units = units

    def removeUnit(self, unit, unitTile):
        # discard does not throw an error if unit is not in units
        self.__units.discard(unit)
        if unitTile:
            unitTile.currentUnit = None

    def drawUnits(self, screen, tileSize, xCamera, yCamera):
        for unit in self.__units:
            unit.draw(screen, tileSize, xCamera, yCamera)

    def addPlayerUnitsToNewMap(self, tileMap):
        for unit in self.__units: 
            if not unit.getIsPlayer():
                self.__units.discard(unit)
            else:
                try:
                    tileMap.addUnitToStartTile(unit)
                except:
                    self.__tooManyPlayerUnits = True
