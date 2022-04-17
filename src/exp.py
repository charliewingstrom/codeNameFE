import pygame 
import random
from assetLoader import AssetLoader
from unit        import Stat

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
        self.currUnit       = None
        self.delay          = 5
        self.levelIndex     = 0

        # for drawing the animation
        # once the value is true, a "+ 1" will be displayed next to the stat
        self.hasLeveledStat = {Stat.MAX_HP : False, Stat.STR : False, Stat.DEF : False, Stat.SPD : False, 
                                Stat.SKL: False, Stat.LCK : False }
        self.statsLeveled   = []
        self.levelUpUI      = AssetLoader.assets["levelUp.png"]
        self.X              = (gameWidth/2)-(self.levelUpUI.get_width()/2)
        self.Y              = (gameHeight/2)-(self.levelUpUI.get_height()/2)
    
    # get the stats to level up before drawing the level up screen/animation
    def roll(self, unit):
        self.currUnit = unit
        for stat in self.hasLeveledStat.keys():
            self.hasLeveledStat[stat] = False

        self.statsLeveled = []
        for stat, growth in self.currUnit.getGrowths().items():
            if growth > random.randint(0, 99):
                self.statsLeveled.append(stat)


    def getHasLeveled(self, index):
        if self.hasLeveledStat[index]:
            return " += 1"
        else:
            return ""

    def draw(self, screen, font):
        if self.currUnit != None:
            screen.blit(self.levelUpUI, (self.X, self.Y))

            hpT = font.render(str(self.currUnit.getStat(Stat.MAX_HP))+self.getHasLeveled(Stat.MAX_HP), True, (0,0,0))
            hpR = hpT.get_rect()
            hpR.topleft = (self.X+380, self.Y+370)

            strT = font.render(str(self.currUnit.getStat(Stat.STR))+self.getHasLeveled(Stat.STR), True, (0,0,0))
            strR = hpT.get_rect()
            strR.topleft = (self.X+380, self.Y+520)

            defT = font.render(str(self.currUnit.getStat(Stat.DEF))+self.getHasLeveled(Stat.DEF), True, (0,0,0))
            defR = hpT.get_rect()
            defR.topleft = (self.X+380, self.Y+670)

            spdT = font.render(str(self.currUnit.getStat(Stat.SPD))+self.getHasLeveled(Stat.SPD), True, (0,0,0))
            spdR = hpT.get_rect()
            spdR.topleft = (self.X+380, self.Y+820)

            sklT = font.render(str(self.currUnit.getStat(Stat.SKL))+self.getHasLeveled(Stat.SKL), True, (0,0,0))
            sklR = hpT.get_rect()
            sklR.topleft = (self.X+900, self.Y+370)

            lckT = font.render(str(self.currUnit.getStat(Stat.LCK))+self.getHasLeveled(Stat.LCK), True, (0,0,0))
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
                # reset
                if self.levelIndex > len(self.statsLeveled):
                    self.levelIndex = 0
                    self.delay = 5
                    self.currUnit = None
                    return True

                # we are finished, but let the user see the result before resetting
                elif self.levelIndex == len(self.statsLeveled):
                    self.levelIndex+=1
                    self.delay = 10

                else:
                    self.delay = 5
                    statToLevelUp = self.statsLeveled[self.levelIndex]
                    self.currUnit.addToStat(statToLevelUp, 1)
                    self.hasLeveledStat[statToLevelUp]  = True
                    self.levelIndex+=1
        return False