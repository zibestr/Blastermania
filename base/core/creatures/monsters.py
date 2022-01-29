from random import choice


# класс, отвечающий за производство экземпляров классов монстров
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


# класс с ИИ монстров
class MonsterAI:
    def run(self, room_rect, monster_rect, hero_rect):
        pass
