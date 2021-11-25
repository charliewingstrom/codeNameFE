import pygame

from enum       import Enum, auto
from pathlib    import Path

## custom classes
from pathManager    import PathManager
from ui             import MainMenu, BattleForecast, MapUnitUI, UnitInfo
from exp            import Exp, LevelUp
from inventory      import HealingItem, Sword, Bow, Javelin
from unit           import Unit
from unitHolder     import UnitHolder
from combatManager  import CombatManager
from mapManager     import MapManager

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
#---------------------------

# globals
currentUnit = None
defendingUnit = None
## map
tileSize = 96
maxDistance = 256

## movement
moving = False

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

currentState = states.inMainMenu

playerTurn = True

# states while attacking
class atkStates(Enum):
    attacking           = auto()
    finishedAttacking   = auto()
    addingExp           = auto()
    levelingUp          = auto()


attackingState = atkStates.attacking

## menu items
menuOptions = []
menuOptions.append("wait")
menuSelectionIndex = 0



### attacking selection
unitsInRange = []
attackUnitIndex = 0

font = pygame.font.Font('freesansbold.ttf', 52)

## custom class instances
myMainMenu = MainMenu()

myUnitHolder = UnitHolder()

## creating units
protag = Unit(3, 3, tileSize, [Bow()], True)
protag.attack = 7
protag.defense = 6
protag.speed = 5
protag.skill = 7
protag.luck = 8

Jagen = Unit(3, 5, tileSize, [Sword(), Javelin(), HealingItem()], True)
Jagen.name = 'Jagen'
Jagen.attack = 15
Jagen.defense = 10
Jagen.speed = 9
Jagen.skill = 8
Jagen.luck = 8

myUnitHolder.addUnit(protag)
myUnitHolder.addUnit(Jagen)

myBattleForecast = BattleForecast(gameWidth)
myMapManager    = MapManager(tileSize, gameWidth, gameHeight, myUnitHolder)
myUnitInfo      = UnitInfo()
myMapUnitUI     = MapUnitUI(gameWidth, gameHeight)
myExp           = Exp()
myLevelUp       = LevelUp(gameWidth, gameHeight)
myPathManager   = PathManager()
myCombatManager = CombatManager(screen, gameWidth, gameHeight, font)

def findPlayerTarget(tiles, unit):
    possibleTargets = []
    for tile in tiles:
        for attackableTile in findTilesInAttackRange(tile, unit.getAttackRange()):
            if attackableTile.currentUnit != None and attackableTile.currentUnit.getIsPlayer():
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
    myMapManager.resetCurrentMap
    currentTile = myMapManager.getTileUnitIsOn(unit)
    currentTile.distance = 0
    queue = []
    added = []
    tilesInRange = []
    queue.append(currentTile)
    added.append(currentTile)
    while len(queue) > 0:
        queue.sort(key=lambda tile:tile.distance)
        currTile = queue.pop(0)
        if unit.getIsPlayer():
            if currTile.distance <= currentUnit.mov and currTile.walkable and (currTile.currentUnit == None or currTile.currentUnit.getIsPlayer()):
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
            if currTile.distance <= currentUnit.mov and currTile.walkable and (currTile.currentUnit == None or currTile.currentUnit in myUnitHolder.getEnemies()):
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
    myMapManager.resetCurrentMap()

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

# TODO
# def aimAtUnit(defendingUnit, unitsInRange, attackUnitIndex, myMapManager, myBattleForecast):
#     defendingUnit = unitsInRange[attackUnitIndex]
#     myMapManager.setCursorOnUnit(defendingUnit)
#     myBattleForecast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, myMapManager.getCurrentMap())

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

                if lastTile:
                    currentUnitTile = lastTile
                    currentUnitTile.currentUnit = currentUnit

                moving = False
                if not playerTurn:
                    myBattleForecast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, myMapManager.getCurrentMap())
                    myBattleForecast.roll()
                    currentState = states.attacking
                    myCombatManager.setupAttack(currentUnit, defendingUnit, myBattleForecast, False)
                    
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
                        if tile.currentUnit != None and tile.currentUnit in myUnitHolder.getEnemies():
                            unitsInRange.append(tile.currentUnit)
                    if len(unitsInRange) > 0:
                        menuOptions.insert(0, "attack")
    # not moving
    else: 
        ## automated enemy phase actions
        if not playerTurn and currentState != states.attacking:
            activeEnemyUnit = myUnitHolder.getActiveEnemyUnit()
            if activeEnemyUnit:
                currentUnit = activeEnemyUnit
                currentUnitStartingTile = myMapManager.getTileUnitIsOn(currentUnit)
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
                    
                myMapManager.resetCurrentMap()
                
            else:
                playerTurn = True
                currentUnit = None
                myUnitHolder.resetForNextTurn()
        
        ## menu and cursor controls 
        ## if keys (they are up here because you should be able to hold the key)
        elif playerTurn and not (currentState in  [states.selectingAction, states.selectingAttack, states.selectingItems, states.selectingWeapon, states.attacking]):
            # cursor controls
            # get the arrow keys pressed 
            arrowKeys = [keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_LEFT]]
            myMapManager.checkUI(arrowKeys, myMapUnitUI, myBattleForecast, myPathManager)
            
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
                        myBattleForecast.roll()
                        myCombatManager.setupAttack(currentUnit, defendingUnit, myBattleForecast, True)

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_UP):
                        if attackUnitIndex < len(unitsInRange) - 1:
                            attackUnitIndex += 1
                        else:
                            attackUnitIndex = 0
                        defendingUnit = unitsInRange[attackUnitIndex]
                        myMapManager.setCursorOnUnit(defendingUnit)
                        myBattleForecast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, myMapManager.getCurrentMap())

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_DOWN):
                        if attackUnitIndex > 0:
                            attackUnitIndex -= 1
                        else:
                            attackUnitIndex = len(unitsInRange)-1
                        defendingUnit = unitsInRange[attackUnitIndex]
                        myMapManager.setCursorOnUnit(defendingUnit)
                        myBattleForecast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, myMapManager.getCurrentMap())

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
                        myMapManager.resetCurrentMap()
                        for tile in findTilesInAttackRange(currentUnitTile, currentUnit.inventory.avaliableItems[0].range):
                            if tile.currentUnit != None and tile.currentUnit in myUnitHolder.getEnemies():
                                unitsInRange.append(tile.currentUnit)
                            tile.attackable = True
                        currentState = states.selectingAttack
                        attackUnitIndex = 0
                        defendingUnit = unitsInRange[attackUnitIndex]
                        myMapManager.setCursorOnUnit(defendingUnit)
                        myBattleForecast.calculate(currentUnit, defendingUnit, findTilesInAttackRange, myMapManager.getCurrentMap())

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
                                    if tile.currentUnit != None and tile.currentUnit in myUnitHolder.getEnemies():
                                        currentUnit.inventory.avaliableItems.append(weapon)
                                        break

                        if menuOptions[menuSelectionIndex] == 'items':                            
                            currentState = states.selectingItems
                            currentUnit.inventory.avaliableItems = currentUnit.getInventory()
                    # go back to selecting tile
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        myMapManager.resetCurrentMap()
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
                        cursorTile = myMapManager.getTileCursorIsOn()
                        myPathManager.resetPath(cursorTile)
                        

                ### selecting what tile to move to 
                elif currentState == states.selectingTile:
                    # Select tile and get ready to move to it
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        if myMapManager.getTileCursorIsOn().selectable:
                            moving = True
                            currentState = states.selectingUnit
                            myPathManager.followPath()
                            myMapManager.resetCurrentMap()

                    # Stop selecting tile
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        # clear path
                        myPathManager.emptyPath()
                        myMapManager.resetCurrentMap()
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
                        currentTile = myMapManager.getTileCursorIsOn()
                        currentUnit = currentTile.currentUnit
                        
                        # get tiles in range of that unit and highlight them
                        if currentUnit != None:
                            setTilesInRangeAttackable(currentUnit.inventory.getBestRange(), findTilesInMovRange(currentUnit))
                            if currentUnit.active and currentUnit.getIsPlayer():
                                currentState = states.selectingTile
                                currentUnitTile = currentTile
                                currentUnitStartingTile = currentTile
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentUnit = None
                        myMapManager.resetCurrentMap()
                        myPathManager.emptyPath()
                        currentState = states.selectingUnit
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                        currentTile = myMapManager.getTileCursorIsOn()
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
        
        if attackingState == atkStates.levelingUp:
            if myLevelUp.draw(screen, font):
                attackingState = atkStates.addingExp
                myLevelUp.currUnit = None 
                
        elif attackingState == atkStates.addingExp:
            if myExp.currUnit.exp >= 100:
                attackingState = atkStates.levelingUp
                myLevelUp.currUnit = myExp.currUnit
                myLevelUp.roll(myExp.currUnit)
                myExp.currUnit.exp = 0
                myExp.currUnit.level += 1

            elif myExp.draw(screen, gameWidth):
                attackingState = atkStates.finishedAttacking 

        elif myCombatManager.runSequence():
            if currentUnit.hp <= 0:
                myUnitHolder.removeUnit(currentUnit)
                myMapManager.getTileUnitIsOn(currentUnit).currentUnit = None
            if defendingUnit.hp <= 0:
                myUnitHolder.removeUnit(defendingUnit)
                myMapManager.getTileUnitIsOn(defendingUnit).currentUnit = None
                
            if myCombatManager.getExp() > 0:
                attackingState = atkStates.addingExp
                if currentUnit.hp > 0 and currentUnit.getIsPlayer():
                    myExp.setup(currentUnit, myCombatManager.getExp())

                elif defendingUnit.hp > 0 and defendingUnit.getIsPlayer():
                    myExp.setup(defendingUnit, myCombatManager.getExp())

                else:
                    attackingState = atkStates.finishedAttacking
                    
            else:
                attackingState = atkStates.finishedAttacking

        if attackingState == atkStates.finishedAttacking:
            attackingState = atkStates.attacking
            # break out of attacking
            currentState = states.selectingUnit
            resetAfterAction()

            ## check if we have to transition to the next map
            mapComplete, noMoreMaps = myMapManager.checkForMapCompletion()
            if mapComplete and not noMoreMaps:
                playerTurn = True
                myUnitHolder.moveToNextMap(myMapManager.getCurrentMap())
            if noMoreMaps:
                running = False

    else:
        screen.fill((0,0,0))
        myMapManager.draw(screen)
        
        myUnitHolder.drawUnits(screen, tileSize, myMapManager.getCameraX(), myMapManager.getCameraY())

        myMapUnitUI.draw(screen, font)
        if currentState == states.selectingAttack:
            myBattleForecast.draw(screen, font, currentUnit, unitsInRange[attackUnitIndex])

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