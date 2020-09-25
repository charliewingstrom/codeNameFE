import pygame

class Tile(object):
    
    def __init__(self, window, posX, posY, width = 100, height = 100, defaultColor = (0,0,0), borderColor = (255, 255, 255)):
        self.window = window
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.defaultColor = defaultColor
        self.currentColor = defaultColor
        self.borderColor = borderColor
        self.currentUnit = None
        
    def __str__(self):
        return (str(self.posX) + ", " + str(self.posY))
    
    def draw(self):
        pygame.draw.rect(self.window, self.borderColor,(self.posX, self.posY, self.width, self.height))
        pygame.draw.rect(self.window, self.currentColor, (self.posX+5, self.posY+5, self.width-10, self.height-10))
    
    def setCurrentUnit(self, Unit):
        self.currentUnit = Unit
        
    def getCenter(self):
        return (self.posX + (self.width//2), self.posY + (self.height//2))

    def setColor(self, color):
        self.currentColor = color
        
    def highlighted(self):
        self.borderColor = (0, 255, 0)
        
    def unhighlighted(self):
        self.borderColor = (255, 255, 255)