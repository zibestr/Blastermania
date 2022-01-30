from base.core.creatures import RunningSprite

slime_idle = ['slime\\slime_idle_spritesheet.png', 6, 1]
slime_run = ['slime\\slime_run_spritesheet.png', 6, 1]


class Slime(RunningSprite):
    def __init__(self, x, y, speed, rooms, ai, hero, *group):
        super().__init__(slime_idle, slime_run, x, y, speed, rooms, *group)
        self.hp = 1
        self.attack = 1
        self.ai = ai
        self.hero = hero

    # для интеллекта
    def update(self):
        super().update()
        self.ai.run(self, self.hero)
