import pygame
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
        self.__maxHp = 15
        self.__hp    = self.__maxHp
        self.__str   = 5
        self.__def   = 3
        self.__spd   = 4
        self.__skl   = 4
        self.__lck   = 0
        self.__mov   = 5

        # growths
        self.__hpG  = 50
        self.__strG = 50
        self.__defG = 50
        self.__spdG = 50
        self.__sklG = 50
        self.__lckG = 50
        
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
        match stat:
            case Stat.HP:
                self.__hp = value
            case Stat.MAX_HP:
                self.__maxHp = value
            case Stat.STR:
                self.__str = value
            case Stat.DEF:
                self.__def = value
            case Stat.SPD:
                self.__spd = value
            case Stat.SKL:
                self.__skl = value
            case Stat.LCK:
                self.__lck = value
            case Stat.MOV:
                self.__mov = value
            case _:
                print(f"WARNING : stat {stat} not recognized")

    def getStat(self, stat):
        match stat:
            case Stat.HP:
                return self.__hp
            case Stat.MAX_HP:
                return self.__maxHp
            case Stat.STR:
                return self.__str
            case Stat.DEF:
                return self.__def
            case Stat.SPD:
                return self.__spd
            case Stat.SKL:
                return self.__skl
            case Stat.LCK:
                return self.__lck
            case Stat.MOV:
                return self.__mov
            case _:
                print(f"WARNING : stat {stat} not recognized")

    def addToStat(self, index, amount):
        if index == 0:
            self.__maxHp += amount
        if index == 1:
            self.__str += amount
        if index == 2:
            self.__def += amount
        if index == 3:
            self.__spd += amount
        if index == 4:
            self.__skl += amount
        if index == 5:
            self.__lck += amount

    def getGrowths(self):
        return [self.hpG, self.attackG, self.defenseG, self.speedG, self.skillG, self.luckG]

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
            self.__hp = min(self.__maxHp, self.__hp + amount)

    def removeHp(self, amount):
        if amount > 0:
            self.__hp = max(0, self.__hp - amount)

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
        healthPercent = self.__hp/self.__maxHp
        color = (0, 255, 0)
        if healthPercent < 0.2:
            color = (255, 0, 0)
        elif healthPercent < 0.5:
            color = (238, 255, 0)
        pygame.draw.rect(screen, color, pygame.Rect(self.X*tileSize + xCamera, (self.Y*tileSize)+tileSize-5 + yCamera, healthPercent * tileSize, 5))