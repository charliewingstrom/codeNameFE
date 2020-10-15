import pygame
from Menu import Menu
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
class ActionMenu(Menu):

    def __init__(self, window, screenWidth, screenHeight):
        super().__init__(window, screenWidth, screenHeight)
        self.selectedIndex = 0
        self.menuItems = ["Wait"]
        self.posY = 100
    def reset(self):
        self.selectedIndex = 0
        self.menuItems = ["Wait"]

    def addAttack(self):
        self.menuItems.insert(0, "Attack")

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
        if (len(self.menuItems) == 1):
            pygame.draw.rect(self.window, white, (self.posX, self.posY, 150, (100)))
        else:
            pygame.draw.rect(self.window, white, (self.posX, self.posY, 150, (75*len(self.menuItems))))

        for i in range(len(self.menuItems)):
            if i == self.selectedIndex:
                color = green
            else:
                color = black
            tmpText = font.render(self.menuItems[i], True, color)
            tmpTextRect = tmpText.get_rect()
            tmpTextRect.center = (self.posX+75, self.posY+(50 * (i+1)))
            self.window.blit(tmpText, tmpTextRect)
        


