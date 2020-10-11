import pygame
from Tile import Tile
from cursor import Cursor

tileSize = 103
class Map(object):
    
    def __init__(self, window, screenWidth, screenHeight, width = 20, height = 20, Tiles = []):
        self.window = window
        self.width = width
        self.height = height
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.tileSize = tileSize
        if (Tiles == []):
            tmpTiles = []
            posX = 0
            posY = 0
            for i in range(height):
                tmp = []
                for j in range(width):
                    tmp.append(Tile(window, posX, posY, i, j))
                    posX += tileSize
                posY += tileSize
                posX = 0
                tmpTiles.append(tmp)
                tmp = []
            self.Tiles = tmpTiles
        else:
            self.Tiles = Tiles
        
    def scrollDown(self):
        for row in self.Tiles:
            for tile in row:
                tile.posY -= self.tileSize

    def scrollUp(self):
        for row in self.Tiles:
            for tile in row:
                tile.posY += self.tileSize

    def scrollLeft(self):
        for row in self.Tiles:
            for tile in row:
                tile.posX += self.tileSize
        
    def scrollRight(self):
        for row in self.Tiles:
            for tile in row:
                tile.posX -= self.tileSize

    def addUnit(self, Unit, Xcoord, Ycoord):
        Unit.setCurrentTile(self.Tiles[Xcoord][Ycoord])
        self.Tiles[Xcoord][Ycoord].setCurrentUnit(Unit)

    def draw(self):
        for row in self.Tiles:
            for Tile in row:
                Tile.draw()