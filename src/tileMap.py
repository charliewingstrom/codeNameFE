from tile import Tile

class Map():

    def __init__(self, width, height, background, tileSize, winCondition, enemyUnits = set()):
        self.__width=width
        self.__height=height
        self.__background = background
        # creates a list of rows of tiles
        tiles = []
        currHeight = 0
        currWidth = 0
        for i in range(width):
            row = []
            for j in range(height):
                row.append(Tile(currWidth, currHeight, tileSize))
                currHeight+=1
            currHeight = 0
            currWidth+=1
            tiles.append(row)
        self.__tiles = tiles
        for row in self.__tiles:
            for tile in row:
                if tile.Y < self.__height-1:
                    tile.getAdjList().append(self.__tiles[tile.X][tile.Y+1])
                if tile.Y > 0:
                    tile.getAdjList().append(self.__tiles[tile.X][tile.Y-1])
                if tile.X < self.__width-1:
                    tile.getAdjList().append(self.__tiles[tile.X+1][tile.Y])
                if tile.X > 0:
                    tile.getAdjList().append(self.__tiles[tile.X-1][tile.Y])

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
            self.__tiles[unit.X][unit.Y].currentUnit = unit
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
                return self.__tiles[X][Y]
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