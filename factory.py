import parsers
import tcod
import room
from entity import Creature, Item, Equipment
from gamemap import GameMap
from random import choice, shuffle, randint, choices


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
    base_map.cave_iteration(4)
    base_map.wall_wrap()
    base_map.set_regions()
    base_map.close_small_regions(20)
    base_map.connect_regions()
    return base_map


def rooms(m_id, name, width, height, wall_color, floor_color, light=True):
    base_map = GameMap(width, height, m_id, name, wall_color, floor_color,
                       light)
    base_map.all_tile('wall')
    MAX_ROOMS = 50
    MIN_ROOM_SIZE = 5
    MAX_ROOM_SIZE = 10
    room_list = []

    for _ in range(MAX_ROOMS):
        valid = True
        x = randint(1, width - MIN_ROOM_SIZE)
        y = randint(1, height - MIN_ROOM_SIZE)
        w = randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        h = randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        room_cand = room.Room(x, y, w, h)

        if room_list:
            for room in room_list:
                too_big = room_cand.x2 >= width or room_cand.y2 >= height
                if room_cand.intersect(room) or too_big:
                    valid = False
                    break

        if valid:
            room_list.append(room_cand)
            base_map.carve_room(room_cand)

    shuffle(room_list)
    room_from = room_list.pop()
    path = tcod.path.AStar(base_map.move_cost, 0)
    base_map.set_regions()

    while room_list:
        #TODO: Place items/monsters
        room_to = room_list.pop()
        fx, fy = room_from.center
        tx, ty = room_to.center

        def check_path(x, y):
            return path.get_path(x, y, tx, ty)

        base_map.carve_to(fx, fy, tx, ty, 'floor', check_path)
        base_map.set_tile(fx, fy, 'mark')
        base_map.set_tile(tx, ty, 'mark')
        room_from = room_to

    base_map.place_doors()

    base_map.wall_wrap()
    return base_map


def digger(m_id, name, width, height, wall_color, floor_color, light=True):
    base_map = GameMap(width, height, m_id, name, wall_color, floor_color,
                       light)
    base_map.all_tile('wall')

    MAX_FEATURES = 100
    MIN_FEATURE_DIM = 5
    MAX_FEATURE_DIM = 10
    feature_list = []

    for _ in range(MAX_FEATURES):
        if feature_list:
            #get a random feature to connect to
            cur_feature = choice(feature_list)

            if type(cur_feature) is room.BaseFeature:
                selection = 'corr'
            elif type(cur_feature) is room.BaseCorridor:
                selection = 'room' if randint(0, 1) else 'corr'

            #get a random connect point on said feature
            conn_x, conn_y = choice(cur_feature.connection_points)

            #get a start point based on connection orientation
            conn = (conn_x, conn_y)
            if conn in cur_feature.east:
                start_x, start_y = conn_x + 1, conn_y
            elif conn in cur_feature.west:
                start_x, start_y = conn_x - 1, conn_y
            elif conn in cur_feature.north:
                start_x, start_y = conn_x, conn_y - 1
            elif conn in cur_feature.south:
                start_x, start_y = conn_x, conn_y + 1

            #make the feature candidate

            if select == 'corr':
                pass

            #make sure feature doesn't overlap or go out of bounds

            #determine where the connect point is on the feature
            #choose appropriate feature based on orientation
        else:
            #first feature is a room
            x_min = 1
            x_max = width - MAX_FEATURE_DIM
            y_min = 1
            y_max = height - MAX_FEATURE_DIM
            x = randint(x_min, x_max)
            y = randint(y_min, y_max)
            w = randint(MIN_FEATURE_DIM, MAX_FEATURE_DIM)
            h = randint(MIN_FEATURE_DIM, MAX_FEATURE_DIM)
            room_cand = room.BaseFeature(x, y, w, h)
            room_cand.carve(base_map)
