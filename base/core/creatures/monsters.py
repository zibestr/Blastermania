from random import choice
from pygame import Vector2
from base.core.mapping.level_map import DungeonRoom
from base.core.creatures.entities import PotionChest, BulletChest


# класс, отвечающий за производство экземпляров классов монстров
class MonsterFabric:
    def __init__(self, types: dict, sprites_group, rooms):
        self.monster_types = types
        self.sprites_group = sprites_group
        self.container = list()
        self.rooms = rooms
        self.ai = MonsterAI()

    def create_random_monster(self, x, y):
        monster_type = self.monster_types[choice(list(self.monster_types.keys()))]
        self.container.append(monster_type(x, y, [0, 0], self.rooms, self.ai, self.sprites_group))
        return self.container[-1]

    # создаёт 4 сундука
    def create_chests(self, spawn_room):
        rooms = list(filter(lambda elem: isinstance(elem, DungeonRoom), self.rooms))
        for _ in range(4):
            room = choice(rooms)
            while room is spawn_room:
                room = choice(rooms)
            chest = PotionChest(*room.rect.center, self.sprites_group)
            rooms.remove(room)
            self.container.append(chest)
            self.sprites_group.add(chest)
        for _ in range(4):
            room = choice(rooms)
            while room is spawn_room:
                room = choice(rooms)
            chest = BulletChest(*room.rect.center, self.sprites_group)
            rooms.remove(room)
            self.container.append(chest)
            self.sprites_group.add(chest)


# класс с ИИ монстров
class MonsterAI:
    def run(self, monster, hero):
        if hero.is_alive:
            if hero.rect.colliderect(monster.start_room.rect):
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
            else:
                if monster.rect.x != monster.start_x or monster.rect.y != monster.start_y:
                    monster_speed = 0.01
                    start_vector = Vector2(monster.start_x, monster.start_y)
                    monster_vector = Vector2(monster.rect.x, monster.rect.y)
                    movement = start_vector - monster_vector
                    try:
                        movement.normalize()
                    except ValueError:
                        pass
                    movement *= monster_speed
                    monster.speed = movement
                else:
                    monster.speed *= 0
        else:
            monster.speed *= 0

