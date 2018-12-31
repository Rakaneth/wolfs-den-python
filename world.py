import random
from datetime import datetime


class World:
    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
        else:
            random.seed(datetime.now())
        self.things = {}
        self.maps = {}
        self.cur_map_id = 'none'
        self.hud_dirty = True
        self.player = None

    @property
    def cur_map(self):
        return self.maps[self.cur_map_id]

    @property
    def cur_things(self):
        return [
            thing for thing in self.things.values()
            if thing.map_id == self.cur_map_id
        ]

    def things_at(self, x, y):
        return [
            thing for thing in self.cur_things if (thing.x, thing.y) == (x, y)
        ]

    def add_map(self, game_map):
        self.maps[game_map.id] = game_map

    def add_entity(self, entity):
        self.things[entity.id] = entity

    def remove_entity(self, entity):
        del self.things[entity.id]

    def set_cur_map(self, map_id):
        self.cur_map_id = map_id


WORLD = World(0xDEADBEEF)