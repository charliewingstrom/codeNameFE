import  pygame

from pathlib    import Path
from unit       import Unit
from tileMap    import Map
from cursor     import Cursor
from camera     import Camera
from inventory  import HealingItem, Sword, Bow, Javelin

map1background = pygame.image.load(Path(__file__).parent / "../assets/level1Background.png")
map2background = pygame.image.load(Path(__file__).parent / "../assets/map2-background.png")



class MapManager():

    def __init__(self, tileSize, gameWidth, gameHeight, myUnitHolder):
        firstMapWidth = 32
        firstMapHeight = 19

        self.__tileSize     = tileSize
        self.__gameWidth    = gameWidth
        #self.__gameHeight   = gameHeight
        self.__cursor       = Cursor(self.__tileSize, firstMapWidth, firstMapHeight, gameWidth, gameHeight)
        self.__camera       = Camera()

        self.__maps         = []
        self.__currentMap   = None
        # do I build all of my maps here?
        map1Enemies = [Unit(9, 5, tileSize, [Sword()]), Unit(9, 6, tileSize, [Sword()])]
        
        ## setting up the map
        def map1Win():
            return map1Enemies[0].hp <= 0

        map1 = Map(firstMapWidth, firstMapHeight, map1background, tileSize, map1Win, set(map1Enemies))

        myUnitHolder.setEnemiesToMap(map1, map1Enemies)

        # set unique tiles
        for i in range(3):
            map1.tiles[i][4].walkable = False
        for i in range(5):
            map1.tiles[4][i].walkable = False
        for i in range(3):
            map1.tiles[i+5][4].walkable = False
        for i in range(5):
            map1.tiles[9][i].walkable = False
        for i in range(3):
            map1.tiles[i+10][4].walkable = False
        for i in range(5):
            map1.tiles[14][i].walkable = False
        for i in range(14):
            map1.tiles[i][7].walkable = False

        self.__maps.append(map1)

        # map2
        map2enemies = [Unit(1, 2, tileSize, [Sword()]), Unit(2, 1, tileSize, [Sword()])]

        def map2Win():
            return map2enemies[0].hp <= 0

        map2 = Map(12, 12, map2background, tileSize, map2Win, set(map2enemies))

        myUnitHolder.setEnemiesToMap(map2, map2enemies)

        self.__maps.append(map2)

        self.__setupNextMap()
        myUnitHolder.moveToNextMap(self.__currentMap)

    def getCurrentMap(self):
        return self.__currentMap

    def __drawCurrentMap(self, screen):
        self.__currentMap.draw(screen, self.__camera.getX(), self.__camera.getY())

    def draw(self, screen):
        self.__drawCurrentMap(screen)
        self.__cursor.draw(screen)

    def resetCurrentMap(self):
        self.__currentMap.reset()

    def checkForMapCompletion(self):
        mapComplete = self.__currentMap.checkForWin()
        noMoreMaps  = False
        if mapComplete:
            noMoreMaps = self.__setupNextMap()

        return mapComplete, noMoreMaps

    def getTileUnitIsOn(self, unit):
        toReturn = self.__currentMap.tiles[unit.X][unit.Y]
        if toReturn.currentUnit != unit:
            print("Get Tile Unit is on failed")
        return toReturn

    def getTileCursorIsOn(self):
        return self.__currentMap.tiles[self.__cursor.X][self.__cursor.Y]

    def setCursorOnUnit(self, unit):
        self.__cursor.X = unit.X
        self.__cursor.Y = unit.Y
    def getCameraX(self):
        return self.__camera.getX()

    def getCameraY(self):
        return self.__camera.getY()
    
    def checkUI(self, arrowKeys, myMapUnitUI, myBattleForecast, myPathManager):
        if self.__camera.updateFromCursor(self.__cursor, arrowKeys):
            self.checkMapUI(myMapUnitUI, myBattleForecast)
            cursorTile = self.getTileCursorIsOn()
            myPathManager.resetPath(cursorTile)
                
    ## compares the UI elements to the cursor location
    ## keeps the UI from covering up the map
    def checkMapUI(self, myMapUnitUI, myBattleForecast):
        if self.__cursor.X * self.__tileSize > self.__gameWidth / 2:
            myMapUnitUI.X = 10
            myBattleForecast.X = 10
        else:
            myMapUnitUI.X = self.__gameWidth - 460
            myBattleForecast.X = self.__gameWidth - 500
        
        ## check if cursor is over a player
        cursorTileUnit = self.getTileCursorIsOn().currentUnit
        myMapUnitUI.reset(cursorTileUnit)

    def __setupNextMap(self):
        noMoreMaps = True
        self.__currentMap = None
        if len(self.__maps) > 0:
            self.__currentMap = self.__maps.pop(0)
            self.__cursor.resetFromMap(self.__currentMap)
            noMoreMaps = False
        return noMoreMaps
        