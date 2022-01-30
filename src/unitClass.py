from enum import Enum, auto

class UnitClassType(Enum):
    BANDIT = auto()
    LORD   = auto()
    KNIGHT = auto()
    MAGE   = auto()
    GUNNER = auto()
    ARCHER = auto()

class UnitClass(object):
    def __init__(self):
        # class growths
        self.__hp   = 0
        self.__str  = 0
        self.__def  = 0
        self.__spd  = 0
        self.__skl  = 0
        self.__lck  = 0
        
        self.__usesMagic = False

    def usesMagic(self):
        return self.__usesMagic

    


classes = {}
classes[UnitClassType.BANDIT] = UnitClass()

        