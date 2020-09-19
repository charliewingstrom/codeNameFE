
import pygame
from Tile import Tile

class Unit(object):

    def __init__(self, window, currTile = None):
        self.window = window
        self.currTile = currTile


    def setCurrTile(self, tile):
        self.currTile = tile


    def draw(self):
        pygame.draw.circle(self.window, (255, 0, 0), self.currTile.getCenter(), 10)