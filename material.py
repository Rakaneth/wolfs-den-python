import tcod


class Material:
    def __init__(self):
        self.name = 'No Name'
        self.color = tcod.white
        self.hardness = 0
        self.sword = {}
        self.axe = {}
        self.hammer = {}
        self.staff = {}
        self.rapier = {}
        self.armor = {}
        self.frequency = 0
