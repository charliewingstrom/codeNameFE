import json
from tile           import Tile
from unit           import Unit
from unitClass      import UnitClass
from inventory      import Sword, Bow
from assetLoader    import AssetLoader

class MapParser(object):

    mapDir = "./maps"
    tileSize = 96

    def __init__(self):
        self.__enemies = []

    def parse(self, mapName : str):
        self.__enemies = []
        mapInfo = {}
        with open(MapParser.mapDir + "/" + mapName, 'r') as mapFile:
            mapInfo = json.load(mapFile)

        if mapInfo:
            layout = mapInfo['layout']
            # loop through the layout parsing each tile and adding it to tiles
            tiles = []
            for rowNum, row in enumerate(layout):
                currRow = []
                for tileNum, tileInfo in enumerate(row.values()):
                    currTile = Tile(tileNum, rowNum, MapParser.tileSize)
                    self.parseTile(tileInfo["tile"], currTile)
                    ## TODO check for enemy
                    self.parseEnemy(tileInfo, tileNum, rowNum, currTile)
                    currRow.append(currTile)
                tiles.append(currRow)

        return tiles, self.__enemies

    def parseTile(self, tileType : str, inputTile : Tile):
        tileType = tileType.split(',')
        while tileType:
            infoPiece = tileType.pop(0)
            match infoPiece:
                case "wall":
                    inputTile.walkable = False
                    inputTile.pic      = AssetLoader.assets["wall.png"]

                case "brick":
                    ## TODO yeah this should be brick
                    inputTile.pic = AssetLoader.assets["grassTile2.png"]

                case _ :
                    print(f"WARNING : case {infoPiece} not matched")
                    inputTile.pic = AssetLoader.assets["grassTile2.png"]

    def parseEnemy(self, tileInfo : str, x : int, y : int, inputTile : Tile):
        enemyClass = tileInfo.get("enemy_class")
        if enemyClass:
            # parse inventory of enemy
            inventory = []
            for item in tileInfo.get("enemy_inv").split(","):
                match item:
                    case "sword":
                        inventory.append(Sword())
                        
                    case "bow":
                        inventory.append(Bow())
                    case _ : 
                        print(f"WARNING : case {item} not matched")

            enemy = Unit(x, y, MapParser.tileSize, inventory, False, UnitClass.getClass(enemyClass.upper()))

            inputTile.currentUnit = enemy
            self.__enemies.append(enemy)