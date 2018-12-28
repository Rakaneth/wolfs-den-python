import tcod


class Entity:
    counter = 1

    def __init__(self,
                 name='No name',
                 desc='No desc',
                 glyph=ord('@'),
                 color=tcod.white,
                 blocks=False):
        self.name = name
        self.desc = desc
        self.glyph = glyph
        self.color = color
        self.blocks = blocks
        self.x = 0
        self.y = 0
        self.stats = {}
        self.inventory = []
        self.ai = None
        self.effect_list = []
        self.id = Entity.counter
        self.equipped = False
        self.eq_slot = None
        Entity.counter += 1

    def move(self, x, y):
        self.x, self.y = x, y

    def get_stat(self, stat):
        base = self.stats.get(stat, 0)
        for eff in self.effect_list:
            base += eff.get_stat(stat)
        for eqp in [i for i in self.inventory if i.equipped]:
            base += eqp.get_stat(stat)
        return base

    def set_stat(self, stat, val):
        self.stats[stat] = val

    def __str__(self):
        statline = ''
        if len(self.stats) > 0:
            for stat, val in self.stats.items():
                statline += f'{stat}: {val} '
        else:
            statline = 'No statline.'
        return (f'{chr(self.glyph)} {self.name}\n'
                f'{self.desc}\n'
                f'{statline}\n')
