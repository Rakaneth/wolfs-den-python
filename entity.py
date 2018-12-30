import tcod
import parsers


class Entity:
    counter = 1

    def __init__(self,
                 name='No name',
                 desc='No desc',
                 glyph=ord('@'),
                 color=tcod.white,
                 blocks=False,
                 layer=1,
                 tags=None):
        self.name = name
        self.desc = desc
        self.glyph = glyph
        self.color = color
        self.blocks = blocks
        self.x = 0
        self.y = 0
        self.stats = {}
        self.id = Entity.counter
        self.tags = [] if tags is None else tags
        self.layer = layer
        self.map_id = 'None'
        Entity.counter += 1

    def get_bonus(self, stat):
        return int(self.get_stat(stat) / 10)

    @property
    def atp(self):
        return self.get_stat('atp') + self.get_stat('skl')

    @property
    def dfp(self):
        return self.get_stat('dfp') + self.get_stat('spd')

    @property
    def dmg(self):
        return self.get_stat('dmg') + self.get_bonus('str')

    @property
    def res(self):
        return self.get_stat('res') + self.get_stat('sag')

    @property
    def tou(self):
        return self.get_stat('res') + self.get_stat('stam')

    @property
    def wil(self):
        return self.get_stat('wil') + self.get_stat('sag')

    @property
    def pwr(self):
        return self.get_stat('pwr') + self.get_stat('smt')

    def move(self, x, y):
        self.x, self.y = x, y

    def get_stat(self, stat):
        return self.stats.get(stat, 0)

    def set_stat(self, stat, val):
        self.stats[stat] = val

    def __str__(self):
        statline = ''
        if len(self.stats) > 0:
            for stat, val in self.stats.items():
                statline += f'{stat}: {val} '
        else:
            statline = 'No statline.'
        return (f'{chr(self.glyph)} {self.name} (ID: {self.id})\n'
                f'{self.desc}\n'
                f'{statline}\n'
                f'Tags: {self.tags}')


class Creature(Entity):
    def __init__(self,
                 name='No name',
                 desc='No desc',
                 color=tcod.white,
                 stats=dict(),
                 glyph=ord('@'),
                 ai='hunt',
                 player=False,
                 tags=None):
        Entity.__init__(
            self,
            name=name,
            desc=desc,
            glyph=glyph,
            color=color,
            layer=2 if player else 3,
            tags=tags)
        self.inventory = []
        self.effect_list = []
        self.edr_mult = 2.0
        self.stats = stats

    def get_stat(self, stat):
        base = self.stats.get(stat, 0)
        for eff in self.effect_list:
            base += eff.get_stat(stat)
        for eqp in [i for i in self.inventory if i.equipped]:
            base += eqp.get_stat(stat)
        return base

    @property
    def max_vit(self):
        return self.get_stat('stam')

    @property
    def max_edr(self):
        return int(self.get_stat('stam') * self.edr_mult)

    def change_vit(self, val):
        self.set_stat('vit', min(self.get_stat('vit') + val, self.max_vit))

    def change_edr(self, val):
        self.set_stat('edr', min(self.get_stat('edr') + val, self.max_edr))


class Equipment(Entity):
    def __init__(self,
                 name='No name',
                 desc='No desc',
                 color=tcod.white,
                 stats=dict(),
                 glyph=ord('x'),
                 slot='trinket',
                 hardness=5,
                 tags=None):
        Entity.__init__(
            self, name=name, desc=desc, glyph=glyph, color=color, tags=tags)
        self.stats = stats
        self.equipped = False
        self.slot = slot
        self.hardness = hardness
        self.damage_type = None


class Item(Entity):
    def __init__(self,
                 name='No name',
                 desc='No desc',
                 glyph=ord('x'),
                 color=tcod.white,
                 amt=0.0,
                 flat=False,
                 typ='healing',
                 uses=1,
                 tags=None):
        Entity.__init__(
            self, name=name, desc=desc, glyph=glyph, color=color, tags=tags)
        self.amt = amt
        self.flat = flat
        self.type = typ
        self.uses = uses

    def use(self, user: Creature):
        if self.type == 'healing':
            func = user.change_vit
            base = user.max_vit
        else:
            func = user.change_edr
            base = user.max_edr

        amt = self.amt if self.flat else int(self.amt * base)
        func(amt)
        self.uses -= 1
