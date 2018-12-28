import tcod
from material import Material

CREATURE_TEMPLATES = {}
ITEM_TEMPLATES = {}
EQ_TEMPLATES = {}
MATERIAL_TEMPLATES = {}
MAP_TEMPLATES = {}


class TempBase:
    def __init__(self):
        self.name = 'No name'
        self.desc = 'No desc'
        self.type = 'No type'
        self.color = tcod.white
        self.glyph = ord('@')
        self.tags = []
        self.frequency = 0


class CreatureTemplate(TempBase):
    def __init__(self):
        TempBase.__init__(self)
        self.stats = dict(str=10, stam=10, spd=10, skl=10, sag=10, smt=10)
        self.unarmed = 'hands'
        self.start_items = []

    def __str__(self):
        return ('---\n'
                f'{chr(self.glyph)} {self.name} - {self.type}\n'
                f'{self.desc}\n'
                f'Freq: {self.frequency}\n')

    def __repr__(self):
        return f'{chr(self.glyph)} {self.name} - {self.type}'


class EquipTemplate(TempBase):
    def __init__(self):
        TempBase.__init__(self)
        self.stats = dict()
        self.slot = None
        self.material = False
        self.damageType = None
        self.equipType = None


class ItemTemplate(TempBase):
    def __init__(self):
        TempBase.__init__(self)
        self.amt = 0.0


class MapTemplate:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.connections = {}
        self.name = 'No name'
        self.light = True
        self.gen_type = 'caves'


class CreatureParser:
    def __init__(self):
        self.temp = CreatureTemplate()

    def new_struct(self, struct, name):
        if tcod.struct_get_name(struct) == 'creature':
            print(f'Parsing creature: {name}')
            self.temp = CreatureTemplate()
        return True

    def new_flag(self, name):
        return True

    def new_property(self, name, typ, value):
        stat_names = ['str', 'stam', 'spd', 'skl', 'sag', 'smt']
        if name == 'name':
            self.temp.name = value
        elif name == 'type':
            self.temp.type = value
        elif name == 'desc':
            self.temp.desc = value
        elif name == 'unarmed':
            self.temp.unarmed = value
        elif name == 'glyph':
            if isinstance(value, str):
                self.temp.glyph = ord(value)
            else:
                self.temp.glyph = value
        elif name in stat_names:
            self.temp.stats[name] = value
        elif name == 'col':
            self.temp.color = value
        elif name == 'tags':
            self.temp.tags = value
        elif name == 'startItems':
            self.temp.start_items = value
        return True

    def end_struct(self, struct, name):
        if tcod.struct_get_name(struct) == 'creature':
            CREATURE_TEMPLATES[name] = self.temp
        return True

    def error(self, msg):
        print(f'Error parsing creature file: {msg}')
        return False


class ItemParser:
    def __init__(self):
        self.temp = None


class EquipParser:
    def __init__(self):
        self.temp = None


class MaterialParser:
    def __init__(self):
        self.temp = None


class MapParser:
    def __init__(self):
        self.temp = None


def parse_creatures(filename):
    parser = tcod.parser_new()
    creature = tcod.parser_new_struct(parser, b'creature')
    stats = tcod.parser_new_struct(parser, b'stats')
    tcod.struct_add_structure(creature, stats)
    tcod.struct_add_property(creature, b'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(creature, b'type', tcod.TYPE_STRING, True)
    tcod.struct_add_property(creature, b'desc', tcod.TYPE_STRING, True)
    tcod.struct_add_property(creature, b'unarmed', tcod.TYPE_STRING, False)
    tcod.struct_add_property(creature, b'glyph', tcod.TYPE_CHAR, True)
    tcod.struct_add_property(creature, b'col', tcod.TYPE_COLOR, False)
    tcod.struct_add_property(stats, b'str', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'stam', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'skl', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'spd', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'sag', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'smt', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'vision', tcod.TYPE_INT, False)
    tcod.struct_add_list_property(creature, b'tags', tcod.TYPE_STRING, True)
    tcod.struct_add_list_property(creature, b'startItems', tcod.TYPE_STRING,
                                  False)
    tcod.parser_run(parser, filename, CreatureParser())
    tcod.parser_delete(parser)


def parse_items(filename):
    parser = tcod.parser_new()
    item = tcod.parser_new_struct(parser, 'item')
    tcod.struct_add_property(item, 'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(item, 'type', tcod.TYPE_STRING, True)
    tcod.struct_add_property(item, 'desc', tcod.TYPE_STRING, True)
    tcod.struct_add_property(item, 'glyph', tcod.TYPE_CHAR, True)
    tcod.struct_add_property(item, 'col', tcod.TYPE_COLOR, False)
    tcod.struct_add_property(item, 'frequency', tcod.TYPE_INT, False)
    tcod.struct_add_property(item, 'amt', tcod.TYPE_FLOAT, True)
    tcod.struct_add_list_property(item, 'tags', tcod.TYPE_STRING, True)
    tcod.parser_run(parser, filename, ItemParser())
    tcod.parser_delete(parser)


def parse_equip(filename):
    parser = tcod.parser_new()
    equip = tcod.parser_new_struct(parser, 'equip')
    stats = tcod.parser_new_struct(parser, 'stats')
    tcod.struct_add_structure(equip, stats)
    tcod.struct_add_property(equip, 'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(equip, 'type', tcod.TYPE_STRING, True)
    tcod.struct_add_property(equip, 'desc', tcod.TYPE_STRING, True)
    tcod.struct_add_property(equip, 'glyph', tcod.TYPE_CHAR, True)
    tcod.struct_add_property(equip, 'col', tcod.TYPE_COLOR, False)
    tcod.struct_add_property(equip, 'frequency', tcod.TYPE_INT, False)
    tcod.struct_add_property(equip, 'damageType', tcod.TYPE_STRING, False)
    tcod.struct_add_property(equip, 'equipType', tcod.TYPE_STRING, False)
    tcod.struct_add_flag(equip, 'material')
    tcod.struct_add_property(stats, 'atp', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'dfp', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'dmg', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'res', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'tou', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'wil', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'pwr', tcod.TYPE_INT, False)
    tcod.struct_add_list_property(equip, 'tags', tcod.TYPE_STRING, True)
    tcod.parser_run(parser, filename, EquipParser())
    tcod.parser_delete(parser)


def parse_materials(filename):
    parser = tcod.parser_new()
    mat = tcod.parser_new_struct(parser, 'material')
    stats = tcod.parser_new_struct(parser, 'stats')
    tcod.struct_add_structure(mat, stats)
    tcod.struct_add_property(mat, 'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(mat, 'col', tcod.TYPE_COLOR, False)
    tcod.struct_add_property(mat, 'hardness', tcod.TYPE_INT, True)
    tcod.struct_add_property(mat, 'frequency', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'atp', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'dfp', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'dmg', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'res', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'tou', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'wil', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, 'pwr', tcod.TYPE_INT, False)
    tcod.parser_run(parser, filename, MaterialParser())
    tcod.parser_delete(parser)


def parse_maps(filename):
    parser = tcod.parser_new()
    m = tcod.parser_new_struct(parser, 'map')
    connex = tcod.parser_new_struct(parser, 'connections')
    tcod.struct_add_structure(m, connex)
    tcod.struct_add_flag(m, 'light')
    tcod.struct_add_property(m, 'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(m, 'genType', tcod.TYPE_STRING, True)
    tcod.struct_add_property(m, 'width', tcod.TYPE_INT, True)
    tcod.struct_add_property(m, 'height', tcod.TYPE_INT, True)
    tcod.struct_add_property(connex, 'id', tcod.TYPE_STRING, True)
    tcod.struct_add_property(connex, 'from', tcod.TYPE_STRING, False)
    tcod.struct_add_property(connex, 'to', tcod.TYPE_STRING, False)
    tcod.struct_add_flag(connex, 'twoWay')
    tcod.parser_run(parser, filename, MapParser())
    tcod.parser_delete(parser)