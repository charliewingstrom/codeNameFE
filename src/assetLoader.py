import pygame
import os

class AssetLoader(object):
    assets = {}

    def __init__(self):
        pass

    def loadAssets(self):
        for file in os.listdir("./assets"):
            AssetLoader.assets[file] = pygame.image.load("./assets/" + file).convert_alpha()
