from Menu import Menu
import pygame
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
class Inventory(Menu):

    def __init__(self, window, screenWidth, screenHight):
        super().__init__(window, screenWidth, screenHight)
        self.__currentUnit = None
        self.posY = 100
        self.posX = 100
        self.selectedIndex = 0
        self.itemSelected = False

    def setCurrentUnit(self, unit):
        self.__currentUnit = unit

    def highlightDown(self):
        self.selectedIndex+=1
        if (self.selectedIndex > len(self.__currentUnit.inventory) + len(self.__currentUnit.weapons) - 1):
            self.selectedIndex = 0

    def highlightUp(self):
        self.selectedIndex-=1
        if (self.selectedIndex < 0):
            self.selectedIndex = len(self.menuItems) - 1

    def checkPos(self, currentTile):
        self.selectedIndex = 0
        if (currentTile.posX < self.screenWidth // 2):
            self.posX = self.screenWidth-200
        else:
            self.posX = 100
    
    def selectOption(self):
        if (not self.itemSelected):
            self.selectItem()
    def selectItem(self):
        self.itemSelected = True

    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 32)

        unitInventory = self.__currentUnit.inventory
        unitWeapons = self.__currentUnit.weapons
        if (self.itemSelected):
            pass
        else:
            if (len(unitInventory) + len(unitWeapons) <= 1):
                pygame.draw.rect(self.window, white, (self.posX, self.posY, 150, (100)))
            else:
                pygame.draw.rect(self.window, white, (self.posX, self.posY, 150, (75*(len(unitInventory) + len(unitWeapons)))))
            weaponsText = font.render("Weapons", True, black)
            for i in range(len(unitInventory) + len(unitWeapons)):
                if i == self.selectedIndex:
                    color = green
                else:
                    color = black
                if i < len(unitInventory):
                    text = font.render(unitInventory[i].name, True, color)
                else:
                    text = font.render(str(unitWeapons[i - len(unitInventory)]), True, color)
                textRect = text.get_rect() 
                textRect.center = (self.posX+75, self.posY +(50 * (i+1)))
                self.window.blit(text, textRect)