from base.core.creatures import RunningSprite

slime_idle = ['slime\\slime_idle_spritesheet.png', 6, 1]
slime_run = ['slime\\slime_run_spritesheet.png', 6, 1]


class Slime(RunningSprite):
    def __init__(self, x, y, speed, *group):
        super().__init__(slime_idle, slime_run, x, y, speed, *group)
        self.hp = 1
