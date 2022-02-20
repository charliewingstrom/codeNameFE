import pygame

from enum       import Enum, auto

## custom classes
from pathManager        import PathManager
from ui                 import MainMenu, BattleForecast, MapUnitUI, UnitInfo
from menu               import Menu, menuOptions
from exp                import Exp, LevelUp
from inventory          import HealingItem, Sword, Bow, Javelin
from unit               import Unit, Stat
from unitHolder         import UnitHolder
from combatManager      import CombatManager
from mapManager         import MapManager
from selectingUnit      import SelectingUnit
from assetLoader        import AssetLoader

pygame.init()
pygame.display.set_caption("Code FE")

## player state
class states(Enum):
    inMainMenu      = auto()
    selectingUnit   = auto()
    selectingTile   = auto()
    selectingAction = auto()
    selectingAttack = auto()
    selectingItems  = auto()
    selectingTrade  = auto()
    selectingWeapon = auto()
    attacking       = auto()
    trading         = auto()
    viewingUnitInfo = auto()

# states while attacking
class atkStates(Enum):
    attacking           = auto()
    finishedAttacking   = auto()
    addingExp           = auto()
    levelingUp          = auto()

font = pygame.font.Font('freesansbold.ttf', 52)

class Game(object):
    def __init__(self):
        self.__gameWidth    = 1920
        self.__gameHeight   = 1080
        # for debugging purposes, will need to change this when it comes to general use
        self.__screen       = pygame.display.set_mode((self.__gameWidth, self.__gameHeight), pygame.FULLSCREEN, 0, 1)
        self.__assetLoader  = AssetLoader()
        self.__assetLoader.loadAssets()
        
        self.__attackingBackground = self.__assetLoader.assets["attacking-background.png"]

        self.__currentState = states.inMainMenu

        self.__playerTurn               = True
        self.__running                  = True
        self.__currentUnit              = None
        self.__defendingUnit            = None
        self.__currentUnitTile          = None
        self.__currentUnitStartingTile  = None

        ## map
        self.__tileSize = 96

        ## movement
        self.__moving = False
        self.__attackingState = atkStates.attacking

        ## custom class instances
        self.__mainMenu = MainMenu()

        self.__unitHolder = UnitHolder()

        ## creating units
        protag = Unit(3, 3, self.__tileSize, [Bow()], True)
        protag.setStat(Stat.STR, 4)
        protag.setStat(Stat.DEF, 3)
        protag.setStat(Stat.SPD, 5)
        protag.setStat(Stat.SKL, 7)
        protag.setStat(Stat.LCK, 7)

        Jagen = Unit(3, 5, self.__tileSize, [Sword(), Javelin(), HealingItem()], True)
        Jagen.name = 'Jagen'
        Jagen.setStat(Stat.STR, 9)
        Jagen.setStat(Stat.DEF, 6)
        Jagen.setStat(Stat.SPD, 6)
        Jagen.setStat(Stat.SKL, 8)
        Jagen.setStat(Stat.LCK, 8)

        self.__unitHolder.addUnit(protag)
        self.__unitHolder.addUnit(Jagen)

        self.__battleForecast = BattleForecast(self.__gameWidth)
        self.__mapManager    = MapManager(self.__tileSize, self.__gameWidth, self.__gameHeight, self.__unitHolder)
        self.__unitInfo      = UnitInfo()
        self.__mapUnitUI     = MapUnitUI(self.__gameWidth, self.__gameHeight)
        self.__exp           = Exp()
        self.__levelUp       = LevelUp(self.__gameWidth, self.__gameHeight)
        self.__pathManager   = PathManager()
        self.__combatManager = CombatManager(self.__screen, self.__gameWidth, self.__gameHeight, font)
        self.__actionMenu      = Menu()
        self.__selectingAttack = SelectingUnit()
        self.__selectingTrade  = SelectingUnit()
        

    def findPlayerTarget(self, tiles, unit):
        # TODO how to find a player target that is not within the enemy's movement + attack range
        possibleTargets = []
        for tile in tiles:
            for attackableTile in self.findTilesInAttackRange(tile, unit.getAttackRange()):
                if attackableTile.currentUnit != None and attackableTile.currentUnit.getIsPlayer():
                    possibleTargets.append((attackableTile.currentUnit, tile))
        
        bestTarget = (None, None)
        for target in possibleTargets:
            if target[0].getStat(Stat.HP) < (unit.getStat(Stat.STR) + unit.getEquippedWeapon().might) - target[0].getStat(Stat.DEF):
                return target
            elif bestTarget == (None, None):
                bestTarget = target
            elif bestTarget[0].getStat(Stat.DEF) > target[0].getStat(Stat.DEF):
                bestTarget = target
            
        return bestTarget        

    # find a path to the nearest player unit
    # only include tiles up to the mov value of the unit
    def findNearestPlayerPath(self, unit):
        self.__mapManager.resetCurrentMap()
        currTile = self.__mapManager.getTileUnitIsOn(unit)
        currTile.distance = 0
        queue   = []
        visited = []
        queue.append(currTile)
        visited.append(currTile)
        while len(queue) > 0:
            # get the tile with the smallest distance
            queue.sort(key=lambda tile:tile.distance)
            currTile = queue.pop(0)
            if currTile.currentUnit != None and currTile.currentUnit.getIsPlayer():
                ## currTile contains a player, meaning currTile.parent is the tile we want to move towards...
                break

            if currTile.walkable:
                visited.append(currTile)
                for tile in currTile.getAdjList():
                    if tile not in visited:
                        altDist = currTile.distance + 1
                        if tile.distance > altDist:
                            tile.distance = altDist
                            tile.parent = currTile
                        queue.append(tile)

        path = []
        while currTile != None:
            path.append(currTile)
            currTile = currTile.parent
            
        return path[-(unit.getStat(Stat.MOV)+1):]


    def findTilesInMovRange(self, unit):
        self.__mapManager.resetCurrentMap()
        currentTile = self.__mapManager.getTileUnitIsOn(unit)
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
                if currTile.distance <= self.__currentUnit.getStat(Stat.MOV) and currTile.walkable and (currTile.currentUnit == None or currTile.currentUnit.getIsPlayer()):
                    tilesInRange.append(currTile)
                    added.append(currTile)
                    for tile in currTile.getAdjList():
                        if tile not in added:
                            altDist = currTile.distance + 1
                            if tile.distance > altDist:
                                tile.distance = altDist
                                tile.parent = currTile
                            queue.append(tile)
            else:
                if currTile.distance <= self.__currentUnit.getStat(Stat.MOV) and currTile.walkable and (currTile.currentUnit == None or currTile.currentUnit in self.__unitHolder.getEnemies()):
                    tilesInRange.append(currTile)
                    added.append(currTile)
                    for tile in currTile.getAdjList():
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

    def resetAfterAction(self):
        self.__currentUnitTile = None
        self.__currentUnitStartingTile = None
        if self.__currentUnit:
            self.__currentUnit.active = False
        self.__currentUnit = None
        self.__defendingUnit = None
        self.__currentState = states.selectingUnit
        self.__mapManager.resetCurrentMap()

    # for finding all tiles in attack range from a given tile 
    # i.e, after/without moving
    def findTilesInAttackRange(self, startTile, atkRange):
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
                for tile in currTile.getAdjList():
                    if tile not in visited:
                        visited.append(tile)
                        queue.append(tile)
                        dist[tile] = dist[currTile] + 1
        return inRange

    # for showing all tiles that a unit could attack before they move
    def setTilesInRangeAttackable(self, atkRange, tilesInRange):
        for tile in tilesInRange:
            if tile.currentUnit == None or tile.currentUnit == self.__currentUnit:
                tile.selectable = True
                for atkTile in self.findTilesInAttackRange(tile, atkRange):
                    if atkTile not in tilesInRange:
                        atkTile.attackable = True

    def canDefendingUnitCounter(self, currentUnit, defendingUnit):
        toReturn = False
        for tile in self.findTilesInAttackRange(self.__mapManager.getTileUnitIsOn(defendingUnit), defendingUnit.getAttackRange()):
            if tile.currentUnit == currentUnit:
                toReturn = True
                break
        return toReturn

    def run(self):
        # main game loop
        while self.__running:
            keys = pygame.key.get_pressed()
            
            # if something is moving there shouldn't be any other input accepted
            if self.__moving:
                
                if self.__pathManager.moveUnitByVelocity(self.__currentUnit):
                    stillMoving, lastTile = self.__pathManager.followPath()
                    if not stillMoving:

                        ## finish moving
                        self.__currentUnitStartingTile.currentUnit = None

                        if lastTile:
                            self.__currentUnitTile = lastTile
                            self.__currentUnitTile.currentUnit = self.__currentUnit

                        self.__moving = False
                        self.__pathManager.emptyPath()
                        if not self.__playerTurn:
                            if self.__defendingUnit:
                                self.__battleForecast.calculate(self.__currentUnit, self.__defendingUnit, self.canDefendingUnitCounter(self.__currentUnit, self.__defendingUnit))
                                self.__battleForecast.roll()
                                self.__currentState = states.attacking
                                self.__combatManager.setupAttack(self.__currentUnit, self.__defendingUnit, self.__battleForecast, False)
                            else:
                                self.__currentState = states.selectingUnit     
                        else:
                            self.__currentState = states.selectingAction
                            #;)
                            tilesInAttackRange = self.findTilesInAttackRange(self.__mapManager.getTileUnitIsOn(self.__currentUnit), self.__currentUnit.inventory.getBestRange())
                            for tile in tilesInAttackRange: tile.attackable = True
                            self.__selectingAttack.getUnitsInRange(tilesInAttackRange, self.__unitHolder.getEnemies())
                            self.__selectingTrade.getUnitsInRange(self.__mapManager.getTileUnitIsOn(self.__currentUnit).getAdjList(), self.__unitHolder.getPlayers())
                            self.__actionMenu.checkForMenuOptions(self.__currentUnit, self.__selectingAttack.areUnitsInRange(), self.__selectingTrade.areUnitsInRange())

            # not moving
            else: 
                ## automated enemy phase actions
                if not self.__playerTurn and self.__currentState != states.attacking:
                    activeEnemyUnit = self.__unitHolder.getActiveEnemyUnit()
                    if activeEnemyUnit:
                        self.__currentUnit = activeEnemyUnit
                        self.__currentUnitStartingTile = self.__mapManager.getTileUnitIsOn(self.__currentUnit)
                        enemyTilesInRange = self.findTilesInMovRange(self.__currentUnit)
                        for tile in enemyTilesInRange:
                            if tile.currentUnit == None or tile.currentUnit == self.__currentUnit:
                                tile.selectable = True

                        ## Target Tile is target to move to,
                        ## defendingUnit is unit to attack
                        ## only make defendingUnit != None if they can be attacked
                        ## but we need to change this ... need to search the whole board if we don't find something here in order to find a path
                        self.__defendingUnit, targetTile = self.findPlayerTarget(enemyTilesInRange, self.__currentUnit)

                        # we did not find a target to attack, just move as close as we can to a target
                        if self.__defendingUnit == None:
                            path = self.findNearestPlayerPath(self.__currentUnit)
                            # don't target a tile that has a unit already, unless it is self.__currentUnit
                            for tile in path:
                                if tile.currentUnit == None or tile.currentUnit == self.__currentUnit:
                                    targetTile = tile
                                    break

                        self.__pathManager.resetPath(targetTile)
                        self.__pathManager.followPath()
                        self.__moving = True
                        self.__mapManager.resetCurrentMap()

                    else:
                        self.__playerTurn = True
                        self.__currentUnit = None
                        self.__unitHolder.resetForNextTurn()
                
                ## menu and cursor controls 
                ## if keys (they are up here because you should be able to hold the key)
                ## TODO maybe these should be a variable OR there should be one state that 
                ## covers when the cursor controls should be active...
                elif self.__playerTurn and not (self.__currentState in [states.selectingAction, states.selectingAttack, states.selectingTrade, states.selectingItems, states.selectingWeapon, states.attacking]):
                    # cursor controls
                    # get the arrow keys pressed 
                    arrowKeys = [keys[pygame.K_DOWN], keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_LEFT]]
                    self.__mapManager.checkUI(arrowKeys, self.__mapUnitUI, self.__battleForecast, self.__pathManager)
                    
                # menu movement controls
                elif self.__playerTurn and self.__currentState == states.selectingAction:
                    menuKeys = [keys[pygame.K_DOWN], keys[pygame.K_UP]]
                    self.__actionMenu.checkForMenuControls(menuKeys)

                for event in pygame.event.get():
                    ## quit
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.__running = False
                    if self.__currentState == states.inMainMenu: 
                        if event.type == pygame.KEYDOWN:
                            self.__currentState = states.selectingUnit
                    # player turn
                    elif self.__playerTurn:
                        # picking a unit to attack
                        if self.__currentState == states.selectingAttack:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                                self.__currentState = states.attacking
                                self.__battleForecast.roll()
                                self.__combatManager.setupAttack(self.__currentUnit, self.__defendingUnit, self.__battleForecast, True)

                            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_UP):
                                self.__selectingAttack.moveUp()
                                self.__defendingUnit = self.__selectingAttack.getTargetedUnit()
                                self.__mapManager.setCursorOnUnit(self.__defendingUnit)
                                self.__battleForecast.calculate(self.__currentUnit, self.__defendingUnit, self.canDefendingUnitCounter(self.__currentUnit, self.__defendingUnit))

                            if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_DOWN):
                                self.__selectingAttack.moveDown()
                                self.__defendingUnit = self.__selectingAttack.getTargetedUnit()
                                self.__mapManager.setCursorOnUnit(self.__defendingUnit)
                                self.__battleForecast.calculate(self.__currentUnit, self.__defendingUnit, self.canDefendingUnitCounter(self.__currentUnit, self.__defendingUnit))

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                                self.__currentState = states.selectingWeapon

                        elif self.__currentState == states.selectingItems:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                                self.__currentState = states.selectingAction
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                                self.__currentUnit.inventory.up()
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                                self.__currentUnit.inventory.down()
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                                if self.__currentUnit.inventory.activateItem(self.__currentUnit):
                                    self.resetAfterAction()

                        elif self.__currentState == states.selectingTrade:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                                pass
                                # TODO implement trading
                                # currentState = states.trading

                            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_UP):
                                self.__selectingTrade.moveUp()
                                self.__defendingUnit = self.__selectingTrade.getTargetedUnit()
                                self.__mapManager.setCursorOnUnit(self.__defendingUnit)
                                # TODO draw defendingUnit inventory
                                ## also below case

                            if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_DOWN):
                                self.__selectingTrade.moveDown()
                                self.__defendingUnit = self.__selectingTrade.getTargetedUnit()
                                self.__mapManager.setCursorOnUnit(self.__defendingUnit)

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                                self.__currentState = states.selectingAction

                        elif self.__currentState == states.selectingWeapon:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                                self.__currentState = states.selectingAttack
                                self.__currentUnit.inventory.equipSelectedWeapon()
                                self.__mapManager.resetCurrentMap()
                                tilesInAttackRange = self.findTilesInAttackRange(self.__mapManager.getTileUnitIsOn(self.__currentUnit), self.__currentUnit.inventory.getEquippedWeapon().range)
                                self.__selectingAttack.getUnitsInRange(tilesInAttackRange, self.__unitHolder.getEnemies())
                                self.__defendingUnit = self.__selectingAttack.getTargetedUnit()
                                self.__mapManager.setCursorOnUnit(self.__defendingUnit)
                                self.__battleForecast.calculate(self.__currentUnit, self.__defendingUnit, self.canDefendingUnitCounter(self.__currentUnit, self.__defendingUnit))

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                                self.__currentState = states.selectingAction

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                                self.__currentUnit.inventory.up()
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                                self.__currentUnit.inventory.down()

                        ### selecting action in menu
                        elif self.__currentState == states.selectingAction:
                            # action selected from menu
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                                selectedOption = self.__actionMenu.selectOption()
                                if selectedOption == menuOptions.wait:
                                    self.resetAfterAction()
                                    
                                elif selectedOption == menuOptions.attack:
                                    self.__currentUnit.inventory.getAvaliableWeapons(self.findTilesInAttackRange, self.__mapManager.getTileUnitIsOn(self.__currentUnit), self.__unitHolder.getEnemies())
                                    self.__currentState = states.selectingWeapon

                                elif selectedOption == menuOptions.items:                            
                                    self.__currentState = states.selectingItems
                                    self.__currentUnit.inventory.setAllItemsAvaliable()

                                elif selectedOption == menuOptions.trade:
                                    self.__currentState = states.selectingTrade
                                    self.__currentUnit.inventory.setAllItemsAvaliable()
                                    self.__defendingUnit = self.__selectingTrade.getTargetedUnit()
                                    self.__defendingUnit.inventory.setAllItemsAvaliable()
                                    self.__mapManager.setCursorOnUnit(self.__defendingUnit)


                            # go back to selecting tile
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                                self.__mapManager.resetCurrentMap()
                                self.__currentUnitTile.currentUnit = None
                                self.__currentUnit.X = self.__currentUnitStartingTile.X
                                self.__currentUnit.Y = self.__currentUnitStartingTile.Y
                                self.__currentUnitStartingTile.currentUnit = self.__currentUnit
                                self.__currentUnitTile = self.__currentUnitStartingTile
                                # update state
                                self.__currentState = states.selectingTile
                                tilesInRange = self.findTilesInMovRange(self.__currentUnit)
                                for tile in tilesInRange:
                                    if tile.currentUnit == None or tile.currentUnit == self.__currentUnit:
                                        tile.selectable = True
                                        for atkTile in self.findTilesInAttackRange(tile, self.__currentUnit.inventory.getBestRange()):
                                            if atkTile not in tilesInRange:
                                                atkTile.attackable = True
                                cursorTile = self.__mapManager.getTileCursorIsOn()
                                if cursorTile.selectable:
                                    self.__pathManager.resetPath(cursorTile)
                                

                        ### selecting what tile to move to 
                        elif self.__currentState == states.selectingTile:
                            # Select tile and get ready to move to it
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                                cursorTile = self.__mapManager.getTileCursorIsOn()
                                if cursorTile.selectable:
                                    self.__moving = True
                                    self.__currentState = states.selectingUnit
                                    self.__pathManager.resetPath(cursorTile)
                                    self.__pathManager.followPath()
                                    self.__mapManager.resetCurrentMap()

                            # Stop selecting tile
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                                # clear path
                                self.__pathManager.emptyPath()
                                self.__mapManager.resetCurrentMap()
                                self.__currentUnit = None
                                self.__currentUnitTile = None
                                self.__currentUnitStartingTile = None
                                self.__currentState = states.selectingUnit
                                
                                

                        elif self.__currentState == states.viewingUnitInfo:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                                self.__currentState = states.selectingUnit

                        ### no unit selected, waiting for next unit to be selected
                        elif self.__currentState == states.selectingUnit:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                self.__playerTurn = False
                                
                            # Select unit and show their range
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                                
                                # get the unit that cursor is on
                                currentTile = self.__mapManager.getTileCursorIsOn()
                                self.__currentUnit = currentTile.currentUnit
                                
                                # get tiles in range of that unit and highlight them
                                if self.__currentUnit != None:
                                    self.setTilesInRangeAttackable(self.__currentUnit.inventory.getBestRange(), self.findTilesInMovRange(self.__currentUnit))
                                    if self.__currentUnit.active and self.__currentUnit.getIsPlayer():
                                        self.__currentState = states.selectingTile
                                        self.__currentUnitTile = currentTile
                                        self.__currentUnitStartingTile = currentTile
                            
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                                self.__currentUnit = None
                                self.__mapManager.resetCurrentMap()
                                self.__pathManager.emptyPath()
                                self.__currentState = states.selectingUnit
                                
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                                currentTile = self.__mapManager.getTileCursorIsOn()
                                if currentTile.currentUnit != None:
                                    self.__currentUnit = currentTile.currentUnit
                                    self.__unitInfo.reset(self.__currentUnit)
                                    self.__currentState = states.viewingUnitInfo
            
            #### drawing ####
            if self.__currentState == states.inMainMenu:
                self.__mainMenu.draw(self.__screen)
            
            ## attacking ####
            elif self.__currentState == states.attacking:
                self.__screen.blit(self.__attackingBackground, (0, 0))
                
                if self.__attackingState == atkStates.levelingUp:
                    if self.__levelUp.draw(self.__screen, font):
                        self.__attackingState = atkStates.addingExp
                        self.__levelUp.currUnit = None 
                        
                elif self.__attackingState == atkStates.addingExp:
                    if self.__exp.currUnit.exp >= 100:
                        self.__attackingState = atkStates.levelingUp
                        self.__levelUp.currUnit = self.__exp.currUnit
                        self.__levelUp.roll(self.__exp.currUnit)
                        self.__exp.currUnit.exp = 0
                        self.__exp.currUnit.level += 1

                    elif self.__exp.draw(self.__screen, self.__gameWidth):
                        self.__attackingState = atkStates.finishedAttacking 

                elif self.__combatManager.runSequence():
                    if self.__currentUnit.getStat(Stat.HP) <= 0:
                        self.__unitHolder.removeUnit(self.__currentUnit)
                        self.__mapManager.getTileUnitIsOn(self.__currentUnit).currentUnit = None
                    if self.__defendingUnit.getStat(Stat.HP) <= 0:
                        self.__unitHolder.removeUnit(self.__defendingUnit)
                        self.__mapManager.getTileUnitIsOn(self.__defendingUnit).currentUnit = None
                        
                    if self.__combatManager.getExp() > 0:
                        self.__attackingState = atkStates.addingExp
                        if self.__currentUnit.getStat(Stat.HP) > 0 and self.__currentUnit.getIsPlayer():
                            self.__exp.setup(self.__currentUnit, self.__combatManager.getExp())

                        elif self.__defendingUnit.getStat(Stat.HP) > 0 and self.__defendingUnit.getIsPlayer():
                            self.__exp.setup(self.__defendingUnit, self.__combatManager.getExp())

                        else:
                            self.__attackingState = atkStates.finishedAttacking
                            
                    else:
                        self.__attackingState = atkStates.finishedAttacking

                if self.__attackingState == atkStates.finishedAttacking:
                    self.__attackingState = atkStates.attacking
                    # break out of attacking
                    self.__currentState = states.selectingUnit
                    self.resetAfterAction()

                    ## check if we have to transition to the next map
                    mapComplete, noMoreMaps = self.__mapManager.checkForMapCompletion()
                    if mapComplete and not noMoreMaps:
                        self.__playerTurn = True
                        self.__unitHolder.moveToNextMap(self.__mapManager.getCurrentMap())
                    if noMoreMaps:
                        self.__running = False

            else:
                self.__screen.fill((0,0,0))
                self.__mapManager.draw(self.__screen)
                
                self.__unitHolder.drawUnits(self.__screen, self.__tileSize, self.__mapManager.getCameraX(), self.__mapManager.getCameraY())

                self.__mapUnitUI.draw(self.__screen, font)
                if self.__currentState == states.selectingAttack:
                    self.__battleForecast.draw(self.__screen, font, self.__currentUnit, self.__selectingAttack.getTargetedUnit())

                elif self.__currentState == states.selectingItems:
                    self.__currentUnit.inventory.draw(self.__screen, font)         

                elif self.__currentState == states.selectingWeapon:
                    self.__currentUnit.inventory.draw(self.__screen, font)

                elif self.__currentState == states.trading:
                    self.__defendingUnit.inventory.draw(self.__screen, font)

                elif self.__currentState == states.selectingAction:
                    self.__actionMenu.draw(self.__screen, self.__gameWidth)
                
                elif self.__currentState == states.viewingUnitInfo:
                    self.__unitInfo.draw(self.__screen, font)
                        
            pygame.display.update()
            pygame.time.delay(60)

game = Game()
game.run()