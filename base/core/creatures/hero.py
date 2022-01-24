from base.core.creatures import RunningSprite

hero_idle = ['hero\\knight_idle_spritesheet.png', 6, 1]
hero_run = ['hero\\knight_run_spritesheet.png', 6, 1]


# класс реализующий героя
class Hero(RunningSprite):
    def __init__(self, x, y, speed, group):
        super().__init__(hero_idle, hero_run, x, y, speed, group)
        self.hp = 8
        self.attack = 1

