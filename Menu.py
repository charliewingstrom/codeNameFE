import pygame

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
class Menu(object):

    def __init__(self, window, screenWidth):
        pygame.init()
        self.window = window
        self.screenWidth = screenWidth
        self.posX = 100
        self.posY = 100
        self.selectedIndex = 0
        self.menuItems = ["Items", "Wait"]

    def highlightDown(self):
        self.selectedIndex+=1
        if (self.selectedIndex > len(self.menuItems) - 1):
            self.selectedIndex = 0

    def highlightUp(self):
        self.selectedIndex-=1
        if (self.selectedIndex < 0):
            self.selectedIndex = len(self.menuItems) - 1

    def checkPos(self, currentTile):
        self.selectedIndex = 0
        if (currentTile.posX < self.screenWidth // 2):
            self.posX = 800
        else:
            self.posX = 100
        
    
    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        pygame.draw.rect(self.window, white, (self.posX, self.posY, 150, (100*len(self.menuItems))))

        for i in range(len(self.menuItems)):
            if i == self.selectedIndex:
                color = green
            else:
                color = black
            tmpText = font.render(self.menuItems[i], True, color)
            tmpTextRect = tmpText.get_rect()
            tmpTextRect.center = (self.posX+75, self.posY+(50 * (i+1)))
            self.window.blit(tmpText, tmpTextRect)
        


