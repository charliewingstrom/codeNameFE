from tile import Tile

class Map():

    def __init__(self, width, height, background, tileSize):
        self.width=width
        self.height=height
        self.background = background
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
        self.tiles = tiles
        for row in self.tiles:
            for tile in row:
                if tile.Y < self.height-1:
                    tile.adjList.append(self.tiles[tile.X][tile.Y+1])
                if tile.Y > 0:
                    tile.adjList.append(self.tiles[tile.X][tile.Y-1])
                if tile.X < self.width-1:
                    tile.adjList.append(self.tiles[tile.X+1][tile.Y])
                if tile.X > 0:
                    tile.adjList.append(self.tiles[tile.X-1][tile.Y])

    def addUnitToMap(self, unit):
        self.tiles[unit.X][unit.Y].currentUnit = unit

    def reset(self):
        for row in self.tiles:
            for tile in row:
                tile.reset()

    def draw(self, screen, xCamera, yCamera):
        screen.blit(self.background, (xCamera, yCamera))
        for row in self.tiles:
            for tile in row:
                tile.draw(screen, xCamera, yCamera)