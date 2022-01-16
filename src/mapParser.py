import json
import pygame
from tile           import Tile
from pathlib        import Path
from assetLoader    import AssetLoader

class MapParser(object):

    mapDir = "./maps"
    tileSize = 96

    def __init__(self):
        pass 

    def parse(self, mapName : str):
        mapInfo = {}
        with open(MapParser.mapDir + "/" + mapName, 'r') as mapFile:
            mapInfo = json.load(mapFile)

        if mapInfo:
            layout = mapInfo['layout']
            # loop through the layout parsing each tile and adding it to tiles
            tiles = []
            for row in enumerate(layout):
                currRow = []
                for tile in enumerate(row[1]):
                    currTile = Tile(tile[0], row[0], MapParser.tileSize)
                    self.parseTile(tile[1], currTile)
                    currRow.append(currTile)
                tiles.append(currRow)

        return tiles


    def parseTile(self, tileInfo : str, inputTile : Tile):
        tileInfo = tileInfo.split(',')
        while tileInfo:
            match tileInfo.pop(0):
                case "1":
                    inputTile.walkable = False
                    inputTile.pic      = AssetLoader.assets["wall.png"]

                case _ :
                    inputTile.pic = AssetLoader.assets["grassTile2.png"]
