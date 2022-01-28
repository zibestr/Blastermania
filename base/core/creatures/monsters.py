from random import choice


# класс, отвечающий за производство экземпляров классов монстров
class MonsterFabric:
    def __init__(self, types: dict, sprites_group):
        self.monster_types = types
        self.sprites_group = sprites_group
        self.container = list()

    def create_random_monster(self, x, y):
        monster_type = self.monster_types[choice(list(self.monster_types.keys()))]
        self.container.append(monster_type(x, y, [0, 0], self.sprites_group))
        return self.container[-1]


# класс с ИИ монстров
class MonsterAI:
    def run(self, room_rect, monster_rect, hero_rect):
        pass
