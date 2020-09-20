import pygame
from Tile import Tile
class Map(object):
    
    def __init__(self, window, width = 7, height = 7, Tiles = []):
        self.window = window
        self.width = width
        self.height = height
        self.cursor = [width//2,height//2]
        self.isUnitSelected = False
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
        self.Tiles[Xcoord][Ycoord].setCurrentUnit(Unit)

    def unitSelectedCursor(self):
        if (self.getTileCursorIsOn().currentUnit != None):
            print("Theres a guy there")
            self.isUnitSelected = True
        else:
            print("Theres no one home")

    def selectLeft(self):
        self.getTileCursorIsOn().unselected()
        self.cursor[1] -= 1
        self.getTileCursorIsOn().selected()

    def selectRight(self):
        self.getTileCursorIsOn().unselected()
        self.cursor[1] += 1
        self.getTileCursorIsOn().selected()
    
    def selectUp(self):
        self.getTileCursorIsOn().unselected()
        self.cursor[0] -= 1
        self.getTileCursorIsOn().selected()

    def selectDown(self):
        self.getTileCursorIsOn().unselected()
        self.cursor[0] += 1
        self.getTileCursorIsOn().selected()

    def getTileCursorIsOn(self):
        return self.Tiles[self.cursor[0]][self.cursor[1]]

    def draw(self):
        for row in self.Tiles:
            for Tile in row:
                Tile.draw()