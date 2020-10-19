import pygame

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
        
        ## for BFS
        self.visited = False
        self.distance = 0

        ## all stuff for drawing
        self.width = width
        self.height = height
        self.defaultColor = defaultColor
        self.currentColor = defaultColor
        self.defaultBorderColor = borderColor
        self.borderColor = borderColor
        
    def getAdjList(self):
        Tiles = self.currentMap.Tiles
        if (self.heightIndex < self.currentMap.height-1):# and self.heightIndex > 0 and self.widthIndex < self.currentMap.width-1 and self.widthIndex > 0):
            self.adjList.append(Tiles[self.heightIndex+1][self.widthIndex])
        if (self.heightIndex > 0):
            self.adjList.append(Tiles[self.heightIndex-1][self.widthIndex])
        if (self.widthIndex < self.currentMap.width-1):
            self.adjList.append(Tiles[self.heightIndex][self.widthIndex+1])
        if (self.widthIndex > 0):
            self.adjList.append(Tiles[self.heightIndex][self.widthIndex-1])   
    
    def __str__(self):
        return (str(self.posX) + ", " + str(self.posY))
    
    def reset(self):
        self.visited = False
        self.distance = 0

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
        self.getAdjList()
        self.borderColor = (0, 255, 0)
        for tile in self.adjList:
            tile.borderColor = (0, 255, 0)
    def unhighlighted(self):
        self.borderColor = self.defaultBorderColor
        for tile in self.adjList:
            tile.borderColor = tile.defaultBorderColor