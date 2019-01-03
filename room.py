from utils import between
from itertools import product


class Room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.x2 = x + w - 1
        self.y2 = y + h - 1

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
