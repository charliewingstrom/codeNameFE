from consumable import Consumable

class Estus(Consumable):

    def __init__(self):
        super().__init__()
        self.name = "Estus"

    def consume(self, unit):
        unit.hp = min(unit.maxHp, unit.hp + 10)