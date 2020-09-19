import pygame
from Tile import Tile
class Map(object):
    
    def __init__(self, window, width = 7, height = 7, Tiles = []):
        self.window = window
        self.width = width
        self.height = height
        self.cursor = [width//2,height//2]
        
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
            tmpTiles[self.cursor[0]][self.cursor[1]].selected()
            self.Tiles = tmpTiles
        else:
            self.Tiles = Tiles
        
    def addUnit(self, Unit, Xcoord, Ycoord):
        Unit.setCurrTile(self.Tiles[Xcoord][Ycoord])

    def selectLeft(self):
        self.Tiles[self.cursor[0]][self.cursor[1]].unselected()
        self.cursor[1] -= 1
        self.Tiles[self.cursor[0]][self.cursor[1]].selected()

    def selectRight(self):
        self.Tiles[self.cursor[0]][self.cursor[1]].unselected()
        self.cursor[1] += 1
        self.Tiles[self.cursor[0]][self.cursor[1]].selected()
    
    def selectUp(self):
        self.Tiles[self.cursor[0]][self.cursor[1]].unselected()
        self.cursor[0] -= 1
        self.Tiles[self.cursor[0]][self.cursor[1]].selected()

    def selectDown(self):
        self.Tiles[self.cursor[0]][self.cursor[1]].unselected()
        self.cursor[0] += 1
        self.Tiles[self.cursor[0]][self.cursor[1]].selected()

    def draw(self):
        for row in self.Tiles:
            for Tile in row:
                Tile.draw()