import pygame
from enum import Enum, auto
from pathlib import Path

## custom classes
from pathManager import PathManager
from tileMap import Map
from cursor import Cursor
from ui import MainMenu, BattleForcast, CombatUI, MapUnitUI, UnitInfo
from exp import Exp, LevelUp
from inventory import HealingItem, Sword, Bow, Javelin
from unit import Unit
from combatManager import CombatManager

pygame.init()
gameWidth = 1920
gameHeight = 1080
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Code FE")
running = True

#------ load assets --------
## Menu
waitButton = pygame.image.load(Path(__file__).parent / "../assets/wait-button.png")
itemsButton = pygame.image.load(Path(__file__).parent / "../assets/items-button.png")
attackButton = pygame.image.load(Path(__file__).parent / "../assets/attack-button.png")
menuCursor = pygame.image.load(Path(__file__).parent / "../assets/menu-cursor.png")

## backgrounds
attacingBackground = pygame.image.load(Path(__file__).parent / "../assets/attacking-background.png")
map1background = pygame.image.load(Path(__file__).parent / "../assets/level1Background.png")
map2background = pygame.image.load(Path(__file__).parent / "../assets/map2-background.png")
#---------------------------

# globals
currentUnit = None
defendingUnit = None
## map
tileSize = 96
mapWidth = 32
mapHeight = 19
maxDistance = 256
maps = []

## camera
yCamera = 0
xCamera = 0

## movement
moving = False

## combat
experience = 0

## player state
class states(Enum):
    inMainMenu = auto()
    selectingUnit = auto()
    selectingTile = auto()
    selectingAction = auto()
    selectingAttack = auto()
    selectingItems = auto()
    selectingWeapon = auto()
    attacking = auto()
    viewingUnitInfo = auto()
    
    finishedAttacking = auto()
    addingExp = auto()
    levelingUp = auto()

currentState = states.inMainMenu

playerTurn = True

## this might be tricky to add to states because it defaults to True
## there will be multiple exits for attacking to finishedAttacking
finishedAttacking = True
addingExp = False
levelingUp = False

# states while attacking

class atkStates(Enum):
    currentUnitAttacking = auto()
    defendingUnitAttacking = auto()

    currentUnitDoubling = auto()
    defendingUnitDoubling = auto()

    finishedAttacking = auto()
    addingExp = auto()
    levelingUp = auto()

attackingState = atkStates.currentUnitAttacking

## menu items
menuOptions = []
menuOptions.append("wait")
menuSelectionIndex = 0

## unit arrays
playerUnits = []
activeEnemyUnits = []

### attacking selection
unitsInRange = []
attackUnitIndex = 0

font = pygame.font.Font('freesansbold.ttf', 52)

## custom class instances
myMainMenu = MainMenu()
myBattleForcast = BattleForcast(gameWidth)
mainCursor = Cursor(tileSize, mapWidth, mapHeight, gameWidth, gameHeight)
myCombatUI = CombatUI(0, gameHeight - 385)
myUnitInfo = UnitInfo()
myMapUnitUI = MapUnitUI(gameWidth, gameHeight)
myExp = Exp()
myLevelUp = LevelUp(gameWidth, gameHeight)

myPathManager = PathManager()
myCombatManager = CombatManager(screen)

## creating units
protag = Unit(3, 3, tileSize)
protag.inventory.addItem(Bow())
protag.attack = 7
protag.defense = 6
protag.speed = 5
protag.skill = 7
protag.luck = 8

Jagen = Unit(3, 5, tileSize)
Jagen.inventory.addItem(Sword())
Jagen.inventory.addItem(Javelin())
Jagen.inventory.addItem(HealingItem())
Jagen.name = 'Jagen'
Jagen.attack = 3
Jagen.defense = 10
Jagen.speed = 9
Jagen.skill = 8
Jagen.luck = 8

enemy = Unit(9, 5, tileSize)
enemy.inventory.addItem(Sword())
enemy1 = Unit(9, 6, tileSize)
enemy1.inventory.addItem(Sword())

## setting up the map
def map1Win():
    return enemy.hp <= 0

map1 = Map(mapWidth, mapHeight, map1background, tileSize, map1Win, [enemy, enemy1])

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

# map2

enemy3 = Unit(1, 2, tileSize)
enemy3.inventory.addItem(Sword())
enemy4 = Unit(2, 1, tileSize)
enemy4.inventory.addItem(Sword())

def map2Win():
    return enemy4.hp <= 0

map2 = Map(12, 12, map2background, tileSize, map2Win, [enemy3, enemy4])

maps.append(map2)

currentMap = map1

# Setting up for game
currentMap.addUnitToMap(protag)
currentMap.addUnitToMap(Jagen)

playerUnits.append(protag)
playerUnits.append(Jagen)

activeEnemyUnits.append(enemy)
activeEnemyUnits.append(enemy1)

def findPlayerTarget(tiles, unit):
    possibleTargets = []
    for tile in tiles:
        for attackableTile in findTilesInAttackRange(tile, unit.getAttackRange()):
            if attackableTile.currentUnit != None and attackableTile.currentUnit in playerUnits:
                possibleTargets.append((attackableTile.currentUnit, tile))
    
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
            if currTile.distance <= currentUnit.mov and currTile.walkable and (currTile.currentUnit == None or currTile.currentUnit in currentMap.enemyUnits):
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

def resetAfterAction():
    global currentUnit
    global currentUnitTile 
    global currentUnitStartingTile 
    global defendingUnit
    global currentState
    
    currentUnitTile = None
    currentUnitStartingTile = None
    if currentUnit:
        currentUnit.active = False
    currentUnit = None
    defendingUnit = None
    currentState = states.selectingUnit
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

def getTileCursorIsOn(tileMap, cursor):
    return tileMap.tiles[cursor.X][cursor.Y]

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
    cursorTileUnit = getTileCursorIsOn(currentMap, mainCursor).currentUnit
    myMapUnitUI.reset(cursorTileUnit)

## given an attacking and defending unit, blit both first frames to the screen (if they are alive)
def drawFirstFrames(currentUnit, defendingUnit):
    if currentUnit.hp > 0:
        screen.blit(currentUnit.getCombatAniFirstFrame(), (0, 0))
    if defendingUnit.hp > 0:
        screen.blit(pygame.transform.flip(defendingUnit.getCombatAniFirstFrame(), True, False), (0, 0))


# main game loop
while running:
    keys = pygame.key.get_pressed()
    
    # if something is moving there shouldn't be any other input accepted
    if moving:
        
        if myPathManager.moveUnitByVelocity(currentUnit):
            stillMoving, lastTile = myPathManager.followPath()
            if not stillMoving:

                ## finish moving
                currentUnitStartingTile.currentUnit = None
                currentUnitTile = lastTile
                currentUnitTile.currentUnit = currentUnit

                moving = False
                if not playerTurn:
                    myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, currentMap)
                    myBattleForcast.roll()
                    currentState = states.attacking
                    myCombatManager.setupAttack(currentUnit, defendingUnit, myBattleForcast, False)
                    
                else:
                    currentState = states.selectingAction
                    menuOptions = []
                    menuSelectionIndex = 0
                    menuOptions.insert(0, "wait")
                    if len(currentUnit.getInventory()) > 0:
                        menuOptions.insert(0, "items")
                    unitsInRange = []
                    for tile in findTilesInAttackRange(currentUnitTile, currentUnit.inventory.getBestRange()):
                        tile.attackable = True
                        if tile.currentUnit != None and tile.currentUnit in currentMap.enemyUnits:
                            unitsInRange.append(tile.currentUnit)
                    if len(unitsInRange) > 0:
                        menuOptions.insert(0, "attack")
    # not moving
    else: 
        ## automated enemy phase actions
        if not playerTurn and currentState != states.attacking:
            if len(activeEnemyUnits) > 0:
                currentUnit = activeEnemyUnits.pop(0)
                currentUnitStartingTile = currentMap.tiles[currentUnit.X][currentUnit.Y]
                enemyTilesInRange = findTilesInMovRange(currentUnit)
                for tile in enemyTilesInRange:
                    if tile.currentUnit == None or tile.currentUnit == currentUnit:
                        tile.selectable = True
                defendingUnit, targetTile = findPlayerTarget(enemyTilesInRange, currentUnit)

                ## for now if a unit is not in range, don't move
                if defendingUnit != None:
                    myPathManager.resetPath(targetTile)
                    myPathManager.followPath()
                    moving = True
                    
                currentMap.reset()
                
            else:
                playerTurn = True
                currentUnit = None
                for unit in playerUnits:
                    unit.active = True
                for unit in currentMap.enemyUnits:
                    activeEnemyUnits.append(unit)
        

        ## menu and cursor controls 
        ## if keys (they are up here because you should be able to hold the key)
        elif playerTurn and not (currentState in  [states.selectingAction, states.selectingAttack, states.selectingItems, states.selectingWeapon, states.attacking]):
            # cursor controls
            arrowKeyPressed = False
            if keys[pygame.K_DOWN]:
                yCamera += mainCursor.down(yCamera)
                checkMapUI()
                arrowKeyPressed = True
            if keys[pygame.K_UP]:
                yCamera += mainCursor.up(yCamera)
                checkMapUI()
                arrowKeyPressed = True
            if keys[pygame.K_RIGHT]:
                xCamera += mainCursor.right(xCamera)
                checkMapUI()
                arrowKeyPressed = True
            if keys[pygame.K_LEFT]:
                xCamera += mainCursor.left(xCamera)
                checkMapUI()
                arrowKeyPressed = True
            if arrowKeyPressed:
                cursorTile = getTileCursorIsOn(currentMap, mainCursor)
                myPathManager.resetPath(cursorTile)

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
                    currentState = states.selectingUnit
            # player turn
            elif playerTurn:
                # picking a unit to attack
                if currentState == states.selectingAttack:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        currentState = states.attacking
                        myBattleForcast.roll()
                        myCombatManager.setupAttack(currentUnit, defendingUnit, myBattleForcast, True)

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
                        currentState = states.selectingWeapon

                elif currentState == states.selectingItems:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentState = states.selectingAction
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        currentUnit.inventory.up()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        currentUnit.inventory.down()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        if currentUnit.inventory.activateItem(currentUnit):
                            resetAfterAction()

                elif currentState == states.selectingWeapon:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        currentUnit.inventory.equipSelectedWeapon()
                        unitsInRange = []
                        currentMap.reset()
                        for tile in findTilesInAttackRange(currentUnitTile, currentUnit.inventory.avaliableItems[0].range):
                            if tile.currentUnit != None and tile.currentUnit in currentMap.enemyUnits:
                                unitsInRange.append(tile.currentUnit)
                            tile.attackable = True
                        currentState = states.selectingAttack
                        attackUnitIndex = 0
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, currentMap)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentState = states.selectingAction

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
                            currentState = states.selectingWeapon
                            
                            currentUnit.inventory.selectionIndex = 0
                            currentUnit.inventory.avaliableItems = []
                            for weapon in currentUnit.inventory.weapons:
                                for tile in findTilesInAttackRange(currentUnitTile, weapon.range):
                                    if tile.currentUnit != None and tile.currentUnit in currentMap.enemyUnits:
                                        currentUnit.inventory.avaliableItems.append(weapon)
                                        break

                        if menuOptions[menuSelectionIndex] == 'items':                            
                            currentState = states.selectingItems
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
                        cursorTile = getTileCursorIsOn(currentMap, mainCursor)
                        myPathManager.resetPath(cursorTile)
                        

                ### selecting what tile to move to 
                elif currentState == states.selectingTile:
                    # Select tile and get ready to move to it
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        if getTileCursorIsOn(currentMap, mainCursor).selectable:
                            moving = True
                            currentState = states.selectingUnit
                            myPathManager.followPath()
                            currentMap.reset()

                    # Stop selecting tile
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        # clear path
                        myPathManager.emptyPath()
                        currentMap.reset()
                        currentUnit = None
                        currentUnitTile = None
                        currentUnitStartingTile = None
                        currentState = states.selectingUnit
                        
                        

                elif currentState == states.viewingUnitInfo:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentState = states.selectingUnit

                ### no unit selected, waiting for next unit to be selected
                elif currentState == states.selectingUnit:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        playerTurn = False
                        
                    # Select unit and show their range
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        
                        # get the unit that cursor is on
                        currentTile = getTileCursorIsOn(currentMap, mainCursor)
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
                        myPathManager.emptyPath()
                        currentState = states.selectingUnit
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                        currentTile = getTileCursorIsOn(currentMap, mainCursor)
                        if currentTile.currentUnit != None:
                            currentUnit = currentTile.currentUnit
                            myUnitInfo.reset(currentUnit)
                            currentState = states.viewingUnitInfo
    
    #### drawing ####
    if currentState == states.inMainMenu:
        myMainMenu.draw(screen)
    
    ## attacking ####
    elif currentState == states.attacking:
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

        if attackingState == atkStates.currentUnitAttacking:
            screen.blit(pygame.transform.flip(defendingUnit.getCombatAniFirstFrame(), True, False), (0, 0))
            
            if myBattleForcast.attackingUnitWillHit:
                ## animations are called continously, 
                ## once the animation is complete, it returns true
                if currentUnit.combatAnimation.draw(screen, 0, 0, False):
                    ## remove health
                    defendingUnit.hp -= myBattleForcast.attackingUnitDmg
                    attackingState = atkStates.defendingUnitAttacking
                    if currentUnit in playerUnits:
                        experience += myBattleForcast.attackingUnitDmg
            ## unit will miss, play miss animation
            else:
                if currentUnit.combatAnimation.draw(screen, 0, 0, False):
                    attackingState = atkStates.defendingUnitAttacking
                    experience += 1
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, currentMap.enemyUnits, playerUnits)

        elif attackingState == atkStates.defendingUnitAttacking:
            if defendingUnit.hp > 0:
                screen.blit(currentUnit.getCombatAniFirstFrame(), (0, 0))
                if myBattleForcast.defendingUnitCanCounter:
                    if myBattleForcast.defendingUnitWillHit:
                        if defendingUnit.combatAnimation.draw(screen, 0, 0, True):
                            # remove health
                            currentUnit.hp -= myBattleForcast.defendingUnitDmg
                            attackingState = atkStates.finishedAttacking
                            if defendingUnit in playerUnits:
                                experience += myBattleForcast.defendingUnitDmg
                            if currentUnit.hp <= 0:
                                if currentUnit in playerUnits:
                                    playerUnits.remove(currentUnit)
                                elif currentUnit in currentMap.enemyUnits:
                                    currentMap.enemyUnits.remove(currentUnit)
                                    experience += 30
                                currentMap.tiles[currentUnit.X][currentUnit.Y].currentUnit = None
                    ## unit will miss, play miss animation
                    else:
                        if defendingUnit.combatAnimation.draw(screen, 0, 0, True):
                            attackingState = atkStates.finishedAttacking
                            experience += 1
                else:
                    screen.blit(pygame.transform.flip(defendingUnit.getCombatAniFirstFrame(), True, False), (0, 0))
                    attackingState = atkStates.finishedAttacking
            else:
                # if here, defending unit has died,
                # remove from game
                attackingState = atkStates.finishedAttacking

                ## remove unit from game
                if defendingUnit in playerUnits:
                    playerUnits.remove(defendingUnit)
                elif defendingUnit in currentMap.enemyUnits:
                    currentMap.enemyUnits.remove(defendingUnit)
                    activeEnemyUnits.remove(defendingUnit)
                    experience += 30
                currentMap.tiles[defendingUnit.X][defendingUnit.Y].currentUnit = None
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, currentMap.enemyUnits, playerUnits)

        elif attackingState == atkStates.finishedAttacking:
            drawFirstFrames(currentUnit, defendingUnit)
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, currentMap.enemyUnits, playerUnits)
            if experience > 0:
                attackingState = atkStates.addingExp
                if currentUnit in playerUnits:
                    myExp.setup(currentUnit, experience)
                elif defendingUnit in playerUnits:
                    myExp.setup(defendingUnit, experience)
            else:
                attackingState = None

        elif attackingState == atkStates.levelingUp:
            drawFirstFrames(currentUnit, defendingUnit)
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, currentMap.enemyUnits, playerUnits)

            if myLevelUp.draw(screen, font):
                attackingState = atkStates.addingExp
                myLevelUp.currUnit = None

        elif attackingState == atkStates.addingExp:
            drawFirstFrames(currentUnit, defendingUnit)
            myCombatUI.draw(screen, myBattleForcast, font, currentUnit, defendingUnit, currentMap.enemyUnits, playerUnits)

            if myExp.currUnit.exp >= 100:
                attackingState = atkStates.levelingUp
                myLevelUp.currUnit = myExp.currUnit
                myLevelUp.roll(myExp.currUnit)
                myExp.currUnit.exp = 0
                myExp.currUnit.level += 1

            elif myExp.draw(screen, gameWidth):
                attackingState = None
                checkMapUI()


        else:
            # reset for next time
            attackingState = atkStates.currentUnitAttacking
            # break out of attacking
            currentState = states.selectingUnit
            experience = 0
            resetAfterAction()

            ## check if we have to transition to the next map
            if currentMap.checkForWin():
                if len(maps) == 0:
                    running = False
                else:
                    currentMap = maps.pop(0)
                    playerTurn = True
                    # setup players
                    for i in range(len(playerUnits)):
                        tmpPlayerUnit = playerUnits[i]
                        tmpPlayerUnit.X = 0
                        tmpPlayerUnit.Y = i
                        currentMap.addUnitToMap(tmpPlayerUnit)
                        tmpPlayerUnit.active = True

                    # setup enemies
                    activeEnemyUnits = []
                    for unit in currentMap.enemyUnits:
                        activeEnemyUnits.append(unit)
                
    
    else:
        screen.fill((0,0,0))
        currentMap.draw(screen, xCamera, yCamera)
        mainCursor.draw(screen)
        for unit in playerUnits:
            unit.draw(screen, tileSize, xCamera, yCamera)
        for enemy in currentMap.enemyUnits:
            enemy.draw(screen, tileSize, xCamera, yCamera)
        
        myMapUnitUI.draw(screen, font)
        if currentState == states.selectingAttack:
            myBattleForcast.draw(screen, font, currentUnit, unitsInRange[attackUnitIndex])

        elif currentState == states.selectingItems:
            currentUnit.inventory.draw(screen, font)            
        elif currentState == states.selectingWeapon:
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
        
        elif currentState == states.viewingUnitInfo:
            myUnitInfo.draw(screen, font)
                
    pygame.display.update()
    pygame.time.delay(60)