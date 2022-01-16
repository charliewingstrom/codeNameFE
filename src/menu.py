from enum           import Enum, auto
from assetLoader    import AssetLoader

class menuOptions(Enum):
    wait    = auto()
    items   = auto()
    trade   = auto()
    attack  = auto()

class Menu(object):

    def __init__(self):
        self.__options          = []
        self.__selectionIndex   = 0

        self.__waitButton   = AssetLoader.assets["wait-button.png"]
        self.__itemsButton  = AssetLoader.assets["items-button.png"]
        self.__attackButton = AssetLoader.assets["attack-button.png"]
        self.__menuCursor   = AssetLoader.assets["menu-cursor.png"]

    def checkForMenuOptions(self, currentUnit, isEnemyInRange, isTradeInRange):
        self.__options          = []
        self.__selectionIndex   = 0

        self.__options.insert(0, menuOptions.wait)
        
        if isTradeInRange:
            self.__options.insert(0, menuOptions.trade)

        if len(currentUnit.getInventory()) > 0:
            self.__options.insert(0, menuOptions.items)

        if isEnemyInRange:
            self.__options.insert(0, menuOptions.attack)

    def checkForMenuControls(self, menuKeys):
        if menuKeys[0] and self.__selectionIndex < len(self.__options)-1:
            self.__selectionIndex += 1
        if menuKeys[1] and self.__selectionIndex > 0:
            self.__selectionIndex -= 1

    def selectOption(self):
        return self.__options[self.__selectionIndex]

    def draw(self, screen, gameWidth):
        screen.blit(self.__menuCursor, (gameWidth-450, 240+(165*self.__selectionIndex)))
        Y = 200
        # TODO rewrite this so that the order will always be the same as 
        # what is found in checkMenuOptions
        # Possibly use a dictionary with menuOptions as keys and 
        # images (buttons) as values
        if menuOptions.attack in self.__options:
            screen.blit(self.__attackButton, (gameWidth - 300, Y))
            Y+= 165
        if menuOptions.items in self.__options:
            screen.blit(self.__itemsButton, (gameWidth - 300, Y))
            Y+= 165
        if menuOptions.trade in self.__options:
            screen.blit(self.__itemsButton, (gameWidth - 300, Y))
            Y+= 165
        if menuOptions.wait in self.__options:
            screen.blit(self.__waitButton, (gameWidth - 300, Y))          
        