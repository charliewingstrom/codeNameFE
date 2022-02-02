
class Camera(object):

    def __init__(self):
        self.__x = 0
        self.__y = 0

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def updateFromCursor(self, cursor, arrowKeys):
        arrowKeyPressed = False
        if cursor.canMove():
            arrowKeyPressed = any(arrowKeys)
            if arrowKeys[0]:
                self.__y += cursor.down(self.__y)
            if arrowKeys[1]:
                self.__y += cursor.up(self.__y)
            if arrowKeys[2]:
                self.__x += cursor.right(self.__x)
            if arrowKeys[3]:
                self.__x += cursor.left(self.__x)
        return arrowKeyPressed


