from enum   import Enum, auto
from exp    import Exp, LevelUp
from ui     import CombatUI

class atkStates(Enum):

    currentUnitAttacking = auto()
    defendingUnitAttacking = auto()

    currentUnitDoubling = auto()
    defendingUnitDoubling = auto()

    finishedAttacking = auto()
    addingExp = auto()
    levelingUp = auto()


class CombatManager():

    def __init__(self, screen, gameWidth, gameHeight, font):
        self.__screen           = screen
        self.__state            = atkStates.currentUnitAttacking
        self.__attackingUnit    = None
        self.__defendingUnit    = None
        self.__battleForcast    = None 
        self.__exp              = 0
        self.__expManager       = Exp()
        self.__gameWidth        = gameWidth
        self.__levelUp          = LevelUp(gameWidth, gameHeight)
        self.__combatUI         = CombatUI(0, gameHeight - 385, font)

    # Used to setup the usage of this class
    # This is an extention of the constructor considering the class can't be used without it
    def setupAttack(self, attackingUnit, defendingUnit, battleForcast, attackingUnitIsPlayer):
        self.__attackingUnit            = attackingUnit
        self.__defendingUnit            = defendingUnit
        self.__battleForcast            = battleForcast
        self.__attackingUnitIsPlayer    = attackingUnitIsPlayer
        self.__runningUnit              = self.__attackingUnit
        self.__standingUnit             = self.__defendingUnit

        ## when miss animations are added in, this needs to be an if based on whether the runningUnit will hit
        self.__runningAction            = self.__runningUnit.combatAnimation.draw 
        self.__dmg                      = self.__battleForcast.attackingUnitDmg
        self.__willHit                  = self.__battleForcast.attackingUnitWillHit
        self.__state                    = atkStates.currentUnitAttacking
        self.__exp                      = 0

    # public function for running the sequence
    # returns true if finished
    def runSequence(self):
        if self.__run():
            self.__moveToNextState()

        self.__combatUI.draw(self.__screen, self.__battleForcast, self.__attackingUnit, self.__defendingUnit)
        return self.__state == atkStates.finishedAttacking
        
    def getExp(self):
        return self.__exp
        
    ## Handles the running of an attack action
    def __run(self):
        actionFinished = False
        # check if runningUnit will hit
        if self.__willHit:
            # play hit animation
            if self.__runningAction(self.__screen, 0, 0, self.__runningUnit != self.__attackingUnit):
                actionFinished = True
                self.__standingUnit.hp -= self.__dmg
                if self.__attackingUnitIsPlayer:
                    self.__exp += self.__dmg
                    # standingUnitDied
                    if self.__standingUnit.hp <= 0:
                        self.__exp += 30
            
            ## TODO may need to play "finishing" animation here
        else:
            # play miss animation
            if self.__runningAction(self.__screen, 0, 0, self.__runningUnit != self.__attackingUnit):
                actionFinished = True
                if self.__attackingUnitIsPlayer:
                    self.__exp += 2

        return actionFinished

    ## Handles the transitions between attack actions
    def __moveToNextState(self):
        ## Order of operations
        ##      currentUnitAttacking
        ##      defendingUnitAttacking (if they can)
        ##      finishedAttacking
        if self.__state == atkStates.currentUnitAttacking:
            if self.__defendingUnit.hp <= 0:
                self.__state = atkStates.finishedAttacking
            else:
                self.__state                    = atkStates.defendingUnitAttacking
                self.__runningUnit              = self.__defendingUnit
                self.__standingUnit             = self.__attackingUnit
                self.__runningAction            = self.__runningUnit.combatAnimation.draw
                self.__dmg                      = self.__battleForcast.defendingUnitDmg
                self.__willHit                  = self.__battleForcast.defendingUnitCanCounter and self.__battleForcast.defendingUnitWillHit
                self.__attackingUnitIsPlayer    = not self.__attackingUnitIsPlayer

        elif self.__state == atkStates.defendingUnitAttacking:
            ## TODO Check for doubling here
            if False:
                pass
            else:
                self.__state = atkStates.finishedAttacking
        
    # Returns true if user needs to move to the next state
    def __addExp(self):
        if self.__expManager.currUnit.exp >= 100:
            return True
        else:
            return self.__expManager.draw(self.__screen, self.__gameWidth)



        
        
