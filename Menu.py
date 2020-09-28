import pygame

white = (255, 255, 255)
black = (0, 0, 0)
class Menu(object):

    def __init__(self, window, cursorPos, screenWidth):
        pygame.init()
        self.window = window
        self.cursorPos = cursorPos
        self.screenWidth = screenWidth
        self.posX = 400
        self.posY = 400
    def draw(self):

        font = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render("Menu", True, black)
        text2 = font.render("Wait", True, black)
        textRect = text.get_rect()
        textRect2 = text2.get_rect()
        textRect.center = (self.posX // 2, self.posY // 2)
        
        textRect2.center = (self.posX // 2, self.posY+0.5 // 2)
        pygame.draw.rect(self.window, white, (100, 100, 200, 400))
        self.window.blit(text, textRect)
        self.window.blit(text2, textRect2)


