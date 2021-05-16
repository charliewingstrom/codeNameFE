import pygame
from pathlib import Path

maxDistance = 256

grassTilePic = pygame.image.load(Path(__file__).parent / "../assets/grassTile.png")
selectablePic = pygame.image.load(Path(__file__).parent / "../assets/selectableHighlight.png")
attackablePic = pygame.image.load(Path(__file__).parent / "../assets/attackableHighlight.png")
occupiedPic = pygame.image.load(Path(__file__).parent / "../assets/occupiedHighlight.png")

class Tile():

    def __init__(self, X, Y, tileSize):
        self.X = X
        self.Y = Y
        self.tileSize = tileSize
        self.currentUnit = None
        self.pic = pygame.transform.scale(grassTilePic, (tileSize, tileSize))
        self.walkable = True
        self.selectable = False
        self.selectablePic = pygame.transform.scale(selectablePic, (tileSize, tileSize))
        self.attackable = False
        self.attackablePic = pygame.transform.scale(attackablePic, (tileSize, tileSize))
        self.occupiedPic = pygame.transform.scale(occupiedPic, (tileSize, tileSize))
        self.adjList = []
        self.distance = maxDistance
        self.parent = None

    def __repr__(self):
        return "X: {0}\tY: {1}".format(self.X, self.Y)

    def reset(self):
        self.parent = None
        self.distance = maxDistance
        self.selectable = False
        self.attackable = False

    def draw(self, screen, xCamera, yCamera):
        if self.currentUnit != None:
            screen.blit(self.occupiedPic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))
        elif self.attackable:
            screen.blit(self.attackablePic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))
        elif self.selectable:
            screen.blit(self.selectablePic, (self.X*self.tileSize + xCamera, self.Y*self.tileSize + yCamera))