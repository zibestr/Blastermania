import os
import pygame
import time


# метод загрузки изображения
def load_image(name):
    fullname = os.path.join(f'{os.getcwd()}\\base\\core\\graphics\\ui', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    return image


# класс реализующий интерфейс игрока
class HUD:
    def __init__(self, sizes, hero):
        self.surface = pygame.Surface((sizes[0], sizes[1])).convert_alpha()
        self.health_ui = load_image('health_ui.png')
        self.heath_bar = None
        self.dodge_ui = load_image('dodge_icon.png')
        self.bullets_ui = load_image('spentshell.png')
        self.hero = hero
        self.timer = time.time()
        self.time_count = time.strftime("%M:%S", time.gmtime(time.time() - self.timer))

    # рендер полоски здоровья
    def health_bar(self):
        sizes = self.health_ui.get_rect().w, self.health_ui.get_rect().h
        scale = self.surface.get_width() / 4.0 / sizes[0]
        pygame.draw.rect(self.surface, pygame.Color(80, 0, 0), (10 + int(19 * scale), 20,
                                                                 int(self.hero.max_hp * sizes[0] / 5.3 * scale),
                                                                 int(sizes[1] / 2 * scale)))
        pygame.draw.rect(self.surface, pygame.Color(150, 0, 0), (10 + int(19 * scale), 20,
                                                                 int(self.hero.hp * sizes[0] / 5.3 * scale),
                                                                 int(sizes[1] / 2 * scale)))
        self.heath_bar = pygame.transform.scale(self.health_ui, (scale * sizes[0],
                                                                 scale * sizes[1]))
        self.surface.blit(self.heath_bar, (10, 10))

    # рендер счетчика времени
    def time_counter(self, is_win, is_game_over):
        font = pygame.font.Font(f'{os.getcwd()}\\base\\core\\graphics\\fonts\\Pixeboy.ttf',
                                self.surface.get_width() // 30)
        if not is_win:
            self.time_count = time.strftime("%M:%S", time.gmtime(time.time() - self.timer))
        count = font.render(f'{self.time_count}', True,
                            (255, 255, 255))
        self.surface.blit(count,
                          (30, 9 * self.health_ui.get_height()))

    # рендер иконки отката уклонения
    def dodge_icon(self):
        sizes = self.surface.get_width() * 0.05, self.surface.get_width() * 0.05
        dodge_surface = pygame.transform.scale(self.dodge_ui, sizes).convert_alpha()
        if self.hero.dodge_time != 0:
            dodge_surface.set_alpha(80)
            font = pygame.font.Font(f'{os.getcwd()}\\base\\core\\graphics\\fonts\\Pixeboy.ttf',
                                    self.surface.get_width() // 25)
            timer = font.render(str(round((self.hero.dodge_cooldown - self.hero.dodge_time) / 120, 1)), True,
                                (255, 255, 255))
            dodge_surface.blit(timer, (8, 8))

        self.surface.blit(dodge_surface,
                          (self.surface.get_width() * 0.05 + self.heath_bar.get_width(), 10))

    def bullets_counter(self):
        sizes = self.surface.get_width() * 0.04, self.surface.get_width() * 0.04
        bullet_image = pygame.transform.scale(self.bullets_ui, sizes)
        font = pygame.font.Font(f'{os.getcwd()}\\base\\core\\graphics\\fonts\\Pixeboy.ttf',
                                self.surface.get_width() // 30)
        count = font.render(f'{self.hero.amount_bullets} / {self.hero.max_bullets}', True,
                            (255, 255, 255))
        self.surface.blit(count,
                          (30, 6 * self.health_ui.get_height()))
        self.surface.blit(bullet_image,
                          (40 + count.get_width(), 5 * self.health_ui.get_height()))

    def render(self, is_win, is_game_over):
        self.surface.fill([0, 0, 0, 0])
        self.health_bar()
        self.dodge_icon()
        self.bullets_counter()
        self.time_counter(is_win, is_game_over)
        return self.surface
