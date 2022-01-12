import pygame
from base.core.graphics.camera import Camera
from base.core.graphics.pause_menu import MenuUI
from base.core.graphics.hud import HUD
from base.core.mapping.level_map import DungeonLevel

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
        self.game_surface, self.menu_surface, self.hud_surface = self.get_surfaces()
        # камера
        self.camera = Camera(self.game_surface)

    def get_surfaces(self):
        return GameSurface(self.window_sizes, 5, 1), \
               MenuUI(self.window_sizes), \
               HUD()

    # метод для отрисовки всей игры
    def render(self):
        if not self.pause:
            self.display.fill(pygame.Color('white'))
            self.display.blit(self.camera.render_surface(), (0, 0))

    # метод для обработки событий
    def event_handler(self):
        speed = 1
        for event in pygame.event.get():
            # если игра на паузе, то ничего не делает
            if self.pause:
                break
            if event.type == pygame.QUIT:
                self.game_running = False
            keys = pygame.key.get_pressed()
            self.camera.move((keys[pygame.K_d] - keys[pygame.K_a]) * speed,
                             (keys[pygame.K_s] - keys[pygame.K_w]) * speed)

    # метод для запуска игры
    def run(self):
        self.game_running = True
        while self.game_running:
            self.event_handler()
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
        self.surface = pygame.Surface((sizes[0], sizes[1] * 0.93))
        # список со всеми уровнями
        try:
            self.levels = self.generate_dungeon(count_levels, size_compare[map_size],
                                                size_compare[map_size][0] - 4)
        except KeyError:
            self.levels = self.generate_dungeon(count_levels, size_compare[0],
                                                size_compare[0][0] - 4)
        self.current_level = 0

    # метод для генерации уровней в начале игры
    def generate_dungeon(self, count, board_sizes, tries):
        dungeon = list()
        for _ in range(count):
            dungeon.append(DungeonLevel(self.surface.get_size(), board_sizes, tries))
        return dungeon

    # центр поверхности
    @property
    def center(self):
        return self.levels[self.current_level].spawn_point
