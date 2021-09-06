import pygame
from pathlib import Path
import random

mainMenuPic = pygame.image.load(Path(__file__).parent / "../assets/main-menu.png")
battleForecastPic = pygame.image.load(Path(__file__).parent / "../assets/battle-forecast.png")

combatUI = pygame.image.load(Path(__file__).parent / "../assets/Combat-UI.png")
combatUIRed = pygame.image.load(Path(__file__).parent / "../assets/Combat-UI-red.png")
healthbarfullPiece = pygame.image.load(Path(__file__).parent / "../assets/healthbar-piece.png")
healthbarEmptyPiece = pygame.image.load(Path(__file__).parent / "../assets/healthbar-piece-empty.png")

mapUnitUI = pygame.image.load(Path(__file__).parent / "../assets/map-unit-UI.png")

unitInfoPic = pygame.image.load(Path(__file__).parent / "../assets/unit-info.png")

class MainMenu():

    def draw(self, screen):
        screen.blit(mainMenuPic, (0,0))

class BattleForcast():

    def __init__(self, gameWidth):
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

    def calculate(self, attackingUnit, defendingUnit, findTilesInAttackRange, map1):
        ## need to check if defendingUnit is in range to counter attack
        self.defendingUnitCanCounter = False
        for tile in findTilesInAttackRange(map1.tiles[defendingUnit.X][defendingUnit.Y], defendingUnit.getAttackRange()):
            if tile.currentUnit == attackingUnit:
                self.defendingUnitCanCounter = True
        

        #TODO calculate crit
        self.attackingUnitDmg = max(0, (attackingUnit.attack + attackingUnit.getEquippedWeapon().might) - defendingUnit.defense)
        self.attackingUnitHit = min(100, int((attackingUnit.getEquippedWeapon().hit + (attackingUnit.skill * 2) + attackingUnit.luck / 2) - ((defendingUnit.speed * 2) + defendingUnit.luck)))
        self.defendingUnitCrit = 0
        if self.defendingUnitCanCounter:
            self.defendingUnitDmg = max(0, (defendingUnit.attack + defendingUnit.getEquippedWeapon().might) - attackingUnit.defense)
            self.defendingUnitHit = min(100, int((defendingUnit.getEquippedWeapon().hit + (defendingUnit.skill * 2) + defendingUnit.luck / 2) - ((attackingUnit.speed * 2) + attackingUnit.luck)))
            self.defendingUnitCrit = 0
        else:
            self.defendingUnitDmg = "-"
            self.defendingUnitHit = "-"
            self.defendingUnitCrit = "-"

            
    def roll(self):
        if random.randint(0, 100) <= self.attackingUnitHit:
            self.attackingUnitWillHit = True
        else:
            self.attackingUnitWillHit = False
        if self.defendingUnitCanCounter:
            if random.randint(0, 100) <= self.defendingUnitHit:
                self.defendingUnitWillHit = True
            else:
                self.defendingUnitWillHit = False

    def draw(self, screen, font, currentUnit, defendingUnit):
        if currentUnit and defendingUnit:
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

            eHpText = font.render(str(defendingUnit.hp), True, (0,0,0))
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

    def __init__(self, X, Y, font):
        self.X = X
        self.Y = Y
        self.__font = font
        self.pic = combatUI
        self.enemyPic = combatUIRed
        
    def draw(self, screen, battleForcast, currentUnit, defendingUnit):
        DUOffset = 1075
        screen.blit(self.pic, (self.X, self.Y))
        screen.blit(self.pic, (self.X + DUOffset, self.Y))
        if currentUnit.hp > 0:
            CUNameText = self.__font.render(currentUnit.name, True, (0,0,0))
            CUNameRect = CUNameText.get_rect()
            CUNameRect.center = (self.X + (len(currentUnit.name) * 25), self.Y + 100)

            CUAttackText = self.__font.render(str(battleForcast.attackingUnitDmg), True, (0,0,0))
            CUAttackRect = CUAttackText.get_rect()
            CUAttackRect.center = (self.X + 185, self.Y + 330)

            CUHitText = self.__font.render(str(battleForcast.attackingUnitHit), True, (0,0,0))
            CUHitRect = CUHitText.get_rect()
            CUHitRect.center = (self.X + 450, self.Y + 330)

            CUCritText = self.__font.render(str(battleForcast.attackingUnitCrit), True, (0,0,0))
            CUCritRect = CUCritText.get_rect()
            CUCritRect.center = (self.X + 720, self.Y + 330)

            for i in range(currentUnit.maxHp):
                screen.blit(healthbarEmptyPiece, (self.X + 50 + (20*i), self.Y + 140))
            for i in range(currentUnit.hp):
                screen.blit(healthbarfullPiece, (self.X + 50 + (20*i), self.Y + 140))
                
            screen.blit(CUNameText, CUNameRect)
            screen.blit(CUAttackText, CUAttackRect)
            screen.blit(CUHitText, CUHitRect)
            screen.blit(CUCritText, CUCritRect)
            
        if defendingUnit and defendingUnit.hp > 0:
            ## defending unit stuff
            DUNameText = self.__font.render(defendingUnit.name, True, (0,0,0))
            DUNameRect = DUNameText.get_rect()
            DUNameRect.center = (self.X + DUOffset + (len(defendingUnit.name) * 25), self.Y + 100)

            DUAttackText = self.__font.render(str(battleForcast.defendingUnitDmg), True, (0,0,0))
            DUAttackRect = DUAttackText.get_rect()
            DUAttackRect.center = (self.X + DUOffset + 185, self.Y + 330)

            DUHitText = self.__font.render(str(battleForcast.defendingUnitHit), True, (0,0,0))
            DUHitRect = DUHitText.get_rect()
            DUHitRect.center = (self.X + DUOffset + 450, self.Y + 330)

            DUCritText = self.__font.render(str(battleForcast.defendingUnitCrit), True, (0,0,0))
            DUCritRect = DUCritText.get_rect()
            DUCritRect.center = (self.X + 720 + DUOffset, self.Y + 330)

            for i in range(defendingUnit.maxHp):
                screen.blit(healthbarEmptyPiece, (self.X + 50 + (20*i) + DUOffset, self.Y + 140))
            for i in range(defendingUnit.hp):
                screen.blit(healthbarfullPiece, (self.X + 50 + (20*i) + DUOffset, self.Y + 140))

            screen.blit(DUNameText, DUNameRect)
            screen.blit(DUAttackText, DUAttackRect)
            screen.blit(DUHitText, DUHitRect)
            screen.blit(DUCritText, DUCritRect)

class MapUnitUI():

    def __init__(self, gameWidth, gameHeight):
        self.X = gameWidth - 460
        self.Y = gameHeight - 280
        self.pic = mapUnitUI
        self.currUnit = None
    
    def reset(self, unit):
        self.currUnit = unit

    def draw(self, screen, font):
        if self.currUnit != None:
            screen.blit(self.pic, (self.X, self.Y))

            nameT = font.render(self.currUnit.name, True, (0,0,0))
            nameR = nameT.get_rect()
            nameR.center = (self.X + 21*len(self.currUnit.name), self.Y + 50)

            hpT = font.render(str(self.currUnit.hp) + " /", True, (0,0,0))
            hpR = hpT.get_rect()
            hpR.center = (self.X + 70, self.Y + 150)

            mHpT = font.render(str(self.currUnit.maxHp), True, (0,0,0))
            mHpR = mHpT.get_rect()
            mHpR.center = (self.X + 150, self.Y + 150)



            screen.blit(nameT, nameR)
            screen.blit(hpT, hpR)
            screen.blit(mHpT, mHpR)


class UnitInfo():

    def __init__(self):
        self.pic = unitInfoPic
        self.currUnit = None
    def reset(self, unit):
        self.currUnit = unit

    def draw(self, screen, font):
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

        Yoffset = 100
        for item in self.currUnit.getInventory():
            itemT = font.render(item.name, True, (0,0,0))
            itemR = itemT.get_rect()
            itemR.center = (1600, Yoffset)
            screen.blit(itemT, itemR)
            Yoffset += 100