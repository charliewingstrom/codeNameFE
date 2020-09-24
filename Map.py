import pygame
from Tile import Tile
from cursor import Cursor
class Map(object):
    
    def __init__(self, window, width = 20, height = 20, Tiles = []):
        self.window = window
        self.width = width
        self.height = height
        if (Tiles == []):
            tmpTiles = []
            posX = width
            posY = height
            for i in range(height):
                tmp = []
                for j in range(width):
                    tmp.append(Tile(window, posX, posY))
                    posX += 103
                posY += 103
                posX = width
                tmpTiles.append(tmp)
                tmp = []
            self.Tiles = tmpTiles
        else:
            self.Tiles = Tiles
        
    def addUnit(self, Unit, Xcoord, Ycoord):
        Unit.setCurrentTile(self.Tiles[Xcoord][Ycoord])
        self.Tiles[Xcoord][Ycoord].setCurrentUnit(Unit)

    def draw(self):
        for row in self.Tiles:
            for Tile in row:
                Tile.draw()