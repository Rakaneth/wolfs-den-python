class Effect:
    INFINITE = -1

    def __init__(self, name, owner, stats=dict(), duration=Effect.INFINITE):
        self.name = name
        self.owner = owner
        self.stats = stats
        self.duration = duration

    def on_merge(self, eff):
        pass

    def on_apply(self):
        print(f'Effect {self.name} applied.')

    def on_remove(self):
        print(f'Effect {self.name} removed.')

    def get_stat(self, stat):
        return self.stats.get(stat, 0)

    def set_stat(self, stat, val):
        self.stats[stat] = val

    def on_tick(self, ticks=1):
        if self.duration > 0:
            self.duration -= ticks
            if self.duration <= 0:
                self.on_remove()

    def __str__(self):
        return (
            f'{self.name}\n'
            f'Duration: {"infinite" if self.duration < 0 else self.duration}')


class MightEffect(Effect):
    def __init__(self, amt, owner, duration):
        Effect.__init__(
            self,
            name='might',
            owner=owner,
            stats=dict(str=amt),
            duration=duration)

    def on_merge(self, eff):  #Only the mightiest might applies
        if eff.get_stat('str') > self.get_stat('str'):
            self.set_stat('str', eff.get_stat('str'))
            self.duration = eff.duration


class PoisonEffect(Effect):
    def __init__(self, pwr, owner, duration):
        Effect.__init__(self, name='poison', owner=owner, duration=duration)
        self.pwr = pwr

    def on_merge(self, eff):  #Poison stacks power and duration - very deadly!
        self.pwr += eff.pwr
        self.duration += eff.duration

    def on_apply(self):
        pass  #TODO: Message to player

    def on_remove(self):
        pass  #TODO: Message to player

    def on_tick(self, ticks=1):
        for i in range(ticks):
            pass  #TODO: damage, message to player
        Effect.on_tick(self, ticks)