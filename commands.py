from entity import Entity


class Command:
    def execute(self, entity: Entity) -> int:
        raise NotImplementedError


class MoveByCommand(Command):
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def execute(self, entity: Entity) -> int:
        entity.x += self.dx
        entity.y += self.dy
        return max(100 - entity.get_stat('spd'), 1)


class ExitCommand(Command):
    def execute(self, entity: Entity) -> int:
        return -1


class WaitCommand(Command):
    def execute(self, entity: Entity) -> int:
        return 100