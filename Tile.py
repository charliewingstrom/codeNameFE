import pygame
cursorColor = (255,140,25)
maxDistance = 1024
class Tile(object):
    
    def __init__(self, window, currentMap, posX, posY, verticalIndex, horizontalIndex, width = 100, height = 100, defaultColor = (0,0,0), borderColor =(255, 255, 255)):
        self.window = window
        self.currentMap = currentMap
        self.posX = posX
        self.posY = posY
        self.heightIndex = verticalIndex
        self.widthIndex = horizontalIndex
        self.currentUnit = None
        self.adjList = []
        self.selectable = False
        ## for searching algo
        self.visited = False
        self.distance = maxDistance
        self.movPenalty = 1
        self.parent = None

        ## for A* path finding algo
        f = 0.0
        g = 0.0
        h = 0.0

        ## all stuff for drawing
        self.width = width
        self.height = height
        self.defaultColor = defaultColor
        self.currentColor = defaultColor
        self.defaultBorderColor = borderColor
        self.borderColor = borderColor
        
    def getAdjList(self):
        Tiles = self.currentMap.Tiles
        if (self.heightIndex < self.currentMap.height-1):
            self.adjList.append(Tiles[self.heightIndex+1][self.widthIndex])
        if (self.heightIndex > 0):
            self.adjList.append(Tiles[self.heightIndex-1][self.widthIndex])
        if (self.widthIndex < self.currentMap.width-1):
            self.adjList.append(Tiles[self.heightIndex][self.widthIndex+1])
        if (self.widthIndex > 0):
            self.adjList.append(Tiles[self.heightIndex][self.widthIndex-1])   
    
    def __str__(self):
        return (str(self.heightIndex) + ", " + str(self.widthIndex))
    
    def reset(self):
        self.setColor(self.defaultColor)
        self.parent = None
        self.selectable = False
        self.visited = False
        self.distance = maxDistance
        self.f = 0.0
        self.g = 0.0
        self.h = 0.0

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
        self.borderColor = cursorColor

    def unhighlighted(self):
        self.borderColor = self.defaultBorderColor