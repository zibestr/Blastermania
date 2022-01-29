import random
import pygame
import math
from base.core.mapping.tiles_map import FloorTile

# grey stone
DUNGEON_ROOM_COLOR = (50, 49, 49)


# класс, реализующий уровень подземелья
# имеет свою собственную систему координат, отличную от дисплея pygame
class DungeonLevel:
    def __init__(self, surface_sizes, board_sizes, tries, tiles_group):
        # объекты, расположенные на уровне
        self.objects = list()
        # размеры комнаты на уровне
        self.room_sizes = (math.ceil(min(surface_sizes) / 2),
                           math.ceil(min(surface_sizes) / 2))
        # размеры для вертикального коридора
        self.corridor_sizes = (self.room_sizes[0] / 3,
                               self.room_sizes[1])
        # генерация карты уровня
        self.tries = tries
        self.generator = GeneratorLevel(board_sizes)
        self.level_map = self.generator(self.tries)

        # все тайлы на уровне подземелья
        self.tiles = list()

        # заполняет objects комнатами и коридорами
        self.fill_map(tiles_group)
        # проверяет пустой список объектов на уровне или нет
        # и регенерирует уровень
        while len(self.objects) < 4:
            self.regenerate()
            self.fill_map(tiles_group)
        # точка спавна игрока
        self.spawn_point = (0, 0)
        self.spawn_room = None
        self.set_spawn()

    # заново сгенерировать подземелье
    def regenerate(self):
        self.level_map = self.generator(self.tries)

    # заменить числа на карте на объекты нужны классов
    def fill_map(self, tiles_group):
        for i in range(len(self.level_map)):
            for j in range(len(self.level_map[i])):
                if self.level_map[i][j] == 1 or self.level_map[i][j] == 4:
                    self.objects.append(DungeonRoom(self.room_sizes,
                                                    j * self.room_sizes[1],
                                                    i * self.room_sizes[0],
                                                    tiles_group))
                elif self.level_map[i][j] == 2:
                    self.objects.append(DungeonCorridor(self.corridor_sizes,
                                                        j * self.room_sizes[0] + self.corridor_sizes[0],
                                                        i * self.corridor_sizes[1],
                                                        tiles_group))
                elif self.level_map[i][j] == 3:
                    self.objects.append(DungeonCorridor(self.corridor_sizes[::-1],
                                                        j * self.corridor_sizes[1],
                                                        i * self.room_sizes[0] + self.corridor_sizes[0],
                                                        tiles_group))
                try:
                    self.tiles += self.objects[-1].tiles
                except IndexError:
                    pass

    # ставит точку спавна игрока
    def set_spawn(self):
        # потенциальные места для спавна
        potential_places = list()
        for obj in self.objects:
            if isinstance(obj, DungeonRoom):
                potential_places.append(obj)
        # перемешиваем места для случайного выбора точки спавна
        random.shuffle(potential_places)
        # умножаем размеры на первоначальный масштаб
        self.spawn_point = (potential_places[0].rect.x + potential_places[0].rect.width // 2,
                            potential_places[0].rect.y + potential_places[0].rect.height // 2)
        self.spawn_room = potential_places[0]


# класс для генерации уровня
class GeneratorLevel:
    def __init__(self, sizes):
        self.level_map = [[0] * sizes[0]
                          for _ in range(sizes[1])]

    # генерирует карту уровня
    def generate_level(self, count_tries):
        center = (math.ceil(len(self.level_map[0]) / 2) - 1, math.ceil(len(self.level_map) / 2) - 1)
        # 1 - комната, 2 - вертикальный коридор, 3 - горизонтальный коридор, 4 - тупик, 0 - пустота
        self.level_map[center[0]][center[1]] = 1
        self.level_map = self.dead_end_set(self.set_ways(self.level_map, center))
        # генерирует подземелье с учётом количества попыток
        for _ in range(count_tries):
            self.level_map = self.generate_try(self.level_map)
        # возвращает карту уровня после удаления лишних элементов
        self.level_map = self.del_rooms(self.del_corridors(self.del_random_rooms(self.level_map)))

    # попытка генерации уровня
    # каждая попытка увеличивает уровень путём добавления новых коридоров от тупиков
    def generate_try(self, level):
        for i in range(len(level)):
            for j in range(len(level[i])):
                # если нашёл комнату, то строит от неё коридоры
                if level[i][j] == 4:
                    level = self.dead_end_set(self.set_ways(level, (i, j)))
                    level[i][j] = 1
        return self.set_rooms(level)

    # подсчитывает количество путей в комнату
    def count_ways(self, y, x):
        result = 0
        if y > 0:
            if self.level_map[y - 1][x] == 2:
                result += 1
        if y < len(self.level_map) - 1:
            if self.level_map[y + 1][x] == 2:
                result += 1
        if x > 0:
            if self.level_map[y][x - 1] == 3:
                result += 1
        if x < len(self.level_map[y]) - 1:
            if self.level_map[y][x + 1] == 3:
                result += 1
        return result

    def set_ways(self, level, room_coords):
        # количество генерируемых коридоров
        count_ways = random.randint(1, 4)
        ways = [(room_coords[0] - 1, room_coords[1]),
                (room_coords[0] + 1, room_coords[1]),
                (room_coords[0], room_coords[1] - 1),
                (room_coords[0], room_coords[1] + 1)]
        # очистка невозможных коридоров
        if room_coords[0] - 1 <= 0:
            ways.remove((room_coords[0] - 1, room_coords[1]))
        if room_coords[0] + 1 >= len(level[0]) - 1:
            ways.remove((room_coords[0] + 1, room_coords[1]))
        if room_coords[1] - 1 <= 0:
            ways.remove((room_coords[0], room_coords[1] - 1))
        if room_coords[1] + 1 >= len(level) - 1:
            ways.remove((room_coords[0], room_coords[1] + 1))
        # если коридоров стало меньше, чем планировалось сгенерировать
        if count_ways > len(ways):
            count_ways = random.randint(1, len(ways))
        for _ in range(count_ways):
            # выбор случайного из возможных путей
            if ways:
                random.shuffle(ways)
                level[ways[0][0]][ways[0][1]] = self.type_way(room_coords, ways[0])
                del ways[0]
        return level

    # определяет тип коридора в зависимости от его расположения относительно комнаты
    @staticmethod
    def type_way(room_coords, corridor_coords):
        if room_coords[0] == corridor_coords[0]:
            return 3
        return 2

    # закрывает коридоры тупиками
    @staticmethod
    def dead_end_set(level):
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 2:
                    # проверяет, где находится исходная комната
                    if level[i - 1][j] == 1:
                        level[i + 1][j] = 4
                    elif level[i + 1][j] == 1:
                        level[i - 1][j] = 4
                elif level[i][j] == 3:
                    if level[i][j - 1] == 1:
                        level[i][j + 1] = 4
                    elif level[i][j + 1] == 1:
                        level[i][j - 1] = 4
        return level

    # заменяет тупики на закрытые комнаты
    def set_rooms(self, level):
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 4:
                    if self.count_ways(i, j) > 2:
                        level[i][j] = 1
        return level

    # удаляет лишние коридоры
    @staticmethod
    def del_corridors(level):
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 2:
                    if i > 0:
                        if level[i - 1][j] == 0:
                            level[i][j] = 0
                    if i < len(level) - 1:
                        if level[i + 1][j] == 0:
                            level[i][j] = 0
                if level[i][j] == 3:
                    if j > 0:
                        if level[i][j - 1] == 0:
                            level[i][j] = 0
                    if j < len(level[i]) - 1:
                        if level[i][j + 1] == 0:
                            level[i][j] = 0
        return level

    # находит комнаты с 4 путями
    def find_overflow_rooms(self, level):
        result = list()
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 1:
                    if self.count_ways(i, j) == 4:
                        result.append((i, j))
        return result

    # удаляет четверть комнат с 4 путями случайным образом
    def del_random_rooms(self, level):
        rooms = self.find_overflow_rooms(level)
        random.shuffle(rooms)
        for room in rooms[:len(rooms) // 4 + 1]:
            level[room[0]][room[1]] = 0
        return level

    # удаляет лишние комнаты
    def del_rooms(self, level):
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 1 or level[i][j] == 4:
                    if self.count_ways(i, j) == 0:
                        level[i][j] = 0
        return level

    def __call__(self, count_tries):
        self.generate_level(count_tries)
        return self.level_map


# любой объект на уровне
class ObjectLevel:
    def __init__(self, sizes, x, y):
        self.rect = pygame.Rect(x, y, *sizes)


# класс для комнат подземелья
class DungeonRoom(ObjectLevel):
    def __init__(self, sizes, x, y, tiles_group):
        super().__init__(sizes, x, y)
        self.tiles = list()
        self.generate_tiles(tiles_group)

    # заполняет комнату тайлами пола
    def generate_tiles(self, tiles_group):
        tile_width = self.rect.width // 6 + 1
        tile_height = tile_width
        for i in range(6):
            for j in range(6):
                self.tiles.append(FloorTile(self.rect.x + tile_width * j,
                                            self.rect.y + tile_height * i,
                                            tile_width, tile_height, tiles_group))


# класс для коридоров подземелья
class DungeonCorridor(ObjectLevel):
    def __init__(self, sizes, x, y, tiles_group):
        super().__init__(sizes, x, y)
        self.tiles = list()
        self.generate_tiles(tiles_group)

    # заполняет коридор тайлами пола
    def generate_tiles(self, tiles_group):
        if self.rect.width > self.rect.height:
            lim1 = 2
            lim2 = 6
            tile_width = self.rect.width // lim2 + 1
            tile_height = tile_width
        else:
            lim1 = 6
            lim2 = 2
            tile_height = self.rect.height // lim1 + 1
            tile_width = tile_height
        for i in range(lim1):
            for j in range(lim2):
                self.tiles.append(FloorTile(self.rect.x + tile_width * j,
                                            self.rect.y + tile_height * i,
                                            tile_width, tile_height, tiles_group))
