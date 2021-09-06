from pathlib import Path
import pygame 
import random

levelUpUI = pygame.image.load(Path(__file__).parent / "../assets/levelUp.png") 


class Exp():

    def __init__(self):
        self.currUnit = None
        self.expToAdd = 0

    def setup(self, unit, exp):
        self.currUnit = unit
        self.expToAdd = exp
        self.delay = 10

    def draw(self, screen, gameWidth):
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
    def __init__(self, gameWidth, gameHeight):
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

    def draw(self, screen, font):
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