import pygame

white = (255, 255, 255)
black = (0, 0, 0)
class Menu(object):

    def __init__(self, window):
        pygame.init()
        self.window = window
        self.posX = 400
        self.posY = 400

    def draw(self):

        pygame.display.set_caption('Menu Text')

        font = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render("Menu", True, black)

        textRect = text.get_rect()

        textRect.center = (self.posX // 2, self.posY // 2)


        self.window.blit(text, textRect)


