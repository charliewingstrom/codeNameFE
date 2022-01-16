import pygame
from assetLoader import AssetLoader

maxDistance = 256

class Tile():

    def __init__(self, X, Y, tileSize):
        self.X              = X
        self.Y              = Y
        self.tileSize       = tileSize
        self.__color        = (128, 128, 128)
        self.currentUnit    = None
        self.distance       = maxDistance
        self.parent         = None
        self.walkable       = True
        self.selectable     = False
        self.selectablePic  = pygame.transform.scale(AssetLoader.assets["selectableHighlight.png"], (tileSize, tileSize))
        self.attackable     = False
        self.attackablePic  = pygame.transform.scale(AssetLoader.assets["attackableHighlight.png"], (tileSize, tileSize))
        self.inPath         = False
        self.inPathPic      = pygame.transform.scale(AssetLoader.assets["occupiedHighlight.png"], (tileSize, tileSize))
        self.__adjList      = []

    def __repr__(self):
        return "X: {0}\tY: {1}".format(self.X, self.Y)

    def getAdjList(self):
        return self.__adjList
        
    def reset(self):
        self.parent = None
        self.distance = maxDistance
        self.selectable = False
        self.attackable = False

    def setColor(self, color):
        self.__color = color

    def draw(self, screen, xCamera, yCamera):
        if self.currentUnit != None:
            color = (0, 0, 0)
        else:
            color = self.__color

        # TODO add tile textures
        # TODO try to draw this without lagging
        screen.blit(self.pic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))
        #pygame.draw.rect(screen, color, pygame.Rect(self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera, self.tileSize, self.tileSize))
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera, self.tileSize, self.tileSize), 2)
        

        if self.attackable:
            screen.blit(self.attackablePic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))
        elif self.inPath:
            screen.blit(self.inPathPic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))
        elif self.selectable:
            screen.blit(self.selectablePic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))