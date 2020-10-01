
import pygame
from Tile import Tile

class Unit(object):

    def __init__(self, window, currTile = None):
        self.window = window
        self.currentTile = currTile
        self.mov = 5
        self.attackRange = 1
        
        self.hp = 23
        self.stength = 6
        self.defense = 4

    def setCurrentTile(self, tile):
        self.currentTile = tile


    def draw(self):
        pygame.draw.circle(self.window, (255, 255, 0), self.currentTile.getCenter(), 10)