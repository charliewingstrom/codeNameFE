import pygame
from Tile import Tile
from Unit import Unit
class PlayerUnit(Unit):

    def __init__(self, window, name):
        super().__init__(window, name)