import pygame
from pathlib import Path

maxDistance = 256

grassTilePic = pygame.image.load(Path(__file__).parent / "../assets/grassTile.png")
selectablePic = pygame.image.load(Path(__file__).parent / "../assets/selectableHighlight.png")
attackablePic = pygame.image.load(Path(__file__).parent / "../assets/attackableHighlight.png")
inPathPic = pygame.image.load(Path(__file__).parent / "../assets/occupiedHighlight.png")

class Tile():

    def __init__(self, X, Y, tileSize):
        self.X = X
        self.Y = Y
        self.tileSize       = tileSize
        self.__color        = (128, 128, 128)
        self.currentUnit    = None
        self.distance       = maxDistance
        self.parent         = None
        self.walkable       = True
        self.pic            = pygame.transform.scale(grassTilePic, (tileSize, tileSize))
        self.selectable     = False
        self.selectablePic  = pygame.transform.scale(selectablePic, (tileSize, tileSize))
        self.attackable     = False
        self.attackablePic  = pygame.transform.scale(attackablePic, (tileSize, tileSize))
        self.inPath         = False
        self.inPathPic      = pygame.transform.scale(inPathPic, (tileSize, tileSize))
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
        pygame.draw.rect(screen, color, pygame.Rect(self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera, self.tileSize, self.tileSize))
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera, self.tileSize, self.tileSize), 2)
        
        if self.attackable:
            screen.blit(self.attackablePic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))
        elif self.inPath:
            screen.blit(self.inPathPic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))
        elif self.selectable:
            screen.blit(self.selectablePic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))