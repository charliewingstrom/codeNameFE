from assetLoader    import AssetLoader
from mapParser      import MapParser
from unit           import Stat
from tileMap        import Map
from cursor         import Cursor
from camera         import Camera

class MapManager():
    mapParser = MapParser()

    def __init__(self, tileSize, gameWidth, gameHeight, myUnitHolder):
        #TODO this is kind of a hack..
        firstMapWidth = 32
        firstMapHeight = 19

        self.__tileSize     = tileSize
        self.__gameWidth    = gameWidth
        self.__cursor       = Cursor(self.__tileSize, firstMapWidth, firstMapHeight, gameWidth, gameHeight)
        self.__camera       = Camera()

        self.__maps         = []
        self.__currentMap   = None
        
        def map1Win():
            # Check if all units are dead
            for unit in map1Enemies:
                if unit.getStat(Stat.HP) > 0:
                    return False

                else:
                    return True

        ## TODO make mapParser return a fully constructed map  
        map1tiles, map1Enemies = MapManager.mapParser.parse("one.json")        

        map1 = Map(AssetLoader.assets["level1Background.png"], map1tiles, map1Win)

        myUnitHolder.setEnemiesToMap(map1, map1Enemies)

        self.__maps.append(map1)

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

    def getTileAt(self, X, Y):
        return self.__currentMap.getTileAt(X, Y)
        
    def getTileUnitIsOn(self, unit):
        toReturn = self.__currentMap.getTileAt(unit.X, unit.Y)
        if toReturn.currentUnit != unit:
            print("Get Tile Unit is on failed")
        return toReturn

    def getTileCursorIsOn(self):
        return self.__currentMap.getTileAt(self.__cursor.X, self.__cursor.Y)

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
            if cursorTile.selectable:
                myPathManager.resetPath(cursorTile)
            else:
                myPathManager.emptyPath()
                
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
        