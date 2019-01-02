import random
import tcod
from numpy import full
from utils import between, clamp
from itertools import product
from queue import Queue


class Tile:
    def __init__(self, glyph, fg=tcod.white, bg=None, see=True, walk=1):
        self.glyph = glyph
        self.see = see
        self.walk = walk
        self.fg = fg
        self.bg = bg


WALL = Tile(178, None, None, False, 0)
FLOOR = Tile(ord(' '))
DOOR_CLOSED = Tile(ord('+'), tcod.white, tcod.sepia, False, 0)
DOOR_OPEN = Tile(ord('/'), tcod.white, tcod.sepia)
STAIRS_UP = Tile(ord('<'), tcod.light_sepia)
STAIRS_DOWN = Tile(ord('>'), tcod.light_sepia)
STAIRS_OUT = Tile(ord('<'), tcod.light_green)
WATER_SHALLOW = Tile(ord('~'), tcod.white, tcod.cyan, True, 5)
WATER_DEEP = Tile(ord('~'), tcod.white, tcod.blue, True, 0)
NULL_TILE = Tile(0, None, None, False, 0)


class MapConnection:
    def __init__(self, map_id, to_x, to_y):
        self.map_id = map_id
        self.to_x = to_x
        self.to_y = to_y


class GameMap(tcod.map.Map):
    TILES = [
        NULL_TILE, WALL, FLOOR, DOOR_CLOSED, DOOR_OPEN, STAIRS_UP, STAIRS_DOWN,
        STAIRS_OUT, WATER_SHALLOW, WATER_DEEP
    ]
    TILE_ID = {
        'null': 0,
        'wall': 1,
        'floor': 2,
        'door_closed': 3,
        'door_open': 4,
        'stairs_up': 5,
        'stairs_down': 6,
        'stairs_out': 7,
        'water_shallow': 8,
        'water_deep': 9,
    }

    def __init__(self,
                 width,
                 height,
                 id,
                 name,
                 floor_color,
                 wall_color,
                 light=True):
        tcod.map.Map.__init__(self, width, height)
        self.explored = full((height, width), False, dtype=bool)
        self.tiles = full((height, width), 0, dtype=int)
        self.dirty = full((height, width), True, dtype=bool)
        self.carve_cost = full((height, width), 0, dtype=int)
        self.move_cost = full((height, width), 0, dtype=int)
        self.name = name
        self.id = id
        self.floor_color = floor_color
        self.wall_color = wall_color
        self.light = light
        self.connections = {}
        self.floors = set()
        self._flood_table = {}
        self.regions = {}

    def __iter__(self):
        return product(range(self.width), range(self.height))

    def in_bounds(self, x, y):
        return between(x, 0, self.width - 1) and between(y, 0, self.height - 1)

    def on_edge(self, x, y):
        return x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1

    def get_tile(self, x, y):
        if self.in_bounds(x, y):
            idx = self.tiles[y, x]
            return GameMap.TILES[idx]
        else:
            return GameMap.TILES[0]

    def set_tile(self, x, y, tile_name):
        idx = GameMap.TILE_ID[tile_name]
        tile_data = GameMap.TILES[idx]
        self.tiles[y, x] = idx
        self.transparent[y, x] = tile_data.see
        can_walk = tile_data.walk > 0
        self.walkable[y, x] = can_walk
        pt = (x, y)
        self.move_cost[y, x] = tile_data.walk
        if can_walk:
            self.carve_cost[y, x] = 10
            self.floors.add(pt)
        elif pt in self.floors:
            if tile_name == 'wall' and not self.on_edge(x, y):
                self.carve_cost[y, x] = 1
            self.floors.remove(pt)

        if self.on_edge(x, y):
            self.carve_cost[y, x] = 0

    def neighbors(self, x, y, skip_walls=True, four_way=False):
        x_min = max(0, x - 1)
        x_max = min(self.width - 1, x + 1)
        y_min = max(0, y - 1)
        y_max = min(self.height - 1, y + 1)

        return [(xs, ys) for xs in range(x_min, x_max + 1)
                for ys in range(y_min, y_max + 1)
                if not (skip_walls and not self.walkable[ys, xs])
                if not (four_way and (xs != x and ys != y))
                if (xs, ys) != (x, y)]

    def random_floor(self, near_x=None, near_y=None, radius=None):
        if near_x is not None and near_y is not None and radius:
            x_min = max(near_x - radius, 0)
            x_max = min(near_x + radius, self.width - 1)
            y_min = max(near_y - radius, 0)
            y_max = min(near_y + radius, self.height - 1)
            cands = [
                pt for pt in self.floors if between(pt[0], x_min, x_max)
                and between(pt[1], y_min, y_max)
            ]
            if cands:
                return random.choice(cands)
            else:
                print(
                    f'Unable to find space near {(near_x, near_y)} in radius {radius}'
                )
                return None
        else:
            return random.choice(list(self.floors))

    def connect(self, dest_map_id, from_x, from_y, to_x, to_y):
        self.connections[(from_x, from_y)] = MapConnection(
            dest_map_id, to_x, to_y)

    def randomize(self, chance):
        for x, y in self:
            if random.random() < chance:
                self.set_tile(x, y, 'wall')
            else:
                self.set_tile(x, y, 'floor')

    def cave_iteration(self, times):
        for i in range(times):
            print(f'Smoothing caves in {self.name}: iteration {i+1}')
            toWall = []
            toFloor = []
            for x, y in self:
                walls = len([
                    nei for nei in self.neighbors(x, y, False)
                    if not self.get_tile(*nei).walk
                ])
                if walls >= 5:
                    toWall.append((x, y))
                elif walls < 4:
                    toFloor.append((x, y))
            for wx, wy in toWall:
                self.set_tile(wx, wy, 'wall')
            for fx, fy in toFloor:
                self.set_tile(fx, fy, 'floor')

    def wall_wrap(self):
        toWrap = [(x, y) for (x, y) in self if self.on_edge(x, y)]
        for wx, wy in toWrap:
            self.set_tile(wx, wy, 'wall')

    def all_tile(self, tile_name):
        for x, y in self:
            self.set_tile(x, y, tile_name)

    def set_dirty(self, x, y):
        self.dirty[y, x] = True

    def clean(self, x, y):
        self.dirty[y, x] = False

    def is_dirty(self, x, y):
        return self.dirty[y, x]

    def explore(self, x, y):
        self.explored[y, x] = True

    def is_explored(self, x, y):
        return self.explored[y, x]

    def update_fov(self, entity):
        if entity.is_player:
            for x, y in [(xs, ys) for (xs, ys) in self if self.fov[ys, xs]]:
                self.set_dirty(x, y)
        vis = entity.get_stat('vision')
        self.compute_fov(entity.x, entity.y, vis)
        entity.fov = self.fov
        if entity.is_player:
            for x2, y2 in [(xxs, yys) for (xxs, yys) in self
                           if self.fov[yys, xxs]]:
                self.explore(x2, y2)
                self.set_dirty(x2, y2)

    def flood(self, x, y, region_id):
        q = Queue()
        q.put((x, y))
        result = [(x, y)]
        print(f'Flooding about point {(x, y)} in region {region_id}')
        self._flood_table[(x, y)] = region_id
        while not q.empty():
            next_x, next_y = q.get()
            neis = self.neighbors(next_x, next_y, True, True)
            for nei in neis:
                if self._flood_table.get(nei) is not None:
                    continue
                else:
                    self._flood_table[nei] = region_id
                    result.append(nei)
                    q.put(nei)
        return result

    def set_regions(self):
        self.regions = {}
        self._flood_table = {}
        region_id = 0
        for x, y in self.floors:
            if self._flood_table.get((x, y)) is None:
                print(f'Getting region {region_id} in {self.name}')
                self.regions[region_id] = self.flood(x, y, region_id)
                region_id += 1

    def close_small_regions(self, min_region_size):
        print(
            f'Removing regions smaller than {min_region_size} tiles from {self.name}'
        )
        for region in self.regions.values():
            if len(region) < min_region_size:
                for x, y in region:
                    self.set_tile(x, y, 'wall')
        self.set_regions()

    def can_walk(self, x, y):
        return self.move_cost[y, x] > 0

    def can_see(self, x, y):
        return self.transparent[y, x]
