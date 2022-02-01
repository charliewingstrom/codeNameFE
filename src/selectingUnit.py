# TODO remake this to handle selecting units generally
class SelectingUnit(object):

    def __init__(self):
        self.__unitsInRange = []
        self.__selectionIndex  = 0

    def getUnitsInRange(self, tilesInRange, units):
        self.__unitsInRange = []
        self.__selectionIndex  = 0
        for tile in tilesInRange:
            if tile.currentUnit != None and tile.currentUnit in units:
                self.__unitsInRange.append(tile.currentUnit)
        return self.__unitsInRange

    def getTargetedUnit(self):
        targetedUnit    = None
        numUnitsInRange = len(self.__unitsInRange)
        if numUnitsInRange > 0 and self.__selectionIndex < numUnitsInRange:
            targetedUnit = self.__unitsInRange[self.__selectionIndex]
        return targetedUnit

    def moveUp(self):
        if self.__selectionIndex < len(self.__unitsInRange) - 1:
            self.__selectionIndex += 1
        else:
            self.__selectionIndex = 0
    
    def moveDown(self):
        if self.__selectionIndex > 0:
            self.__selectionIndex -= 1
        else:
            self.__selectionIndex = len(self.__unitsInRange) - 1

    def areUnitsInRange(self):
        return len(self.__unitsInRange) > 0