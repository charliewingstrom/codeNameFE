from weapon import weapon

class javelin(weapon):

    def __init__(self):
        super().__init__()
        self.range = 2
    def __str__(self):
        return "Javelin"