import pygame

class Menu(object):

    def __init__(self, window, screenWidth, screenHeight):
        pygame.init()
        self.window = window
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.posX = screenWidth // 2
        self.posY = screenHeight // 2