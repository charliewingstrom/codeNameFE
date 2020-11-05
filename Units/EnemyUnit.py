import pygame
from Tile import Tile
from Unit import Unit
class EnemyUnit(Unit):

    def __init__(self, window, name):
        super().__init__(window, name)

    def draw(self):
        pygame.draw.circle(self.window, (0, 0, 0), self.currentTile.getCenter(), 25)
        pygame.draw.circle(self.window, (255, 0, 0), self.currentTile.getCenter(), 15)

        