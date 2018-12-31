from entity import Entity
from world import WORLD


class Command:
    def execute(self, entity: Entity) -> int:
        raise NotImplementedError


class MoveByCommand(Command):
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def execute(self, entity: Entity) -> int:
        m = entity.get_map
        m.set_dirty(entity.x, entity.y)
        entity.x += self.dx
        entity.y += self.dy
        m.set_dirty(entity.x, entity.y)
        return max(100 - entity.get_stat('spd'), 1)


class ExitCommand(Command):
    def execute(self, entity: Entity) -> int:
        return -1


class WaitCommand(Command):
    def execute(self, entity: Entity) -> int:
        return 100