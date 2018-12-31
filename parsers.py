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
        self.glyph = ord('x')
        self.tags = []
        self.frequency = 0

    def __str__(self):
        return ('---\n'
                f'{chr(self.glyph)} {self.name} - {self.type}\n'
                f'{self.desc}\n'
                f'Freq: {self.frequency}\n'
                f'Color: {self.color}\n'
                f'Tags: {self.tags}\n')


class CreatureTemplate(TempBase):
    def __init__(self):
        TempBase.__init__(self)
        self.stats = dict(
            str=10, stam=10, spd=10, skl=10, sag=10, smt=10, vision=6)
        self.unarmed = 'hands'
        self.start_items = []

    def __str__(self):
        return (f'{TempBase.__str__(self)}'
                f'Stats: {self.stats}\n'
                f'Unarmed weapon: {self.unarmed}\n'
                f'Starting items: {self.start_items}\n')


class EquipTemplate(TempBase):
    def __init__(self):
        TempBase.__init__(self)
        self.stats = dict()
        self.slot = None
        self.material = False
        self.damage_type = None
        self.equip_type = None

    def __str__(self):
        return (f'{TempBase.__str__(self)}'
                f'Slot" {self.slot}\n'
                f'Stats: {self.stats}\n'
                f'Material: {self.material}\n'
                f'Damage Type: {self.damage_type}\n'
                f'Equip Type: {self.equip_type}')


class ItemTemplate(TempBase):
    def __init__(self):
        TempBase.__init__(self)
        self.amt = 0.0
        self.flat = False

    def __str__(self):
        return (f'{TempBase.__str__(self)}\n'
                f'Amount: {self.amt}\n'
                f'Flat: {self.flat}')


class MapTemplate:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.connections = []
        self.name = 'No name'
        self.light = False
        self.gen_type = 'caves'

    def __str__(self):
        return (f'---\n{self.name}\n'
                f'{self.width} x {self.height}\n'
                f'Generation: {self.gen_type}\n'
                f'{"" if self.light else "Not "}Lit\n'
                f'{self.connections}')


class BaseParser:
    def __init__(self, pID):
        self.pID = pID

    def error(self, msg):
        print(f'Error in parsing {self.pID} file: {msg}')
        return False


class CreatureParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self, 'creature')
        self.temp = CreatureTemplate()

    def new_struct(self, struct, name):
        if tcod.struct_get_name(struct) == 'creature':
            print(f'Parsing creature: {name}')
            self.temp = CreatureTemplate()
        return True

    def new_flag(self, name):
        return True

    def new_property(self, name, typ, value):
        stat_names = ['str', 'stam', 'spd', 'skl', 'sag', 'smt', 'vision']
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
            print(f'Adding {name} to creature templates')
            CREATURE_TEMPLATES[name] = self.temp
        return True


class ItemParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self, 'item')
        self.temp = ItemTemplate()

    def new_struct(self, struct, name):
        self.temp = ItemTemplate()
        return True

    def new_flag(self, name):
        if name == 'flat':
            self.temp.flat = True
        return True

    def new_property(self, name, typ, value):
        if name == 'name':
            self.temp.name = value
        elif name == 'type':
            self.temp.type = value
        elif name == 'desc':
            self.temp.desc = value
        elif name == 'glyph':
            if isinstance(value, str):
                self.temp.glyph = ord(value)
            else:
                self.temp.glyph = value
        elif name == 'col':
            self.temp.color = value
        elif name == 'tags':
            self.temp.tags = value
        elif name == 'frequency':
            self.temp.frequency = value
        elif name == 'amt':
            self.temp.amt = value
        elif name == 'type':
            self.temp.type = value
        return True

    def end_struct(self, struct, name):
        print(f'Adding {name} to item templates')
        ITEM_TEMPLATES[name] = self.temp
        return True


class EquipParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self, 'equipment')
        self.temp = EquipTemplate()

    def new_struct(self, struct, name):
        if tcod.struct_get_name(struct) == 'equip':
            print(f'New equip: {name}')
            self.temp = EquipTemplate()
        return True

    def new_flag(self, name):
        if name == 'material':
            self.temp.material = True
        return True

    def new_property(self, name, typ, value):
        stat_names = [
            'atp', 'dfp', 'dmg', 'tou', 'res', 'wil', 'pwr', 'vision'
        ]
        if name == 'name':
            self.temp.name = value
        elif name == 'desc':
            self.temp.desc = value
        elif name == 'col':
            self.temp.color = value
        elif name == 'tags':
            self.temp.tags = value
        elif name == 'glyph':
            if isinstance(value, str):
                self.temp.glyph = ord(value)
            else:
                self.temp.glyph = value
        elif name == 'frequency':
            self.temp.frequency = value
        elif name == 'equipType':
            self.temp.equip_type = value
            self.temp.type = value
        elif name == 'damageType':
            self.temp.damage_type = value
        elif name == 'slot':
            self.temp.slot = value
        elif name in stat_names:
            self.temp.stats[name] = value

        return True

    def end_struct(self, struct, name):
        if tcod.struct_get_name(struct) == 'equip':
            print(f'Adding {name} to equipment templates')
            EQ_TEMPLATES[name] = self.temp
        return True


class MaterialParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self, 'material')
        self.temp = Material()
        self.cur_stats = {}

    def new_struct(self, struct, name):
        if tcod.struct_get_name(struct) == 'material':
            print(f'New material: {name}')
            self.temp = Material()
        self.cur_stats = {}
        return True

    def new_flag(self, name):
        return True

    def new_property(self, name, typ, value):
        stat_names = ['atp', 'dfp', 'dmg', 'tou', 'res', 'wil', 'pwr']
        if name == 'name':
            self.temp.name = value
        elif name == 'frequency':
            self.temp.frequency = value
        elif name == 'col':
            self.temp.color = value
        elif name == 'hardness':
            self.temp.hardness = value
        elif name in stat_names:
            self.cur_stats[name] = value
        return True

    def end_struct(self, struct, name):
        cur_struct = tcod.struct_get_name(struct)
        if cur_struct == 'material':
            print(f'Adding {name} to material templates')
            MATERIAL_TEMPLATES[name] = self.temp
        elif cur_struct == 'stats':
            setattr(self.temp, name, self.cur_stats)
        return True


class MapParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self, 'map')
        self.temp = MapTemplate()
        self.cur_con = {}

    def new_struct(self, struct, name):
        if tcod.struct_get_name(struct) == 'map':
            print(f'New map: {name}')
            self.temp = MapTemplate()
        self.cur_con = {}
        return True

    def new_flag(self, name):
        if name == 'light':
            self.temp.light = True
        elif name == 'twoWay':
            self.cur_con['two_way'] = True
        return True

    def new_property(self, name, typ, value):
        conn_stats = ['id', 'from', 'to']
        if name == 'name':
            self.temp.name = value
        elif name == 'width':
            self.temp.width = value
        elif name == 'height':
            self.temp.height = value
        elif name == 'genType':
            self.temp.gen_type = value
        elif name in conn_stats:
            self.cur_con[name] = value
        return True

    def end_struct(self, struct, name):
        cur_struct = tcod.struct_get_name(struct)
        if cur_struct == 'map':
            print(f'Adding {name} to map templates')
            MAP_TEMPLATES[name] = self.temp
        elif cur_struct == 'connections':
            self.temp.connections.append(self.cur_con)
        return True


def parse_creatures(filename):
    parser = tcod.parser_new()
    creature = tcod.parser_new_struct(parser, b'creature')
    stats = tcod.parser_new_struct(parser, b'stats')
    tcod.struct_add_structure(creature, stats)
    tcod.struct_add_property(creature, b'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(creature, b'type', tcod.TYPE_STRING, True)
    tcod.struct_add_property(creature, b'desc', tcod.TYPE_STRING, True)
    tcod.struct_add_property(creature, b'unarmed', tcod.TYPE_STRING, False)
    tcod.struct_add_property(creature, b'glyph', tcod.TYPE_CHAR, False)
    tcod.struct_add_property(creature, b'col', tcod.TYPE_COLOR, False)
    tcod.struct_add_property(stats, b'str', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'stam', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'skl', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'spd', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'sag', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'smt', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'vision', tcod.TYPE_INT, False)
    tcod.struct_add_property(creature, b'frequency', tcod.TYPE_INT, False)
    tcod.struct_add_list_property(creature, b'tags', tcod.TYPE_STRING, True)
    tcod.struct_add_list_property(creature, b'startItems', tcod.TYPE_STRING,
                                  False)
    tcod.parser_run(parser, filename, CreatureParser())
    tcod.parser_delete(parser)
    print(f'{len(CREATURE_TEMPLATES)} creature templates added.')


def parse_items(filename):
    parser = tcod.parser_new()
    item = tcod.parser_new_struct(parser, b'item')
    tcod.struct_add_property(item, b'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(item, b'type', tcod.TYPE_STRING, True)
    tcod.struct_add_property(item, b'desc', tcod.TYPE_STRING, True)
    tcod.struct_add_property(item, b'glyph', tcod.TYPE_CHAR, False)
    tcod.struct_add_property(item, b'col', tcod.TYPE_COLOR, False)
    tcod.struct_add_property(item, b'frequency', tcod.TYPE_INT, False)
    tcod.struct_add_property(item, b'amt', tcod.TYPE_FLOAT, True)
    tcod.struct_add_flag(item, b"flat")
    tcod.struct_add_list_property(item, b'tags', tcod.TYPE_STRING, True)
    tcod.parser_run(parser, filename, ItemParser())
    tcod.parser_delete(parser)
    print(f'{len(ITEM_TEMPLATES)} item templates added.')


def parse_equip(filename):
    parser = tcod.parser_new()
    equip = tcod.parser_new_struct(parser, b'equip')
    stats = tcod.parser_new_struct(parser, b'stats')
    tcod.struct_add_structure(equip, stats)
    tcod.struct_add_property(equip, b'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(equip, b'type', tcod.TYPE_STRING, True)
    tcod.struct_add_property(equip, b'desc', tcod.TYPE_STRING, True)
    tcod.struct_add_property(equip, b'glyph', tcod.TYPE_CHAR, False)
    tcod.struct_add_property(equip, b'col', tcod.TYPE_COLOR, False)
    tcod.struct_add_property(equip, b'frequency', tcod.TYPE_INT, False)
    tcod.struct_add_property(equip, b'damageType', tcod.TYPE_STRING, False)
    tcod.struct_add_property(equip, b'equipType', tcod.TYPE_STRING, False)
    tcod.struct_add_flag(equip, b'material')
    tcod.struct_add_property(equip, b'slot', tcod.TYPE_STRING, False)
    tcod.struct_add_property(stats, b'atp', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'dfp', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'dmg', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'res', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'tou', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'wil', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'pwr', tcod.TYPE_INT, False)
    tcod.struct_add_list_property(equip, b'tags', tcod.TYPE_STRING, True)
    tcod.parser_run(parser, filename, EquipParser())
    tcod.parser_delete(parser)
    print(f'{len(EQ_TEMPLATES)} equipment templates added.')


def parse_materials(filename):
    parser = tcod.parser_new()
    mat = tcod.parser_new_struct(parser, b'material')
    stats = tcod.parser_new_struct(parser, b'stats')
    tcod.struct_add_structure(mat, stats)
    tcod.struct_add_property(mat, b'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(mat, b'col', tcod.TYPE_COLOR, False)
    tcod.struct_add_property(mat, b'hardness', tcod.TYPE_INT, True)
    tcod.struct_add_property(mat, b'frequency', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'atp', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'dfp', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'dmg', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'res', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'tou', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'wil', tcod.TYPE_INT, False)
    tcod.struct_add_property(stats, b'pwr', tcod.TYPE_INT, False)
    tcod.parser_run(parser, filename, MaterialParser())
    tcod.parser_delete(parser)
    print(f'{len(MATERIAL_TEMPLATES)} materials added.')


def parse_maps(filename):
    parser = tcod.parser_new()
    m = tcod.parser_new_struct(parser, b'map')
    connex = tcod.parser_new_struct(parser, b'connections')
    tcod.struct_add_structure(m, connex)
    tcod.struct_add_flag(m, b'light')
    tcod.struct_add_property(m, b'name', tcod.TYPE_STRING, True)
    tcod.struct_add_property(m, b'genType', tcod.TYPE_STRING, True)
    tcod.struct_add_property(m, b'width', tcod.TYPE_INT, True)
    tcod.struct_add_property(m, b'height', tcod.TYPE_INT, True)
    tcod.struct_add_property(connex, b'id', tcod.TYPE_STRING, True)
    tcod.struct_add_property(connex, b'from', tcod.TYPE_STRING, False)
    tcod.struct_add_property(connex, b'to', tcod.TYPE_STRING, False)
    tcod.struct_add_flag(connex, b'twoWay')
    tcod.parser_run(parser, filename, MapParser())
    tcod.parser_delete(parser)
    print(f'{len(MAP_TEMPLATES)} map templates added.')