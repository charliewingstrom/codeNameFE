import pygame

from pathlib    import Path
from enum       import Enum, auto

from inventory import Inventory
from animation import Animation


protagPicA = pygame.image.load(Path(__file__).parent / "../assets/protag_A.png")
protagPicB = pygame.image.load(Path(__file__).parent / "../assets/protag_B.png")

combatUnit1 = pygame.image.load(Path(__file__).parent / "../assets/Combat-1.png")
combatUnit2 = pygame.image.load(Path(__file__).parent / "../assets/Combat-2.png")
combatUnit3 = pygame.image.load(Path(__file__).parent / "../assets/Combat-3.png")
combatUnit4 = pygame.image.load(Path(__file__).parent / "../assets/Combat-4.png")
combatUnit5 = pygame.image.load(Path(__file__).parent / "../assets/Combat-5.png")
combatUnit6 = pygame.image.load(Path(__file__).parent / "../assets/Combat-6.png")

class UnitType(Enum):
    Player  = auto()
    Enemy   = auto()
    Other   = auto()

class Unit():

    def __init__(self, X, Y, tileSize, isPlayer = False):
        self.name = "generic"
        self.level = 1
        self.exp = 0
        if isPlayer:
            self.__unitType = UnitType.Player
        else:
            self.__unitType = UnitType.Enemy 
        
        # stats
        self.maxHp = 15
        self.hp = self.maxHp
        self.attack = 5
        self.defense = 3
        self.speed = 4
        self.skill = 4
        self.luck = 0
        self.mov = 5

        # growths
        self.hpG = 50
        self.attackG = 50
        self.defenseG = 50
        self.speedG = 50
        self.skillG = 50
        self.luckG = 50
        self.inventory = Inventory()
        self.X = X
        self.Y = Y

        self.fieldPics = [pygame.transform.scale(protagPicA, (tileSize, tileSize)), pygame.transform.scale(protagPicB, (tileSize, tileSize))] 
        self.aniTimer = 5
        self.combatAnimation = Animation([combatUnit1,combatUnit2, combatUnit3,combatUnit4, combatUnit5, combatUnit6,combatUnit5, combatUnit4, combatUnit3, combatUnit2, combatUnit1])

        self.active = True

    def __repr__(self):
        return f"Unit({self.name})"
        
    def getIsPlayer(self):
        return self.__unitType == UnitType.Player
        
    def getStats(self):
        return [self.maxHp, self.attack, self.defense, self.speed, self.skill, self.luck]

    def addToStat(self, index, amount):
        if index == 0:
            self.maxHp += amount
        if index == 1:
            self.attack += amount
        if index == 2:
            self.defense += amount
        if index == 3:
            self.speed += amount
        if index == 4:
            self.skill += amount
        if index == 5:
            self.luck += amount

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
        healthPercent = self.hp/self.maxHp
        color = (0, 255, 0)
        if healthPercent < 0.2:
            color = (255, 0, 0)
        elif healthPercent < 0.5:
            color = (238, 255, 0)
        pygame.draw.rect(screen, color, pygame.Rect(self.X*tileSize + xCamera, (self.Y*tileSize)+tileSize-5 + yCamera, healthPercent * tileSize, 5))