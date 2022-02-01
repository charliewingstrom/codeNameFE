from assetLoader import AssetLoader

class Inventory():
    
    def __init__(self):
        self.X = 300
        self.Y = 300
        
        self.UI         = AssetLoader.assets["inventory.png"]
        self.menuCursor = AssetLoader.assets["menu-cursor.png"]
        
        self.__weapons          = []
        self.__items            = []
        # items or weapons that can currently be used 
        self.__avaliableItems   = []
        self.__selectionIndex   = 0
        
    def getInventory(self):
        return self.__weapons + self.__items

    def addItem(self, item):
        if issubclass(type(item), Weapon):
            self.__weapons.append(item)
        else:
            self.__items.append(item)

    def activateItem(self, unit):
        activatedItem = self.__avaliableItems[self.__selectionIndex]
        
        if isinstance(activatedItem, Weapon):
            self.equipSelectedWeapon()
            self.__selectionIndex = 0
            return False
        else:
            if activatedItem.use(unit):
                self.__items.remove(activatedItem)
            self.__selectionIndex = 0
            return True

    def trade(self, unit):
        itemToTrade = self.__avaliableItems.pop(self.__selectionIndex)
        unit.inventory.addItem(itemToTrade)
        self.__selectionIndex = 0

    def getAvaliableWeapons(self, findTilesInAttackRange, startTile, enemies):
        self.__selectionIndex = 0
        self.__avaliableItems = []
        for weapon in self.__weapons:
            for tile in findTilesInAttackRange(startTile, weapon.range):
                if tile.currentUnit != None and tile.currentUnit in enemies:
                    self.__avaliableItems.append(weapon)
                    break

    def getEquippedWeapon(self):
        if len(self.__weapons) > 0:
            return self.__weapons[0]
        return None

    def equipSelectedWeapon(self):
        weaponToEquip = self.__avaliableItems[self.__selectionIndex]
        self.__weapons.remove(weaponToEquip)
        self.__weapons.insert(0, weaponToEquip)
        self.__avaliableItems.remove(weaponToEquip)
        self.__avaliableItems.insert(0, weaponToEquip)
        
    
    # gets largest range of all weapons in the inventory
    def getBestRange(self):
        MAX_RANGE = 256
        largestRange = [MAX_RANGE,0]
        if len(self.__weapons) > 0:
            largestRange[0] = self.__weapons[0].range[0]
            for weapon in self.__weapons:
                if weapon.range[1] > largestRange[1]:
                    largestRange[1] = weapon.range[1]
                if weapon.range[0] < largestRange[0]:
                    largestRange[0] = weapon.range[0]
        return largestRange

    def setAllItemsAvaliable(self):
        self.__avaliableItems = self.__weapons + self.__items
    
    def draw(self, screen, font):
        Yoffset = 50
        screen.blit(self.UI, (self.X, self.Y))
        screen.blit(self.menuCursor, (self.X+15, self.Y+15+(75*self.__selectionIndex)))
        for item in self.__avaliableItems:
            itemT = font.render(item.name, True, (0,0,0))
            itemR = itemT.get_rect()
            itemR.center = (self.X+250, self.Y+Yoffset)
            screen.blit(itemT, itemR)
            Yoffset += 75

        screen.blit(self.UI, (self.X+630, self.Y))

        highlightedItem = self.__avaliableItems[self.__selectionIndex]

        highlightedItem.drawDesc(screen, font, self.X + 630, self.Y)


    def down(self):
        if self.__selectionIndex < len(self.__avaliableItems) - 1:
            self.__selectionIndex += 1
        else:
            self.__selectionIndex = 0
    def up(self):
        if self.__selectionIndex > 0:
            self.__selectionIndex -= 1
        else:
            self.__selectionIndex = len(self.__avaliableItems) - 1

class Item():

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.uses = 1
        self.UI = AssetLoader.assets["inventory.png"]

    def drawDesc(self, screen, font, x, y):
        screen.blit(self.UI, (x, y))
        middle = self.UI.get_width() / 2
        descT = font.render(self.description, True, (0,0,0))
        descR = descT.get_rect()
        descR.center = (x+ middle, y + 50)

        usesT = font.render("Uses: "+str(self.uses), True, (0,0,0))
        usesR = usesT.get_rect()
        usesR.center = (x+150, y+300)

        screen.blit(descT, descR)
        screen.blit(usesT, usesR)

class HealingItem(Item):
    def __init__(self, name = "generic heal", description = "Heals 10 HP"):
        super().__init__(name, description)
        self.power = 10
        self.uses = 3

    # return True if we are out of uses
    def use(self, unit):
        unit.addHp(self.power)
        self.uses -= 1
        return self.uses <= 0
            
class Weapon(Item):
    def __init__(self, name = "genericW", description = "Basic Weapon"):
        super().__init__(name, description)
        self.range = (1, 1)
        self.uses = 45
        self.might = 5
        self.hit = 80
        self.crit = 0

    def drawDesc(self, screen, font, x, y):
        super().drawDesc(screen, font,x, y)
        mightT = font.render("Mt: "+str(self.might), True, (0,0,0))
        mightR = mightT.get_rect()
        mightR.center = (x + 90, y + 150)

        hitT = font.render("Hit: "+str(self.hit), True, (0,0,0))
        hitR = hitT.get_rect()
        hitR.center = (x + 290, y + 150)

        critT = font.render("Crit: "+str(self.crit), True, (0,0,0))
        critR = critT.get_rect()
        critR.center = (x + 490, y + 150)

        screen.blit(mightT, mightR)
        screen.blit(hitT, hitR)
        screen.blit(critT, critR)


class Sword(Weapon):
    def __init__(self):
        super().__init__("Sword", "Basic Blade")
        self.hit = 90

class Bow(Weapon):
    def __init__(self):
        super().__init__("Bow", "Attack from a Distance")
        self.range = (2, 3)

class Javelin(Weapon):
    def __init__(self):
        super().__init__("Javelin", "Throwable Spear")
        self.range = (1, 2)
