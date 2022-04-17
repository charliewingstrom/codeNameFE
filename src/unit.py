import pygame
from copy           import deepcopy
from enum           import Enum, auto
from assetLoader    import AssetLoader
from inventory      import Inventory
from animation      import Animation

class UnitType(Enum):
    Player  = auto()
    Enemy   = auto()
    Other   = auto()

class Stat(Enum):
    MAX_HP  = auto()
    HP      = auto()
    STR     = auto()
    DEF     = auto()
    SPD     = auto()
    SKL     = auto()
    LCK     = auto()
    MOV     = auto()

class Unit():

    def __init__(self, X, Y, tileSize, startingInventory, isPlayer = False):
        self.name           = "generic"
        self.level          = 1
        self.exp            = 0
        self.__unitClass    = None

        if isPlayer:
            self.__unitType = UnitType.Player
        else:
            self.__unitType = UnitType.Enemy 
        
        # stats
        self.__stats = {
            Stat.MAX_HP : 15,
            Stat.HP     : 15, 
            Stat.STR    : 3,
            Stat.DEF    : 3,
            Stat.SPD    : 4,
            Stat.SKL    : 4,
            Stat.LCK    : 0,
            Stat.MOV    : 5
        }

        self.__growths = {
            Stat.HP     : 50,
            Stat.STR    : 50,
            Stat.DEF    : 50,
            Stat.SPD    : 50,
            Stat.SKL    : 50,
            Stat.LCK    : 50,
        }
        
        self.inventory = Inventory()
        for item in startingInventory:
            self.inventory.addItem(item)

        self.X = X
        self.Y = Y

        self.fieldPics = [pygame.transform.scale(AssetLoader.assets["protag_A.png"], (tileSize, tileSize)), pygame.transform.scale(AssetLoader.assets["protag_B.png"], (tileSize, tileSize))] 
        self.aniTimer = 5
        self.combatAnimation = Animation([AssetLoader.assets["Combat-1.png"],AssetLoader.assets["Combat-2.png"], AssetLoader.assets["Combat-3.png"],AssetLoader.assets["Combat-4.png"], AssetLoader.assets["Combat-5.png"], 
                                        AssetLoader.assets["Combat-6.png"],AssetLoader.assets["Combat-5.png"], AssetLoader.assets["Combat-4.png"], AssetLoader.assets["Combat-3.png"], AssetLoader.assets["Combat-2.png"], AssetLoader.assets["Combat-1.png"]])

        self.active = True

    def __repr__(self):
        return f"Unit({self.name})"
        
    def getIsPlayer(self):
        return self.__unitType == UnitType.Player
        
    def setStat(self, stat, value):
        self.__stats[stat] = value

    def getStat(self, stat):
        return self.__stats[stat]

    def addToStat(self, stat, amount):
        self.__stats[stat] += amount

    def getGrowths(self):
        return deepcopy(self.__growths)

    def getEquippedWeapon(self):
        if len(self.getInventory()) > 0:
            return self.getInventory()[0] 
        return None
    
    def getInventory(self):
        return self.inventory.getInventory()

    def getAttackRange(self):
        if len(self.getInventory()) > 0:
            return self.getEquippedWeapon().range
        return [0,0]

    def addHp(self, amount):
        if amount > 0:
            self.__stats[Stat.HP] = min(self.__stats[Stat.MAX_HP], self.__stats[Stat.HP] + amount)

    def removeHp(self, amount):
        if amount > 0:
            self.__stats[Stat.HP] = max(0, self.__stats[Stat.HP] - amount)

    def drawFirstFrame(self, screen, x, y, reverse):
        return self.combatAnimation.drawFirstFrame(screen, x, y, reverse)

    def draw(self, screen, tileSize, xCamera, yCamera):
        screen.blit(self.fieldPics[0], (self.X*tileSize + xCamera, self.Y*tileSize + yCamera))
        self.aniTimer -= 1
        if self.aniTimer < 0:
            tmpPic = self.fieldPics.pop(0)
            self.fieldPics.append(tmpPic)
            self.aniTimer = 5
        
        ## draw health bar 
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.X*tileSize + xCamera, (self.Y*tileSize)+tileSize-5 + yCamera, tileSize, 5))
        healthPercent = self.__stats[Stat.HP]/self.__stats[Stat.MAX_HP]
        color = (0, 255, 0)
        if healthPercent < 0.2:
            color = (255, 0, 0)
        elif healthPercent < 0.5:
            color = (238, 255, 0)
        pygame.draw.rect(screen, color, pygame.Rect(self.X*tileSize + xCamera, (self.Y*tileSize)+tileSize-5 + yCamera, healthPercent * tileSize, 5))