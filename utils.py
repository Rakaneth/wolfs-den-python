def clamp(val, low, high):
    if val < low:
        return low
    elif val > high:
        return high
    else:
        return val


def between(val, low, high):
    return clamp(val, low, high) == val


DIRS = {
    'N': (0, -1),
    'NE': (1, -1),
    'E': (1, 0),
    'SE': (1, 1),
    'S': (0, 1),
    'SW': (-1, 1),
    'W': (-1, 0),
    'NW': (-1, -1),
    'NONE': (0, 0)
}