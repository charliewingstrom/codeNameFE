from tile import Tile

class Map():

    def __init__(self, background, tiles, winCondition, enemyUnits = set()):
        self.__background = background
        self.__tiles = tiles
        self.__width=len(tiles[0])
        self.__height=len(tiles)
        for row in self.__tiles:
            for tile in row:
                if tile.Y < self.__height-1:
                    tile.getAdjList().append(self.__tiles[tile.Y+1][tile.X])
                if tile.Y > 0:
                    tile.getAdjList().append(self.__tiles[tile.Y-1][tile.X])
                if tile.X < self.__width-1:
                    tile.getAdjList().append(self.__tiles[tile.Y][tile.X+1])
                if tile.X > 0:
                    tile.getAdjList().append(self.__tiles[tile.Y][tile.X-1])

        self.__startTiles = []

        for i in range(10):
            self.__startTiles.append(self.__tiles[i][5])

        ## win condition is a function that returns true if the condition has been met
        self.__winCondition = winCondition
        for unit in enemyUnits:
            self.addUnitToMap(unit)

    # for adding enemies
    def addUnitToMap(self, unit):
        try: 
            self.__tiles[unit.Y][unit.X].currentUnit = unit
        except IndexError as e:
            print(f"{e} tileMap : addUnitToMap => Unit X or Y out of map range")

    ## for adding players
    ## will throw an exception if number of units is greater than 
    ## the number of start tiles
    def addUnitToStartTile(self, unit):
        for tile in self.__startTiles:
            if tile.currentUnit == None and tile.walkable:
                tile.currentUnit = unit
                unit.X = tile.X
                unit.Y = tile.Y
                unit.active = True
                break
        else:
            return True
        return False
    
    def getTileAt(self, X, Y):
        if X >= 0 and Y >= 0:
            try:
                return self.__tiles[Y][X]
            except IndexError as e:
                print("getTileAt failed, ", str(e))
            

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def reset(self):
        for row in self.__tiles:
            for tile in row:
                tile.reset()

    def checkForWin(self):
        return self.__winCondition()
        
    def draw(self, screen, xCamera, yCamera):
        screen.blit(self.__background, (xCamera, yCamera))
        for row in self.__tiles:
            for tile in row:
                tile.draw(screen, xCamera, yCamera)