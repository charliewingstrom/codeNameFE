import pygame
import random
from pathlib import Path

## custom classes
from tileMap import Map
from cursor import Cursor
from ui import MainMenu, BattleForcast, CombatUI, MapUnitUI, UnitInfo
from inventory import Inventory, Weapon, HealingItem
from animation import Animation


pygame.init()
gameWidth = 1920
gameHeight = 1080
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Code FE")
running = True

#------ load assets --------
## Characters
protagPicA = pygame.image.load(Path(__file__).parent / "../assets/protag_A.png")
protagPicB = pygame.image.load(Path(__file__).parent / "../assets/protag_B.png")

combatUnit1 = pygame.image.load(Path(__file__).parent / "../assets/Combat-1.png")
combatUnit2 = pygame.image.load(Path(__file__).parent / "../assets/Combat-2.png")
combatUnit3 = pygame.image.load(Path(__file__).parent / "../assets/Combat-3.png")
combatUnit4 = pygame.image.load(Path(__file__).parent / "../assets/Combat-4.png")
combatUnit5 = pygame.image.load(Path(__file__).parent / "../assets/Combat-5.png")
combatUnit6 = pygame.image.load(Path(__file__).parent / "../assets/Combat-6.png")

## Menu
waitButton = pygame.image.load(Path(__file__).parent / "../assets/wait-button.png")
itemsButton = pygame.image.load(Path(__file__).parent / "../assets/items-button.png")
attackButton = pygame.image.load(Path(__file__).parent / "../assets/attack-button.png")
menuCursor = pygame.image.load(Path(__file__).parent / "../assets/menu-cursor.png")

### Combat and UI
levelUpUI = pygame.image.load(Path(__file__).parent / "../assets/levelUp.png") 
## backgrounds
attacingBackground = pygame.image.load(Path(__file__).parent / "../assets/attacking-background.png")
map1background = pygame.image.load(Path(__file__).parent / "../assets/level1Background.png")
#---------------------------

# globals
currentUnit = None
defendingUnit = None
## map
tileSize = 96
mapWidth = 32
mapHeight = 19
maxDistance = 256

## camera
yCamera = 0
xCamera = 0

## movement
moving = False
moveVelocity = ()
moveSpeed = 10
targetTile = None

## combat
currentUnitAttacking = True
defendingUnitAttacking = True
experience = 0

## player state
inMainMenu = True
playerTurn = True
viewingUnitInfo = False
selectingTile = False
selectingAction = False
selectingItems = False
selectingWeapon = False
selectingAttack = False
attacking = False
finishedAttacking = True
addingExp = False
levelingUp = False

## menu items
menuOptions = []
menuOptions.append("wait")
menuSelectionIndex = 0

## unit arrays
playerUnits = []
enemyUnits = []
activeEnemyUnits = []

### attacking selection
unitsInRange = []
attackUnitIndex = 0

font = pygame.font.Font('freesansbold.ttf', 52)


# custom classes

        







        


class Unit():

    def __init__(self, X, Y):
        self.name = "generic"
        self.level = 1
        self.exp = 0
        
        # stats
        self.maxHp = 15
        self.hp = self.maxHp
        self.attack = 10
        self.defense = 5
        self.speed = 6
        self.skill = 6
        self.luck = 4
        self.mov = 5

        # growths
        self.hpG = 50
        self.attackG = 50
        self.defenseG = 50
        self.speedG = 50
        self.skillG = 50
        self.luckG = 50
        self.inventory = Inventory()
        self.X = X
        self.Y = Y

        self.fieldPics = [pygame.transform.scale(protagPicA, (tileSize, tileSize)), pygame.transform.scale(protagPicB, (tileSize, tileSize))] 
        self.aniTimer = 5
        self.combatAnimation = Animation([combatUnit1,combatUnit2, combatUnit3,combatUnit4, combatUnit5, combatUnit6,combatUnit5, combatUnit4, combatUnit3, combatUnit2, combatUnit1])

        self.active = True

    def getStats(self):
        return [self.maxHp, self.attack, self.defense, self.speed, self.skill, self.luck]

    def addToStat(self, index, amount):
        if index == 0:
            self.maxHp += amount
        if index == 1:
            self.attack += amount
        if index == 2:
            self.defense += amount
        if index == 3:
            self.speed += amount
        if index == 4:
            self.skill += amount
        if index == 5:
            self.luck += amount

    def getGrowths(self):
        return [self.hpG, self.attackG, self.defenseG, self.speedG, self.skillG, self.luckG]

    def getEquippedWeapon(self):
        if len(self.getInventory()) > 0:
            return self.getInventory()[0] 
        return None
    
    def getInventory(self):
        return self.inventory.getInventory()

    def getAttackRange(self):
        if len(self.getInventory()) > 0:
            return self.getEquippedWeapon().range
        return [0,0]

    def draw(self, screen):
        screen.blit(self.fieldPics[0], (self.X*tileSize + xCamera, self.Y*tileSize + yCamera))
        self.aniTimer -= 1
        if self.aniTimer < 0:
            tmpPic = self.fieldPics.pop(0)
            self.fieldPics.append(tmpPic)
            self.aniTimer = 5
        
        ## draw health bar 
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.X*tileSize + xCamera, (self.Y*tileSize)+tileSize-5 + yCamera, tileSize, 5))
        healthPercent = self.hp/self.maxHp
        color = (0, 255, 0)
        if healthPercent < 0.2:
            color = (255, 0, 0)
        elif healthPercent < 0.5:
            color = (238, 255, 0)
        pygame.draw.rect(screen, color, pygame.Rect(self.X*tileSize + xCamera, (self.Y*tileSize)+tileSize-5 + yCamera, healthPercent * tileSize, 5))

class Exp():

    def __init__(self):
        self.currUnit = None
        self.expToAdd = 0

    def setup(self, unit, exp):
        self.currUnit = unit
        self.expToAdd = exp
        self.delay = 10

    def draw(self, screen):
        if self.currUnit != None:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((gameWidth / 2) - (gameWidth/4), 900, gameWidth / 3, 20))
            pygame.draw.rect(screen, (252, 219, 3), pygame.Rect((gameWidth / 2) - (gameWidth/4), 900, (gameWidth / 3) * (self.currUnit.exp / 100), 20))
            if self.expToAdd > 6 and self.currUnit.exp + 6 < 100:
                self.currUnit.exp += 6
                self.expToAdd -= 6
            elif self.expToAdd > 0:
                self.currUnit.exp += 1
                self.expToAdd -= 1
            elif self.delay > 0:
                self.delay -= 1
            else:
                self.delay = 10
                return True
        return False

class LevelUp():
    def __init__(self):
        self.currUnit = None
        self.delay = 5
        self.levelIndex = 0
        self.hasLeveledStat = [False, False, False, False, False, False]
        self.statsLeveled = []
        self.X = (gameWidth/2)-(levelUpUI.get_width()/2)
        self.Y = (gameHeight/2)-(levelUpUI.get_height()/2)
    
    def roll(self, unit):
        self.currUnit = unit
        self.hasLeveledStat = [False, False, False, False, False, False]
        self.statsLeveled = []
        for i in range(len(self.currUnit.getGrowths())):
            if self.currUnit.getGrowths()[i] > random.randint(0, 99):
                self.statsLeveled.append(i)


    def getHasLeveled(self, index):
        if self.hasLeveledStat[index]:
            return " += 1"
        else:
            return ""

    def draw(self, screen):
        if self.currUnit != None:
            screen.blit(levelUpUI, (self.X, self.Y))

            hpT = font.render(str(self.currUnit.maxHp)+self.getHasLeveled(0), True, (0,0,0))
            hpR = hpT.get_rect()
            hpR.topleft = (self.X+380, self.Y+370)

            strT = font.render(str(self.currUnit.attack)+self.getHasLeveled(1), True, (0,0,0))
            strR = hpT.get_rect()
            strR.topleft = (self.X+380, self.Y+520)

            defT = font.render(str(self.currUnit.defense)+self.getHasLeveled(2), True, (0,0,0))
            defR = hpT.get_rect()
            defR.topleft = (self.X+380, self.Y+670)

            spdT = font.render(str(self.currUnit.speed)+self.getHasLeveled(3), True, (0,0,0))
            spdR = hpT.get_rect()
            spdR.topleft = (self.X+380, self.Y+820)

            sklT = font.render(str(self.currUnit.skill)+self.getHasLeveled(4), True, (0,0,0))
            sklR = hpT.get_rect()
            sklR.topleft = (self.X+900, self.Y+370)

            lckT = font.render(str(self.currUnit.luck)+self.getHasLeveled(5), True, (0,0,0))
            lckR = hpT.get_rect()
            lckR.topleft = (self.X+900, self.Y+520)

            screen.blit(hpT, hpR)
            screen.blit(strT, strR)
            screen.blit(defT, defR)
            screen.blit(spdT, spdR)
            screen.blit(sklT, sklR)
            screen.blit(lckT, lckR)

            ## count down delay, either add 1 to level stat, or wait after all the stats are shown or reset and return True 
            self.delay -= 1
            if self.delay <= 0:
                if self.levelIndex > len(self.statsLeveled):
                    self.levelIndex = 0
                    self.delay = 5
                    self.currUnit = None
                    return True
                elif self.levelIndex == len(self.statsLeveled):
                    self.levelIndex+=1
                    self.delay = 10
                else:
                    self.delay = 5
                    self.currUnit.addToStat(self.statsLeveled[self.levelIndex], 1)
                    self.hasLeveledStat[self.statsLeveled[self.levelIndex]] = True
                    self.levelIndex+=1
        return False
                    


## custom class instances
myMainMenu = MainMenu()
map1 = Map(mapWidth, mapHeight, map1background, tileSize)
myBattleForcast = BattleForcast(gameWidth)
mainCursor = Cursor(tileSize, mapWidth, mapHeight, gameWidth, gameHeight)
myCombatUI = CombatUI(0, gameHeight - 385)
myUnitInfo = UnitInfo()
myMapUnitUI = MapUnitUI(gameWidth, gameHeight)
myExp = Exp()
myLevelUp = LevelUp()

## width first, height second (width goes from left to right, height goes from top to bottom)
protag = Unit(3, 3)
bow = Weapon("bow")
bow.range = [3,3]
protag.inventory.addItem(bow)
Jagen = Unit(3, 5)
Jagen.exp = 90
Jagen.inventory.addItem(Weapon("Sword"))
lance = Weapon("Javelin")
lance.range = [1,2]
lance.might = 3
Jagen.inventory.addItem(lance)
Jagen.inventory.addItem(HealingItem())
Jagen.name = 'Jagen'
Jagen.attack = 10
Jagen.defense = 10
Jagen.speed = 9

myLevelUp.currUnit = Jagen

enemy = Unit(9, 5)
enemy.inventory.addItem(Weapon())
enemy1 = Unit(9, 6)
enemy1.inventory.addItem(Weapon())
enemy1.defense = 7
# Setting up for game
map1.addUnitToMap(enemy)
map1.addUnitToMap(enemy1)
map1.addUnitToMap(protag)
map1.addUnitToMap(Jagen)
playerUnits.append(protag)
playerUnits.append(Jagen)
enemyUnits.append(enemy)
enemyUnits.append(enemy1)
activeEnemyUnits.append(enemy)
activeEnemyUnits.append(enemy1)

for i in range(3):
    map1.tiles[i][4].walkable = False
for i in range(5):
    map1.tiles[4][i].walkable = False
for i in range(3):
    map1.tiles[i+5][4].walkable = False
for i in range(5):
    map1.tiles[9][i].walkable = False
for i in range(3):
    map1.tiles[i+10][4].walkable = False
for i in range(5):
    map1.tiles[14][i].walkable = False
for i in range(14):
    map1.tiles[i][7].walkable = False


def findPlayerTarget(tiles, unit):
    possibleTargets = []
    for tile in tiles:
        for attackableTile in findTilesInAttackRange(tile, unit.getAttackRange()):
            if attackableTile.currentUnit != None and attackableTile.currentUnit in playerUnits:
                possibleTargets.append((attackableTile.currentUnit, tile))
    #print(possibleTargets[0][0])
    bestTarget = (None, None)
    for target in possibleTargets:
        if target[0].hp < (unit.attack + unit.getEquippedWeapon().might) - target[0].defense:
            return target
        elif bestTarget == (None, None):
            bestTarget = target
        elif bestTarget[0].defense > target[0].defense:
            bestTarget = target
        
    return bestTarget        

def findTilesInMovRange(unit):
    map1.reset()
    currentTile = map1.tiles[unit.X][unit.Y]
    currentTile.distance = 0
    queue = []
    added = []
    tilesInRange = []
    queue.append(currentTile)
    added.append(currentTile)
    while len(queue) > 0:
        queue.sort(key=lambda tile:tile.distance)
        currTile = queue.pop(0)
        if unit in playerUnits:
            if currTile.distance <= currentUnit.mov and currTile.walkable and (currTile.currentUnit == None or currTile.currentUnit in playerUnits):
                tilesInRange.append(currTile)
                added.append(currTile)
                for tile in currTile.adjList:
                    if tile not in added:
                        altDist = currTile.distance + 1
                        if tile.distance > altDist:
                            tile.distance = altDist
                            tile.parent = currTile
                        queue.append(tile)
        else:
            if currTile.distance <= currentUnit.mov and currTile.walkable and (currTile.currentUnit == None or currTile.currentUnit in enemyUnits):
                tilesInRange.append(currTile)
                added.append(currTile)
                for tile in currTile.adjList:
                    if tile not in added:
                        altDist = currTile.distance + 1
                        if tile.distance > altDist:
                            tile.distance = altDist
                            tile.parent = currTile
                        queue.append(tile)
    toReturn = []
    for tile in tilesInRange:
        if tile.currentUnit == None or tile.currentUnit == unit:
            toReturn.append(tile)
    return toReturn

def getMoveVelocity(start, end, moveSpeed):
    velocityX = (end.X - start.X) / moveSpeed
    velocityY = (end.Y - start.Y) / moveSpeed
    return (velocityX, velocityY)

def resetAfterAction(unit):
    if unit:
        currentUnit.active = False
    map1.reset()

def findTilesInAttackRange(startTile, atkRange):

    rangeMin = atkRange[0]
    rangeMax = atkRange[1]
    visited = []
    inRange = []
    queue = []
    currTile = startTile
    visited.append(currTile)
    queue.append(currTile)
    
    dist = {}
    dist[currTile] = 0

    while (len(queue) > 0):
        currTile = queue.pop(0)
        if dist[currTile] <= rangeMax:
            if dist[currTile] >= rangeMin:
                inRange.append(currTile)
            for tile in currTile.adjList:
                if tile not in visited:
                    visited.append(tile)
                    queue.append(tile)
                    dist[tile] = dist[currTile] + 1
    return inRange

def setTilesInRangeAttackable(startTile, atkRange, tilesInRange):
    startTile.selectable = True
    for atkTile in findTilesInAttackRange(startTile, atkRange):
        if atkTile not in tilesInRange:
            atkTile.attackable = True



def checkMapUI():
    if mainCursor.X * tileSize > gameWidth / 2:
        myMapUnitUI.X = 10
        myBattleForcast.X = 10
    else:
        myMapUnitUI.X = gameWidth - 460
        myBattleForcast.X = gameWidth - 500
    
    ## check if cursor is over a player
    cursorTileUnit = map1.tiles[mainCursor.X][mainCursor.Y].currentUnit
    myMapUnitUI.reset(cursorTileUnit)




# main game loop
while running:

    #### moving ####
    keys = pygame.key.get_pressed()

    
    # if something is moving there shouldn't be any other input accepted
    if moving:
        currentUnit.X += moveVelocity[0]
        currentUnit.Y += moveVelocity[1]
        if round(currentUnit.X) == targetTile.X and round(currentUnit.Y) == targetTile.Y:
            ## finish moving
            currentUnit.X = targetTile.X
            currentUnit.Y = targetTile.Y
            currentUnitStartingTile.currentUnit = None
            targetTile.currentUnit = currentUnit
            currentUnitTile = targetTile

            moving = False
            if not playerTurn:
                print("setup attack...")
                myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, map1)
                myBattleForcast.roll()
                attacking = True
                
            else:
                selectingAction = True
                menuOptions = []
                menuSelectionIndex = 0
                menuOptions.insert(0, "wait")
                if len(currentUnit.getInventory()) > 0:
                    menuOptions.insert(0, "items")
                unitsInRange = []
                ## TODO check to see if they can attack with any weapon (ie all ranges)
                for tile in findTilesInAttackRange(currentUnitTile, currentUnit.inventory.getBestRange()):
                    tile.attackable = True
                    if tile.currentUnit != None and tile.currentUnit in enemyUnits:
                        unitsInRange.append(tile.currentUnit)
                if len(unitsInRange) > 0:
                    menuOptions.insert(0, "attack")
    # not moving
    else: 
        ## automated enemy phase actions
        if not playerTurn and not attacking:
            if len(activeEnemyUnits) > 0:
                currentUnit = activeEnemyUnits.pop(0)
                currentUnitStartingTile = map1.tiles[currentUnit.X][currentUnit.Y]
                enemyTilesInRange = findTilesInMovRange(currentUnit)
                defendingUnit, targetTile = findPlayerTarget(enemyTilesInRange, currentUnit)
                ## for now if a unit is not in range, don't move
                if defendingUnit != None:
                    moveVelocity = getMoveVelocity(currentUnitStartingTile, targetTile, moveSpeed)
                    moving = True
                
            else:
                playerTurn = True
                for unit in playerUnits:
                    unit.active = True
                for unit in enemyUnits:
                    activeEnemyUnits.append(unit)
        

        ## menu and cursor controls 
        ## if keys (they are up here because you should be able to hold the key)
        elif playerTurn and not (selectingAction or selectingAttack or selectingWeapon or selectingItems):
            # cursor controls
            if keys[pygame.K_DOWN]:
                yCamera += mainCursor.down(yCamera)
                checkMapUI()
            if keys[pygame.K_UP]:
                yCamera += mainCursor.up(yCamera)
                checkMapUI()
            if keys[pygame.K_RIGHT]:
                xCamera += mainCursor.right(xCamera)
                checkMapUI()
            if keys[pygame.K_LEFT]:
                xCamera += mainCursor.left(xCamera)
                checkMapUI()
            # end cursor controls

        # menu movement controls
        elif playerTurn and selectingAction:
            if keys[pygame.K_DOWN]:
                if (menuSelectionIndex < len(menuOptions)-1):
                    menuSelectionIndex+=1
            if keys[pygame.K_UP]:
                if (menuSelectionIndex > 0):
                    menuSelectionIndex-=1
        # end menu movement controls

        for event in pygame.event.get():
            ## quit
            if event.type == pygame.QUIT:
                running = False
            if inMainMenu: 
                if event.type == pygame.KEYDOWN:
                    inMainMenu = False
            # player turn
            elif playerTurn:
                # picking a unit to attack
                if selectingAttack:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        attacking = True
                        myBattleForcast.roll()

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_UP):
                        if attackUnitIndex < len(unitsInRange) - 1:
                            attackUnitIndex += 1
                        else:
                            attackUnitIndex = 0
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, map1)

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_DOWN):
                        if attackUnitIndex > 0:
                            attackUnitIndex -= 1
                        else:
                            attackUnitIndex = len(unitsInRange)-1
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, map1)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        selectingAttack = False
                        selectingAction = True

                elif selectingItems:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        selectingItems = False
                        selectingAction = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        currentUnit.inventory.up()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        currentUnit.inventory.down()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        if currentUnit.inventory.activateItem(currentUnit):
                            currentUnitTile = None
                            currentUnitStartingTile = None
                            currentUnit.active = False
                            currentUnit = None
                            defendingUnit = None
                            selectingTile = False
                            selectingAction = False
                            selectingAttack = False
                            selectingItems = False
                            map1.reset()

                elif selectingWeapon:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        currentUnit.inventory.equipSelectedWeapon()
                        unitsInRange = []
                        map1.reset()
                        for tile in findTilesInAttackRange(currentUnitTile, currentUnit.inventory.avaliableItems[0].range):
                            if tile.currentUnit != None and tile.currentUnit in enemyUnits:
                                unitsInRange.append(tile.currentUnit)
                            tile.attackable = True

                        selectingWeapon = False
                        selectingAttack = True
                        attackUnitIndex = 0
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, map1)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        currentUnit.inventory.up()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        currentUnit.inventory.down()

                ### selecting action in menu
                elif selectingAction:
                    # action selected from menu
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        if menuOptions[menuSelectionIndex] == 'wait':
                            resetAfterAction(currentUnit)
                            currentUnit = None
                            currentUnitStartingTile = None
                            currentUnitTile = None
                            selectingAction = False
                            
                            
                        if menuOptions[menuSelectionIndex] == 'attack':
                            selectingAction = False
                            selectingWeapon = True
                            currentUnit.inventory.selectionIndex = 0
                            ## TODO get the weapons that can be used to attack
                            currentUnit.inventory.avaliableItems = []
                            for weapon in currentUnit.inventory.weapons:
                                for tile in findTilesInAttackRange(currentUnitTile, weapon.range):
                                    if tile.currentUnit != None and tile.currentUnit in enemyUnits:
                                        currentUnit.inventory.avaliableItems.append(weapon)
                                        break

                        if menuOptions[menuSelectionIndex] == 'items':
                            selectingItems = True
                            selectingAction = False
                            currentUnit.inventory.avaliableItems = currentUnit.getInventory()
                    # go back to selecting tile
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        map1.reset()
                        currentUnitTile.currentUnit = None
                        currentUnit.X = currentUnitStartingTile.X
                        currentUnit.Y = currentUnitStartingTile.Y
                        currentUnitStartingTile.currentUnit = currentUnit
                        currentUnitTile = currentUnitStartingTile
                        selectingTile = True
                        selectingAction = False
                        tilesInRange = findTilesInMovRange(currentUnit)
                        for tile in tilesInRange:
                            if tile.currentUnit == None or tile.currentUnit == currentUnit:
                                tile.selectable = True
                                for atkTile in findTilesInAttackRange(tile, currentUnit.inventory.getBestRange()):
                                    if atkTile not in tilesInRange:
                                        atkTile.attackable = True

                ### selecting what tile to move to 
                elif selectingTile:
                    # Select tile and get ready to move to it
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        tileToMoveTo = map1.tiles[mainCursor.X][mainCursor.Y]
                        if tileToMoveTo.selectable:
                            targetTile = tileToMoveTo
                            moving = True
                            selectingTile = False
                            moveVelocity = getMoveVelocity(currentUnitTile, targetTile, moveSpeed)
                            map1.reset()

                    # Stop selecting tile
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        map1.reset()
                        currentUnit = None
                        currentUnitTile = None
                        currentUnitStartingTile = None
                        selectingTile = False

                elif viewingUnitInfo:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        viewingUnitInfo = False

                ### no unit selected, waiting for next unit to be selected
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        playerTurn = False
                        selectingAction = False
                    # Select unit and show their range
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        
                        # get the unit that cursor is on
                        currentTile = map1.tiles[mainCursor.X][mainCursor.Y]
                        currentUnit = currentTile.currentUnit
                        
                        # get tiles in range of that unit and highlight them
                        if currentUnit != None and currentUnit.active and currentUnit in playerUnits:
                            # need to save this for later
                            currentUnitTile = currentTile
                            currentUnitStartingTile = currentTile
                            tilesInRange = findTilesInMovRange(currentUnit)
                            for tile in tilesInRange:
                                if tile.currentUnit == None or tile.currentUnit == currentUnit:
                                    setTilesInRangeAttackable(tile, currentUnit.inventory.getBestRange(), tilesInRange)
                                    # tile.selectable = True
                                    # for atkTile in findTilesInAttackRange(tile, currentUnit.inventory.getBestRange()):
                                    #     if atkTile not in tilesInRange:
                                    #         atkTile.attackable = True
                            selectingTile = True
                        elif currentUnit != None and currentUnit in enemyUnits:
                            tilesInRange = findTilesInMovRange(currentUnit)
                            for tile in tilesInRange:
                                if tile.currentUnit == None:
                                    tile.selectable = True
                                    for atkTile in findTilesInAttackRange(tile, currentUnit.inventory.getBestRange()):
                                        if atkTile not in tilesInRange:
                                            atkTile.attackable = True
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentUnit = None
                        map1.reset()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                        currentTile = map1.tiles[mainCursor.X][mainCursor.Y]
                        if currentTile.currentUnit != None:
                            currentUnit = currentTile.currentUnit
                            myUnitInfo.reset(currentUnit)
                            viewingUnitInfo = True
                        
    
    #### drawing ####
    if inMainMenu:
        myMainMenu.draw(screen)
    
    ## attacking ####
    elif attacking:
        screen.blit(attacingBackground, (0, 0))
        # if current player attacking, 
        ## if player will hit, play hit animation and remove the required health from the opponent
        ### then set current player attacking to false
        #### if the unit died, remove the unit and end combat
        ### if the opposing unit is still alive and will counter
        #### if the unit will hit
        ##### play opposing unit attack animation and remove required health
        #### if the unit will miss
        ##### play miss animation 

        if currentUnitAttacking:
            screen.blit(pygame.transform.flip(combatUnit1, True, False), (0, 0))
            
            if myBattleForcast.attackingUnitWillHit:
                if currentUnit.combatAnimation.draw(screen, 0, 0, False):
                    ## remove health
                    print("Damage = " + str(myBattleForcast.attackingUnitDmg))
                    defendingUnit.hp -= myBattleForcast.attackingUnitDmg
                    currentUnitAttacking = False
                    print("current unit hit")
                    if currentUnit in playerUnits:
                        experience += myBattleForcast.attackingUnitDmg
            ## unit will miss, play miss animation
            else:
                if currentUnit.combatAnimation.draw(screen, 0, 0, False):
                    print("current unit miss")
                    currentUnitAttacking = False
                    experience += 1
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)

        elif defendingUnitAttacking:
            if defendingUnit.hp > 0:
                screen.blit(combatUnit1, (0, 0))
                if myBattleForcast.defendingUnitCanCounter:
                    if myBattleForcast.defendingUnitWillHit:
                        if defendingUnit.combatAnimation.draw(screen, 0, 0, True):
                            # remove health
                            currentUnit.hp -= myBattleForcast.defendingUnitDmg
                            defendingUnitAttacking = False
                            if defendingUnit in playerUnits:
                                experience += myBattleForcast.defendingUnitDmg
                            print("defending unit hit")
                            if currentUnit.hp <= 0:
                                if currentUnit in playerUnits:
                                    playerUnits.remove(currentUnit)
                                elif currentUnit in enemyUnits:
                                    enemyUnits.remove(currentUnit)
                                    experience += 30
                                map1.tiles[currentUnit.X][currentUnit.Y].currentUnit = None
                    ## unit will miss, play miss animation
                    else:
                        if defendingUnit.combatAnimation.draw(screen, 0, 0, True):
                            print("defending unit miss")
                            defendingUnitAttacking = False
                            experience += 1
                else:
                    screen.blit(pygame.transform.flip(combatUnit1, True, False), (0, 0))
                    defendingUnitAttacking = False
            else:
                defendingUnitAttacking = False
                print("defending unit died")
                ## remove unit from game
                if defendingUnit in playerUnits:
                    playerUnits.remove(defendingUnit)
                elif defendingUnit in enemyUnits:
                    enemyUnits.remove(defendingUnit)
                    activeEnemyUnits.remove(defendingUnit)
                    experience += 30
                map1.tiles[defendingUnit.X][defendingUnit.Y].currentUnit = None
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)

        elif finishedAttacking:
            if currentUnit.hp > 0:
                screen.blit(combatUnit1, (0, 0))
            if defendingUnit.hp > 0:
                screen.blit(pygame.transform.flip(combatUnit1, True, False), (0, 0))
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)
            if experience > 0:
                experience = 99
                addingExp = True
                if currentUnit in playerUnits:
                    myExp.setup(currentUnit, experience)
                elif defendingUnit in playerUnits:
                    myExp.setup(defendingUnit, experience)
            finishedAttacking = False

        elif levelingUp:
            if currentUnit.hp > 0:
                screen.blit(combatUnit1, (0, 0))
            if defendingUnit.hp > 0:
                screen.blit(pygame.transform.flip(combatUnit1, True, False), (0, 0))
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)
            if myLevelUp.draw(screen):
                levelingUp = False
                myLevelUp.currUnit = None
        elif addingExp:
            if currentUnit.hp > 0:
                screen.blit(combatUnit1, (0, 0))
            if defendingUnit.hp > 0:
                screen.blit(pygame.transform.flip(combatUnit1, True, False), (0, 0))
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)
            if myExp.currUnit.exp >= 100:
                levelingUp = True
                myLevelUp.currUnit = myExp.currUnit
                myLevelUp.roll(myExp.currUnit)
                myExp.currUnit.exp = 0
                myExp.currUnit.level += 1
            elif myExp.draw(screen):
                addingExp = False


        else:
            experience = 0
            currentUnitAttacking = True
            defendingUnitAttacking = True
            attacking = False
            finishedAttacking = True
            currentUnitTile = None
            currentUnitStartingTile = None
            currentUnit.active = False
            currentUnit = None
            defendingUnit = None
            selectingTile = False
            selectingAction = False
            selectingAttack = False
            
            map1.reset()
    
    
    
    else:
        screen.fill((0,0,0))
        map1.draw(screen, xCamera, yCamera)
        mainCursor.draw(screen)
        for unit in playerUnits:
            unit.draw(screen)
        for enemy in enemyUnits:
            enemy.draw(screen)
        
        myMapUnitUI.draw(screen, font)
        if selectingAttack:
            myBattleForcast.draw(screen, font, currentUnit, unitsInRange[attackUnitIndex])

        elif selectingItems:
            currentUnit.inventory.draw(screen, font)            
        elif selectingWeapon:
            currentUnit.inventory.draw(screen, font)

        elif selectingAction:
            screen.blit(menuCursor, (gameWidth-450, 240+(165*menuSelectionIndex)))
            Y = 200
            if "attack" in menuOptions:
                screen.blit(attackButton, (gameWidth - 300, Y))
                Y+= 165
            if "items" in menuOptions:
                screen.blit(itemsButton, (gameWidth - 300, Y))
                Y+= 165
            if "wait" in menuOptions:
                screen.blit(waitButton, (gameWidth - 300, Y))
        
        elif viewingUnitInfo:
            myUnitInfo.draw(screen, font)
                
    pygame.display.update()
    pygame.time.delay(60)
