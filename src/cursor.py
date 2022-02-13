import pygame
from assetLoader import AssetLoader

class Cursor():

    def __init__(self, tileSize, mapWidth, mapHeight, gameWidth, gameHeight):
        self.X = 3
        self.Y = 3
        self.tileSize = tileSize
        self.__mapWidth = mapWidth
        self.__mapHeight = mapHeight
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.yCameraOffset = 0
        self.xCameraOffset = 0
        self.pic = pygame.transform.scale(AssetLoader.assets["cursor.png"], (tileSize, tileSize))
        self.__moving = False
        self.__delay = 0
        self.__pressedThisFrame = False

    def canMove(self):
        return self.__delay <= 0

    # start moving
    def __checkMoving(self):
        self.__pressedThisFrame = True
        if self.__moving:
            self.__delay = 0
        else: 
            self.__delay = 5
        self.__moving = True

    def down(self, yCamera):
        self.__checkMoving()
        if self.Y < self.__mapHeight-1:
            self.Y+=1
            if (self.Y * self.tileSize) + yCamera + self.tileSize  > self.gameHeight:
                self.yCameraOffset += 1
                return -self.tileSize
        return 0

    def up(self, yCamera):
        self.__checkMoving()
        if self.Y > 0:
            self.Y-=1
            if (self.Y * self.tileSize) + yCamera < self.tileSize:
                self.yCameraOffset -= 1
                return self.tileSize
        return 0

    def right(self, xCamera):
        self.__checkMoving()
        if self.X < self.__mapWidth-1:
            self.X+=1
            if (self.X * self.tileSize) + xCamera + self.tileSize > self.gameWidth:
                self.xCameraOffset += 1
                return -self.tileSize
        return 0

    def left(self, xCamera):
        self.__checkMoving()
        if self.X > 0:
            self.X-=1
            if (self.X * self.tileSize) + xCamera < self.tileSize:
                self.xCameraOffset -= 1
                return self.tileSize
        return 0

    def resetFromMap(self, tileMap):
        self.__mapWidth   = tileMap.getWidth()
        self.__mapHeight  = tileMap.getHeight()

    def draw(self, screen):
        self.__delay -= 1
        if not self.__pressedThisFrame and self.__delay < 0:
            self.__moving = False
        self.__pressedThisFrame = False
        screen.blit(self.pic, ((self.X*self.tileSize) - (self.xCameraOffset*self.tileSize), (self.Y*self.tileSize) - (self.yCameraOffset*self.tileSize)))