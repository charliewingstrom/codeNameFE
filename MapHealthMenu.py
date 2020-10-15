import pygame
from Menu import Menu
class MapHealthMenu(Menu):

    def __init__(self, window, screenWidth, screenHeight):
        self.window = window
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.currentUnit = None
        self.posX = screenWidth - 300
        self.posY = screenHeight - 200

    def checkPos(self, currentTile):
        if (currentTile.posX < self.screenWidth // 2):
            self.posX = self.screenWidth - 300
        else:
            self.posX = 100

    def setCurrentUnit(self, unit):
        self.currentUnit = unit

    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 24)

        name = font.render(self.currentUnit.name, True, (0, 0, 0))
        nameRect = name.get_rect()
        nameRect.center = (self.posX + 50, self.posY + 25)

        currentHealth = self.currentUnit.hp
        maxHealth = self.currentUnit.maxHp
        currentHealthText = font.render(str(currentHealth) + "/" + str(maxHealth), True, (0, 0, 0))
        currentHealthRect = currentHealthText.get_rect()
        currentHealthRect.center = (self.posX + 150, self.posY + 25)

        pygame.draw.rect(self.window, (255, 255, 255), (self.posX, self.posY, 200, 100))

        # unit name
        self.window.blit(name, nameRect)

        # unit current health / max health
        self.window.blit(currentHealthText, currentHealthRect)


        # unit health bar 
        healthRemainingBarLength = round(180 * (currentHealth / maxHealth))
        pygame.draw.rect(self.window, (0, 255, 0), (self.posX+10, self.posY + 75, healthRemainingBarLength, 10))
        pygame.draw.rect(self.window, (0, 0, 0), (self.posX+10+healthRemainingBarLength, self.posY + 75, 180 - healthRemainingBarLength, 10))

