from base.core.creatures import RunningSprite

hero_idle = ['hero\\knight_idle_spritesheet.png', 6, 1]
hero_run = ['hero\\knight_run_spritesheet.png', 6, 1]


# класс реализующий героя
class Hero(RunningSprite):
    def __init__(self, x, y, speed, group):
        super().__init__(hero_idle, hero_run, x, y, speed, group)
        self.hp = 4
        self.attack = 1

        # переменные, связанные с уклонением
        self.dodge_tick = 0
        self.dodge_limit = 2
        self.dodge_cooldown = 120 * 1.5
        self.dodge_time = 0

    def dodge(self):
        if self.dodge_time == 0:
            self.dodge_tick = 1
            self.dodge_time = 1

    def move(self):
        if 0 < self.dodge_tick <= self.dodge_limit:
            self.speed = [self.speed[0] * 1.8, self.speed[1] * 1.8]
            self.dodge_tick += 1
        else:
            self.dodge_tick = 0
        if self.dodge_time != 0:
            if self.dodge_time >= self.dodge_cooldown:
                self.dodge_time = 0
            else:
                self.dodge_time += 1

        super().move()
