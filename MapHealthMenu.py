import pygame
from Menu import Menu
class MapHealthMenu(Menu):

    def __init__(self, window, screenWidth, screenHeight):
        self.window = window
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.unitName = "No Name given"
        self.unitHp = 0
        self.unitMaxHp = 0
        self.posX = screenWidth - 200
        self.posY = screenHeight - 100

    def checkPos(self, currentTile):
        if (currentTile.posX < self.screenWidth // 2):
            self.posX = self.screenWidth - 200
        else:
            self.posX = 200

    def draw(self):
        pygame.draw.rect(self.window, (255, 255, 255), (self.posX, self.posY, 100, 100))
