import parsers
from entity import Creature, Item, Equipment
from gamemap import GameMap


def seed(entity, map_id, x=None, y=None):
    entity.map_id = map_id
    if x is None or y is None:
        x, y = entity.get_map.random_floor()
    entity.move(x, y)


def creature_from_template(buildID, mapID=None, start_x=None, start_y=None):
    temp = parsers.CREATURE_TEMPLATES.get(buildID)
    assert temp, f'BuildID {buildID} not in creature templates'
    foetus = Creature(
        name=temp.name,
        desc=temp.desc,
        glyph=temp.glyph,
        color=temp.color,
        stats=temp.stats,
        tags=temp.tags)
    foetus.heal()
    if mapID:
        seed(foetus, mapID, start_x, start_y)
        foetus.get_map.update_fov(foetus)
    return foetus


def equip_from_template(buildID,
                        matID=None,
                        mapID=None,
                        start_x=None,
                        start_y=None):
    temp = parsers.EQ_TEMPLATES.get(buildID)
    if matID:
        mat = parsers.MATERIAL_TEMPLATES.get(matID)
    else:
        mat = None
    assert temp, f'BuildID {buildID} not in equip templates'
    mould = Equipment(
        name=temp.name,
        desc=temp.desc,
        glyph=temp.glyph,
        color=temp.color,
        slot=temp.slot,
        stats=temp.stats,
        tags=temp.tags)
    mould.damage_type = temp.damage_type

    if temp.material:
        str_material = '<material>'
        assert matID, f'{temp.name} must be made of a material, none given'
        assert mat, f'{matID} not in material templates'
        mould.name = f'{mat.name} {mould.name}'
        mould.desc = mould.desc.replace(str_material, mat.name)
        mould.color = mat.color
        stat_set = getattr(mat, temp.equip_type)
        mould.hardness = mat.hardness

        for k, v in stat_set.items():
            mould.set_stat(k, mould.get_stat(k) + v)

    if mapID:
        seed(mould, mapID, start_x, start_y)
    return mould


def item_from_template(buildID, mapID=None, start_x=None, start_y=None):
    temp = parsers.ITEM_TEMPLATES.get(buildID)
    assert temp, f'BuildID {buildID} not in item templates'
    mould = Item(
        name=temp.name,
        desc=temp.desc,
        glyph=temp.glyph,
        color=temp.color,
        amt=temp.amt,
        flat=temp.flat,
        typ=temp.type,
        tags=temp.tags)
    if mapID:
        seed(mould, mapID, start_x, start_y)
    return mould


def caves(m_id, name, width, height, wall_color, floor_color, light=True):
    base_map = GameMap(width, height, m_id, name, wall_color, floor_color,
                       light)
    base_map.randomize(0.5)
    base_map.cave_iteration(5)
    base_map.wall_wrap()
    return base_map
