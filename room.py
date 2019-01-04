from utils import between
from itertools import product


class Orientation:
    INTERIOR = "interior"
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"
    EXTERIOR = "exterior"
    CORNER = "corner"

    @classmethod
    def opposite(cls, direction):
        if direction == cls.NORTH:
            return cls.SOUTH
        elif direction == cls.EAST:
            return cls.WEST
        elif direction == cls.WEST:
            return cls.EAST
        elif direction == cls.SOUTH:
            return cls.NORTH
        else:
            return None


class Room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.x2 = x + w - 1
        self.y2 = y + h - 1
        self.connect_points = None

    def __iter__(self):
        return product(range(self.x, self.x2 + 1), range(self.y, self.y2 + 1))

    def __contains__(self, pt):
        return pt in self.__iter__()

    @property
    def w(self):
        return self.x2 - self.x + 1

    @property
    def h(self):
        return self.y2 - self.y + 1

    def is_corner(self, x, y):
        return (x == self.x or x == self.x2) and (y == self.y or y == self.y2)

    def is_perimeter(self, x, y):
        return (not self.is_corner(x, y)) and (x == self.x or x == self.x2
                                               or y == self.y or y == self.y2)

    def is_interior(self, x, y):
        return x > self.x and x < self.x2 and y > self.y and y < self.y2

    def is_exterior(self, x, y):
        return x < self.x or x > self.x2 or y < self.y or y > self.y2

    @property
    def perimiter(self):
        return [(x, y) for (x, y) in self if self.is_perimeter(x, y)]

    @property
    def interior(self):
        return [(x, y) for (x, y) in self if self.is_interior(x, y)]

    @property
    def center(self):
        x = (self.x + self.x2) // 2
        y = (self.y + self.y2) // 2
        return (x, y)

    def intersect(self, other_rect):
        if self.x > other_rect.x2 or self.x2 < other_rect.x:
            return False
        elif self.y > other_rect.y2 or self.y2 < other_rect.y:
            return False
        elif other_rect.x > self.x2 or other_rect.x2 < self.x:
            return False
        elif other_rect.y > self.y2 or other_rect.y2 < self.y:
            return False
        else:
            return True

    def get_orientation(self, x, y):
        if self.is_corner(x, y):
            return Orientation.CORNER
        elif self.is_interior(x, y):
            return Orientation.INTERIOR
        elif self.is_exterior(x, y):
            return Orientation.EXTERIOR
        elif x == self.x:
            return Orientation.WEST
        elif x == self.x2:
            return Orientation.EAST
        elif y == self.y:
            return Orientation.NORTH
        elif y == self.y2:
            return Orientation.SOUTH

    def carve(self, game_map):
        for x, y in self.interior:
            game_map.set_tile(x, y, 'floor')


class BaseFeature(Room):
    def __init__(self, x, y, w, h):
        Room.__init__(self, x, y, w, h)
        self.connect_points = [(i, j) for (i, j) in self
                               if self.is_perimeter(i, j)]
        self.start = self.center

    @property
    def east(self):
        return [(x, y) for (x, y) in self.perimiter
                if self.get_orientation(x, y) == Orientation.EAST]

    @property
    def west(self):
        return [(x, y) for (x, y) in self.perimiter
                if self.get_orientation(x, y) == Orientation.WEST]

    @property
    def south(self):
        return [(x, y) for (x, y) in self.perimiter
                if self.get_orientation(x, y) == Orientation.SOUTH]

    @property
    def north(self):
        return [(x, y) for (x, y) in self.perimiter
                if self.get_orientation(x, y) == Orientation.NORTH]


class BaseCorridor(BaseFeature):
    def carve(self, game_map):
        BaseFeature.carve(self, game_map)
        x, y = self.start
        game_map.set_tile(x, y, 'floor')
        self.connect_points.remove(self.start)


class EastCorridor(BaseCorridor):
    def __init__(self, x, y, l):
        BaseFeature.__init__(self, x, y - 1, l + 1, 3)
        self.start = (x, y)


class WestCorridor(BaseCorridor):
    def __init__(self, x, y, l):
        BaseFeature.__init__(self, x + 1 - l, y - 1, l + 1, 3)
        self.start = (x, y)


class SouthCorridor(BaseCorridor):
    def __init__(self, x, y, l):
        BaseFeature.__init__(self, x - 1, y, 3, l + 1)
        self.start = (x, y)


class NorthCorridtor(BaseCorridor):
    def __init__(self, x, y, l):
        BaseFeature.__init__(self, x - 1, y + l - 1, 3, l + 1)
        self.start = (x, y)