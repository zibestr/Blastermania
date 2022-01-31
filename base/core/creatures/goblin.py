from base.core.mapping.level_map import DungeonRoom
from base.core.creatures import RunningSprite

goblin_idle = ['goblin\\goblin_idle_spritesheet.png', 6, 1]
goblin_run = ['goblin\\goblin_run_spritesheet.png', 6, 1]


# ВСЕХ МОНСТРОВ СОЗДАВАТЬ ПО ЭТОМУ ШАБЛОНУ
class Goblin(RunningSprite):
    def __init__(self, x, y, speed, rooms, ai, *group):
        super().__init__(goblin_idle, goblin_run, x, y, speed, rooms, *group)
        self.hp = 2
        self.attack = 1
        self.ai = ai
        self.start_x = x
        self.start_y = y
        index = self.rect.collidelist(list(filter(lambda elem: isinstance(elem, DungeonRoom), self.rooms)))
        self.start_room = list(filter(lambda elem: isinstance(elem, DungeonRoom), self.rooms))[index]

    # для интеллекта
    def update(self):
        super().update()
        self.ai.run(self, self.hero)

    def move(self):
        super().move()
        if self.speed.x != 0 or self.speed.y != 0:
            self.is_running = True
        else:
            self.is_running = False

