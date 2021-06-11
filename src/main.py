import pygame
import random
from enum import Enum, auto
from pathlib import Path

## custom classes
from tileMap import Map
from cursor import Cursor
from ui import MainMenu, BattleForcast, CombatUI, MapUnitUI, UnitInfo
from inventory import Inventory, Weapon, HealingItem, Javelin
from animation import Animation
from unit import Unit


pygame.init()
gameWidth = 1920
gameHeight = 1080
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Code FE")
running = True

#------ load assets --------
## Characters


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
class states(Enum):
    inMainMenu = auto()
    selectingTile = auto()
    selectingAction = auto()
    selectingAttack = auto()
    selectingItems = auto()
    selectingWeapon = auto()
    viewingUnitInfo = auto()
    attacking = auto()
    finishedAttacking = auto()
    addingExp = auto()
    levelingUp = auto()

currentState = states.inMainMenu

playerTurn = True
viewingUnitInfo = False
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

myBattleForcast = BattleForcast(gameWidth)
mainCursor = Cursor(tileSize, mapWidth, mapHeight, gameWidth, gameHeight)
myCombatUI = CombatUI(0, gameHeight - 385)
myUnitInfo = UnitInfo()
myMapUnitUI = MapUnitUI(gameWidth, gameHeight)
myExp = Exp()
myLevelUp = LevelUp()

## creating units
protag = Unit(3, 3, tileSize)
bow = Weapon("bow")
bow.range = [3,3]
protag.inventory.addItem(bow)

Jagen = Unit(3, 5, tileSize)
Jagen.exp = 90
Jagen.inventory.addItem(Weapon("Sword"))
Jagen.inventory.addItem(Javelin())
Jagen.inventory.addItem(HealingItem())
Jagen.name = 'Jagen'
Jagen.attack = 10
Jagen.defense = 10
Jagen.speed = 9
enemy = Unit(9, 5, tileSize)
enemy.inventory.addItem(Weapon())
enemy1 = Unit(9, 6, tileSize)
enemy1.inventory.addItem(Weapon())
enemy1.defense = 7

## setting up the map
def map1Win():
    return enemy.hp <= 0

map1 = Map(mapWidth, mapHeight, map1background, tileSize, map1Win)

# set unique tiles
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

currentMap = map1

# Setting up for game
currentMap.addUnitToMap(enemy)
currentMap.addUnitToMap(enemy1)
currentMap.addUnitToMap(protag)
currentMap.addUnitToMap(Jagen)

playerUnits.append(protag)
playerUnits.append(Jagen)

enemyUnits.append(enemy)
enemyUnits.append(enemy1)

activeEnemyUnits.append(enemy)
activeEnemyUnits.append(enemy1)




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
    currentMap.reset()
    currentTile = currentMap.tiles[unit.X][unit.Y]
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

def resetAfterAction():
    global currentUnit
    global selectingAttack
    global currentUnitTile 
    global currentUnitStartingTile 
    global defendingUnit
    global selectingItems
    currentUnitTile = None
    currentUnitStartingTile = None
    if currentUnit:
        currentUnit.active = False
    currentUnit = None
    defendingUnit = None
    selectingAttack = False
    selectingItems = False
    currentMap.reset()

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

def setTilesInRangeAttackable(atkRange, tilesInRange):
    global currentUnit
    for tile in tilesInRange:
        if tile.currentUnit == None or tile.currentUnit == currentUnit:
            tile.selectable = True
            for atkTile in findTilesInAttackRange(tile, atkRange):
                if atkTile not in tilesInRange:
                    atkTile.attackable = True


## compares the UI elements to the cursor location
## keeps the UI from covering up the map
def checkMapUI():
    if mainCursor.X * tileSize > gameWidth / 2:
        myMapUnitUI.X = 10
        myBattleForcast.X = 10
    else:
        myMapUnitUI.X = gameWidth - 460
        myBattleForcast.X = gameWidth - 500
    
    ## check if cursor is over a player
    cursorTileUnit = currentMap.tiles[mainCursor.X][mainCursor.Y].currentUnit
    myMapUnitUI.reset(cursorTileUnit)

## given an attacking and defending unit, blit both first frames to the screen (if they are alive)
def drawFirstFrames(currentUnit, defendingUnit):
    if currentUnit.hp > 0:
        screen.blit(currentUnit.getCombatAniFirstFrame(), (0, 0))
    if defendingUnit.hp > 0:
        screen.blit(pygame.transform.flip(defendingUnit.getCombatAniFirstFrame(), True, False), (0, 0))


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
                myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, currentMap)
                myBattleForcast.roll()
                attacking = True
                
            else:
                currentState = states.selectingAction
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
                currentUnitStartingTile = currentMap.tiles[currentUnit.X][currentUnit.Y]
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
        elif playerTurn and not (currentState in  [states.selectingAction, states.selectingAttack] or selectingWeapon or selectingItems or attacking):
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
        elif playerTurn and currentState == states.selectingAction:
            if keys[pygame.K_DOWN]:
                if (menuSelectionIndex < len(menuOptions)-1):
                    menuSelectionIndex+=1
            if keys[pygame.K_UP]:
                if (menuSelectionIndex > 0):
                    menuSelectionIndex-=1
        # end menu movement controls

        for event in pygame.event.get():
            ## quit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if currentState == states.inMainMenu: 
                if event.type == pygame.KEYDOWN:
                    currentState = None
            # player turn
            elif playerTurn:
                # picking a unit to attack
                if currentState == states.selectingAttack:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        attacking = True
                        currentState = None
                        myBattleForcast.roll()

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_UP):
                        if attackUnitIndex < len(unitsInRange) - 1:
                            attackUnitIndex += 1
                        else:
                            attackUnitIndex = 0
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, currentMap)

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_DOWN):
                        if attackUnitIndex > 0:
                            attackUnitIndex -= 1
                        else:
                            attackUnitIndex = len(unitsInRange)-1
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, currentMap)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentState = states.selectingAction

                elif selectingItems:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        selectingItems = False
                        currentState = states.selectingAction
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        currentUnit.inventory.up()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        currentUnit.inventory.down()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        if currentUnit.inventory.activateItem(currentUnit):
                            resetAfterAction()

                elif selectingWeapon:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        currentUnit.inventory.equipSelectedWeapon()
                        unitsInRange = []
                        currentMap.reset()
                        for tile in findTilesInAttackRange(currentUnitTile, currentUnit.inventory.avaliableItems[0].range):
                            if tile.currentUnit != None and tile.currentUnit in enemyUnits:
                                unitsInRange.append(tile.currentUnit)
                            tile.attackable = True

                        selectingWeapon = False
                        currentState = states.selectingAttack
                        attackUnitIndex = 0
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, currentMap)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        currentUnit.inventory.up()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        currentUnit.inventory.down()

                ### selecting action in menu
                elif currentState == states.selectingAction:
                    # action selected from menu
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        if menuOptions[menuSelectionIndex] == 'wait':
                            resetAfterAction()
                            
                            
                        if menuOptions[menuSelectionIndex] == 'attack':
                            currentState = None
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
                            currentState = None
                            currentUnit.inventory.avaliableItems = currentUnit.getInventory()
                    # go back to selecting tile
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentMap.reset()
                        currentUnitTile.currentUnit = None
                        currentUnit.X = currentUnitStartingTile.X
                        currentUnit.Y = currentUnitStartingTile.Y
                        currentUnitStartingTile.currentUnit = currentUnit
                        currentUnitTile = currentUnitStartingTile
                        # update state
                        currentState = states.selectingTile
                        tilesInRange = findTilesInMovRange(currentUnit)
                        for tile in tilesInRange:
                            if tile.currentUnit == None or tile.currentUnit == currentUnit:
                                tile.selectable = True
                                for atkTile in findTilesInAttackRange(tile, currentUnit.inventory.getBestRange()):
                                    if atkTile not in tilesInRange:
                                        atkTile.attackable = True

                ### selecting what tile to move to 
                elif currentState == states.selectingTile:
                    # Select tile and get ready to move to it
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        tileToMoveTo = currentMap.tiles[mainCursor.X][mainCursor.Y]
                        if tileToMoveTo.selectable:
                            targetTile = tileToMoveTo
                            moving = True
                            currentState = None
                            moveVelocity = getMoveVelocity(currentUnitTile, targetTile, moveSpeed)
                            currentMap.reset()

                    # Stop selecting tile
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentMap.reset()
                        currentUnit = None
                        currentUnitTile = None
                        currentUnitStartingTile = None
                        currentState = None

                elif viewingUnitInfo:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        viewingUnitInfo = False

                ### no unit selected, waiting for next unit to be selected
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        playerTurn = False
                        currentState = None
                    # Select unit and show their range
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        
                        # get the unit that cursor is on
                        currentTile = currentMap.tiles[mainCursor.X][mainCursor.Y]
                        currentUnit = currentTile.currentUnit
                        
                        # get tiles in range of that unit and highlight them
                        if currentUnit != None:
                            setTilesInRangeAttackable(currentUnit.inventory.getBestRange(), findTilesInMovRange(currentUnit))
                            if currentUnit.active and currentUnit in playerUnits:
                                currentState = states.selectingTile
                                currentUnitTile = currentTile
                                currentUnitStartingTile = currentTile
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentUnit = None
                        currentMap.reset()
                        currentState = None
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                        currentTile = currentMap.tiles[mainCursor.X][mainCursor.Y]
                        if currentTile.currentUnit != None:
                            currentUnit = currentTile.currentUnit
                            myUnitInfo.reset(currentUnit)
                            viewingUnitInfo = True
                        
    
    #### drawing ####
    if currentState == states.inMainMenu:
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
            screen.blit(pygame.transform.flip(defendingUnit.getCombatAniFirstFrame(), True, False), (0, 0))
            
            if myBattleForcast.attackingUnitWillHit:
                ## animations are called continously, 
                ## once the animation is complete, it returns true
                if currentUnit.combatAnimation.draw(screen, 0, 0, False):
                    ## remove health
                    defendingUnit.hp -= myBattleForcast.attackingUnitDmg
                    currentUnitAttacking = False
                    if currentUnit in playerUnits:
                        experience += myBattleForcast.attackingUnitDmg
            ## unit will miss, play miss animation
            else:
                if currentUnit.combatAnimation.draw(screen, 0, 0, False):
                    currentUnitAttacking = False
                    experience += 1
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)

        elif defendingUnitAttacking:
            if defendingUnit.hp > 0:
                screen.blit(currentUnit.getCombatAniFirstFrame(), (0, 0))
                if myBattleForcast.defendingUnitCanCounter:
                    if myBattleForcast.defendingUnitWillHit:
                        if defendingUnit.combatAnimation.draw(screen, 0, 0, True):
                            # remove health
                            currentUnit.hp -= myBattleForcast.defendingUnitDmg
                            defendingUnitAttacking = False
                            if defendingUnit in playerUnits:
                                experience += myBattleForcast.defendingUnitDmg
                            if currentUnit.hp <= 0:
                                if currentUnit in playerUnits:
                                    playerUnits.remove(currentUnit)
                                elif currentUnit in enemyUnits:
                                    enemyUnits.remove(currentUnit)
                                    experience += 30
                                currentMap.tiles[currentUnit.X][currentUnit.Y].currentUnit = None
                    ## unit will miss, play miss animation
                    else:
                        if defendingUnit.combatAnimation.draw(screen, 0, 0, True):
                            defendingUnitAttacking = False
                            experience += 1
                else:
                    screen.blit(pygame.transform.flip(defendingUnit.getCombatAniFirstFrame(), True, False), (0, 0))
                    defendingUnitAttacking = False
            else:
                # if here, defending unit has died,
                # remove from game
                defendingUnitAttacking = False

                ## remove unit from game
                if defendingUnit in playerUnits:
                    playerUnits.remove(defendingUnit)
                elif defendingUnit in enemyUnits:
                    enemyUnits.remove(defendingUnit)
                    activeEnemyUnits.remove(defendingUnit)
                    experience += 30
                currentMap.tiles[defendingUnit.X][defendingUnit.Y].currentUnit = None
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)

        elif finishedAttacking:
            drawFirstFrames(currentUnit, defendingUnit)
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)
            if experience > 0:
                addingExp = True
                if currentUnit in playerUnits:
                    myExp.setup(currentUnit, experience)
                elif defendingUnit in playerUnits:
                    myExp.setup(defendingUnit, experience)
            finishedAttacking = False

        elif levelingUp:
            drawFirstFrames(currentUnit, defendingUnit)
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)

            if myLevelUp.draw(screen):
                levelingUp = False
                myLevelUp.currUnit = None

        elif addingExp:
            drawFirstFrames(currentUnit, defendingUnit)
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, enemyUnits, playerUnits)

            if myExp.currUnit.exp >= 100:
                levelingUp = True
                myLevelUp.currUnit = myExp.currUnit
                myLevelUp.roll(myExp.currUnit)
                myExp.currUnit.exp = 0
                myExp.currUnit.level += 1

            elif myExp.draw(screen):
                addingExp = False
                checkMapUI()


        else:
            experience = 0
            currentUnitAttacking = True
            defendingUnitAttacking = True
            attacking = False
            currentState = None
            finishedAttacking = True
            resetAfterAction()

            if currentMap.checkForWin():
                print("Map is finished")
    
    
    
    else:
        screen.fill((0,0,0))
        currentMap.draw(screen, xCamera, yCamera)
        mainCursor.draw(screen)
        for unit in playerUnits:
            unit.draw(screen, tileSize, xCamera, yCamera)
        for enemy in enemyUnits:
            enemy.draw(screen, tileSize, xCamera, yCamera)
        
        myMapUnitUI.draw(screen, font)
        if currentState == states.selectingAttack:
            myBattleForcast.draw(screen, font, currentUnit, unitsInRange[attackUnitIndex])

        elif selectingItems:
            currentUnit.inventory.draw(screen, font)            
        elif selectingWeapon:
            currentUnit.inventory.draw(screen, font)

        elif currentState == states.selectingAction:
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
