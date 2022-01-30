from random import choice


# класс, отвечающий за производство экземпляров классов монстров
from base.core.mapping.level_map import DungeonRoom
from base.core.creatures.entities import Chest


class MonsterFabric:
    def __init__(self, types: dict, sprites_group, rooms):
        self.monster_types = types
        self.sprites_group = sprites_group
        self.container = list()
        self.rooms = rooms

    def create_random_monster(self, x, y):
        monster_type = self.monster_types[choice(list(self.monster_types.keys()))]
        self.container.append(monster_type(x, y, [0, 0], self.rooms, self.sprites_group))
        return self.container[-1]

    # создаёт 4 сундука
    def create_chests(self):
        for _ in range(4):
            room = choice(list(filter(lambda elem: isinstance(elem, DungeonRoom), self.rooms)))
            chest = Chest(*room.rect.center, self.sprites_group)
            self.container.append(chest)
            self.sprites_group.add(chest)


# класс с ИИ монстров
class MonsterAI:
    def run(self, room_rect, monster_rect, hero_rect):
        pass
