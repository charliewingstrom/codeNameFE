
import pygame
import random
from Tile import Tile

class Unit(object):

    def __init__(self, window, name, currTile = None):
        self.window = window
        self.name = name
        self.currentTile = currTile
        
        self.mov = 5
        
        self.inventory = []
        self.weapons = []
        self.equippedWeaponIndex = 0
        
        self.maxHp = 23
        self.hp = self.maxHp
        self.strength = 6
        self.defense = 4
        self.spd = 5
        self.dex = 5
        self.luck = 5
        
        self.level = 1
        self.exp = 0
        #growths
        self.hpG = 50
        self.strG = 50
        self.defG = 50
        self.spdG = 50
        self.dexG = 50
        self.luckG = 50

        self.active = False

    

    def __str__(self):
        return self.name
        
    def setCurrentTile(self, tile):
        self.currentTile = tile

    def addExp(self, exp):
        self.exp += exp
        if (self.exp > 99):
            self.exp -= 100
            self.level+=1
            self.levelUp()
    def levelUp(self):
        print(self.name + " Levels up")
        if (random.randint(1, 100) <= self.hpG):
            self.hp+=1
            print("Hp + 1")
        if (random.randint(1, 100) <= self.strG):
            self.strength+=1
            print("Str + 1")
        if (random.randint(1, 100) <= self.defG):
            self.defense+=1
            print("Def + 1")
        if (random.randint(1, 100) <= self.spdG):
            self.spd+=1
            print("Spd + 1")
        if (random.randint(1, 100) <= self.dexG):
            self.dex+=1
            print("Dex + 1")
        if (random.randint(1, 100) <= self.luckG):
            self.luck+=1
            print("Luck + 1")
    
    def draw(self):
        pygame.draw.circle(self.window, (0, 0, 0), self.currentTile.getCenter(), 25)
        pygame.draw.circle(self.window, (0, 0, 255), self.currentTile.getCenter(), 15)