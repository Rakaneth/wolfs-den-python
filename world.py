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
        self.cur_map = 'none'

    @property
    def cur_map(self):
        return self.maps[self.cur_map]

    @property
    def cur_things(self):
        return [
            thing for thing in self.things.values()
            if thing.map_id == self.cur_map
        ]

    def things_at(self, x, y):
        return [
            thing for thing in self.cur_things if (thing.x, thing.y) == (x, y)
        ]

    def add_entity(self, entity):
        self.things[entity.id] = entity

    def remove_entity(self, entity):
        del self.things[entity.id]

    def set_cur_map(self, map_id):
        self.cur_map = map_id