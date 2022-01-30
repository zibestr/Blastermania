from random import choice
from pygame import Vector2

# класс, отвечающий за производство экземпляров классов монстров
from base.core.mapping.level_map import DungeonRoom
from base.core.creatures.entities import Chest


class MonsterFabric:
    def __init__(self, types: dict, sprites_group, rooms, hero):
        self.monster_types = types
        self.sprites_group = sprites_group
        self.container = list()
        self.rooms = rooms
        self.hero = hero
        self.ai = MonsterAI()
    
    def create_random_monster(self, x, y):
        monster_type = self.monster_types[choice(list(self.monster_types.keys()))]
        self.container.append(monster_type(x, y, [0, 0], self.rooms, self.ai, self.hero, self.sprites_group))
        return self.container[-1]
    
    # создаёт 4 сундука
    def create_chests(self, spawn_room):
        for _ in range(4):
            room = choice(list(filter(lambda elem: isinstance(elem, DungeonRoom), self.rooms)))
            while room is spawn_room:
                room = choice(list(filter(lambda elem: isinstance(elem, DungeonRoom), self.rooms)))
            chest = Chest(*room.rect.center, self.sprites_group)
            self.container.append(chest)
            self.sprites_group.add(chest)


# класс с ИИ монстров
class MonsterAI:
    # поставь монстрам такую скорость
    # self.speed = pygame.Vector2(xмонстра - xигрока, yмонстра - yигрока).scale_tolength(скоростьмонстра)
    def run(self, monster, hero):
        monster_speed = 0.01
        hero_vector = Vector2(hero.rect.x, hero.rect.y)
        monster_vector = Vector2(monster.rect.x, monster.rect.y)
        movement = hero_vector - monster_vector
        try:
            movement.normalize()
        except ValueError:
            pass
        movement *= monster_speed
        monster.speed = movement
