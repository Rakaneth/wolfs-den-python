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

    def __str__(self):
        return (f'---\nName: {self.name}\n'
                f'Color: {self.color}\n'
                f'Hardness: {self.hardness}\n'
                f'Frequency: {self.frequency}\n'
                f'Sword Stats: {self.sword}\n'
                f'Hammer Stats: {self.hammer}\n'
                f'Rapier Stats: {self.rapier}\n'
                f'Axe Stats: {self.axe}\n'
                f'Armor Stats: {self.armor}\n'
                f'Staff Stats: {self.staff}')
