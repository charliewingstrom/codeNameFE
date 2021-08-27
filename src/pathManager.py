class PathManager():

    def __init__(self):

        self.__path = []
        self.__targetTile = None
        self.__startTile = None
        self.__velocity = (0, 0)
        self.__moveSpeed = 2

    def __findPath(self, targetTile : object):
        while targetTile != None:
            targetTile.inPath = True
            self.__path.append(targetTile)
            targetTile = targetTile.parent
        self.__path.reverse()

    def emptyPath(self):
        while(len(self.__path) > 0): self.__path.pop().inPath = False
        self.__targetTile   = None
        self.__startTile    = None
        self.__velocity     = (0, 0) 

    def resetPath(self, targetTile : object):
        self.emptyPath()
        if targetTile.selectable:
            self.__findPath(targetTile)

    # pops off the path
    # returns True if the path is not empty and the targetTile
    # so that the user knows if we are still moving
    def followPath(self):
        stillMoving  = False
        
        if self.__targetTile is None and self.__path:
            # we have just started following the path
            self.__targetTile = self.__path.pop(0)
            self.__targetTile.inPath = False
        
        # need to check the length of the path
        if self.__path:
            self.__startTile    = self.__targetTile
            self.__targetTile   = self.__path.pop(0)

            self.__targetTile.inPath = False
            self.__calcVelocity()
            stillMoving = True

        return stillMoving, self.__targetTile

    def __calcVelocity(self):
        velocityX = round((self.__targetTile.X - self.__startTile.X) / self.__moveSpeed, 1)
        velocityY = round((self.__targetTile.Y - self.__startTile.Y) / self.__moveSpeed, 1)
        self.__velocity = (velocityX, velocityY)

    def moveUnitByVelocity(self, unit):
        finishedMoving = False
        if unit and self.__velocity != (0, 0):
            unit.X += self.__velocity[0]
            unit.Y += self.__velocity[1]

            if round(unit.X, 1) == self.__targetTile.X and round(unit.Y, 1) == self.__targetTile.Y:
                unit.X, unit.Y = self.__targetTile.X, self.__targetTile.Y
                finishedMoving = True
        else:
            finishedMoving = True

        return finishedMoving