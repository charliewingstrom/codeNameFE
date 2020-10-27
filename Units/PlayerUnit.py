import pygame
from Tile import Tile
from Unit import Unit
class PlayerUnit(Unit):

    def __init__(self, window, name):
        super().__init__(window, name)

    ## if direction is > 0, go up in index, otherwise go down in index
    def changeCurrentWeapon(self, direction):
        if (direction > 0):
            self.equippedWeaponIndex+= 1
            if (self.equippedWeaponIndex > len(self.weapons) - 1):
                self.equippedWeaponIndex = 0
            
        else:
            self.equippedWeaponIndex -= 1
            if (self.equippedWeaponIndex < 0):
                self.equippedWeaponIndex = len(self.weapons)-1
