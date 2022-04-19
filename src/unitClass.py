from enum import Enum, auto
from unit import Stat
class UnitClassType(Enum):
    BANDIT = auto()
    LORD   = auto()
    KNIGHT = auto()
    MAGE   = auto()
    GUNNER = auto()
    ARCHER = auto()

class UnitClass(object):

    classes = {}

    def getClass(classType):
        return UnitClass.classes[UnitClassType[classType]]

    def __init__(self, growths, usesMagic):
        self.__growths      = growths
        self.__usesMagic    = usesMagic

    def usesMagic(self):
        return self.__usesMagic

    def getGrowths(self):
        return self.__growths.copy()

banditGrowths = {
    Stat.MAX_HP : 5,
    Stat.STR    : 5,
    Stat.DEF    : 5,
    Stat.SPD    : 5,
    Stat.SKL    : 5,
    Stat.LCK    : 5,
}

UnitClass.classes[UnitClassType.BANDIT] = UnitClass(banditGrowths, False)

lordGrowths = {
    Stat.MAX_HP : 10,
    Stat.STR    : 10,
    Stat.DEF    : 3,
    Stat.SPD    : 6,
    Stat.SKL    : 7,
    Stat.LCK    : 5,
}

UnitClass.classes[UnitClassType.LORD] = UnitClass(lordGrowths, False)

knightGrowths = {
    Stat.MAX_HP : 10,
    Stat.STR    : 10,
    Stat.DEF    : 10,
    Stat.SPD    : 0,
    Stat.SKL    : 0,
    Stat.LCK    : 5,
}

UnitClass.classes[UnitClassType.KNIGHT] = UnitClass(knightGrowths, False)

## we are done here, don't let users create UnitClasses
UnitClass.__init__ = None