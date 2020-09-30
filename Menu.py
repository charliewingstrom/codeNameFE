import pygame

white = (255, 255, 255)
black = (0, 0, 0)
class Menu(object):

    def __init__(self, window, screenWidth):
        pygame.init()
        self.window = window
        self.screenWidth = screenWidth
        self.posX = 100
        self.posY = 100

    def checkPos(self, currentTile):
        if (currentTile.posX < self.screenWidth // 2):
            self.posX = 800
        else:
            self.posX = 100
    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render("Menu", True, black)
        text2 = font.render("Wait", True, black)
        textRect = text.get_rect()
        textRect.center = (self.posX+75, self.posY+50)
        
        pygame.draw.rect(self.window, white, (self.posX, self.posY, 150, 100))
        self.window.blit(text, textRect)


