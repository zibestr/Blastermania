from base.core.creatures import RunningSprite

fly_idle = ['flying creature\\fly_anim_spritesheet.png', 4, 1]
fly_run = ['flying creature\\fly_anim_spritesheet.png', 4, 1]


class FlyingCreature(RunningSprite):
    def __init__(self, x, y, speed, rooms, *group):
        super().__init__(fly_idle, fly_run, x, y, speed, rooms, *group)
        self.hp = 3
        self.attack = 1
