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
        self.screenBufferTop = 0
        self.screenBufferBottom = screenHeight
        self.screenBufferLeft = 0
        self.screenBufferRight = screenWidth
        if (Tiles == []):
            tmpTiles = []
            posX = 10
            posY = 10
            for i in range(height):
                tmp = []
                for j in range(width):
                    tmp.append(Tile(window, posX, posY))
                    posX += tileSize
                posY += tileSize
                posX = 10
                tmpTiles.append(tmp)
                tmp = []
            self.Tiles = tmpTiles
        else:
            self.Tiles = Tiles
        
    def scrollDown(self):
        for row in self.Tiles:
            for tile in row:
                tile.posY -=tileSize
        self.screenBufferTop -= tileSize
        self.screenBufferBottom -= tileSize    
    
    def scrollUp(self):
        for row in self.Tiles:
            for tile in row:
                tile.posY +=tileSize
        self.screenBufferTop += tileSize
        self.screenBufferBottom += tileSize    

    def scrollLeft(self):
        for row in self.Tiles:
            for tile in row:
                tile.posX +=tileSize
        self.screenBufferRight += tileSize
        self.screenBufferLeft += tileSize    
    
    def scrollRight(self):
        for row in self.Tiles:
            for tile in row:
                tile.posX -=tileSize
        self.screenBufferRight -= tileSize
        self.screenBufferLeft -= tileSize

    def addUnit(self, Unit, Xcoord, Ycoord):
        Unit.setCurrentTile(self.Tiles[Xcoord][Ycoord])
        self.Tiles[Xcoord][Ycoord].setCurrentUnit(Unit)

    def draw(self):
        for row in self.Tiles:
            for Tile in row:
                Tile.draw()