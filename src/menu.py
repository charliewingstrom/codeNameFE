import pygame
from pathlib    import Path
from enum       import Enum, auto

waitButton = pygame.image.load(Path(__file__).parent / "../assets/wait-button.png")
itemsButton = pygame.image.load(Path(__file__).parent / "../assets/items-button.png")
attackButton = pygame.image.load(Path(__file__).parent / "../assets/attack-button.png")
menuCursor = pygame.image.load(Path(__file__).parent / "../assets/menu-cursor.png")

class menuOptions(Enum):
    wait    = auto()
    items   = auto()
    attack  = auto()

class Menu(object):

    def __init__(self):
        self.__options          = []
        self.__selectionIndex   = 0

    def checkForMenuOptions(self, currentUnit, unitsInRange):
        self.__options          = []
        self.__selectionIndex   = 0

        self.__options.insert(0, menuOptions.wait)
        if len(currentUnit.getInventory()) > 0:
            self.__options.insert(0, menuOptions.items)

        if len(unitsInRange) > 0:
            self.__options.insert(0, menuOptions.attack)

    def checkForMenuControls(self, menuKeys):
        if menuKeys[0] and self.__selectionIndex < len(self.__options)-1:
            self.__selectionIndex += 1
        if menuKeys[1] and self.__selectionIndex > 0:
            self.__selectionIndex -= 1

    def selectOption(self):
        return self.__options[self.__selectionIndex]

    def draw(self, screen, gameWidth):
        screen.blit(menuCursor, (gameWidth-450, 240+(165*self.__selectionIndex)))
        Y = 200
        if menuOptions.attack in self.__options:
            screen.blit(attackButton, (gameWidth - 300, Y))
            Y+= 165
        if menuOptions.items in self.__options:
            screen.blit(itemsButton, (gameWidth - 300, Y))
            Y+= 165
        if menuOptions.wait in self.__options:
            screen.blit(waitButton, (gameWidth - 300, Y))          
        