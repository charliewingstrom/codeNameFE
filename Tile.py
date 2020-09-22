import pygame

class Tile(object):
    
    def __init__(self, window, posX, posY, width = 100, height = 100, color = (0,0,0), borderColor = (255, 255, 255)):
        self.window = window
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.color = color
        self.borderColor = borderColor
        self.currentUnit = None
        
    
    def draw(self):
        pygame.draw.rect(self.window, self.borderColor,(self.posX, self.posY, self.width, self.height))
        pygame.draw.rect(self.window, self.color, (self.posX+1, self.posY+1, self.width-2, self.height-2))
    
    def setCurrentUnit(self, Unit):
        self.currentUnit = Unit
        
    def getCenter(self):
        return (self.posX + (self.width//2), self.posY + (self.height//2))

    def setColor(self, color):
        self.color = color
        
    def selected(self):
        self.borderColor = (0, 255, 0)
        
    def unselected(self):
        self.borderColor = (255, 255, 255)