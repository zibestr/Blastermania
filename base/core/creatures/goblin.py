from base.core.creatures import RunningSprite

goblin_idle = ['goblin\\goblin_idle_spritesheet.png', 6, 1]
goblin_run = ['goblin\\goblin_run_spritesheet.png', 6, 1]


# ВСЕХ МОНСТРОВ СОЗДАВАТЬ ПО ЭТОМУ ШАБЛОНУ
class Goblin(RunningSprite):
    def __init__(self, x, y, speed, rooms, ai, hero, *group):
        super().__init__(goblin_idle, goblin_run, x, y, speed, rooms, *group)
        self.hp = 2
        self.attack = 1
        self.ai = ai
        self.hero = hero

    # для интеллекта
    def update(self):
        super().update()
        self.ai.run(self, self.hero)
