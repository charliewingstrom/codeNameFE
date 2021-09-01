from enum import Enum, auto

class atkStates(Enum):

    currentUnitAttacking = auto()
    defendingUnitAttacking = auto()

    currentUnitDoubling = auto()
    defendingUnitDoubling = auto()

    finishedAttacking = auto()
    addingExp = auto()
    levelingUp = auto()


class CombatManager():

    def __init__(self, screen):
        self.__screen           = screen
        self.__state            = atkStates.currentUnitAttacking
        self.__attackingUnit    = None
        self.__defendingUnit    = None
        self.__battleForcast    = None 
        self.__exp              = 0

    def setupAttack(self, attackingUnit, defendingUnit, battleForcast, attackingUnitIsPlayer):
        self.__attackingUnit            = attackingUnit
        self.__defendingUnit            = defendingUnit
        self.__battleForcast            = battleForcast
        self.__exp                      = 0
        self.__attackingUnitIsPlayer    = attackingUnitIsPlayer
        self.__runningUnit              = self.__attackingUnit
        self.__standingUnit             = self.__defendingUnit

        ## when miss animations are added in, this needs to be an if based on whether the runningUnit will hit
        self.__runningAction            = self.__runningUnit.combatAnimation.draw 
        self.__dmg                      = self.__battleForcast.attackingUnitDmg
        self.__willHit                  = self.__battleForcast.attackingUnitWillHit

    def runSequence(self):
        while(self.__state!=atkStates.finishedAttacking):
            if self.__run():
                self.__moveToNextState()
        


    def __run(self):
        finishedAttacking = False
        # check if runningUnit will hit
        if self.__willHit:
            # play hit animation
            if self.__runningAction(self.__screen, 0, 0, self.__runningUnit != self.__attackingUnit):
                finishedAttacking = True
                self.__standingUnit.hp -= self.__dmg
                if self.__attackingUnitIsPlayer:
                    self.__exp += self.__dmg
        else:
            # play miss animation
            if self.__runningAction(self.__screen, 0, 0, self.__runningUnit != self.__attackingUnit):
                finishedAttacking = True
                if self.__attackingUnitIsPlayer:
                    self.__exp += 2

        return finishedAttacking

        
    def __moveToNextState(self):
        ## TODO finish this
        ## Need to add doubling into this
        if self.__state == atkStates.currentUnitAttacking:
            if self.__defendingUnit.hp <= 0:
                self.__state = atkStates.finishedAttacking
            else:
                self.__state = atkStates.defendingUnitAttacking
            self.__runningUnit = self.__defendingUnit
            self.__standingUnit = self.__attackingUnit
            self.__dmg          = self.__battleForcast.defendingUnitDmg
            self.__willHit = self.__battleForcast.defendingUnitWillHit

        elif self.__state == atkStates.defendingUnitAttacking:
            self.__state = atkStates.finishedAttacking

        
        
