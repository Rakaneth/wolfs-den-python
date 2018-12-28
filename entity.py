import tcod
import parsers


class Entity:
    counter = 1

    @staticmethod
    def creature_from_template(buildID):
        temp = parsers.CREATURE_TEMPLATES.get(buildID)
        assert temp, f'BuildID {buildID} not in creature templates'
        foetus = Entity(
            name=temp.name,
            desc=temp.desc,
            glyph=temp.glyph,
            color=temp.color,
            blocks=True,
            layer=2)
        foetus.stats = temp.stats
        foetus.tags = temp.tags
        return foetus

    @staticmethod
    def equip_from_template(buildID, matID=None):
        temp = parsers.EQ_TEMPLATES.get(buildID)
        if matID:
            mat = parsers.MATERIAL_TEMPLATES.get(matID)
        else:
            mat = None
        assert temp, f'BuildID {buildID} not in equip templates'
        mould = Entity(
            name=temp.name,
            desc=temp.desc,
            glyph=temp.glyph,
            color=temp.color,
            blocks=False,
            layer=1)

        mould.stats = temp.stats
        mould.damage_type = temp.damage_type

        if temp.material:
            str_material = '<material>'
            assert matID, f'{temp.name} must be made of a material, none given'
            assert mat, f'{matID} not in material templates'
            mould.name.replace(str_material, mat.name)
            mould.desc.replace(str_material, mat.name)
            mould.color = mat.color
            stat_set = getattr(mat, temp.equip_type)
            mould.hardness = mat.hardness

            for k, v in stat_set.items():
                mould.set_stat(k, mould.get_stat(k) + v)

    def __init__(self,
                 name='No name',
                 desc='No desc',
                 glyph=ord('@'),
                 color=tcod.white,
                 blocks=False,
                 layer=1):
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
        self.tags = []
        self.layer = layer
        self.hardess = 5
        self.damage_type = None
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
                f'{statline}\n'
                f'Tags: {self.tags}')
