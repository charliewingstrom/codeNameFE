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
        self.__menuCursor   = AssetLoader.assets["menu-cursor.png"]

        # keep the menu options to the button images
        self.__optionsToButtons = {
            menuOptions.wait    : AssetLoader.assets["wait-button.png"],
            menuOptions.items   : AssetLoader.assets["items-button.png"],
            menuOptions.trade   : AssetLoader.assets["items-button.png"],
            menuOptions.attack  : AssetLoader.assets["attack-button.png"]
        }

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
        for option in self.__options:
            screen.blit(self.__optionsToButtons[option], (gameWidth - 300, Y))
            Y+= 165