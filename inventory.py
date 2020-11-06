from Menu import Menu
import pygame
white = (255, 255, 255)
class Inventory(Menu):

    def __init__(self, window, screenWidth, screenHight):
        super().__init__(window, screenWidth, screenHight)
        self.__currentUnit = None
        self.posY = 100

    def setCurrentUnit(self, unit):
        self.__currentUnit = unit

    def checkPos(self, currentTile):
        self.selectedIndex = 0
        if (currentTile.posX < self.screenWidth // 2):
            self.posX = self.screenWidth-200
        else:
            self.posX = 100
    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        pygame.draw.rect(self.window, white, (self.posX, self.posY, 150, (100)))
