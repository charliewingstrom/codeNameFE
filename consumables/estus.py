from consumable import Consumable

class Estus(Consumable):

    def __init__(self):
        super().__init__()
        self.name = "Estus"

    def consume(self, unit):
        self.unit.hp = min(self.unit.maxHp, self.unit.hp + 10)