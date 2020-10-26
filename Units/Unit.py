
import pygame
from Tile import Tile

class Unit(object):

    def __init__(self, window, name, currTile = None):
        self.window = window
        self.name = name
        self.currentTile = currTile
        
        self.mov = 5
        self.attackRange = 2
        
        self.inventory = []
        self.equipedWeapon = None
        
        self.maxHp = 23
        self.hp = self.maxHp
        self.strength = 6
        self.defense = 4
        self.dex = 5
        self.spd = 5
        
        self.active = False

    def __str__(self):
        return self.name
        
    def setCurrentTile(self, tile):
        self.currentTile = tile

    def draw(self):
        pygame.draw.circle(self.window, (0, 0, 0), self.currentTile.getCenter(), 25)
        pygame.draw.circle(self.window, (0, 0, 255), self.currentTile.getCenter(), 15)