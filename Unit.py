
import pygame
from Tile import Tile

class Unit(object):

    def __init__(self, window, currTile = None):
        self.window = window
        self.currentTile = currTile
        self.mov = 5
        self.attackRange = 2
        
        self.maxHp = 23
        self.hp = self.maxHp
        self.strength = 6
        self.defense = 4

    def setCurrentTile(self, tile):
        self.currentTile = tile

    def draw(self):
        pygame.draw.circle(self.window, (0, 0, 0), self.currentTile.getCenter(), 25)
        pygame.draw.circle(self.window, (0, 0, 255), self.currentTile.getCenter(), 15)