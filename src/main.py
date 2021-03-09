import pygame
import random

pygame.init()
gameWidth = 1920
gameHeight = 1080
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Code FE")
running = True

#------ load assets --------
## Tiles
grassTilePic = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/grassTile.png")
selectablePic = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/selectableHighlight.png")
attackablePic = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/attackableHighlight.png")
occupiedPic = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/occupiedHighlight.png")
cursorPic = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/cursor.png")

## Characters
protagPicA = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/protag_A.png")
protagPicB = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/protag_B.png")

combatUnit = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/combat-unit.png")
## Menu
waitButton = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/wait-button.png")
attackButton = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/attack-button.png")
menuCursor = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/menu-cursor.png")

### Battle Forecast
battleForecastPic = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/battle-forecast.png")

## backgrounds
attacingBackground = pygame.image.load("C:/Users/Charlie/Desktop/tryingThisAgain/assets/attacking-background.png")
#---------------------------

class Map():

    def __init__(self, width, height):
        self.width=width
        self.height=height

        # creates a list of rows of tiles
        tiles = []
        currHeight = 0
        currWidth = 0
        for i in range(width):
            row = []
            for j in range(height):
                row.append(Tile(currWidth, currHeight))
                currHeight+=1
            currHeight = 0
            currWidth+=1
            tiles.append(row)
        self.tiles = tiles
        for row in self.tiles:
            for tile in row:
                if tile.Y < self.height-1:
                    tile.adjList.append(self.tiles[tile.X][tile.Y+1])
                if tile.Y > 0:
                    tile.adjList.append(self.tiles[tile.X][tile.Y-1])
                if tile.X < self.width-1:
                    tile.adjList.append(self.tiles[tile.X+1][tile.Y])
                if tile.X > 0:
                    tile.adjList.append(self.tiles[tile.X-1][tile.Y])
                    
    def scrollUp(self):
        for row in self.tiles:
            for tile in row:
                tile.Y -= tileSize
    def scrollDown(self):
        for row in self.tiles:
            for tile in row:
                tile.Y += tileSize
    def scrollRight(self):
        for row in self.tiles:
            for tile in row:
                tile.X += tileSize
    def scrollLeft(self):
        for row in self.tiles:
            for tile in row:
                tile.X -= tileSize

    def addUnitToMap(self, unit):
        self.tiles[unit.X][unit.Y].currentUnit = unit

    def reset(self):
        for row in self.tiles:
            for tile in row:
                tile.reset()
    def draw(self, screen):
        for row in self.tiles:
            for tile in row:
                tile.draw(screen)
            
class Tile():

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.currentUnit = None
        self.pic = pygame.transform.scale(grassTilePic, (tileSize, tileSize))
        self.selectable = False
        self.selectablePic = pygame.transform.scale(selectablePic, (tileSize, tileSize))
        self.attackable = False
        self.attackablePic = pygame.transform.scale(attackablePic, (tileSize, tileSize))
        self.occupiedPic = pygame.transform.scale(occupiedPic, (tileSize, tileSize))
        self.adjList = []
        self.distance = maxDistance
        self.parent = None

    def __str__(self):
        return "X: {0}\tY: {1}".format(self.X, self.Y)

    def reset(self):
        self.parent = None
        self.distance = maxDistance
        self.selectable = False
        self.attackable = False

    def draw(self, screen):
        screen.blit(self.pic, (self.X*tileSize, self.Y*tileSize))
        if self.currentUnit != None:
            screen.blit(self.occupiedPic, (self.X*tileSize, self.Y*tileSize))
        elif self.attackable:
            screen.blit(self.attackablePic, (self.X*tileSize, self.Y*tileSize))
        elif self.selectable:
            screen.blit(self.selectablePic, (self.X*tileSize, self.Y*tileSize))
        
class Cursor():

    def __init__(self):
        self.X = 1
        self.Y = 2
        self.pic = pygame.transform.scale(cursorPic, (tileSize, tileSize))

    def down(self):
        if self.Y < mapHeight-1:
            self.Y+=1
    def up(self):
        if self.Y > 0:
            self.Y-=1
    def right(self):
        if self.X < mapWidth-1:
            self.X+=1
    def left(self):
        if self.X > 0:
            self.X-=1

    def draw(self, screen):
        screen.blit(self.pic, (self.X*tileSize, self.Y*tileSize))

class BattleForcast():

    def __init__(self):
        self.X = gameWidth - 500
        self.Y = 200
        self.pic = battleForecastPic

        self.attackingUnitDmg = 0
        self.defendingUnitDmg = 0
        self.attackingUnitHit = 0
        self.defendingUnitHit = 0
        self.attackingUnitCrit = 0
        self.defendingUnitCrit = 0

        self.attackingUnitWillHit = False
        self.defendingUnitWillHit = False


        self.defendingUnitCanCounter = True

    def calculate(self, attackingUnit, defendingUnit):
        self.attackingUnitDmg = max(0, attackingUnit.attack - defendingUnit.defense)
        self.attackingUnitHit = int((75 + (attackingUnit.skill * 2) + attackingUnit.luck / 2) - ((defendingUnit.speed * 2) + defendingUnit.luck))

        
        self.defendingUnitDmg = max(0, defendingUnit.attack - attackingUnit.defense)
        self.defendingUnitHit = int((75 + (defendingUnit.skill * 2) + defendingUnit.luck / 2) - ((attackingUnit.speed * 2) + attackingUnit.luck))

    def roll(self):
        if random.randint(0, 100) < self.attackingUnitHit:
            self.attackingUnitWillHit = True
        else:
            self.attackingUnitWillHit = False
        if random.randint(0, 100) < self.defendingUnitHit:
            self.defendingUnitWillHit = True
        else:
            self.defendingUnitWillHit = False

    def draw(self, screen):
        screen.blit(self.pic, (self.X, self.Y))

        pHpText = font.render(str(currentUnit.hp), True, (0,0,0))
        pHpRect = pHpText.get_rect()
        pHpRect.center = (self.X+75, self.Y+85)

        pAttackText = font.render(str(self.attackingUnitDmg), True, (0,0,0))
        pAttackRect = pAttackText.get_rect()
        pAttackRect.center = (self.X+75, self.Y+185) 

        pHitText = font.render(str(self.attackingUnitHit), True, (0,0,0))
        pHitRect = pHitText.get_rect()
        pHitRect.center = (self.X+75, self.Y+330)

        pCritText = font.render(str(self.attackingUnitCrit), True, (0,0,0))
        pCritRect = pCritText.get_rect()
        pCritRect.center = (self.X+75, self.Y+500)

        eHpText = font.render(str(unitsInRange[attackUnitIndex].hp), True, (0,0,0))
        eHpRect = eHpText.get_rect()
        eHpRect.center = (self.X+390, self.Y+85)

        eAttackText = font.render(str(self.defendingUnitDmg), True, (0,0,0))
        eAttackRect = eAttackText.get_rect()
        eAttackRect.center = (self.X + 390, self.Y+185)

        eHitText = font.render(str(self.defendingUnitHit), True, (0,0,0))
        eHitRect = eHitText.get_rect()
        eHitRect.center = (self.X+390, self.Y+330)

        eCritText = font.render(str(self.defendingUnitCrit), True, (0,0,0))
        eCritRect = eCritText.get_rect()
        eCritRect.center = (self.X+390, self.Y+500)

        screen.blit(pHpText, pHpRect)
        screen.blit(pAttackText, pAttackRect) 
        screen.blit(pHitText, pHitRect)
        screen.blit(pCritText, pCritRect)

        screen.blit(eHpText, eHpRect)
        screen.blit(eAttackText, eAttackRect)
        screen.blit(eHitText, eHitRect)
        screen.blit(eCritText, eCritRect)
        
class CombatAnimation():

    def __init__(self):
        self.attackingUnitAnimation = []
        self.defendingUnitAnimation = []
        self.animationRunning = True
        self.AUAindex = 0
        self.DUAindex = 0

    def setup(self, attackingUnitAnimation, defendingUnitAnimation):
        self.attackingUnitAnimation = attackingUnitAnimation
        self.defendingUnitAnimation = defendingUnitAnimation
        self.AUAindex = 0
        self.DUAindex = 0
        self.animationRunning = True

    def draw(self, screen):
        screen.blit(attacingBackground, (0,0))
        ## go through each frame in attackingUnitAnimation unit there is none left
        if self.AUAindex <= len(self.attackingUnitAnimation)-1:
            screen.blit(self.attackingUnitAnimation[self.AUAindex], (200, 200))
            screen.blit(self.defendingUnitAnimation[self.DUAindex], (1500, 200))
            self.AUAindex += 1
        elif self.DUAindex <= len(self.defendingUnitAnimation)-1:
            screen.blit(self.attackingUnitAnimation[self.AUAindex-1], (200, 200))
            screen.blit(self.defendingUnitAnimation[self.DUAindex], (1500, 200))
            self.DUAindex += 1
        else:
            self.animationRunning = False
        

class Unit():

    def __init__(self, X, Y):
        self.maxHp = 100
        self.hp = self.maxHp
        self.attack = 10
        self.defense = 5
        self.speed = 6
        self.skill = 6
        self.luck = 4
        self.mov = 4
        self.attackRange = [2, 5]
        self.X = X
        self.Y = Y

        self.fieldPics = [pygame.transform.scale(protagPicA, (tileSize, tileSize)), pygame.transform.scale(protagPicB, (tileSize, tileSize))] 
        self.aniTimer = 5


        self.combatPics = [combatUnit]
        self.combatAniTimer = 20

        self.active = True

    ## return False if animation is done, else return True
    def playCombatAnimation(self, screen, x, y):
        screen.blit(self.combatPics[0], (x, y))
        self.combatAniTimer -=1
        if self.combatAniTimer <= 0:
            self.combatAniTimer = 20
            return False
        else:
            return True

    def draw(self, screen):
        screen.blit(self.fieldPics[0], (self.X*tileSize, self.Y*tileSize))
        self.aniTimer -= 1
        if self.aniTimer < 0:
            tmpPic = self.fieldPics.pop(0)
            self.fieldPics.append(tmpPic)
            self.aniTimer = 5

# globals
currentUnit = None
defendingUnit = None
## map
tileSize = 96
mapWidth = 24
mapHeight = 16
maxDistance = 256

## movement
moving = False
movingVelocity = 3
moveTimer = movingVelocity
currentUnitTile = None
currentUnitStartingTile = None
path = []

## player state
playerTurn = True
selectingTile = False
selectingAction = False
selectingAttack = False
attacking = False
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


## custom classes
map1 = Map(mapWidth, mapHeight)
myBattleForcast = BattleForcast()
myCombatAnimation = CombatAnimation()

mainCursor = Cursor()
## width first, height second (width goes from left to right, height goes from top to bottom)
protag = Unit(3, 9)
Jagen = Unit(3, 5)
Jagen.attack = 90000
Jagen.defense = 10
Jagen.speed = 9

enemy = Unit(2, 2)
enemy1 = Unit(2, 3)
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


# main game loop
while running:
    keys = pygame.key.get_pressed()

    # if something is moving there shouldn't be any other input accepted
    if moving:
        moveTimer -=1
        if moveTimer < 0:
            moveTimer = movingVelocity
            # if there is still another tile in the path
            if len(path) > 0:
                nextTile = path.pop()
                currentUnit.X = nextTile.X
                currentUnit.Y = nextTile.Y
                currentUnitTile = nextTile
            # there's no more tiles to move to so we are done moving
            else:
                moving = False
                
                # we are done moving time to find a way to attack
                if not playerTurn:
                    pass
                # pass control back to player to pick an option
                else:
                    selectingAction = True
                    # reset menu options
                    menuOptions = ['wait']
                    menuSelectionIndex = 0
                    # check what menu options are avaliable (wait added by default)
                    ## check if there is a unit to attack in range
                    unitsInRange = []
                    for row in map1.tiles:
                        for tile in row:
                            tile.distance = maxDistance
                    currTile = currentUnitTile
                    currTile.distance = 0
                    queue = []
                    visited = []
                    queue.append(currTile)
                    visited.append(currTile)
                    while len(queue) > 0:
                        queue.sort(key=lambda tile:tile.distance)
                        currTile = queue.pop(0)
                        if currTile.distance <= currentUnit.attackRange[1]:
                            if currTile.distance >= currentUnit.attackRange[0]:
                                currTile.attackable = True
                                if currTile.currentUnit != None and currTile.currentUnit in enemyUnits and currTile.currentUnit not in unitsInRange:
                                    unitsInRange.append(currTile.currentUnit)
                            for tile in currTile.adjList:
                                if tile not in visited:
                                    visited.append(currTile)
                                    tile.distance = currTile.distance + 1
                                    queue.append(tile)
                    if len(unitsInRange) > 0:
                        menuOptions.append('attack')

    # not moving
    else: 
        ## if keys (they are up here because you should be able to hold the key)
        if playerTurn and not selectingAction and not selectingAttack:
            # cursor controls
            if keys[pygame.K_DOWN]:
                mainCursor.down()
            if keys[pygame.K_UP]:
                mainCursor.up()
            if keys[pygame.K_RIGHT]:
                mainCursor.right()
            if keys[pygame.K_LEFT]:
                mainCursor.left()
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
            # if its player turn or not
            ## end turn
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                playerTurn = False
                selectingAction = False
            ## quit
            if event.type == pygame.QUIT:
                running = False
            
            if not playerTurn:
                if len(activeEnemyUnits) > 0:
                    # find closest player unit
                    currentUnit = activeEnemyUnits.pop()
                    currTile = map1.tiles[currentUnit.X][currentUnit.Y]
                    currentUnitTile = currTile
                    currTile.distance = 0
                    queue = []
                    added = []
                    queue.append(currTile)
                    while len(queue) > 0:
                        queue.sort(key=lambda tile:tile.distance)
                        currTile = queue.pop(0)
                        added.append(currTile)
                        for tile in currTile.adjList:
                            if moving:
                                break
                            # if we found a player unit
                            if tile.currentUnit != None and tile.currentUnit in playerUnits:
                                while currTile.parent!=None:
                                    path.append(currTile)
                                    currTile = currTile.parent
                                # make sure we can't move past our move
                                if len(path) > currentUnit.mov:
                                    path = path[len(path)-currentUnit.mov:]
                                moving = True
                                map1.reset()
                            elif tile not in added and tile.currentUnit == None:
                                altDist = currTile.distance + 1
                                if tile.distance > altDist:
                                    tile.distance = altDist
                                    tile.parent = currTile
                                queue.append(tile)
                        if moving:
                                currentUnitTile.currentUnit = None
                                if len(path) > 0:
                                    path[0].currentUnit = currentUnit
                                break
                else:
                    # there are no more Enemy Units to move
                    # start player turn
                    playerTurn = True
                    for unit in playerUnits:
                        unit.active = True
                    for unit in enemyUnits:
                        activeEnemyUnits.append(unit)

            # player turn
            else:
                # picking a unit to attack
                if selectingAttack:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        attacking = True
                        myBattleForcast.roll()
                        myCombatAnimation.setup(currentUnit.combatPics, defendingUnit.combatPics)

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_UP):
                        if attackUnitIndex < len(unitsInRange) - 1:
                            attackUnitIndex += 1
                        else:
                            attackUnitIndex = 0
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit)

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_DOWN):
                        if attackUnitIndex > 0:
                            attackUnitIndex -= 1
                        else:
                            attackUnitIndex = len(unitsInRange)-1
                        defendingUnit = unitsInRange[attackUnitIndex]
                        mainCursor.X = defendingUnit.X
                        mainCursor.Y = defendingUnit.Y
                        myBattleForcast.calculate(currentUnit, defendingUnit)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        selectingAttack = False
                        selectingAction = True

                ### selecting action in menu
                elif selectingAction:
                    # action selected from menu
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        if menuOptions[menuSelectionIndex] == 'wait':
                            currentUnit.active = False
                            currentUnit = None
                            currentUnitStartingTile = None
                            currentUnitTile = None
                            path = []
                            map1.reset()
                            selectingAction = False
                            selectingTile = False
                            
                        if menuOptions[menuSelectionIndex] == 'attack':
                            selectingAction = False
                            selectingAttack = True
                            attackUnitIndex = 0
                            defendingUnit = unitsInRange[attackUnitIndex]
                            mainCursor.X = defendingUnit.X
                            mainCursor.Y = defendingUnit.Y
                            myBattleForcast.calculate(currentUnit, defendingUnit)
                    # go back to selecting tile
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        currentUnitTile.currentUnit = None
                        currentUnit.X = currentUnitStartingTile.X
                        currentUnit.Y = currentUnitStartingTile.Y
                        currentUnitStartingTile.currentUnit = currentUnit
                        selectingAction = False
                        selectingTile = True
                        for row in map1.tiles:
                            for tile in row:
                                tile.attackable = False

                ### selecting what tile to move to 
                elif selectingTile:
                    # Select tile and get ready to move to it
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        tileToMoveTo = map1.tiles[mainCursor.X][mainCursor.Y]
                        if tileToMoveTo.selectable:
                            currentUnitStartingTile.currentUnit = None
                            tileToMoveTo.currentUnit = currentUnit
                            path = []
                            while tileToMoveTo.parent!=None:
                                path.append(tileToMoveTo)
                                tileToMoveTo = tileToMoveTo.parent
                            selectingTile = False
                            moving = True
                    # Stop selecting tile
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        map1.reset()
                        currentUnitStartingTile.currentUnit = currentUnit
                        currentUnit = None
                        currentUnitTile = None
                        currentUnitStartingTile = None
                        selectingTile = False

                ### no unit selected, waiting for next unit to be selected
                else:
                    # Select unit and show their range
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        
                        # get the unit that cursor is on
                        currentTile = map1.tiles[mainCursor.X][mainCursor.Y]
                        currentUnit = currentTile.currentUnit
                        
                        # get tiles in range of that unit and highlight them
                        if currentUnit != None and currentUnit.active and currentUnit in playerUnits:
                            # need to save this for later
                            currentUnitTile = currentTile
                            currentUnitTile.currentUnit = None
                            currentUnitStartingTile = currentTile
                            
                            currentTile.distance = 0
                            queue = []
                            added = []
                            queue.append(currentTile)
                            added.append(currentTile)
                            while len(queue) > 0:
                                queue.sort(key=lambda tile:tile.distance)
                                currTile = queue.pop(0)
                                if currTile.distance <= currentUnit.mov and (currTile.currentUnit == None or currTile.currentUnit == currentUnit):
                                    currTile.selectable = True
                                    added.append(currTile)
                                    for tile in currTile.adjList:
                                        if tile not in added:
                                            altDist = currTile.distance + 1
                                            if tile.distance > altDist:
                                                tile.distance = altDist
                                                tile.parent = currTile
                                            queue.append(tile)
                            selectingTile = True
                                

    if attacking:
        

        ## play currentUnit attacking animation
        if myCombatAnimation.animationRunning:
            myCombatAnimation.draw(screen)
        ## if current unit will miss, play defending unit dodge animation
        ## else play defending unit hit animation

        ## if defending unit died or can't counter, end attack
        ## else play counter attack animation
        ## if 


        else:
            # finish up attacking
            if myBattleForcast.attackingUnitWillHit:
                defendingUnit.hp -= myBattleForcast.attackingUnitDmg
                print("attacking unit hit")
            else:
                print("attacking unit miss")

            if defendingUnit.hp > 0 and myBattleForcast.defendingUnitCanCounter and myBattleForcast.defendingUnitWillHit:
                currentUnit.hp -= myBattleForcast.defendingUnitDmg
                print("defending unit hit")
            elif not myBattleForcast.defendingUnitWillHit:
                print("defending unit miss")
            if defendingUnit.hp <= 0:
                enemyUnits.remove(defendingUnit)
                activeEnemyUnits.remove(defendingUnit)
                map1.tiles[defendingUnit.X][defendingUnit.Y].currentUnit = None
                print("defending unit died")
            if currentUnit.hp <= 0:
                playerUnits.remove(currentUnit)
                map1.tiles[currentUnit.X][currentUnit.Y].currentUnit = None
                print("attacking unit died")
            attacking = False
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
        map1.draw(screen)
        mainCursor.draw(screen)
        for unit in playerUnits:
            unit.draw(screen)
        for enemy in enemyUnits:
            enemy.draw(screen)
        
        if selectingAttack:
            myBattleForcast.draw(screen)

        elif selectingAction:
            screen.blit(menuCursor, (gameWidth-350, 200+(165*menuSelectionIndex)))
            Y = 200
            if "wait" in menuOptions:
                screen.blit(waitButton, (gameWidth - 300, Y))
                Y+= 165
            if "attack" in menuOptions:
                screen.blit(attackButton, (gameWidth - 300, Y))

    pygame.display.update()
    pygame.time.delay(60)
