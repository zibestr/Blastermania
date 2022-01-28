import pygame

from base.core.creatures.fly_creature import FlyingCreature
from base.core.creatures.goblin import Goblin
from base.core.creatures.monsters import MonsterFabric
from base.core.creatures.slime import Slime
from base.core.graphics.camera import Camera
from base.core.graphics.pause_menu import MenuUI
from base.core.graphics.hud import HUD
from base.core.mapping.level_map import DungeonLevel, DungeonRoom
from base.core.creatures.hero import Hero
from base.core.creatures import SpritesCameraGroup
from random import choices, randint

# инициализируем pygame

pygame.init()


# основной класс проекта (ВНОСИТЬ ИЗМЕНЕНИЯ ТОЛЬКО С СОГЛАСИЯ ТИМЛИДА!!!)
class Game:
    def __init__(self, window_sizes, fps):
        # количество кадров в секунду
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.game_running = False
        # размеры окна
        self.window_sizes = window_sizes
        # переменная, которая показывает - на паузе игра или нет
        self.pause = False
        # объект окна pygame
        self.display = pygame.display.set_mode(window_sizes)
        pygame.display.set_caption('Blastermania')
        # поверхности для отрисовки
        # game_surface - поверхность с основной игрой
        # menu_surface - поверхность для отрисовки меню
        # hud_surface - поверхность для отрисовки интерфейса игрока
        self.game_surface = GameSurface(self.window_sizes, 1, 1)
        self.menu_surface = MenuUI(self.window_sizes)
        self.hud_surface = HUD(self.window_sizes, self.game_surface.hero)
        # камера
        self.camera = Camera(self.game_surface)
        # курсор
        pygame.mouse.set_visible(False)
        self.cursor_image = pygame.image.load('D:\\git_lab3_lesson2\\Blastermania\\base\\core\\graphics\\ui'
                                              '\\crosshair_1.png').convert_alpha()
        # музыка
        self.music_files = ['DarkChapel.mp3', 'BehindEnemyStripes.mp3',
                            'CarefreeSpirit.mp3', 'DunesOfTheLost.mp3',
                            'HiddenUtopia.mp3', 'Spinetingler.mp3']

    # метод для проигрывания музыки
    def play_background_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(f'D:\\git_lab3_lesson2\\Blastermania\\base'
                                    f'\\music\\background\\{choices(self.music_files)[0]}')
            pygame.mixer.music.play(loops=1)
            pygame.mixer.music.set_volume(0.1)

    # метод для отрисовки всей игры
    def render(self):
        if not self.pause:
            self.display.fill(pygame.Color('white'))
            # отрисовка основной поверхности
            self.display.blit(self.camera.render_surface(), (0, 0))
            # отрисовка интерфейса игрока
            self.display.blit(self.hud_surface.render(), (0, 0))
            # заменяет курсор
            self.display.blit(pygame.transform.scale(self.cursor_image,
                                                     (self.window_sizes[0] * 0.03,
                                                      self.window_sizes[0] * 0.03)),
                              (pygame.mouse.get_pos()))

    # метод для обработки событий
    def event_handler(self):
        speed = 2

        for event in pygame.event.get():
            # если игра на паузе, то ничего не делает
            if self.pause:
                break
            if event.type == pygame.QUIT:
                self.game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    self.game_surface.hero.dodge()
            keys = pygame.key.get_pressed()
            if abs(keys[pygame.K_d] - keys[pygame.K_a]) > 0 or abs(keys[pygame.K_s] - keys[pygame.K_w]) > 0:
                self.game_surface.hero.is_running = True
            else:
                self.game_surface.hero.is_running = False
            self.game_surface.hero.speed = (keys[pygame.K_d] - keys[pygame.K_a]) * speed, \
                                           (keys[pygame.K_s] - keys[pygame.K_w]) * speed

    # метод для обновления всех процессов в игре
    def update(self):
        if not self.pause:
            self.game_surface.update_level()
            self.camera.move()

    # метод для запуска игры
    def run(self):
        self.game_running = True
        while self.game_running:
            self.play_background_music()
            self.event_handler()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()


# поверхность для основной игры
# map_size: 0 - маленькая карта (подземелье 8 на 8 ячеек),
# 1 - средняя карта (подземелье 10 на 10),
# 2 - большая карта (подземелье 15 на 15)
class GameSurface:
    def __init__(self, sizes, count_levels, map_size):
        size_compare = {
            0: (8, 8),
            1: (10, 10),
            2: (15, 15)
        }
        self.surface = pygame.Surface((sizes[0], sizes[1]))
        # создаёт группы спрайтов
        self.creatures_sprites = SpritesCameraGroup()
        self.tiles_sprites = SpritesCameraGroup()
        # генератор монстров
        self.monsters = MonsterFabric({'goblin': Goblin, 'slime': Slime, 'fly': FlyingCreature}, self.creatures_sprites)
        # список со всеми уровнями
        try:
            self.levels = self.generate_dungeon(count_levels, size_compare[map_size],
                                                size_compare[map_size][0] - 4)
        except KeyError:
            self.levels = self.generate_dungeon(count_levels, size_compare[0],
                                                size_compare[0][0] - 4)
        self.current_level = 0

        # генерирует монстров
        self.generate_monsters(1, 2)

        # создаёт игрока
        self.hero = Hero(self.center[0], self.center[1], [0, 0], self.creatures_sprites)
        self.creatures_sprites.add(self.hero)
        self.tiles_sprites.add(*self.levels[self.current_level].tiles)
        # добавляет группы спрайтов на уровни
        self.levels[self.current_level].objects.append(self.creatures_sprites)
        self.levels[self.current_level].objects.append(self.tiles_sprites)

    # обновляет текущий уровень
    def update_level(self):
        for obj in self.levels[self.current_level].objects:
            try:
                obj.update()
            except AttributeError:
                pass

    # метод для генерации уровней в начале игры
    def generate_dungeon(self, count, board_sizes, tries):
        dungeon = list()
        for _ in range(count):
            dungeon.append(DungeonLevel(self.surface.get_size(), board_sizes, tries, self.tiles_sprites))
        return dungeon

    # метод для генерации монстров
    def generate_monsters(self, min_count, max_count):
        for obj in self.levels[self.current_level].objects:
            if isinstance(obj, DungeonRoom):
                if obj is not self.levels[self.current_level].spawn_room:
                    for _ in range(randint(min_count, max_count)):
                        x = randint(obj.rect.x + 10, obj.rect.right - 50)
                        y = randint(obj.rect.y + 10, obj.rect.bottom - 50)
                        monster = self.monsters.create_random_monster(x, y)
                        self.creatures_sprites.add(monster)

    # центр поверхности
    @property
    def center(self):
        return self.levels[self.current_level].spawn_point
