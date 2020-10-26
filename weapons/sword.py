from weapon import weapon

class sword(weapon):

    def __init__(self):
        super().__init__()
        self.strength = 4 
        self.hit = 70
        self.crit = 3

    def __str__(self):
        return "sword"