import pygame
from pathlib import Path
inventoryUI = pygame.image.load(Path(__file__).parent / "../assets/inventory.png") 
menuCursor = pygame.image.load(Path(__file__).parent / "../assets/menu-cursor.png")

class Inventory():
    
    def __init__(self):
        self.X = 300
        self.Y = 300
        self.weapons = []
        self.items = []
        self.avaliableItems = []
        self.selectionIndex = 0
        
    def getInventory(self):
        return self.weapons + self.items

    def addItem(self, item):
        if issubclass(type(item), Weapon):
            self.weapons.append(item)
        else:
            self.items.append(item)

    def activateItem(self, unit):
        activatedItem = self.avaliableItems[self.selectionIndex]
        
        if isinstance(activatedItem, Weapon):
            self.equipSelectedWeapon()
            self.selectionIndex = 0
            return False
        else:
            if activatedItem.use(unit):
                self.items.remove(activatedItem)
            self.selectionIndex = 0
            return True

    def getEquippedWeapon(self):
        if len(self.weapons) > 0:
            return self.weapons[0]
        return None

    def equipSelectedWeapon(self):
        weaponToEquip = self.avaliableItems[self.selectionIndex]
        self.weapons.remove(weaponToEquip)
        self.weapons.insert(0, weaponToEquip)
        self.avaliableItems.remove(weaponToEquip)
        self.avaliableItems.insert(0, weaponToEquip)
        
    
    # gets largest range of all weapons in the inventory
    def getBestRange(self):
        largestRange = [0,0]
        if len(self.weapons) > 0:
            largestRange[0] = self.weapons[0].range[0]
            for weapon in self.weapons:
                if weapon.range[1] > largestRange[1]:
                    largestRange[1] = weapon.range[1]
                if weapon.range[0] < largestRange[0]:
                    largestRange[0] = weapon.range[0]
        return largestRange

    def draw(self, screen, font):
        Yoffset = 50
        screen.blit(inventoryUI, (self.X, self.Y))
        screen.blit(menuCursor, (self.X+15, self.Y+15+(75*self.selectionIndex)))
        for item in self.avaliableItems:
            itemT = font.render(item.name, True, (0,0,0))
            itemR = itemT.get_rect()
            itemR.center = (self.X+250, self.Y+Yoffset)
            screen.blit(itemT, itemR)
            Yoffset += 75

        screen.blit(inventoryUI, (self.X+630, self.Y))
        highlightedItem = self.avaliableItems[self.selectionIndex]

        highlightedItem.drawDesc(screen, font, self.X + 630, self.Y)


    def down(self):
        if self.selectionIndex < len(self.avaliableItems) - 1:
            self.selectionIndex += 1
        else:
            self.selectionIndex = 0
    def up(self):
        if self.selectionIndex > 0:
            self.selectionIndex -= 1
        else:
            self.selectionIndex = len(self.avaliableItems) - 1

class Item():

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.uses = 1

    def drawDesc(self, screen, font, x, y):
        screen.blit(inventoryUI, (x, y))
        middle = inventoryUI.get_width() / 2
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
        if unit.hp + self.power < unit.maxHp:
            unit.hp += self.power
        else: 
            unit.hp = unit.maxHp
        self.uses -= 1
        return self.uses <= 0
            
class Weapon(Item):
    def __init__(self, name = "genericW", description = "Basic Weapon"):
        super().__init__(name, description)
        self.range = [1, 1]
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


class Javelin(Weapon):
    def __init__(self):
        super().__init__("Javelin", "Throwable Spear: Good for hitting enemies at a range with more damage than an arrow.")
        self.range = [1, 2]
