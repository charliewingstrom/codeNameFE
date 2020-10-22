from EnemyUnit import EnemyUnit
from PlayerUnit import PlayerUnit

red = (185, 0, 0)
blue = (0, 0, 255)

class Movement(object):

    def __init__(self, currentMap):
        self.currentMap = currentMap
        self.currentUnit = None

    ## finds the tiles that the current unit can move to and changes their color,
    ## then finds the tiles that a unit can attack (but not move to) and makes them a different color
    def findTilesInRange(self, unit):
        oppositeType = EnemyUnit
        if type(unit) == EnemyUnit:
            oppositeType = PlayerUnit
        currentTile = unit.currentTile
        movement = unit.mov
        attackRange = unit.attackRange
        currentTile.visited = True
        currentTile.selectable = True
        currentTile.setColor(blue)
        currentTile.distance = 0
        queue = []
        visited = []
        for row in self.currentMap.Tiles:
            for tile in row:
                queue.append(tile)

        ## main loop to find tiles in range, accounts for movement penalty
        while (len(queue) > 0):
            queue.sort(key=lambda tile: tile.distance)
            currentTile = queue.pop(0)
            if (currentTile.distance <= movement):
                
                if (type(currentTile.currentUnit) != oppositeType):
                    currentTile.setColor(blue)
                    currentTile.selectable = True
                    currentTile.visited = True
                    visited.append(currentTile)
                    for tile in currentTile.adjList:
                        altDist = currentTile.distance + tile.movPenalty
                        if (altDist <= movement and altDist < tile.distance):
                            tile.parent = currentTile
                            tile.distance = altDist
        
        ## reset to run bfs on edge tiles
        for row in self.currentMap.Tiles:
            for tile in row:
                tile.distance = 0
        edgeTiles = []
        for visitedTile in visited:
            for tile in visitedTile.adjList:
                if (not tile.visited):
                    tile.setColor(red)
                    tile.visited = True
                    tile.distance = 1
                    edgeTiles.append(tile)
        
        ## run bfs on edge tiles to show attack range
        for edgeTile in edgeTiles:
            tmpQueue = []
            tmpQueue.append(edgeTile)
            while(len(tmpQueue) > 0):
                currentTile = tmpQueue.pop(0)
                if (currentTile.distance < attackRange):
                    for tile in currentTile.adjList:
                        if not tile.visited:
                            tile.visited = True
                            tile.setColor(red)
                            tile.distance = currentTile.distance+1
                            tmpQueue.append(tile)

    #def findPath(self, unit, target):
