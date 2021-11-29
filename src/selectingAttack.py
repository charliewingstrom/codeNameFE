
import pygame

class SelectingAttack(object):

    def __init__(self):
        self.__unitsInRange = []
        self.__attackIndex  = 0

        pass

    def getEnemyUnitsInRange(self, tilesInRange, unitHolder):
        self.__unitsInRange = []
        self.__attackIndex  = 0
        for tile in tilesInRange:
            tile.attackable = True
            if tile.currentUnit != None and tile.currentUnit in unitHolder.getEnemies():
                self.__unitsInRange.append(tile.currentUnit)
        return self.__unitsInRange

    def getTargetedUnit(self):
        targetedUnit    = None
        numUnitsInRange = len(self.__unitsInRange)
        if numUnitsInRange > 0 and self.__attackIndex < numUnitsInRange:
            targetedUnit = self.__unitsInRange[self.__attackIndex]
        return targetedUnit

    def moveUp(self):
        if self.__attackIndex < len(self.__unitsInRange) - 1:
            self.__attackIndex += 1
        else:
            self.__attackIndex = 0
    
    def moveDown(self):
        if self.__attackIndex > 0:
            self.__attackIndex -= 1
        else:
            self.__attackIndex = len(self.__unitsInRange) - 1

    def areUnitsInRange(self):
        return len(self.__unitsInRange) > 0