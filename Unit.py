
import pygame
from Tile import Tile

class Unit(object):

    def __init__(self, window, currTile):
        self.window = window
        self.currTile = currTile


    def draw(self):
        pygame.draw.circle(self.window, (255, 0, 0), self.currTile.posX, self.currTile.posY)