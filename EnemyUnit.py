import pygame
from Tile import Tile
from Unit import Unit
class EnemyUnit(Unit):

    def __init__(self, window):
        super().__init__(window)

    def draw(self):
        pygame.draw.circle(self.window, (255, 0, 0), self.currentTile.getCenter(), 10)

        