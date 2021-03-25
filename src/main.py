import pygame
import random
from pathlib import Path

pygame.init()
gameWidth = 1920
gameHeight = 1080
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Code FE")
running = True

#------ load assets --------

## Tiles
grassTilePic = pygame.image.load(Path(__file__).parent / "../assets/grassTile.png")
selectablePic = pygame.image.load(Path(__file__).parent / "../assets/selectableHighlight.png")
attackablePic = pygame.image.load(Path(__file__).parent / "../assets/attackableHighlight.png")
occupiedPic = pygame.image.load(Path(__file__).parent / "../assets/occupiedHighlight.png")
cursorPic = pygame.image.load(Path(__file__).parent / "../assets/cursor.png")

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
attackButton = pygame.image.load(Path(__file__).parent / "../assets/attack-button.png")
menuCursor = pygame.image.load(Path(__file__).parent / "../assets/menu-cursor.png")
unitInfoPic = pygame.image.load(Path(__file__).parent / "../assets/unit-info.png")

### Combat and UI
battleForecastPic = pygame.image.load(Path(__file__).parent / "../assets/battle-forecast.png")
combatUI = pygame.image.load(Path(__file__).parent / "../assets/Combat-UI.png")
combatUIRed = pygame.image.load(Path(__file__).parent / "../assets/Combat-UI-red.png")
healthbarfullPiece = pygame.image.load(Path(__file__).parent / "../assets/healthbar-piece.png")
healthbarEmptyPiece = pygame.image.load(Path(__file__).parent / "../assets/healthbar-piece-empty.png")
mapUnitUI = pygame.image.load(Path(__file__).parent / "../assets/map-unit-UI.png")

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


## player state
playerTurn = True
viewingUnitInfo = False
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


# custom classes
class Map():

    def __init__(self, width, height, background):
        self.width=width
        self.height=height
        self.background = background
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

    def addUnitToMap(self, unit):
        self.tiles[unit.X][unit.Y].currentUnit = unit

    def reset(self):
        for row in self.tiles:
            for tile in row:
                tile.reset()

    def draw(self, screen):
        screen.blit(self.background, (xCamera, yCamera))
        for row in self.tiles:
            for tile in row:
                tile.draw(screen)
            
class Tile():

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.currentUnit = None
        self.pic = pygame.transform.scale(grassTilePic, (tileSize, tileSize))
        self.walkable = True
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
        #screen.blit(self.pic, (self.X*tileSize, self.Y*tileSize))
        if self.currentUnit != None:
            screen.blit(self.occupiedPic, (self.X*tileSize + xCamera, self.Y*tileSize + yCamera))
        elif self.attackable:
            screen.blit(self.attackablePic, (self.X*tileSize + xCamera, self.Y*tileSize + yCamera))
        elif self.selectable:
            screen.blit(self.selectablePic, (self.X*tileSize + xCamera, self.Y*tileSize + yCamera))
        
class Cursor():

    def __init__(self):
        self.X = 1
        self.Y = 2
        self.yCameraOffset = 0
        self.xCameraOffset = 0
        self.pic = pygame.transform.scale(cursorPic, (tileSize, tileSize))

    def down(self):
        if self.Y < mapHeight-1:
            self.Y+=1
            if (self.Y * tileSize) + yCamera + tileSize  > gameHeight:
                self.yCameraOffset += 1
                return -tileSize
        return 0

    def up(self):
        if self.Y > 0:
            self.Y-=1
            if (self.Y * tileSize) + yCamera < tileSize:
                self.yCameraOffset -= 1
                return tileSize
        return 0

    def right(self):
        if self.X < mapWidth-1:
            self.X+=1
            if (self.X * tileSize) + xCamera + tileSize > gameWidth:
                self.xCameraOffset += 1
                return -tileSize
        return 0

    def left(self):
        if self.X > 0:
            self.X-=1
            if (self.X * tileSize) + xCamera < tileSize:
                self.xCameraOffset -= 1
                return tileSize
        return 0

    def draw(self, screen):
        screen.blit(self.pic, ((self.X*tileSize) - (self.xCameraOffset*tileSize), (self.Y*tileSize) - (self.yCameraOffset*tileSize)))

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
        ## need to check if defendingUnit is in range to counter attack
        self.defendingUnitCanCounter = False
        for tile in findTilesInAttackRange(map1.tiles[defendingUnit.X][defendingUnit.Y], defendingUnit.attackRange):
            if tile.currentUnit == attackingUnit:
                self.defendingUnitCanCounter = True
        

        self.attackingUnitDmg = max(0, attackingUnit.attack - defendingUnit.defense)
        self.attackingUnitHit = int((75 + (attackingUnit.skill * 2) + attackingUnit.luck / 2) - ((defendingUnit.speed * 2) + defendingUnit.luck))
        
        self.defendingUnitDmg = max(0, defendingUnit.attack - attackingUnit.defense)
        self.defendingUnitHit = int((75 + (defendingUnit.skill * 2) + defendingUnit.luck / 2) - ((attackingUnit.speed * 2) + attackingUnit.luck))

    def roll(self):
        if random.randint(0, 100) <= self.attackingUnitHit:
            self.attackingUnitWillHit = True
        else:
            self.attackingUnitWillHit = False
        if random.randint(0, 100) <= self.defendingUnitHit:
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
        
class CombatUI():

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.pic = combatUI
        self.enemyPic = combatUIRed
        
    def draw(self, screen, battleForcast):
        DUOffset = 1075
        if currentUnit in enemyUnits:
            screen.blit(self.enemyPic, (self.X, self.Y))
            screen.blit(self.pic, (self.X + DUOffset, self.Y))
        else:
            screen.blit(self.pic, (self.X, self.Y))
            screen.blit(self.enemyPic, (self.X + DUOffset, self.Y))

        CUNameText = font.render(currentUnit.name, True, (0,0,0))
        CUNameRect = CUNameText.get_rect()
        CUNameRect.center = (self.X + (len(currentUnit.name) * 25), self.Y + 100)

        CUAttackText = font.render(str(battleForcast.attackingUnitDmg), True, (0,0,0))
        CUAttackRect = CUAttackText.get_rect()
        CUAttackRect.center = (self.X + 185, self.Y + 330)

        CUHitText = font.render(str(battleForcast.attackingUnitHit), True, (0,0,0))
        CUHitRect = CUHitText.get_rect()
        CUHitRect.center = (self.X + 450, self.Y + 330)

        CUCritText = font.render(str(battleForcast.attackingUnitCrit), True, (0,0,0))
        CUCritRect = CUCritText.get_rect()
        CUCritRect.center = (self.X + 720, self.Y + 330)

        for i in range(currentUnit.maxHp):
            screen.blit(healthbarEmptyPiece, (self.X + 50 + (20*i), self.Y + 140))
        for i in range(currentUnit.hp):
            screen.blit(healthbarfullPiece, (self.X + 50 + (20*i), self.Y + 140))
        
        ## defending unit stuff
        DUNameText = font.render(defendingUnit.name, True, (0,0,0))
        DUNameRect = DUNameText.get_rect()
        DUNameRect.center = (self.X + DUOffset + (len(defendingUnit.name) * 25), self.Y + 100)

        DUAttackText = font.render(str(battleForcast.defendingUnitDmg), True, (0,0,0))
        DUAttackRect = DUAttackText.get_rect()
        DUAttackRect.center = (self.X + DUOffset + 185, self.Y + 330)

        DUHitText = font.render(str(battleForcast.defendingUnitHit), True, (0,0,0))
        DUHitRect = DUHitText.get_rect()
        DUHitRect.center = (self.X + DUOffset + 450, self.Y + 330)

        DUCritText = font.render(str(battleForcast.defendingUnitCrit), True, (0,0,0))
        DUCritRect = CUCritText.get_rect()
        DUCritRect.center = (self.X + 720 + DUOffset, self.Y + 330)

        for i in range(defendingUnit.maxHp):
            screen.blit(healthbarEmptyPiece, (self.X + 50 + (20*i) + DUOffset, self.Y + 140))
        for i in range(defendingUnit.hp):
            screen.blit(healthbarfullPiece, (self.X + 50 + (20*i) + DUOffset, self.Y + 140))

        # draw
        ## current unit
        screen.blit(CUNameText, CUNameRect)
        screen.blit(CUAttackText, CUAttackRect)
        screen.blit(CUHitText, CUHitRect)
        screen.blit(CUCritText, CUCritRect)

        ## defending unit
        screen.blit(DUNameText, DUNameRect)
        screen.blit(DUAttackText, DUAttackRect)
        screen.blit(DUHitText, DUHitRect)
        screen.blit(DUCritText, DUCritRect)

class MapUnitUI():

    def __init__(self):
        self.X = gameWidth - 460
        self.Y = gameHeight - 280
        self.pic = mapUnitUI
    def draw(self, screen):
        screen.blit(self.pic, (self.X, self.Y))

class UnitInfo():

    def __init__(self):
        self.pic = unitInfoPic
        self.currUnit = None
    def reset(self, unit):
        self.currUnit = unit

    def draw(self, screen):
        screen.blit(self.pic, (0, 0))

        nameT = font.render(self.currUnit.name, True, (0,0,0))
        nameR = nameT.get_rect()
        nameR.center = (250, 650)

        lvlT = font.render(str(self.currUnit.level), True, (0,0,0))
        lvlR = lvlT.get_rect()
        lvlR.center = (270, 870)

        expT = font.render(str(self.currUnit.exp), True, (0,0,0))
        expR = expT.get_rect()
        expR.center = (630, 870)

        hpT = font.render(str(self.currUnit.hp), True, (0,0,0))
        hpR = hpT.get_rect()
        hpR.center = (330, 990)

        mhpT = font.render(str(self.currUnit.maxHp), True, (0,0,0))
        mhpR = mhpT.get_rect()
        mhpR.center = (450, 990)

        strT = font.render(str(self.currUnit.attack), True, (0,0,0))
        strR = strT.get_rect()
        strR.center = (870, 110)

        sklT = font.render(str(self.currUnit.skill), True, (0,0,0))
        sklR = strT.get_rect()
        sklR.center = (870, 230)

        spdT = font.render(str(self.currUnit.speed), True, (0,0,0))
        spdR = spdT.get_rect()
        spdR.center = (870, 340)

        lckT = font.render(str(self.currUnit.luck), True, (0,0,0))
        lckR = lckT.get_rect()
        lckR.center = (870, 460)

        defT = font.render(str(self.currUnit.defense), True, (0,0,0))
        defR = defT.get_rect()
        defR.center = (870, 580)

        movT = font.render(str(self.currUnit.mov), True, (0,0,0))
        movR = movT.get_rect()
        movR.center = (870, 700)

        screen.blit(nameT, nameR)
        screen.blit(lvlT, lvlR)
        screen.blit(expT, expR)

        screen.blit(hpT, hpR)
        screen.blit(mhpT, mhpR)
        screen.blit(strT, strR)
        screen.blit(sklT, sklR)
        screen.blit(spdT, spdR)
        screen.blit(lckT, lckR)
        screen.blit(defT, defR)
        screen.blit(movT, movR)

class Animation():
    
    def __init__(self, frames):
        ## list of frames for the animation
        self.frames = frames
        ## index for which frame we are on
        self.index = 0

    ## draws 1 frame each call, if animation is finished, resets index and returns true, else returns false
    def draw(self, screen, x, y, reverse):
        if reverse:
            screen.blit(pygame.transform.flip(self.frames[self.index], True, False), (x, y))
        else:
            screen.blit(self.frames[self.index], (x, y))
        self.index+=1
        if self.index == len(self.frames):
            self.index = 0
            return True
        else:
            return False

class Unit():

    def __init__(self, X, Y):
        self.name = "generic"
        self.level = 1
        self.exp = 0
        self.maxHp = 15
        self.hp = self.maxHp
        self.attack = 10
        self.defense = 5
        self.speed = 6
        self.skill = 6
        self.luck = 4
        self.mov = 4
        self.attackRange = [1, 1]
        self.X = X
        self.Y = Y

        self.fieldPics = [pygame.transform.scale(protagPicA, (tileSize, tileSize)), pygame.transform.scale(protagPicB, (tileSize, tileSize))] 
        self.aniTimer = 5

        self.combatAnimation = Animation([combatUnit1,combatUnit2, combatUnit3,combatUnit4, combatUnit5, combatUnit6,combatUnit5, combatUnit4, combatUnit3, combatUnit2, combatUnit1])

        self.active = True


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

class Weapon():
    def __init__(self):
        self.name = "generic"
        self.range = [1, 1]
        self.uses = 45
        self.might = 5
        self.hit = 80
        self.crit = 0

## custom class instances
map1 = Map(mapWidth, mapHeight, map1background)
myBattleForcast = BattleForcast()
mainCursor = Cursor()
myCombatUI = CombatUI(0, gameHeight - 385)
myUnitInfo = UnitInfo()
myMapUnitUI = MapUnitUI()

## width first, height second (width goes from left to right, height goes from top to bottom)
protag = Unit(3, 3)
Jagen = Unit(3, 5)
Jagen.name = 'Jagen'
Jagen.attack = 21
Jagen.defense = 110
Jagen.speed = 9

enemy = Unit(11, 5)
enemy1 = Unit(14, 5)
enemy1.defense = 7
enemy1.attackRange = [2,3]
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


def findPlayerTarget(tiles, unit):
    possibleTargets = []
    for tile in tiles:
        for attackableTile in findTilesInAttackRange(tile, unit.attackRange):
            if attackableTile.currentUnit != None and attackableTile.currentUnit in playerUnits:
                possibleTargets.append((attackableTile.currentUnit, tile))
    #print(possibleTargets[0][0])
    bestTarget = (None, None)
    for target in possibleTargets:
        if target[0].hp < unit.attack - target[0].defense:
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

def checkMapUI():
    if mainCursor.X * tileSize > gameWidth / 2:
        myMapUnitUI.X = 10
        myBattleForcast.X = 10
    else:
        myMapUnitUI.X = gameWidth - 460
        myBattleForcast.X = gameWidth - 500


# main game loop
while running:
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
                myBattleForcast.calculate(currentUnit, defendingUnit)
                myBattleForcast.roll()
                attacking = True
                
            else:
                selectingAction = True
                menuOptions = []
                menuSelectionIndex = 0
                menuOptions.insert(0, "wait")
                unitsInRange = []
                for tile in findTilesInAttackRange(currentUnitTile, currentUnit.attackRange):
                    if tile.currentUnit != None and tile.currentUnit in enemyUnits:
                        unitsInRange.append(tile.currentUnit)
                if len(unitsInRange) > 0:
                    menuOptions.insert(0, "attack")
    # not moving
    else: 
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
        
        ## if keys (they are up here because you should be able to hold the key)
        elif playerTurn and not selectingAction and not selectingAttack:
            # cursor controls
            if keys[pygame.K_DOWN]:
                yCamera += mainCursor.down()
            if keys[pygame.K_UP]:
                yCamera += mainCursor.up()
            if keys[pygame.K_RIGHT]:
                xCamera += mainCursor.right()
                checkMapUI()
            if keys[pygame.K_LEFT]:
                xCamera += mainCursor.left()
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
                            resetAfterAction(currentUnit)
                            currentUnit = None
                            currentUnitStartingTile = None
                            currentUnitTile = None
                            selectingAction = False
                            
                            
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
                        currentUnitTile = currentUnitStartingTile
                        selectingTile = True
                        selectingAction = False

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
                                    tile.selectable = True
                                    for atkTile in findTilesInAttackRange(tile, currentUnit.attackRange):
                                        if atkTile not in tilesInRange:
                                            atkTile.attackable = True
                            selectingTile = True
                        elif currentUnit != None and currentUnit in enemyUnits:
                            tilesInRange = findTilesInMovRange(currentUnit)
                            for tile in tilesInRange:
                                if tile.currentUnit == None:
                                    tile.selectable = True
                                    for atkTile in findTilesInAttackRange(tile, currentUnit.attackRange):
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
                        
    if attacking:
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
            ## unit will miss, play miss animation
            else:
                if currentUnit.combatAnimation.draw(screen, 0, 0, False):
                    print("current unit miss")
                    currentUnitAttacking = False
            myCombatUI.draw(screen, myBattleForcast)

        elif defendingUnitAttacking:
            if defendingUnit.hp > 0:
                screen.blit(combatUnit1, (0, 0))
                if myBattleForcast.defendingUnitCanCounter:
                    if myBattleForcast.defendingUnitWillHit:
                        if defendingUnit.combatAnimation.draw(screen, 0, 0, True):
                            # remove health
                            currentUnit.hp -= myBattleForcast.defendingUnitDmg
                            defendingUnitAttacking = False
                            print("defending unit hit")
                            if currentUnit.hp <= 0:
                                if currentUnit in playerUnits:
                                    playerUnits.remove(currentUnit)
                                elif currentUnit in enemyUnits:
                                    enemyUnits.remove(currentUnit)
                                map1.tiles[currentUnit.X][currentUnit.Y].currentUnit = None
                    ## unit will miss, play miss animation
                    else:
                        if defendingUnit.combatAnimation.draw(screen, 0, 0, True):
                            print("defending unit miss")
                            defendingUnitAttacking = False
                else:
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
                map1.tiles[defendingUnit.X][defendingUnit.Y].currentUnit = None
            myCombatUI.draw(screen, myBattleForcast)


        else:
            currentUnitAttacking = True
            defendingUnitAttacking = True
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
        screen.fill((0,0,0))
        map1.draw(screen)
        mainCursor.draw(screen)
        for unit in playerUnits:
            unit.draw(screen)
        for enemy in enemyUnits:
            enemy.draw(screen)
        
        myMapUnitUI.draw(screen)
        if selectingAttack:
            myBattleForcast.draw(screen)

        elif selectingAction:
            screen.blit(menuCursor, (gameWidth-350, 200+(165*menuSelectionIndex)))
            Y = 200
            if "attack" in menuOptions:
                screen.blit(attackButton, (gameWidth - 300, Y))
                Y+= 165
            if "wait" in menuOptions:
                screen.blit(waitButton, (gameWidth - 300, Y))
        
        elif viewingUnitInfo:
            myUnitInfo.draw(screen)
                
    pygame.display.update()
    pygame.time.delay(60)
